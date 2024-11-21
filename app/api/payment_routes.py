from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse
import stripe
from bitcoinlib.wallets import Wallet, wallet_create_or_open
import httpx
import asyncio
from typing import Optional
from datetime import datetime
from decimal import Decimal
from ..config.payment_config import (
    STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET,
    BITCOIN_NETWORK, BITCOIN_WALLET_NAME, BITCOIN_ACCOUNT_NAME,
    BITCOIN_WALLET_PASSPHRASE, BITCOIN_MASTER_KEY, BITCOIN_API_KEY
)

router = APIRouter()
stripe.api_key = STRIPE_SECRET_KEY

# Keep track of payment addresses and their associated orders
bitcoin_payments = {}

async def get_btc_price() -> float:
    """Get current BTC/USD price from CoinGecko."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.coingecko.com/v3/simple/price",
                params={"ids": "bitcoin", "vs_currencies": "usd"}
            )
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to fetch BTC price")
            data = response.json()
            return float(data["bitcoin"]["usd"])
    except Exception as e:
        print(f"Error fetching BTC price: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch BTC price")

def create_or_load_wallet():
    """Create or load Bitcoin wallet with proper error handling."""
    try:
        # First try to load existing wallet
        try:
            wallet = Wallet(
                BITCOIN_WALLET_NAME,
                password=BITCOIN_WALLET_PASSPHRASE
            )
            print(f"Loaded existing wallet: {BITCOIN_WALLET_NAME}")
        except Exception as e:
            print(f"Creating new wallet: {BITCOIN_WALLET_NAME}")
            # If loading fails, create new wallet
            wallet = Wallet.create(
                BITCOIN_WALLET_NAME,
                keys=BITCOIN_MASTER_KEY if BITCOIN_MASTER_KEY else None,
                network=BITCOIN_NETWORK,
                password=BITCOIN_WALLET_PASSPHRASE,
                witness_type='segwit'  # Use modern address format
            )
        
        # Make sure wallet is using correct network
        if wallet.network.name != BITCOIN_NETWORK:
            raise ValueError(f"Wallet network mismatch: {wallet.network.name} != {BITCOIN_NETWORK}")
        
        return wallet
    except Exception as e:
        print(f"Error creating/loading wallet: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Wallet error: {str(e)}")

async def monitor_bitcoin_payment(address: str, expected_amount: float, order_id: str):
    """Background task to monitor Bitcoin payment."""
    try:
        wallet = create_or_load_wallet()
        max_confirmations = 6
        check_interval = 60  # seconds
        max_attempts = 24 * 60  # 24 hours worth of checks
        attempts = 0

        while attempts < max_attempts:
            try:
                wallet.scan()
                transactions = wallet.transactions()
                
                for tx in transactions:
                    if tx.status == 'confirmed' and tx.confirmations >= max_confirmations:
                        # Check if this transaction involves our address
                        for output in tx.outputs:
                            if output.address == address and \
                               float(output.value) >= float(expected_amount):
                                # Payment confirmed
                                bitcoin_payments[address]["status"] = "confirmed"
                                bitcoin_payments[address]["transaction_id"] = tx.txid
                                print(f"Payment confirmed for address {address}")
                                return
                
                if bitcoin_payments[address]["status"] == "confirmed":
                    return
                
                attempts += 1
                await asyncio.sleep(check_interval)
            except Exception as e:
                print(f"Error in monitoring loop: {str(e)}")
                await asyncio.sleep(check_interval)
                
    except Exception as e:
        print(f"Error in payment monitor: {str(e)}")
        bitcoin_payments[address]["status"] = "error"
        bitcoin_payments[address]["error"] = str(e)

@router.post("/create-payment-intent")
async def create_payment_intent(data: dict):
    try:
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=data.get("amount"),  # amount in cents
            currency="usd",
            automatic_payment_methods={
                "enabled": True,
            },
            metadata={
                "order_id": data.get("order_id"),
                "customer_email": data.get("customer_email")
            }
        )
        return {"clientSecret": intent.client_secret}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request):
    try:
        # Get the webhook data
        data = await request.body()
        # Verify webhook signature
        event = stripe.Webhook.construct_event(
            payload=data,
            sig_header=request.headers.get('stripe-signature'),
            secret=STRIPE_WEBHOOK_SECRET
        )
        
        # Handle the event
        if event.type == 'payment_intent.succeeded':
            payment_intent = event.data.object
            # Handle successful payment
            # Update order status, send confirmation email, etc.
            print(f"Payment succeeded for order {payment_intent.metadata.order_id}")
        
        return JSONResponse(content={"status": "success"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/create-bitcoin-payment")
async def create_bitcoin_payment(data: dict, background_tasks: BackgroundTasks):
    """Create a new Bitcoin payment request."""
    try:
        # Validate input
        if "amount" not in data or not isinstance(data["amount"], (int, float)):
            raise HTTPException(status_code=400, detail="Invalid amount")
        if "order_id" not in data:
            raise HTTPException(status_code=400, detail="Missing order_id")

        # Initialize wallet
        wallet = create_or_load_wallet()
        
        # Generate new address for payment
        key = wallet.get_key()
        address = key.address
        
        # Get current BTC price and calculate amount
        btc_price = await get_btc_price()
        usd_amount = Decimal(data["amount"]) / Decimal(100)  # Convert cents to dollars
        btc_amount = float(usd_amount / Decimal(btc_price))
        
        # Store payment details
        bitcoin_payments[address] = {
            "order_id": data["order_id"],
            "expected_amount": btc_amount,
            "created_at": datetime.utcnow().isoformat(),
            "status": "pending",
            "transaction_id": None,
            "error": None
        }
        
        # Start monitoring payment in background
        background_tasks.add_task(
            monitor_bitcoin_payment,
            address,
            btc_amount,
            data["order_id"]
        )
        
        return {
            "address": address,
            "amount_btc": btc_amount,
            "amount_usd": float(usd_amount),
            "exchange_rate": btc_price,
            "order_id": data["order_id"],
            "network": BITCOIN_NETWORK
        }
    except Exception as e:
        print(f"Error creating payment: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/check-bitcoin-payment/{address}")
async def check_bitcoin_payment(address: str):
    try:
        # Check if we're tracking this payment
        if address not in bitcoin_payments:
            raise HTTPException(status_code=404, detail="Payment address not found")
        
        payment_info = bitcoin_payments[address]
        
        # If payment is still pending, check for updates
        if payment_info["status"] == "pending":
            wallet = create_or_load_wallet()
            wallet.scan()
            
            # Check for new transactions
            for tx in wallet.transactions():
                if tx.status == 'confirmed':
                    for output in tx.outputs:
                        if output.address == address and \
                           float(output.value) >= float(payment_info["expected_amount"]):
                            payment_info["status"] = "confirmed"
                            payment_info["transaction_id"] = tx.txid
                            break
        
        return {
            "status": payment_info["status"],
            "transaction_id": payment_info["transaction_id"],
            "order_id": payment_info["order_id"],
            "created_at": payment_info["created_at"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/bitcoin-transaction/{txid}")
async def get_bitcoin_transaction(txid: str):
    """Get detailed information about a Bitcoin transaction."""
    try:
        wallet = create_or_load_wallet()
        
        tx = wallet.transaction(txid)
        if not tx:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        return {
            "txid": tx.txid,
            "status": tx.status,
            "confirmations": tx.confirmations,
            "block_height": tx.block_height,
            "block_hash": tx.block_hash,
            "timestamp": tx.date.isoformat() if tx.date else None,
            "amount": sum(o.value for o in tx.outputs),
            "fee": tx.fee
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

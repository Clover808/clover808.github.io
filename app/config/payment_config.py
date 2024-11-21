import os
from dotenv import load_dotenv

load_dotenv()

# Stripe configuration
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')

# Bitcoin configuration
BITCOIN_NETWORK = os.getenv('BITCOIN_NETWORK', 'testnet')
if BITCOIN_NETWORK not in ['testnet', 'mainnet']:
    raise ValueError(f"Invalid BITCOIN_NETWORK value: {BITCOIN_NETWORK}. Must be 'testnet' or 'mainnet'")

BITCOIN_WALLET_NAME = os.getenv('BITCOIN_WALLET_NAME', 'cloverclothes_wallet')
BITCOIN_ACCOUNT_NAME = os.getenv('BITCOIN_ACCOUNT_NAME', 'merchant')

# Required for secure wallet operations
BITCOIN_WALLET_PASSPHRASE = os.getenv('BITCOIN_WALLET_PASSPHRASE')
if not BITCOIN_WALLET_PASSPHRASE:
    raise ValueError("BITCOIN_WALLET_PASSPHRASE must be set")

# Optional: Import existing wallet
BITCOIN_MASTER_KEY = os.getenv('BITCOIN_MASTER_KEY')

# Optional: API key for price data
BITCOIN_API_KEY = os.getenv('BITCOIN_API_KEY')

# CloverClothes - FastAPI E-commerce Platform

A modern e-commerce platform built with FastAPI for fashion, fabrics, and tailoring services.

## Features

- Product browsing and filtering
- Shopping cart functionality
- Multiple payment methods (Stripe and Bitcoin)
- User authentication
- Responsive design
- Real-time payment status monitoring

## Tech Stack

- Backend: FastAPI
- Frontend: HTML, CSS, JavaScript
- Database: PostgreSQL
- Payment Processing: Stripe, Bitcoin
- Deployment: Render

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/CloverClothes-FastAPI.git
cd CloverClothes-FastAPI
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:
```env
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret
BITCOIN_NETWORK=testnet
BITCOIN_WALLET_NAME=your_wallet_name
BITCOIN_ACCOUNT_NAME=your_account_name
BITCOIN_WALLET_PASSPHRASE=your_wallet_passphrase
BITCOIN_MASTER_KEY=your_master_key
BITCOIN_API_KEY=your_api_key
DATABASE_URL=postgresql://user:password@localhost/dbname
```

5. Run the development server:
```bash
uvicorn app.main:app --reload
```

## Deployment

This application is configured for deployment on Render. Follow these steps to deploy:

1. Create a Render account at https://render.com

2. Connect your GitHub repository to Render:
   - Go to your Render dashboard
   - Click "New +" and select "Web Service"
   - Connect your GitHub repository
   - Select the repository you want to deploy

3. Configure your web service:
   - Name: cloverclothes-fastapi
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. Add environment variables:
   - Go to your web service's "Environment" tab
   - Add all the variables from your `.env` file
   - Make sure to keep sensitive information secure

5. Deploy:
   - Click "Create Web Service"
   - Render will automatically build and deploy your application

Your application will be available at `https://cloverclothes-fastapi.onrender.com` (or your custom domain if configured).

## API Documentation

Once the application is running, you can access the API documentation at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Your Name - your.email@example.com
Project Link: https://github.com/yourusername/CloverClothes-FastAPI

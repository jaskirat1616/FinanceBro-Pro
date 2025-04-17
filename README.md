# FinanceBro Pro 📈

![GitHub License](https://img.shields.io/github/license/yourusername/financebro_pro)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![Flask Version](https://img.shields.io/badge/flask-2.3.2-blue)

FinanceBro Pro is a modern, professional financial analysis platform built with Flask that provides real-time market data, technical analysis, sentiment tracking, and AI-powered trading insights.

<p align="center">
  <img src="app/static/img/screenshot.png" alt="FinanceBro Pro Dashboard" width="720">
</p>

## ✨ Features

- **Real-time Market Data**: Track stock prices, volume, and key metrics
- **Technical Analysis**: View moving averages, RSI, MACD, and other indicators
- **Sentiment Analysis**: Monitor market sentiment based on news sources
- **Trade Ideas**: Get data-driven trade recommendations based on technical patterns
- **AI Insights**: Ask questions about stocks and get AI-powered answers via Google Gemini
- **Dark/Light Mode**: Toggle between dark and light themes for optimal viewing
- **Responsive Design**: Mobile-friendly interface works on all devices

## 🚀 Technology Stack

- **Backend**: Flask, Python 3.9+
- **Data Processing**: Pandas, NumPy, yfinance
- **Visualization**: Plotly, Matplotlib
- **AI Integration**: Google Gemini API
- **Caching**: Flask-Caching
- **Production Server**: Gunicorn, Gevent

## 🛠️ Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Local Development Setup

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/financebro_pro.git
   cd financebro_pro
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your configuration
   ```
   FLASK_ENV=development
   FLASK_DEBUG=True
   SECRET_KEY=your-secret-key-here
   GEMINI_API_KEY=your-gemini-api-key  # Optional for AI features
   ```

5. Run the development server
   ```bash
   python run.py
   ```

6. Access the application at http://localhost:5000

## 🚀 Production Deployment

### Using Gunicorn (Recommended)

1. Set environment variables for production
   ```
   FLASK_ENV=production
   FLASK_DEBUG=False
   SECRET_KEY=your-secure-random-key
   ```

2. Run with Gunicorn
   ```bash
   gunicorn -c gunicorn_config.py run:app
   ```

### Docker Deployment

1. Build the Docker image
   ```bash
   docker build -t financebro_pro:latest .
   ```

2. Run the container
   ```bash
   docker run -d -p 5000:5000 --env-file .env.prod --name financebro_pro financebro_pro:latest
   ```

## 🔑 API Keys

FinanceBro Pro uses several external APIs:

- **[Google Gemini API](https://ai.google.dev/)**: For AI-powered insights (optional)
  - Get your API key from the [Google AI Studio](https://makersuite.google.com/)
  - Add it to your `.env` file as `GEMINI_API_KEY=your-key-here`

## 📊 Key Components

- `app/utils.py`: Financial analysis utilities
- `app/routes.py`: API endpoints and page routes
- `app/models.py`: Data models for the application
- `app/templates/`: HTML templates for the UI
- `app/static/`: CSS, JavaScript, and other static assets

## 🎨 Features

### Dashboard
The main dashboard provides a quick overview with:
- Stock price chart with moving averages
- Technical indicators summary
- Recent sentiment analysis
- Quick trade ideas

### Technical Analysis
Detailed stock analysis including:
- Company information
- Key technical indicators
- Moving averages
- RSI analysis

### Trade Ideas
AI-generated trading strategies based on:
- Technical patterns
- Trend analysis
- Overbought/oversold conditions
- Support/resistance levels

### AI Insights
Ask specific questions about a stock to get intelligent answers about:
- Company outlook
- Financial metrics
- Market conditions
- Trading strategies

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📢 Acknowledgments

- [Yahoo Finance](https://finance.yahoo.com/) for financial data
- [Google Gemini](https://ai.google.dev/) for AI capabilities

---

**Disclaimer**: FinanceBro Pro is for educational and informational purposes only. Do not make investment decisions based solely on this tool's recommendations. 
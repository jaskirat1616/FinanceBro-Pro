import yfinance as yf
import pandas as pd
from textblob import TextBlob
import plotly.graph_objects as go
from flask import current_app, g
import newspaper
from datetime import datetime, timedelta
import google.generativeai as genai
import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FinanceAnalyzer:
    def __init__(self):
        # Don't initialize Gemini here
        self.gemini = None
        self._gemini_initialized = False
        self.bro_phrases = [
            "To the moon! 🚀",
            "Diamond hands only 💎🙌",
            "This is the way.",
            "Buy the dip!",
            "Short squeeze incoming!",
            "IV crush gonna wreck these options",
            "FOMO is real right now",
            "This is financial advice (not really)"
        ]
    
    def _initialize_gemini(self):
        """Initializes the Gemini client if not already done."""
        if not self._gemini_initialized:
            self._gemini_initialized = True # Mark as attempted initialization
            api_key = current_app.config.get('GEMINI_API_KEY')
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    self.gemini = genai.GenerativeModel('gemini-2.0-flash-lite')
                    logger.info("Gemini AI client initialized successfully.")
                except Exception as e:
                    logger.error(f"Failed to initialize Gemini AI: {e}")
                    self.gemini = None
            else:
                logger.warning("GEMINI_API_KEY not found in config. AI features disabled.")
                self.gemini = None
    
    def get_bro_phrase(self):
        return random.choice(self.bro_phrases)
    
    def get_stock_data(self, ticker, period='1mo'):
        try:
            logger.info(f"Downloading data for {ticker} (period: {period})...")
            # Explicitly set auto_adjust=True (or False if you prefer unadjusted data)
            # Keep actions=False unless you need dividend/split data separately
            # group_by='ticker' can sometimes cause MultiIndex issues, let's remove it for single ticker downloads
            data = yf.download(ticker, period=period, auto_adjust=True, actions=False) # Removed group_by

            if data.empty:
                logger.warning(f"No data found for ticker: {ticker} with period: {period}")
                return None

            # --- Simplify MultiIndex Columns if present ---
            if isinstance(data.columns, pd.MultiIndex):
                logger.info(f"Detected MultiIndex columns for {ticker}. Simplifying...")
                # If only one ticker was requested, the second level index will be the ticker name
                # We want to keep the first level ('Open', 'High', 'Low', 'Close', 'Volume')
                # Example: columns might be [('Open', 'MSFT'), ('High', 'MSFT'), ...]
                # We want ['Open', 'High', ...]
                try:
                    # Get the first level of the index (Open, High, etc.)
                    data.columns = data.columns.get_level_values(0)
                    logger.info(f"Simplified columns for {ticker}: {data.columns.tolist()}")
                except Exception as idx_err:
                     logger.error(f"Failed to simplify MultiIndex columns for {ticker}: {idx_err}")
                     # Return None or raise error if columns are unusable
                     return None


            # Ensure index is datetime
            data.index = pd.to_datetime(data.index)
            logger.info(f"Successfully downloaded data for {ticker}. Shape: {data.shape}")
            # Log columns AFTER potential simplification
            logger.info(f"Final columns for {ticker} data: {data.columns.tolist()}")
            return data
        except Exception as e:
            logger.error(f"Error in yf.download for {ticker}: {str(e)}", exc_info=True)
            return None
    
    def get_technical_analysis(self, ticker):
        """Calculate technical indicators for a stock."""
        try:
            data = self.get_stock_data(ticker, period='3mo')

            logger.info(f"--- Technical Analysis Start for {ticker} ---")
            if data is None or data.empty:
                logger.warning(f"No valid data obtained for {ticker}. Cannot calculate TA.")
                return None
                
            if not isinstance(data, pd.DataFrame):
                logger.error(f"get_stock_data returned non-DataFrame for {ticker}. Type: {type(data)}")
                return None

            # Create a default result in case calculations fail
            default_result = {
                'current_price': None,
                'sma_20': None,
                'sma_50': None,
                'rsi': None,
                'trend': 'N/A'
            }

            # Get the latest close price
            if 'Close' not in data.columns:
                logger.error(f"'Close' column not found in data for {ticker}. Columns: {data.columns}")
                return default_result
                
            # Get the latest price
            try:
                latest_close = data['Close'].iloc[-1]
                default_result['current_price'] = round(latest_close, 2)
            except (IndexError, KeyError) as e:
                logger.error(f"Error getting latest close price: {e}")
                # Continue with default_result

            # Calculate indicators
            try:
                # Ensure Close is numeric
                close_series = pd.to_numeric(data['Close'], errors='coerce')
                close_series.dropna(inplace=True)

                if close_series.empty:
                    logger.warning(f"Close series became empty after to_numeric/dropna for {ticker}.")
                    return default_result

                # Calculate SMAs
                data['SMA_20'] = close_series.rolling(window=20).mean()
                data['SMA_50'] = close_series.rolling(window=50).mean()

                # Calculate RSI
                delta = close_series.diff()
                gain = delta.where(delta > 0, 0)
                loss = -delta.where(delta < 0, 0)
                avg_gain = gain.rolling(window=14).mean()
                avg_loss = loss.rolling(window=14).mean()
                rs = avg_gain / avg_loss.replace(0, 0.001)  # Avoid division by zero
                rsi = 100 - (100 / (1 + rs))

                # Get latest values
                latest = data.iloc[-1]
                sma_20 = round(latest['SMA_20'], 2) if pd.notna(latest['SMA_20']) else None
                sma_50 = round(latest['SMA_50'], 2) if pd.notna(latest['SMA_50']) else None
                latest_rsi = round(rsi.iloc[-1], 2) if not rsi.empty else None

                # Determine trend
                trend = 'Neutral'
                current_price = default_result['current_price']
                if current_price and sma_20 and sma_50:
                    if current_price > sma_20 > sma_50:
                        trend = 'Bullish'
                    elif current_price < sma_20 < sma_50:
                        trend = 'Bearish'

                return {
                    'current_price': current_price,
                    'sma_20': sma_20,
                    'sma_50': sma_50,
                    'rsi': latest_rsi,
                    'trend': trend
                }
            except Exception as e:
                logger.error(f"Error calculating technical indicators: {e}", exc_info=True)
                return default_result
                
        except Exception as e:
            logger.error(f"Technical analysis failed: {e}", exc_info=True)
            return {
                'current_price': None,
                'sma_20': None, 
                'sma_50': None, 
                'rsi': None, 
                'trend': 'Error'
            }
    
    def get_sentiment_analysis(self, ticker):
        try:
            stock = yf.Ticker(ticker)
            news = None # Initialize news to None
            try:
                # Attempt to fetch news, catching potential request/decode errors
                news = stock.news
            except Exception as news_err:
                 logger.error(f"Error fetching news for {ticker} from yfinance: {news_err}")
                 # Proceed without news if fetching fails

            if not news: # Check if news is None or empty
                logger.info(f"No news found or fetch failed for {ticker}")
                # Return None or a default structure if you prefer
                # For consistency, let's return None if no news is available
                return None

            sentiments = []
            summaries = []
            processed_links = set() # Avoid processing duplicate links if any
            
            for item in news[:5]:  # Analyze top 5 news items
                link = item.get('link')
                title = item.get('title', 'No Title')
                
                if not link or link in processed_links:
                    continue
                processed_links.add(link)
                
                try:
                    # Use newspaper3k to extract better content
                    article = newspaper.Article(link)
                    article.download()
                    article.parse()
                    # Use article text if available and long enough, otherwise fallback to title
                    text_to_analyze = article.text if article.text and len(article.text) > 50 else title
                    
                    if not text_to_analyze: # Skip if no text could be extracted
                         continue
                    
                    analysis = TextBlob(text_to_analyze)
                    sentiments.append(analysis.sentiment.polarity)
                    # Create a summary snippet
                    summary_text = text_to_analyze[:250] + ('...' if len(text_to_analyze) > 250 else '')
                    summaries.append(f"📰 <strong>{title}</strong><br><small>{summary_text}</small>")
                    
                except newspaper.article.ArticleException as article_err:
                     logger.warning(f"Could not process article {link} for {ticker}: {article_err}. Falling back to title.")
                     # Fallback to title only if article parsing fails
                     analysis = TextBlob(title)
                     sentiments.append(analysis.sentiment.polarity)
                     summaries.append(f"📰 <strong>{title}</strong>")
                except Exception as e:
                    logger.error(f"Unexpected error processing news item {link} for {ticker}: {e}")
                    continue # Skip this item
            
            if not sentiments:
                 logger.info(f"No processable news items found for sentiment analysis for {ticker}")
                 return None
            
            avg_sentiment = sum(sentiments) / len(sentiments)
            return {
                'score': round(avg_sentiment, 3), # More precision for sentiment
                'summaries': summaries
            }
        except Exception as e:
            # Use the logger
            logger.error(f"General sentiment analysis error for {ticker}: {str(e)}")
            return None
    
    def generate_price_chart(self, ticker):
        data = self.get_stock_data(ticker, period='3mo')
        if data is None:
            return None
        
        fig = go.Figure()
        
        # Price line
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'],
            name='Price',
            line=dict(color='#1f77b4')
        ))
        
        # SMAs
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'].rolling(window=20).mean(),
            name='20-day SMA',
            line=dict(color='orange', dash='dot')
        ))
        
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'].rolling(window=50).mean(),
            name='50-day SMA',
            line=dict(color='red', dash='dot')
        ))
        
        fig.update_layout(
            title=f'{ticker} Price Analysis (3 Months)',
            xaxis_title='Date',
            yaxis_title='Price ($)',
            template='plotly_white',
            hovermode='x unified',
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            margin=dict(l=40, r=20, t=50, b=40)
        )
        
        return fig.to_html(full_html=False, include_plotlyjs=False)
    
    def generate_trade_ideas(self, ticker):
        """Generate trade ideas based on technical analysis."""
        try:
            # Get technical analysis
            ta = self.get_technical_analysis(ticker)
            
            # Return empty if no technical analysis
            if not ta or ta.get('current_price') is None:
                logger.warning(f"Cannot generate trade ideas without technical analysis for {ticker}")
                return []
                
            ideas = []
            
            # Generate basic ideas based on trend
            current_price = ta.get('current_price')
            trend = ta.get('trend', 'Neutral')
            rsi = ta.get('rsi')
            
            # Add trend-based ideas
            if trend == 'Bullish':
                target_price = round(current_price * 1.05, 2)
                stop_loss = round(current_price * 0.97, 2)
                ideas.append({
                    'strategy': 'Trend Following',
                    'action': 'Buy',
                    'entry': f"${current_price:.2f}",
                    'target': f"${target_price:.2f}",
                    'stop_loss': f"${stop_loss:.2f}",
                    'confidence': 'Medium',
                    'reason': f"Stock is in an uptrend with price above SMA 20 and 50."
                })
            elif trend == 'Bearish':
                target_price = round(current_price * 0.95, 2)
                stop_loss = round(current_price * 1.03, 2)
                ideas.append({
                    'strategy': 'Trend Following',
                    'action': 'Sell',
                    'entry': f"${current_price:.2f}",
                    'target': f"${target_price:.2f}",
                    'stop_loss': f"${stop_loss:.2f}",
                    'confidence': 'Medium',
                    'reason': f"Stock is in a downtrend with price below SMA 20 and 50."
                })
            
            # Add RSI-based ideas
            if rsi is not None:
                if rsi < 30:
                    target_price = round(current_price * 1.07, 2)
                    stop_loss = round(current_price * 0.96, 2)
                    ideas.append({
                        'strategy': 'Oversold Reversal',
                        'action': 'Buy',
                        'entry': f"${current_price:.2f}",
                        'target': f"${target_price:.2f}",
                        'stop_loss': f"${stop_loss:.2f}",
                        'confidence': 'High',
                        'reason': f"RSI at {rsi:.1f} suggests stock is oversold."
                    })
                elif rsi > 70:
                    target_price = round(current_price * 0.93, 2)
                    stop_loss = round(current_price * 1.04, 2)
                    ideas.append({
                        'strategy': 'Overbought Reversal',
                        'action': 'Sell',
                        'entry': f"${current_price:.2f}",
                        'target': f"${target_price:.2f}",
                        'stop_loss': f"${stop_loss:.2f}",
                        'confidence': 'High',
                        'reason': f"RSI at {rsi:.1f} suggests stock is overbought."
                    })
            
            # Add a default/fallback idea if none generated
            if not ideas:
                target_price = round(current_price * 1.05, 2)
                stop_loss = round(current_price * 0.95, 2)
                ideas.append({
                    'strategy': 'Mean Reversion',
                    'action': 'Buy',
                    'entry': f"${current_price:.2f}",
                    'target': f"${target_price:.2f}",
                    'stop_loss': f"${stop_loss:.2f}",
                    'confidence': 'Low',
                    'reason': f"No strong signals, but stock may revert to mean."
                })
            
            # Add a "bro phrase" to a random idea
            if ideas:
                random_idea_index = random.randrange(len(ideas))
                ideas[random_idea_index]['reason'] += f" ({self.get_bro_phrase()})"
            
            return ideas
            
        except Exception as e:
            logger.error(f"Error generating trade ideas: {e}", exc_info=True)
            return []
    
    def get_ai_insights(self, ticker, question=None):
        """Get AI-powered insights using Gemini"""
        self._initialize_gemini() # Ensure client is initialized

        if not self.gemini:
            logger.error(f"Gemini client not available for {ticker} request.")
            # Return a user-friendly error message
            return "Sorry, bro! The AI analysis service isn't available right now. Check the API key configuration or try again later."

        try:
            # Fetch necessary data - reuse existing methods
            ta = self.get_technical_analysis(ticker)
            sentiment_data = self.get_sentiment_analysis(ticker)
            company_info = self.get_company_info(ticker) # Fetch company info too

            # --- Prepare context strings, handling None cases ---
            price_str = f"${ta['current_price']:.2f}" if ta and ta.get('current_price') is not None else "N/A"
            trend_str = ta.get('trend', 'N/A') if ta else "N/A"
            rsi_str = f"{ta['rsi']:.2f}" if ta and ta.get('rsi') is not None else "N/A"

            sentiment_score_str = "N/A"
            sentiment_summary_str = "No recent news summaries available."
            if sentiment_data and sentiment_data.get('score') is not None:
                sentiment_score_str = f"{sentiment_data['score']:.3f}"
                # Extract titles cleanly
                titles = [s.split('<strong>')[1].split('</strong>')[0] for s in sentiment_data.get('summaries', []) if '<strong>' in s]
                if titles:
                    sentiment_summary_str = "; ".join(titles[:3]) # Top 3 titles

            company_sector_str = company_info.get('Sector', 'N/A') if company_info else "N/A"
            company_industry_str = company_info.get('Industry', 'N/A') if company_info else "N/A"

            # --- Build the prompt ---
            prompt = f"""
            You are FinanceBro, an AI assistant providing stock market analysis. Your tone is confident, knowledgeable, and uses occasional, appropriate "finance bro" slang (like 'listen up', 'the play here', 'keep an eye on', 'solid move', 'DYOR') but remains professional overall. Avoid excessive emojis.

            Analyze the stock: {ticker}

            Here's the current data snapshot:
            - Company Sector: {company_sector_str}
            - Company Industry: {company_industry_str}
            - Current Price: {price_str}
            - Recent Trend (SMA-based): {trend_str}
            - RSI (14-day): {rsi_str}
            - Recent News Sentiment Score: {sentiment_score_str}
            - Recent News Headlines: {sentiment_summary_str}

            User Question: "{question if question else "Provide a brief overall analysis and potential outlook."}"

            Instructions:
            1.  Provide a concise analysis (1-3 paragraphs) directly addressing the user's question (or the default analysis if no question was provided).
            2.  **Crucially, base your analysis on the provided data points.** Reference the price, trend, RSI, and sentiment score where relevant to support your points.
            3.  If specific data points are 'N/A', acknowledge that information is missing and adjust the analysis accordingly (e.g., "Without recent sentiment data, focusing on technicals...").
            4.  Maintain the FinanceBro persona throughout.
            5.  **Do NOT give direct financial advice.** Conclude with a clear disclaimer.

            Analysis:
            """

            logger.info(f"Generating AI insight for {ticker} with prompt.")
            # Consider adding a timeout to the API call if needed, though the default might be sufficient
            response = self.gemini.generate_content(prompt)

            # Add the disclaimer automatically
            # Ensure response.text exists and handle potential generation errors/empty responses
            ai_response_text = getattr(response, 'text', "Sorry, the AI couldn't generate a response for this request.")
            ai_response_text += "\n\n*(Disclaimer: This AI analysis is for informational purposes only and not financial advice. Always DYOR - Do Your Own Research!)*"

            return ai_response_text

        except Exception as e:
            logger.error(f"AI insight generation error for {ticker}: {str(e)}", exc_info=True)
            # Provide a more specific user-friendly error message
            return f"Sorry, bro! The AI service encountered an unexpected issue while analyzing {ticker}. Maybe try rephrasing your question? (Error: {str(e)})"
    
    def get_company_info(self, ticker):
        """Fetches basic company information from Yahoo Finance."""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            # Select a subset of useful info to display
            relevant_info = {
                'Company Name': info.get('longName'),
                'Sector': info.get('sector'),
                'Industry': info.get('industry'),
                'Website': info.get('website'),
                'Market Cap': info.get('marketCap'),
                'P/E Ratio': info.get('trailingPE'),
                'Forward P/E': info.get('forwardPE'),
                'Dividend Yield': info.get('dividendYield'),
                '52 Week High': info.get('fiftyTwoWeekHigh'),
                '52 Week Low': info.get('fiftyTwoWeekLow'),
                'Avg Volume': info.get('averageVolume'),
                'Summary': info.get('longBusinessSummary')
            }
            # Format some values
            if relevant_info['Market Cap']:
                relevant_info['Market Cap'] = f"${relevant_info['Market Cap']:,}"
            if relevant_info['Dividend Yield']:
                 relevant_info['Dividend Yield'] = f"{relevant_info['Dividend Yield']*100:.2f}%"
            if relevant_info['Avg Volume']:
                 relevant_info['Avg Volume'] = f"{relevant_info['Avg Volume']:,}"

            # Filter out None values for cleaner display
            return {k: v for k, v in relevant_info.items() if v is not None}

        except Exception as e:
            logger.error(f"Error fetching company info for {ticker}: {str(e)}")
            return None
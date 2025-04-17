from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional, Union, Any
import json

@dataclass
class StockData:
    """Class for representing stock data"""
    ticker: str
    current_price: float
    open_price: Optional[float] = None
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    volume: Optional[int] = None
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    fifty_two_week_high: Optional[float] = None
    fifty_two_week_low: Optional[float] = None
    last_updated: datetime = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the stock data to a dictionary"""
        return {
            'ticker': self.ticker,
            'current_price': self.current_price,
            'open_price': self.open_price,
            'high_price': self.high_price,
            'low_price': self.low_price,
            'volume': self.volume,
            'market_cap': self.market_cap,
            'pe_ratio': self.pe_ratio,
            'dividend_yield': self.dividend_yield,
            'fifty_two_week_high': self.fifty_two_week_high,
            'fifty_two_week_low': self.fifty_two_week_low,
            'last_updated': self.last_updated.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StockData':
        """Create a StockData object from a dictionary"""
        if 'last_updated' in data and isinstance(data['last_updated'], str):
            data['last_updated'] = datetime.fromisoformat(data['last_updated'])
        return cls(**data)

@dataclass
class TechnicalAnalysis:
    """Class for technical analysis data"""
    ticker: str
    current_price: float
    sma_20: Optional[float] = None
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None
    ema_12: Optional[float] = None
    ema_26: Optional[float] = None
    rsi: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    macd_hist: Optional[float] = None
    bollinger_upper: Optional[float] = None
    bollinger_middle: Optional[float] = None
    bollinger_lower: Optional[float] = None
    trend: str = 'Neutral'
    last_updated: datetime = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the technical analysis to a dictionary"""
        return {
            'ticker': self.ticker,
            'current_price': self.current_price,
            'sma_20': self.sma_20,
            'sma_50': self.sma_50,
            'sma_200': self.sma_200,
            'ema_12': self.ema_12,
            'ema_26': self.ema_26,
            'rsi': self.rsi,
            'macd': self.macd,
            'macd_signal': self.macd_signal,
            'macd_hist': self.macd_hist,
            'bollinger_upper': self.bollinger_upper,
            'bollinger_middle': self.bollinger_middle,
            'bollinger_lower': self.bollinger_lower,
            'trend': self.trend,
            'last_updated': self.last_updated.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TechnicalAnalysis':
        """Create a TechnicalAnalysis object from a dictionary"""
        if 'last_updated' in data and isinstance(data['last_updated'], str):
            data['last_updated'] = datetime.fromisoformat(data['last_updated'])
        return cls(**data)

@dataclass
class SentimentAnalysis:
    """Class for sentiment analysis data"""
    ticker: str
    score: float
    magnitude: Optional[float] = None
    recent_news_count: Optional[int] = None
    news_sources: Optional[List[str]] = None
    positive_articles: Optional[int] = None
    negative_articles: Optional[int] = None
    neutral_articles: Optional[int] = None
    last_updated: datetime = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the sentiment analysis to a dictionary"""
        return {
            'ticker': self.ticker,
            'score': self.score,
            'magnitude': self.magnitude,
            'recent_news_count': self.recent_news_count,
            'news_sources': self.news_sources,
            'positive_articles': self.positive_articles,
            'negative_articles': self.negative_articles,
            'neutral_articles': self.neutral_articles,
            'last_updated': self.last_updated.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SentimentAnalysis':
        """Create a SentimentAnalysis object from a dictionary"""
        if 'last_updated' in data and isinstance(data['last_updated'], str):
            data['last_updated'] = datetime.fromisoformat(data['last_updated'])
        return cls(**data)

@dataclass
class TradeIdea:
    """Class for trade ideas"""
    ticker: str
    strategy: str
    target_price: Optional[float] = None
    stop_loss: Optional[float] = None
    entry_price: Optional[float] = None
    risk_reward_ratio: Optional[float] = None
    confidence: Optional[int] = None  # 1-5 scale
    timeframe: Optional[str] = None
    reasoning: Optional[str] = None
    created_at: datetime = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the trade idea to a dictionary"""
        return {
            'ticker': self.ticker,
            'strategy': self.strategy,
            'target_price': self.target_price,
            'stop_loss': self.stop_loss,
            'entry_price': self.entry_price,
            'risk_reward_ratio': self.risk_reward_ratio,
            'confidence': self.confidence,
            'timeframe': self.timeframe,
            'reasoning': self.reasoning,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TradeIdea':
        """Create a TradeIdea object from a dictionary"""
        if 'created_at' in data and isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        return cls(**data)

@dataclass
class CompanyInfo:
    """Class for company information"""
    ticker: str
    name: str
    sector: Optional[str] = None
    industry: Optional[str] = None
    country: Optional[str] = None
    exchange: Optional[str] = None
    currency: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    employees: Optional[int] = None
    founded: Optional[int] = None
    ceo: Optional[str] = None
    headquarters: Optional[str] = None
    last_updated: datetime = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the company info to a dictionary"""
        return {
            'ticker': self.ticker,
            'name': self.name,
            'sector': self.sector,
            'industry': self.industry,
            'country': self.country,
            'exchange': self.exchange,
            'currency': self.currency,
            'website': self.website,
            'description': self.description,
            'employees': self.employees,
            'founded': self.founded,
            'ceo': self.ceo,
            'headquarters': self.headquarters,
            'last_updated': self.last_updated.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CompanyInfo':
        """Create a CompanyInfo object from a dictionary"""
        if 'last_updated' in data and isinstance(data['last_updated'], str):
            data['last_updated'] = datetime.fromisoformat(data['last_updated'])
        return cls(**data)

from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.utils import FinanceAnalyzer
from app.forms import TickerForm, AIQuestionForm
from app import cache
from markdown import markdown # Import markdown

bp = Blueprint('main', __name__)
analyzer = FinanceAnalyzer()

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/dashboard', methods=['GET', 'POST'])
# @cache.cached(timeout=60) # REMOVE cache from the entire route
def dashboard():
    form = TickerForm()
    analysis = None
    chart = None
    ideas = []
    sentiment_data = None
    ticker = request.args.get('ticker', None)  # Get ticker from URL param if available
    
    # Pre-fill form if ticker is provided
    if ticker and request.method == 'GET':
        form.ticker.data = ticker

    if form.validate_on_submit():
        ticker = form.ticker.data.upper()
        # Fetch data (These calls might hit cache from other pages now)
        analysis = analyzer.get_technical_analysis(ticker)
        sentiment_data = analyzer.get_sentiment_analysis(ticker)
        chart = analyzer.generate_price_chart(ticker)
        ideas = analyzer.generate_trade_ideas(ticker)

        if not analysis:
            flash(f'Could not fetch data for {ticker}. Please check the ticker symbol.', 'warning')
        else:
            analysis['ticker'] = ticker
            if sentiment_data:
                analysis['sentiment'] = sentiment_data.get('score')

    # If it's a GET request or POST failed, render potentially empty
    return render_template('dashboard.html',
                         form=form,
                         analysis=analysis,
                         chart=chart,
                         ideas=ideas,
                         sentiment_data=sentiment_data,
                         ticker=ticker) # Pass ticker to template if available

@bp.route('/ai-insights', methods=['GET', 'POST'])
def ai_insights():
    form = TickerForm()
    ai_form = AIQuestionForm()
    insights_html = None
    ticker = request.args.get('ticker', None)  # Get ticker from URL param if available
    
    # Pre-fill form if ticker is provided
    if ticker and request.method == 'GET':
        ai_form.ticker.data = ticker
    
    if ai_form.validate_on_submit():
        ticker = ai_form.ticker.data.upper()
        raw_insights = analyzer.get_ai_insights(ticker, ai_form.question.data)
        insights_html = markdown(raw_insights, extensions=['fenced_code', 'tables'])
    
    return render_template('ai_insights.html',
                         form=form,
                         ai_form=ai_form,
                         insights_html=insights_html,
                         ticker=ticker)

@bp.route('/analysis', methods=['GET', 'POST'])
def analysis():
    form = TickerForm()
    company_info = None
    technical_analysis = None
    ticker = request.args.get('ticker', None)  # Get ticker from URL param if available
    
    # Pre-fill form if ticker is provided
    if ticker and request.method == 'GET':
        form.ticker.data = ticker

    if form.validate_on_submit():
        ticker = form.ticker.data.upper()
        company_info = analyzer.get_company_info(ticker)
        technical_analysis = analyzer.get_technical_analysis(ticker) # Reuse existing method

        if not company_info and not technical_analysis:
            flash(f'Could not fetch detailed analysis data for {ticker}. Please check the ticker symbol.', 'warning')
        elif not company_info:
             flash(f'Could not fetch company info for {ticker}. Displaying technical data only.', 'info')
        elif not technical_analysis:
             flash(f'Could not fetch technical data for {ticker}. Displaying company info only.', 'info')


    return render_template('analysis.html',
                           form=form,
                           ticker=ticker,
                           company_info=company_info,
                           technical_analysis=technical_analysis)

@bp.route('/trade-ideas', methods=['GET', 'POST'])
def trade_ideas():
    form = TickerForm()
    ideas = []
    ticker = request.args.get('ticker', None)  # Get ticker from URL param if available
    
    # Pre-fill form if ticker is provided
    if ticker and request.method == 'GET':
        form.ticker.data = ticker
        # Auto-generate ideas if ticker is provided in URL
        ideas = analyzer.generate_trade_ideas(ticker)
        if not ideas:
            flash(f'Could not generate trade ideas for {ticker}. This might be due to insufficient data.', 'warning')

    if form.validate_on_submit():
        ticker = form.ticker.data.upper()
        ideas = analyzer.generate_trade_ideas(ticker)

        if not ideas:
            flash(f'Could not generate trade ideas for {ticker}. This might be due to insufficient data.', 'warning')

    return render_template('trade_ideas.html',
                           form=form,
                           ticker=ticker,
                           ideas=ideas)
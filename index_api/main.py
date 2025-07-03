from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd
import uvicorn
import sys
import os

# Add the current directory to Python path so it can find plotting.py and html_rendering.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from plotting import create_index_radar_figure, get_company_metric_breakdown, create_dashboard_figures
from html_rendering import render_index_plot_html, render_scatter_dashboard_html

app = FastAPI()


@app.get("/index/f/{ticker}")
def get_index_score(ticker: str):
    df = pd.read_csv("../data/company_financial_indexes.csv")
    df = df[df["ticker"] == ticker.upper()]
    return df.to_dict(orient="records")

@app.get("/index/f/")
def get_all_index_scores():
    df = pd.read_csv("../data/company_financial_indexes.csv")
    return df.to_dict(orient="records")

@app.get("/plot/{ticker}", response_class=HTMLResponse)
def get_index_plot_html(ticker: str):
    """Get an interactive HTML radar plot for a specific ticker"""
    df = pd.read_csv("../data/company_financial_indexes.csv")
    company_df = df[df["ticker"] == ticker.upper()]
    if company_df.empty:
        return f"""
        <html>
            <head><title>No Data Found</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px;">
                <h1>No Data Found</h1>
                <p>No financial data found for ticker: <strong>{ticker.upper()}</strong></p>
                <p><a href="/available-tickers">View available tickers</a></p>
            </body>
        </html>
        """
    fig = create_index_radar_figure(company_df)
    metrics = get_company_metric_breakdown(company_df)
    index_score = company_df.iloc[0]["index_score"] if not company_df.empty else None
    return render_index_plot_html(fig, ticker.upper(), metrics, index_score)

@app.get("/s&p500", response_class=HTMLResponse)
def get_scatter_plot():
    """Get an interactive multi-company radar plot showing financial strengths/weaknesses"""
    df = pd.read_csv("../data/company_financial_indexes.csv")
    dashboard = create_dashboard_figures(df)
    return render_scatter_dashboard_html(dashboard)

@app.get("/available-tickers", response_class=HTMLResponse)
def get_available_tickers():
    """Show all available tickers as clickable links"""
    df = pd.read_csv("../data/company_financial_indexes.csv")
    tickers = sorted(df['ticker'].unique())
    ticker_links = []
    for ticker in tickers:
        ticker_links.append(f'<li><a href="/plot/{ticker}">{ticker}</a></li>')
    html = f"""
    <html>
        <head>
            <title>Available Stock Tickers</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .container {{ max-width: 800px; margin: 0 auto; }}
                ul {{ columns: 3; column-gap: 30px; }}
                li {{ margin: 5px 0; }}
                a {{ text-decoration: none; color: #007bff; }}
                a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Available Stock Tickers</h1>
                <p>Click on any ticker below to view its financial health radar chart:</p>
                <ul>
                    {"".join(ticker_links)}
                </ul>
                <p style="margin-top: 30px; text-align: center;">
                    <em>Total companies: {len(tickers)}</em>
                </p>
            </div>
        </body>
    </html>
    """
    return html

@app.get("/", response_class=HTMLResponse)
def root():
    return """
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FS Chain API: Valuation as a Service</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            line-height: 1.6;
            color: #333;
            background: #fafafa;
        }
        h1 {
            font-size: 2.5em;
            
            color: #1a1a1a;
            font-weight: 700;
        }
        p {
            font-size: 1.1em;
            margin-bottom: 20px;
            color: #555;
        }
        .highlight {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 600;
        }
        .index-item {
            background: white;
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
        }
        .index-title {
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 8px;
        }
        .index-desc {
            color: #666;
            font-size: 0.95em;
        }
        .value-prop {
            background: white;
            padding: 25px;
            border-radius: 12px;
            margin: 30px 0;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            border: 1px solid #e1e5e9;
        }
        a {
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }
        a:hover {
            text-decoration: underline;
        }
        .coming-soon {
            background: #f8f9fa;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            color: #666;
            margin-left: 10px;
        }
    </style>
</head>
<body>
    <h1>📊 FS Chain API: Valuation as a Service</h1>
    
    <p>The financial markets have operated on noisy data for decades. <span class="highlight">FS Chain changes that</span>.</p>
    
    <p>Our API delivers unprecedented precision in S&P 500 company valuations through two revolutionary, independent tracking systems that eliminate the noise plaguing traditional investment strategies.</p>
    
    <div class="index-item">
        <div class="index-title">F-Index</div>
        <div class="index-desc">Pure financial fundamentals stripped of market emotion and speculation.</div>
    </div>
    
    <div class="index-item">
        <div class="index-title">S-Index <span class="coming-soon">launching soon</span></div>
        <div class="index-desc">Real-time sentiment dynamics captured and quantified.</div>
    </div>
    
    <div class="value-prop">
        <p>Each index enables portfolio construction with surgical precision, allowing institutional investors to isolate fundamental value from sentiment-driven volatility. The indices power our F-Token and S-Token pricing mechanisms, creating the first truly separated value streams in financial markets.</p>
        
        <p>This is not incremental improvement. This is market infrastructure reimagined.</p>
    </div>
    
    <p>Complete technical specifications and research available at <a href="https://fschain.framer.wiki/in-laymens-terms">FS Chain Wiki</a>.</p>
    
   <h3>Available Dashboards:</h3>
               
                <a href="/s&p500" class="button">🎯 S&P 500 Dashboard</a>
                <a href="/plot/AAPL" class="button">🔍 Dashboard Example: (AAPL)</a>
                <a href="/index/f/AAPL" class="button">📋 Raw Data (JSON) for AAPL</a>
                <a href="/available-tickers" class="button">📈 Available Tickers</a>
                
</body>
</html>
    """

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

        
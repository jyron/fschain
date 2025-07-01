from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd
import uvicorn
import sys
import os

# Add the current directory to Python path so it can find plotting.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from plotting import create_index_plot_html, create_company_radar_plot

app = FastAPI()


@app.get("/index/f/{ticker}")
def get_index_score(ticker: str):
    df = pd.read_csv("data/company_financial_indexes.csv")
    df = df[df["ticker"] == ticker.upper()]
    return df.to_dict(orient="records")

@app.get("/index/f/")
def get_all_index_scores():
    df = pd.read_csv("data/company_financial_indexes.csv")
    return df.to_dict(orient="records")

@app.get("/plot/{ticker}", response_class=HTMLResponse)
def get_index_plot_html(ticker: str):
    """Get an interactive HTML radar plot for a specific ticker"""
    df = pd.read_csv("data/company_financial_indexes.csv")
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
    
    return create_index_plot_html(company_df)

@app.get("/available-tickers", response_class=HTMLResponse)
def get_available_tickers():
    """Show all available tickers as clickable links"""
    df = pd.read_csv("data/company_financial_indexes.csv")
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
    """Landing page with navigation"""
    return """
    <html>
        <head>
            <title>Financial Index API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; text-align: center; }
                .container { max-width: 600px; margin: 0 auto; }
                .button { 
                    display: inline-block; 
                    padding: 10px 20px; 
                    margin: 10px; 
                    background-color: #007bff; 
                    color: white; 
                    text-decoration: none; 
                    border-radius: 5px; 
                }
                .button:hover { background-color: #0056b3; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Financial Index API</h1>
                <p>Welcome to the Financial Health Analysis API!</p>
                
                <h3>Available Options:</h3>
                <a href="/available-tickers" class="button">📈 View All Stock Tickers</a>
                <a href="/plot/AAPL" class="button">🔍 Example: Apple (AAPL)</a>
                <a href="/index/f/" class="button">📋 Raw Data (JSON)</a>
                
                <h3>API Endpoints:</h3>
                <ul style="text-align: left; margin-top: 20px;">
                    <li><code>/plot/{ticker}</code> - Interactive radar chart for specific ticker</li>
                    <li><code>/index/f/{ticker}</code> - JSON data for specific ticker</li>
                    <li><code>/index/f/</code> - JSON data for all companies</li>
                    <li><code>/available-tickers</code> - List of all available tickers</li>
                </ul>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
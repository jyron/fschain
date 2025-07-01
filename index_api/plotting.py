import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def get_rating(score):
    """Convert numeric score to descriptive rating"""
    if score >= 0.8:
        return "Excellent"
    elif score >= 0.6:
        return "Very Good"
    elif score >= 0.4:
        return "Good"
    elif score >= 0.2:
        return "Fair"
    else:
        return "Poor"


def create_index_plot_html(df: pd.DataFrame) -> str:
    """Create a radar plot and return as HTML string"""
    # Get the first row of data (assuming single company)
    if df.empty:
        return "<h1>No data to plot</h1>"
    
    # Get the first company's data
    company_data = df.iloc[0]
    ticker = company_data['ticker']
    
    # Define better labels and descriptions for the metrics
    metric_labels = {
        'Profitability_score': 'Profitability',
        'Liquidity_score': 'Liquidity', 
        'Efficiency_score': 'Efficiency',
        'Solvency_score': 'Solvency',
        'AssetQuality_score': 'Asset Quality',
        'InvestmentCost_score': 'Investment Cost',
        'PerShareFundamentals_score': 'Per Share Value'
    }
    
    # Get metric columns (exclude ticker and overall index_score)
    metric_columns = [col for col in df.columns if col not in ['ticker', 'index_score']]
    
    # Prepare data for the radar chart
    values = [company_data[col] for col in metric_columns]
    labels = [metric_labels.get(col, col.replace('_score', '').replace('_', ' ').title()) for col in metric_columns]
    
    # Create the radar chart
    fig = px.line_polar(
        r=values,
        theta=labels,
        line_close=True,
        title=f'Financial Health Radar - {ticker}',
        range_r=[0, 1]  # Set range from 0 to 1 since scores are normalized
    )
    
    # Customize the chart for better readability
    fig.update_traces(
        fill='toself',
        fillcolor='rgba(0, 123, 255, 0.3)',
        line=dict(color='rgb(0, 123, 255)', width=3)
    )
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickvals=[0.2, 0.4, 0.6, 0.8, 1.0],
                ticktext=['Poor', 'Fair', 'Good', 'Very Good', 'Excellent'],
                gridcolor='lightgray'
            ),
            angularaxis=dict(
                tickfont=dict(size=12),
                gridcolor='lightgray'
            )
        ),
        title=dict(
            text=f'Financial Health Radar - {ticker}<br><sub>Overall Score: {company_data["index_score"]:.3f}/1.000</sub>',
            x=0.5,
            font=dict(size=16)
        ),
        width=700,
        height=700,
        showlegend=False
    )
    
    # Create metrics summary table
    metrics_html = """
    <div style="margin-top: 20px; font-family: Arial, sans-serif;">
        <h3>Individual Metrics Breakdown:</h3>
        <table style="border-collapse: collapse; width: 100%; margin-top: 10px;">
            <tr style="background-color: #f2f2f2;">
                <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Metric</th>
                <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Score</th>
                <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Rating</th>
            </tr>
    """
    
    for col, label in zip(metric_columns, labels):
        score = company_data[col]
        rating = get_rating(score)
        color = get_rating_color(score)
        metrics_html += f"""
            <tr>
                <td style="border: 1px solid #ddd; padding: 8px;">{label}</td>
                <td style="border: 1px solid #ddd; padding: 8px;">{score:.3f}</td>
                <td style="border: 1px solid #ddd; padding: 8px; background-color: {color}; font-weight: bold;">{rating}</td>
            </tr>
        """
    
    metrics_html += """
        </table>
        <div style="margin-top: 20px; padding: 15px; background-color: #f9f9f9; border-radius: 5px;">
            <h4>Metric Explanations:</h4>
            <ul style="line-height: 1.6;">
                <li><strong>Profitability:</strong> How well the company generates profit</li>
                <li><strong>Liquidity:</strong> Ability to meet short-term obligations</li>
                <li><strong>Efficiency:</strong> How effectively assets are used</li>
                <li><strong>Solvency:</strong> Long-term financial stability</li>
                <li><strong>Asset Quality:</strong> Quality and productivity of assets</li>
                <li><strong>Investment Cost:</strong> Cost efficiency of investments</li>
                <li><strong>Per Share Value:</strong> Value metrics per share</li>
            </ul>
        </div>
    </div>
    """
    
    # Convert plot to HTML and combine with metrics
    plot_html = fig.to_html(include_plotlyjs=True)
    
    # Combine plot and metrics in a nice layout
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Financial Analysis - {ticker}</title>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            .header {{ text-align: center; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Financial Health Analysis - {ticker}</h1>
                <p style="font-size: 18px; color: #666;">Overall Index Score: <strong>{company_data["index_score"]:.3f}/1.000</strong></p>
            </div>
            {plot_html.split('<body>')[1].split('</body>')[0]}
            {metrics_html}
        </div>
    </body>
    </html>
    """
    
    return full_html


def get_rating_color(score):
    """Get color based on rating score"""
    if score >= 0.8:
        return "#d4edda"  # Light green
    elif score >= 0.6:
        return "#d1ecf1"  # Light blue
    elif score >= 0.4:
        return "#fff3cd"  # Light yellow
    elif score >= 0.2:
        return "#f8d7da"  # Light red
    else:
        return "#f5c6cb"  # Darker red


def create_index_plot(df: pd.DataFrame):
    """Create a radar plot and show it (for desktop use)"""
    # Get the first row of data (assuming single company)
    if df.empty:
        print("No data to plot")
        return
    
    # Get the first company's data
    company_data = df.iloc[0]
    ticker = company_data['ticker']
    
    # Define better labels and descriptions for the metrics
    metric_labels = {
        'Profitability_score': 'Profitability',
        'Liquidity_score': 'Liquidity', 
        'Efficiency_score': 'Efficiency',
        'Solvency_score': 'Solvency',
        'AssetQuality_score': 'Asset Quality',
        'InvestmentCost_score': 'Investment Cost',
        'PerShareFundamentals_score': 'Per Share Value'
    }
    
    # Get metric columns (exclude ticker and overall index_score)
    metric_columns = [col for col in df.columns if col not in ['ticker', 'index_score']]
    
    # Prepare data for the radar chart
    values = [company_data[col] for col in metric_columns]
    labels = [metric_labels.get(col, col.replace('_score', '').replace('_', ' ').title()) for col in metric_columns]
    
    # Create the radar chart
    fig = px.line_polar(
        r=values,
        theta=labels,
        line_close=True,
        title=f'Financial Health Radar - {ticker}',
        range_r=[0, 1]  # Set range from 0 to 1 since scores are normalized
    )
    
    # Customize the chart for better readability
    fig.update_traces(
        fill='toself',
        fillcolor='rgba(0, 123, 255, 0.3)',
        line=dict(color='rgb(0, 123, 255)', width=3)
    )
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickvals=[0.2, 0.4, 0.6, 0.8, 1.0],
                ticktext=['Poor', 'Fair', 'Good', 'Very Good', 'Excellent'],
                gridcolor='lightgray'
            ),
            angularaxis=dict(
                tickfont=dict(size=12),
                gridcolor='lightgray'
            )
        ),
        title=dict(
            text=f'Financial Health Radar - {ticker}<br><sub>Overall Score: {company_data["index_score"]:.3f}/1.000</sub>',
            x=0.5,
            font=dict(size=16)
        ),
        width=700,
        height=700,
        showlegend=False
    )
    
    print(f"\n=== Financial Health Analysis for {ticker} ===")
    print(f"Overall Index Score: {company_data['index_score']:.3f}/1.000")
    print("\nIndividual Metrics:")
    for col, label in zip(metric_columns, labels):
        score = company_data[col]
        rating = get_rating(score)
        print(f"  {label}: {score:.3f} ({rating})")
    
    fig.show()


def create_company_radar_plot(ticker: str):
    """Create a radar plot for a specific company ticker"""
    df = pd.read_csv("data/company_financial_indexes.csv")
    company_df = df[df["ticker"] == ticker.upper()]
    
    if company_df.empty:
        print(f"No data found for ticker: {ticker}")
        return
    
    create_index_plot(company_df) 
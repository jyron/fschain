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


def create_index_radar_figure(df: pd.DataFrame):
    """Create a radar plot as a Plotly Figure for a single company"""
    if df.empty:
        return None
    company_data = df.iloc[0]
    ticker = company_data['ticker']
    metric_labels = {
        'Profitability_score': 'Profitability',
        'Liquidity_score': 'Liquidity', 
        'Efficiency_score': 'Efficiency',
        'Solvency_score': 'Solvency',
        'AssetQuality_score': 'Asset Quality',
        'InvestmentCost_score': 'Investment Cost',
        'PerShareFundamentals_score': 'Per Share Value'
    }
    metric_columns = [col for col in df.columns if col not in ['ticker', 'index_score']]
    values = [company_data[col] for col in metric_columns]
    labels = [metric_labels.get(col, col.replace('_score', '').replace('_', ' ').title()) for col in metric_columns]
    fig = px.line_polar(
        r=values,
        theta=labels,
        line_close=True,
        title=f'Financial Health Radar - {ticker}',
        range_r=[0, 1]
    )
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
    return fig


def get_company_metric_breakdown(df: pd.DataFrame):
    """Return a list of (label, score, rating, color) for each metric for a company"""
    if df.empty:
        return []
    company_data = df.iloc[0]
    metric_labels = {
        'Profitability_score': 'Profitability',
        'Liquidity_score': 'Liquidity', 
        'Efficiency_score': 'Efficiency',
        'Solvency_score': 'Solvency',
        'AssetQuality_score': 'Asset Quality',
        'InvestmentCost_score': 'Investment Cost',
        'PerShareFundamentals_score': 'Per Share Value'
    }
    metric_columns = [col for col in df.columns if col not in ['ticker', 'index_score']]
    labels = [metric_labels.get(col, col.replace('_score', '').replace('_', ' ').title()) for col in metric_columns]
    breakdown = []
    for col, label in zip(metric_columns, labels):
        score = company_data[col]
        rating = get_rating(score)
        color = get_rating_color(score)
        breakdown.append((label, score, rating, color))
    return breakdown


def create_dashboard_figures(df: pd.DataFrame):
    """Create all dashboard figures and return as a dict of Plotly Figures and summary data"""
    if df.empty:
        return {}
    df = df.copy()
    df['f_token_price'] = df['index_score'] * 100
    metric_labels = {
        'Profitability_score': 'Profitability',
        'Liquidity_score': 'Liquidity', 
        'Efficiency_score': 'Efficiency',
        'Solvency_score': 'Solvency',
        'AssetQuality_score': 'Asset Quality',
        'InvestmentCost_score': 'Investment Cost',
        'PerShareFundamentals_score': 'Per Share Value'
    }
    metric_columns = [col for col in df.columns if col not in ['ticker', 'index_score', 'f_token_price']]
    labels = [metric_labels.get(col, col.replace('_score', '').replace('_', ' ').title()) for col in metric_columns]
    df_sorted = df.sort_values('f_token_price', ascending=False).reset_index(drop=True)
    # Heatmap
    fig1 = px.imshow(
        df_sorted[metric_columns].T,
        x=df_sorted['ticker'],
        y=labels,
        color_continuous_scale='RdYlGn',
        aspect='auto',
        title='Financial Health Heatmap - All Companies (Ranked by F-Token Price)',
        labels={'color': 'Score'},
        color_continuous_midpoint=0.5
    )
    fig1.update_layout(
        width=1400,
        height=500,
        title_font_size=16,
        xaxis_title="Companies (Ranked by F-Token Performance)",
        yaxis_title="Financial Metrics",
        font=dict(size=12),
        xaxis=dict(showticklabels=False),
        margin=dict(l=150, r=50, t=80, b=50)
    )
    # F-Token price distribution
    fig2 = px.histogram(
        df_sorted,
        x='f_token_price',
        nbins=50,
        title='F-Token Price Distribution',
        labels={'f_token_price': 'F-Token Price ($)', 'count': 'Number of Companies'},
        color_discrete_sequence=['#1f77b4']
    )
    fig2.add_vline(x=df_sorted['f_token_price'].mean(), line_dash="dash", line_color="red",
                   annotation_text=f"Mean: ${df_sorted['f_token_price'].mean():.2f}")
    fig2.add_vline(x=df_sorted['f_token_price'].median(), line_dash="dash", line_color="orange",
                   annotation_text=f"Median: ${df_sorted['f_token_price'].median():.2f}")
    fig2.update_layout(
        width=700,
        height=400,
        title_font_size=14,
        showlegend=False
    )
    # Correlation matrix
    correlation_df = df_sorted[metric_columns + ['index_score']].corr()
    correlation_labels = labels + ['Overall Index']
    fig3 = px.imshow(
        correlation_df.values,
        x=correlation_labels,
        y=correlation_labels,
        color_continuous_scale='RdBu',
        title='Financial Metrics Correlation Matrix',
        labels={'color': 'Correlation'},
        color_continuous_midpoint=0
    )
    fig3.update_layout(
        width=700,
        height=400,
        title_font_size=14,
        font=dict(size=10)
    )
    # Performance tiers
    df_sorted['performance_tier'] = pd.cut(
        df_sorted['f_token_price'], 
        bins=5, 
        labels=['Tier 5 (Developing)', 'Tier 4 (Fair)', 'Tier 3 (Good)', 'Tier 2 (Very Good)', 'Tier 1 (Excellent)']
    )
    fig4 = px.box(
        df_sorted,
        x='performance_tier',
        y='f_token_price',
        title='F-Token Price Distribution by Performance Tier',
        labels={'performance_tier': 'Performance Tier', 'f_token_price': 'F-Token Price ($)'},
        color='performance_tier',
        color_discrete_sequence=['#d62728', '#ff7f0e', '#ffbb78', '#2ca02c', '#1f77b4']
    )
    fig4.update_layout(
        width=1000,
        height=400,
        title_font_size=14,
        showlegend=False,
        xaxis_tickangle=-45
    )
    # Summary data
    total_companies = len(df_sorted)
    avg_price = df_sorted['f_token_price'].mean()
    top_price = df_sorted['f_token_price'].max()
    top_company = df_sorted.iloc[0]['ticker']
    top_10 = df_sorted.head(10)
    bottom_10 = df_sorted.tail(10)
    metric_averages = {labels[i]: df_sorted[metric_columns[i]].mean() for i in range(len(metric_columns))}
    strongest_metric = max(metric_averages.items(), key=lambda x: x[1])
    weakest_metric = min(metric_averages.items(), key=lambda x: x[1])
    summary = {
        'total_companies': total_companies,
        'avg_price': avg_price,
        'top_price': top_price,
        'top_company': top_company,
        'top_10': top_10,
        'bottom_10': bottom_10,
        'strongest_metric': strongest_metric,
        'weakest_metric': weakest_metric,
        'df_sorted': df_sorted,
        'labels': labels,
        'metric_columns': metric_columns
    }
    return {
        'heatmap': fig1,
        'distribution': fig2,
        'correlation': fig3,
        'tiers': fig4,
        'summary': summary
    }


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
            .f-token-price {{ 
                background-color: #e8f4fd; 
                border: 2px solid #007bff; 
                border-radius: 10px; 
                padding: 15px; 
                margin: 20px 0; 
                text-align: center; 
                font-size: 18px; 
                font-weight: bold; 
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Financial Health Analysis - {ticker}</h1>
                <p style="font-size: 18px; color: #666;">Overall Index Score: <strong>{company_data["index_score"]:.3f}/1.000</strong></p>
                <div class="f-token-price">
                    🪙 F-{ticker} Price: <span style="color: #007bff;">${company_data["index_score"] * 100:.2f}</span>
                </div>
            </div>
            {plot_html.split('<body>')[1].split('</body>')[0]}
            {metrics_html}
        </div>
    </body>
    </html>
    """
    
    return full_html


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
    print(f"🪙 F-{ticker} Price: ${company_data['index_score'] * 100:.2f}")
    print("\nIndividual Metrics:")
    for col, label in zip(metric_columns, labels):
        score = company_data[col]
        rating = get_rating(score)
        print(f"  {label}: {score:.3f} ({rating})")
    
    fig.show()


def create_company_radar_plot(ticker: str):
    """Create a radar plot for a specific company and show it"""
    df = pd.read_csv("data/company_financial_indexes.csv")
    company_df = df[df["ticker"] == ticker.upper()]
    
    if company_df.empty:
        print(f"No data found for ticker: {ticker}")
        return
    
    create_index_plot(company_df)


def create_scatter_plot_html() -> str:
    """Create a professional financial dashboard showing all companies"""
    df = pd.read_csv("data/company_financial_indexes.csv")
    
    if df.empty:
        return "<h1>No data available</h1>"
    
    # Calculate F-token prices
    df['f_token_price'] = df['index_score'] * 100
    
    # Define metric labels
    metric_labels = {
        'Profitability_score': 'Profitability',
        'Liquidity_score': 'Liquidity', 
        'Efficiency_score': 'Efficiency',
        'Solvency_score': 'Solvency',
        'AssetQuality_score': 'Asset Quality',
        'InvestmentCost_score': 'Investment Cost',
        'PerShareFundamentals_score': 'Per Share Value'
    }
    
    # Get metric columns
    metric_columns = [col for col in df.columns if col not in ['ticker', 'index_score', 'f_token_price']]
    labels = [metric_labels.get(col, col.replace('_score', '').replace('_', ' ').title()) for col in metric_columns]
    
    # Sort by F-token price for better organization
    df_sorted = df.sort_values('f_token_price', ascending=False).reset_index(drop=True)
    
    # Create main heatmap showing all companies
    fig1 = px.imshow(
        df_sorted[metric_columns].T,
        x=df_sorted['ticker'],
        y=labels,
        color_continuous_scale='RdYlGn',
        aspect='auto',
        title='Financial Health Heatmap - All Companies (Ranked by F-Token Price)',
        labels={'color': 'Score'},
        color_continuous_midpoint=0.5
    )
    
    fig1.update_layout(
        width=1400,
        height=500,
        title_font_size=16,
        xaxis_title="Companies (Ranked by F-Token Performance)",
        yaxis_title="Financial Metrics",
        font=dict(size=12),
        xaxis=dict(showticklabels=False),  # Hide individual ticker names for cleaner look
        margin=dict(l=150, r=50, t=80, b=50)
    )
    
    # Create F-Token price distribution
    fig2 = px.histogram(
        df_sorted,
        x='f_token_price',
        nbins=50,
        title='F-Token Price Distribution',
        labels={'f_token_price': 'F-Token Price ($)', 'count': 'Number of Companies'},
        color_discrete_sequence=['#1f77b4']
    )
    
    fig2.add_vline(x=df_sorted['f_token_price'].mean(), line_dash="dash", line_color="red",
                   annotation_text=f"Mean: ${df_sorted['f_token_price'].mean():.2f}")
    fig2.add_vline(x=df_sorted['f_token_price'].median(), line_dash="dash", line_color="orange",
                   annotation_text=f"Median: ${df_sorted['f_token_price'].median():.2f}")
    
    fig2.update_layout(
        width=700,
        height=400,
        title_font_size=14,
        showlegend=False
    )
    
    # Create correlation matrix
    correlation_df = df_sorted[metric_columns + ['index_score']].corr()
    correlation_labels = labels + ['Overall Index']
    
    fig3 = px.imshow(
        correlation_df.values,
        x=correlation_labels,
        y=correlation_labels,
        color_continuous_scale='RdBu',
        title='Financial Metrics Correlation Matrix',
        labels={'color': 'Correlation'},
        color_continuous_midpoint=0
    )
    
    fig3.update_layout(
        width=700,
        height=400,
        title_font_size=14,
        font=dict(size=10)
    )
    
    # Create sector performance (if we can determine sectors)
    # For now, we'll create performance tiers
    df_sorted['performance_tier'] = pd.cut(
        df_sorted['f_token_price'], 
        bins=5, 
        labels=['Tier 5 (Developing)', 'Tier 4 (Fair)', 'Tier 3 (Good)', 'Tier 2 (Very Good)', 'Tier 1 (Excellent)']
    )
    
    tier_summary = df_sorted.groupby('performance_tier').agg({
        'f_token_price': ['mean', 'count'],
        'index_score': 'mean'
    }).round(3)
    
    fig4 = px.box(
        df_sorted,
        x='performance_tier',
        y='f_token_price',
        title='F-Token Price Distribution by Performance Tier',
        labels={'performance_tier': 'Performance Tier', 'f_token_price': 'F-Token Price ($)'},
        color='performance_tier',
        color_discrete_sequence=['#d62728', '#ff7f0e', '#ffbb78', '#2ca02c', '#1f77b4']
    )
    
    fig4.update_layout(
        width=1000,
        height=400,
        title_font_size=14,
        showlegend=False,
        xaxis_tickangle=-45
    )
    
    # Convert all plots to HTML
    heatmap_html = fig1.to_html( div_id="heatmap")
    distribution_html = fig2.to_html( div_id="distribution")
    correlation_html = fig3.to_html( div_id="correlation")
    tiers_html = fig4.to_html(div_id="tiers")
    
    # Calculate key statistics
    total_companies = len(df_sorted)
    avg_price = df_sorted['f_token_price'].mean()
    top_price = df_sorted['f_token_price'].max()
    top_company = df_sorted.iloc[0]['ticker']
    
    # Get top performers
    top_10 = df_sorted.head(10)
    bottom_10 = df_sorted.tail(10)
    
    # Calculate metric averages
    metric_averages = {labels[i]: df_sorted[metric_columns[i]].mean() for i in range(len(metric_columns))}
    strongest_metric = max(metric_averages.items(), key=lambda x: x[1])
    weakest_metric = min(metric_averages.items(), key=lambda x: x[1])
    
    # Create comprehensive dashboard HTML
    dashboard_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Financial Intelligence Dashboard - F-Token Analytics</title>
        <meta charset="utf-8">
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #2d3748;
            }}
            
            .dashboard-container {{
                max-width: 1600px;
                margin: 0 auto;
                padding: 20px;
            }}
            
            .header {{
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 30px;
                margin-bottom: 30px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
                text-align: center;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            
            .header h1 {{
                font-size: 2.5rem;
                font-weight: 700;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 10px;
            }}
            
            .header p {{
                font-size: 1.1rem;
                color: #718096;
                font-weight: 400;
            }}
            
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            
            .stat-card {{
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 16px;
                padding: 25px;
                text-align: center;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }}
            
            .stat-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
            }}
            
            .stat-number {{
                font-size: 2.2rem;
                font-weight: 700;
                color: #1a202c;
                margin-bottom: 8px;
            }}
            
            .stat-label {{
                font-size: 0.9rem;
                color: #718096;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            
            .chart-grid {{
                display: grid;
                grid-template-columns: 1fr;
                gap: 30px;
                margin-bottom: 30px;
            }}
            
            .chart-container {{
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 25px;
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            
            .chart-row {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 30px;
                margin-bottom: 30px;
            }}
            
            .performance-tables {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 30px;
                margin-top: 30px;
            }}
            
            .table-container {{
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 16px;
                padding: 25px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            
            .table-container h3 {{
                font-size: 1.3rem;
                font-weight: 600;
                margin-bottom: 20px;
                color: #1a202c;
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                font-size: 0.9rem;
            }}
            
            th, td {{
                padding: 12px 8px;
                text-align: left;
                border-bottom: 1px solid #e2e8f0;
            }}
            
            th {{
                background-color: #f7fafc;
                font-weight: 600;
                color: #2d3748;
                font-size: 0.8rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            
            .ticker {{
                font-weight: 600;
                color: #2b6cb0;
            }}
            
            .price {{
                font-weight: 600;
                color: #38a169;
            }}
            
            .back-link {{
                display: inline-block;
                margin-bottom: 20px;
                padding: 12px 24px;
                background: rgba(255, 255, 255, 0.9);
                color: #4a5568;
                text-decoration: none;
                border-radius: 12px;
                font-weight: 500;
                transition: all 0.3s ease;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }}
            
            .back-link:hover {{
                background: rgba(255, 255, 255, 1);
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            }}
            
            .insights-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }}
            
            .insight-card {{
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 16px;
                padding: 25px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            
            .insight-card h4 {{
                font-size: 1.1rem;
                font-weight: 600;
                margin-bottom: 15px;
                color: #1a202c;
            }}
            
            .insight-list {{
                list-style: none;
                padding: 0;
            }}
            
            .insight-list li {{
                padding: 8px 0;
                border-bottom: 1px solid #f0f0f0;
                font-size: 0.9rem;
                color: #4a5568;
            }}
            
            .insight-list li:last-child {{
                border-bottom: none;
            }}
            
            .metric-strength {{
                display: inline-block;
                padding: 4px 8px;
                border-radius: 6px;
                font-size: 0.8rem;
                font-weight: 500;
                margin-left: 8px;
            }}
            
            .excellent {{ background-color: #c6f6d5; color: #22543d; }}
            .very-good {{ background-color: #bee3f8; color: #2a4365; }}
            .good {{ background-color: #fefcbf; color: #744210; }}
            .fair {{ background-color: #fed7d7; color: #742a2a; }}
            .poor {{ background-color: #fed7e2; color: #702459; }}
        </style>
    </head>
    <body>
        <div class="dashboard-container">
            <a href="/" class="back-link">← Back to Home</a>
            
            <div class="header">
                <h1>Financial Intelligence Dashboard</h1>
                <p>Comprehensive F-Token Market Analysis & Performance Metrics</p>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{total_companies}</div>
                    <div class="stat-label">Total Companies</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${avg_price:.2f}</div>
                    <div class="stat-label">Average F-Token Price</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${top_price:.2f}</div>
                    <div class="stat-label">Highest F-Token Price</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{top_company}</div>
                    <div class="stat-label">Top Performer</div>
                </div>
            </div>
            
            <div class="insights-grid">
                <div class="insight-card">
                    <h4>💪 Market Strengths</h4>
                    <ul class="insight-list">
                        <li>Strongest Metric: {strongest_metric[0]} 
                            <span class="metric-strength {get_rating(strongest_metric[1]).lower().replace(' ', '-')}">{get_rating(strongest_metric[1])}</span>
                        </li>
                        <li>Top 10% F-Token Range: ${df_sorted.head(int(len(df_sorted)*0.1))['f_token_price'].min():.2f} - ${top_price:.2f}</li>
                        <li>Companies Above Average: {len(df_sorted[df_sorted['f_token_price'] > avg_price])}</li>
                    </ul>
                </div>
                <div class="insight-card">
                    <h4>📈 Improvement Areas</h4>
                    <ul class="insight-list">
                        <li>Weakest Metric: {weakest_metric[0]} 
                            <span class="metric-strength {get_rating(weakest_metric[1]).lower().replace(' ', '-')}">{get_rating(weakest_metric[1])}</span>
                        </li>
                        <li>Bottom 10% F-Token Range: ${df_sorted.tail(int(len(df_sorted)*0.1))['f_token_price'].min():.2f} - ${df_sorted.tail(int(len(df_sorted)*0.1))['f_token_price'].max():.2f}</li>
                        <li>Companies Below Average: {len(df_sorted[df_sorted['f_token_price'] < avg_price])}</li>
                    </ul>
                </div>
                <div class="insight-card">
                    <h4>🎯 Key Metrics</h4>
                    <ul class="insight-list">
                        <li>Price Volatility: {(df_sorted['f_token_price'].std()/avg_price*100):.1f}% CV</li>
                        <li>Market Spread: ${df_sorted['f_token_price'].max() - df_sorted['f_token_price'].min():.2f}</li>
                        <li>Median F-Token: ${df_sorted['f_token_price'].median():.2f}</li>
                    </ul>
                </div>
            </div>
            
            <div class="chart-container">
                {heatmap_html}
            </div>
            
            <div class="chart-row">
                <div class="chart-container">
                    {distribution_html}
                </div>
                <div class="chart-container">
                    {correlation_html}
                </div>
            </div>
            
            <div class="chart-container">
                {tiers_html}
            </div>
            
            <div class="performance-tables">
                <div class="table-container">
                    <h3>🏆 Top 10 F-Token Performers</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Rank</th>
                                <th>Ticker</th>
                                <th>F-Token Price</th>
                                <th>Index Score</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
    """
    
    # Add top 10 performers
    for i, (_, company) in enumerate(top_10.iterrows(), 1):
        dashboard_html += f"""
                            <tr>
                                <td>#{i}</td>
                                <td class="ticker">{company['ticker']}</td>
                                <td class="price">${company['f_token_price']:.2f}</td>
                                <td>{company['index_score']:.3f}</td>
                                <td><a href="/plot/{company['ticker']}" style="color: #3182ce; text-decoration: none;">View Details</a></td>
                            </tr>
        """
    
    dashboard_html += """
                        </tbody>
                    </table>
                </div>
                
                <div class="table-container">
                    <h3>📊 Bottom 10 F-Token Performers</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Rank</th>
                                <th>Ticker</th>
                                <th>F-Token Price</th>
                                <th>Index Score</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
    """
    
    # Add bottom 10 performers
    for i, (_, company) in enumerate(bottom_10.iterrows(), 1):
        rank = total_companies - len(bottom_10) + i
        dashboard_html += f"""
                            <tr>
                                <td>#{rank}</td>
                                <td class="ticker">{company['ticker']}</td>
                                <td class="price">${company['f_token_price']:.2f}</td>
                                <td>{company['index_score']:.3f}</td>
                                <td><a href="/plot/{company['ticker']}" style="color: #3182ce; text-decoration: none;">View Details</a></td>
                            </tr>
        """
    
    dashboard_html += """
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        
        <script>
            // Add some interactive enhancements
            document.addEventListener('DOMContentLoaded', function() {
                // Add hover effects to stat cards
                const statCards = document.querySelectorAll('.stat-card');
                statCards.forEach(card => {
                    card.addEventListener('mouseenter', function() {
                        this.style.transform = 'translateY(-5px) scale(1.02)';
                    });
                    card.addEventListener('mouseleave', function() {
                        this.style.transform = 'translateY(0) scale(1)';
                    });
                });
            });
        </script>
    </body>
    </html>
    """
    
    return dashboard_html 
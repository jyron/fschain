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


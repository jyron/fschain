from plotly.graph_objs import Figure
from typing import List, Tuple, Optional
import pandas as pd

def render_index_plot_html(fig: Figure, ticker: str, metrics: List[Tuple[str, float, str, str]], index_score: Optional[float]) -> str:
    plot_html = fig.to_html(include_plotlyjs=True) if fig else "<h1>No data to plot</h1>"
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
    for label, score, rating, color in metrics:
        metrics_html += f"""
            <tr>
                <td style=\"border: 1px solid #ddd; padding: 8px;\">{label}</td>
                <td style=\"border: 1px solid #ddd; padding: 8px;\">{score:.3f}</td>
                <td style=\"border: 1px solid #ddd; padding: 8px; background-color: {color}; font-weight: bold;\">{rating}</td>
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
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Financial Analysis - {ticker}</title>
        <meta charset=\"utf-8\">
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
        <div class=\"container\">
        <a href=\"/\" class=\"back-link\">← Back to Home</a>
            <div class=\"header\">
                <h1>Financial Health Analysis - {ticker}</h1>
                <p style=\"font-size: 18px; color: #666;\">Overall Index Score: <strong>{index_score:.3f}/1.000</strong></p>
                <div class=\"f-token-price\">
                    🪙 F-{ticker} Price: <span style=\"color: #007bff;\">${index_score * 100:.2f}</span>
                </div>
            </div>
            {plot_html.split('<body>')[1].split('</body>')[0] if '<body>' in plot_html else plot_html}
            {metrics_html}
        </div>
    </body>
    </html>
    """
    return full_html

def render_scatter_dashboard_html(dashboard: dict) -> str:
    # Extract figures and summary
    heatmap_html = dashboard['heatmap'].to_html(div_id="heatmap") if dashboard.get('heatmap') else ""
    distribution_html = dashboard['distribution'].to_html(div_id="distribution") if dashboard.get('distribution') else ""
    correlation_html = dashboard['correlation'].to_html(div_id="correlation") if dashboard.get('correlation') else ""
    tiers_html = dashboard['tiers'].to_html(div_id="tiers") if dashboard.get('tiers') else ""
    summary = dashboard.get('summary', {})
    total_companies = summary.get('total_companies', 0)
    avg_price = summary.get('avg_price', 0)
    top_price = summary.get('top_price', 0)
    top_company = summary.get('top_company', '')
    top_10 = summary.get('top_10', pd.DataFrame())
    bottom_10 = summary.get('bottom_10', pd.DataFrame())
    strongest_metric = summary.get('strongest_metric', ("", 0))
    weakest_metric = summary.get('weakest_metric', ("", 0))
    df_sorted = summary.get('df_sorted', pd.DataFrame())
    # HTML rendering (copied and modularized from previous dashboard_html)
    dashboard_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Financial Intelligence Dashboard - F-Token Analytics</title>
        <meta charset=\"utf-8\">
        <script src=\"https://cdn.plot.ly/plotly-latest.min.js\"></script>
        <link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap\" rel=\"stylesheet\">
        <style>
            /* ... (same CSS as before, omitted for brevity) ... */
            body {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; color: #2d3748; }}
            .dashboard-container {{ max-width: 1600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border-radius: 20px; padding: 30px; margin-bottom: 30px; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1); text-align: center; border: 1px solid rgba(255, 255, 255, 0.2); }}
            .header h1 {{ font-size: 2.5rem; font-weight: 700; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px; }}
            .header p {{ font-size: 1.1rem; color: #718096; font-weight: 400; }}
            .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }}
            .stat-card {{ background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border-radius: 16px; padding: 25px; text-align: center; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); border: 1px solid rgba(255, 255, 255, 0.2); transition: transform 0.3s ease, box-shadow 0.3s ease; }}
            .stat-card:hover {{ transform: translateY(-5px); box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15); }}
            .stat-number {{ font-size: 2.2rem; font-weight: 700; color: #1a202c; margin-bottom: 8px; }}
            .stat-label {{ font-size: 0.9rem; color: #718096; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }}
            .chart-grid {{ display: grid; grid-template-columns: 1fr; gap: 30px; margin-bottom: 30px; }}
            .chart-container {{ background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border-radius: 20px; padding: 25px; box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1); border: 1px solid rgba(255, 255, 255, 0.2); }}
            .chart-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 30px; }}
            .performance-tables {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-top: 30px; }}
            .table-container {{ background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border-radius: 16px; padding: 25px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); border: 1px solid rgba(255, 255, 255, 0.2); }}
            .table-container h3 {{ font-size: 1.3rem; font-weight: 600; margin-bottom: 20px; color: #1a202c; }}
            table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
            th, td {{ padding: 12px 8px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
            th {{ background-color: #f7fafc; font-weight: 600; color: #2d3748; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.5px; }}
            .ticker {{ font-weight: 600; color: #2b6cb0; }}
            .price {{ font-weight: 600; color: #38a169; }}
            .back-link {{ display: inline-block; margin-bottom: 20px; padding: 12px 24px; background: rgba(255, 255, 255, 0.9); color: #4a5568; text-decoration: none; border-radius: 12px; font-weight: 500; transition: all 0.3s ease; backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.3); }}
            .back-link:hover {{ background: rgba(255, 255, 255, 1); transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1); }}
            .insights-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 30px 0; }}
            .insight-card {{ background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border-radius: 16px; padding: 25px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); border: 1px solid rgba(255, 255, 255, 0.2); }}
            .insight-card h4 {{ font-size: 1.1rem; font-weight: 600; margin-bottom: 15px; color: #1a202c; }}
            .insight-list {{ list-style: none; padding: 0; }}
            .insight-list li {{ padding: 8px 0; border-bottom: 1px solid #f0f0f0; font-size: 0.9rem; color: #4a5568; }}
            .insight-list li:last-child {{ border-bottom: none; }}
            .metric-strength {{ display: inline-block; padding: 4px 8px; border-radius: 6px; font-size: 0.8rem; font-weight: 500; margin-left: 8px; }}
            .excellent {{ background-color: #c6f6d5; color: #22543d; }}
            .very-good {{ background-color: #bee3f8; color: #2a4365; }}
            .good {{ background-color: #fefcbf; color: #744210; }}
            .fair {{ background-color: #fed7d7; color: #742a2a; }}
            .poor {{ background-color: #fed7e2; color: #702459; }}
        </style>
    </head>
    <body>
        <div class=\"dashboard-container\">
            <a href=\"/\" class=\"back-link\">← Back to Home</a>
            <div class=\"header\">
                <h1>Financial Intelligence Dashboard</h1>
                <p>Comprehensive F-Token Market Analysis & Performance Metrics</p>
            </div>
            <div class=\"stats-grid\">
                <div class=\"stat-card\">
                    <div class=\"stat-number\">{total_companies}</div>
                    <div class=\"stat-label\">Total Companies</div>
                </div>
                <div class=\"stat-card\">
                    <div class=\"stat-number\">${avg_price:.2f}</div>
                    <div class=\"stat-label\">Average F-Token Price</div>
                </div>
                <div class=\"stat-card\">
                    <div class=\"stat-number\">${top_price:.2f}</div>
                    <div class=\"stat-label\">Highest F-Token Price</div>
                </div>
                <div class=\"stat-card\">
                    <div class=\"stat-number\">{top_company}</div>
                    <div class=\"stat-label\">Top Performer</div>
                </div>
            </div>
            <div class=\"insights-grid\">
                <div class=\"insight-card\">
                    <h4>💪 Market Strengths</h4>
                    <ul class=\"insight-list\">
                        <li>Strongest Metric: {strongest_metric[0]} 
                            <span class=\"metric-strength {str(strongest_metric[0]).lower().replace(' ', '-')}\">{strongest_metric[0]}</span>
                        </li>
                        <li>Top 10% F-Token Range: ${df_sorted.head(int(len(df_sorted)*0.1))['f_token_price'].min():.2f} - ${top_price:.2f}</li>
                        <li>Companies Above Average: {len(df_sorted[df_sorted['f_token_price'] > avg_price])}</li>
                    </ul>
                </div>
                <div class=\"insight-card\">
                    <h4>📈 Improvement Areas</h4>
                    <ul class=\"insight-list\">
                        <li>Weakest Metric: {weakest_metric[0]} 
                            <span class=\"metric-strength {str(weakest_metric[0]).lower().replace(' ', '-')}\">{weakest_metric[0]}</span>
                        </li>
                        <li>Bottom 10% F-Token Range: ${df_sorted.tail(int(len(df_sorted)*0.1))['f_token_price'].min():.2f} - ${df_sorted.tail(int(len(df_sorted)*0.1))['f_token_price'].max():.2f}</li>
                        <li>Companies Below Average: {len(df_sorted[df_sorted['f_token_price'] < avg_price])}</li>
                    </ul>
                </div>
                <div class=\"insight-card\">
                    <h4>🎯 Key Metrics</h4>
                    <ul class=\"insight-list\">
                        <li>Price Volatility: {(df_sorted['f_token_price'].std()/avg_price*100):.1f}% CV</li>
                        <li>Market Spread: ${df_sorted['f_token_price'].max() - df_sorted['f_token_price'].min():.2f}</li>
                        <li>Median F-Token: ${df_sorted['f_token_price'].median():.2f}</li>
                    </ul>
                </div>
            </div>
            <div class=\"chart-container\">
                {heatmap_html}
            </div>
            <div class=\"chart-row\">
                <div class=\"chart-container\">
                    {distribution_html}
                </div>
                <div class=\"chart-container\">
                    {correlation_html}
                </div>
            </div>
            <div class=\"chart-container\">
                {tiers_html}
            </div>
            <div class=\"performance-tables\">
                <div class=\"table-container\">
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
    if not top_10.empty:
        for i, (_, company) in enumerate(top_10.iterrows(), 1):
            dashboard_html += f"""
                                <tr>
                                    <td>#{i}</td>
                                    <td class=\"ticker\">{company['ticker']}</td>
                                    <td class=\"price\">${company['f_token_price']:.2f}</td>
                                    <td>{company['index_score']:.3f}</td>
                                    <td><a href=\"/plot/{company['ticker']}\" style=\"color: #3182ce; text-decoration: none;\">View Details</a></td>
                                </tr>
            """
    dashboard_html += """
                            </tbody>
                        </table>
                    </div>
                    <div class=\"table-container\">
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
    if not bottom_10.empty:
        for i, (_, company) in enumerate(bottom_10.iterrows(), 1):
            rank = total_companies - len(bottom_10) + i
            dashboard_html += f"""
                                <tr>
                                    <td>#{rank}</td>
                                    <td class=\"ticker\">{company['ticker']}</td>
                                    <td class=\"price\">${company['f_token_price']:.2f}</td>
                                    <td>{company['index_score']:.3f}</td>
                                    <td><a href=\"/plot/{company['ticker']}\" style=\"color: #3182ce; text-decoration: none;\">View Details</a></td>
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
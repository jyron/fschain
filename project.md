# FS CHAIN Dual-Token Market Model: Technical Specification Outline

## 1. Introduction

### Project Overview and Objectives

The FS Chain Dual-Token Market Model represents a revolutionary approach to tokenizing company valuation through two complementary indices: Financial Index (F-Index) and Sentiment Index (S-Index). This system creates a comprehensive, real-time valuation framework that captures both quantitative financial performance and qualitative market sentiment.

**Core Objectives**:

- **Democratize Financial Analysis**: Provide standardized, transparent company valuations accessible to all market participants
- **Real-Time Market Reflection**: Bridge traditional financial metrics with modern sentiment analysis for dynamic pricing
- **Decentralized Oracle Infrastructure**: Establish trustless, consensus-driven data validation and price discovery
- **Innovative Investment Products**: Enable new forms of tokenized exposure to company performance

### Dual-Token Concept (F-Token, S-Token)

**F-Token (Financial Token)**:

- Represents exposure to company financial performance
- Backed by 7-pillar financial analysis framework
- Lower volatility, fundamentals-focused
- Target investors: Value investors, institutional funds, conservative traders

**S-Token (Sentiment Token)**:

- Represents exposure to company market sentiment
- Driven by social media, news, and viral content analysis
- Higher volatility, market psychology-focused
- Target investors: Momentum traders, sentiment-driven strategies, short-term speculators

**Synergistic Design**:

- Complementary exposure profiles allow for sophisticated portfolio construction
- Combined F+S positions provide holistic company exposure
- Arbitrage opportunities between tokens encourage market efficiency
- Independent token mechanics enable specialized trading strategies

### High-Level Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     FS Chain Architecture                       │
├─────────────────────┬───────────────────────┬───────────────────┤
│   Financial Index   │   Sentiment Index     │   Oracle Network │
│     Subsystem       │     Subsystem         │                   │
│                     │                       │                   │
│ • Data Ingestion    │ • Social Media APIs   │ • 7+ Nodes        │
│ • Metric Normaliz.  │ • NLP Processing      │ • Consensus       │
│ • Pillar Scoring    │ • Trend Analysis      │ • Validation      │
│ • Index Aggregation │ • Sentiment Aggreg.   │ • Gas Optimization│
└─────────────────────┴───────────────────────┴───────────────────┤
                              │                                    │
┌─────────────────────────────▼────────────────────────────────────┤
│                   Smart Contract Layer                          │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │  F-Token    │  │  S-Token    │  │     Governance          │  │
│  │  Contract   │  │  Contract   │  │     Contract            │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

**Data Flow**:

1. Raw financial and sentiment data collection
2. Multi-stage processing and normalization
3. Index calculation and validation
4. Oracle consensus and cryptographic signing
5. On-chain price updates with gas optimization
6. Token price derivation and trading facilitation

### MVP Scope and Future Vision

**Phase 1: MVP (3-6 months)**

- Core F-Index calculation with 5 major companies (AAPL, GOOGL, MSFT, TSLA, AMZN)
- Basic S-Index using Twitter and news sentiment
- 7-node oracle network on Ethereum testnet
- Simple F-Token and S-Token contracts
- Web dashboard for price tracking

**Success Metrics**:

- F-Index updates within 24 hours of financial data availability
- S-Index updates every 2 hours during market hours
- Oracle consensus achieved in >95% of update cycles
- Gas costs <$5 per company update

**Phase 2: Enhanced Oracle (6-12 months)**

- Expand to 25 companies across major sectors
- Advanced NLP models for sentiment analysis
- Multi-source data integration (Reddit, TikTok, LinkedIn)
- Mainnet deployment with optimized gas costs
- Mobile application and API access

**Phase 3: Full Decentralization (12-18 months)**

- Open oracle node operation to community
- Machine learning model improvements
- Cross-chain deployment (Polygon, Arbitrum, BSC)
- DAO governance for parameter adjustments
- Institutional-grade APIs and tools

**Long-term Vision**:

- Global standard for tokenized company valuation
- Integration with major DeFi protocols
- Regulatory compliance framework
- AI-driven predictive modeling
- Support for 500+ public companies worldwide

## 2. Financial Index Subsystem

### Overview

The Financial Index Subsystem calculates a normalized financial health score (F-Index) for each company based on quantitative financial metrics. The F-Index ranges from 0.0 to 1.0, where 1.0 represents the strongest financial position relative to the analyzed universe of companies.

**Primary Purpose**: Generate standardized financial scores for F-Token price determination and oracle data pipeline consumption.

### Module Architecture

#### 2.1 Data Ingestion Module

**Module Name**: `FinancialDataIngester`

**Input Requirements**:

```python
{
    "data_sources": [
        {
            "source_type": "api",  # "api", "file", "database"
            "source_name": "bloomberg_api",  # Identifier for the source
            "api_endpoint": "https://api.bloomberg.com/financial-data",
            "authentication": {"type": "api_key", "key": "xxx"},
            "update_frequency": "daily",  # "daily", "hourly", "quarterly"
            "metrics_mapping": {  # Map source field names to internal names
                "total_revenue": "revenueTTM",
                "net_income": "netIncomeTTM",
                # ... additional mappings
            }
        }
    ],
    "companies": [
        {
            "company_id": "AAPL",
            "company_name": "Apple Inc.",
            "external_identifiers": {
                "ticker": "AAPL",
                "cusip": "037833100",
                "isin": "US0378331005"
            }
        }
    ]
}
```

**Output Format**:

```python
{
    "companies": {
        "AAPL": {
            "company_info": {
                "company_id": "AAPL",
                "company_name": "Apple Inc.",
                "last_updated": "2024-01-15T10:30:00Z"
            },
            "financial_metrics": {
                "revenueTTM": 394328000000,
                "netIncomeTTM": 97394000000,
                "totalAssets": 352755000000,
                "totalLiabilities": 290437000000,
                "operatingCashFlowTTM": 110543000000,
                # ... 50+ additional metrics
            },
            "data_quality": {
                "completeness_score": 0.95,  # Percentage of required metrics available
                "freshness_hours": 2,  # Hours since last update
                "source_reliability": 0.98  # Historical accuracy score
            }
        }
    },
    "ingestion_metadata": {
        "total_companies": 1,
        "successful_updates": 1,
        "failed_updates": 0,
        "timestamp": "2024-01-15T10:30:00Z"
    }
}
```

**Core Functions**:

- `fetch_financial_data(companies: List[str], metrics: List[str]) -> Dict`
- `validate_data_quality(data: Dict) -> Dict`
- `standardize_metric_names(raw_data: Dict) -> Dict`
- `handle_missing_values(data: Dict, strategy: str) -> Dict`

#### 2.2 Metric Normalization Module

**Module Name**: `MetricNormalizer`

**Input Requirements**:

```python
{
    "raw_metrics": {
        "AAPL": {
            "returnOnEquityTTM": 0.1569,
            "debtToEquityRatioTTM": 1.73,
            "currentRatioTTM": 1.05,
            # ... all company metrics
        }
    },
    "normalization_boundaries": {
        "returnOnEquityTTM": {
            "percentile_10": -0.05,
            "percentile_90": 0.40,
            "is_inverse": false
        },
        "debtToEquityRatioTTM": {
            "percentile_10": 0.1,
            "percentile_90": 3.0,
            "is_inverse": true  # Lower values are better
        }
    }
}
```

**Output Format**:

```python
{
    "normalized_metrics": {
        "AAPL": {
            "returnOnEquityTTM": 0.72,  # Normalized to 0-1 scale
            "debtToEquityRatioTTM": 0.43,  # Inverse normalized (lower debt = higher score)
            "currentRatioTTM": 0.51,
            # ... all normalized metrics
        }
    },
    "normalization_stats": {
        "total_metrics": 52,
        "successfully_normalized": 50,
        "failed_normalizations": 2,
        "boundary_violations": {
            "below_minimum": 3,
            "above_maximum": 5
        }
    }
}
```

**Core Functions**:

- `normalize_metric(value: float, min_bound: float, max_bound: float, is_inverse: bool) -> float`
- `calculate_percentile_boundaries(historical_data: Dict, percentiles: Tuple[int, int]) -> Dict`
- `handle_outliers(value: float, boundaries: Dict, strategy: str) -> float`
- `batch_normalize_company_metrics(companies_data: Dict, boundaries: Dict) -> Dict`

#### 2.3 Pillar Scoring Module

**Module Name**: `PillarScorer`

**Input Requirements**:

```python
{
    "normalized_metrics": {
        "AAPL": {
            "returnOnEquityTTM": 0.72,
            "netProfitMarginTTM": 0.85,
            "currentRatioTTM": 0.51,
            # ... all normalized metrics
        }
    },
    "pillar_definitions": {
        "Profitability": {
            "weight": 0.25,
            "metrics": {
                "returnOnEquityTTM": 0.20,
                "netProfitMarginTTM": 0.20,
                "operatingProfitMarginTTM": 0.20,
                "returnOnInvestedCapitalTTM": 0.25,
                "ebitdaMarginTTM": 0.15
            }
        },
        "Liquidity": {
            "weight": 0.20,
            "metrics": {
                "currentRatioTTM": 0.20,
                "quickRatioTTM": 0.15,
                "cashRatioTTM": 0.15,
                "operatingCashFlowCoverageRatioTTM": 0.30,
                "freeCashFlowOperatingCashFlowRatioTTM": 0.20
            }
        }
        # ... 5 more pillars
    }
}
```

**Output Format**:

```python
{
    "pillar_scores": {
        "AAPL": {
            "Profitability": 0.764,
            "Liquidity": 0.623,
            "Efficiency": 0.812,
            "Solvency": 0.445,
            "AssetQuality": 0.689,
            "InvestmentCost": 0.723,
            "PerShareFundamentals": 0.691
        }
    },
    "pillar_details": {
        "AAPL": {
            "Profitability": {
                "score": 0.764,
                "contributing_metrics": {
                    "returnOnEquityTTM": {"value": 0.72, "weight": 0.20, "contribution": 0.144},
                    "netProfitMarginTTM": {"value": 0.85, "weight": 0.20, "contribution": 0.170},
                    # ... other metrics
                },
                "missing_metrics": [],
                "coverage_percentage": 1.0
            }
        }
    }
}
```

**Core Functions**:

- `calculate_pillar_score(normalized_metrics: Dict, pillar_config: Dict) -> float`
- `validate_pillar_coverage(available_metrics: List[str], required_metrics: List[str]) -> Dict`
- `handle_missing_metrics(pillar_config: Dict, available_metrics: Dict, strategy: str) -> Dict`
- `generate_pillar_breakdown(pillar_scores: Dict, metric_contributions: Dict) -> Dict`

#### 2.4 Index Aggregation Module

**Module Name**: `IndexAggregator`

**Input Requirements**:

```python
{
    "pillar_scores": {
        "AAPL": {
            "Profitability": 0.764,
            "Liquidity": 0.623,
            "Efficiency": 0.812,
            "Solvency": 0.445,
            "AssetQuality": 0.689,
            "InvestmentCost": 0.723,
            "PerShareFundamentals": 0.691
        }
    },
    "pillar_weights": {
        "Profitability": 0.25,
        "Liquidity": 0.20,
        "Efficiency": 0.15,
        "Solvency": 0.15,
        "AssetQuality": 0.10,
        "InvestmentCost": 0.10,
        "PerShareFundamentals": 0.05
    }
}
```

**Output Format**:

```python
{
    "financial_indices": {
        "AAPL": {
            "f_index_score": 0.673,  # Final F-Index (0.0 to 1.0)
            "calculation_timestamp": "2024-01-15T10:30:00Z",
            "pillar_breakdown": {
                "Profitability": {"score": 0.764, "weight": 0.25, "contribution": 0.191},
                "Liquidity": {"score": 0.623, "weight": 0.20, "contribution": 0.125},
                # ... other pillars
            },
            "quality_metrics": {
                "data_completeness": 0.96,
                "calculation_confidence": 0.94,
                "historical_volatility": 0.08
            }
        }
    },
    "batch_metadata": {
        "total_companies_processed": 1,
        "successful_calculations": 1,
        "failed_calculations": 0,
        "processing_time_seconds": 0.45
    }
}
```

**Core Functions**:

- `calculate_weighted_index(pillar_scores: Dict, weights: Dict) -> float`
- `validate_weight_consistency(weights: Dict) -> bool`
- `generate_index_breakdown(pillar_scores: Dict, weights: Dict) -> Dict`
- `batch_calculate_indices(companies_pillars: Dict, weights: Dict) -> Dict`

### Data Flow Architecture

**Processing Pipeline**:

1. `FinancialDataIngester` → Raw financial data from external sources
2. `MetricNormalizer` → Normalized metrics (0-1 scale) with outlier handling
3. `PillarScorer` → Pillar-level scores with weighted metric aggregation
4. `IndexAggregator` → Final F-Index scores with quality metrics

**Error Handling Strategy**:

- Each module implements circuit breaker patterns for external API failures
- Graceful degradation when partial data is available
- Comprehensive logging and error reporting for debugging
- Fallback mechanisms for critical calculations

### Integration Interfaces

**Oracle Data Pipeline Interface**:

```python
def get_f_index_for_oracle(company_ids: List[str]) -> Dict:
    """
    Returns F-Index data formatted for oracle consumption
    """
    return {
        "data_type": "financial_index",
        "version": "1.0",
        "timestamp": "2024-01-15T10:30:00Z",
        "companies": {
            "AAPL": {
                "f_index": 0.673,
                "confidence": 0.94,
                "last_updated": "2024-01-15T10:30:00Z"
            }
        }
    }
```

**Configuration Management**:

- All weights, boundaries, and parameters stored in versioned configuration files
- Hot-reload capability for configuration changes
- Audit trail for all parameter modifications
- A/B testing support for configuration variations

## 3. Sentiment Index Subsystem

### Overview

The Sentiment Index Subsystem calculates a normalized sentiment score (S-Index) for each company based on real-time and periodic data from social media, news, search trends, and brand perception sources. The S-Index ranges from 0.0 to 1.0, where 1.0 represents the most positive sentiment relative to the analyzed universe of companies.

**Primary Purpose**: Generate standardized sentiment scores for S-Token price determination and oracle data pipeline consumption.

### Module Architecture

#### 3.1 Multi-Source Data Ingestion Module

**Module Name**: `SentimentDataIngester`

**Input Requirements**:

```python
{
    "data_sources": [
        {
            "source_type": "social_media",
            "platform": "twitter",
            "api_config": {
                "endpoint": "https://api.twitter.com/2/tweets/search/recent",
                "authentication": {"bearer_token": "xxx"},
                "rate_limit": 300,  # requests per 15 minutes
                "max_results": 100
            },
            "search_parameters": {
                "query_template": "($TICKER OR $COMPANY_NAME) -is:retweet lang:en",
                "time_window_hours": 24,
                "include_metrics": ["public_metrics", "author_metrics"]
            }
        },
        {
            "source_type": "news",
            "platform": "news_api",
            "api_config": {
                "endpoint": "https://newsapi.org/v2/everything",
                "authentication": {"api_key": "xxx"},
                "rate_limit": 1000
            },
            "search_parameters": {
                "query_template": "($COMPANY_NAME OR $TICKER) AND (earnings OR revenue OR stock OR financial)",
                "time_window_hours": 24,
                "domains": ["reuters.com", "bloomberg.com", "cnbc.com", "marketwatch.com"]
            }
        }
    ],
    "companies": [
        {
            "company_id": "AAPL",
            "company_name": "Apple Inc.",
            "search_terms": ["Apple", "AAPL", "iPhone", "Tim Cook"],
            "excluded_terms": ["apple fruit", "apple tree"]
        }
    ]
}
```

**Output Format**:

```python
{
    "raw_sentiment_data": {
        "AAPL": {
            "social_media": {
                "twitter": {
                    "posts": [
                        {
                            "id": "1234567890",
                            "text": "Apple's new iPhone is amazing! $AAPL to the moon 🚀",
                            "timestamp": "2024-01-15T10:30:00Z",
                            "author_id": "user123",
                            "engagement": {
                                "likes": 45,
                                "retweets": 12,
                                "replies": 8,
                                "views": 2100
                            },
                            "author_metrics": {
                                "followers": 15000,
                                "verified": false,
                                "influence_score": 0.65
                            }
                        }
                    ],
                    "collection_metadata": {
                        "total_posts": 1247,
                        "collection_start": "2024-01-15T10:00:00Z",
                        "collection_end": "2024-01-15T11:00:00Z",
                        "api_calls_used": 15
                    }
                }
            },
            "news": {
                "articles": [
                    {
                        "id": "news_001",
                        "title": "Apple Reports Strong Q4 Earnings",
                        "content": "Apple Inc. reported quarterly earnings...",
                        "timestamp": "2024-01-15T08:00:00Z",
                        "source": "reuters.com",
                        "author": "John Smith",
                        "engagement": {
                            "shares": 230,
                            "comments": 45
                        }
                    }
                ],
                "collection_metadata": {
                    "total_articles": 156,
                    "collection_timespan": "24h",
                    "sources_covered": 12
                }
            }
        }
    },
    "ingestion_quality": {
        "total_companies": 1,
        "successful_collections": 1,
        "failed_collections": 0,
        "data_freshness_minutes": 5
    }
}
```

**Core Functions**:

- `collect_social_media_data(company: Dict, platform_config: Dict) -> Dict`
- `collect_news_data(company: Dict, news_config: Dict) -> Dict`
- `collect_search_trends(company: Dict, search_config: Dict) -> Dict`
- `validate_content_relevance(content: str, company_terms: List[str]) -> float`

#### 3.2 NLP Processing Module

**Module Name**: `SentimentAnalyzer`

**Input Requirements**:

```python
{
    "text_data": {
        "AAPL": {
            "social_posts": [
                {
                    "text": "Apple's new iPhone is amazing! $AAPL to the moon 🚀",
                    "metadata": {
                        "platform": "twitter",
                        "timestamp": "2024-01-15T10:30:00Z",
                        "engagement_score": 0.75,
                        "author_influence": 0.65
                    }
                }
            ],
            "news_articles": [
                {
                    "title": "Apple Reports Strong Q4 Earnings",
                    "content": "Apple Inc. reported quarterly earnings...",
                    "metadata": {
                        "source": "reuters.com",
                        "timestamp": "2024-01-15T08:00:00Z",
                        "credibility_score": 0.95
                    }
                }
            ]
        }
    },
    "analysis_config": {
        "sentiment_model": {
            "type": "transformer",  # "vader", "textblob", "transformer"
            "model_name": "cardiffnlp/twitter-roberta-base-sentiment-latest",
            "confidence_threshold": 0.7
        },
        "preprocessing": {
            "remove_urls": true,
            "remove_mentions": false,
            "normalize_text": true,
            "filter_languages": ["en"]
        }
    }
}
```

**Output Format**:

```python
{
    "sentiment_analysis": {
        "AAPL": {
            "social_sentiment": {
                "individual_scores": [
                    {
                        "text": "Apple's new iPhone is amazing! $AAPL to the moon 🚀",
                        "sentiment": {
                            "polarity": 0.85,  # -1 to 1 scale
                            "confidence": 0.92,
                            "classification": "positive",
                            "emotional_intensity": 0.78
                        },
                        "weighted_score": 0.64,  # Adjusted for engagement and author influence
                        "metadata": {
                            "platform": "twitter",
                            "processing_time_ms": 45
                        }
                    }
                ],
                "aggregated_metrics": {
                    "average_sentiment": 0.72,
                    "sentiment_distribution": {
                        "positive": 0.65,
                        "neutral": 0.25,
                        "negative": 0.10
                    },
                    "volume_metrics": {
                        "total_posts": 1247,
                        "engagement_weighted_volume": 8456
                    }
                }
            },
            "news_sentiment": {
                "individual_scores": [
                    {
                        "title": "Apple Reports Strong Q4 Earnings",
                        "sentiment": {
                            "polarity": 0.65,
                            "confidence": 0.88,
                            "classification": "positive"
                        },
                        "weighted_score": 0.62,  # Adjusted for source credibility
                        "metadata": {
                            "source": "reuters.com",
                            "analysis_type": "title_and_content"
                        }
                    }
                ],
                "aggregated_metrics": {
                    "average_sentiment": 0.68,
                    "sentiment_distribution": {
                        "positive": 0.70,
                        "neutral": 0.20,
                        "negative": 0.10
                    },
                    "volume_metrics": {
                        "total_articles": 156,
                        "credibility_weighted_volume": 942
                    }
                }
            }
        }
    },
    "processing_metadata": {
        "total_texts_processed": 1403,
        "processing_time_seconds": 12.5,
        "model_performance": {
            "average_confidence": 0.89,
            "low_confidence_items": 23
        }
    }
}
```

**Core Functions**:

- `analyze_text_sentiment(text: str, model_config: Dict) -> Dict`
- `preprocess_text(text: str, preprocessing_config: Dict) -> str`
- `calculate_engagement_weight(engagement_metrics: Dict) -> float`
- `batch_sentiment_analysis(texts: List[Dict], config: Dict) -> Dict`

#### 3.3 Trend Analysis Module

**Module Name**: `TrendAnalyzer`

**Input Requirements**:

```python
{
    "search_trend_data": {
        "AAPL": {
            "google_trends": {
                "search_volume": [
                    {"date": "2024-01-14", "volume": 85, "related_queries": ["apple stock", "aapl price"]},
                    {"date": "2024-01-15", "volume": 92, "related_queries": ["apple earnings", "iphone sales"]}
                ],
                "geographic_data": {
                    "US": 0.85,
                    "CN": 0.12,
                    "EU": 0.67
                }
            },
            "social_volume": {
                "twitter": {"mentions_per_hour": 234, "trending_hashtags": ["#AAPL", "#Apple"]},
                "reddit": {"posts_per_hour": 12, "upvote_ratio": 0.78}
            }
        }
    },
    "historical_baselines": {
        "AAPL": {
            "average_search_volume": 78,
            "average_social_mentions": 198,
            "volatility_metrics": {
                "search_volatility": 0.15,
                "social_volatility": 0.28
            }
        }
    }
}
```

**Output Format**:

```python
{
    "trend_analysis": {
        "AAPL": {
            "search_trend_score": 0.76,  # 0-1 normalized score
            "social_volume_score": 0.82,
            "viral_factor_score": 0.34,
            "trend_components": {
                "search_momentum": {
                    "current_vs_baseline": 1.18,  # 18% above baseline
                    "growth_rate": 0.08,  # 8% growth rate
                    "geographic_spread": 0.71
                },
                "social_momentum": {
                    "mention_velocity": 1.28,
                    "engagement_growth": 0.15,
                    "reach_expansion": 0.92
                },
                "viral_indicators": {
                    "hashtag_emergence": 0.45,
                    "influencer_adoption": 0.23,
                    "cross_platform_spread": 0.34
                }
            },
            "quality_metrics": {
                "data_completeness": 0.94,
                "trend_confidence": 0.87,
                "anomaly_detection": {
                    "unusual_spikes": 0,
                    "bot_activity_detected": false
                }
            }
        }
    }
}
```

**Core Functions**:

- `calculate_search_trend_score(search_data: Dict, baseline: Dict) -> float`
- `analyze_social_volume_trends(social_data: Dict, baseline: Dict) -> Dict`
- `detect_viral_factors(trend_data: Dict) -> float`
- `normalize_trend_metrics(raw_trends: Dict, historical_context: Dict) -> Dict`

#### 3.4 Sentiment Aggregation Module

**Module Name**: `SentimentAggregator`

**Input Requirements**:

```python
{
    "component_scores": {
        "AAPL": {
            "social_sentiment": 0.72,
            "news_sentiment": 0.68,
            "search_trend_score": 0.76,
            "brand_perception_score": 0.71,
            "viral_factor_score": 0.34
        }
    },
    "component_weights": {
        "social_sentiment": 0.35,
        "news_sentiment": 0.25,
        "search_trend_score": 0.20,
        "brand_perception_score": 0.15,
        "viral_factor_score": 0.05
    },
    "time_decay_factors": {
        "social_sentiment": 0.95,  # 5% decay per hour
        "news_sentiment": 0.98,    # 2% decay per hour
        "search_trend_score": 0.92,
        "brand_perception_score": 0.99,
        "viral_factor_score": 0.85
    }
}
```

**Output Format**:

```python
{
    "sentiment_indices": {
        "AAPL": {
            "s_index_score": 0.698,  # Final S-Index (0.0 to 1.0)
            "calculation_timestamp": "2024-01-15T10:30:00Z",
            "component_breakdown": {
                "social_sentiment": {"score": 0.72, "weight": 0.35, "contribution": 0.252},
                "news_sentiment": {"score": 0.68, "weight": 0.25, "contribution": 0.170},
                "search_trend_score": {"score": 0.76, "weight": 0.20, "contribution": 0.152},
                "brand_perception_score": {"score": 0.71, "weight": 0.15, "contribution": 0.107},
                "viral_factor_score": {"score": 0.34, "weight": 0.05, "contribution": 0.017}
            },
            "quality_metrics": {
                "data_completeness": 0.91,
                "calculation_confidence": 0.89,
                "temporal_stability": 0.82,
                "source_diversity": 0.95
            },
            "historical_context": {
                "percentile_rank": 0.76,  # 76th percentile historically
                "volatility_score": 0.28,
                "trend_direction": "positive",
                "momentum_strength": 0.65
            }
        }
    },
    "batch_metadata": {
        "total_companies_processed": 1,
        "successful_calculations": 1,
        "failed_calculations": 0,
        "processing_time_seconds": 2.1
    }
}
```

**Core Functions**:

- `calculate_weighted_sentiment(component_scores: Dict, weights: Dict) -> float`
- `apply_time_decay(scores: Dict, decay_factors: Dict, time_elapsed: float) -> Dict`
- `validate_sentiment_consistency(historical_scores: List[float], current_score: float) -> Dict`
- `generate_sentiment_breakdown(components: Dict, weights: Dict) -> Dict`

### Data Flow Architecture

**Processing Pipeline**:

1. `SentimentDataIngester` → Raw social media, news, and trend data from multiple sources
2. `SentimentAnalyzer` → NLP-processed sentiment scores with confidence metrics
3. `TrendAnalyzer` → Volume and viral trend analysis with historical context
4. `SentimentAggregator` → Final S-Index scores with component breakdowns

**Real-time vs Batch Processing**:

- **Real-time**: Social media sentiment (streaming APIs, 5-minute updates)
- **Hourly**: News sentiment and search trends
- **Daily**: Brand perception and viral factor analysis
- **Weekly**: Historical baseline recalculation

### Integration Interfaces

**Oracle Data Pipeline Interface**:

```python
def get_s_index_for_oracle(company_ids: List[str]) -> Dict:
    """
    Returns S-Index data formatted for oracle consumption
    """
    return {
        "data_type": "sentiment_index",
        "version": "1.0",
        "timestamp": "2024-01-15T10:30:00Z",
        "companies": {
            "AAPL": {
                "s_index": 0.698,
                "confidence": 0.89,
                "last_updated": "2024-01-15T10:30:00Z",
                "volatility_warning": false
            }
        }
    }
```

**Configuration Management**:

- Dynamic model switching (VADER → Transformer → Custom models)
- Real-time weight adjustments through governance
- Source reliability scoring and automatic filtering
- A/B testing framework for sentiment models

### Quality Assurance & Monitoring

**Data Quality Metrics**:

- Source reliability tracking and scoring
- Spam and bot detection algorithms
- Content relevance validation
- Temporal consistency monitoring

**Model Performance Monitoring**:

- Sentiment classification accuracy tracking
- Confidence score distributions
- Model drift detection and alerting
- Human-in-the-loop validation sampling

## 4. Oracle Data Pipeline Architecture

### Overview

- Decentralized oracle network responsible for collecting, validating, and submitting F-Index and S-Index data to on-chain smart contracts.
- Ensures data integrity through multi-node consensus and cryptographic validation.
- Optimized for gas efficiency and high availability with redundancy and failover mechanisms.

### Oracle Node Network

- **Minimum Configuration**: 7 oracle nodes for MVP deployment
- **Node Roles**:
  - **Data Collector Nodes**: Gather raw data from Financial and Sentiment Index subsystems
  - **Validator Nodes**: Cross-validate collected data and perform integrity checks
  - **Aggregator Nodes**: Normalize and aggregate validated data for on-chain submission
  - **Coordinator Node**: Orchestrates the consensus process and manages node communication
- **Node Distribution**: Geographically distributed to prevent single points of failure
- **Hardware Requirements**: Minimum 4GB RAM, 100GB storage, stable internet connection

### Core Services Architecture

#### Data Retrieval Service

- **Financial Data Fetcher**: Polls Financial Index subsystem for latest F-Index scores
- **Sentiment Data Fetcher**: Retrieves S-Index scores from Sentiment Index subsystem
- **Update Scheduler**: Manages data collection frequency (hourly for S-Index, daily for F-Index)
- **Data Validation**: Performs initial sanity checks on collected data (range validation, format verification)

#### Validation Engine

- **Cross-Node Verification**: Compares data across multiple oracle nodes
- **Anomaly Detection**: Identifies outliers and potential data manipulation attempts
- **Historical Consistency**: Validates against previous submissions for trend analysis
- **Signature Verification**: Ensures data authenticity through cryptographic signatures

#### Data Normalization Module

- **Format Standardization**: Converts data to blockchain-compatible formats
- **Precision Adjustment**: Handles floating-point precision for smart contract compatibility
- **Batch Preparation**: Groups multiple company updates for efficient gas usage
- **Timestamp Synchronization**: Ensures consistent timing across all submissions

### Consensus Mechanism

#### Agreement Protocol

- **Threshold**: 5 out of 7 nodes must agree for data submission (71% majority)
- **Voting Process**:
  1. Each node submits data hash and signature
  2. Cross-validation of submitted hashes
  3. Majority consensus determination
  4. Final data package preparation
- **Conflict Resolution**: When consensus fails, nodes re-fetch data and retry up to 3 times
- **Tie-Breaking**: Coordinator node provides casting vote in edge cases

#### Security Measures

- **Node Authentication**: Each node maintains unique cryptographic identity
- **Stake Requirements**: Nodes must stake tokens to participate (slashing for misbehavior)
- **Reputation System**: Track node reliability and accuracy over time
- **Rotation Policy**: Periodic node rotation to prevent long-term manipulation

### Blockchain Interface

#### Smart Contract Integration

- **Contract Endpoints**:
  - `updateTokenPrices(companyIds, fIndexes, sIndexes, timestamp, signatures)`
  - `submitBatchUpdate(batchData, merkleRoot, proofs)`
  - `emergencyPause()` for circuit breaker activation
- **Data Submission Format**:
  ```solidity
  struct OracleUpdate {
      bytes32 companyId;
      uint256 fIndex;      // F-Index score (0-100000 for precision)
      uint256 sIndex;      // S-Index score (0-100000 for precision)
      uint256 timestamp;
      bytes32 dataHash;
      bytes[] signatures;  // Multi-signature validation
  }
  ```

#### Transaction Management

- **Gas Optimization**:
  - Batch multiple company updates in single transaction
  - Use CREATE2 for deterministic contract addresses
  - Implement meta-transactions for gas-less user interactions
- **Priority Scheduling**: High-priority updates (significant price changes) submitted immediately
- **Retry Logic**: Failed transactions automatically retried with adjusted gas prices

### Gas Optimization Strategies

#### Batching and Aggregation

- **Company Grouping**: Update multiple companies in single transaction (up to 50 per batch)
- **Time-based Batching**: Collect updates over 15-minute windows for efficiency
- **Merkle Tree Proofs**: Use Merkle trees for efficient batch verification
- **Data Compression**: Compress repetitive data using lookup tables

#### Layer 2 Integration

- **Polygon Integration**: Deploy oracle contracts on Polygon for reduced gas costs
- **State Channels**: Use payment channels for frequent micro-updates
- **Rollup Compatibility**: Design for future Optimistic/ZK rollup deployment
- **Cross-chain Bridges**: Enable multi-chain oracle data availability

### Monitoring and Alerting

#### Performance Metrics

- **Uptime Tracking**: Monitor node availability and response times
- **Consensus Success Rate**: Track successful consensus achievement
- **Gas Usage Analytics**: Monitor and optimize transaction costs
- **Data Latency**: Measure time from data generation to on-chain submission

#### Alert Systems

- **Node Failure Detection**: Immediate alerts for offline nodes
- **Consensus Failures**: Escalation procedures for failed consensus attempts
- **Anomaly Detection**: Alerts for unusual data patterns or potential attacks
- **Gas Price Spikes**: Dynamic gas management during network congestion

### Redundancy and Failover

#### High Availability Design

- **Backup Nodes**: Additional standby nodes ready for activation
- **Data Replication**: Cross-node data synchronization and backup
- **Geographic Distribution**: Nodes distributed across multiple regions
- **Load Balancing**: Dynamic routing of requests across healthy nodes

#### Emergency Protocols

- **Circuit Breaking**: Automatic system pause during detected anomalies
- **Manual Override**: Governance-controlled emergency interventions
- **Data Recovery**: Procedures for recovering from node failures or data corruption
- **Rollback Mechanisms**: Ability to revert problematic submissions

### Integration Points

- **Financial Index Interface**: Direct connection to F-Index calculation engine
- **Sentiment Index Interface**: Real-time data feeds from S-Index pipeline
- **Smart Contract Communication**: Secure channels to F-Token and S-Token contracts
- **Governance Integration**: DAO-controlled parameter adjustments and node management

### Technology Stack

- **Backend**: Python/Node.js for oracle node implementation
- **Blockchain**: Web3.py/Ethers.js for smart contract interaction
- **Database**: PostgreSQL for data persistence and Redis for caching
- **Message Queue**: RabbitMQ/Apache Kafka for inter-node communication
- **Monitoring**: Prometheus + Grafana for metrics and alerting
- **Security**: HashiCorp Vault for key management

## 5. Token Smart Contracts Suite

### Overview

The Token Smart Contracts Suite implements the dual-token economic model through F-Token and S-Token contracts. These contracts handle token lifecycle management, oracle data integration, price updates, and governance mechanisms while maintaining ERC20 compatibility and upgradeable architecture.

**Primary Purpose**: Provide on-chain token infrastructure that responds to F-Index and S-Index data from the Oracle Data Pipeline to enable real-time token price adjustments based on company financial and sentiment performance.

### Contract Architecture

#### 5.1 F-Token Contract (Financial Token)

**Contract Name**: `FToken.sol`

**Core Responsibilities**:

- Represents tokenized exposure to company financial performance
- Receives F-Index data from Oracle Data Pipeline
- Implements dynamic pricing based on financial metrics
- Manages token minting, burning, and transfers
- Integrates with governance mechanisms

**State Variables**:

```solidity
contract FToken is ERC20Upgradeable, OwnableUpgradeable, PausableUpgradeable {
    // Company and pricing data
    struct CompanyData {
        bytes32 companyId;           // Unique company identifier
        uint256 fIndex;              // Financial Index (0-100000 for precision)
        uint256 basePrice;           // Base token price in wei
        uint256 lastUpdate;          // Last oracle update timestamp
        uint256 totalSupply;         // Company-specific token supply
        bool isActive;               // Company status flag
    }

    // Storage mappings
    mapping(bytes32 => CompanyData) public companies;
    mapping(address => mapping(bytes32 => uint256)) public userBalances;
    mapping(bytes32 => address[]) public companyHolders;

    // Oracle and governance addresses
    address public oracleAddress;
    address public governanceAddress;
    address public treasuryAddress;

    // Economic parameters
    uint256 public volatilityFactor;     // Price volatility multiplier
    uint256 public mintingFee;           // Fee for minting tokens (basis points)
    uint256 public burningFee;           // Fee for burning tokens (basis points)
    uint256 public maxSupplyPerCompany;  // Maximum tokens per company

    // Circuit breaker parameters
    uint256 public maxPriceChange;       // Maximum price change per update (basis points)
    uint256 public emergencyThreshold;   // Threshold for emergency pause
    bool public emergencyPaused;         // Emergency pause state

    // Events
    event CompanyAdded(bytes32 indexed companyId, uint256 basePrice);
    event PriceUpdated(bytes32 indexed companyId, uint256 oldPrice, uint256 newPrice, uint256 fIndex);
    event TokensMinted(bytes32 indexed companyId, address indexed user, uint256 amount, uint256 price);
    event TokensBurned(bytes32 indexed companyId, address indexed user, uint256 amount, uint256 price);
    event EmergencyPaused(string reason);
    event OracleUpdated(address oldOracle, address newOracle);
}
```

**Core Functions**:

```solidity
// Company management
function addCompany(
    bytes32 companyId,
    uint256 basePrice,
    uint256 initialSupply
) external onlyGovernance;

function removeCompany(bytes32 companyId) external onlyGovernance;

function pauseCompany(bytes32 companyId) external onlyGovernance;

// Oracle integration
function updateFIndex(
    bytes32[] calldata companyIds,
    uint256[] calldata fIndexes,
    uint256 timestamp,
    bytes[] calldata signatures
) external onlyOracle {
    require(companyIds.length == fIndexes.length, "Array length mismatch");
    require(_verifyOracleSignatures(companyIds, fIndexes, timestamp, signatures), "Invalid signatures");

    for (uint256 i = 0; i < companyIds.length; i++) {
        _updateCompanyPrice(companyIds[i], fIndexes[i], timestamp);
    }
}

// Token operations
function mintTokens(
    bytes32 companyId,
    uint256 amount
) external payable whenNotPaused returns (uint256 totalCost) {
    require(companies[companyId].isActive, "Company not active");
    require(amount > 0, "Amount must be positive");

    uint256 currentPrice = calculateCurrentPrice(companyId);
    uint256 fee = (currentPrice * amount * mintingFee) / 10000;
    totalCost = (currentPrice * amount) + fee;

    require(msg.value >= totalCost, "Insufficient payment");
    require(companies[companyId].totalSupply + amount <= maxSupplyPerCompany, "Exceeds max supply");

    userBalances[msg.sender][companyId] += amount;
    companies[companyId].totalSupply += amount;

    if (userBalances[msg.sender][companyId] == amount) {
        companyHolders[companyId].push(msg.sender);
    }

    // Send excess back to user
    if (msg.value > totalCost) {
        payable(msg.sender).transfer(msg.value - totalCost);
    }

    emit TokensMinted(companyId, msg.sender, amount, currentPrice);
    return totalCost;
}

function burnTokens(
    bytes32 companyId,
    uint256 amount
) external whenNotPaused returns (uint256 payout) {
    require(userBalances[msg.sender][companyId] >= amount, "Insufficient balance");
    require(amount > 0, "Amount must be positive");

    uint256 currentPrice = calculateCurrentPrice(companyId);
    uint256 fee = (currentPrice * amount * burningFee) / 10000;
    payout = (currentPrice * amount) - fee;

    userBalances[msg.sender][companyId] -= amount;
    companies[companyId].totalSupply -= amount;

    payable(msg.sender).transfer(payout);
    payable(treasuryAddress).transfer(fee);

    emit TokensBurned(companyId, msg.sender, amount, currentPrice);
    return payout;
}

// Price calculation
function calculateCurrentPrice(bytes32 companyId) public view returns (uint256) {
    CompanyData memory company = companies[companyId];
    if (!company.isActive) return 0;

    // Price = basePrice * (1 + (fIndex - 50000) / 50000 * volatilityFactor)
    // fIndex is normalized to 0-100000, so 50000 represents neutral
    int256 indexDeviation = int256(company.fIndex) - 50000;
    int256 priceMultiplier = 100000 + (indexDeviation * int256(volatilityFactor)) / 50000;

    if (priceMultiplier < 10000) priceMultiplier = 10000; // Minimum 10% of base price
    if (priceMultiplier > 300000) priceMultiplier = 300000; // Maximum 300% of base price

    return (company.basePrice * uint256(priceMultiplier)) / 100000;
}

// Governance functions
function setVolatilityFactor(uint256 newFactor) external onlyGovernance;
function setFees(uint256 newMintingFee, uint256 newBurningFee) external onlyGovernance;
function setOracleAddress(address newOracle) external onlyGovernance;
function emergencyPause(string calldata reason) external onlyGovernance;
```

#### 5.2 S-Token Contract (Sentiment Token)

**Contract Name**: `SToken.sol`

**Core Responsibilities**:

- Represents tokenized exposure to company sentiment performance
- Receives S-Index data from Oracle Data Pipeline
- Implements dynamic pricing based on sentiment metrics
- Manages token minting, burning, and transfers with higher volatility
- Integrates with social sentiment decay mechanisms

**State Variables**:

```solidity
contract SToken is ERC20Upgradeable, OwnableUpgradeable, PausableUpgradeable {
    // Company and sentiment data
    struct CompanyData {
        bytes32 companyId;           // Unique company identifier
        uint256 sIndex;              // Sentiment Index (0-100000 for precision)
        uint256 basePrice;           // Base token price in wei
        uint256 lastUpdate;          // Last oracle update timestamp
        uint256 totalSupply;         // Company-specific token supply
        uint256 volatilityScore;     // Current sentiment volatility
        uint256 decayRate;           // Sentiment decay rate per hour
        bool isActive;               // Company status flag
    }

    // Similar storage mappings as FToken but with sentiment-specific fields
    mapping(bytes32 => CompanyData) public companies;
    mapping(address => mapping(bytes32 => uint256)) public userBalances;
    mapping(bytes32 => uint256) public lastDecayUpdate;

    // Sentiment-specific parameters
    uint256 public sentimentVolatilityMultiplier;  // Higher volatility than F-Token
    uint256 public viralBoostFactor;               // Boost for viral content
    uint256 public sentimentDecayRate;             // Base decay rate for sentiment
    uint256 public maxSentimentChange;             // Maximum sentiment change per update

    // Events
    event SentimentUpdated(bytes32 indexed companyId, uint256 oldSIndex, uint256 newSIndex, uint256 volatility);
    event ViralBoostApplied(bytes32 indexed companyId, uint256 boostFactor);
    event SentimentDecayApplied(bytes32 indexed companyId, uint256 decayAmount);
}
```

**Core Functions**:

```solidity
// Sentiment-specific oracle integration
function updateSIndex(
    bytes32[] calldata companyIds,
    uint256[] calldata sIndexes,
    uint256[] calldata volatilityScores,
    uint256 timestamp,
    bytes[] calldata signatures
) external onlyOracle;

// Price calculation with sentiment volatility
function calculateCurrentPrice(bytes32 companyId) public view returns (uint256) {
    CompanyData memory company = companies[companyId];
    if (!company.isActive) return 0;

    // Apply time-based sentiment decay
    uint256 decayAmount = _calculateSentimentDecay(companyId);
    uint256 adjustedSIndex = company.sIndex > decayAmount ? company.sIndex - decayAmount : 0;

    // Higher volatility multiplier for sentiment
    int256 indexDeviation = int256(adjustedSIndex) - 50000;
    int256 priceMultiplier = 100000 + (indexDeviation * int256(sentimentVolatilityMultiplier)) / 50000;

    // Apply volatility boost based on current sentiment volatility
    uint256 volatilityBoost = (company.volatilityScore * viralBoostFactor) / 100000;
    priceMultiplier += int256(volatilityBoost);

    if (priceMultiplier < 5000) priceMultiplier = 5000;   // Minimum 5% (more volatile than F-Token)
    if (priceMultiplier > 500000) priceMultiplier = 500000; // Maximum 500% (more volatile than F-Token)

    return (company.basePrice * uint256(priceMultiplier)) / 100000;
}

// Sentiment decay mechanism
function _calculateSentimentDecay(bytes32 companyId) internal view returns (uint256) {
    uint256 timeSinceUpdate = block.timestamp - lastDecayUpdate[companyId];
    uint256 hoursSinceUpdate = timeSinceUpdate / 3600; // Convert to hours

    return (companies[companyId].decayRate * hoursSinceUpdate * companies[companyId].sIndex) / 100000;
}

function applySentimentDecay(bytes32 companyId) external {
    require(block.timestamp > lastDecayUpdate[companyId] + 3600, "Too soon for decay");

    uint256 decayAmount = _calculateSentimentDecay(companyId);
    if (decayAmount > 0) {
        companies[companyId].sIndex = companies[companyId].sIndex > decayAmount
            ? companies[companyId].sIndex - decayAmount
            : 0;
        lastDecayUpdate[companyId] = block.timestamp;

        emit SentimentDecayApplied(companyId, decayAmount);
    }
}
```

#### 5.3 Governance Contract

**Contract Name**: `TokenGovernance.sol`

**Core Responsibilities**:

- Manages governance proposals and voting
- Controls parameter updates for both F-Token and S-Token
- Handles oracle management and emergency controls
- Implements DAO voting mechanisms

**State Variables**:

```solidity
contract TokenGovernance is GovernorUpgradeable, GovernorVotesUpgradeable {
    struct Proposal {
        uint256 id;
        address proposer;
        string description;
        bytes32 targetContract;      // 'FTOKEN', 'STOKEN', 'ORACLE'
        bytes callData;
        uint256 votingPeriod;
        uint256 executionTime;
        ProposalState state;
    }

    // Voting parameters
    uint256 public proposalThreshold;     // Minimum tokens needed to propose
    uint256 public votingDelay;           // Delay before voting starts
    uint256 public votingPeriod;          // Voting duration
    uint256 public quorumPercentage;      // Minimum participation for validity

    // Contract addresses
    address public fTokenAddress;
    address public sTokenAddress;
    address public oracleAddress;

    // Governance token (for voting rights)
    IERC20 public governanceToken;

    mapping(uint256 => Proposal) public proposals;
    mapping(address => uint256) public votingPower;
}
```

**Core Functions**:

```solidity
// Proposal management
function propose(
    string calldata description,
    bytes32 targetContract,
    bytes calldata callData
) external returns (uint256 proposalId);

function vote(uint256 proposalId, bool support) external;

function execute(uint256 proposalId) external;

// Parameter management
function updateTokenParameters(
    bytes32 tokenType,  // 'FTOKEN' or 'STOKEN'
    bytes calldata parameterData
) external onlyGovernance;

// Emergency controls
function emergencyPause(bytes32 tokenType, string calldata reason) external;
function emergencyUnpause(bytes32 tokenType) external;
```

#### 5.4 Oracle Integration Contract

**Contract Name**: `OracleIntegration.sol`

**Core Responsibilities**:

- Validates oracle signatures and data integrity
- Implements circuit breakers for anomalous data
- Manages oracle node authentication
- Handles batch updates and gas optimization

**State Variables**:

```solidity
contract OracleIntegration is OwnableUpgradeable, PausableUpgradeable {
    struct OracleNode {
        address nodeAddress;
        bytes32 nodeId;
        uint256 reputation;
        bool isActive;
        uint256 lastUpdate;
    }

    struct DataUpdate {
        bytes32 companyId;
        uint256 fIndex;
        uint256 sIndex;
        uint256 timestamp;
        bytes32 dataHash;
    }

    // Oracle management
    mapping(address => OracleNode) public oracleNodes;
    mapping(bytes32 => uint256) public lastUpdateTimestamp;
    address[] public activeNodes;

    // Consensus parameters
    uint256 public consensusThreshold;    // Minimum nodes needed for consensus
    uint256 public maxPriceDeviation;     // Maximum allowed price deviation
    uint256 public updateFrequency;       // Minimum time between updates

    // Circuit breaker parameters
    uint256 public anomalyThreshold;      // Threshold for detecting anomalies
    bool public circuitBreakerActive;     // Circuit breaker state
}
```

**Core Functions**:

```solidity
// Oracle validation
function verifyOracleSignatures(
    DataUpdate[] calldata updates,
    bytes[] calldata signatures
) external view returns (bool);

function submitBatchUpdate(
    DataUpdate[] calldata updates,
    bytes[] calldata signatures
) external onlyActiveOracle;

// Circuit breaker
function checkAnomalyThreshold(
    bytes32 companyId,
    uint256 newValue,
    uint256 oldValue
) internal view returns (bool);

function activateCircuitBreaker(string calldata reason) external;
```

### ERC20 Compatibility and Extensions

**Standard Compliance**:

- Full ERC20 compatibility for both F-Token and S-Token
- ERC20Upgradeable pattern for future improvements
- Support for ERC20 approve/transfer mechanisms
- Integration with existing DeFi protocols

**Extensions Implemented**:

```solidity
// ERC20 extensions
contract TokenExtensions {
    // Metadata extension
    function name() public view returns (string memory);
    function symbol() public view returns (string memory);
    function decimals() public view returns (uint8);

    // Burnable extension
    function burn(uint256 amount) public;
    function burnFrom(address account, uint256 amount) public;

    // Pausable extension
    function pause() public onlyRole(PAUSER_ROLE);
    function unpause() public onlyRole(PAUSER_ROLE);

    // Snapshot extension (for governance)
    function snapshot() public onlyRole(SNAPSHOT_ROLE) returns (uint256);
    function balanceOfAt(address account, uint256 snapshotId) public view returns (uint256);
    function totalSupplyAt(uint256 snapshotId) public view returns (uint256);
}
```

### Access Control and Security Patterns

**Role-Based Access Control**:

```solidity
// Access control roles
bytes32 public constant ORACLE_ROLE = keccak256("ORACLE_ROLE");
bytes32 public constant GOVERNANCE_ROLE = keccak256("GOVERNANCE_ROLE");
bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");
bytes32 public constant UPGRADER_ROLE = keccak256("UPGRADER_ROLE");

// Modifiers
modifier onlyOracle() {
    require(hasRole(ORACLE_ROLE, msg.sender), "Caller is not an oracle");
    _;
}

modifier onlyGovernance() {
    require(hasRole(GOVERNANCE_ROLE, msg.sender), "Caller is not governance");
    _;
}
```

**Security Patterns**:

- ReentrancyGuard for token operations
- Pausable functionality for emergency stops
- Circuit breakers for anomalous price changes
- Multi-signature requirements for critical functions
- Time locks for governance changes

### Upgradeability Architecture

**Proxy Pattern Implementation**:

```solidity
// Upgradeable contracts using OpenZeppelin's proxy pattern
contract FTokenV1 is Initializable, ERC20Upgradeable, OwnableUpgradeable {
    function initialize(
        string memory name,
        string memory symbol,
        address governance,
        address oracle
    ) public initializer {
        __ERC20_init(name, symbol);
        __Ownable_init();
        governanceAddress = governance;
        oracleAddress = oracle;
    }
}
```

**Upgrade Process**:

1. Governance proposal for upgrade
2. Community voting period
3. Time-locked execution
4. Migration of critical state
5. Verification and testing period

### Gas Optimization Strategies

**Batch Operations**:

- Batch minting/burning for multiple users
- Batch oracle updates for multiple companies
- Merkle tree proofs for efficient verification

**Storage Optimization**:

- Packed structs to minimize storage slots
- Efficient data structures for mappings
- Gas-optimized loops and iterations

**Function Optimization**:

```solidity
// Gas-optimized batch operations
function batchMintTokens(
    bytes32[] calldata companyIds,
    uint256[] calldata amounts,
    address[] calldata recipients
) external payable returns (uint256[] memory costs) {
    require(companyIds.length == amounts.length && amounts.length == recipients.length, "Length mismatch");

    costs = new uint256[](companyIds.length);
    uint256 totalRequired = 0;

    // Calculate total cost first
    for (uint256 i = 0; i < companyIds.length; i++) {
        costs[i] = calculateMintingCost(companyIds[i], amounts[i]);
        totalRequired += costs[i];
    }

    require(msg.value >= totalRequired, "Insufficient payment");

    // Execute minting
    for (uint256 i = 0; i < companyIds.length; i++) {
        _executeMint(companyIds[i], amounts[i], recipients[i]);
    }

    return costs;
}
```

### Integration with Oracle Data Pipeline

**Data Reception Interface**:

```solidity
interface IOracleReceiver {
    function receiveOracleUpdate(
        bytes32[] calldata companyIds,
        uint256[] calldata fIndexes,
        uint256[] calldata sIndexes,
        uint256 timestamp,
        bytes calldata proof
    ) external;
}
```

**Update Validation**:

- Cryptographic signature verification
- Timestamp validation and ordering
- Data consistency checks
- Circuit breaker activation on anomalies

This comprehensive Token Smart Contracts Suite provides the foundation for the dual-token economic model while maintaining security, upgradeability, and efficient gas usage patterns.

## 6. Price Update Mechanism

### Overview

The Price Update Mechanism orchestrates the flow of F-Index and S-Index data from the Oracle Data Pipeline to on-chain smart contracts, ensuring real-time token price adjustments with high reliability, gas efficiency, and comprehensive safeguards.

**Primary Purpose**: Translate validated oracle data into smart contract state updates while maintaining system stability, cost efficiency, and protection against manipulation or technical failures.

### Update Flow Architecture

#### 6.1 Oracle-to-Contract Update Flow

**Trigger Sources**:

```python
{
    "update_triggers": {
        "scheduled_updates": {
            "f_index_updates": {
                "frequency": "daily",
                "execution_time": "08:00 UTC",
                "batch_size": 50,
                "priority": "normal"
            },
            "s_index_updates": {
                "frequency": "hourly",
                "execution_time": "every hour at :05",
                "batch_size": 30,
                "priority": "normal"
            }
        },
        "event_driven_updates": {
            "significant_change_threshold": 0.05,  # 5% index change
            "viral_content_threshold": 0.80,       # High viral factor
            "earnings_announcement": "immediate",
            "emergency_news": "immediate",
            "priority": "high"
        },
        "governance_updates": {
            "parameter_changes": "immediate",
            "contract_upgrades": "time_locked",
            "emergency_controls": "immediate",
            "priority": "critical"
        }
    }
}
```

**Update Processing Pipeline**:

```python
def process_oracle_update():
    """
    Complete oracle-to-contract update flow
    """
    # Step 1: Data Collection and Validation
    oracle_data = collect_consensus_data()
    validated_data = validate_oracle_signatures(oracle_data)

    # Step 2: Change Detection and Prioritization
    significant_changes = detect_significant_changes(validated_data)
    update_priority = calculate_update_priority(significant_changes)

    # Step 3: Circuit Breaker Checks
    anomaly_check = run_circuit_breaker_analysis(validated_data)
    if anomaly_check.circuit_breaker_triggered:
        trigger_emergency_pause(anomaly_check.reason)
        return {"status": "paused", "reason": anomaly_check.reason}

    # Step 4: Transaction Preparation
    batched_transactions = prepare_batch_transactions(validated_data, update_priority)
    gas_optimized_tx = optimize_transaction_gas(batched_transactions)

    # Step 5: On-chain Submission
    submission_result = submit_to_blockchain(gas_optimized_tx)

    # Step 6: Monitoring and Alerting
    log_update_metrics(submission_result)
    trigger_alerts_if_needed(submission_result)

    return submission_result
```

#### 6.2 Transaction Batching and Scheduling

**Batch Optimization Strategy**:

```solidity
contract PriceUpdateBatcher {
    struct BatchConfig {
        uint256 maxBatchSize;        // Maximum companies per batch
        uint256 maxGasPerBatch;      // Gas limit per batch transaction
        uint256 minTimeBetweenBatches; // Minimum time between batches
        uint256 priorityThreshold;   // Threshold for priority batching
    }

    struct UpdateBatch {
        bytes32[] companyIds;
        uint256[] fIndexes;
        uint256[] sIndexes;
        uint256[] timestamps;
        uint256 batchTimestamp;
        uint256 totalGasEstimate;
        BatchPriority priority;
    }

    enum BatchPriority {
        LOW,      // Regular scheduled updates
        NORMAL,   // Standard updates with moderate changes
        HIGH,     // Significant changes or time-sensitive updates
        CRITICAL  // Emergency updates or governance changes
    }

    mapping(BatchPriority => BatchConfig) public batchConfigs;
    mapping(uint256 => UpdateBatch) public pendingBatches;

    uint256 public nextBatchId;
    uint256 public lastExecutionTime;
}
```

**Scheduling Logic**:

```solidity
function scheduleBatchUpdate(
    bytes32[] calldata companyIds,
    uint256[] calldata fIndexes,
    uint256[] calldata sIndexes,
    BatchPriority priority
) external onlyOracle returns (uint256 batchId) {

    BatchConfig memory config = batchConfigs[priority];

    // Create new batch
    UpdateBatch memory newBatch = UpdateBatch({
        companyIds: companyIds,
        fIndexes: fIndexes,
        sIndexes: sIndexes,
        timestamps: new uint256[](companyIds.length),
        batchTimestamp: block.timestamp,
        totalGasEstimate: _estimateBatchGas(companyIds.length),
        priority: priority
    });

    // Validate batch constraints
    require(companyIds.length <= config.maxBatchSize, "Batch too large");
    require(newBatch.totalGasEstimate <= config.maxGasPerBatch, "Exceeds gas limit");

    // Store batch
    batchId = nextBatchId++;
    pendingBatches[batchId] = newBatch;

    // Schedule execution based on priority
    if (priority == BatchPriority.CRITICAL) {
        _executeImmediately(batchId);
    } else if (priority == BatchPriority.HIGH) {
        _scheduleHighPriority(batchId);
    } else {
        _scheduleNormalExecution(batchId);
    }

    emit BatchScheduled(batchId, companyIds.length, priority);
    return batchId;
}

function executeBatch(uint256 batchId) external {
    UpdateBatch storage batch = pendingBatches[batchId];
    require(batch.companyIds.length > 0, "Batch not found");
    require(_canExecuteBatch(batch), "Execution conditions not met");

    // Execute F-Token updates
    IFToken(fTokenAddress).updateFIndex(
        batch.companyIds,
        batch.fIndexes,
        batch.batchTimestamp,
        _generateSignatures(batch)
    );

    // Execute S-Token updates
    ISToken(sTokenAddress).updateSIndex(
        batch.companyIds,
        batch.sIndexes,
        _calculateVolatilityScores(batch.companyIds),
        batch.batchTimestamp,
        _generateSignatures(batch)
    );

    // Update execution tracking
    lastExecutionTime = block.timestamp;
    delete pendingBatches[batchId];

    emit BatchExecuted(batchId, batch.companyIds.length, block.timestamp);
}
```

#### 6.3 Dynamic Gas Management

**Gas Optimization Module**:

```python
class GasOptimizer:
    def __init__(self):
        self.gas_price_tracker = GasPriceTracker()
        self.network_monitor = NetworkMonitor()
        self.historical_data = GasHistoricalData()

    def optimize_transaction_timing(self, update_batch):
        """
        Determine optimal timing for transaction submission
        """
        current_gas_price = self.gas_price_tracker.get_current_price()
        network_congestion = self.network_monitor.get_congestion_level()

        if update_batch.priority == "critical":
            return {"submit": "immediate", "gas_price": current_gas_price * 1.5}

        optimal_time = self._predict_optimal_gas_window()

        if current_gas_price <= optimal_time["threshold"]:
            return {"submit": "immediate", "gas_price": current_gas_price}
        else:
            return {
                "submit": "delayed",
                "optimal_time": optimal_time["timestamp"],
                "estimated_savings": optimal_time["savings_percentage"]
            }

    def calculate_adaptive_gas_price(self, priority, base_gas_price):
        """
        Calculate gas price based on priority and network conditions
        """
        multipliers = {
            "low": 1.0,
            "normal": 1.2,
            "high": 1.5,
            "critical": 2.0
        }

        congestion_factor = self.network_monitor.get_congestion_multiplier()
        priority_multiplier = multipliers.get(priority, 1.0)

        return int(base_gas_price * priority_multiplier * congestion_factor)
```

### Emergency Controls and Circuit Breakers

#### 6.4 Circuit Breaker Implementation

**Anomaly Detection System**:

```solidity
contract CircuitBreaker {
    struct AnomalyThresholds {
        uint256 maxPriceChangePercent;    // Maximum allowed price change (basis points)
        uint256 maxVolumeSpike;           // Maximum volume increase multiplier
        uint256 maxConsecutiveFailures;   // Maximum consecutive oracle failures
        uint256 suspiciousPatternThreshold; // Threshold for suspicious trading patterns
    }

    struct SystemState {
        bool emergencyPaused;
        uint256 pauseTimestamp;
        string pauseReason;
        uint256 consecutiveFailures;
        mapping(bytes32 => uint256) lastValidPrice;
        mapping(bytes32 => uint256) priceChangeAccumulator;
    }

    AnomalyThresholds public thresholds;
    SystemState public systemState;

    event CircuitBreakerTriggered(string reason, uint256 timestamp);
    event AnomalyDetected(bytes32 indexed companyId, string anomalyType, uint256 value);
    event SystemResumed(uint256 timestamp, address resumedBy);
}
```

**Anomaly Detection Logic**:

```solidity
function checkForAnomalies(
    bytes32[] calldata companyIds,
    uint256[] calldata newPrices,
    uint256[] calldata volumes
) internal returns (bool anomalyDetected) {

    for (uint256 i = 0; i < companyIds.length; i++) {
        bytes32 companyId = companyIds[i];
        uint256 newPrice = newPrices[i];
        uint256 volume = volumes[i];

        // Check price change anomaly
        uint256 lastPrice = systemState.lastValidPrice[companyId];
        if (lastPrice > 0) {
            uint256 priceChangePercent = _calculatePercentageChange(lastPrice, newPrice);
            if (priceChangePercent > thresholds.maxPriceChangePercent) {
                emit AnomalyDetected(companyId, "EXCESSIVE_PRICE_CHANGE", priceChangePercent);
                return true;
            }
        }

        // Check volume spike anomaly
        uint256 averageVolume = _getAverageVolume(companyId, 24 hours);
        if (volume > averageVolume * thresholds.maxVolumeSpike) {
            emit AnomalyDetected(companyId, "VOLUME_SPIKE", volume);
            return true;
        }

        // Check for suspicious patterns
        if (_detectSuspiciousPattern(companyId, newPrice, volume)) {
            emit AnomalyDetected(companyId, "SUSPICIOUS_PATTERN", 0);
            return true;
        }
    }

    return false;
}

function triggerCircuitBreaker(string calldata reason) external {
    require(hasRole(EMERGENCY_ROLE, msg.sender) || msg.sender == address(this), "Unauthorized");

    systemState.emergencyPaused = true;
    systemState.pauseTimestamp = block.timestamp;
    systemState.pauseReason = reason;

    // Pause all token contracts
    IFToken(fTokenAddress).pause();
    ISToken(sTokenAddress).pause();

    emit CircuitBreakerTriggered(reason, block.timestamp);
}
```

#### 6.5 Fallback Mechanisms

**Oracle Failure Handling**:

```python
class OracleFailureHandler:
    def __init__(self):
        self.backup_oracles = BackupOracleNetwork()
        self.historical_data = HistoricalDataStore()
        self.manual_override = ManualOverrideSystem()

    def handle_oracle_failure(self, failed_updates):
        """
        Handle oracle node failures with multiple fallback strategies
        """
        failure_response = {
            "primary_action": None,
            "backup_actions": [],
            "manual_intervention_required": False
        }

        # Strategy 1: Switch to backup oracle nodes
        if self.backup_oracles.available_nodes >= 5:
            failure_response["primary_action"] = "switch_to_backup_oracles"
            backup_data = self.backup_oracles.collect_consensus_data()
            return self._process_backup_data(backup_data)

        # Strategy 2: Use historical extrapolation for short-term
        elif self._can_use_historical_extrapolation(failed_updates):
            failure_response["primary_action"] = "historical_extrapolation"
            extrapolated_data = self.historical_data.extrapolate_values(
                failed_updates, max_extrapolation_hours=6
            )
            return self._process_extrapolated_data(extrapolated_data)

        # Strategy 3: Freeze prices with decay mechanism
        elif self._should_freeze_prices(failed_updates):
            failure_response["primary_action"] = "price_freeze_with_decay"
            return self._activate_price_freeze_mode()

        # Strategy 4: Manual intervention required
        else:
            failure_response["manual_intervention_required"] = True
            self.manual_override.alert_operators(failed_updates)
            return failure_response

    def _activate_price_freeze_mode(self):
        """
        Freeze current prices with gradual decay towards baseline
        """
        return {
            "action": "price_freeze",
            "decay_rate": 0.02,  # 2% decay per hour towards baseline
            "max_freeze_duration": 24,  # 24 hours maximum
            "baseline_convergence": True
        }
```

### Performance and Monitoring

#### 6.6 Performance Targets and SLAs

**System Performance Requirements**:

```python
PERFORMANCE_TARGETS = {
    "update_latency": {
        "f_index_updates": {
            "target": 30,  # seconds from oracle consensus to on-chain
            "maximum": 120,  # seconds
            "measurement": "end_to_end_latency"
        },
        "s_index_updates": {
            "target": 15,  # seconds (more time-sensitive)
            "maximum": 60,  # seconds
            "measurement": "end_to_end_latency"
        },
        "emergency_updates": {
            "target": 10,  # seconds
            "maximum": 30,  # seconds
            "measurement": "end_to_end_latency"
        }
    },
    "transaction_success_rate": {
        "target": 99.5,  # percentage
        "minimum": 98.0,  # percentage
        "measurement_window": "24_hours"
    },
    "gas_efficiency": {
        "cost_per_update": {
            "target": 0.01,  # ETH per company update
            "maximum": 0.05,  # ETH per company update
        },
        "batch_optimization": {
            "target_batch_size": 30,  # companies per batch
            "minimum_efficiency": 75  # percentage savings vs individual updates
        }
    },
    "availability": {
        "uptime_target": 99.9,  # percentage
        "max_downtime": 8.76,  # hours per year
        "recovery_time": 300  # seconds
    }
}
```

#### 6.7 Monitoring and Alerting System

**Comprehensive Monitoring Framework**:

```python
class PriceUpdateMonitor:
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.alert_manager = AlertManager()
        self.dashboard = MonitoringDashboard()

    def setup_monitoring(self):
        """
        Initialize comprehensive monitoring for price update mechanism
        """
        # Performance metrics
        self.metrics_collector.track_metric("update_latency", "histogram")
        self.metrics_collector.track_metric("transaction_gas_usage", "gauge")
        self.metrics_collector.track_metric("batch_size", "histogram")
        self.metrics_collector.track_metric("update_success_rate", "counter")

        # Business metrics
        self.metrics_collector.track_metric("price_change_magnitude", "histogram")
        self.metrics_collector.track_metric("active_companies", "gauge")
        self.metrics_collector.track_metric("total_volume", "counter")

        # Error metrics
        self.metrics_collector.track_metric("oracle_failures", "counter")
        self.metrics_collector.track_metric("circuit_breaker_triggers", "counter")
        self.metrics_collector.track_metric("anomaly_detections", "counter")

    def configure_alerts(self):
        """
        Set up alerting rules for critical system events
        """
        alert_rules = [
            {
                "name": "high_update_latency",
                "condition": "avg(update_latency) > 60s",
                "severity": "warning",
                "notification": ["slack", "email"]
            },
            {
                "name": "oracle_consensus_failure",
                "condition": "oracle_failures > 3 in 5m",
                "severity": "critical",
                "notification": ["pagerduty", "sms", "slack"]
            },
            {
                "name": "circuit_breaker_triggered",
                "condition": "circuit_breaker_triggers > 0",
                "severity": "critical",
                "notification": ["pagerduty", "sms", "slack", "email"]
            },
            {
                "name": "gas_cost_spike",
                "condition": "avg(transaction_gas_usage) > 0.05 ETH",
                "severity": "warning",
                "notification": ["slack", "email"]
            },
            {
                "name": "low_success_rate",
                "condition": "update_success_rate < 98% in 1h",
                "severity": "error",
                "notification": ["pagerduty", "slack"]
            }
        ]

        for rule in alert_rules:
            self.alert_manager.create_alert_rule(rule)
```

**Real-time Dashboard Metrics**:

```python
def generate_dashboard_data():
    """
    Generate real-time dashboard data for price update monitoring
    """
    return {
        "system_health": {
            "status": "healthy|degraded|critical",
            "uptime_percentage": 99.95,
            "last_update": "2024-01-15T10:30:00Z",
            "active_oracle_nodes": 7,
            "circuit_breaker_status": "normal"
        },
        "performance_metrics": {
            "average_update_latency": 25.3,  # seconds
            "updates_per_hour": 48,
            "successful_updates_24h": 1147,
            "failed_updates_24h": 3,
            "gas_cost_24h": 2.34  # ETH
        },
        "recent_updates": [
            {
                "company_id": "AAPL",
                "f_index_change": 0.023,
                "s_index_change": -0.015,
                "timestamp": "2024-01-15T10:28:00Z",
                "gas_used": 0.0087
            }
        ],
        "alerts": {
            "active_alerts": 0,
            "recent_alerts": [
                {
                    "severity": "warning",
                    "message": "High gas prices detected",
                    "timestamp": "2024-01-15T09:45:00Z",
                    "resolved": True
                }
            ]
        }
    }
```

### Integration and Dependencies

**External System Interfaces**:

```python
class PriceUpdateIntegrations:
    def __init__(self):
        self.oracle_pipeline = OracleDataPipeline()
        self.f_token_contract = FTokenContract()
        self.s_token_contract = STokenContract()
        self.governance_contract = GovernanceContract()

    def coordinate_update_cycle(self):
        """
        Coordinate complete update cycle across all integrated systems
        """
        # 1. Collect validated data from oracle pipeline
        oracle_data = self.oracle_pipeline.get_consensus_data()

        # 2. Check governance overrides or parameter changes
        governance_updates = self.governance_contract.get_pending_updates()

        # 3. Process and validate combined updates
        combined_updates = self._merge_updates(oracle_data, governance_updates)
        validated_updates = self._validate_update_consistency(combined_updates)

        # 4. Execute coordinated smart contract updates
        update_results = self._execute_coordinated_updates(validated_updates)

        # 5. Update monitoring and notification systems
        self._update_monitoring_systems(update_results)

        return update_results
```

This comprehensive Price Update Mechanism ensures reliable, efficient, and secure token price updates while maintaining system stability and providing comprehensive monitoring and emergency controls.

## 7. Company Valuation Workflow

### Overview

The Company Valuation Workflow orchestrates the complete end-to-end process of transforming raw financial and sentiment data into tokenized company valuations. This workflow integrates F-Index and S-Index calculations with governance-controlled parameters to produce dynamic token prices that reflect both quantitative financial performance and market sentiment.

**Primary Purpose**: Provide a systematic, transparent, and auditable method for converting multi-dimensional company data into actionable token valuations that can be used for investment decisions and portfolio management.

### 7.1 End-to-End Data Flow Architecture

**Complete Data Processing Pipeline**:

```python
def complete_valuation_workflow():
    """
    Complete workflow from raw data to final token valuation
    """
    workflow_steps = {
        "step_1": "Raw Data Collection",
        "step_2": "Data Validation and Cleaning",
        "step_3": "Financial Index Calculation",
        "step_4": "Sentiment Index Calculation",
        "step_5": "Combined Valuation Formula",
        "step_6": "Token Price Calculation",
        "step_7": "Oracle Data Submission",
        "step_8": "Smart Contract Price Update",
        "step_9": "Data Persistence and Historical Archive"
    }

    # Step 1: Raw Data Collection
    raw_financial_data = collect_financial_data([
        "revenueTTM", "netIncomeTTM", "totalAssets", "totalLiabilities",
        "operatingCashFlowTTM", "returnOnEquityTTM", "debtToEquityRatioTTM"
    ])

    raw_sentiment_data = collect_sentiment_data([
        "social_media_posts", "news_articles", "search_trends",
        "brand_perception_scores", "viral_content_metrics"
    ])

    # Step 2: Data Validation and Cleaning
    validated_financial = validate_and_clean_financial_data(raw_financial_data)
    validated_sentiment = validate_and_clean_sentiment_data(raw_sentiment_data)

    # Step 3: Financial Index Calculation
    f_index = calculate_f_index(validated_financial)

    # Step 4: Sentiment Index Calculation
    s_index = calculate_s_index(validated_sentiment)

    # Step 5: Combined Valuation Formula
    combined_valuation = calculate_combined_valuation(f_index, s_index)

    # Step 6: Token Price Calculation
    token_prices = calculate_token_prices(combined_valuation)

    # Step 7: Oracle Data Submission
    oracle_submission = prepare_oracle_data(f_index, s_index, token_prices)

    # Step 8: Smart Contract Price Update
    blockchain_update = submit_to_smart_contracts(oracle_submission)

    # Step 9: Data Persistence and Historical Archive
    persistence_result = persist_valuation_data(combined_valuation, blockchain_update)

    return {
        "f_index": f_index,
        "s_index": s_index,
        "combined_valuation": combined_valuation,
        "token_prices": token_prices,
        "blockchain_update": blockchain_update,
        "persistence_result": persistence_result
    }
```

**Data Flow Stages**:

1. **Raw Data Ingestion**: Financial metrics from APIs, sentiment data from social platforms
2. **Data Normalization**: Standardization, outlier detection, missing value imputation
3. **Index Calculation**: F-Index (7 financial pillars) and S-Index (5 sentiment components)
4. **Valuation Synthesis**: Weighted combination of indices with governance-adjustable parameters
5. **Price Derivation**: Token price calculation based on combined valuation score
6. **Oracle Validation**: Multi-node consensus and cryptographic verification
7. **On-Chain Update**: Smart contract state updates with gas optimization
8. **Historical Archive**: Persistent storage for trend analysis and auditing

### 7.2 Combined Valuation Formula

**Core Valuation Algorithm**:

The combined valuation score integrates F-Index and S-Index through a weighted formula that accounts for market conditions, volatility, and governance-controlled parameters:

```python
def calculate_combined_valuation(f_index, s_index, governance_params):
    """
    Calculate combined company valuation using F-Index and S-Index

    Args:
        f_index: Financial Index (0.0 to 1.0)
        s_index: Sentiment Index (0.0 to 1.0)
        governance_params: DAO-controlled parameters

    Returns:
        combined_score: Weighted valuation score (0.0 to 1.0)
    """

    # Base weights (governance adjustable)
    base_f_weight = governance_params.get("f_weight", 0.70)  # 70% financial weight
    base_s_weight = governance_params.get("s_weight", 0.30)  # 30% sentiment weight

    # Dynamic weight adjustments based on market conditions
    volatility_factor = calculate_market_volatility()
    sentiment_reliability = calculate_sentiment_reliability(s_index)

    # Adjust weights based on conditions
    if volatility_factor > 0.8:  # High volatility market
        # Increase financial weight, decrease sentiment weight
        adjusted_f_weight = min(base_f_weight * 1.2, 0.85)
        adjusted_s_weight = 1.0 - adjusted_f_weight
    elif sentiment_reliability < 0.6:  # Low sentiment reliability
        # Reduce sentiment influence
        adjusted_f_weight = min(base_f_weight * 1.1, 0.80)
        adjusted_s_weight = 1.0 - adjusted_f_weight
    else:
        adjusted_f_weight = base_f_weight
        adjusted_s_weight = base_s_weight

    # Core valuation formula
    base_score = (f_index * adjusted_f_weight) + (s_index * adjusted_s_weight)

    # Apply momentum factor for trending companies
    momentum_factor = calculate_momentum_factor(f_index, s_index)
    momentum_adjusted_score = base_score * (1 + momentum_factor)

    # Apply governance modifiers
    governance_multiplier = governance_params.get("global_multiplier", 1.0)
    company_specific_modifier = governance_params.get("company_modifiers", {}).get(company_id, 1.0)

    # Final combined score
    combined_score = momentum_adjusted_score * governance_multiplier * company_specific_modifier

    # Ensure score remains within bounds
    combined_score = max(0.0, min(1.0, combined_score))

    return {
        "combined_score": combined_score,
        "f_contribution": f_index * adjusted_f_weight,
        "s_contribution": s_index * adjusted_s_weight,
        "momentum_factor": momentum_factor,
        "adjusted_weights": {
            "f_weight": adjusted_f_weight,
            "s_weight": adjusted_s_weight
        },
        "governance_impact": governance_multiplier * company_specific_modifier
    }

def calculate_momentum_factor(f_index, s_index):
    """
    Calculate momentum factor based on index alignment and strength
    """
    # Strong alignment bonus (both indices moving in same direction)
    alignment_bonus = 0.0
    if (f_index > 0.6 and s_index > 0.6) or (f_index < 0.4 and s_index < 0.4):
        alignment_bonus = 0.05  # 5% bonus for strong alignment

    # Exceptional performance bonus
    exceptional_bonus = 0.0
    if f_index > 0.8 and s_index > 0.7:
        exceptional_bonus = 0.10  # 10% bonus for exceptional performance
    elif f_index < 0.2 and s_index < 0.3:
        exceptional_bonus = -0.05  # 5% penalty for poor performance

    return alignment_bonus + exceptional_bonus
```

**Token Price Calculation**:

```python
def calculate_token_prices(combined_valuation, base_price=1.0):
    """
    Convert combined valuation score to F-Token and S-Token prices
    """
    combined_score = combined_valuation["combined_score"]
    f_contribution = combined_valuation["f_contribution"]
    s_contribution = combined_valuation["s_contribution"]

    # F-Token price based on financial contribution
    f_token_price = base_price * (1 + (f_contribution - 0.5) * 2)  # -100% to +100% range

    # S-Token price based on sentiment contribution (higher volatility)
    s_token_price = base_price * (1 + (s_contribution - 0.5) * 3)  # -150% to +150% range

    # Apply volatility constraints
    f_token_price = max(base_price * 0.1, min(base_price * 3.0, f_token_price))
    s_token_price = max(base_price * 0.05, min(base_price * 5.0, s_token_price))

    return {
        "f_token_price": f_token_price,
        "s_token_price": s_token_price,
        "combined_score": combined_score,
        "price_breakdown": {
            "f_contribution": f_contribution,
            "s_contribution": s_contribution
        }
    }
```

### 7.3 Example Calculation for Apple Inc. (AAPL)

**Sample Data Input**:

```python
# Apple Inc. sample data as of January 15, 2024
apple_sample_data = {
    "company_id": "AAPL",
    "company_name": "Apple Inc.",
    "financial_data": {
        "f_index": 0.723,  # Strong financial performance
        "pillar_breakdown": {
            "Profitability": 0.85,      # Excellent margins and returns
            "Liquidity": 0.72,          # Strong cash position
            "Efficiency": 0.78,         # Good asset utilization
            "Solvency": 0.65,           # Moderate debt levels
            "AssetQuality": 0.74,       # High-quality assets
            "InvestmentCost": 0.68,     # Reasonable valuation
            "PerShareFundamentals": 0.80 # Strong per-share metrics
        }
    },
    "sentiment_data": {
        "s_index": 0.681,  # Positive sentiment
        "component_breakdown": {
            "social_sentiment": 0.72,    # Positive social media
            "news_sentiment": 0.68,      # Favorable news coverage
            "search_trends": 0.75,       # High search interest
            "brand_perception": 0.78,    # Strong brand loyalty
            "viral_factors": 0.31        # Moderate viral content
        }
    },
    "governance_params": {
        "f_weight": 0.70,              # 70% financial weight
        "s_weight": 0.30,              # 30% sentiment weight
        "global_multiplier": 1.0,      # No global adjustment
        "company_modifiers": {
            "AAPL": 1.05               # 5% premium for Apple
        }
    }
}
```

**Step-by-Step Calculation**:

```python
# Step 1: Base weighted calculation
f_contribution = 0.723 * 0.70 = 0.5061
s_contribution = 0.681 * 0.30 = 0.2043
base_score = 0.5061 + 0.2043 = 0.7104

# Step 2: Market condition adjustments
# Assuming normal market conditions (no weight adjustments)
adjusted_f_weight = 0.70
adjusted_s_weight = 0.30

# Step 3: Momentum factor calculation
# Both indices are strong (>0.6), so alignment bonus applies
momentum_factor = 0.05  # 5% bonus for strong alignment

# Step 4: Apply momentum factor
momentum_adjusted_score = 0.7104 * (1 + 0.05) = 0.7459

# Step 5: Apply governance modifiers
governance_multiplier = 1.0
company_modifier = 1.05
final_score = 0.7459 * 1.0 * 1.05 = 0.7832

# Step 6: Calculate token prices (assuming $1.00 base price)
f_token_price = $1.00 * (1 + (0.5061 - 0.5) * 2) = $1.00 * 1.0122 = $1.01
s_token_price = $1.00 * (1 + (0.2043 - 0.5) * 3) = $1.00 * 0.1129 = $0.11

# Apply volatility constraints and recalculate
f_token_price = max($0.10, min($3.00, $1.01)) = $1.01
s_token_price = max($0.05, min($5.00, $0.11)) = $0.11
```

**Final Apple Valuation Result**:

```python
apple_valuation_result = {
    "company_id": "AAPL",
    "combined_score": 0.7832,
    "f_index": 0.723,
    "s_index": 0.681,
    "token_prices": {
        "f_token_price": 1.01,
        "s_token_price": 0.11
    },
    "calculation_breakdown": {
        "f_contribution": 0.5061,
        "s_contribution": 0.2043,
        "momentum_bonus": 0.05,
        "governance_impact": 1.05
    },
    "confidence_metrics": {
        "data_quality": 0.96,
        "calculation_confidence": 0.94,
        "market_stability": 0.87
    },
    "calculation_timestamp": "2024-01-15T10:30:00Z"
}
```

### 7.4 Governance Weight Adjustment Mechanism

**DAO Governance Interface**:

```solidity
contract ValuationGovernance {
    struct WeightAdjustmentProposal {
        uint256 proposalId;
        string description;
        uint256 newFWeight;        // New F-Index weight (basis points)
        uint256 newSWeight;        // New S-Index weight (basis points)
        uint256 globalMultiplier;  // Global adjustment factor
        mapping(bytes32 => uint256) companyModifiers;  // Company-specific modifiers
        uint256 votingDeadline;
        uint256 executionDelay;
        bool executed;
    }

    mapping(uint256 => WeightAdjustmentProposal) public proposals;
    mapping(address => uint256) public votingPower;

    // Current active parameters
    uint256 public currentFWeight = 7000;      // 70.00% in basis points
    uint256 public currentSWeight = 3000;      // 30.00% in basis points
    uint256 public globalMultiplier = 10000;   // 100.00% in basis points

    event WeightAdjustmentProposed(uint256 proposalId, uint256 newFWeight, uint256 newSWeight);
    event WeightAdjustmentExecuted(uint256 proposalId, uint256 oldFWeight, uint256 newFWeight);
    event EmergencyWeightAdjustment(uint256 oldFWeight, uint256 newFWeight, string reason);

    function proposeWeightAdjustment(
        string calldata description,
        uint256 newFWeight,
        uint256 newSWeight,
        uint256 newGlobalMultiplier
    ) external returns (uint256 proposalId) {
        require(newFWeight + newSWeight == 10000, "Weights must sum to 100%");
        require(newFWeight >= 5000 && newFWeight <= 9000, "F-Weight must be 50-90%");
        require(newGlobalMultiplier >= 5000 && newGlobalMultiplier <= 15000, "Global multiplier must be 50-150%");

        proposalId = _createProposal(description, newFWeight, newSWeight, newGlobalMultiplier);
        emit WeightAdjustmentProposed(proposalId, newFWeight, newSWeight);

        return proposalId;
    }

    function executeWeightAdjustment(uint256 proposalId) external {
        WeightAdjustmentProposal storage proposal = proposals[proposalId];
        require(block.timestamp > proposal.votingDeadline, "Voting still active");
        require(block.timestamp > proposal.votingDeadline + proposal.executionDelay, "Still in execution delay");
        require(!proposal.executed, "Already executed");
        require(_hasPassedVote(proposalId), "Proposal did not pass");

        uint256 oldFWeight = currentFWeight;
        currentFWeight = proposal.newFWeight;
        currentSWeight = proposal.newSWeight;
        globalMultiplier = proposal.globalMultiplier;

        proposal.executed = true;

        emit WeightAdjustmentExecuted(proposalId, oldFWeight, proposal.newFWeight);
    }
}
```

**Parameter Update Process**:

1. **Proposal Creation**: Community members propose weight adjustments with rationale
2. **Discussion Period**: 7-day community discussion and analysis period
3. **Voting Period**: 5-day voting period with governance token holders
4. **Execution Delay**: 2-day time lock before execution for security
5. **Implementation**: Automatic parameter updates across all valuation calculations
6. **Monitoring**: 30-day monitoring period for impact assessment

**Emergency Adjustment Mechanism**:

```python
def emergency_weight_adjustment(reason, new_weights):
    """
    Emergency governance mechanism for critical market conditions
    """
    emergency_conditions = [
        "market_crash",           # Major market downturn
        "data_manipulation",      # Detected manipulation attempts
        "oracle_failure",         # Oracle system failures
        "regulatory_change"       # Regulatory compliance updates
    ]

    if reason in emergency_conditions:
        # Immediate weight adjustment with 24-hour governance override
        implement_emergency_weights(new_weights)
        schedule_governance_review(24)  # Review within 24 hours
        notify_stakeholders(reason, new_weights)

        return {
            "status": "emergency_adjustment_applied",
            "reason": reason,
            "new_weights": new_weights,
            "governance_review_deadline": "24_hours"
        }
```

### 7.5 Data Persistence and Historical Access

**Multi-Layer Data Storage Architecture**:

```python
class ValuationDataPersistence:
    def __init__(self):
        self.primary_db = PostgreSQLDatabase()      # Real-time operational data
        self.time_series_db = InfluxDB()           # Historical time series
        self.blockchain_archive = IPFSStorage()    # Immutable records
        self.cache_layer = RedisCache()            # High-speed access

    def persist_valuation_data(self, valuation_result):
        """
        Persist valuation data across multiple storage layers
        """
        persistence_result = {
            "primary_db": None,
            "time_series": None,
            "blockchain_archive": None,
            "cache_update": None
        }

        # Primary database storage
        persistence_result["primary_db"] = self.primary_db.store_valuation({
            "company_id": valuation_result["company_id"],
            "combined_score": valuation_result["combined_score"],
            "f_index": valuation_result["f_index"],
            "s_index": valuation_result["s_index"],
            "token_prices": valuation_result["token_prices"],
            "timestamp": valuation_result["calculation_timestamp"],
            "metadata": valuation_result["calculation_breakdown"]
        })

        # Time series database for historical analysis
        persistence_result["time_series"] = self.time_series_db.insert_measurement({
            "measurement": "company_valuations",
            "tags": {
                "company_id": valuation_result["company_id"],
                "calculation_type": "combined_valuation"
            },
            "fields": {
                "combined_score": valuation_result["combined_score"],
                "f_index": valuation_result["f_index"],
                "s_index": valuation_result["s_index"],
                "f_token_price": valuation_result["token_prices"]["f_token_price"],
                "s_token_price": valuation_result["token_prices"]["s_token_price"]
            },
            "timestamp": valuation_result["calculation_timestamp"]
        })

        # Blockchain archival for immutable records
        persistence_result["blockchain_archive"] = self.blockchain_archive.store_hash({
            "data_hash": self._calculate_data_hash(valuation_result),
            "company_id": valuation_result["company_id"],
            "timestamp": valuation_result["calculation_timestamp"],
            "ipfs_hash": self._store_to_ipfs(valuation_result)
        })

        # Cache layer update for fast access
        persistence_result["cache_update"] = self.cache_layer.update_cache({
            f"valuation:{valuation_result['company_id']}": valuation_result,
            f"latest_scores:{valuation_result['company_id']}": {
                "combined_score": valuation_result["combined_score"],
                "last_updated": valuation_result["calculation_timestamp"]
            }
        })

        return persistence_result

    def get_historical_valuations(self, company_id, time_range, granularity="1h"):
        """
        Retrieve historical valuation data with specified granularity
        """
        query = f"""
        SELECT mean(combined_score) as avg_score,
               mean(f_index) as avg_f_index,
               mean(s_index) as avg_s_index,
               mean(f_token_price) as avg_f_price,
               mean(s_token_price) as avg_s_price
        FROM company_valuations
        WHERE company_id = '{company_id}'
        AND time >= '{time_range.start}'
        AND time <= '{time_range.end}'
        GROUP BY time({granularity})
        """

        return self.time_series_db.query(query)

    def generate_valuation_report(self, company_id, report_type="monthly"):
        """
        Generate comprehensive valuation analysis report
        """
        report_data = {
            "company_id": company_id,
            "report_type": report_type,
            "generation_timestamp": datetime.utcnow().isoformat(),
            "summary_statistics": self._calculate_summary_statistics(company_id, report_type),
            "trend_analysis": self._analyze_valuation_trends(company_id, report_type),
            "performance_metrics": self._calculate_performance_metrics(company_id, report_type),
            "comparison_analysis": self._compare_with_peers(company_id, report_type)
        }

        # Store report in primary database
        report_id = self.primary_db.store_report(report_data)

        return {
            "report_id": report_id,
            "report_data": report_data,
            "download_url": f"/api/reports/{report_id}",
            "expiry_date": datetime.utcnow() + timedelta(days=90)
        }
```

**Data Access Patterns**:

```python
# Real-time access
current_valuation = get_current_valuation("AAPL")

# Historical analysis
historical_trend = get_historical_valuations("AAPL", last_30_days, granularity="1d")

# Comparative analysis
peer_comparison = compare_valuations(["AAPL", "GOOGL", "MSFT"], last_quarter)

# Audit trail
audit_trail = get_valuation_audit_trail("AAPL", specific_date)
```

This comprehensive Company Valuation Workflow provides a robust, transparent, and auditable framework for converting raw company data into actionable token valuations while maintaining governance control and historical integrity.

## 8. Supporting Services and Data Models

### 8.1 Company and Metric Data Models

**Core Data Models**:

```python
# Company Entity Model
class Company:
    """
    Central company entity with comprehensive metadata
    """
    def __init__(self):
        self.company_id: str           # Unique identifier (ticker symbol)
        self.company_name: str         # Official company name
        self.sector: str              # Industry sector classification
        self.market_cap: float        # Current market capitalization
        self.external_identifiers: Dict = {
            "ticker": str,            # Stock ticker symbol
            "cusip": str,            # CUSIP identifier
            "isin": str,             # International Securities ID
            "cik": str,              # SEC Central Index Key
            "lei": str               # Legal Entity Identifier
        }
        self.metadata: Dict = {
            "founded_date": str,      # Company founding date
            "headquarters": str,      # Headquarters location
            "employees": int,         # Number of employees
            "description": str,       # Business description
            "website": str,          # Official website
            "status": str            # Active, delisted, merged, etc.
        }
        self.data_sources: List[str]  # Configured data sources
        self.update_schedule: Dict    # Update frequency settings
        self.created_at: datetime
        self.updated_at: datetime

# Financial Metrics Model
class FinancialMetrics:
    """
    Comprehensive financial metrics for F-Index calculation
    """
    def __init__(self):
        self.company_id: str
        self.reporting_period: str    # "Q1 2024", "FY 2023", etc.
        self.currency: str           # USD, EUR, etc.

        # Profitability Metrics
        self.revenue_ttm: float
        self.net_income_ttm: float
        self.gross_profit_ttm: float
        self.operating_income_ttm: float
        self.ebitda_ttm: float
        self.return_on_equity_ttm: float
        self.return_on_assets_ttm: float
        self.net_profit_margin_ttm: float
        self.operating_profit_margin_ttm: float
        self.gross_profit_margin_ttm: float

        # Liquidity Metrics
        self.current_ratio: float
        self.quick_ratio: float
        self.cash_ratio: float
        self.operating_cash_flow_ttm: float
        self.free_cash_flow_ttm: float
        self.cash_and_equivalents: float

        # Solvency Metrics
        self.total_debt: float
        self.debt_to_equity_ratio: float
        self.interest_coverage_ratio: float
        self.debt_to_assets_ratio: float

        # Efficiency Metrics
        self.asset_turnover_ratio: float
        self.inventory_turnover_ratio: float
        self.receivables_turnover_ratio: float
        self.return_on_invested_capital: float

        # Per-Share Metrics
        self.earnings_per_share_ttm: float
        self.book_value_per_share: float
        self.revenue_per_share_ttm: float
        self.cash_per_share: float

        # Metadata
        self.data_quality_score: float  # 0-1 completeness score
        self.source_reliability: float  # Historical accuracy
        self.last_updated: datetime
        self.next_update: datetime

# Sentiment Data Model
class SentimentData:
    """
    Sentiment analysis results and metadata
    """
    def __init__(self):
        self.company_id: str
        self.collection_timestamp: datetime
        self.analysis_timestamp: datetime

        # Social Media Sentiment
        self.social_sentiment_score: float    # 0-1 normalized score
        self.social_volume: int              # Number of mentions
        self.social_engagement: float        # Weighted engagement score
        self.platform_breakdown: Dict = {
            "twitter": {"score": float, "volume": int, "engagement": float},
            "reddit": {"score": float, "volume": int, "engagement": float},
            "tiktok": {"score": float, "volume": int, "engagement": float}
        }

        # News Sentiment
        self.news_sentiment_score: float     # 0-1 normalized score
        self.news_volume: int               # Number of articles
        self.news_credibility_score: float  # Source reliability weight
        self.source_breakdown: Dict = {
            "reuters": {"score": float, "articles": int, "credibility": float},
            "bloomberg": {"score": float, "articles": int, "credibility": float},
            "cnbc": {"score": float, "articles": int, "credibility": float}
        }

        # Search Trends
        self.search_trend_score: float       # 0-1 normalized score
        self.search_volume_index: int        # Google Trends index
        self.search_momentum: float          # Rate of change

        # Viral Factors
        self.viral_score: float             # 0-1 viral content indicator
        self.hashtag_trends: List[str]      # Trending hashtags
        self.influencer_mentions: int       # High-influence account mentions

        # Quality Metrics
        self.confidence_score: float        # Analysis confidence
        self.anomaly_flags: List[str]       # Detected anomalies
        self.processing_time_ms: int        # Analysis duration

# Index Calculation Results
class IndexResults:
    """
    F-Index and S-Index calculation results with audit trail
    """
    def __init__(self):
        self.company_id: str
        self.calculation_timestamp: datetime

        # F-Index Results
        self.f_index_score: float           # Final F-Index (0-1)
        self.f_pillar_scores: Dict = {
            "Profitability": float,
            "Liquidity": float,
            "Efficiency": float,
            "Solvency": float,
            "AssetQuality": float,
            "InvestmentCost": float,
            "PerShareFundamentals": float
        }
        self.f_index_confidence: float      # Calculation confidence

        # S-Index Results
        self.s_index_score: float           # Final S-Index (0-1)
        self.s_component_scores: Dict = {
            "social_sentiment": float,
            "news_sentiment": float,
            "search_trends": float,
            "brand_perception": float,
            "viral_factors": float
        }
        self.s_index_confidence: float      # Calculation confidence

        # Combined Metrics
        self.combined_valuation_score: float # Weighted combination
        self.governance_adjustments: Dict    # Applied governance parameters

        # Audit Trail
        self.calculation_parameters: Dict    # All parameters used
        self.data_sources_used: List[str]   # Data sources included
        self.quality_flags: List[str]       # Quality concerns
        self.version: str                   # Calculation algorithm version
```

### 8.2 Data Storage Architecture

**Multi-Tier Storage Strategy**:

```python
class DataStorageManager:
    """
    Comprehensive data storage management across multiple tiers
    """
    def __init__(self):
        # Tier 1: Hot Storage (Redis) - Real-time access
        self.redis_client = RedisClient(
            host="redis-cluster",
            port=6379,
            db=0,
            max_connections=100,
            ttl_default=3600  # 1 hour default TTL
        )

        # Tier 2: Warm Storage (PostgreSQL) - Operational data
        self.postgres_client = PostgreSQLClient(
            host="postgres-primary",
            port=5432,
            database="fschain_main",
            read_replicas=["postgres-replica-1", "postgres-replica-2"],
            connection_pool_size=20
        )

        # Tier 3: Cold Storage (InfluxDB) - Historical time series
        self.influx_client = InfluxDBClient(
            host="influxdb-cluster",
            port=8086,
            database="fschain_timeseries",
            retention_policy="365d",  # 1 year retention
            shard_duration="7d"
        )

        # Tier 4: Archive Storage (IPFS) - Immutable records
        self.ipfs_client = IPFSClient(
            gateway="ipfs-gateway",
            api_port=5001,
            encryption_enabled=True
        )

        # Tier 5: On-Chain Storage - Critical state
        self.blockchain_client = Web3Client(
            provider="https://mainnet.infura.io/v3/API_KEY",
            gas_strategy="medium",
            retry_attempts=3
        )

    def store_company_data(self, company: Company):
        """Store company data across appropriate tiers"""
        # Hot storage - current company info
        self.redis_client.hset(
            f"company:{company.company_id}",
            mapping=company.to_dict()
        )

        # Warm storage - persistent company record
        self.postgres_client.upsert(
            table="companies",
            data=company.to_dict(),
            conflict_columns=["company_id"]
        )

    def store_financial_metrics(self, metrics: FinancialMetrics):
        """Store financial metrics with versioning"""
        # Time series storage for historical analysis
        self.influx_client.write_points([{
            "measurement": "financial_metrics",
            "tags": {
                "company_id": metrics.company_id,
                "reporting_period": metrics.reporting_period
            },
            "fields": metrics.to_dict(),
            "time": metrics.last_updated
        }])

        # Hot storage for latest metrics
        self.redis_client.hset(
            f"metrics:financial:{metrics.company_id}",
            mapping=metrics.to_dict(),
            ex=86400  # 24 hour TTL
        )

    def store_index_results(self, results: IndexResults):
        """Store index calculation results with audit trail"""
        # Archive immutable calculation record
        ipfs_hash = self.ipfs_client.add_json(results.to_dict())

        # Store calculation in warm storage
        self.postgres_client.insert(
            table="index_calculations",
            data={
                **results.to_dict(),
                "ipfs_hash": ipfs_hash
            }
        )

        # Update current index values in hot storage
        self.redis_client.hmset(
            f"index:current:{results.company_id}",
            {
                "f_index": results.f_index_score,
                "s_index": results.s_index_score,
                "combined_score": results.combined_valuation_score,
                "last_updated": results.calculation_timestamp.isoformat()
            }
        )
```

**Database Schema Design**:

```sql
-- PostgreSQL Schema for Core Tables

-- Companies table
CREATE TABLE companies (
    company_id VARCHAR(10) PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    sector VARCHAR(100),
    market_cap DECIMAL(20,2),
    external_identifiers JSONB,
    metadata JSONB,
    data_sources TEXT[],
    update_schedule JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Financial metrics table (versioned)
CREATE TABLE financial_metrics (
    id SERIAL PRIMARY KEY,
    company_id VARCHAR(10) REFERENCES companies(company_id),
    reporting_period VARCHAR(20),
    metrics_data JSONB NOT NULL,
    data_quality_score DECIMAL(3,2),
    source_reliability DECIMAL(3,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(company_id, reporting_period)
);

-- Index calculations table
CREATE TABLE index_calculations (
    id SERIAL PRIMARY KEY,
    company_id VARCHAR(10) REFERENCES companies(company_id),
    f_index_score DECIMAL(5,4) NOT NULL,
    s_index_score DECIMAL(5,4) NOT NULL,
    combined_score DECIMAL(5,4) NOT NULL,
    pillar_scores JSONB,
    component_scores JSONB,
    calculation_parameters JSONB,
    ipfs_hash VARCHAR(64),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    INDEX idx_company_timestamp (company_id, created_at)
);

-- Oracle submissions table
CREATE TABLE oracle_submissions (
    id SERIAL PRIMARY KEY,
    batch_id UUID UNIQUE,
    company_updates JSONB NOT NULL,
    transaction_hash VARCHAR(66),
    gas_used INTEGER,
    submission_status VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 8.3 API Endpoints and Service Interfaces

**RESTful API Design**:

```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="FS Chain API", version="1.0.0")
security = HTTPBearer()

# API Response Models
class CompanyResponse(BaseModel):
    company_id: str
    company_name: str
    sector: str
    current_f_index: Optional[float]
    current_s_index: Optional[float]
    last_updated: str

class IndexHistoryResponse(BaseModel):
    company_id: str
    time_range: str
    granularity: str
    data_points: List[Dict]

# Company Management Endpoints
@app.get("/api/v1/companies", response_model=List[CompanyResponse])
async def list_companies(
    sector: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    """List all tracked companies with optional sector filter"""
    companies = await company_service.get_companies(
        sector=sector, limit=limit, offset=offset
    )
    return companies

@app.get("/api/v1/companies/{company_id}", response_model=CompanyResponse)
async def get_company(company_id: str):
    """Get detailed company information"""
    company = await company_service.get_company(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

# Index Data Endpoints
@app.get("/api/v1/companies/{company_id}/f-index")
async def get_f_index(company_id: str):
    """Get current F-Index score and breakdown"""
    f_index_data = await index_service.get_current_f_index(company_id)
    return f_index_data

@app.get("/api/v1/companies/{company_id}/s-index")
async def get_s_index(company_id: str):
    """Get current S-Index score and breakdown"""
    s_index_data = await index_service.get_current_s_index(company_id)
    return s_index_data

@app.get("/api/v1/companies/{company_id}/history")
async def get_index_history(
    company_id: str,
    time_range: str = "30d",  # 1d, 7d, 30d, 90d, 1y
    granularity: str = "1h"   # 5m, 15m, 1h, 1d
):
    """Get historical index data"""
    history = await index_service.get_index_history(
        company_id, time_range, granularity
    )
    return history

# Token Price Endpoints
@app.get("/api/v1/tokens/{company_id}/prices")
async def get_token_prices(company_id: str):
    """Get current F-Token and S-Token prices"""
    prices = await price_service.get_current_prices(company_id)
    return prices

# Market Data Endpoints
@app.get("/api/v1/market/overview")
async def get_market_overview():
    """Get overall market statistics"""
    overview = await market_service.get_market_overview()
    return overview

@app.get("/api/v1/market/top-movers")
async def get_top_movers(
    metric: str = "f_index",  # f_index, s_index, combined
    direction: str = "up",    # up, down
    limit: int = 10
):
    """Get top performing companies"""
    movers = await market_service.get_top_movers(metric, direction, limit)
    return movers

# Governance Endpoints
@app.get("/api/v1/governance/parameters")
async def get_governance_parameters():
    """Get current governance parameters"""
    params = await governance_service.get_current_parameters()
    return params

@app.get("/api/v1/governance/proposals")
async def get_governance_proposals(status: str = "active"):
    """Get governance proposals"""
    proposals = await governance_service.get_proposals(status)
    return proposals

# Oracle Status Endpoints
@app.get("/api/v1/oracle/status")
async def get_oracle_status():
    """Get oracle network status"""
    status = await oracle_service.get_network_status()
    return status

@app.get("/api/v1/oracle/nodes")
async def get_oracle_nodes():
    """Get oracle node information"""
    nodes = await oracle_service.get_node_status()
    return nodes
```

**WebSocket Real-Time API**:

```python
from fastapi import WebSocket, WebSocketDisconnect
import asyncio
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.company_subscribers: Dict[str, List[WebSocket]] = defaultdict(list)

    async def connect(self, websocket: WebSocket, company_id: str = None):
        await websocket.accept()
        self.active_connections.append(websocket)
        if company_id:
            self.company_subscribers[company_id].append(websocket)

    def disconnect(self, websocket: WebSocket, company_id: str = None):
        self.active_connections.remove(websocket)
        if company_id and websocket in self.company_subscribers[company_id]:
            self.company_subscribers[company_id].remove(websocket)

manager = ConnectionManager()

@app.websocket("/ws/companies/{company_id}")
async def websocket_company_updates(websocket: WebSocket, company_id: str):
    await manager.connect(websocket, company_id)
    try:
        while True:
            # Keep connection alive and listen for updates
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket, company_id)

# Real-time update broadcaster
async def broadcast_index_update(company_id: str, update_data: dict):
    """Broadcast index updates to subscribers"""
    message = json.dumps({
        "type": "index_update",
        "company_id": company_id,
        "data": update_data,
        "timestamp": datetime.utcnow().isoformat()
    })

    for websocket in manager.company_subscribers[company_id]:
        try:
            await websocket.send_text(message)
        except:
            manager.disconnect(websocket, company_id)
```

### 8.4 Logging and Monitoring Infrastructure

**Comprehensive Logging Architecture**:

```python
import logging
import structlog
from pythonjsonlogger import jsonlogger
from prometheus_client import Counter, Histogram, Gauge

# Structured logging configuration
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.add_logger_name,
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Prometheus metrics
REQUESTS_TOTAL = Counter('api_requests_total', 'Total API requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('api_request_duration_seconds', 'API request duration')
ACTIVE_CONNECTIONS = Gauge('websocket_connections_active', 'Active WebSocket connections')
INDEX_CALCULATIONS = Counter('index_calculations_total', 'Total index calculations', ['company_id', 'type'])
ORACLE_SUBMISSIONS = Counter('oracle_submissions_total', 'Total oracle submissions', ['status'])

class FSChainLogger:
    """Centralized logging for all FS Chain services"""

    def __init__(self, service_name: str):
        self.logger = structlog.get_logger(service_name)
        self.service_name = service_name

    def log_api_request(self, method: str, endpoint: str, status_code: int, duration: float):
        """Log API request with metrics"""
        REQUESTS_TOTAL.labels(method=method, endpoint=endpoint, status=status_code).inc()
        REQUEST_DURATION.observe(duration)

        self.logger.info(
            "API request",
            method=method,
            endpoint=endpoint,
            status_code=status_code,
            duration_seconds=duration
        )

    def log_index_calculation(self, company_id: str, index_type: str,
                            score: float, confidence: float, duration_ms: int):
        """Log index calculation results"""
        INDEX_CALCULATIONS.labels(company_id=company_id, type=index_type).inc()

        self.logger.info(
            "Index calculation completed",
            company_id=company_id,
            index_type=index_type,
            score=score,
            confidence=confidence,
            calculation_duration_ms=duration_ms
        )

    def log_oracle_submission(self, batch_id: str, company_count: int,
                            gas_used: int, status: str):
        """Log oracle submission to blockchain"""
        ORACLE_SUBMISSIONS.labels(status=status).inc()

        self.logger.info(
            "Oracle submission",
            batch_id=batch_id,
            company_count=company_count,
            gas_used=gas_used,
            status=status
        )

    def log_error(self, error_type: str, error_message: str,
                  context: dict = None, stack_trace: str = None):
        """Log errors with context"""
        self.logger.error(
            "Service error",
            error_type=error_type,
            error_message=error_message,
            context=context or {},
            stack_trace=stack_trace,
            service=self.service_name
        )
```

**Monitoring and Alerting Configuration**:

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "fschain_alerts.yml"

scrape_configs:
  - job_name: "fschain-api"
    static_configs:
      - targets: ["api-service:8000"]
    scrape_interval: 5s
    metrics_path: /metrics

  - job_name: "fschain-oracle"
    static_configs:
      - targets: ["oracle-node-1:9090", "oracle-node-2:9090"]
    scrape_interval: 10s

  - job_name: "fschain-indexers"
    static_configs:
      - targets: ["f-index-service:8001", "s-index-service:8002"]
    scrape_interval: 30s

# fschain_alerts.yml
groups:
  - name: fschain.rules
    rules:
      - alert: HighAPILatency
        expr: histogram_quantile(0.95, api_request_duration_seconds) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High API latency detected"
          description: "95th percentile latency is {{ $value }}s"

      - alert: OracleConsensusFailure
        expr: rate(oracle_submissions_total{status="failed"}[5m]) > 0.1
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Oracle consensus failures detected"
          description: "Oracle failure rate: {{ $value }}/min"

      - alert: IndexCalculationStuck
        expr: time() - max(index_calculation_timestamp) > 3600
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Index calculations stopped"
          description: "No index calculations in the last hour"
```

### 8.5 DevOps and Deployment Infrastructure

**Docker Compose Development Setup**:

```yaml
# docker-compose.yml
version: "3.8"

services:
  # Database Services
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: fschain_main
      POSTGRES_USER: fschain
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./sql/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"

  influxdb:
    image: influxdb:2.0
    environment:
      INFLUXDB_DB: fschain_timeseries
      INFLUXDB_ADMIN_USER: admin
      INFLUXDB_ADMIN_PASSWORD: ${INFLUXDB_PASSWORD}
    volumes:
      - influxdb_data:/var/lib/influxdb2
    ports:
      - "8086:8086"

  # Application Services
  api-service:
    build:
      context: ./app
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql://fschain:${POSTGRES_PASSWORD}@postgres:5432/fschain_main
      - REDIS_URL=redis://redis:6379/0
      - INFLUXDB_URL=http://influxdb:8086
    volumes:
      - ./app:/app
      - ./logs:/app/logs
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
      - influxdb

  f-index-service:
    build:
      context: ./app/services
      dockerfile: Dockerfile.f-index
    environment:
      - DATABASE_URL=postgresql://fschain:${POSTGRES_PASSWORD}@postgres:5432/fschain_main
      - REDIS_URL=redis://redis:6379/1
    volumes:
      - ./app/services:/app
      - ./logs:/app/logs
    ports:
      - "8001:8001"
    depends_on:
      - postgres
      - redis

  s-index-service:
    build:
      context: ./app/services
      dockerfile: Dockerfile.s-index
    environment:
      - DATABASE_URL=postgresql://fschain:${POSTGRES_PASSWORD}@postgres:5432/fschain_main
      - REDIS_URL=redis://redis:6379/2
      - TWITTER_API_KEY=${TWITTER_API_KEY}
      - NEWS_API_KEY=${NEWS_API_KEY}
    volumes:
      - ./app/services:/app
      - ./logs:/app/logs
    ports:
      - "8002:8002"
    depends_on:
      - postgres
      - redis

  # Oracle Network
  oracle-node-1:
    build:
      context: ./oracle
      dockerfile: Dockerfile
    environment:
      - NODE_ID=node-1
      - ETHEREUM_RPC_URL=${ETHEREUM_RPC_URL}
      - PRIVATE_KEY=${ORACLE_PRIVATE_KEY_1}
      - COORDINATOR_ADDRESS=${COORDINATOR_ADDRESS}
    volumes:
      - ./oracle:/app
      - oracle_1_data:/app/data
    ports:
      - "9090:9090"

  oracle-node-2:
    build:
      context: ./oracle
      dockerfile: Dockerfile
    environment:
      - NODE_ID=node-2
      - ETHEREUM_RPC_URL=${ETHEREUM_RPC_URL}
      - PRIVATE_KEY=${ORACLE_PRIVATE_KEY_2}
      - COORDINATOR_ADDRESS=${COORDINATOR_ADDRESS}
    volumes:
      - ./oracle:/app
      - oracle_2_data:/app/data
    ports:
      - "9091:9090"

  # Monitoring Stack
  prometheus:
    image: prom/prometheus:latest
    command:
      - "--config.file=/etc/prometheus/prometheus.yml"
      - "--storage.tsdb.path=/prometheus"
      - "--web.console.libraries=/etc/prometheus/console_libraries"
      - "--web.console.templates=/etc/prometheus/consoles"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./monitoring/alerts.yml:/etc/prometheus/alerts.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana:latest
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/dashboards:/var/lib/grafana/dashboards
    ports:
      - "3000:3000"
    depends_on:
      - prometheus

volumes:
  postgres_data:
  redis_data:
  influxdb_data:
  oracle_1_data:
  oracle_2_data:
  prometheus_data:
  grafana_data:
```

**Environment Configuration**:

```bash
# .env.example
# Database Configuration
POSTGRES_PASSWORD=secure_postgres_password
INFLUXDB_PASSWORD=secure_influxdb_password
REDIS_PASSWORD=secure_redis_password

# API Keys
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
NEWS_API_KEY=your_news_api_key
BLOOMBERG_API_KEY=your_bloomberg_api_key

# Blockchain Configuration
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/your_project_id
ORACLE_PRIVATE_KEY_1=0x...
ORACLE_PRIVATE_KEY_2=0x...
COORDINATOR_ADDRESS=0x...

# Monitoring
GRAFANA_PASSWORD=secure_grafana_password

# Application Settings
LOG_LEVEL=INFO
DEBUG=false
ENVIRONMENT=development
```

**Production Kubernetes Deployment**:

```yaml
# k8s/api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fschain-api
  labels:
    app: fschain-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fschain-api
  template:
    metadata:
      labels:
        app: fschain-api
    spec:
      containers:
        - name: api
          image: fschain/api:latest
          ports:
            - containerPort: 8000
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: fschain-secrets
                  key: database-url
            - name: REDIS_URL
              valueFrom:
                secretKeyRef:
                  name: fschain-secrets
                  key: redis-url
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
```

This comprehensive Supporting Services and Data Models section provides the foundational infrastructure needed to support the FS Chain dual-token system with robust data management, APIs, monitoring, and deployment capabilities.

## 9. Security & Governance

- Anti-manipulation safeguards (outlier detection, circuit breakers)
- Node security (signing, staking, slashing)
- DAO governance hooks (parameter updates, onboarding)
- Emergency protocols and backup strategies

## 10. Roadmap and Implementation Phases

- Phase 1: MVP (core architecture, 3-5 companies, basic validation)
- Phase 2: Enhanced Oracle (expanded data, advanced NLP, more companies)
- Phase 3: Full Decentralization (open node ops, ML, cross-chain)
- Testing, validation, and performance KPIs

## 11. Risks and Limitations

- Data integrity and source reliability
- Sentiment analysis challenges
- Gas costs and update frequency
- Regulatory and legal considerations

## 12. References

- oracle-spec.md
- whitepaper.md
- financial-formulas.txt

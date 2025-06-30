# Token Valuation Workflow

<!--
This document describes the complete workflow for taking a single company
and creating two SEPARATE token valuations: F-Token (Financial) and S-Token (Sentiment).
The key principle is SEPARATION, these are independent valuations, not combined.
-->

## Overview

The FS Chain system takes a single company and creates two completely separate token valuations:

- **F-Token**: Based purely on financial fundamentals
- **S-Token**: Based purely on market sentiment

These tokens operate independently and serve different investment strategies.

## Workflow Steps

### 1. Company Onboarding

- Add company to tracking system (ticker, name, identifiers)
- Configure data sources for financial and sentiment collection
- Set update schedules and quality thresholds

### 2. Financial Data Pipeline (F-Token Path)

- **Data Collection**: Gather financial metrics from APIs (revenue, profits, ratios, etc.)
- **Data Validation**: Check completeness, accuracy, and timeliness
- **Metric Normalization**: Convert all metrics to 0-1 scale using percentile boundaries
- **Pillar Scoring**: Calculate scores for 7 financial pillars (Profitability, Liquidity, etc.)
- **F-Index Calculation**: Weighted average of pillar scores = Final F-Index (0.0 to 1.0)

### 3. Sentiment Data Pipeline (S-Token Path)

- **Data Collection**: Gather sentiment from social media, news, search trends
- **NLP Processing**: Analyze text sentiment, engagement, and viral factors
- **Trend Analysis**: Calculate search momentum and social volume changes
- **Component Scoring**: Score 5 sentiment components (social, news, trends, etc.)
- **S-Index Calculation**: Weighted average of components = Final S-Index (0.0 to 1.0)

### 4. Oracle Validation

- **Consensus Building**: 7+ oracle nodes validate both F-Index and S-Index independently
- **Data Signing**: Cryptographic signatures on both index values
- **Batch Preparation**: Group multiple company updates for gas efficiency

### 5. Token Price Calculation (Separate Paths)

- **F-Token Price**: Base price × F-Index multiplier (lower volatility, fundamentals-focused)
- **S-Token Price**: Base price × S-Index multiplier (higher volatility, sentiment-focused)
- **No Mixing**: Prices calculated completely independently

### 6. On-Chain Updates

- **Smart Contract Updates**: Submit F-Index and S-Index to respective token contracts
- **Price Derivation**: Each contract calculates its own token price independently
- **Trading Activation**: Tokens available for minting/burning at current prices

### 7. Market Operation

- **Independent Trading**: F-Tokens and S-Tokens trade separately
- **Different Strategies**: Value investors buy F-Tokens, momentum traders buy S-Tokens
- **Arbitrage Opportunities**: Price differences between tokens create trading opportunities
- **Portfolio Construction**: Investors can combine both tokens for diversified exposure

## Key Principles

1. **Complete Separation**: F-Index and S-Index never mixed or combined
2. **Independent Pricing**: Each token has its own price calculation
3. **Different Volatility**: S-Tokens more volatile than F-Tokens by design
4. **Separate Use Cases**: Different tokens serve different investment strategies
5. **Governance Control**: DAO can adjust parameters for each token type independently

## Data Flow Summary

```
Company → [Financial Data] → F-Index → F-Token Price → F-Token Trading
       → [Sentiment Data] → S-Index → S-Token Price → S-Token Trading
```

The two paths run in parallel but remain completely separate throughout the entire process.

# LEGO Market Analytics Platform

A full-stack data engineering and machine learning system for real-time LEGO market intelligence.

This project is a portfolio-ready implementation of an arbitrage detection engine, an end-to-end pipeline that ingests marketplace data, enriches it with LEGO metadata, builds ML-ready features, and scores listings to surface undervalued buying opportunities.

It demonstrates production-style data engineering patterns, feature pipelines, and machine learning–driven decision systems.

---

## System Architecture
<pre>
Marketplace APIs (eBay Active + Sold)
↓
Raw Ingestion Layer
↓
Canonicalization Layer
↓
Set Extraction + Normalization
↓
Grouping by LEGO Set Number
↓
Rebrickable Enrichment Layer
↓
Sold Market Feature Builder
↓
Active vs Sold Joiner
↓
Scoring Engine (ML + Heuristics)
↓
Dashboard / API
</pre>



---

## Technologies

### Backend / Pipeline
- Python  
- FastAPI  
- SQLite  
- Pandas  
- Scikit-learn  
- Aiohttp (async ingestion)

### Frontend
- SvelteKit  
- TailwindCSS  
- Vite  

---

## Features

### Data Engineering
- Automated ingestion of active and sold marketplace listings
- Robust canonicalization of noisy real-world listing data
- Set number extraction using regex + heuristics
- Normalization of condition, completeness, and seller attributes
- Grouping by LEGO set number

### Enrichment Layer
- Integration with Rebrickable metadata API
- Theme, year, and piece count enrichment
- Local caching layer for fast repeated lookups

### Feature Engineering
- Sold-market historical feature builder
- Price distribution modeling per set
- Attribute extraction (condition, completeness, shipping cost, etc.)

### Machine Learning
- Production price prediction model for expected resale value
- Experimental set-number inference model (partially replaced by deterministic matching due to data limitations)
- Hybrid scoring engine combining ML predictions + heuristic rules

### Storage Layer
- SQLite schema for opportunities and event history
- Repository pattern for clean data access abstraction
- Snapshot-based storage for reproducibility and debugging

### Dashboard / API
- FastAPI backend exposing opportunities, snapshots, and pipeline runs
- SvelteKit dashboard for browsing and analyzing scored deals
- Real-time scoring endpoint for active listings

---

## Machine Learning Components

### Production Model
**Price Prediction Model**
- Predicts expected sold price using enriched listing features and historical market data

### Experimental Models
- Set number inference model (superseded by deterministic matching + heuristics)

---

## Example Pipeline Output

```json
{
  "product_key": "75192-1",
  "buy_price": 649.99,
  "sell_price": 720.50,
  "profit": 70.51,
  "roi": 0.108,
  "score": 0.87,
  "buy_url": "https://ebay.com/itm/12345"
}
```

## How To Run Locally

Follow these steps to run the pipeline demo, API backend, and dashboard locally.

### 1. Clone the Repository

```bash
git clone https://github.com/Garrett-Stroud/lego-market-analytics-public-.git
```
Navigate to correct directory
```bash
cd lego-market-analytics-public-
```

### 2. . Run setup
```bash
.\setup.ps1
```


### 3. Start the app
```bash
.\start-dev.ps1
```



# LEGO Market Analytics Platform

An end-to-end data platform for collecting, processing, enriching, and modeling LEGO marketplace data.

## Architecture

Marketplace APIs
    ↓
Raw Ingestion
    ↓
Canonicalization
    ↓
Enrichment
    ↓
Feature Engineering
    ↓
Machine Learning
    ↓
Scoring
    ↓
Dashboard/API

## Technologies

- Python
- FastAPI
- SQLite
- Pandas
- Scikit-Learn
- Svelte

## Features

- Automated marketplace data ingestion
- Data normalization and validation
- LEGO set enrichment using external metadata
- Machine learning price prediction
- Set-number inference models
- Dashboard and API layer

## Machine Learning Components

### Active Models
- Price prediction model (production)

### Experimental Models
- Set number inference model (currently replaced by fuzzy matching due to data limitations)
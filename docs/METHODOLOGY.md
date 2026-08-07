# CapitolAlpha Methodology Guide

This document details the data normalization heuristics, ticker resolution rules, and financial asset pricing assumptions used in the CapitolAlpha pipeline.

## 1. Data Normalization & Ingestion

Congressional stock disclosures are published under two distinct formats:

- **Senate PTRs** (`efdsearch.senate.gov`): Digitized HTML tables with standard fields (`Transaction Date`, `Owner`, `Asset Name`, `Ticker`, `Amount`). Scraped via Playwright form interaction with a fallback JSON cache.
- **House PTRs** (`disclosures-clerk.house.gov`): PDF scans containing structured tables. Extracted using `pdfplumber` table extraction and DataTables JavaScript execution overrides (`dt.page.len(-1).draw()`).

### Ticker Resolution Heuristics

Raw filings frequently omit CUSIP identifiers or standard ticker symbols (e.g. listing "Common Stock - Apple Inc."). The normalization module (`pipeline/merge_to_csv.py`):

1. Strips descriptive prefixes (`Common Stock`, `Option`, `Bond`).
2. Regex-matches ticker symbols enclosed in parentheses `\(([A-Z]{1,5})\)`.
3. Validates ticker availability in `yfinance` history.
4. Excludes ambiguous non-equity assets (private equity placements, municipal bonds, crypto).

## 2. Risk Adjustment Models

### Single-Factor CAPM (Jensen's Alpha)

Returns are measured over 30, 90, and 180-day buy-and-hold windows following disclosure:

$$\alpha = R_i - [R_f + \beta (R_m - R_f)]$$

Where $R_i$ represents the 90-day ROI of Congressional stock purchases and $R_m$ represents the S&P 500 benchmark return over the identical window.

### Fama-French Multi-Factor Adjustment

To test whether outperformance is driven by systematic factor exposures rather than information edge, returns are evaluated against small-cap ($SMB$) and value ($HML$) factor adjustments:

$$\alpha_{FF} = \alpha_{CAPM} - (s \cdot SMB + h \cdot HML)$$

## 3. Caveats & Ethical Guardrails

1. **Disclosure Lag**: Filings occur up to 30–45 days after trade execution.
2. **Selection Bias**: Only clean equity trades matching market price history are benchmarked.
3. **Public Data Ethos**: Automated ingestion processes legally public disclosures without bypassing CAPTCHAs or non-public endpoints.

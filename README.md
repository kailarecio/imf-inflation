# PCA of Inflation by Category

Principal component analysis of monthly year-over-year CPI inflation, broken out by COICOP category, using IMF data. The rendered report plots the first two principal components for the United States. Points are colored by year, and arrows show how much each category contributes to each component.

## Data

Raw data comes from the IMF Consumer Price Index (CPI) dataset ([data.imf.org](https://data.imf.org)). Export it as CSV and save it as `inflation.csv` in this folder. The raw file isn't tracked in git.

The countries to keep are listed in `countries.yaml`.

## How to run

1. **Clean the data in Python.** This turns `inflation.csv` into `headline_all_cats.csv`:
   ```bash
   pip install -r requirements.txt
   python clean_inflation.py
   ```
2. **Render the report in R with Quarto.** This produces `pca.html`:
   ```r
   install.packages(c("tidyverse", "ggrepel", "ggsci"))
   ```
   ```bash
   quarto render pca.qmd
   ```

## Files

| File | Description |
|---|---|
| `clean_inflation.py` | Keeps monthly YoY series, reshapes the data to one column per category, and filters to the countries in `countries.yaml` and dates before 2026 |
| `countries.yaml` | Countries to keep |
| `pca.qmd` | Runs the PCA and draws the biplot (R / Quarto) |
| `headline_all_cats.csv` | Cleaned data that `pca.qmd` reads |
| `pca.html` | Rendered report |

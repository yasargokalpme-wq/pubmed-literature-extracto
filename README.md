# PubMed Literature Extractor

Automated tool for extracting scientific literature from PubMed using NCBI E-utilities API.

## Features

- Search by keyword, date, journal
- Extract titles, authors, abstracts, journal names, publication years
- Export to clean Excel files
- Handle missing data gracefully
- Remove duplicates automatically

## Requirements
```bash
pip install biopython pandas openpyxl
```

## Quick Start
```python
python pubmed_extractor.py
```

## Usage Examples

### Basic Search
```python
search_term = "CRISPR"
max_results = 50
```

### Advanced Searches
```python
# Date range filter
search_term = "cancer AND 2020:2024[PDAT]"

# Title search only
search_term = "Alzheimer[TITL]"

# Multiple keywords
search_term = "(diabetes OR obesity) AND treatment"

# Specific journal
search_term = "COVID-19 AND Nature[JOUR]"
```

## Output

Excel file with these columns:
- PMID (PubMed ID)
- Title
- Authors (first 3 + et al.)
- Journal
- Year
- Abstract
- PubMed Link

## Example

See `example_output.xlsx` for a sample of 10 CRISPR articles.

## Use Cases

- Literature reviews
- Systematic reviews
- Meta-analysis data collection
- Research trend analysis

## Tools Used

- Python 3.x
- Biopython (NCBI E-utilities API)
- Pandas (data processing)
- openpyxl (Excel export)

## Contact

Available for PubMed data extraction projects on Upwork.

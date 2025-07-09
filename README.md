# Professional CV Generator (Python Version)

This is a Python translation of the original R/Quarto-based CV generator. The CV dynamically pulls data from Google Sheets and includes automated citation scraping from Google Scholar.

## Key Architecture

- **cv_generator.py**: Main CV generation script that creates LaTeX output
- **functions.py**: Core utility functions for data processing, Google Sheets integration, and text formatting
- **cite_scrape.py**: Script for scraping Google Scholar citation data
- **preamble.tex**: LaTeX configuration for PDF styling and formatting (from original)
- **Google Sheets integration**: CV data is stored in a Google Sheet with multiple sheets for different CV sections

## Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

You'll also need:
- LaTeX distribution (XeLaTeX) for PDF generation
- Google Sheets API credentials (if using authenticated access)

## Usage

### Generate LaTeX CV

```bash
python cv_generator.py
```

This will generate `cv-ddcf-professional.tex` which can be compiled to PDF using:

```bash
xelatex cv-ddcf-professional.tex
```

### Citation Scraping

```bash
python cite_scrape.py
```

## Data Sources

The CV pulls data from several sheets in the Google Sheets document:
- `pubs`: Publications and conference abstracts
- `classes`: Teaching experience
- `advising`: Mentoring and thesis supervision
- `teaching`: Other teaching activities

## Key Functions

- `get_cv_sheet(sheet)`: Retrieves data from specified Google Sheets tab
- `gscholar_stats(url)`: Scrapes citation statistics from Google Scholar
- `make_bullet_list_filtered(df, cat)`: Creates formatted bullet lists for CV sections
- `make_ordered_list_filtered(df, cat)`: Creates formatted ordered lists for CV sections

## Python Dependencies

- **pandas**: Data manipulation and analysis
- **requests**: HTTP requests for web scraping
- **beautifulsoup4**: HTML parsing for Google Scholar scraping
- **gspread**: Google Sheets API interaction
- **oauth2client**: Google API authentication
- **lxml**: XML/HTML parsing

## Migration from R Version

This Python version maintains the same functionality as the original R/Quarto version:

1. **Data retrieval**: Uses `gspread` instead of `googlesheets4`
2. **Web scraping**: Uses `requests` and `BeautifulSoup` instead of `rvest` and `xml2`
3. **Data processing**: Uses `pandas` instead of `dplyr`
4. **Output generation**: Generates LaTeX directly instead of using Quarto/R Markdown

## Google Sheets Setup

For public access (equivalent to `gs4_deauth()` in R), the current setup assumes public read access to the Google Sheet. For authenticated access, you'll need to:

1. Create a Google Cloud Project
2. Enable the Google Sheets API
3. Create service account credentials
4. Download the credentials JSON file
5. Update the `get_cv_sheet()` function to use the credentials

## Important Notes

- The Google Sheets API is configured for public access by default
- LaTeX styling uses XeLaTeX engine with custom formatting in preamble.tex
- Author highlighting in citations uses regex replacement to underline the author's name
- The CV includes the same sections as the original R version

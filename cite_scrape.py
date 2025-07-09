from functions import get_cv_sheet
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Store IDs
gscholar_id = 'iNdNU5QAAAAJ'
gscholar_page = f"https://scholar.google.com/citations?user={gscholar_id}"

# Get publication data
sheet = get_cv_sheet('pubs')
# Filter for non-null scholar IDs and get the first one
scholar_ids = sheet[sheet['id_scholar'].notna()]['id_scholar']
if len(scholar_ids) > 0:
    scholar_id = scholar_ids.iloc[0]
    url = f"https://scholar.google.com/citations?view_op=view_citation&hl=en&user=DY2D56IAAAAJ&citation_for_view=DY2D56IAAAAJ:{scholar_id}"
    
    # Scrape the citation page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract citation links
    citation_links = soup.select('.gs_scl a')
    citation_texts = [link.get_text(strip=True) for link in citation_links]
    
    print("Citation links found:")
    for text in citation_texts:
        print(text)
    
    # Alternative approach: get page content and split by 'cited by'
    page_content = response.text.lower()
    cited_by_sections = page_content.split('cited by')
    
    print(f"\nFound {len(cited_by_sections)} 'cited by' sections")
    
else:
    print("No scholar IDs found in the sheet")
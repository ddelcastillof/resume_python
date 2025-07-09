import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from typing import Dict, List, Optional
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_cites(url: str) -> Dict[str, str]:
    """
    Scrape citation statistics from Google Scholar profile page.
    
    Args:
        url (str): Google Scholar profile URL
        
    Returns:
        Dict[str, str]: Dictionary containing citations, h-index, and i10-index
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the statistics table
    stats_table = soup.find('table', {'id': 'gsc_rsb_st'})
    if not stats_table:
        return {'citations': '0', 'hindex': '0', 'i10index': '0'}
    
    # Extract values from the second column
    values = [td.text.strip() for td in stats_table.find_all('td')[1::2]]
    
    return {
        'citations': values[0] if len(values) > 0 else '0',
        'hindex': values[1] if len(values) > 1 else '0',
        'i10index': values[2] if len(values) > 2 else '0'
    }


def gscholar_stats(url: str) -> str:
    """
    Get formatted citation statistics from Google Scholar.
    
    Args:
        url (str): Google Scholar profile URL
        
    Returns:
        str: Formatted citation statistics string
    """
    cites = get_cites(url)
    return f"Citations: {cites['citations']} | h-index: {cites['hindex']} | i10-index: {cites['i10index']}"


def get_cv_sheet(sheet_name: str) -> pd.DataFrame:
    """
    Get data from a specific sheet in the CV Google Sheets document.
    
    Args:
        sheet_name (str): Name of the sheet to retrieve
        
    Returns:
        pd.DataFrame: Data from the specified sheet
    """
    try:
        # Try multiple authentication methods
        gc = None
        
        # Method 1: Try service account if available
        try:
            gc = gspread.service_account()
        except:
            pass
        
        # Method 2: Try OAuth if service account fails
        if gc is None:
            try:
                gc = gspread.oauth()
            except:
                pass
        
        # Method 3: Try using public access with no auth
        if gc is None:
            # For public sheets, we can try direct API access
            import requests
            sheet_id = '1yEYPdjQNqIw_lrOjUPDKjx9wMfzTeYrcdrtSDRj6Zhw'
            url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
            response = requests.get(url)
            if response.status_code == 200:
                from io import StringIO
                return pd.read_csv(StringIO(response.text))
        
        if gc is not None:
            sheet_id = '1yEYPdjQNqIw_lrOjUPDKjx9wMfzTeYrcdrtSDRj6Zhw'
            sheet = gc.open_by_key(sheet_id)
            worksheet = sheet.worksheet(sheet_name)
            
            # Get all records and convert to DataFrame
            records = worksheet.get_all_records()
            return pd.DataFrame(records)
        
        raise Exception("Could not authenticate with Google Sheets")
        
    except Exception as e:
        print(f"Warning: Could not access Google Sheets for {sheet_name}: {e}")
        # Return empty DataFrame with basic structure for common sheets
        if sheet_name == 'pubs':
            return pd.DataFrame(columns=['author', 'year', 'title', 'journal_abbv', 'number', 'doi', 'pub_date', 'category'])
        elif sheet_name == 'advising':
            return pd.DataFrame(columns=['name', 'title', 'institution', 'date_start', 'date_stop', 'defense_date', 'complete', 'category'])
        elif sheet_name == 'classes':
            return pd.DataFrame(columns=['univ', 'number', 'name', 'type', 'semester', 'level'])
        elif sheet_name == 'teaching':
            return pd.DataFrame(columns=['title', 'host', 'location', 'date', 'with', 'url', 'category'])
        else:
            return pd.DataFrame()


def make_ordered_list(items: List[str]) -> str:
    """
    Create an ordered list from a list of items in LaTeX format.
    
    Args:
        items (List[str]): List of items to format
        
    Returns:
        str: LaTeX formatted ordered list
    """
    if not items:
        return ""
    
    latex_items = []
    latex_items.append(r"\begin{enumerate}")
    for item in items:
        latex_items.append(f"\\item {item}")
    latex_items.append(r"\end{enumerate}")
    
    return '\n'.join(latex_items)


def make_bullet_list(items: List[str]) -> str:
    """
    Create a bullet list from a list of items in LaTeX format.
    
    Args:
        items (List[str]): List of items to format
        
    Returns:
        str: LaTeX formatted bullet list
    """
    if not items:
        return ""
    
    latex_items = []
    latex_items.append(r"\begin{itemize}")
    for item in items:
        latex_items.append(f"\\item {item}")
    latex_items.append(r"\end{itemize}")
    
    return '\n'.join(latex_items)


def make_ordered_list_filtered(df: pd.DataFrame, category: str) -> str:
    """
    Create an ordered list from filtered DataFrame with author highlighting.
    
    Args:
        df (pd.DataFrame): DataFrame containing citation data
        category (str): Category to filter by
        
    Returns:
        str: LaTeX formatted ordered list with author highlighting
    """
    if df.empty or 'category' not in df.columns:
        return r"\begin{itemize}\item No data available\end{itemize}"
    
    filtered_df = df[df['category'] == category].copy()
    
    if filtered_df.empty:
        return r"\begin{itemize}\item No data available\end{itemize}"
    
    # Apply author highlighting (underline author names with double asterisk)
    if 'citation' in filtered_df.columns:
        filtered_df['citation'] = filtered_df['citation'].str.replace(
            r'\*\*([^*]+)\*\*', r'\\underline{\\textbf{\1}}', regex=True
        )
        citations = filtered_df['citation'].tolist()
    else:
        citations = [f"Data available but citation format not ready"]
    
    return make_ordered_list(citations)


def make_bullet_list_filtered(df: pd.DataFrame, category: str) -> str:
    """
    Create a bullet list from filtered DataFrame with author highlighting.
    
    Args:
        df (pd.DataFrame): DataFrame containing citation data
        category (str): Category to filter by
        
    Returns:
        str: LaTeX formatted bullet list with author highlighting
    """
    if df.empty or 'category' not in df.columns:
        return r"\begin{itemize}\item No data available\end{itemize}"
    
    filtered_df = df[df['category'] == category].copy()
    
    if filtered_df.empty:
        return r"\begin{itemize}\item No data available\end{itemize}"
    
    # Apply author highlighting (underline author names with double asterisk)
    if 'citation' in filtered_df.columns:
        filtered_df['citation'] = filtered_df['citation'].str.replace(
            r'\*\*([^*]+)\*\*', r'\\underline{\\textbf{\1}}', regex=True
        )
        citations = filtered_df['citation'].tolist()
    else:
        citations = [f"Data available but citation format not ready"]
    
    return make_bullet_list(citations)


def na_to_space(value) -> str:
    """
    Convert NaN/None values to empty string.
    
    Args:
        value: Value to check and convert
        
    Returns:
        str: Original value or empty string if NaN/None
    """
    if pd.isna(value) or value is None:
        return ''
    return str(value)


def enquote(text: str) -> str:
    """
    Wrap text in double quotes.
    
    Args:
        text (str): Text to quote
        
    Returns:
        str: Quoted text
    """
    return f'"{text}"'


def markdown_url(url: str) -> str:
    """
    Format URL as markdown link.
    
    Args:
        url (str): URL to format
        
    Returns:
        str: Markdown formatted URL
    """
    return f'[{url}]({url})'
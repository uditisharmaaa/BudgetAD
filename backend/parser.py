from bs4 import BeautifulSoup
import pandas as pd
import io

def parse_fab_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': 'printTable2'})

    if table is None:
        print("❌ Transaction table not found.")
        return None

    df = pd.read_html(io.StringIO(str(table)))[0]
    df.columns = ['Txn ID', 'Date', 'Description', 'Debit (-)', 'Credit (+)', 'Balance']
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Debit (-)'] = pd.to_numeric(df['Debit (-)'], errors='coerce').fillna(0)
    df['Credit (+)'] = pd.to_numeric(df['Credit (+)'], errors='coerce').fillna(0)
    df['Balance'] = pd.to_numeric(df['Balance'], errors='coerce').fillna(0)
    return df

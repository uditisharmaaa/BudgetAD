import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import os

# Global aesthetic settings
plt.style.use('seaborn-v0_8-muted')
plt.rcParams.update({
    'font.size': 34,
    'axes.titlesize': 34,
    'axes.labelsize': 34,
    'xtick.labelsize': 34,
    'ytick.labelsize': 34,
    'figure.titlesize': 44,
    'axes.edgecolor': '#333333',
    'axes.labelcolor': '#333333',
    'xtick.color': '#333333',
    'ytick.color': '#333333'
})

MAIN_COLOR = '#6C5CE7'        # Indigo
SPENDING_COLOR = '#FF7675'    # Soft Red
EARNINGS_COLOR = '#00B894'    # Soft Green
DAILY_COLOR = '#FAB1A0'       # Light Coral
GRID_COLOR = '#DDDDDD'

def plot_all_charts(df, output_folder):
    image_filenames = []
    df = df.sort_values('Date')
    df['Net'] = df['Credit (+)'] - df['Debit (-)']
    df['Cumulative Balance'] = df['Net'].cumsum()
    years = df['Date'].dt.year.unique()

    # 1. Monthly Spending per Year
    for year in years:
        yearly = df[df['Date'].dt.year == year]
        monthly_spend = yearly.groupby(yearly['Date'].dt.month)['Debit (-)'].sum()
        month_names = pd.to_datetime(monthly_spend.index, format='%m').month_name()

        plt.figure(figsize=(26, 13))
        plt.bar(month_names, monthly_spend, color=MAIN_COLOR)
        plt.title(f'Monthly Spending - {year}')
        plt.xlabel('Month')
        plt.ylabel('Amount (AED)')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', color=GRID_COLOR, alpha=0.7)
        plt.tight_layout()
        filename = f'spending_{year}.png'
        plt.savefig(os.path.join(output_folder, filename), dpi=150)
        plt.close()
        image_filenames.append(f'/static/{filename}')

    # 2. Top Vendors
    top_vendors = df.groupby('Description')['Debit (-)'].sum().sort_values(ascending=False).head(10)
    if not top_vendors.empty:
        plt.figure(figsize=(26, 13))
        top_vendors.sort_values().plot(kind='barh', color=MAIN_COLOR)
        plt.title('Top 10 Vendors by Total Spend')
        plt.xlabel('Total Spend (AED)')
        plt.grid(axis='x', linestyle='--', color=GRID_COLOR, alpha=0.7)
        plt.tight_layout()
        filename = 'top_vendors.png'
        plt.savefig(os.path.join(output_folder, filename), dpi=150)
        plt.close()
        image_filenames.append(f'/static/{filename}')

    # 3. Cumulative Balance
    plt.figure(figsize=(26, 13))
    plt.plot(df['Date'], df['Cumulative Balance'], color=MAIN_COLOR, linewidth=4)
    plt.title('Cumulative Balance Over Time')
    plt.xlabel('Date')
    plt.ylabel('Balance (AED)')
    plt.grid(True, linestyle='--', color=GRID_COLOR, alpha=0.7)
    plt.tight_layout()
    filename = 'cumulative_balance.png'
    plt.savefig(os.path.join(output_folder, filename), dpi=150)
    plt.close()
    image_filenames.append(f'/static/{filename}')

    # 4. Monthly Earnings vs Spending
    monthly = df.groupby(df['Date'].dt.to_period('M')).agg({'Debit (-)': 'sum', 'Credit (+)': 'sum'}).reset_index()
    monthly['Month'] = monthly['Date'].dt.strftime('%b %Y')

    plt.figure(figsize=(26, 13))
    plt.bar(monthly['Month'], monthly['Credit (+)'], color=EARNINGS_COLOR, label='Earnings')
    plt.bar(monthly['Month'], monthly['Debit (-)'], bottom=monthly['Credit (+)'], color=SPENDING_COLOR, label='Spending')
    plt.title('Monthly Earnings vs Spending')
    plt.xlabel('Month')
    plt.ylabel('Amount (AED)')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.grid(axis='y', linestyle='--', color=GRID_COLOR, alpha=0.7)
    plt.tight_layout()
    filename = 'earnings_vs_spending.png'
    plt.savefig(os.path.join(output_folder, filename), dpi=150)
    plt.close()
    image_filenames.append(f'/static/{filename}')

    # 5. Daily Spending
    plt.figure(figsize=(26, 13))
    plt.plot(df['Date'], df['Debit (-)'].fillna(0), color=DAILY_COLOR, alpha=0.9, linewidth=3)
    plt.title('Daily Spending Over Time')
    plt.xlabel('Date')
    plt.ylabel('Spending (AED)')
    plt.grid(True, linestyle='--', color=GRID_COLOR, alpha=0.7)
    plt.tight_layout()
    filename = 'daily_spending.png'
    plt.savefig(os.path.join(output_folder, filename), dpi=150)
    plt.close()
    image_filenames.append(f'/static/{filename}')

    # 6. Subscriptions: Vendors with Same-Day Recurrence (3+ Months)
    df['Day'] = df['Date'].dt.day
    subscription_candidates = []

    for vendor, vendor_df in df.groupby('Description'):
        vendor_df['YearMonth'] = vendor_df['Date'].dt.to_period('M')
        day_counts = vendor_df.groupby(['YearMonth', 'Day']).size().reset_index(name='count')
        recurring_days = day_counts.groupby('Day').size()
        if any(recurring_days >= 3):
            subscription_candidates.append(vendor)

    if subscription_candidates:
        sub_spend = df[df['Description'].isin(subscription_candidates)].groupby('Description')['Debit (-)'].sum().sort_values(ascending=False)

        plt.figure(figsize=(26, 13))
        sub_spend.plot(kind='barh', color=MAIN_COLOR)
        plt.title('Potential Subscriptions (Same-Day Recurrence)')
        plt.xlabel('Total Spend (AED)')
        plt.tight_layout()
        filename = 'subscriptions.png'
        plt.savefig(os.path.join(output_folder, filename), dpi=150)
        plt.close()
        image_filenames.append(f'/static/{filename}')

    return image_filenames, years

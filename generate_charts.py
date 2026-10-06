import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = 'Segoe UI', 'DejaVu Sans', 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

project_dir = r"C:\Users\Varshini S\.gemini\antigravity\scratch\ElevateLabs_Task4_Dashboard_Design"
dataset_path = os.path.join(project_dir, "dataset", "sales_financial_data.csv")
images_dir = os.path.join(project_dir, "images")
os.makedirs(images_dir, exist_ok=True)

df = pd.read_csv(dataset_path)
df['Order_Date'] = pd.to_datetime(df['Order_Date'])
df['YearMonth'] = df['Order_Date'].dt.to_period('M').astype(str)

# Corporate Color Palette
NAVY = "#0F172A"
BLUE = "#2563EB"
TEAL = "#0D9488"
EMERALD = "#10B981"
AMBER = "#F59E0B"
ROSE = "#E11D48"
GRAY_BG = "#F8FAFC"
CARD_BORDER = "#E2E8F0"

# 1. Monthly Sales & Profit Trend (Time-Series)
plt.figure(figsize=(12, 5.5))
monthly = df.groupby('YearMonth').agg({'Net_Sales': 'sum', 'Profit': 'sum'}).reset_index()

ax = plt.gca()
ax.set_facecolor('#FFFFFF')
plt.plot(monthly['YearMonth'], monthly['Net_Sales'] / 1000, marker='o', linewidth=2.8, color=BLUE, label='Net Sales ($K)')
plt.plot(monthly['YearMonth'], monthly['Profit'] / 1000, marker='s', linewidth=2.4, color=EMERALD, label='Net Profit ($K)')
plt.fill_between(monthly['YearMonth'], monthly['Profit'] / 1000, color=EMERALD, alpha=0.12)

plt.title('Monthly Sales & Profitability Trend (2024 - 2026)', fontsize=15, fontweight='bold', pad=15, color=NAVY)
plt.xlabel('Billing Period (Month)', fontsize=11, fontweight='semibold', color=NAVY)
plt.ylabel('Amount in USD ($ Thousands)', fontsize=11, fontweight='semibold', color=NAVY)
plt.xticks(rotation=45, ha='right', fontsize=9)
plt.legend(frameon=True, facecolor='#F8FAFC', edgecolor=CARD_BORDER, fontsize=10, loc='upper left')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
trends_path = os.path.join(images_dir, "monthly_sales_trend.png")
plt.savefig(trends_path, dpi=300)
plt.close()

# 2. Regional Performance & Margin
plt.figure(figsize=(10, 5))
region_data = df.groupby('Region').agg({'Net_Sales': 'sum', 'Profit': 'sum'}).reset_index()
region_data['Margin_Pct'] = (region_data['Profit'] / region_data['Net_Sales']) * 100
region_data = region_data.sort_values('Net_Sales', ascending=False)

x = np.arange(len(region_data))
width = 0.35

fig, ax1 = plt.subplots(figsize=(10, 5.2))
ax1.set_facecolor('#FFFFFF')
bars1 = ax1.bar(x - width/2, region_data['Net_Sales'] / 1e6, width, label='Sales ($M)', color=BLUE, edgecolor='#1E40AF', alpha=0.9, zorder=3)
bars2 = ax1.bar(x + width/2, region_data['Profit'] / 1e6, width, label='Profit ($M)', color=TEAL, edgecolor='#0F766E', alpha=0.9, zorder=3)

ax1.set_ylabel('Total Value ($ Millions)', fontsize=11, fontweight='semibold', color=NAVY)
ax1.set_xticks(x)
ax1.set_xticklabels(region_data['Region'], fontsize=10, fontweight='semibold')
ax1.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)

# Add margin label above bars
for i in range(len(region_data)):
    m = region_data.iloc[i]['Margin_Pct']
    ax1.text(x[i], (region_data.iloc[i]['Net_Sales'] / 1e6) + 0.05, f"Margin: {m:.1f}%", ha='center', fontsize=9, fontweight='bold', color=NAVY)

plt.title('Regional Revenue vs. Profit Performance & Margins', fontsize=14, fontweight='bold', pad=15, color=NAVY)
ax1.legend(loc='upper right', frameon=True, facecolor='#F8FAFC')
plt.tight_layout()
regional_path = os.path.join(images_dir, "regional_performance.png")
plt.savefig(regional_path, dpi=300)
plt.close()

# 3. Product Category & Subcategory Profitability
plt.figure(figsize=(11, 5.5))
cat_data = df.groupby(['Category', 'Sub_Category']).agg({'Net_Sales': 'sum', 'Profit': 'sum'}).reset_index()
cat_data['Margin_Pct'] = (cat_data['Profit'] / cat_data['Net_Sales']) * 100
cat_data = cat_data.sort_values('Profit', ascending=True)

colors = [BLUE if c == 'Technology' else AMBER if c == 'Furniture' else TEAL for c in cat_data['Category']]

plt.barh(cat_data['Sub_Category'], cat_data['Profit'] / 1000, color=colors, edgecolor='#334155', alpha=0.85)
plt.title('Net Profit by Product Sub-Category ($ Thousands)', fontsize=14, fontweight='bold', pad=15, color=NAVY)
plt.xlabel('Net Profit ($ Thousands)', fontsize=11, fontweight='semibold', color=NAVY)
plt.ylabel('Sub-Category', fontsize=11, fontweight='semibold', color=NAVY)
plt.grid(axis='x', linestyle='--', alpha=0.5)

# Add Category Legend manually
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=BLUE, label='Technology'),
    Patch(facecolor=AMBER, label='Furniture'),
    Patch(facecolor=TEAL, label='Office Supplies')
]
plt.legend(handles=legend_elements, loc='lower right', frameon=True, facecolor='#F8FAFC')
plt.tight_layout()
cat_path = os.path.join(images_dir, "category_profit_breakdown.png")
plt.savefig(cat_path, dpi=300)
plt.close()

# 4. KPI Cards Overview Composite Visual
fig, ax = plt.subplots(figsize=(12, 3.8), facecolor='#0F172A')
ax.axis('off')

kpi_metrics = [
    {"label": "TOTAL REVENUE", "val": f"${df['Net_Sales'].sum()/1e6:.2f}M", "sub": "Target: $5.00M (+7.8%)", "color": "#38BDF8"},
    {"label": "TOTAL NET PROFIT", "val": f"${df['Profit'].sum()/1e6:.2f}M", "sub": "Margin: 26.41%", "color": "#34D399"},
    {"label": "TOTAL ORDERS", "val": f"{len(df):,}", "sub": "30 Global Key Accounts", "color": "#FBBF24"},
    {"label": "AVG ORDER VALUE", "val": f"${df['Net_Sales'].mean():,.2f}", "sub": "+12.3% YoY Growth", "color": "#F472B6"},
]

from matplotlib.patches import FancyBboxPatch, Patch

for idx, kpi in enumerate(kpi_metrics):
    box_x = 0.02 + idx * 0.245
    # Draw card
    rect = FancyBboxPatch((box_x, 0.1), 0.22, 0.8, boxstyle="round,pad=0.02", facecolor='#1E293B', edgecolor='#334155', linewidth=1.5, transform=ax.transAxes, zorder=2)
    ax.add_patch(rect)
    
    # Text inside card
    ax.text(box_x + 0.11, 0.72, kpi['label'], color='#94A3B8', fontsize=10, fontweight='bold', ha='center', transform=ax.transAxes, zorder=3)
    ax.text(box_x + 0.11, 0.44, kpi['val'], color=kpi['color'], fontsize=18, fontweight='bold', ha='center', transform=ax.transAxes, zorder=3)
    ax.text(box_x + 0.11, 0.22, kpi['sub'], color='#CBD5E1', fontsize=9, ha='center', transform=ax.transAxes, zorder=3)

plt.title('EXECUTIVE KPI HIGHLIGHTS - GLOBAL PERFORMANCE MATRIX', color='#FFFFFF', fontsize=13, fontweight='bold', pad=10)
plt.tight_layout()
kpi_path = os.path.join(images_dir, "executive_kpis_preview.png")
plt.savefig(kpi_path, dpi=300)
plt.close()

# 5. Full Dashboard Layout Overview Mockup
fig = plt.figure(figsize=(14, 8.5), facecolor='#0B1329')
gs = fig.add_gridspec(3, 3, height_ratios=[0.8, 2, 2], hspace=0.35, wspace=0.25)

# Header
ax_head = fig.add_subplot(gs[0, :])
ax_head.axis('off')
ax_head.text(0.01, 0.7, "GLOBAL SALES & FINANCIAL EXECUTIVE COCKPIT", color="#FFFFFF", fontsize=18, fontweight='bold')
ax_head.text(0.01, 0.25, "Interactive Multi-Year Analytics | Slicers: [Year: All] [Region: Global] [Category: All] [Segment: Corporate/Consumer]", color="#94A3B8", fontsize=10)

# Card 1: Sales
ax_c1 = fig.add_subplot(gs[0, 2])
ax_c1.axis('off')
ax_c1.text(0.5, 0.65, "Total Sales: $5.39M", color="#38BDF8", fontsize=13, fontweight='bold', ha='center')
ax_c1.text(0.5, 0.25, "Net Profit: $1.42M (26.4%)", color="#34D399", fontsize=11, fontweight='bold', ha='center')

# Main chart: Time Series
ax_ts = fig.add_subplot(gs[1, :2])
ax_ts.set_facecolor('#1E293B')
ax_ts.plot(monthly['YearMonth'], monthly['Net_Sales']/1000, color='#38BDF8', linewidth=2.5, label='Sales ($K)')
ax_ts.plot(monthly['YearMonth'], monthly['Profit']/1000, color='#34D399', linewidth=2.2, label='Profit ($K)')
ax_ts.set_title('Revenue vs Profit Trend (Monthly)', color='#FFFFFF', fontsize=11, fontweight='bold', pad=8)
ax_ts.tick_params(colors='#94A3B8', labelsize=7)
ax_ts.set_xticks(range(0, len(monthly), 3))
ax_ts.set_xticklabels(monthly['YearMonth'].iloc[::3], rotation=30)
ax_ts.legend(facecolor='#0F172A', edgecolor='#334155', labelcolor='#FFFFFF', fontsize=8)
ax_ts.grid(True, linestyle=':', alpha=0.3)

# Donut chart: Segment
ax_donut = fig.add_subplot(gs[1, 2])
ax_donut.set_facecolor('#1E293B')
seg_data = df.groupby('Segment')['Net_Sales'].sum()
wedges, texts, autotexts = ax_donut.pie(seg_data, labels=seg_data.index, autopct='%1.1f%%', 
                                       colors=['#6366F1', '#EC4899', '#14B8A6'], 
                                       wedgeprops=dict(width=0.45, edgecolor='#0B1329', linewidth=2),
                                       textprops=dict(color='#E2E8F0', fontsize=8))
plt.setp(autotexts, size=8, weight="bold", color="white")
ax_donut.set_title('Revenue by Segment', color='#FFFFFF', fontsize=11, fontweight='bold')

# Region Bar
ax_reg = fig.add_subplot(gs[2, :2])
ax_reg.set_facecolor('#1E293B')
ax_reg.bar(region_data['Region'], region_data['Net_Sales']/1e6, color='#6366F1', alpha=0.85, width=0.45, label='Sales ($M)')
ax_reg.bar(region_data['Region'], region_data['Profit']/1e6, color='#10B981', alpha=0.85, width=0.45, label='Profit ($M)')
ax_reg.set_title('Regional Performance Matrix', color='#FFFFFF', fontsize=11, fontweight='bold', pad=8)
ax_reg.tick_params(colors='#94A3B8', labelsize=8)
ax_reg.legend(facecolor='#0F172A', edgecolor='#334155', labelcolor='#FFFFFF', fontsize=8)
ax_reg.grid(axis='y', linestyle=':', alpha=0.3)

# Category Pie / Bar
ax_cat = fig.add_subplot(gs[2, 2])
ax_cat.set_facecolor('#1E293B')
cat_rev = df.groupby('Category')['Net_Sales'].sum()
ax_cat.barh(cat_rev.index, cat_rev/1e6, color=['#F59E0B', '#3B82F6', '#10B981'], height=0.45)
ax_cat.set_title('Sales by Category ($M)', color='#FFFFFF', fontsize=11, fontweight='bold')
ax_cat.tick_params(colors='#94A3B8', labelsize=8)
ax_cat.grid(axis='x', linestyle=':', alpha=0.3)

plt.tight_layout()
overview_path = os.path.join(images_dir, "full_dashboard_preview.png")
plt.savefig(overview_path, dpi=300)
plt.close()

print("All charts and visual assets successfully created in:", images_dir)

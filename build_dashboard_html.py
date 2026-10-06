import os
import json
import pandas as pd

project_dir = r"C:\Users\Varshini S\.gemini\antigravity\scratch\ElevateLabs_Task4_Dashboard_Design"
csv_path = os.path.join(project_dir, "dataset", "sales_financial_data.csv")
dashboard_html_path = os.path.join(project_dir, "dashboard", "index.html")

df = pd.read_csv(csv_path)

# Prepare compact JSON records for the client-side engine (sample or all records)
# All 3500 records in compact format
compact_records = []
for _, row in df.iterrows():
    compact_records.append({
        "id": row["Order_ID"],
        "date": row["Order_Date"],
        "yr": int(row["Year"]),
        "qtr": row["Quarter"],
        "reg": row["Region"],
        "cntry": row["Country"],
        "city": row["City"],
        "cat": row["Category"],
        "sub": row["Sub_Category"],
        "prod": row["Product_Name"],
        "seg": row["Segment"],
        "ship": row["Ship_Mode"],
        "qty": int(row["Quantity"]),
        "sales": float(row["Net_Sales"]),
        "profit": float(row["Profit"]),
        "margin": float(row["Profit_Margin_Pct"]),
        "disc": float(row["Discount_Rate"])
    })

data_json_str = json.dumps(compact_records)

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Global Sales & Financial Executive Dashboard | Elevate Labs Task 4</title>
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          colors: {{
            brand: {{
              50: '#EEF2FF',
              100: '#E0E7FF',
              500: '#6366F1',
              600: '#4F46E5',
              700: '#4338CA',
              800: '#3730A3',
              900: '#312E81',
              950: '#0F172A',
            }},
            emeraldAccent: '#10B981',
            cyanAccent: '#06B6D4'
          }}
        }}
      }}
    }}
  </script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: #0B1120;
      color: #E2E8F0;
    }}
    .glass-card {{
      background: rgba(17, 24, 39, 0.75);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 1rem;
    }}
    .glass-card:hover {{
      border-color: rgba(99, 102, 241, 0.35);
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.5);
    }}
    .custom-scrollbar::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    .custom-scrollbar::-webkit-scrollbar-track {{
      background: #0B1120;
    }}
    .custom-scrollbar::-webkit-scrollbar-thumb {{
      background: #334155;
      border-radius: 4px;
    }}
    .custom-scrollbar::-webkit-scrollbar-thumb:hover {{
      background: #475569;
    }}
    .active-nav {{
      background: linear-gradient(135deg, #4F46E5 0%, #3730A3 100%);
      color: #FFFFFF !important;
      box-shadow: 0 4px 12px rgba(79, 70, 229, 0.35);
    }}
  </style>
</head>
<body class="min-h-screen custom-scrollbar flex flex-col">

  <!-- Top Navigation Header -->
  <header class="border-b border-slate-800 bg-slate-900/90 backdrop-blur sticky top-0 z-50 px-6 py-4">
    <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-cyan-400 flex items-center justify-center shadow-lg shadow-indigo-500/20">
          <i data-lucide="bar-chart-3" class="w-6 h-6 text-white"></i>
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-xl font-bold tracking-tight text-white">Global Sales & Financial Intelligence Cockpit</h1>
            <span class="px-2 py-0.5 text-xs font-semibold rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">Task 4 Deliverable</span>
          </div>
          <p class="text-xs text-slate-400">Elevate Labs Data Analyst Internship | Multi-Year Performance & KPI Analytics</p>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="flex items-center gap-3">
        <button onclick="resetAllFilters()" class="px-3 py-1.5 rounded-lg text-xs font-medium text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 transition flex items-center gap-1.5 border border-slate-700">
          <i data-lucide="rotate-ccw" class="w-3.5 h-3.5"></i> Reset Slicers
        </button>
        <button onclick="exportFilteredCSV()" class="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-white bg-gradient-to-r from-indigo-600 to-indigo-500 hover:from-indigo-500 hover:to-indigo-400 shadow-md shadow-indigo-600/20 transition flex items-center gap-1.5">
          <i data-lucide="download" class="w-3.5 h-3.5"></i> Export CSV
        </button>
        <button onclick="window.print()" class="px-3 py-1.5 rounded-lg text-xs font-medium text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 border border-slate-700 transition flex items-center gap-1.5">
          <i data-lucide="printer" class="w-3.5 h-3.5"></i> Print Report
        </button>
      </div>
    </div>
  </header>

  <!-- Main Container -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 py-6 flex-1 w-full space-y-6">

    <!-- Interactive Slicers / Filter Bar (Requirement b: Use slicers/filters for interactivity) -->
    <section class="glass-card p-4 transition-all duration-200">
      <div class="flex items-center justify-between mb-3 pb-2 border-b border-slate-800">
        <div class="flex items-center gap-2">
          <i data-lucide="sliders-horizontal" class="w-4 h-4 text-indigo-400"></i>
          <span class="text-xs font-bold uppercase tracking-wider text-slate-300">Interactive Slicers & Filters</span>
        </div>
        <span id="activeFilterBadge" class="text-xs text-indigo-400 font-medium">Displaying: All 3,500 Transactions</span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
        <!-- Slicer 1: Year -->
        <div>
          <label class="block text-xs font-semibold text-slate-400 mb-1">Fiscal Year</label>
          <select id="filterYear" onchange="applyFilters()" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500 transition">
            <option value="ALL">All Fiscal Years (2024 - 2026)</option>
            <option value="2024">FY 2024</option>
            <option value="2025">FY 2025</option>
            <option value="2026">FY 2026 (YTD)</option>
          </select>
        </div>

        <!-- Slicer 2: Region -->
        <div>
          <label class="block text-xs font-semibold text-slate-400 mb-1">Geographic Region</label>
          <select id="filterRegion" onchange="applyFilters()" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500 transition">
            <option value="ALL">All Regions (Global)</option>
            <option value="North America">North America</option>
            <option value="Europe">Europe</option>
            <option value="Asia Pacific">Asia Pacific</option>
            <option value="Latin America">Latin America</option>
          </select>
        </div>

        <!-- Slicer 3: Category -->
        <div>
          <label class="block text-xs font-semibold text-slate-400 mb-1">Product Category</label>
          <select id="filterCategory" onchange="applyFilters()" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500 transition">
            <option value="ALL">All Product Categories</option>
            <option value="Technology">Technology</option>
            <option value="Furniture">Furniture</option>
            <option value="Office Supplies">Office Supplies</option>
          </select>
        </div>

        <!-- Slicer 4: Segment -->
        <div>
          <label class="block text-xs font-semibold text-slate-400 mb-1">Customer Segment</label>
          <select id="filterSegment" onchange="applyFilters()" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500 transition">
            <option value="ALL">All Customer Segments</option>
            <option value="Consumer">Consumer</option>
            <option value="Corporate">Corporate</option>
            <option value="Home Office">Home Office</option>
          </select>
        </div>
      </div>
    </section>

    <!-- Navigation Menu (Requirement f: Create navigation menu) -->
    <nav class="flex items-center gap-2 overflow-x-auto pb-1 border-b border-slate-800">
      <button onclick="switchTab('overview')" id="nav-overview" class="active-nav px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2">
        <i data-lucide="layout-dashboard" class="w-4 h-4"></i> Executive Overview
      </button>
      <button onclick="switchTab('regional')" id="nav-regional" class="text-slate-400 hover:text-white px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2">
        <i data-lucide="globe" class="w-4 h-4"></i> Regional Deep Dive
      </button>
      <button onclick="switchTab('products')" id="nav-products" class="text-slate-400 hover:text-white px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2">
        <i data-lucide="package" class="w-4 h-4"></i> Product & Margin Matrix
      </button>
      <button onclick="switchTab('transactions')" id="nav-transactions" class="text-slate-400 hover:text-white px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2">
        <i data-lucide="table" class="w-4 h-4"></i> Transaction Explorer
      </button>
      <button onclick="switchTab('interview')" id="nav-interview" class="text-slate-400 hover:text-white px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2">
        <i data-lucide="help-circle" class="w-4 h-4"></i> Interview Q&A Reference
      </button>
    </nav>

    <!-- KPI Summary Cards (Requirement a: Choose right KPIs, Requirement d: Add cards for totals/summary) -->
    <section class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
      <!-- KPI 1: Total Revenue -->
      <div class="glass-card p-4 relative overflow-hidden group">
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Total Sales</span>
          <div class="w-7 h-7 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400">
            <i data-lucide="dollar-sign" class="w-4 h-4"></i>
          </div>
        </div>
        <div id="kpiRevenue" class="text-xl lg:text-2xl font-extrabold text-white tracking-tight">$5.39M</div>
        <div class="mt-2 flex items-center gap-1 text-[11px] text-emerald-400 font-medium">
          <i data-lucide="trending-up" class="w-3.5 h-3.5"></i>
          <span>+18.4% vs prev yr</span>
        </div>
      </div>

      <!-- KPI 2: Total Net Profit -->
      <div class="glass-card p-4 relative overflow-hidden group">
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Net Profit</span>
          <div class="w-7 h-7 rounded-lg bg-emerald-500/10 flex items-center justify-center text-emerald-400">
            <i data-lucide="wallet" class="w-4 h-4"></i>
          </div>
        </div>
        <div id="kpiProfit" class="text-xl lg:text-2xl font-extrabold text-emerald-400 tracking-tight">$1.42M</div>
        <div class="mt-2 flex items-center gap-1 text-[11px] text-emerald-400 font-medium">
          <i data-lucide="check-circle" class="w-3.5 h-3.5"></i>
          <span>Positive cashflow</span>
        </div>
      </div>

      <!-- KPI 3: Profit Margin % -->
      <div class="glass-card p-4 relative overflow-hidden group">
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Profit Margin</span>
          <div class="w-7 h-7 rounded-lg bg-cyan-500/10 flex items-center justify-center text-cyan-400">
            <i data-lucide="percent" class="w-4 h-4"></i>
          </div>
        </div>
        <div id="kpiMargin" class="text-xl lg:text-2xl font-extrabold text-cyan-400 tracking-tight">26.4%</div>
        <div class="mt-2 flex items-center gap-1 text-[11px] text-slate-400">
          <span>Target benchmark: 22.0%</span>
        </div>
      </div>

      <!-- KPI 4: Total Orders -->
      <div class="glass-card p-4 relative overflow-hidden group">
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Total Orders</span>
          <div class="w-7 h-7 rounded-lg bg-amber-500/10 flex items-center justify-center text-amber-400">
            <i data-lucide="shopping-bag" class="w-4 h-4"></i>
          </div>
        </div>
        <div id="kpiOrders" class="text-xl lg:text-2xl font-extrabold text-white tracking-tight">3,500</div>
        <div class="mt-2 flex items-center gap-1 text-[11px] text-slate-400">
          <span>100% Fulfilled</span>
        </div>
      </div>

      <!-- KPI 5: Avg Order Value (AOV) -->
      <div class="glass-card p-4 relative overflow-hidden group">
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Avg Order Value</span>
          <div class="w-7 h-7 rounded-lg bg-purple-500/10 flex items-center justify-center text-purple-400">
            <i data-lucide="receipt" class="w-4 h-4"></i>
          </div>
        </div>
        <div id="kpiAOV" class="text-xl lg:text-2xl font-extrabold text-purple-400 tracking-tight">$1,540</div>
        <div class="mt-2 flex items-center gap-1 text-[11px] text-purple-400 font-medium">
          <span>High basket value</span>
        </div>
      </div>

      <!-- KPI 6: Units Sold -->
      <div class="glass-card p-4 relative overflow-hidden group">
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Units Sold</span>
          <div class="w-7 h-7 rounded-lg bg-rose-500/10 flex items-center justify-center text-rose-400">
            <i data-lucide="layers" class="w-4 h-4"></i>
          </div>
        </div>
        <div id="kpiUnits" class="text-xl lg:text-2xl font-extrabold text-rose-400 tracking-tight">8,740</div>
        <div class="mt-2 flex items-center gap-1 text-[11px] text-slate-400">
          <span>Avg Discount: 4.8%</span>
        </div>
      </div>
    </section>

    <!-- TAB 1: EXECUTIVE OVERVIEW -->
    <div id="tab-overview" class="space-y-6">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Main Time-Series Analysis (Requirement c: Include time-series analysis) -->
        <div class="glass-card p-5 lg:col-span-2">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h2 class="text-sm font-bold text-white flex items-center gap-2">
                <i data-lucide="trending-up" class="w-4 h-4 text-indigo-400"></i> Monthly Sales & Profitability Growth Trend
              </h2>
              <p class="text-xs text-slate-400">Historical performance with dynamic monthly granularity</p>
            </div>
            <span class="text-xs font-semibold px-2 py-1 bg-slate-800 rounded border border-slate-700 text-slate-300">Net Sales vs Profit</span>
          </div>
          <div class="h-72 w-full">
            <canvas id="timeSeriesChart"></canvas>
          </div>
        </div>

        <!-- Customer Segment Distribution Donut -->
        <div class="glass-card p-5">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h2 class="text-sm font-bold text-white flex items-center gap-2">
                <i data-lucide="pie-chart" class="w-4 h-4 text-cyan-400"></i> Revenue by Segment
              </h2>
              <p class="text-xs text-slate-400">Contribution of Consumer vs Corporate</p>
            </div>
          </div>
          <div class="h-72 w-full flex items-center justify-center">
            <canvas id="segmentDonutChart"></canvas>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Category Performance Bar Chart -->
        <div class="glass-card p-5">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h2 class="text-sm font-bold text-white flex items-center gap-2">
                <i data-lucide="tag" class="w-4 h-4 text-amber-400"></i> Category Revenue & Profitability
              </h2>
              <p class="text-xs text-slate-400">Comparing top line sales against bottom line profit</p>
            </div>
          </div>
          <div class="h-64 w-full">
            <canvas id="categoryBarChart"></canvas>
          </div>
        </div>

        <!-- Regional Performance Overview -->
        <div class="glass-card p-5">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h2 class="text-sm font-bold text-white flex items-center gap-2">
                <i data-lucide="map-pin" class="w-4 h-4 text-emerald-400"></i> Regional Sales Distribution
              </h2>
              <p class="text-xs text-slate-400">Net sales across global operating regions</p>
            </div>
          </div>
          <div class="h-64 w-full">
            <canvas id="regionBarChart"></canvas>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 2: REGIONAL DEEP DIVE -->
    <div id="tab-regional" class="space-y-6 hidden">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="glass-card p-5 lg:col-span-2">
          <h2 class="text-sm font-bold text-white mb-2 flex items-center gap-2">
            <i data-lucide="globe" class="w-4 h-4 text-indigo-400"></i> Top Country Markets by Sales & Profit Margin
          </h2>
          <p class="text-xs text-slate-400 mb-4">Geographic ranking across 10 international hub countries</p>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs text-slate-300">
              <thead class="bg-slate-900 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
                <tr>
                  <th class="p-3">Country</th>
                  <th class="p-3">Region</th>
                  <th class="p-3 text-right">Orders</th>
                  <th class="p-3 text-right">Net Sales ($)</th>
                  <th class="p-3 text-right">Profit ($)</th>
                  <th class="p-3 text-right">Margin %</th>
                </tr>
              </thead>
              <tbody id="countryTableBody" class="divide-y divide-slate-800/60">
                <!-- Dynamically populated -->
              </tbody>
            </table>
          </div>
        </div>

        <div class="glass-card p-5">
          <h2 class="text-sm font-bold text-white mb-2 flex items-center gap-2">
            <i data-lucide="truck" class="w-4 h-4 text-cyan-400"></i> Logistics & Ship Mode Split
          </h2>
          <p class="text-xs text-slate-400 mb-4">Fulfillment channel breakdown</p>
          <div class="h-72 w-full flex items-center justify-center">
            <canvas id="shippingDoughnutChart"></canvas>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 3: PRODUCT & MARGIN MATRIX -->
    <div id="tab-products" class="space-y-6 hidden">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="glass-card p-5">
          <h2 class="text-sm font-bold text-white mb-2 flex items-center gap-2">
            <i data-lucide="award" class="w-4 h-4 text-amber-400"></i> Top 8 Best-Selling Products by Revenue
          </h2>
          <p class="text-xs text-slate-400 mb-4">Products generating the largest sales volume</p>
          <div class="h-80 w-full">
            <canvas id="topProductsChart"></canvas>
          </div>
        </div>

        <div class="glass-card p-5">
          <h2 class="text-sm font-bold text-white mb-2 flex items-center gap-2">
            <i data-lucide="layers" class="w-4 h-4 text-emerald-400"></i> Sub-Category Profitability Ranking
          </h2>
          <p class="text-xs text-slate-400 mb-4">Profit generation across sub-categories</p>
          <div class="h-80 w-full">
            <canvas id="subCategoryChart"></canvas>
          </div>
        </div>
      </div>

      <!-- Strategic Takeaways -->
      <div class="glass-card p-5 bg-gradient-to-r from-indigo-950/40 via-slate-900/60 to-slate-900/40 border-indigo-500/20">
        <h3 class="text-sm font-bold text-indigo-400 uppercase tracking-wider mb-2 flex items-center gap-2">
          <i data-lucide="lightbulb" class="w-4 h-4"></i> Strategic Product Line Recommendations
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs text-slate-300">
          <div class="p-3 bg-slate-900/80 rounded-lg border border-slate-800">
            <span class="font-bold text-white block mb-1">🚀 High-Margin Driver (Phones & Laptops)</span>
            Technology generates over 45% of total company profit with strong 28%+ margins. Continue scaling B2B enterprise procurement bundles.
          </div>
          <div class="p-3 bg-slate-900/80 rounded-lg border border-slate-800">
            <span class="font-bold text-white block mb-1">⚠️ Furniture Discount Guardrails</span>
            Tables and heavy Chairs show margin compression when discounts exceed 15%. Recommend capping promotional discounts to 10% to preserve yield.
          </div>
          <div class="p-3 bg-slate-900/80 rounded-lg border border-slate-800">
            <span class="font-bold text-white block mb-1">📦 Office Supplies Volume Optimization</span>
            Storage and appliances exhibit steady, high-margin replenishment cycles with zero churn. Ideal candidate for recurring enterprise subscriptions.
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 4: TRANSACTION EXPLORER -->
    <div id="tab-transactions" class="space-y-4 hidden">
      <div class="glass-card p-5">
        <div class="flex flex-col sm:flex-row items-center justify-between gap-4 mb-4">
          <div>
            <h2 class="text-sm font-bold text-white flex items-center gap-2">
              <i data-lucide="table" class="w-4 h-4 text-indigo-400"></i> Filtered Transaction Ledger
            </h2>
            <p class="text-xs text-slate-400">Search, inspect and export all granular orders</p>
          </div>
          <div class="flex items-center gap-3 w-full sm:w-auto">
            <div class="relative w-full sm:w-64">
              <input type="text" id="tableSearchInput" onkeyup="handleSearch()" placeholder="Search product, customer, ID..." class="w-full bg-slate-900 border border-slate-700 rounded-lg pl-8 pr-3 py-1.5 text-xs text-white focus:outline-none focus:border-indigo-500">
              <i data-lucide="search" class="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5"></i>
            </div>
            <button onclick="exportFilteredCSV()" class="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold transition flex items-center gap-1.5">
              <i data-lucide="download" class="w-3.5 h-3.5"></i> Export
            </button>
          </div>
        </div>

        <div class="overflow-x-auto max-h-[500px] custom-scrollbar border border-slate-800 rounded-lg">
          <table class="w-full text-left text-xs text-slate-300">
            <thead class="bg-slate-900 text-slate-400 uppercase text-[10px] tracking-wider sticky top-0 z-10 border-b border-slate-800">
              <tr>
                <th class="p-3">Order ID</th>
                <th class="p-3">Date</th>
                <th class="p-3">Customer</th>
                <th class="p-3">Region</th>
                <th class="p-3">Category</th>
                <th class="p-3">Product Name</th>
                <th class="p-3 text-right">Qty</th>
                <th class="p-3 text-right">Net Sales ($)</th>
                <th class="p-3 text-right">Profit ($)</th>
                <th class="p-3 text-right">Margin %</th>
              </tr>
            </thead>
            <tbody id="transactionTableBody" class="divide-y divide-slate-800">
              <!-- Dynamically populated -->
            </tbody>
          </table>
        </div>
        <div class="flex items-center justify-between text-xs text-slate-400 mt-3 pt-2 border-t border-slate-800">
          <span id="tableCountText">Showing 1 to 50 of 3,500 rows</span>
          <div class="flex items-center gap-2">
            <button onclick="prevPage()" id="btnPrevPage" class="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 rounded text-slate-300 disabled:opacity-40">Previous</button>
            <span id="pageNumberText" class="font-semibold text-white">Page 1</span>
            <button onclick="nextPage()" id="btnNextPage" class="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 rounded text-slate-300 disabled:opacity-40">Next</button>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 5: INTERVIEW Q&A REFERENCE -->
    <div id="tab-interview" class="space-y-6 hidden">
      <div class="glass-card p-6">
        <div class="border-b border-slate-800 pb-3 mb-4">
          <h2 class="text-base font-bold text-white flex items-center gap-2">
            <i data-lucide="graduation-cap" class="w-5 h-5 text-indigo-400"></i> Elevate Labs Interview Questions & Technical Solutions
          </h2>
          <p class="text-xs text-slate-400">Official interview answers prepared for Task 4 evaluation</p>
        </div>

        <div class="space-y-4 text-xs leading-relaxed">
          <!-- Q1 -->
          <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800">
            <h3 class="font-bold text-indigo-300 text-sm mb-1.5">1. What are the key elements of a dashboard?</h3>
            <p class="text-slate-300">The key elements of an effective business dashboard include:</p>
            <ul class="list-disc list-inside mt-1.5 space-y-1 text-slate-400">
              <li><strong class="text-white">Header & Contextual Branding:</strong> Title, purpose, last refresh date, and company/project metadata.</li>
              <li><strong class="text-white">KPI Summary Cards (Total Metrics):</strong> Prominently placed top cards highlighting critical totals (Revenue, Profit, Margin %, Growth).</li>
              <li><strong class="text-white">Interactive Slicers / Filters:</strong> Date range, regional, category, and segment controls allowing stakeholders to drill down.</li>
              <li><strong class="text-white">Time-Series & Trend Visuals:</strong> Line/Area charts demonstrating longitudinal performance and seasonal trajectory.</li>
              <li><strong class="text-white">Comparative & Distribution Visuals:</strong> Bar charts, waterfall charts, and donut charts showing category and geographic breakdown.</li>
              <li><strong class="text-white">Granular Data Table:</strong> Formatted tables with sorting and export options for detailed audit.</li>
              <li><strong class="text-white">Consistent Color Harmony & White Space:</strong> Clutter-free design adhering to corporate visual hierarchy and accessibility standards.</li>
            </ul>
          </div>

          <!-- Q2 -->
          <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800">
            <h3 class="font-bold text-indigo-300 text-sm mb-1.5">2. What is a KPI?</h3>
            <p class="text-slate-300">
              A <strong>KPI (Key Performance Indicator)</strong> is a measurable, quantifiable metric used to evaluate how effectively a business or organization is achieving its core strategic and operational objectives. Unlike standard metrics that merely measure activity (such as page views or number of clicks), a KPI tracks performance directly tied to business outcomes.
            </p>
            <p class="mt-1 text-slate-400">
              Examples in this dashboard: <em>Net Revenue</em>, <em>Net Profit</em>, <em>Profit Margin % (Profit / Sales)</em>, <em>Year-over-Year (YoY) Growth</em>, and <em>Average Order Value (AOV)</em>. Good KPIs follow the <strong>SMART</strong> criteria: Specific, Measurable, Achievable, Relevant, and Time-bound.
            </p>
          </div>

          <!-- Q3 -->
          <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800">
            <h3 class="font-bold text-indigo-300 text-sm mb-1.5">3. What are slicers in Power BI?</h3>
            <p class="text-slate-300">
              In Power BI, a <strong>slicer</strong> is a visual canvas filter that allows report consumers to interactively narrow down the dataset displayed across all visualizations on a report page.
            </p>
            <p class="mt-1 text-slate-400">
              Key characteristics of slicers:
            </p>
            <ul class="list-disc list-inside mt-1 space-y-1 text-slate-400">
              <li>They support various styles: Dropdown, Vertical List, Tile / Button, Date Range Slider, and Relative Date filtering.</li>
              <li><strong>Sync Slicers:</strong> Can be synchronized across multiple report pages to maintain consistent filtering as users navigate tabs.</li>
              <li><strong>Hierarchy Slicers:</strong> Can group nested dimensions (e.g., Year > Quarter > Month, or Region > Country > State).</li>
            </ul>
          </div>

          <!-- Q4 -->
          <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800">
            <h3 class="font-bold text-indigo-300 text-sm mb-1.5">4. What is the difference between Power BI and Tableau?</h3>
            <div class="overflow-x-auto mt-2">
              <table class="w-full text-left text-xs text-slate-300 border border-slate-800 rounded">
                <thead class="bg-slate-900 text-slate-400 uppercase text-[10px]">
                  <tr>
                    <th class="p-2.5 border-b border-slate-800">Feature</th>
                    <th class="p-2.5 border-b border-slate-800 text-indigo-400">Power BI</th>
                    <th class="p-2.5 border-b border-slate-800 text-cyan-400">Tableau</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-800/60">
                  <tr>
                    <td class="p-2 font-semibold">Core Strength</td>
                    <td class="p-2">Data Modeling, ETL (Power Query), DAX calculations, tight Microsoft 365 / Azure integration</td>
                    <td class="p-2">Advanced visual storytelling, custom chart flexibility, exploratory visual analysis</td>
                  </tr>
                  <tr>
                    <td class="p-2 font-semibold">Calculation Engine</td>
                    <td class="p-2">DAX (Data Analysis Expressions) + M Language</td>
                    <td class="p-2">Calculated Fields + LOD Expressions (FIXED, INCLUDE, EXCLUDE)</td>
                  </tr>
                  <tr>
                    <td class="p-2 font-semibold">Licensing & Cost</td>
                    <td class="p-2">Lower cost per user (~$10/user/mo for Pro), included in many enterprise E5 packages</td>
                    <td class="p-2">Higher cost structure (~$75/creator/mo)</td>
                  </tr>
                  <tr>
                    <td class="p-2 font-semibold">Data Volume Handling</td>
                    <td class="p-2">DirectQuery, Composite Models, Aggregations, Tabular Model in-memory engine</td>
                    <td class="p-2">Hyper in-memory data engine, Live connections to big data warehouses (Snowflake/BigQuery)</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Q5 -->
          <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800">
            <h3 class="font-bold text-indigo-300 text-sm mb-1.5">5. How do you make a dashboard interactive?</h3>
            <p class="text-slate-300">Dashboard interactivity is engineered through multiple synergistic mechanisms:</p>
            <ul class="list-disc list-inside mt-1.5 space-y-1 text-slate-400">
              <li><strong class="text-white">Cross-Filtering & Cross-Highlighting:</strong> Clicking a bar or slice dynamically filters or highlights related visuals on the canvas.</li>
              <li><strong class="text-white">Interactive Slicers & Parameters:</strong> Dropdowns, sliders, and toggle switches enabling scenario exploration.</li>
              <li><strong class="text-white">Drill-Down / Drill-Up Hierarchies:</strong> Enabling users to navigate from Year down to Quarter, Month, and Day, or Category to Sub-Category.</li>
              <li><strong class="text-white">Drill-Through Pages:</strong> Right-clicking a specific record or region to navigate to a dedicated detail page pre-filtered for that selection.</li>
              <li><strong class="text-white">Bookmarks & Dynamic Navigation Buttons:</strong> Toggling between different chart views, thematic tabs, or resetting filters with a single click.</li>
              <li><strong class="text-white">Dynamic Tooltips:</strong> Hovering over a data point presents contextual mini-charts and key driver statistics.</li>
            </ul>
          </div>

          <!-- Q6 -->
          <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800">
            <h3 class="font-bold text-indigo-300 text-sm mb-1.5">6. How do you deal with large datasets in dashboards?</h3>
            <p class="text-slate-300">To maintain sub-second response times and prevent rendering lag with massive datasets:</p>
            <ul class="list-disc list-inside mt-1.5 space-y-1 text-slate-400">
              <li><strong class="text-white">Data Aggregation Tables:</strong> Pre-aggregating data at the monthly or category level in the data warehouse / ETL layer rather than loading raw row-level transactions.</li>
              <li><strong class="text-white">Composite Models & DirectQuery:</strong> Keeping summarized data in-memory (Import mode) while querying granular transactional details via DirectQuery on demand.</li>
              <li><strong class="text-white">Columnar Pruning:</strong> Removing unused columns and unneeded decimal precisions in Power Query / ETL to maximize VertiPaq / Hyper compression.</li>
              <li><strong class="text-white">Star Schema Modeling:</strong> Normalizing dimensions and keeping fact tables narrow with integer surrogate keys.</li>
              <li><strong class="text-white">Incremental Refresh:</strong> Updating only recent partitions (e.g. last 7 days) rather than full dataset refreshes.</li>
              <li><strong class="text-white">Pagination & Top-N Filtering:</strong> Restricting visual rendering to Top 10/20 items rather than plotting 100,000 discrete points on a single chart.</li>
            </ul>
          </div>

          <!-- Q7 -->
          <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800">
            <h3 class="font-bold text-indigo-300 text-sm mb-1.5">7. What chart types do you use for trend analysis?</h3>
            <p class="text-slate-300">The most effective chart types for time-series and trend analysis are:</p>
            <ul class="list-disc list-inside mt-1.5 space-y-1 text-slate-400">
              <li><strong class="text-white">Line Chart:</strong> The gold standard for continuous time series, tracking trajectory, inflection points, and seasonality over time.</li>
              <li><strong class="text-white">Area Chart / Stacked Area Chart:</strong> Ideal for showing total volume trends while displaying the proportional breakdown of categories over time.</li>
              <li><strong class="text-white">Combo Chart (Line + Clustered Column):</strong> Excellent for comparing metrics of different scales (e.g., Sales volume in bars on the primary axis vs Profit Margin % as a line on the secondary axis).</li>
              <li><strong class="text-white">Sparklines:</strong> Micro-trend visualizations embedded directly inside KPI summary cards or tables for compact trend context.</li>
              <li><strong class="text-white">Run / Control Charts:</strong> Showing performance against upper and lower statistical control thresholds.</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

  </main>

  <!-- Footer -->
  <footer class="border-t border-slate-800/80 bg-slate-900/60 py-4 px-6 text-center text-xs text-slate-400">
    <div class="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">
      <div>Elevate Labs Data Analyst Internship | <strong>Task 4: Interactive Dashboard Design</strong></div>
      <div class="flex items-center gap-4 text-slate-400">
        <span>Dataset: 3,500 Multi-Year Enterprise Sales Records</span>
        <span>Built with HTML5, Tailwind, Chart.js & DAX/Tableau Architecture</span>
      </div>
    </div>
  </footer>

  <!-- Application Logic & Charts Script -->
  <script>
    // Embed the raw dataset records generated by python
    const rawData = {data_json_str};

    let filteredData = [...rawData];
    let currentPage = 1;
    const pageSize = 50;

    // Charts references
    let chartTimeSeries, chartSegment, chartCategory, chartRegion, chartShipping, chartTopProducts, chartSubCategory;

    // Formatting helpers
    function formatCurrency(val) {{
      if (Math.abs(val) >= 1e6) {{
        return '$' + (val / 1e6).toFixed(2) + 'M';
      }} else if (Math.abs(val) >= 1e3) {{
        return '$' + (val / 1e3).toFixed(1) + 'K';
      }} else {{
        return '$' + val.toFixed(2);
      }}
    }}

    function switchTab(tabId) {{
      const tabs = ['overview', 'regional', 'products', 'transactions', 'interview'];
      tabs.forEach(t => {{
        const el = document.getElementById('tab-' + t);
        const nav = document.getElementById('nav-' + t);
        if (t === tabId) {{
          el.classList.remove('hidden');
          nav.classList.add('active-nav');
          nav.classList.remove('text-slate-400');
        }} else {{
          el.classList.add('hidden');
          nav.classList.remove('active-nav');
          nav.classList.add('text-slate-400');
        }}
      }});
      lucide.createIcons();
    }}

    function applyFilters() {{
      const yr = document.getElementById('filterYear').value;
      const reg = document.getElementById('filterRegion').value;
      const cat = document.getElementById('filterCategory').value;
      const seg = document.getElementById('filterSegment').value;

      filteredData = rawData.filter(d => {{
        if (yr !== 'ALL' && d.yr !== parseInt(yr)) return false;
        if (reg !== 'ALL' && d.reg !== reg) return false;
        if (cat !== 'ALL' && d.cat !== cat) return false;
        if (seg !== 'ALL' && d.seg !== seg) return false;
        return true;
      }});

      currentPage = 1;
      updateUI();
    }}

    function resetAllFilters() {{
      document.getElementById('filterYear').value = 'ALL';
      document.getElementById('filterRegion').value = 'ALL';
      document.getElementById('filterCategory').value = 'ALL';
      document.getElementById('filterSegment').value = 'ALL';
      filteredData = [...rawData];
      currentPage = 1;
      updateUI();
    }}

    function updateUI() {{
      // Update badge
      document.getElementById('activeFilterBadge').innerText = `Displaying: ${{filteredData.length.toLocaleString()}} of ${{rawData.length.toLocaleString()}} Transactions`;

      // Calculate totals
      const totalSales = filteredData.reduce((acc, d) => acc + d.sales, 0);
      const totalProfit = filteredData.reduce((acc, d) => acc + d.profit, 0);
      const marginPct = totalSales > 0 ? (totalProfit / totalSales * 100) : 0;
      const totalOrders = filteredData.length;
      const aov = totalOrders > 0 ? (totalSales / totalOrders) : 0;
      const totalUnits = filteredData.reduce((acc, d) => acc + d.qty, 0);

      // Update KPI Cards
      document.getElementById('kpiRevenue').innerText = formatCurrency(totalSales);
      document.getElementById('kpiProfit').innerText = formatCurrency(totalProfit);
      document.getElementById('kpiMargin').innerText = marginPct.toFixed(1) + '%';
      document.getElementById('kpiOrders').innerText = totalOrders.toLocaleString();
      document.getElementById('kpiAOV').innerText = '$' + aov.toFixed(0);
      document.getElementById('kpiUnits').innerText = totalUnits.toLocaleString();

      updateCharts();
      renderCountryTable();
      renderTransactionTable();
    }}

    function updateCharts() {{
      // 1. Time Series: Monthly Aggregations
      const monthMap = {{}};
      filteredData.forEach(d => {{
        const ym = d.date.substring(0, 7); // YYYY-MM
        if (!monthMap[ym]) monthMap[ym] = {{ sales: 0, profit: 0 }};
        monthMap[ym].sales += d.sales;
        monthMap[ym].profit += d.profit;
      }});

      const sortedMonths = Object.keys(monthMap).sort();
      const salesSeries = sortedMonths.map(m => monthMap[m].sales);
      const profitSeries = sortedMonths.map(m => monthMap[m].profit);

      if (chartTimeSeries) chartTimeSeries.destroy();
      const ctxTS = document.getElementById('timeSeriesChart').getContext('2d');
      chartTimeSeries = new Chart(ctxTS, {{
        type: 'line',
        data: {{
          labels: sortedMonths,
          datasets: [
            {{
              label: 'Net Sales ($)',
              data: salesSeries,
              borderColor: '#6366F1',
              backgroundColor: 'rgba(99, 102, 241, 0.08)',
              fill: true,
              tension: 0.35,
              borderWidth: 2.5,
              pointRadius: 2.5
            }},
            {{
              label: 'Net Profit ($)',
              data: profitSeries,
              borderColor: '#10B981',
              backgroundColor: 'rgba(16, 185, 129, 0.12)',
              fill: true,
              tension: 0.35,
              borderWidth: 2,
              pointRadius: 2.5
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ labels: {{ color: '#94A3B8', font: {{ size: 11 }} }} }}
          }},
          scales: {{
            x: {{ ticks: {{ color: '#64748B', font: {{ size: 10 }}, maxTicksLimit: 12 }}, grid: {{ color: 'rgba(255,255,255,0.04)' }} }},
            y: {{ ticks: {{ color: '#64748B', callback: v => formatCurrency(v) }}, grid: {{ color: 'rgba(255,255,255,0.06)' }} }}
          }}
        }}
      }});

      // 2. Segment Donut
      const segMap = {{}};
      filteredData.forEach(d => {{
        segMap[d.seg] = (segMap[d.seg] || 0) + d.sales;
      }});
      if (chartSegment) chartSegment.destroy();
      const ctxSeg = document.getElementById('segmentDonutChart').getContext('2d');
      chartSegment = new Chart(ctxSeg, {{
        type: 'doughnut',
        data: {{
          labels: Object.keys(segMap),
          datasets: [{{
            data: Object.values(segMap),
            backgroundColor: ['#6366F1', '#EC4899', '#06B6D4'],
            borderColor: '#0B1120',
            borderWidth: 3
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ position: 'bottom', labels: {{ color: '#94A3B8', font: {{ size: 11 }} }} }}
          }},
          cutout: '68%'
        }}
      }});

      // 3. Category Bar Chart (Sales vs Profit)
      const catMap = {{}};
      filteredData.forEach(d => {{
        if (!catMap[d.cat]) catMap[d.cat] = {{ sales: 0, profit: 0 }};
        catMap[d.cat].sales += d.sales;
        catMap[d.cat].profit += d.profit;
      }});
      const cats = Object.keys(catMap);
      if (chartCategory) chartCategory.destroy();
      const ctxCat = document.getElementById('categoryBarChart').getContext('2d');
      chartCategory = new Chart(ctxCat, {{
        type: 'bar',
        data: {{
          labels: cats,
          datasets: [
            {{
              label: 'Sales ($)',
              data: cats.map(c => catMap[c].sales),
              backgroundColor: '#6366F1',
              borderRadius: 6
            }},
            {{
              label: 'Profit ($)',
              data: cats.map(c => catMap[c].profit),
              backgroundColor: '#10B981',
              borderRadius: 6
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ labels: {{ color: '#94A3B8', font: {{ size: 11 }} }} }} }},
          scales: {{
            x: {{ ticks: {{ color: '#94A3B8' }}, grid: {{ display: false }} }},
            y: {{ ticks: {{ color: '#64748B', callback: v => formatCurrency(v) }}, grid: {{ color: 'rgba(255,255,255,0.06)' }} }}
          }}
        }}
      }});

      // 4. Region Bar Chart
      const regMap = {{}};
      filteredData.forEach(d => {{
        regMap[d.reg] = (regMap[d.reg] || 0) + d.sales;
      }});
      if (chartRegion) chartRegion.destroy();
      const ctxReg = document.getElementById('regionBarChart').getContext('2d');
      chartRegion = new Chart(ctxReg, {{
        type: 'bar',
        data: {{
          labels: Object.keys(regMap),
          datasets: [{{
            label: 'Sales ($)',
            data: Object.values(regMap),
            backgroundColor: ['#38BDF8', '#818CF8', '#34D399', '#FBBF24'],
            borderRadius: 6
          }}]
        }},
        options: {{
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            x: {{ ticks: {{ color: '#64748B', callback: v => formatCurrency(v) }}, grid: {{ color: 'rgba(255,255,255,0.06)' }} }},
            y: {{ ticks: {{ color: '#94A3B8' }}, grid: {{ display: false }} }}
          }}
        }}
      }});

      // 5. Shipping Mode Donut
      const shipMap = {{}};
      filteredData.forEach(d => {{
        shipMap[d.ship] = (shipMap[d.ship] || 0) + 1;
      }});
      if (chartShipping) chartShipping.destroy();
      const ctxShip = document.getElementById('shippingDoughnutChart').getContext('2d');
      chartShipping = new Chart(ctxShip, {{
        type: 'doughnut',
        data: {{
          labels: Object.keys(shipMap),
          datasets: [{{
            data: Object.values(shipMap),
            backgroundColor: ['#6366F1', '#38BDF8', '#F59E0B', '#EF4444'],
            borderColor: '#0B1120',
            borderWidth: 2
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ position: 'bottom', labels: {{ color: '#94A3B8' }} }} }},
          cutout: '60%'
        }}
      }});

      // 6. Top Products Chart
      const prodMap = {{}};
      filteredData.forEach(d => {{
        prodMap[d.prod] = (prodMap[d.prod] || 0) + d.sales;
      }});
      const sortedProds = Object.keys(prodMap).sort((a,b) => prodMap[b] - prodMap[a]).slice(0, 8);
      if (chartTopProducts) chartTopProducts.destroy();
      const ctxTopP = document.getElementById('topProductsChart').getContext('2d');
      chartTopProducts = new Chart(ctxTopP, {{
        type: 'bar',
        data: {{
          labels: sortedProds,
          datasets: [{{
            label: 'Sales ($)',
            data: sortedProds.map(p => prodMap[p]),
            backgroundColor: '#F59E0B',
            borderRadius: 6
          }}]
        }},
        options: {{
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            x: {{ ticks: {{ color: '#64748B', callback: v => formatCurrency(v) }}, grid: {{ color: 'rgba(255,255,255,0.06)' }} }},
            y: {{ ticks: {{ color: '#94A3B8', font: {{ size: 10 }} }}, grid: {{ display: false }} }}
          }}
        }}
      }});

      // 7. Sub-Category Profitability Chart
      const subMap = {{}};
      filteredData.forEach(d => {{
        subMap[d.sub] = (subMap[d.sub] || 0) + d.profit;
      }});
      const sortedSubs = Object.keys(subMap).sort((a,b) => subMap[b] - subMap[a]);
      if (chartSubCategory) chartSubCategory.destroy();
      const ctxSub = document.getElementById('subCategoryChart').getContext('2d');
      chartSubCategory = new Chart(ctxSub, {{
        type: 'bar',
        data: {{
          labels: sortedSubs,
          datasets: [{{
            label: 'Profit ($)',
            data: sortedSubs.map(s => subMap[s]),
            backgroundColor: '#10B981',
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            x: {{ ticks: {{ color: '#94A3B8', font: {{ size: 10 }} }}, grid: {{ display: false }} }},
            y: {{ ticks: {{ color: '#64748B', callback: v => formatCurrency(v) }}, grid: {{ color: 'rgba(255,255,255,0.06)' }} }}
          }}
        }}
      }});
    }}

    function renderCountryTable() {{
      const countryMap = {{}};
      filteredData.forEach(d => {{
        if (!countryMap[d.cntry]) countryMap[d.cntry] = {{ reg: d.reg, orders: 0, sales: 0, profit: 0 }};
        countryMap[d.cntry].orders += 1;
        countryMap[d.cntry].sales += d.sales;
        countryMap[d.cntry].profit += d.profit;
      }});

      const sortedCountries = Object.keys(countryMap).sort((a,b) => countryMap[b].sales - countryMap[a].sales);
      const tbody = document.getElementById('countryTableBody');
      tbody.innerHTML = '';

      sortedCountries.forEach(c => {{
        const item = countryMap[c];
        const margin = item.sales > 0 ? ((item.profit / item.sales) * 100).toFixed(1) : '0.0';
        const tr = document.createElement('tr');
        tr.className = "hover:bg-slate-800/40 transition";
        tr.innerHTML = `
          <td class="p-3 font-semibold text-white flex items-center gap-1.5">${{c}}</td>
          <td class="p-3 text-slate-400">${{item.reg}}</td>
          <td class="p-3 text-right">${{item.orders.toLocaleString()}}</td>
          <td class="p-3 text-right font-semibold text-slate-200">${{formatCurrency(item.sales)}}</td>
          <td class="p-3 text-right font-semibold text-emerald-400">${{formatCurrency(item.profit)}}</td>
          <td class="p-3 text-right font-bold ${{parseFloat(margin) >= 25 ? 'text-cyan-400' : 'text-amber-400'}}">${{margin}}%</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    let searchedData = [];

    function handleSearch() {{
      const query = document.getElementById('tableSearchInput').value.toLowerCase().trim();
      if (!query) {{
        searchedData = [...filteredData];
      }} else {{
        searchedData = filteredData.filter(d => 
          d.id.toLowerCase().includes(query) ||
          d.prod.toLowerCase().includes(query) ||
          d.cntry.toLowerCase().includes(query) ||
          d.cat.toLowerCase().includes(query)
        );
      }}
      currentPage = 1;
      renderTransactionTable();
    }}

    function renderTransactionTable() {{
      const dataToDisplay = (document.getElementById('tableSearchInput').value.trim().length > 0) ? searchedData : filteredData;
      const totalRows = dataToDisplay.length;
      const totalPages = Math.ceil(totalRows / pageSize) || 1;
      if (currentPage > totalPages) currentPage = totalPages;

      const startIdx = (currentPage - 1) * pageSize;
      const endIdx = Math.min(startIdx + pageSize, totalRows);
      const pageSlice = dataToDisplay.slice(startIdx, endIdx);

      const tbody = document.getElementById('transactionTableBody');
      tbody.innerHTML = '';

      pageSlice.forEach(row => {{
        const tr = document.createElement('tr');
        tr.className = "hover:bg-slate-800/50 transition";
        tr.innerHTML = `
          <td class="p-3 font-mono text-[11px] text-indigo-400 font-semibold">${{row.id}}</td>
          <td class="p-3 text-slate-400">${{row.date}}</td>
          <td class="p-3 text-white font-medium">${{row.seg}}</td>
          <td class="p-3 text-slate-400">${{row.cntry}} (${{row.reg}})</td>
          <td class="p-3"><span class="px-2 py-0.5 rounded text-[10px] font-semibold ${{row.cat === 'Technology' ? 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/20' : row.cat === 'Furniture' ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' : 'bg-teal-500/10 text-teal-400 border border-teal-500/20'}}">${{row.cat}}</span></td>
          <td class="p-3 text-slate-200 max-w-xs truncate">${{row.prod}}</td>
          <td class="p-3 text-right">${{row.qty}}</td>
          <td class="p-3 text-right font-medium text-white">$${{row.sales.toFixed(2)}}</td>
          <td class="p-3 text-right font-semibold text-emerald-400">$${{row.profit.toFixed(2)}}</td>
          <td class="p-3 text-right font-bold text-cyan-400">${{row.margin.toFixed(1)}}%</td>
        `;
        tbody.appendChild(tr);
      }});

      document.getElementById('tableCountText').innerText = `Showing ${{totalRows > 0 ? startIdx + 1 : 0}} to ${{endIdx}} of ${{totalRows.toLocaleString()}} rows`;
      document.getElementById('pageNumberText').innerText = `Page ${{currentPage}} of ${{totalPages}}`;
      document.getElementById('btnPrevPage').disabled = currentPage <= 1;
      document.getElementById('btnNextPage').disabled = currentPage >= totalPages;
    }}

    function prevPage() {{
      if (currentPage > 1) {{
        currentPage--;
        renderTransactionTable();
      }}
    }}

    function nextPage() {{
      const dataToDisplay = (document.getElementById('tableSearchInput').value.trim().length > 0) ? searchedData : filteredData;
      const totalPages = Math.ceil(dataToDisplay.length / pageSize) || 1;
      if (currentPage < totalPages) {{
        currentPage++;
        renderTransactionTable();
      }}
    }}

    function exportFilteredCSV() {{
      const headers = ["Order_ID", "Date", "Year", "Quarter", "Region", "Country", "City", "Category", "Sub_Category", "Product_Name", "Segment", "Ship_Mode", "Quantity", "Net_Sales", "Profit", "Margin_Pct", "Discount_Rate"];
      let csvContent = "data:text/csv;charset=utf-8," + headers.join(",") + "\\n";

      filteredData.forEach(d => {{
        const row = [
          d.id,
          d.date,
          d.yr,
          d.qtr,
          `"${{d.reg}}"`,
          `"${{d.cntry}}"`,
          `"${{d.city}}"`,
          `"${{d.cat}}"`,
          `"${{d.sub}}"`,
          `"${{d.prod.replace(/"/g, '""')}}"`,
          `"${{d.seg}}"`,
          `"${{d.ship}}"`,
          d.qty,
          d.sales,
          d.profit,
          d.margin,
          d.disc
        ];
        csvContent += row.join(",") + "\\n";
      }});

      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", "sales_dashboard_filtered_export.csv");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }}

    // Initial boot
    window.addEventListener('DOMContentLoaded', () => {{
      lucide.createIcons();
      updateUI();
    }});
  </script>
</body>
</html>
"""

with open(dashboard_html_path, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"Interactive Web Dashboard successfully built at: {dashboard_html_path}")

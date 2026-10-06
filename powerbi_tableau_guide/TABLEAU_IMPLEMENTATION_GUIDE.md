# 🎨 Tableau Implementation & Visual Calculations Guide
**Elevate Labs Data Analyst Internship — Task 4: Dashboard Design**

---

## 🚀 1. Overview & Connection
This guide details how to build the executive sales dashboard in **Tableau Desktop / Tableau Public**.

### Step 1: Connect to Data Source
1. Open **Tableau Desktop** or **Tableau Public**.
2. Under **Connect** > **To a File**, select **Text file**.
3. Choose `sales_financial_data.csv` in the `dataset/` directory.
4. Verify standard fields:
   - Dimensions: `Category`, `Sub_Category`, `Country`, `Region`, `Segment`, `Ship_Mode`
   - Measures: `Net_Sales`, `Profit`, `Quantity`, `Discount_Rate`
   - Dates: `Order_Date`, `Ship_Date`

---

## 🧮 2. Calculated Fields & Level of Detail (LOD) Expressions

### 1. Overall Profit Ratio
```tableau
// Profit Ratio
SUM([Profit]) / SUM([Net Sales])
```
*Format: Number (Custom) > Percentage with 1 decimal place.*

### 2. Average Order Value (AOV)
```tableau
// Average Order Value
SUM([Net Sales]) / COUNTD([Order ID])
```
*Format: Currency (Standard).*

### 3. Regional Fixed LOD (Market Share Contribution)
```tableau
// Total Sales for Region (Unaffected by Category filters)
{ FIXED [Region] : SUM([Net Sales]) }
```

### 4. Global Baseline Sales LOD
```tableau
// Entire Enterprise Sales Baseline
{ FIXED : SUM([Net Sales]) }
```

### 5. Regional Sales % of Global Total
```tableau
// Regional Contribution %
SUM([Net Sales]) / ATTR({ FIXED : SUM([Net Sales]) })
```

### 6. Dynamic Metric Switcher (Parameter-driven)
Create a parameter `[Select Metric]` with String values: `'Sales'`, `'Profit'`, `'Orders'`.
Then create a calculated measure:
```tableau
CASE [Select Metric]
  WHEN 'Sales' THEN SUM([Net Sales])
  WHEN 'Profit' THEN SUM([Profit])
  WHEN 'Orders' THEN COUNTD([Order ID])
END
```

---

## 📊 3. Worksheet Construction

### Sheet 1: Executive KPI Cards
- Drag `Measure Values` onto Text.
- Keep only: `SUM([Net Sales])`, `SUM([Profit])`, `[Profit Ratio]`, `COUNTD([Order ID])`, `[AOV]`.
- Set Marks to **Text**, align center, apply corporate colors.

### Sheet 2: Time-Series Trend Line (Sales & Profit)
- Columns: `YEAR(Order Date)` > `MONTH(Order Date)` (Continuous)
- Rows: `SUM([Net Sales])`, `SUM([Profit])` (Dual Axis, Synchronized Axis)
- Marks: Net Sales as Area or Line (Color `#6366F1`), Profit as Line (Color `#10B981`).

### Sheet 3: Segment Revenue Donut Chart
- Columns: `AVG(0)`, Rows: `AVG(0)` (Dual Axis for hole)
- Marks Card 1: Pie chart with Color = `[Segment]`, Angle = `SUM([Net Sales])`.
- Marks Card 2: Circle chart with Color = Dark Slate `#0F172A` (creates donut hole).

### Sheet 4: Regional Performance Matrix
- Rows: `[Region]`
- Columns: `SUM([Net Sales])`
- Detail: `SUM([Profit])`, Tooltip: `[Profit Ratio]`

### Sheet 5: Sub-Category Profitability Bar Chart
- Rows: `[Sub_Category]` (Sorted descending by Profit)
- Columns: `SUM([Profit])`
- Color: `[Category]`

---

## 🖱️ 4. Interactive Dashboard Assembly
1. Create a New Dashboard (`1400 x 900` px).
2. Set background color to `#0F172A` (Executive Slate).
3. Drag **Horizontal Containers** for:
   - Header banner (Title + Quick filter controls)
   - KPI Banner
   - Trend & Segment charts
   - Regional & Category charts
4. Add **Dashboard Actions**:
   - Go to **Dashboard** > **Actions** > **Add Action** > **Filter**.
   - Source Sheets: `Regional Performance`, `Segment Donut`.
   - Target Sheets: All sheets.
   - Run action on: **Select**.
   - Clearing the selection will: **Show all values**.
5. Add **Story Points**:
   - Create a Tableau Story to walk executives through:
     - Story 1: Global Macro Performance
     - Story 2: Regional Margin Variances
     - Story 3: Product Portfolio Health

# 📊 Power BI Implementation & DAX Architecture Guide
**Elevate Labs Data Analyst Internship — Task 4: Dashboard Design**

---

## 🎯 1. Overview & Data Ingestion
This guide provides the exact steps to recreate the interactive executive dashboard in **Microsoft Power BI Desktop**.

### Step 1: Ingest Data
1. Launch **Power BI Desktop**.
2. Click **Get Data** > **Text/CSV**.
3. Select `sales_financial_data.csv` located in the `dataset/` directory.
4. In the Power Query preview window, click **Transform Data**.
5. Verify column data types:
   - `Order_Date`, `Ship_Date`: **Date**
   - `Net_Sales`, `Profit`, `Gross_Sales`, `Unit_Cost`, `Unit_Price`: **Fixed Decimal Number ($)**
   - `Discount_Rate`, `Profit_Margin_Pct`: **Percentage / Decimal Number**
   - `Quantity`, `Year`, `Month_Num`: **Whole Number**
   - `Region`, `Country`, `Category`, `Sub_Category`, `Segment`: **Text**
6. Click **Close & Apply**.

---

## 🏗️ 2. Data Modeling (Star Schema)
For best enterprise practice, organize the model into a Star Schema:
- **Fact Table:** `Fact_Sales` (`Order_ID`, `Order_Date`, `Customer_ID`, `Product_ID`, `Net_Sales`, `Profit`, `Quantity`, etc.)
- **Dimension Tables:**
  - `Dim_Calendar` (Generated via DAX `CALENDARAUTO()`)
  - `Dim_Product` (`Product_ID`, `Category`, `Sub_Category`, `Product_Name`)
  - `Dim_Geography` (`City`, `State`, `Country`, `Region`)
  - `Dim_Customer` (`Customer_ID`, `Customer_Name`, `Segment`)

### Calendar Table DAX Formula:
```dax
Dim_Calendar = 
VAR MinYear = YEAR(MIN(Fact_Sales[Order_Date]))
VAR MaxYear = YEAR(MAX(Fact_Sales[Order_Date]))
RETURN
ADDCOLUMNS(
    CALENDAR(DATE(MinYear, 1, 1), DATE(MaxYear, 12, 31)),
    "Year", YEAR([Date]),
    "Quarter", "Q" & FORMAT([Date], "Q"),
    "Month", FORMAT([Date], "mmmm"),
    "Month Number", MONTH([Date]),
    "Year-Month", FORMAT([Date], "yyyy-mm")
)
```

---

## 📐 3. Production DAX Measures
Create a dedicated measures table called `_KeyMeasures`.

### 1. Total Net Sales
```dax
Total Sales = SUM(Fact_Sales[Net_Sales])
```

### 2. Total Net Profit
```dax
Total Profit = SUM(Fact_Sales[Profit])
```

### 3. Total Cost
```dax
Total Cost = SUM(Fact_Sales[Total_Cost])
```

### 4. Profit Margin %
```dax
Profit Margin % = 
DIVIDE(
    [Total Profit], 
    [Total Sales], 
    0
)
```

### 5. Total Order Volume
```dax
Total Orders = DISTINCTCOUNT(Fact_Sales[Order_ID])
```

### 6. Average Order Value (AOV)
```dax
Average Order Value = 
DIVIDE(
    [Total Sales], 
    [Total Orders], 
    0
)
```

### 7. Prior Year Sales (SPLY)
```dax
Sales SPLY = 
CALCULATE(
    [Total Sales], 
    SAMEPERIODLASTYEAR(Dim_Calendar[Date])
)
```

### 8. Year-over-Year (YoY) Sales Growth %
```dax
YoY Sales Growth % = 
VAR SPLY = [Sales SPLY]
RETURN
IF(
    ISBLANK(SPLY), 
    BLANK(), 
    DIVIDE([Total Sales] - SPLY, SPLY, 0)
)
```

### 9. Dynamic KPI Status Color Indicator
```dax
Margin Status Color = 
IF([Profit Margin %] >= 0.25, "#10B981", IF([Profit Margin %] >= 0.20, "#F59E0B", "#EF4444"))
```

---

## 🎨 4. Canvas Layout & Visual Elements

### Visual Canvas Setup
- **Page Size:** 16:9 widescreen (1280 x 720 or 1920 x 1080)
- **Canvas Background:** Hex `#0F172A` (Deep Slate Navy) with 0% transparency

### Top Section: Slicers & Navigation
1. **Year Slicer:** Dropdown or Tile slicer using `Dim_Calendar[Year]`.
2. **Region Slicer:** Dropdown slicer using `Dim_Geography[Region]`.
3. **Category Slicer:** Dropdown slicer using `Dim_Product[Category]`.
4. **Segment Slicer:** Dropdown slicer using `Dim_Customer[Segment]`.
5. **Sync Slicers:** Open **View** > **Sync Slicers** and enable sync across all tabs.

### Row 1: KPI Cards (Multi-Row Card or New Card Visual)
- Card 1: `[Total Sales]` (Formatted as Currency `$`)
- Card 2: `[Total Profit]` (Formatted as Currency `$`)
- Card 3: `[Profit Margin %]` (Formatted as Percentage `0.0%`)
- Card 4: `[Total Orders]` (Formatted as Whole Number `#,##0`)
- Card 5: `[Average Order Value]` (Formatted as Currency `$`)

### Row 2: Time Series & Segment Charts
- **Left (60% width): Line & Stacked Column Combo Chart**
  - Shared Axis: `Dim_Calendar[Year-Month]`
  - Column Values: `[Total Sales]`
  - Line Values: `[Total Profit]`
- **Right (40% width): Donut Chart**
  - Legend: `Fact_Sales[Segment]`
  - Values: `[Total Sales]`

### Row 3: Regional & Product Performance
- **Left (50% width): Clustered Bar Chart**
  - Y-Axis: `Dim_Geography[Region]`
  - X-Axis: `[Total Sales]`, `[Total Profit]`
- **Right (50% width): Clustered Bar Chart**
  - Y-Axis: `Dim_Product[Sub_Category]`
  - X-Axis: `[Total Profit]`
  - Data Color: Formatted by Category

---

## 🧭 5. Interactive Navigation & Drill-Through
1. **Navigation Buttons:** Insert **Buttons** > **Page Navigator** styled with rounded corners and glowing hover states.
2. **Drill-Through Page:**
   - Create a page named `Product Drilldown`.
   - Drag `Fact_Sales[Sub_Category]` into the **Drill-through** field bucket.
   - Right-click any category bar in the main view to drill down to SKU level details.

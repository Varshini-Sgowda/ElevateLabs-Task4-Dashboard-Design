import os
import random
import datetime
import numpy as np
import pandas as pd

# Set fixed seed for reproducibility
random.seed(42)
np.random.seed(42)

project_dir = r"C:\Users\Varshini S\.gemini\antigravity\scratch\ElevateLabs_Task4_Dashboard_Design"
dataset_dir = os.path.join(project_dir, "dataset")
os.makedirs(dataset_dir, exist_ok=True)

# Define reference data
regions_data = {
    "North America": {
        "countries": ["United States", "Canada"],
        "cities": [
            ("New York", "New York", "United States"),
            ("Los Angeles", "California", "United States"),
            ("Chicago", "Illinois", "United States"),
            ("Houston", "Texas", "United States"),
            ("Toronto", "Ontario", "Canada"),
            ("Vancouver", "British Columbia", "Canada")
        ]
    },
    "Europe": {
        "countries": ["United Kingdom", "Germany", "France"],
        "cities": [
            ("London", "England", "United Kingdom"),
            ("Manchester", "England", "United Kingdom"),
            ("Berlin", "Berlin", "Germany"),
            ("Munich", "Bavaria", "Germany"),
            ("Paris", "Île-de-France", "France"),
            ("Lyon", "Auvergne-Rhône-Alpes", "France")
        ]
    },
    "Asia Pacific": {
        "countries": ["Japan", "Australia", "India", "Singapore"],
        "cities": [
            ("Tokyo", "Kanto", "Japan"),
            ("Sydney", "New South Wales", "Australia"),
            ("Melbourne", "Victoria", "Australia"),
            ("Mumbai", "Maharashtra", "India"),
            ("Bangalore", "Karnataka", "India"),
            ("Singapore", "Central", "Singapore")
        ]
    },
    "Latin America": {
        "countries": ["Brazil", "Mexico"],
        "cities": [
            ("São Paulo", "São Paulo", "Brazil"),
            ("Rio de Janeiro", "Rio de Janeiro", "Brazil"),
            ("Mexico City", "Federal District", "Mexico"),
            ("Guadalajara", "Jalisco", "Mexico")
        ]
    }
}

categories_catalog = {
    "Technology": {
        "Phones": [("iPhone 15 Pro", 850, 1099), ("Samsung Galaxy S24", 720, 950), ("Google Pixel 8", 540, 699), ("OnePlus 12", 480, 649)],
        "Laptops": [("MacBook Air M3", 890, 1199), ("Dell XPS 15", 1100, 1450), ("ThinkPad X1 Carbon", 1050, 1399), ("HP Spectre x360", 920, 1250)],
        "Accessories": [("Logitech MX Master 3S", 55, 99), ("Bose QuietComfort Headphones", 180, 279), ("Dell 4K UltraSharp Monitor", 340, 489), ("Anker USB-C Docking Hub", 45, 79)]
    },
    "Furniture": {
        "Chairs": [("Herman Miller Aeron Chair", 750, 1195), ("Ergonomic Mesh Task Chair", 160, 289), ("Steelcase Gesture Chair", 820, 1250), ("Executive Leather Recliner", 260, 420)],
        "Tables": [("Smart Motorized Standing Desk", 320, 560), ("Solid Oak Conference Table", 980, 1480), ("Modular Team Workstation", 640, 990), ("Coffee Break Lounge Table", 120, 210)],
        "Bookcases": [("Modern 5-Tier Industrial Bookshelf", 110, 195), ("Solid Wood Library Cabinet", 450, 720), ("Glass Display Credenza", 310, 520)]
    },
    "Office Supplies": {
        "Storage": [("Heavy Duty 4-Drawer File Cabinet", 130, 220), ("Rolling Mobile Utility Cart", 45, 85), ("Locking Security Storage Box", 65, 115)],
        "Paper": [("Premium Multipurpose Laser Paper 5000ct", 28, 48), ("Heavyweight Cardstock Reams", 16, 32), ("Executive Recycled Notepad Pack", 12, 24)],
        "Appliances": [("Commercial Espresso Barista Machine", 620, 950), ("Smart Office Air Purifier Pro", 140, 249), ("Heavy Duty Cross-Cut Shredder", 90, 165)]
    }
}

customer_names = [
    "Emma Watson", "Liam Johnson", "Olivia Smith", "Noah Williams", "Sophia Brown",
    "James Jones", "Isabella Garcia", "Lucas Miller", "Mia Davis", "Benjamin Rodriguez",
    "Charlotte Martinez", "Elijah Hernandez", "Amelia Lopez", "Alexander Gonzalez", "Harper Wilson",
    "Daniel Anderson", "Evelyn Thomas", "Matthew Taylor", "Abigail Moore", "Henry Jackson",
    "Emily Martin", "Sebastian Lee", "Elizabeth Perez", "Jack Thompson", "Avery White",
    "David Harris", "Ella Sanchez", "Samuel Clark", "Chloe Ramirez", "Joseph Lewis"
]

segments = ["Consumer", "Corporate", "Home Office"]
segment_weights = [0.50, 0.32, 0.18]

ship_modes = ["Standard Class", "Second Class", "First Class", "Same Day"]
ship_mode_weights = [0.58, 0.22, 0.14, 0.06]

payment_methods = ["Credit Card", "Wire Transfer", "PayPal", "Direct Debit"]
payment_weights = [0.45, 0.25, 0.20, 0.10]

# Generate rows spanning 2024-01-01 to 2026-06-30 (2.5 years)
start_date = datetime.date(2024, 1, 1)
end_date = datetime.date(2026, 6, 30)
days_range = (end_date - start_date).days

num_records = 3500
records = []

for i in range(1, num_records + 1):
    order_id = f"ORD-{2024 + (i % 3)}-{10000 + i}"
    
    # Weighted date distribution (higher sales in Q4 each year)
    day_offset = random.randint(0, days_range)
    order_date = start_date + datetime.timedelta(days=day_offset)
    
    # If in Nov/Dec, 40% chance to boost volume
    if order_date.month in [11, 12] and random.random() < 0.35:
        # Holiday seasonality
        pass
        
    ship_delay = random.choices([1, 2, 3, 4, 5, 6], weights=[0.1, 0.3, 0.35, 0.15, 0.07, 0.03])[0]
    ship_date = order_date + datetime.timedelta(days=ship_delay)
    
    ship_mode = random.choices(ship_modes, weights=ship_mode_weights)[0]
    
    cust_idx = random.randint(0, len(customer_names) - 1)
    customer_name = customer_names[cust_idx]
    customer_id = f"CUST-{1000 + cust_idx}"
    
    segment = random.choices(segments, weights=segment_weights)[0]
    
    region = random.choices(list(regions_data.keys()), weights=[0.42, 0.28, 0.20, 0.10])[0]
    city_info = random.choice(regions_data[region]["cities"])
    city, state, country = city_info
    
    category = random.choices(list(categories_catalog.keys()), weights=[0.40, 0.35, 0.25])[0]
    sub_category = random.choice(list(categories_catalog[category].keys()))
    product_item = random.choice(categories_catalog[category][sub_category])
    prod_name, unit_cost, unit_price = product_item
    
    product_id = f"PROD-{category[:3].upper()}-{100 + random.randint(1, 99)}"
    
    # Quantity
    quantity = random.choices([1, 2, 3, 4, 5, 6, 8, 10], weights=[0.30, 0.25, 0.18, 0.12, 0.08, 0.04, 0.02, 0.01])[0]
    
    # Discount rate (higher discount for Corporate or volume)
    if quantity >= 5:
        discount_rate = random.choices([0.10, 0.15, 0.20], weights=[0.5, 0.3, 0.2])[0]
    elif segment == "Corporate":
        discount_rate = random.choices([0.0, 0.05, 0.10, 0.15], weights=[0.4, 0.3, 0.2, 0.1])[0]
    else:
        discount_rate = random.choices([0.0, 0.05, 0.10], weights=[0.6, 0.25, 0.15])[0]
        
    gross_sales = round(quantity * unit_price, 2)
    discount_amount = round(gross_sales * discount_rate, 2)
    net_sales = round(gross_sales - discount_amount, 2)
    
    total_cost = round(quantity * unit_cost, 2)
    profit = round(net_sales - total_cost, 2)
    profit_margin = round((profit / net_sales) * 100, 2) if net_sales > 0 else 0.0
    
    payment = random.choices(payment_methods, weights=payment_weights)[0]
    rating = random.choices([5, 4, 3, 2, 1], weights=[0.55, 0.28, 0.10, 0.04, 0.03])[0]
    
    records.append({
        "Order_ID": order_id,
        "Order_Date": order_date.strftime("%Y-%m-%d"),
        "Ship_Date": ship_date.strftime("%Y-%m-%d"),
        "Year": order_date.year,
        "Quarter": f"Q{(order_date.month - 1) // 3 + 1}",
        "Month": order_date.strftime("%B"),
        "Month_Num": order_date.month,
        "Ship_Mode": ship_mode,
        "Customer_ID": customer_id,
        "Customer_Name": customer_name,
        "Segment": segment,
        "Country": country,
        "Region": region,
        "State": state,
        "City": city,
        "Product_ID": product_id,
        "Category": category,
        "Sub_Category": sub_category,
        "Product_Name": prod_name,
        "Quantity": quantity,
        "Unit_Cost": unit_cost,
        "Unit_Price": unit_price,
        "Gross_Sales": gross_sales,
        "Discount_Rate": discount_rate,
        "Discount_Amount": discount_amount,
        "Net_Sales": net_sales,
        "Total_Cost": total_cost,
        "Profit": profit,
        "Profit_Margin_Pct": profit_margin,
        "Payment_Method": payment,
        "Customer_Rating": rating
    })

df = pd.DataFrame(records)
# Sort by order date
df["Order_Date_dt"] = pd.to_datetime(df["Order_Date"])
df = df.sort_values("Order_Date_dt").reset_index(drop=True)
df = df.drop(columns=["Order_Date_dt"])

csv_path = os.path.join(dataset_dir, "sales_financial_data.csv")
xlsx_path = os.path.join(dataset_dir, "sales_financial_data.xlsx")

df.to_csv(csv_path, index=False)
df.to_excel(xlsx_path, index=False)

print(f"Dataset generated successfully!")
print(f"Total Rows: {len(df)}")
print(f"Total Sales: ${df['Net_Sales'].sum():,.2f}")
print(f"Total Profit: ${df['Profit'].sum():,.2f}")
print(f"Overall Profit Margin: {(df['Profit'].sum() / df['Net_Sales'].sum())*100:.2f}%")
print(f"Files saved at:")
print(f" - CSV: {csv_path}")
print(f" - Excel: {xlsx_path}")

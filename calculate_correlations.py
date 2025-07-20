import sqlite3
import math

# Connect to database and create table with data
conn = sqlite3.connect('retail_analysis.db')
cursor = conn.cursor()

# Drop table if exists and recreate
cursor.execute("DROP TABLE IF EXISTS retail_data")

# Read and execute the data creation part
with open('q-sql-correlation-github-pages.sql', 'r') as f:
    sql_content = f.read()
    cursor.executescript(sql_content)

# Fetch all data
cursor.execute("SELECT Promo_Spend, Avg_Basket, Net_Sales FROM retail_data")
data = cursor.fetchall()

# Convert to lists
promo_spend = [row[0] for row in data]
avg_basket = [row[1] for row in data]
net_sales = [row[2] for row in data]

def calculate_correlation(x, y):
    n = len(x)
    if n == 0:
        return 0
    
    # Calculate means
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    # Calculate correlation coefficient
    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    sum_sq_x = sum((x[i] - mean_x) ** 2 for i in range(n))
    sum_sq_y = sum((y[i] - mean_y) ** 2 for i in range(n))
    
    if sum_sq_x == 0 or sum_sq_y == 0:
        return 0
    
    denominator = math.sqrt(sum_sq_x * sum_sq_y)
    return numerator / denominator

# Calculate correlations
corr_promo_basket = calculate_correlation(promo_spend, avg_basket)
corr_promo_sales = calculate_correlation(promo_spend, net_sales)
corr_basket_sales = calculate_correlation(avg_basket, net_sales)

# Print results
print("Correlation Results:")
print(f"Promo_Spend - Avg_Basket: {corr_promo_basket:.6f} (abs: {abs(corr_promo_basket):.6f})")
print(f"Promo_Spend - Net_Sales: {corr_promo_sales:.6f} (abs: {abs(corr_promo_sales):.6f})")
print(f"Avg_Basket - Net_Sales: {corr_basket_sales:.6f} (abs: {abs(corr_basket_sales):.6f})")

# Find strongest correlation
correlations = [
    ("Promo_Spend - Avg_Basket", corr_promo_basket),
    ("Promo_Spend - Net_Sales", corr_promo_sales),
    ("Avg_Basket - Net_Sales", corr_basket_sales)
]

strongest = max(correlations, key=lambda x: abs(x[1]))
print(f"\nStrongest correlation: {strongest[0]} with coefficient {strongest[1]:.6f}")

# Create JSON result
import json
result = {
    "pair": strongest[0],
    "correlation": round(strongest[1], 6)
}

with open('correlation_result.json', 'w') as f:
    json.dump(result, f, indent=2)

print(f"\nJSON result saved to correlation_result.json:")
print(json.dumps(result, indent=2))

conn.close()
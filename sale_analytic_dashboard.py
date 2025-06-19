import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Created and Loaded SQL Table
# Using SQLite to create a sales database and insert data:

# Load CSV (with correct encoding)
df = pd.read_csv("sales_data_sample.csv", encoding='latin1')

# Connect to SQLite
conn = sqlite3.connect("sales.db")
df.to_sql("sales_data", conn, if_exists="replace", index=False)


# Query SQL and Analyze with Pandas
# Query SQL data
query = "SELECT * FROM sales_data"
sales_df = pd.read_sql_query(query, conn)

# Total Revenue
sales_df["Revenue"] = sales_df["QUANTITYORDERED"] * sales_df["PRICEEACH"]
print("Total Revenue:", sales_df["Revenue"].sum())

# Convert ORDERDATE to datetime
sales_df["ORDERDATE"] = pd.to_datetime(sales_df["ORDERDATE"], errors='coerce')

# Monthly sales
monthly_sales = sales_df.groupby(sales_df["ORDERDATE"].dt.to_period("M"))["Revenue"].sum()
print("Monthly Revenue:")
print(monthly_sales)

# Top Products by Revenue
top_products = sales_df.groupby("PRODUCTCODE")["Revenue"].sum().sort_values(ascending=False).head(5)
print("Top Products:")
print(top_products)


# Visualization (Monthly Revenue)
monthly_sales.plot(kind="bar", title="Monthly Revenue", color='teal')
plt.ylabel("Revenue")
plt.xlabel("Month")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



# Streamlit Dashboard
st.title("📊 Sales Dashboard")
st.subheader("Total Revenue")
st.metric(label="Total Revenue", value=f"${sales_df['Revenue'].sum():,.2f}")

st.subheader("Monthly Revenue Chart")
st.bar_chart(monthly_sales)

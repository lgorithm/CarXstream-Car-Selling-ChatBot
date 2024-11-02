import pandas as pd
from langchain_core.tools import tool, StructuredTool
from fuzzywuzzy import fuzz, process
from pydantic import BaseModel, Field
import re
from io import BytesIO
import traceback
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

output_dir = "graphs"
os.makedirs(output_dir, exist_ok=True)
# CSV file paths
csv_path = "D:/AI_Projects/CarXstream-Car-Selling-ChatBot/Hyderabad_scraped_car_data.csv"  
sells = pd.read_csv(csv_path)
Graph_BytesIO = None
# Parse & Convert the price input to a numeric format
def parse_price(price_input: str) -> int:
    """
    Parses a price input string into a numeric format.
    """
    price = float(price_input.replace('₹', '').replace('L', '').replace(' Crore', '').strip())
    if 'L' in price_input:
        price *= 100000
    elif 'Crore' in price_input:
        price *= 10000000
    return int(price)

def fuzzy_match(df, company, model, variant, threshold=80):
    """
    Performs fuzzy matching to find the closest match in a DataFrame column.
    """
    choices = list(set(df['Make'].dropna().str.lower().tolist()))
    match, score = process.extractOne(company, choices, scorer=fuzz.token_sort_ratio)
    if score < threshold:
        return pd.DataFrame()
    df = df[df['Make'].str.lower() == match]
    
    choices = list(set(df['Model'].dropna().str.lower().tolist()))
    match, score = process.extractOne(model, choices, scorer=fuzz.token_sort_ratio)
    if score < threshold:
        return pd.DataFrame()
    df = df[df['Model'].str.lower() == match]

    choices = list(set(df['Variant'].dropna().str.lower().tolist()))
    match, score = process.extractOne(variant, choices, scorer=fuzz.token_sort_ratio)
    if score < threshold:
        return pd.DataFrame()
    return df[df['Variant'].str.lower() == match]
            
def clean_price(price_str):
    price_str = price_str.replace('₹', '').replace('L', '').strip()
    return float(price_str)*100000

def clean_Kilometers(Kilometers_str):
    Kilometers_str = Kilometers_str.replace('km', '').replace(',', '').strip()
    return float(Kilometers_str)

class recommend_input(BaseModel):
    """Car Price Recommendation."""
    company: str = Field(..., description="Company Name")
    model: str = Field(..., description="Car Model")
    variant: str = Field(..., description="Car Variant")
    price: int = Field(..., description="Car Price")
    odometer_reading: int = Field(..., description="Kilometer Driven By The Car")
    vehicle_number: str = Field(..., description="vehicle number")
def recommend_tool(company: str, model: str, variant: str, price: int, odometer_reading: int, vehicle_number: str) -> any:
    """
    Recommend Tool
    
    It will take this input: company, model, variant, price and odometer_reading from the agent model and recommend the price through graph.
    
    """
    try:
        # Parse and validate input data
        company = company.strip().lower()
        model = model.strip().lower()
        variant = variant.strip().lower()
        # Fuzzy match to get selling price range
        filtered_data = fuzzy_match(sells, company, model, variant)


        if filtered_data.empty:
            return False
        else:
            # Apply the function to the 'price' column
            filtered_data['Price'] = filtered_data['Price'].apply(clean_price)
            filtered_data['Kilometers Driven'] = filtered_data['Kilometers Driven'].apply(clean_Kilometers)
            closest_kilometers_idx = (filtered_data['Kilometers Driven'] - odometer_reading).abs().argmin()
            closest_kilometer_driven = filtered_data['Kilometers Driven'].iloc[closest_kilometers_idx]
            sns.set(style="whitegrid")
            plt.figure(figsize=(8, 4))
            sns.lineplot(filtered_data, x="Kilometers Driven", y="Price", marker='o', color='b', label="Car Prices")
            plt.bar(closest_kilometer_driven, price, color='orange', width=3000, label="Your Car Price")
            plt.xlabel('Kilometers Driven')
            plt.ylabel('Price (INR)')
            plt.title('Kilometers Driven vs Price Comparison with Your Car Highlighted')
            plt.legend(loc='upper right')
            plt.tight_layout()
      
            filepath = os.path.join(output_dir, vehicle_number + '.png')
            plt.savefig(filepath)
            plt.close() 
            return filepath
            
    except Exception as e:
        print(traceback.format_exc())
        return f"Calling tool with arguments:\nraised the following error:\n\n{type(e)}: {e}"   
    
recommend = StructuredTool.from_function(
        func=recommend_tool,
        name="recommend_tool",
        description="It will take this input: company, model, variant, price, odometer_reading and vehicle number from the agent model and recommend the price through graph",
        args_schema=recommend_input,
    )
# print(parse_price('₹10.13L'))
# print(recommend_tool('Hyundai', 'Xcent'))
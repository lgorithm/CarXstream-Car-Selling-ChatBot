import pandas as pd
from langchain_core.tools import tool, StructuredTool
from fuzzywuzzy import fuzz, process
from pydantic import BaseModel, Field
import re

# CSV file paths
csv_path = "D:/AI_Projects/CarXstream-Car-Selling-ChatBot/Hyderabad_scraped_car_data.csv"  
sells = pd.read_csv(csv_path)

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

def fuzzy_match(df, company, model, threshold=80):
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
    return df[df['Model'].str.lower() == match]
            
class recommend_input(BaseModel):
    """Car Price Recommendation."""
    company: str = Field(..., description="Company Name")
    model: str = Field(..., description="Car Model")

def recommend_tool(company: str, model: str) -> any:
    """
    Recommend Tool
    
    It will take this input: company and model from the agent model and find out what is the maximun and minimum price on \
    which it has already been sold previously.
    
    """
    
    # Parse and validate input data
    company = company.strip().lower()
    model = model.strip().lower()
    
    # Fuzzy match to get selling price range
    price_range = fuzzy_match(sells, company, model)

    if price_range.empty:
        return False
    else:
        min_price = price_range['Price'].min()
        max_price = price_range['Price'].max()
        return (min_price, max_price)
    

recommend = StructuredTool.from_function(
        func=recommend_tool,
        name="recommend_tool",
        description="It will take this input: company, model, price and variant from the model and Check if the price of the car model is \
        more than the actual car price",
        args_schema=recommend_input,
    )
# print(parse_price('₹10.13L'))
# print(recommend_tool('Hyundai', 'Xcent'))
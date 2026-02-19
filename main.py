import os
import requests
from pydantic import BaseModel
from typing import Type
from crewai.tools import BaseTool
from dotenv import load_dotenv

load_dotenv()

class CurrencyConverterInput(BaseModel):
    from_currency: str
    to_currency: str
    amount: float

class CurrenyConverterTool(BaseTool):
    name: str = "currency_converter"
    description: str = "Useful for converting currency rates. Inputs: from_currency, to_currency, amount"
    args_schema: Type[BaseModel] = CurrencyConverterInput

    def _run(self, from_currency: str, to_currency: str, amount: float) -> str:
        api_key = os.getenv("EXCHANGE_RATE_API_KEY")

        if not api_key:
            return "Error. EXCHANGE_RATE_API_KEY is missing from environment variables."
        
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency}"

        try:
            response = requests.get(url)
            data = response.json()

            if response.status_code != 200:
                return f"API Error: {data.get('error-type', 'Unknown error')}"
            
            rate = data['conversion_rates'].get(to_currency)
            if not rate:
                return f"Currency {to_currency} not found."

            converted = amount * rate
            return f"{amount} {from_currency} is {converted:.2f} {to_currency}"
        
        except Exception as e:
            return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    tool = CurrenyConverterTool()
    print(tool._run("USD", "EUR", 100))
from pydantic import BaseModel
from datetime import date

class Sale(BaseModel):
    date : date
    product_id = str
    quantity = int
    total_venda = float
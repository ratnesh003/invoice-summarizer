from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class Order(BaseModel):
    order_id: str
    customer_name: str
    product_name: str
    quantity: int
    unit_price: float
    order_date: date

class ProcessedOrder(Order):
    line_total: float
    discount_amount: float
    net_total: float

class CustomerSummary(BaseModel):
    customer_name: str
    order_count: int
    total_items: int
    gross_total: float
    total_discount: float
    net_total: float

class ProcessingResult(BaseModel):
    summary_report: List[CustomerSummary]
    grand_total_gross: float
    grand_total_discount: float
    grand_total_net: float

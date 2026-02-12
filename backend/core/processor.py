import csv
import logging
from datetime import datetime
from typing import List, Tuple, Dict, Optional
from .models import Order, ProcessedOrder, CustomerSummary, ProcessingResult

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_order_line(line: str) -> Tuple[Optional[Order], Optional[str]]:
    """Parses a single line of the order file. Returns (Order, error_message)."""
    parts = line.strip().split('|')
    if len(parts) != 6:
        return None, f"Invalid format: Expected 6 fields, got {len(parts)}. Line: {line.strip()}"
    
    order_id, customer_name, product_name, quantity_str, unit_price_str, order_date_str = parts
    
    try:
        quantity = int(quantity_str)
        if quantity < 0:
             return None, f"Invalid quantity: {quantity}. Must be non-negative. Line: {line.strip()}"
    except ValueError:
        return None, f"Invalid quantity format: {quantity_str}. Line: {line.strip()}"

    try:
        unit_price = float(unit_price_str)
        if unit_price < 0:
             return None, f"Invalid unit price: {unit_price}. Must be non-negative. Line: {line.strip()}"
    except ValueError:
        return None, f"Invalid unit price format: {unit_price_str}. Line: {line.strip()}"

    try:
        # diverse date formats could be supported, but strict adherence to YYYY-MM-DD as per example for now
        # Handling potential different separators could be an enhancement
        order_date = datetime.strptime(order_date_str, '%Y-%m-%d').date()
    except ValueError:
        return None, f"Invalid date format: {order_date_str}. Expected YYYY-MM-DD. Line: {line.strip()}"

    return Order(
        order_id=order_id.strip(),
        customer_name=customer_name.strip(),
        product_name=product_name.strip(),
        quantity=quantity,
        unit_price=unit_price,
        order_date=order_date
    ), None

def calculate_totals(order: Order) -> ProcessedOrder:
    """Calculates totals and discounts for a valid order."""
    line_total = order.quantity * order.unit_price
    discount = 0.0
    
    if line_total > 500:
        discount = line_total * 0.10
        
    net_total = line_total - discount
    
    return ProcessedOrder(
        **order.model_dump(),
        line_total=line_total,
        discount_amount=discount,
        net_total=net_total
    )

def generate_report(orders: List[ProcessedOrder]) -> ProcessingResult:
    """Generates the summary report grouped by customer."""
    customer_data: Dict[str, CustomerSummary] = {}
    
    grand_total_gross = 0.0
    grand_total_discount = 0.0
    grand_total_net = 0.0
    
    for order in orders:
        if order.customer_name not in customer_data:
            customer_data[order.customer_name] = CustomerSummary(
                customer_name=order.customer_name,
                order_count=0,
                total_items=0,
                gross_total=0.0,
                total_discount=0.0,
                net_total=0.0
            )
        
        summary = customer_data[order.customer_name]
        summary.order_count += 1
        summary.total_items += order.quantity
        summary.gross_total += order.line_total
        summary.total_discount += order.discount_amount
        summary.net_total += order.net_total
        
        grand_total_gross += order.line_total
        grand_total_discount += order.discount_amount
        grand_total_net += order.net_total
        
    return ProcessingResult(
        summary_report=list(customer_data.values()),
        grand_total_gross=grand_total_gross,
        grand_total_discount=grand_total_discount,
        grand_total_net=grand_total_net
    )

def process_file_content(content: str) -> Tuple[str, str]:
    """
    Processes the raw file content. 
    Returns (output_report_string, error_log_string).
    """
    valid_orders: List[ProcessedOrder] = []
    errors: List[str] = []
    
    lines = content.strip().split('\n')
    if not lines:
        return "No data processed.", "File is empty."

    for line in lines:
        if not line.strip():
            continue
            
        order, error = parse_order_line(line)
        if error:
            errors.append(error)
        else:
            processed_order = calculate_totals(order)
            valid_orders.append(processed_order)
            
    result = generate_report(valid_orders)
    
    # Generate Output String Table
    from tabulate import tabulate

    # Generate Output String Table
    headers = ["Customer Name", "Orders", "Items", "Gross Total", "Discount", "Net Total"]
    table_data = []
    
    for summary in result.summary_report:
        table_data.append([
            summary.customer_name,
            summary.order_count,
            summary.total_items,
            f"${summary.gross_total:,.2f}",
            f"${summary.total_discount:,.2f}",
            f"${summary.net_total:,.2f}"
        ])
    

    table_data.append([
        "GRAND TOTAL",
        "",
        "",
        f"${result.grand_total_gross:,.2f}",
        f"${result.grand_total_discount:,.2f}",
        f"${result.grand_total_net:,.2f}"
    ])
    
    output_string = tabulate(table_data, headers=headers, tablefmt="grid", stralign="right", numalign="right")
    
    # Custom adjustments if tabulate grid isn't exactly what we want, but "grid" is usually very clean.
    # The user wanted "cleaner and uniform". Grid handles borders well.
    
    return output_string, "\n".join(errors)

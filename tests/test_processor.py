import pytest
from datetime import date
from backend.core.models import Order, ProcessedOrder
from backend.core.processor import parse_order_line, calculate_totals, generate_report, process_file_content

def test_parse_order_line_valid():
    line = "ORD001|John Smith|Laptop|2|999.99|2024-03-15"
    order, error = parse_order_line(line)
    
    assert error is None
    assert isinstance(order, Order)
    assert order.order_id == "ORD001"
    assert order.customer_name == "John Smith"
    assert order.product_name == "Laptop"
    assert order.quantity == 2
    assert order.unit_price == 999.99
    assert order.order_date == date(2024, 3, 15)

def test_parse_order_line_invalid_format():
    line = "ORD001|John Smith|Laptop|2|999.99" # Missing date
    order, error = parse_order_line(line)
    assert order is None
    assert "Expected 6 fields" in error

def test_parse_order_line_invalid_quantity():
    line = "ORD001|John Smith|Laptop|two|999.99|2024-03-15"
    order, error = parse_order_line(line)
    assert order is None
    assert "Invalid quantity format" in error

def test_parse_order_line_negative_quantity():
    line = "ORD001|John Smith|Laptop|-2|999.99|2024-03-15"
    order, error = parse_order_line(line)
    assert order is None
    assert "Invalid quantity" in error

def test_calculate_totals_no_discount():
    order = Order(
        order_id="1", customer_name="Test", product_name="Test",
        quantity=2, unit_price=100.0, order_date=date(2024, 1, 1)
    )
    processed = calculate_totals(order)
    assert processed.line_total == 200.0
    assert processed.discount_amount == 0.0
    assert processed.net_total == 200.0

def test_calculate_totals_with_discount():
    order = Order(
        order_id="1", customer_name="Test", product_name="Test",
        quantity=1, unit_price=600.0, order_date=date(2024, 1, 1)
    )
    processed = calculate_totals(order)
    assert processed.line_total == 600.0
    assert processed.discount_amount == 60.0 # 10% of 600
    assert processed.net_total == 540.0

def test_generate_report():
    orders = [
        ProcessedOrder(
            order_id="1", customer_name="C1", product_name="P1", quantity=1, unit_price=100.0, order_date=date(2024, 1, 1),
            line_total=100.0, discount_amount=0.0, net_total=100.0
        ),
        ProcessedOrder(
            order_id="2", customer_name="C1", product_name="P2", quantity=1, unit_price=600.0, order_date=date(2024, 1, 1),
            line_total=600.0, discount_amount=60.0, net_total=540.0
        ),
        ProcessedOrder(
            order_id="3", customer_name="C2", product_name="P3", quantity=2, unit_price=10.0, order_date=date(2024, 1, 1),
            line_total=20.0, discount_amount=0.0, net_total=20.0
        )
    ]
    
    result = generate_report(orders)
    
    assert len(result.summary_report) == 2
    
    c1 = next(s for s in result.summary_report if s.customer_name == "C1")
    assert c1.order_count == 2
    assert c1.total_items == 2
    assert c1.gross_total == 700.0
    assert c1.total_discount == 60.0
    assert c1.net_total == 640.0
    
    assert result.grand_total_gross == 720.0
    assert result.grand_total_discount == 60.0
    assert result.grand_total_net == 660.0

def test_process_file_content():
    content = """ORD001|C1|P1|1|600.00|2024-01-01
ORD002|C2|P2|1|100.00|2024-01-01
Invalid|Line"""
    
    output, error = process_file_content(content)
    
    assert "C1" in output
    assert "C2" in output
    assert "GRAND TOTAL" in output
    assert "+" in output # Check for table borders from tabulate grid format
    assert "|" in output
    assert "Invalid format" in error
    assert "Invalid|Line" in error

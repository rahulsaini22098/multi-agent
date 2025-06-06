from enum import Enum

class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    DELIVERED = "delivered"

class OrderItem:
    name: str
    quantity: int
    price: float

    def __init__(self, name: str, quantity: int, price: float):
        self.name = name
        self.quantity = quantity
        self.price = price

    def to_json(self):
        return {
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price,
            "total": self.quantity * self.price
        }

class Order:
    id: str
    customer_id: str
    date: str
    time: str
    status: OrderStatus
    total_amount: float
    items: list[OrderItem]

    def __init__(self, id: str, customer_id: str, date: str, time: str, status: OrderStatus, items: list[OrderItem]):
        self.id = id
        self.customer_id = customer_id
        self.date = date
        self.time = time
        self.status = status
        self.items = items
        self.total_amount = sum(item.quantity * item.price for item in items)

    def to_json(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "date": self.date,
            "time": self.time,
            "status": self.status.value,
            "total_amount": self.total_amount,
            "items": [item.to_json() for item in self.items]
        }

class RetailProvider:
    orders: list[Order] = []

    def __init__(self):
        self.orders = []

    def add_order(self, order: Order):
        self.orders.append(order)

    def get_orders(self, customer_id: str):
        return [order.to_json() for order in self.orders if order.customer_id == customer_id]

    def get_order(self, order_id: str):
        order = next((order for order in self.orders if order.id == order_id), None)
        return order.to_json() if order else None

    def update_order(self, order_id: str, status: OrderStatus):
        order = self.get_order(order_id)
        if order:
            order.status = status

# Initialize the retail provider store
retailStore = RetailProvider()

# Create mock orders with realistic scenarios
orders = [
    # Special customer CUST-1000 order
    Order(
        "ORD-2024-000",
        "CUST-1000",
        "2024-03-19",
        "09:15",
        OrderStatus.DELIVERED,
        [
            OrderItem("MacBook Pro M3", 1, 1999.99),
            OrderItem("Magic Mouse", 1, 79.99),
            OrderItem("USB-C Hub", 1, 89.99),
            OrderItem("Laptop Sleeve", 1, 49.99)
        ]
    ),
    
    # Electronics order
    Order(
        "ORD-2024-001",
        "CUST-2001",
        "2024-03-20",
        "10:15",
        OrderStatus.DELIVERED,
        [
            OrderItem("iPhone 15 Pro", 1, 999.99),
            OrderItem("AirPods Pro", 1, 249.99),
            OrderItem("AppleCare+", 1, 199.99)
        ]
    ),
    
    # Grocery order
    Order(
        "ORD-2024-002",
        "CUST-2002",
        "2024-03-20",
        "14:30",
        OrderStatus.CONFIRMED,
        [
            OrderItem("Organic Bananas", 2, 3.99),
            OrderItem("Whole Milk", 1, 4.49),
            OrderItem("Free Range Eggs", 1, 5.99),
            OrderItem("Whole Grain Bread", 1, 3.49)
        ]
    ),
    
    # Home goods order
    Order(
        "ORD-2024-003",
        "CUST-2003",
        "2024-03-21",
        "09:45",
        OrderStatus.PENDING,
        [
            OrderItem("Memory Foam Pillow", 2, 29.99),
            OrderItem("Bed Sheet Set", 1, 49.99),
            OrderItem("Blackout Curtains", 1, 39.99)
        ]
    ),
    
    # Cancelled order
    Order(
        "ORD-2024-004",
        "CUST-2004",
        "2024-03-21",
        "16:20",
        OrderStatus.CANCELLED,
        [
            OrderItem("Gaming Laptop", 1, 1299.99),
            OrderItem("Gaming Mouse", 1, 79.99),
            OrderItem("Mechanical Keyboard", 1, 149.99)
        ]
    ),
    
    # Clothing order
    Order(
        "ORD-2024-005",
        "CUST-2005",
        "2024-03-22",
        "11:30",
        OrderStatus.PENDING,
        [
            OrderItem("Men's Casual Shirt", 2, 34.99),
            OrderItem("Denim Jeans", 1, 59.99),
            OrderItem("Running Shoes", 1, 89.99)
        ]
    )
]

# Add all orders to the retail store
for order in orders:
    retailStore.add_order(order)

# Function to get the retail store
def get_retail_store():
    return retailStore

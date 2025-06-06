from enum import Enum

class AccountType(Enum):
    SAVINGS = "savings"
    CHECKING = "checking"
    FIXED_DEPOSIT = "fixed_deposit"

class Account:
    id: str
    account_number: str
    account_type: AccountType
    balance: float

    def __init__(self, id: str, account_number: str, account_type: AccountType, balance: float = 0.0):
        self.id = id
        self.account_number = account_number
        self.account_type = account_type
        self.balance = balance

    def to_json(self):
        return {
            "id": self.id,
            "account_number": self.account_number,
            "account_type": self.account_type.value,
            "balance": self.balance
        }

class Customer:
    id: str
    customer_id: str
    accounts: list[Account]

    def __init__(self, id: str, customer_id: str):
        self.id = id
        self.customer_id = customer_id
        self.accounts = []

    def add_account(self, account: Account):
        self.accounts.append(account)

    def get_total_balance(self):
        return sum(account.balance for account in self.accounts)

    def to_json(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "accounts": [account.to_json() for account in self.accounts],
            "total_balance": self.get_total_balance()
        }

class BankingProvider:
    customers: list[Customer] = []

    def __init__(self):
        self.customers = []

    def add_customer(self, customer: Customer):
        self.customers.append(customer)

    def get_customer(self, customer_id: str):
        customer = next((customer for customer in self.customers if customer.customer_id == customer_id), None)
        return customer.to_json() if customer else None

    def get_customer_accounts(self, customer_id: str):
        customer = self.get_customer(customer_id)
        return customer["accounts"] if customer else []

    def get_account(self, account_number: str):
        for customer in self.customers:
            for account in customer.accounts:
                if account.account_number == account_number:
                    return account.to_json()
        return None

    def update_account_balance(self, account_number: str, new_balance: float):
        for customer in self.customers:
            for account in customer.accounts:
                if account.account_number == account_number:
                    account.balance = new_balance
                    return True
        return False

# Initialize the banking provider store
bankingStore = BankingProvider()

# Create mock customers with realistic scenarios
customers = [
    # Special customer CUST-1000
    Customer("CUST-1000", "CUST-1000"),
    # Customer 1: Regular banking customer
    Customer("CUST-3001", "CUST-3001"),
    # Customer 2: High net worth individual
    Customer("CUST-3002", "CUST-3002"),
    # Customer 3: Student account
    Customer("CUST-3003", "CUST-3003"),
    # Customer 4: Business owner
    Customer("CUST-3004", "CUST-3004"),
    # Customer 5: Retiree
    Customer("CUST-3005", "CUST-3005")
]

# Add accounts for special customer CUST-1000
customers[0].add_account(Account("ACC-4000", "1000-1234-5678", AccountType.CHECKING, 25000.00))
customers[0].add_account(Account("ACC-4001", "1000-1234-5679", AccountType.SAVINGS, 100000.00))
customers[0].add_account(Account("ACC-4002", "1000-1234-5680", AccountType.FIXED_DEPOSIT, 200000.00))

# Add accounts for each customer
# Customer 1: Regular banking customer
customers[1].add_account(Account("ACC-4003", "1001-2345-6789", AccountType.CHECKING, 5234.56))
customers[1].add_account(Account("ACC-4004", "1001-2345-6790", AccountType.SAVINGS, 15789.23))

# Customer 2: High net worth individual
customers[2].add_account(Account("ACC-4005", "1002-3456-7890", AccountType.CHECKING, 45678.90))
customers[2].add_account(Account("ACC-4006", "1002-3456-7891", AccountType.SAVINGS, 250000.00))
customers[2].add_account(Account("ACC-4007", "1002-3456-7892", AccountType.FIXED_DEPOSIT, 100000.00))

# Customer 3: Student account
customers[3].add_account(Account("ACC-4008", "1003-4567-8901", AccountType.CHECKING, 1234.56))
customers[3].add_account(Account("ACC-4009", "1003-4567-8902", AccountType.SAVINGS, 500.00))

# Customer 4: Business owner
customers[4].add_account(Account("ACC-4010", "1004-5678-9012", AccountType.CHECKING, 78901.23))
customers[4].add_account(Account("ACC-4011", "1004-5678-9013", AccountType.SAVINGS, 150000.00))

# Customer 5: Retiree
customers[5].add_account(Account("ACC-4012", "1005-6789-0123", AccountType.CHECKING, 3456.78))
customers[5].add_account(Account("ACC-4013", "1005-6789-0124", AccountType.SAVINGS, 75000.00))
customers[5].add_account(Account("ACC-4014", "1005-6789-0125", AccountType.FIXED_DEPOSIT, 50000.00))

# Add all customers to the banking store
for customer in customers:
    bankingStore.add_customer(customer)

# Function to get the banking store
def get_banking_store():
    return bankingStore

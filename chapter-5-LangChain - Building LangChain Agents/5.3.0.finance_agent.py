import os
from langchain.agents import create_agent
from langchain.tools import tool
from load_env import load_env
from langchain_openai import ChatOpenAI

load_env()

@tool
def get_account_balance(account_type: str) -> str:
    """
        Get the currrent balance for a specific account.
        Args:
            account_type: Type of account - 'checking', 'savings', or 'investment'
    """
    balances = {
        "checking": 2500.00,
        "savings": 15000.00,
        "investment": 45000.00
    }

    balance = balances.get(account_type.lower())
    if balance is not None:
        return f"Your {account_type} account balance is ${balance:,.2f}"
    
    return f"Unknown account type: {account_type}. Available: checking, savings, and investment"

@tool
def get_recent_transactions(account_type: str, limit: int = 5) -> str:
    """
        Get recent transactions for an account.
        Args:
            account_type: Type of account - savings, investment, checking
            limit: number of transaction to be return
    """

    transactions = {
        "checking": [
            {"date": "2026-01-15", "description": "Grocery Store", "amount": -85.50},
            {"date": "2026-01-25", "description": "Direct deposit", "amount": 3200.00},
            {"date": "2026-01-05", "description": "Electric bill", "amount": -120.00},
            {"date": "2026-01-17", "description": "Restaurant", "amount": -45.50},
            {"date": "2026-01-23", "description": "Gas Station", "amount": -55.50},
        ],
        "savings": [
            {"date": "2026-01-01", "description": "Interest Payment", "amount": 12.50},
            {"date": "2026-01-16", "description": "Transfer from checking", "amount": 500.00},
        ],
        "investment": [
            {"date": "2026-01-14", "description": "Dividend - AAPL", "amount": 125.50},
            {"date": "2026-01-10", "description": "Buy - VTI", "amount": -1000.00},
        ],
    }

    account_transactions = transactions.get(account_type.lower(), [])[:limit]

    if not account_transactions:
        return f"No transactions found for {account_type}"

    result = f"Recent transactions for {account_type}: \n"

    for t in account_transactions:
        sign = "+" if t['amount'] > 0 else ""
        result +=f"{t['date']}: {t['description']} ({sign}${t['amount']:,.2f})\n"

    return result

@tool
def calculate_budget(monthly_income: float, expense_category: str) -> str:
    """
        Calculate recommended budget allocation for an expense category
        Args:
            monthly_income: User's monthly income
            expense_category: Categories like 'housing', 'food' etc
    """

    allocations = {
        "housing": 0.30,
        "food": 0.12,
        "transportation": 0.10,
        "utilities": 0.08,
        "savings": 0.20,
        "entertainment": 0.05,
        "healthcare": 0.05,
        "other": 0.10,
    }

    percentage = allocations.get(expense_category.lower())

    if percentage is None:
        return f"Unkownn category: {expense_category}. Available {", ".join(allocations.keys())}"
    
    recommended = monthly_income * percentage

    return f"Recommended {expense_category} budget: ${recommended:,.2f}/month ({percentage*100:.0f}% of income)"

SYSTEM_PROMPT = """You are a helpful personal finance assistant.
Your capabilities:
- Check account balances (checking, savings, investment)
- View recent transactions
- Calculate budget recomendations

Guidelines:
- Be helpful and informative
- Provide clear, actionable advice
- Use tools to get accurate information before responding
- Format monetary values clearly
"""

model = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    model_name="openai/gpt-oss-120b:free",
    temperature=0.7,
    max_tokens=100,
    openai_api_key=os.environ["OPEN_ROUTER_API_KEY"],
)
tools = [
    get_account_balance,
    get_recent_transactions,
    calculate_budget
]

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=SYSTEM_PROMPT
)


def main():
    print('=' * 50)
    print("Stage 1: Simple Finance Assistant")
    print("="*50)

    # Test 1: check balance
    balance_message = "What's my checking account balance?"

    print(f"\nQuery: {balance_message}")
    response = agent.invoke({
        "messages": [{"role": "user", "content": balance_message}]
    })

    print(f"Agent: {response['messages'][-1].content}")

    # Test 2: Multi-tool query
    multi_tool_prompt = "Show me my savings balance and recent transactions"
    print(f"\nQuery: {multi_tool_prompt}")
    response = agent.invoke({
        "messages": [{"role": "user", "content": multi_tool_prompt}]
    })
    print(f"Agent: {response['messages'][-1].content}")


if __name__ == "__main__":
    main()
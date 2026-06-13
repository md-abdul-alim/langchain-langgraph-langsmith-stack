import os
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from load_env import load_env
from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model
from langchain.agents.middleware import (
    wrap_model_call,
    dynamic_prompt,
    ModelRequest,
    ModelResponse
)
from dataclasses import dataclass
from finance_user_data import USER_DATABASE
from finance_prompts import BASE_PROMPT, PREMIUM_PROMPT, PLATINUM_PROMPT, GUIDELINES, SYSTEM_PROMPT
load_env()

os.environ["OPENROUTER_API_KEY"]=os.environ["OPEN_ROUTER_API_KEY"]

basic_model = init_chat_model(
    model="openai/gpt-oss-120b:free",
    model_provider="openrouter",
    temperature=0.5,
    max_tokens=512
)

premium_model = init_chat_model(
    model="openrouter/owl-alpha",
    model_provider="openrouter",
    max_tokens=2048
)

platinum_model = init_chat_model(
    model="google/gemma-4-31b-it:free",
    model_provider="openrouter",
)

@dataclass
class UserContext:
    user_id: str
    user_name: str
    membership_tier: str # 'basic', 'premium', 'platinum'
    preferred_currency: str

@tool
def get_account_balance(account_type: str, runtime: ToolRuntime[UserContext]) -> str:
    """
        Get the currrent balance for a specific account for a user.
        Args:
            account_type: Type of account - 'checking', 'savings', or 'investment'
    """
    user_id = runtime.context.user_id
    currency = runtime.context.preferred_currency
    user_data = USER_DATABASE.get(user_id)

    balance = user_data.get('account', {}).get(account_type.lower())

    if balance is not None:
        if currency == "EUR":
            balance = balance * 1.4
            return f"Your {account_type} account balance is euro{balance:,.2f}"
        return f"Your {account_type} account balance is ${balance:,.2f}"
    return f"Unkownn account type: {account_type}. Avaliable: checking, saving, investment"

@tool
def get_recent_transactions(
    account_type: str, 
    limit: int = 5,
    runtime: ToolRuntime[UserContext] = None) -> str:
    """
        Get recent transactions for an account.
        Args:
            account_type: Type of account - savings, investment, checking
            limit: number of transaction to be return
    """

    user_id = runtime.context.user_id
    user_data = USER_DATABASE.get(user_id)

    account_transactions = user_data.get("transactions", {}).get(account_type.lower(), [])[:limit]

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

@tool
def get_personalized_greeting(runtime: ToolRuntime[UserContext]) -> str:
    """
        Get a personalized greeting for the user. No arguments required
    """
    name = runtime.context.user_name
    tier = runtime.context.membership_tier

    tier_benefits = {
        "basic": "You have access to standard features.",
        "premium": "As a premium member, you get priority support and advanced analytics!",
        "platinum": "Welcome, platinum member! You have access to all features including personal advisor consultations."
    }

    benefit_message = tier_benefits.get(tier, "")
    return f"Hello, {name}! {benefit_message}"

"""
Define Middlewares
"""
@wrap_model_call
def dynamic_model_selector(request: ModelRequest, handler) -> ModelResponse:
    """
        Selects model based on user's membermship tier
    """

    tier = request.runtime.context.membership_tier
    if tier == "platinum":
        request.override(model=platinum_model)
        print(f"[Middleware] Using PLATINUM model (google/gemma-4-31b-it:free, limitless)")
    elif tier == "premium":
        request.override(model=premium_model)
        print(f"[Middleware] Using PREMIUM model (openrouter/owl-alpha, 2048 tokens)")
    else:
        request.override(model=basic_model)
        print(f"[Middleware] Using BASIC model (openai/gpt-oss-120b:free, 512 tokens)")

    return handler(request)

@dynamic_prompt
def tier_based_prompt(request: ModelRequest) -> str:
    """
        Generate system prompt based on user's membership tier
    """
    tier = request.runtime.context.membership_tier
    user_name = request.runtime.context.user_name

    base_prompt = f""""
        You are a personal finance assistant helping {user_name}.

        {BASE_PROMPT}
    """

    if tier == "premium":
        return base_prompt + PREMIUM_PROMPT
    elif tier == "platinum":
        return base_prompt + PLATINUM_PROMPT
    else: # basic
        return base_prompt + GUIDELINES


tools = [
    get_account_balance,
    get_recent_transactions,
    calculate_budget,
    get_personalized_greeting
]

middleware=[
    dynamic_model_selector,
    tier_based_prompt
]

agent = create_agent(
    model=basic_model,
    tools=tools,
    # system_prompt=SYSTEM_PROMPT,
    context_schema=UserContext,
    middleware=middleware
)

def main():
    print('=' * 50)
    print("Stage 1: Simple Finance Assistant")
    print("="*50)

    alice_context = UserContext(
        user_id='user_001',
        user_name='Alice Johnson',
        membership_tier='platinum',
        preferred_currency='USD'
    )
    bob_context = UserContext(
        user_id='user_002',
        user_name='Bob Smith',
        membership_tier='basic',
        preferred_currency='EUR'
    )
    carol_context = UserContext(
        user_id='user_003',
        user_name='Carol Davis',
        membership_tier='premium',
        preferred_currency='EUR'
    )

    # Test 1: check balance
    # balance_message = "What's my checking account balance?"

    # print(f"\nQuery: {balance_message}")
    # response = agent.invoke(
    #     {
    #         "messages": [{"role": "user", "content": balance_message}]
    #     },
    #     context=alice_context
    # )

    # print(f"Agent response 1: {response['messages'][-1].content}")

    # # Test 2: Multi-tool query
    # multi_tool_prompt = "Show me my savings balance and recent transactions"
    # print(f"\nQuery: {multi_tool_prompt}")
    # response = agent.invoke(
    #     {
    #         "messages": [{"role": "user", "content": multi_tool_prompt}]
    #     },
    #     context=bob_context
    # )
    # print(f"Agent response 2: {response['messages'][-1].content}")

    # # Test 3: Budget calculation
    # budget_prompt = "I make $5000/month. How much should i spend on hoursing?"
    # print(f"\nQuery: {budget_prompt}")
    # response = agent.invoke(
    #     {
    #         "messages": [{"role": "user", "content": budget_prompt}]
    #     },
    #     context=carol_context
    # )
    # print(f"Agent response 3: {response['messages'][-1].content}")
    print("="*40)

    # # Test 4: Financial situation and advice
    financial_situation_query = "What's my financial situation? Check all my accounts and give me advice"
    print("\n Same query, different treatment")
    response = agent.invoke(
        {
            "messages": [{"role": "user", "content": financial_situation_query}]
        },
        context=alice_context
    )
    print(f"Agent response 4: {response['messages'][-1].content}")


if __name__ == "__main__":
    main()
import os
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain.tools import tool, ToolRuntime
from load_env import load_env
from pydantic import BaseModel, Field
from typing import Literal
from langchain.chat_models import init_chat_model
from langchain.agents.middleware import (
    wrap_model_call,
    dynamic_prompt,
    wrap_tool_call,
    ModelRequest,
    ModelResponse
)
from dataclasses import dataclass
from langchain_core.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest
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

class FinancialResponse(BaseModel):
    summary: str = Field(description="A brief summary of the response (1-2 sentences)")
    details: str = Field(description="Detailed explanation or data")

    action_items: list[str] = Field(
        default_factory=list,
        description="List of recommended actions the user should take"
    )
    warnings: list[str] = Field(
        default_factory=list,
        description="Any warnings or concerns to highlight"
    )

    confidence: Literal["high", "medium", "low"] = Field(
        default="high",
        description="Confidence level in the advice provided"
    )

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

@tool
def transfer_money(
    from_account: str,
    to_account: str,
    amount: float,
    runtime: ToolRuntime[UserContext]
) -> str:
    """
        Transfer money between accounts
        Args:
            from_account: Source account ('checking', 'savings', 'investment')
            to_account: Destination account ('checking', 'savings', 'investment')
            amount: Amount to transfer (must be positive)
    """

    if amount <= 0:
        raise ValueError("Transfer amount must be positive")
    if amount > 10000:
        raise ValueError("Transfer amount exceeds the daily limit of $10,000")
    if from_account.lower() == to_account.lower():
        raise ValueError("Cannot transfer to the same account")
    
    user_id = runtime.context.user_id
    user_data = USER_DATABASE.get(user_id, {})
    accounts = user_data.get("accounts", {})

    from_balance = accounts.get(from_account.lower())

    if from_balance is None:
        raise ValueError(f"Source account {from_account} not found.")
    
    if to_account.lower() not in accounts:
        raise ValueError(f"Destination account '{to_account}' not found.")
    
    if from_balance < amount:
        raise ValueError(f"Insufficient funds. {from_account} balance: ${from_balance: .2f}")
    
    # Simulate successful transfer
    return f"Successfully transferred ${amount: .2f} from {from_account} to {to_account}."

@wrap_tool_call
def handle_tool_errors(request: ToolCallRequest, handler) -> ToolMessage:
    """
        Gracefully handles too execution errors
    """
    tool_name = request.tool_call['name']
    try:
        # Attempt to execute the tool
        return handler(request)
    except ValueError as e:
        error_message = f"{tool_name} failed: {str(e)}"
        print(f"[Error Handler] Caught ValueError: {e}")

        return ToolMessage(
            content=error_message,
            tool_call_id=request.tool_call["id"]
        )
    except KeyError as e:
        error_message = f"{tool_name} error: Required data not found - {str(e)}"
        print(f"[Error Handler] Caught KeyError: {e}")

        return ToolMessage(
            content=error_message,
            tool_call_id=request.tool_call["id"]
        )
    except Exception as e:
        error_message = f"{tool_name} encountered an error. Please try again or countact support."
        print(f"[Error Handler] Caught Unexpected error: {type(e).__name__}- {e}")

        return ToolMessage(
            content=error_message,
            tool_call_id=request.tool_call["id"]
        )


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
    get_personalized_greeting,
    transfer_money

]

middleware=[
    dynamic_model_selector,
    tier_based_prompt,
    handle_tool_errors
]

agent = create_agent(
    model=basic_model,
    tools=tools,
    # system_prompt=SYSTEM_PROMPT,
    context_schema=UserContext,
    middleware=middleware,
    response_format=ToolStrategy(FinancialResponse)
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
    # print("="*40)

    # # # Test 4: Financial situation and advice
    # financial_situation_query = "What's my financial situation? Check all my accounts and give me advice"
    # print("\n Same query, different treatment")
    # response = agent.invoke(
    #     {
    #         "messages": [{"role": "user", "content": financial_situation_query}]
    #     },
    #     context=alice_context
    # )
    # print(f"Agent response 4: {response['messages'][-1].content}")

    ## Test 5: Successful transfer
    # print("="*40)

    # successful_transfer_prompt = "Transfer $500 from checking to savings"
    # response = agent.invoke(
    #     {
    #         "messages": [{"role": "user", "content": successful_transfer_prompt}]
    #     },
    #     context=alice_context
    # )
    # print(f"Agent response 5: {response['messages'][-1].content}")

    ## Test 6: Error handling - insufficient funds
    # print("="*40)

    # insufficient_amount_prompt = "Transfer $50000 from checking to savings"
    # response = agent.invoke(
    #     {
    #         "messages": [{"role": "user", "content": insufficient_amount_prompt}]
    #     },
    #     context=alice_context
    # )
    # print(f"Agent response 5: {response['messages'][-1].content}")

    ## Test 7: Error handling - same account
    # print("="*40)

    # same_account_transfer_prompt = "Transfer $100 from checking to checking (should fail)"
    # response = agent.invoke(
    #     {
    #         "messages": [{"role": "user", "content": same_account_transfer_prompt}]
    #     },
    #     context=alice_context
    # )
    # print(f"Agent response 5: {response['messages'][-1].content}")

    ## Test 8 : Structured Response
    print("="*40)

    query = "What's my financial stituation? Check all my accounts and give me advice"
    print('\n Alic - Financial Breakdown')
    response = agent.invoke(
        {
            "messages": [{"role": "user", "content": query}]
        },
        context=alice_context
    )
    # print(f"Agent response 5: {response['messages'][-1].content}")
    structured: FinancialResponse = response["structured_response"]
    print("\nSTRUCTURED RESPONSE")
    print("\nSummary: \n {structured.summary}")
    print("\nDetails: \n {structured.details}")

    print("\nAction Items:")
    for item in structured.action_items:
        print(f"* {item}")

    print("\nWarnings:")
    for warning in structured.warnings:
        print(f"* {warning}")

    print(f"\n Confidence: {structured.confidence}")


if __name__ == "__main__":
    main()
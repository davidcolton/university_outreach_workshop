import mellea
from mellea.backends import ModelOption, tool

@tool
def web_search(query: str) -> str:
    """Search the web for information about a topic.

    Args:
        query: The search query.
    """
    # Stub — replace with a real search client in production.
    return f"Top result for '{query}': Mellea is a Python framework for generative programs."

@tool(name="calculator")
def calculate(expression: str) -> str:
    """Evaluate a safe arithmetic expression and return the result as a string.

    Args:
        expression: An arithmetic expression, e.g. '12 * 7 + 3'.
    """
    allowed = set("0123456789 +-*/(). ")
    if not all(c in allowed for c in expression):
        return "Error: expression contains disallowed characters."
    return str(eval(expression))  # noqa: S307 — only safe characters pass the guard above

m = mellea.start_session()

response = m.instruct(
    "What is Mellea, and how many characters are in the word 'Mellea'?",
    model_options={ModelOption.TOOLS: [web_search, calculate]},
)
print(str(response))
# Output will vary — LLM responses depend on model and temperature.
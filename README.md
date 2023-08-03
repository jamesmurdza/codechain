# CodeChain

CodeChain is a library for generating and evaluating code with LLMs.

To install: `pip install codechain`

To install from source: `pip install -e .`

To run unit tests: `python tests/*.py`

## Code completion

Usage is very simple:

```python
from codechain.generation import CompleteCodeChain
from langchain.chat_models import ChatOpenAI

generator = CompleteCodeChain.from_llm(
    ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)
    )

result = generator.run("""
def fibonacci(n):
# Generate the n-th fibonacci number.
""")

print(result)
```

Output:
```python
def fibonacci(n):
    # Generate the n-th fibonacci number.
    if n <= 0:
        return "Invalid input. n must be a positive integer."
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        fib_list = [0, 1]
        for i in range(2, n):
            fib_list.append(fib_list[i-1] + fib_list[i-2])
        return fib_list[n-1]
```

## LLM evaluation

See [here](https://github.com/jamesmurdza/humaneval-langchain/) for an example of how to use this library with HumanEval.


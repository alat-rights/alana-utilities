from setuptools import setup, find_packages

setup(
    name="alana",
    version="0.0.10",  # Update the version number as needed
    author="Alana",
    author_email="hi@alana.computer",
    description="Utilities for Alana, and maybe you too. Mostly geared toward LLM-heavy workflows.",
    long_description="""
🎵 Note: I have been making new releases frequently. Make sure your package is up-to-date!

⚠️ Warning: This library is in active early development! No guarantees are made for backward compatibility. The library is NOT production-ready.

## Is this for me?
This library is mostly designed for me (hence the name), but they might be helpful for you too!

Here are some questions to ask yourself when considering whether to use this library:
- Do you interact with LLMs? (Currently, only Anthropic LLMs are supported).
- Do you value conciseness?
- Are you writing **non-production prototype code**, where 1, occassional bugs and behavioral changes are acceptable, and 2, developer ergonomics are more important than performance?
  - Note: This library *strongly* assumes this use-case! e.g. `alana.gen` actually writes to the console by default (you can disable this with `loud=False`).
- Do the features appeal to you?

## Philosophy:
- Programming is too slow! This is doubly true when you're interacting with LLMs. By building nice utilities with sane defaults, I hope to speed up my (and maybe your) workflow.
- I make trade-offs to speed up the developer experience:
  - I do not try hard to anticipate future upstream API changes. I'm also ok with breaking backward compatibility to make my functions more concise and more usable.
  - Usability > Principles. While I don't relish in it, I'm ok with breaking conventions designed for large production libraries if it speeds up programmers who use `alana`. The priority is to make the library intuitive and fast.
  - I don't try to serve every use-case.
- Simplicity is key. This library strives to be readable and straightforward.

## Motivating Examples:
(I tested these, and tried to make sure my code was idiomatic in all cases. Sorry if I messed up! Please report any issues to `h i ( a t ) [pip package name for this library] dot computer`.)

Continuing a list of messages using Anthropic API (adapted from [Anthropic API documentation](https://docs.anthropic.com/claude/reference/messages_post):
```
import anthropic
from anthropic.types import MessageParam
messages = [
  MessageParam(
    role="user",
    content="Hello, Claude!"
  ),
]
output_text = anthropic.Anthropic().messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=messages
).content[0].text
messages.append(
  MessageParam(
    role="assistant",
    content=output_text
  )
)
print(messages)  # [{'role': 'user', 'content': 'Hello, Claude!'}, {'role': 'assistant', 'content': "Hello! It's nice to meet you. How are you doing today?"}]
```

Equivalent `alana` code:
```
import alana
messages = []
alana.gen(user="Hello, Claude!", messages=messages, model="opus", max_tokens=1024)
print(messages)  # [{'role': 'user', 'content': 'Hello, Claude!'}, {'role': 'assistant', 'content': "Hello! It's nice to meet you. How are you doing today?"}]
```

Also, equivalent `alana` code thanks to defaults:
```
import alana
messages = []
alana.gen(user="Hello, Claude!", messages=messages)
print(messages)  # [{'role': 'user', 'content': 'Hello, Claude!'}, {'role': 'assistant', 'content': "Hello! It's nice to meet you. How are you doing today?"}]
```
   """,
    long_description_content_type="text/markdown",
    url="https://github.com/alat-rights/alana-utilities",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="LLM, utilities",  # Add relevant keywords
    python_requires=">=3.6",
    install_requires=["anthropic", "colorama", "numpy"],
)

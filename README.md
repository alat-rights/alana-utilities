# alana-utilities (Utilities Library for LLM-Heavy Workflows)

## Install Instructions
```
pip install alana
```
⚠️ Warning: This library is in active early development! No guarantees are made for backward compatibility. The library is NOT intended to be production-ready.

## Is this for me?
This library is mostly designed for me (hence the name), but I hope they're helpful for you too!

- Do you interact with LLMs? (Currently, only Anthropic LLMs are supported).
- Do you value conciseness?
- Are you writing **non-production prototype code**, where 1, occassional bugs and behavioral changes are acceptable, and 2, developer ergonomics are more important than performance?
  - Note: This library *strongly* assumes this use-case! Many functions actually write to the console by default (you can disable this with `loud=False`).
- Do the features appeal to you?

## Philosophy:
- Programming is too slow! This is doubly true when you're interacting with LLMs. By building nice utilities with sane defaults, I hope to speed up my (and maybe your) workflow.
- I make trade-offs to speed up the developer experience:
  - I do not try hard to anticipate future upstream API changes. I'm ok with breaking backward compatibility to make my functions more concise and more usable.
  - Usability > Principles. While I don't relish in it, I'm ok with breaking conventions designed for large production libraries if it speeds up programmers who use `alana`. The priority is to make the library intuitive and fast.
  - I don't try to serve every use-case.

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
print(messages)
```

Equivalent `alana` code:
```
import alana
messages = []
alana.gen(user="Hello, Claude!", messages=messages, model="opus", max_tokens=1024)
print(messages)
```

Also, equivalent `alana` code thanks to defaults:
```
import alana
messages = []
alana.gen(user="Hello, Claude!", messages=messages)
print(messages)
```

## Features:
- Easy color print: `alana.red`, `alana.green`, `alana.blue`, `alana.yellow`, `alana.cyan`
- Easy pretty print with Sonnnet (or an Anthropic model of your choice): `alana.pretty_print`
- Make it easier to use the Anthropic API:
  - `alana.gen`, for easy Claude generations
  - `alana.gen_examples`, `alana.gen_examples_list` for generating few-shot examples
  - `alana.get_xml`, for using regex to get XML tag contents
- Easy prompt generation (meta-prompt) `alana.gen_prompt`
- New (and thus maybe buggy): `alana.remove_xml` to strip certain XML tag-enclosed content from a string (along with the tags). This is primarily intended to get rid of "<reasoning>...</reasoning>" strings.
- A bunch of aliases

## Coming Soon:
- Improve docs
- Generating alternative prompts given a prompt
- Better support for multi-turn prompting
- OpenAI model support
- Support for automatic "are you sure"/"are you confused" multi-turn prompting
- Automatic error checking (are there mistakes in this code, sanity checking of model outputs)
- Automatic model-switching on rate limit
- Prompt test case generation and easy prompt testing

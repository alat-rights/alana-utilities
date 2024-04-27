<p align="center">
  <img style="text-align: center;" src="https://github.com/alat-rights/alana-utilities/assets/54920181/d58b866b-30fc-4697-98d3-63d3742a2198" alt="drawing" width="250"/>
</p>
<p align="center">
  <em>Make prototyping with Claude fast and easy.</em>
</p>
<h1 align="center">
  alana-utilities 
</h1>
<p align="center">
  <a href="https://pypi.org/project/alana/" target="_blank">
      <img alt="Python" src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" />
  </a>
  <a href="https://pypi.org/project/alana/" target="_blank">
      <img alt="Python" src="https://img.shields.io/pypi/v/alana?style=for-the-badge&color=3670A0" />
  </a>
</p>

## What is alana-utilities?
This library is designed to make interacting with Claude fast and easy. It is primarily targetted toward people writing non-production, prototype code. It prioritizes developer ergonomics.

It speeds up lots of things that I frequently find myself doing with Claude.

- Generating a response to a user and system prompt `alana.gen(user=..., system=...)`
- Creating and/or extending a list of MessageParams `alana.respond(message_content, role="user")`
- Extracting content from Claude's output using Regex `alana.get_xml(tag, content)`
- Generate a prompt or a Python list of few-shot examples `alana.gen_prompt` & `alana.few_shot` respectively

## What is alana?
I am alana :)

## Motivating Examples
*I tested these, and I've tried to make sure my code was idiomatic in all cases. Sorry if I messed up! Please open a [GitHub issue](https://github.com/alat-rights/alana-utilities/issues) if you catch a mistake.*

Continuing a list of messages using Anthropic API (adapted from [Anthropic API documentation](https://docs.anthropic.com/claude/reference/messages_post)):
```Python
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
```Python
import alana
messages = []
alana.gen(user="Hello, Claude!", messages=messages, model="opus", max_tokens=1024)
print(messages)  # [{'role': 'user', 'content': 'Hello, Claude!'}, {'role': 'assistant', 'content': "Hello! It's nice to meet you. How are you doing today?"}]
```

Also, equivalent `alana` code thanks to defaults:
```Python
import alana
messages = []
alana.gen(user="Hello, Claude!", messages=messages)
print(messages)  # [{'role': 'user', 'content': 'Hello, Claude!'}, {'role': 'assistant', 'content': "Hello! It's nice to meet you. How are you doing today?"}]
```

## Install Instructions
```Python
pip install alana
```
🎵 Note: I have been making new releases frequently. Make sure your package is up-to-date!

⚠️ Warning: This library is in active early development! No guarantees are made for backward compatibility. The library is NOT production-ready.

## Usage Instructions
1. Import via `import alana` or, if you're brave, `from alana import *`.
2. Make your Anthropic API key available as an environment variable. `os.environ["ANTHROPIC_API_KEY"] = "..."`

The documentation for this project is hosted at [utils.alana.computer](https://utils.alana.computer).

## Philosophy
- Programming is too slow! This is doubly true when you're interacting with LLMs. By building nice utilities with sane defaults, I hope to speed up my (and maybe your) workflow.
- I make trade-offs to speed up the developer experience:
  - I do not try hard to anticipate future upstream API changes. I'm also ok with breaking backward compatibility to make my functions more concise and more usable.
  - Usability > Principles. While I don't relish in it, I'm ok with breaking conventions designed for large production libraries if it speeds up programmers who use `alana`. The priority is to make the library intuitive and fast.
  - I don't try to serve every use-case.
- Simplicity is key. This library strives to be readable and straightforward.

## Features
- Easy color print: `alana.red`, `alana.green`, `alana.blue`, `alana.yellow`, `alana.cyan`. Try `alana.green("Hello!")`
- Easy pretty print with Sonnet (or an Anthropic model of your choice): `alana.pretty_print`. Try `alana.pretty_print(t.arange(16, device='cpu').reshape(2,2,4))`
- Make it easier to use the Anthropic API:
  - `alana.gen`, for easy Claude generations. Try `alana.gen(user="Hello, Claude!")`. You can pass in a `messages` parameter (a list of anthropic.types.MessageParams) either in place of or together with a `user` parameter.
  - `alana.respond`, easily appending a user message to a list of MessageParams!
  - `alana.gen_examples`, `alana.gen_examples_list` for generating few-shot examples.
  - `alana.gen_prompt`, for easy prompt generation (meta-prompt).
  - `alana.get_xml`, for using regex to get XML tag contents from model outputs. ⚠️ Regex parsing of XML may be unreliable!
  - `alana.remove_xml` to strip certain XML tag-enclosed content from a string (along with the tags). This is primarily intended to get rid of "<reasoning>...</reasoning>" strings. ⚠️ Regex parsing of XML may be unreliable!
- A bunch of aliases (Try: `alana.few_shot`, `alana.n_shot`, or `alana.xml`)

## Contributing
A big welcome and thank you for considering contributing to alana-utilities open source project! It’s people like you that make it a reality for users in our community.

Reading and following these guidelines will help us make the contribution process easy and effective for everyone involved. It also communicates that you agree to respect the time of the developers managing and developing these open source projects. In return, we will reciprocate that respect by addressing your issue, assessing changes, and helping you finalize your pull requests.

### Getting started
For changes that address core functionality or would require breaking changes (e.g. a major release), it's best to open an Issue to discuss your proposal first. This is not required but can save time creating and reviewing changes.
In general, we follow the ["fork-and-pull" Git workflow](https://github.com/susam/gitpr).

### Style and formating
We are using [Black](https://github.com/psf/black) for formating and [PyRight](https://github.com/microsoft/pyright) for type checking.

Before pushing your code and making PR make sure that you have run `black .` on your code, otherwise it will fail.
```commandline
  $ pip install black
  $ black.
```
To keep types in code consistent:
```commandline
  $ pip install pyright
  $ pyright .
```

### Testing
There are simple tests written with `unittest`. I am working on extending the test suite.

You may need to provide your Anthropic API key as an environment variable to run all of the unit tests. See [#10](https://github.com/alat-rights/alana-utilities/issues/10).

First install flaky plugin with `pip`:
```
$ pip install flaky
```
Next run:
```
$ python simple_tests.py
```

## Coming Soon
- Generating alternative prompts given a prompt
- OpenAI model support
- Support for automatic "are you sure"/"are you confused" multi-turn prompting
- Automatic error checking (are there mistakes in this code, sanity checking of model outputs)
- Automatic model-switching on rate limit
- Support for quick-and-dirty unit-testing with Claude!
- Prompt test case generation and easy prompt testing

# alana-utilities
Quick utilities mostly geared toward interacting with LLMs.

Designed for myself (hence the name), but hopefully helpful for you too!

Design still in flux!

Install Instructions
```
pip install alana
```

Features
- Easy color print: `alana.red`, `alana.green`, `alana.blue`, `alana.yellow`, `alana.cyan`
- Easy pretty print with Sonnnet (or an Anthropic model of your choice): `alana.pretty_print`
- Make it easier to use the Anthropic API:
  - `alana.gen`, for easy Claude generations
  - `alana.gen_examples`, `alana.gen_examples_list` for generating few-shot examples
  - `alana.get_xml`, for using regex to get XML tag contents
- Easy prompt generation (meta-prompt) `alana.gen_prompt`
- New (and thus maybe buggy): `alana.remove_xml` to strip certain XML tag-enclosed content from a string (along with the tags). This is primarily intended to get rid of "<reasoning>...</reasoning>" strings.
- A bunch of aliases

TODO:
- Generating alternative prompts given a prompt
- Better support for multi-turn prompting
- OpenAI model support
- Support for automatic "are you sure"/"are you confused" multi-turn prompting
- Automatic error checking (are there mistakes in this code, sanity checking of model outputs)
- Automatic model-switching on rate limit
- Prompt test case generation and easy prompt testing

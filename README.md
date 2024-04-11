# alana-utilities
Quick utilities for myself, mostly geared toward interacting with LLMs.

Install Instructions
```
pip install alana
```

- Easy color print: red, green, blue, yellow, cyan
- Make it easier to use the Anthropic API:
  - gen, for easy Claude generations
  - gen_examples, gen_examples_list for generating few-shot examples
  - get_xml, for using regex to get XML tag contents
- A bunch of aliases

TODO:
- Easy prompt generation (meta-prompt) and alternative prompts given prompt
- OpenAI model support
- Support for automatic "are you sure"/"are you confused" multi-turn prompting
- Support for multi-turn model interactions
- Automatic error checking (are there mistakes in this code, sanity checking of model outputs)
- Automatic model-switching on rate limit
- Prompt test case generation and easy prompt testing

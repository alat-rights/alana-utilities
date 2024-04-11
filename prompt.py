from typing import List, Optional
from color import red
import re

def get_xml_pattern(tag: str):
    if tag.count('<') > 0 or tag.count('>') > 0:
        raise ValueError("No '>' or '<' allowed in get_xml!")
    return rf"<{tag}>(.*?)</{tag}>"

def get_xml(tag: str, content: str) -> List[str]:
    if tag.count('<') > 0 or tag.count('>') > 0:
        raise ValueError("No '>' or '<' allowed in get_xml!")
    pattern = get_xml_pattern(tag)
    matches = re.findall(pattern, content, re.DOTALL)
    return matches

def grab(tag: str, content: str) -> List[str]:
    return get_xml(tag, content)

def xml(tag: str, content: str) -> List[str]:
    return get_xml(tag, content)

def gen(user: str, system: str = "", model: str = "opus", api_key: Optional[str] = None, max_tokens = 1024) -> str:
    models = {
        'opus' : 'claude-3-opus-20240229',
        'sonnet' : 'claude-3-sonnet-20240229',
        'haiku' : 'claude-3-haiku-0307'
    }
    backend = models['opus']
    if model in models:
        backend = models[model]

    import os
    from anthropic import Anthropic

    if api_key is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
    client = Anthropic(
        # This is the default and can be omitted
        api_key=api_key,
    )

    message = client.messages.create(
        max_tokens=max_tokens,
        messages=[
            {
                "role": "user",
                "content": user,
            }
        ],
        system=system,
        model=backend,
    )
    return message.content[0].text

def gen_examples_list(instruction: str, n_examples: int = 5, model: str = "opus") -> List[str]:
    system = """You are a prompt engineering assistant tasked with generating few-shot examples given a task.

    Your user would like to accomplish a specific task. His/her description of the task will be enclosed in <description></description> XML tags.
    
    You are to generate {n_examples} examples of this task. EACH example must be enclosed in <example></example> XML tags. Each example should make the input and output clear.

    Make sure your examples are clear, high-quality, consistent, and cover a range of use-cases.
    """.format(n_examples=n_examples)

    user = """
    The user's task is as follows:
    <description>{instruction}</description>

    Before generating your examples, feel free to think out loud using <thinking></thinking> XML tags.
    """.format(instruction=instruction)
    model_output = gen(user=user, system=system, model=model)
    return get_xml('example', model_output)

def gen_examples(instruction: str, n_examples: int = 5, model: str = "opus") -> str:
    examples = gen_examples_list(instruction=instruction, n_examples=n_examples, model=model)
    formatted_examples = "\n<examples>\n<example>" + '</example>\n<example>'.join(examples) + "</example>\n</examples>"
    return formatted_examples

def n_shot_list(instruction: str, n_examples: int = 5, model: str = "opus"):
    return gen_examples_list(instruction=instruction, n_examples=n_examples, model=model)

def n_shot(instruction: str, n_examples: int = 5, model: str = "opus"):
    return gen_examples(instruction=instruction, n_examples=n_examples, model=model)

def few_shot_list(instruction: str, n_examples: int = 5, model: str = "opus"):
    return gen_examples_list(instruction=instruction, n_examples=n_examples, model=model)

def few_shot(instruction: str, n_examples: int = 5, model: str = "opus"):
    return gen_examples(instruction=instruction, n_examples=n_examples, model=model)
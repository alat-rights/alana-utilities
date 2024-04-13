from typing import List, Optional
from alana.color import red
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

DEFAULT_MODEL = "sonnet" # Sonnet so fast!

def create_message(user: str, system: str = "", model: str = DEFAULT_MODEL, api_key: Optional[str] = None, max_tokens = 1024):
    raise NotImplementedError

def gen(user: str, system: str = "", model: str = DEFAULT_MODEL, api_key: Optional[str] = None, max_tokens = 1024) -> str:
    models = {
        'opus' : 'claude-3-opus-20240229',
        'sonnet' : 'claude-3-sonnet-20240229',
        'haiku' : 'claude-3-haiku-0307',
        'claude-2.1' : 'claude-2.1',
        'claude-2.0' : 'claude-2.0',
        'claude-instant-1.2' : 'claude-instant-1.2'
    }
    backend = models[DEFAULT_MODEL]
    if model in models:
        backend = models[model]
    else:
        red(f"gen() -- Caution! model string not recognized; reverting to {DEFAULT_MODEL=}.") # TODO: C'mon we can do better error logging than this

    import os
    from anthropic import Anthropic

    if api_key is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
    client = Anthropic(
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
    red(message)
    return message.content[0].text

def gen_examples_list(instruction: str, n_examples: int = 5, model: str = "sonnet", api_key: Optional[str] = None, max_tokens: int = 1024) -> List[str]:
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
    model_output = gen(user=user, system=system, model=model, api_key=api_key, max_tokens=max_tokens)
    return get_xml('example', model_output)

def gen_examples(instruction: str, n_examples: int = 5, model: str = DEFAULT_MODEL, api_key: Optional[str] = None, max_tokens: int = 1024) -> str:
    examples = gen_examples_list(instruction=instruction, n_examples=n_examples, model=model, api_key=api_key, max_tokens=max_tokens)
    formatted_examples = "\n<examples>\n<example>" + '</example>\n<example>'.join(examples) + "</example>\n</examples>"
    return formatted_examples

def prompt_gen(instruction: str, model: str = DEFAULT_MODEL, api_key: Optional[str] = None, max_tokens: int = 1024) -> str:
    meta_system_prompt = """You are a prompt engineering assistant. Your task is to generate a 

    Your user would like to accomplish a specific task. His/her description of the task will be enclosed in <description></description> XML tags.
    """
    meta_prompt = """

    """
    return gen(meta_prompt, meta_system_prompt, model=model, api_key=api_key, max_tokens=max_tokens)

# Aliases!
def grab(tag: str, content: str) -> List[str]:
    """Alias for get_xml"""
    return get_xml(tag, content)

def xml(tag: str, content: str) -> List[str]:
    """Alias for get_xml"""
    return get_xml(tag, content)

def n_shot_list(instruction: str, n_examples: int = 5, model: str = DEFAULT_MODEL, api_key: Optional[str] = None, max_tokens: int = 1024) -> List[str]:
    """Alias for gen_examples_list"""
    return gen_examples_list(instruction=instruction, n_examples=n_examples, model=model, api_key=api_key, max_tokens=max_tokens)

def n_shot(instruction: str, n_examples: int = 5, model: str = DEFAULT_MODEL, api_key: Optional[str] = None, max_tokens: int = 1024) -> str:
    """Alias for gen_examples"""
    return gen_examples(instruction=instruction, n_examples=n_examples, model=model, api_key=api_key, max_tokens=max_tokens)

def few_shot_list(instruction: str, n_examples: int = 5, model: str = DEFAULT_MODEL, api_key: Optional[str] = None, max_tokens: int = 1024) -> List[str]:
    """Alias for gen_examples_list"""
    return gen_examples_list(instruction=instruction, n_examples=n_examples, model=model, api_key=api_key, max_tokens=max_tokens)

def few_shot(instruction: str, n_examples: int = 5, model: str = DEFAULT_MODEL, api_key: Optional[str] = None, max_tokens: int = 1024) -> str:
    """Alias for gen_examples"""
    return gen_examples(instruction=instruction, n_examples=n_examples, model=model, api_key=api_key, max_tokens=max_tokens)

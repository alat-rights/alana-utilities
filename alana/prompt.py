from typing import List, Dict, Optional, Union, Any
from alana.color import red, yellow
import re
import os
from anthropic import Anthropic
from anthropic.types import Message, MessageParam
from alana import globals

def get_xml_pattern(tag: str):
    if tag.count('<') > 0 or tag.count('>') > 0:
        raise ValueError("No '>' or '<' allowed in get_xml tag name!")
    return rf"<{tag}>(.*?)</{tag}>"

def get_xml(tag: str, content: str) -> List[str]:
    pattern: str = get_xml_pattern(tag=tag)
    matches: List[Any] = re.findall(pattern=pattern, string=content, flags=re.DOTALL)
    return matches

def remove_xml(tag: str = "reasoning", content: str = "") -> str:
    if tag.count('<') > 0 or tag.count('>') > 0:
        raise ValueError("No '>' or '<' allowed in get_xml tag name!")
    if content == "":
        red(var="`remove_xml`: Empty string provided as `content`.") # TODO: Improve error logging
    pattern: str = rf"<{tag}>.*?</{tag}>" # NOTE: Removed group matching, so can't use `get_xml_pattern`
    output: str = re.sub(pattern=pattern, repl="", string=content, flags=re.DOTALL)
    return output


def gen(user: Optional[str] = None, system: str = "", messages: Optional[List[MessageParam]] = None, append: bool = True, model: str = globals.DEFAULT_MODEL, api_key: Optional[str] = None, max_tokens = 1024, temperature=0.3, loud=True, **kwargs) -> str:
    if user is None and messages is None:
        raise ValueError("No prompt provided! `user` and `messages` are both None.")

    if messages is None:
        assert user is not None  # To be stricter, type(user) == str
        messages=[
            MessageParam(role="user", content=user), # type: ignore
        ]
    elif user is not None:
        assert messages is not None  # To be stricter, messages is List[MessageParam]
        messages.append(
            MessageParam(role="user", content=user)  # TODO: Check that non-alternating roles are ok (e.g. user, assistant, assistant)
        )

    output: Message = gen_msg(system=system, messages=messages, model=model, api_key=api_key, max_tokens=max_tokens, temperature=temperature, **kwargs)
    if append == True:
        messages.append(  # TODO: Check that non-alternating roles are ok (e.g. user, assistant, assistant)
            MessageParam(
                role="assistant",
                content=output.content[0].text
            )
        )
    return output.content[0].text

def gen_msg(messages: List[MessageParam], system: str = "", model: str = globals.DEFAULT_MODEL, api_key: Optional[str] = None, max_tokens = 1024, temperature=0.3, loud=True, **kwargs) -> Message:
    backend: str = globals.MODELS[globals.DEFAULT_MODEL]
    if model in globals.MODELS:
        backend = globals.MODELS[model]
    else:
        red(var=f"gen() -- Caution! model string not recognized; reverting to {globals.DEFAULT_MODEL=}.") # TODO: C'mon we can do better error logging than this

    if api_key is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
    client = Anthropic(
        api_key=api_key,
    )

    if 'stream' in kwargs:
        red(var="Streaming not supported! Disabling...")
        kwargs['stream'] = False

    message: Message = client.messages.create(  # TODO: Enable streaming support
        max_tokens=max_tokens,
        messages=messages,
        system=system,
        model=backend,
        temperature=temperature,
        **kwargs
    )
    if loud:
        yellow(var=message)

    return message

def gen_examples_list(instruction: str, n_examples: int = 5, model: str = "sonnet", api_key: Optional[str] = None, max_tokens: int = 1024, temperature=0.3, **kwargs) -> List[str]:
    system: str = globals.SYSTEM["few_shot"].format(n_examples=n_examples)
    user: str = globals.USER["few_shot"].format(instruction=instruction)
    if n_examples < 1:
        red(var="Too few examples provided! Trying anyway...")

    model_output: str = gen(user=user, system=system, model=model, api_key=api_key, max_tokens=max_tokens, temperature=temperature, **kwargs)
    return get_xml(tag='example', content=model_output)

def gen_examples(instruction: str, n_examples: int = 5, model: str = globals.DEFAULT_MODEL, api_key: Optional[str] = None, max_tokens: int = 1024, temperature=0.3, **kwargs) -> str:
    examples: List[str] = gen_examples_list(instruction=instruction, n_examples=n_examples, model=model, api_key=api_key, max_tokens=max_tokens, temperature=temperature, **kwargs)
    formatted_examples: str = "\n<examples>\n<example>" + '</example>\n<example>'.join(examples) + "</example>\n</examples>"
    return formatted_examples

def gen_prompt(instruction: str, model: str = globals.DEFAULT_MODEL, api_key: Optional[str] = None, max_tokens: int = 1024, temperature=0.3, **kwargs) -> Dict[str, Union[str, List]]:
    meta_system_prompt: str = globals.SYSTEM["gen_prompt"]
    meta_prompt: str = globals.USER["gen_prompt"].format(instruction=instruction)

    full_output: str = gen(user=meta_prompt, system=meta_system_prompt, model=model, api_key=api_key, max_tokens=max_tokens, temperature=temperature, **kwargs)
    system_prompt: Union[List[str], str] = get_xml(tag="system_prompt", content=full_output)
    if len(system_prompt) >= 1:
        system_prompt = system_prompt[0]
    user_prompt: Union[List[str], str] = get_xml(tag="user_prompt", content=full_output)
    if len(user_prompt) == 1:
        user_prompt = user_prompt[0]
    return {"system": system_prompt, "user": user_prompt, "full": full_output}

def pretty_print(var: Any, loud: bool = True, model: str = "sonnet") -> str:
    system = globals.SYSTEM["pretty_print"]
    user = globals.USER["pretty_print"].format(var=f'{var}')

    string: str = gen(user=user, system=system, model=model)
    pretty: Union[List[str], str] = get_xml(tag="pretty", content=string)
    if len(pretty) == 0:
        raise ValueError("`pretty_print`: XML parsing error! Number of <pretty/> tags is 0.")
    else:
        pretty = pretty[-1]
    if loud:
        print(pretty)
    return pretty

# Aliases!
def grab(tag: str, content: str) -> List[str]:
    """Alias for get_xml"""
    return get_xml(tag=tag, content=content)

def xml(tag: str, content: str) -> List[str]:
    """Alias for get_xml"""
    return get_xml(tag=tag, content=content)

def rm_xml(tag: str, content: str) -> str:
    """Alias for remove_xml"""
    return rm_xml(tag=tag, content=content)

def n_shot_list(instruction: str, n_examples: int = 5, model: str = globals.DEFAULT_MODEL, api_key: Optional[str] = None, max_tokens: int = 1024, temperature=0.3, **kwargs) -> List[str]:
    """Alias for gen_examples_list"""
    return gen_examples_list(instruction=instruction, n_examples=n_examples, model=model, api_key=api_key, max_tokens=max_tokens, temperature=temperature, **kwargs)

def n_shot(instruction: str, n_examples: int = 5, model: str = globals.DEFAULT_MODEL, api_key: Optional[str] = None, max_tokens: int = 1024, temperature=0.3, **kwargs) -> str:
    """Alias for gen_examples"""
    return gen_examples(instruction=instruction, n_examples=n_examples, model=model, api_key=api_key, max_tokens=max_tokens, temperature=temperature, **kwargs)

def few_shot_list(instruction: str, n_examples: int = 5, model: str = globals.DEFAULT_MODEL, api_key: Optional[str] = None, max_tokens: int = 1024, temperature=0.3, **kwargs) -> List[str]:
    """Alias for gen_examples_list"""
    return gen_examples_list(instruction=instruction, n_examples=n_examples, model=model, api_key=api_key, max_tokens=max_tokens, temperature=temperature, **kwargs)

def few_shot(instruction: str, n_examples: int = 5, model: str = globals.DEFAULT_MODEL, api_key: Optional[str] = None, max_tokens: int = 1024, temperature=0.3, **kwargs) -> str:
    """Alias for gen_examples"""
    return gen_examples(instruction=instruction, n_examples=n_examples, model=model, api_key=api_key, max_tokens=max_tokens, temperature=temperature, **kwargs)

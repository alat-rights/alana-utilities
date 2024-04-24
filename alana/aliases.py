from typing import Optional, List, Any

from alana import get_xml, gen_examples_list, gen_examples, remove_xml
from alana import globals


def grab(tag: str, content: str) -> List[str]:
    """Alias for get_xml"""
    return get_xml(tag=tag, content=content)


def xml(tag: str, content: str) -> List[str]:
    """Alias for get_xml"""
    return get_xml(tag=tag, content=content)


def rm_xml(tag: str, content: str) -> str:
    """Alias for remove_xml"""
    return remove_xml(tag=tag, content=content)


def n_shot_list(
    instruction: str,
    n_examples: int = 5,
    model: str = globals.DEFAULT_MODEL,
    api_key: Optional[str] = None,
    max_tokens: int = 1024,
    temperature=1.0,
    **kwargs: Any
) -> List[str]:
    """Alias for gen_examples_list"""
    return gen_examples_list(
        instruction=instruction,
        n_examples=n_examples,
        model=model,
        api_key=api_key,
        max_tokens=max_tokens,
        temperature=temperature,
        **kwargs
    )


def n_shot(
    instruction: str,
    n_examples: int = 5,
    model: str = globals.DEFAULT_MODEL,
    api_key: Optional[str] = None,
    max_tokens: int = 1024,
    temperature=1.0,
    **kwargs: Any
) -> str:
    """Alias for gen_examples"""
    return gen_examples(
        instruction=instruction,
        n_examples=n_examples,
        model=model,
        api_key=api_key,
        max_tokens=max_tokens,
        temperature=temperature,
        **kwargs
    )


def few_shot_list(
    instruction: str,
    n_examples: int = 5,
    model: str = globals.DEFAULT_MODEL,
    api_key: Optional[str] = None,
    max_tokens: int = 1024,
    temperature=1.0,
    **kwargs: Any
) -> List[str]:
    """Alias for gen_examples_list"""
    return gen_examples_list(
        instruction=instruction,
        n_examples=n_examples,
        model=model,
        api_key=api_key,
        max_tokens=max_tokens,
        temperature=temperature,
        **kwargs
    )


def few_shot(
    instruction: str,
    n_examples: int = 5,
    model: str = globals.DEFAULT_MODEL,
    api_key: Optional[str] = None,
    max_tokens: int = 1024,
    temperature=1.0,
    **kwargs: Any
) -> str:
    """Alias for gen_examples"""
    return gen_examples(
        instruction=instruction,
        n_examples=n_examples,
        model=model,
        api_key=api_key,
        max_tokens=max_tokens,
        temperature=temperature,
        **kwargs
    )

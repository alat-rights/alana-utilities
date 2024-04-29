from anthropic import AsyncAnthropic
import os
from alana import yellow, red
from alana import globals
from alana.prompt import get_xml, _append_assistant_message, _construct_messages
from typing import List, Dict, Literal, Union, Optional, Callable, Any
from anthropic.types import Message, MessageParam

client = AsyncAnthropic(
    # This is the default and can be omitted
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)


async def agen_msg(
    messages: Optional[List[MessageParam]] = None,
    user: Optional[str] = None,
    system: str = "",
    model: str = globals.DEFAULT_MODEL,
    api_key: Optional[str] = None,
    max_tokens=1024,
    temperature=1.0,
    stream_action: Optional[Callable] = lambda x: print(x, end="", flush=True),
    loud=False,
    **kwargs: Any,
):
    """Experimental. Async version of gen_msg. Invoke with `asyncio.run(agen_msg)`"""
    constructed_messages: List[MessageParam] = _construct_messages(
        user_message=user, messages=messages
    )

    backend: str = globals.MODELS[globals.DEFAULT_MODEL]
    if model in globals.MODELS:
        backend = globals.MODELS[model]
    else:
        red(
            var=f"agen_msg() -- Caution! model string not recognized; reverting to {globals.DEFAULT_MODEL=}."
        )  # TODO: C'mon we can do better error logging than this

    if (
        api_key is None
    ):  # TODO: Factor out the auth stuff into a helper fn., for both gen_msg and async_gen_msg
        api_key = os.environ.get("ANTHROPIC_API_KEY")
    client = AsyncAnthropic(
        api_key=api_key,
    )

    if not stream_action:
        message: Message = (
            await client.messages.create(  # TODO: Enable streaming support
                max_tokens=max_tokens,
                messages=constructed_messages,
                system=system,
                model=backend,
                temperature=temperature,
                **kwargs,
            )
        )
    else:
        async with client.messages.stream(
            max_tokens=max_tokens,
            messages=constructed_messages,
            system=system,
            model=backend,
            temperature=temperature,
            **kwargs,
        ) as s:
            async for text in s.text_stream:
                stream_action(text)
        message = await s.get_final_message()

    if loud:
        yellow(message)

    return message


async def agen(
    user: Optional[str] = None,
    system: str = "",
    messages: Optional[List[MessageParam]] = None,
    append: bool = True,
    model: str = globals.DEFAULT_MODEL,
    api_key: Optional[str] = None,
    max_tokens=1024,
    temperature=1.0,
    stream_action: Optional[Callable] = lambda x: print(x, end="", flush=True),
    loud=False,
    **kwargs: Any,
) -> str:
    """Experimental. Async version of gen. Invoke with `asyncio.run(agen)`"""
    constructed_messages: List[MessageParam] = _construct_messages(
        user_message=user, messages=messages
    )
    output: Message = await agen_msg(
        system=system,
        messages=constructed_messages,
        model=model,
        api_key=api_key,
        max_tokens=max_tokens,
        stream_action=stream_action,
        loud=loud,
        temperature=temperature,
        **kwargs,
    )
    if append == True:
        _append_assistant_message(messages=constructed_messages, output=output)
    return output.content[0].text


async def agen_examples_list(
    instruction: str,
    n_examples: int = 5,
    model: str = globals.DEFAULT_MODEL,
    api_key: Optional[str] = None,
    max_tokens: int = 1024,
    temperature=1.0,
    **kwargs: Any,
) -> List[str]:
    """Uses Claude to generate a Python list of few-shot examples for a given natural language instruction.

    Args:
        instruction (str): The natural language instruction for which to generate examples.
        n_examples (int, optional): The number of examples to ask Claude to generate. Defaults to 5.
        model (str, optional): The name of the model to use. Defaults to `globals.DEFAULT_MODEL`.
        api_key (Optional[str], optional): The API key to use for authentication. Defaults to None.
        max_tokens (int, optional): The maximum number of tokens to generate in the response. Defaults to 1024.
        temperature (float, optional): The temperature value for controlling the randomness of the generated response.
        **kwargs: Additional keyword arguments to pass to the `gen` function (`gen` passes kwargs to the Anthropic API).

    Returns:
        List[str]: A Python list of generated few-shot examples.

    Notes:
        - The function constructs a system message using the `globals.SYSTEM["few_shot"]` template and the provided `n_examples`.
        - The function constructs a user message using the `globals.USER["few_shot"]` template and the provided `instruction`.
        - If `n_examples` is less than 1, the function prints a warning message using the `red` function but continues execution.
        - The function calls the `gen` function to generate the model's output based on the constructed system and user messages, along with the specified `model`, `api_key`, `max_tokens`, `temperature`, and any additional keyword arguments.
        - The generated model output is expected to be in XML format, with each example enclosed in `<example/>` tags.
        - The function uses the `get_xml` function to extract the content within the `<example/>` tags and returns it as a Python list of strings.

    Example:
        >>> instruction = "Write a short story about a magical adventure."
        >>> examples = gen_examples_list(instruction, n_examples=3)
        >>> print(examples)
        [
            "Once upon a time, in a land far away, there was a young girl named Lily who discovered a mysterious portal in her backyard...",
            "In a world where magic was a part of everyday life, a brave knight named Eldric embarked on a quest to retrieve a powerful artifact...",
            "Deep in the enchanted forest, a group of talking animals gathered around a wise old oak tree to discuss a pressing matter..."
        ]
    """
    system: str = globals.SYSTEM["few_shot"].format(n_examples=n_examples)
    user: str = globals.USER["few_shot"].format(instruction=instruction)
    if n_examples < 1:
        red(var="Too few examples requested! Trying anyway...")

    model_output: str = await agen(
        user=user,
        system=system,
        model=model,
        api_key=api_key,
        max_tokens=max_tokens,
        temperature=temperature,
        **kwargs,
    )
    return get_xml(tag="example", content=model_output)


async def agen_examples(
    instruction: str,
    n_examples: int = 5,
    model: str = globals.DEFAULT_MODEL,
    api_key: Optional[str] = None,
    max_tokens: int = 1024,
    temperature=1.0,
    **kwargs: Any,
) -> str:
    """Generate a formatted string containing few-shot examples for a given natural language instruction. Uses `gen_examples_list`.

    Args:
        instruction (str): The natural language instruction for which to generate examples.
        n_examples (int, optional): The number of examples to generate. Defaults to 5.
        model (str, optional): The name of the model to use. Defaults to globals.DEFAULT_MODEL.
        api_key (Optional[str], optional): The API key to use for authentication. Defaults to None.
        max_tokens (int, optional): The maximum number of tokens to generate in the response. Defaults to 1024.
        temperature (float, optional): The temperature value for controlling the randomness of the generated response.
        **kwargs: Additional keyword arguments to pass to the `gen_examples_list` function (passed to Anthropic API).

    Returns:
        str: A formatted string containing the generated few-shot examples, enclosed in XML-like tags.

    Notes:
        - The function calls the `gen_examples_list` function to generate a list of few-shot examples based on the provided `instruction`, `n_examples`, `model`, `api_key`, `max_tokens`, `temperature`, and any additional keyword arguments.
        - The generated examples are then formatted into a string, with each example enclosed in `<example/>` tags.
        - The formatted string starts with an opening `<examples>` tag and ends with a closing `</examples>` tag (note plural).

    Example:
        >>> instruction = "Write a short story about a magical adventure."
        >>> examples_str = gen_examples(instruction, n_examples=3)
        >>> print(examples_str)
        <examples>
        <example>Once upon a time, in a land far away, there was a young girl named Lily who discovered a mysterious portal in her backyard...</example>
        <example>In a world where magic was a part of everyday life, a brave knight named Eldric embarked on a quest to retrieve a powerful artifact...</example>
        <example>Deep in the enchanted forest, a group of talking animals gathered around a wise old oak tree to discuss a pressing matter...</example>
        </examples>
    """
    examples: List[str] = await agen_examples_list(
        instruction=instruction,
        n_examples=n_examples,
        model=model,
        api_key=api_key,
        max_tokens=max_tokens,
        temperature=temperature,
        **kwargs,
    )
    formatted_examples: str = (
        "\n<examples>\n<example>"
        + "</example>\n<example>".join(examples)
        + "</example>\n</examples>"
    )
    return formatted_examples


async def agen_prompt(
    instruction: str,
    messages: Optional[List[MessageParam]] = None,
    model: str = globals.DEFAULT_MODEL,
    api_key: Optional[str] = None,
    max_tokens: int = 1024,
    temperature=1.0,
    **kwargs: Any,
) -> Dict[Literal["system", "user", "full"], Union[str, List]]:
    """Meta-prompter! Generate a prompt given an arbitrary instruction.

    Args:
        instruction (str): The arbitrary instruction for which to generate a prompt.
        messages (Optional[List[MessageParam]]): !!!!EXPERIMENTAL!!!! A list wherein to receive a 2-turn prompt generation thread! STRONGLY RECOMMEND TO BE EMPTY.
        model (str, optional): The name of the model to use. Defaults to globals.DEFAULT_MODEL.
        api_key (Optional[str], optional): The API key to use for authentication. Defaults to None.
        max_tokens (int, optional): The maximum number of tokens to generate in the response. Defaults to 1024.
        temperature (float, optional): The temperature value for controlling the randomness of the generated response.
        **kwargs: Additional keyword arguments to pass to the `gen` function.

    Returns:
        Dict[Literal["system", "user", "full"], Union[str, List]]: A dictionary containing the generated prompts.
            - "system" (Union[str, List[str]]): The generated system prompt(s).
            - "user" (Union[str, List[str]]): The generated user prompt(s).
            - "full" (str): The full generated output, including both system and user prompts.

    Notes:
        - The function constructs a meta-system prompt using the `globals.SYSTEM["gen_prompt"]` template.
        - The function constructs a meta-prompt using the `globals.USER["gen_prompt"]` template and the provided `instruction`.
        - The function calls the `gen` function to generate the full output based on the meta-system prompt, meta-prompt, `model`, `api_key`, `max_tokens`, `temperature`, and any additional keyword arguments (which are passed to the Anthropic API).
        - The function uses the `get_xml` function to extract the content within the `<system_prompt/>` and `<user_prompt/>` tags from the full output.
        - The function returns a dictionary containing the generated system prompt(s), user prompt(s), and the full output.
        - Things can get janky if the model tries to provide multiple system prompts or multiple user prompts. I make some wild guess about what you might want to get in that case (right now, it would return the first system prompt, but all the user prompts in a list).

    Example:
        >>> instruction = "Write a story about a robot learning to love."
        >>> prompts = gen_prompt(instruction)
        >>> print(prompts["system"])
        You are a creative story writer. Write a short story based on the given prompt, focusing on character development and emotional depth.
        >>> print(prompts["user"])
        Write a story about a robot learning to love.
        >>> print(prompts["full"])
        <system_prompt>
        You are a creative story writer. Write a short story based on the given prompt, focusing on character development and emotional depth.
        </system_prompt>

        <user_prompt>
        Write a story about a robot learning to love.
        </user_prompt>
    """
    meta_system_prompt: str = globals.SYSTEM["gen_prompt"]
    meta_prompt: str = globals.USER["gen_prompt"].format(instruction=instruction)

    if messages is not None:
        yellow(
            var="`alana.prompt.gen_prompt`: Please note that `messages` support in `gen_prompt` is experimental!"
        )
    if messages is not None and len(messages) > 0:
        red(
            "`alana.prompt.gen_prompt`: Non-empty `messages` received! In `gen_prompt`, it's STRONGLY recommended to pass in an empty list for `messages`."
        )

    full_output: str = (
        await agen(
            user=meta_prompt,
            messages=messages,
            system=meta_system_prompt,
            model=model,
            api_key=api_key,
            max_tokens=max_tokens,
            temperature=temperature,
            stop_sequences=[
                "</user_prompt>",
            ],
            **kwargs,
        )
        + "</user_prompt>"
    )
    system_prompt: Union[List[str], str] = get_xml(
        tag="system_prompt", content=full_output
    )
    if len(system_prompt) >= 1:
        system_prompt = system_prompt[0]
    user_prompt: Union[List[str], str] = get_xml(tag="user_prompt", content=full_output)
    if (
        len(user_prompt) == 1
    ):  # TODO: Find a saner way to handle this. E.g. delegate to a formatter model.
        user_prompt = user_prompt[0]
    return {"system": system_prompt, "user": user_prompt, "full": full_output}

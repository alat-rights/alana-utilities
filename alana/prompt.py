import re
import os
from typing import List, Dict, Optional, Union, Literal, Any
from anthropic import Anthropic
from anthropic.types import Message, MessageParam

from alana.color import red, yellow
from alana import globals

"""
class RequestParams(TypedDict, total=False):
    metadata: Metadata | NotGiven
    stop_sequences: List[str] | NotGiven
    stream: Literal[False] | Literal[True] | NotGiven
    top_k: int | NotGiven
    top_p: float | NotGiven
    extra_headers: Headers | None
    extra_query: Query | None
    extra_body: Body | None
    timeout: float | Union[Optional[float], Tuple[Optional[float], Optional[float], Optional[float], Optional[float]]] | None | NotGiven
"""


def get_xml_pattern(tag: str):
    """Return regex pattern for getting contents of <tag/> XML tags."""
    if tag.count("<") > 0 or tag.count(">") > 0:
        raise ValueError("No '>' or '<' allowed in get_xml tag name!")
    return rf"<{tag}>(.*?)</{tag}>"


def get_xml(tag: str, content: str) -> List[str]:
    """Return contents of <tag/> XML tags."""
    pattern: str = get_xml_pattern(tag=tag)
    matches: List[Any] = re.findall(pattern=pattern, string=content, flags=re.DOTALL)
    return matches


def remove_xml(tag: str = "reasoning", content: str = "", repl: str = "") -> str:
    """Return a copy of `content` with <tag/> XML elements (both content and tag) replaced with `repl` (default "")."""
    if tag.count("<") > 0 or tag.count(">") > 0:
        raise ValueError("No '>' or '<' allowed in get_xml tag name!")
    if content == "":
        red(
            var="`remove_xml`: Empty string provided as `content`."
        )  # TODO: Improve error logging
    pattern: str = (
        rf"<{tag}>.*?</{tag}>"  # NOTE: Removed group matching, so can't use `get_xml_pattern`
    )
    output: str = re.sub(pattern=pattern, repl=repl, string=content, flags=re.DOTALL)
    return output


def respond(
    content: str,
    messages: Optional[List[MessageParam]] = None,
    role: Literal["user", "assistant"] = "user",
) -> List[MessageParam]:
    """Append a user message to messages list.

    Args:
        content (str): The newest message content.
        messages (Optional[List[MessageParam]]): A list of `anthropic.types.MessageParam` objects. The last MessageParam should be from assistant. If `messages` is None, we will populate it with exactly one MessageParam based on `user`.
        role (Literal["user", "assistant"]): Corresponding source for the message!

    Returns:
        List[MessageParam]
    """
    if messages is None:
        messages = []
    messages.append(
        MessageParam(
            role=role,
            content=content,
        )
    )
    return messages


def _construct_messages(
    user_message: Optional[str], messages: Optional[List[MessageParam]]
) -> List[MessageParam]:
    if (
        user_message is not None
        and messages is not None
        and len(messages) >= 1
        and messages[-1]["role"] == "user"
    ):
        # Last message is user-message, but user_message provided
        raise ValueError(
            "`gen`: Bad request! Roles must be alternating. Last message in `messages` is from user, but `user_message` provided."
        )

    if user_message is not None:
        # user_message provided, so we must either create `messages` or append to it
        # user_message should have role "user"
        return respond(content=user_message, messages=messages, role="user")
    elif messages is None:
        # user_message is None and messages is None
        raise ValueError("No prompt provided! `user` and `messages` are both None.")
    else:
        # user_message is None, so we just return the messages we received
        return messages


def _append_assistant_message(messages, output) -> None:
    if len(output.content) == 0:
        raise ValueError(
            f"Assistant did not provide a response. Stop reason: {output.stop_reason}. Full API response: {output}"
        )

    if (
        messages[-1]["role"] == "assistant"
    ):  # NOTE: Anthropic API does not allow non-alternating roles (raises Err400). Let's enforce this.
        # NOTE: messages[-1]["content"] is assistant output, so should be `str`, since Anthropic API (as of Apr 16 2024) only supports text output!
        existing_assistant_content: str = messages[-1]["content"]
        assistant_content: str = existing_assistant_content + output.content[0].text
        messages.pop()
    else:
        assistant_content = output.content[0].text

    respond(content=assistant_content, messages=messages, role="assistant")


def gen(
    user: Optional[str] = None,
    system: str = "",
    messages: Optional[List[MessageParam]] = None,
    append: bool = True,
    model: str = globals.DEFAULT_MODEL,
    api_key: Optional[str] = None,
    max_tokens=1024,
    temperature=1.0,
    loud=True,
    **kwargs: Any,
) -> str:
    """Generate a response from Claude. Returns the text content (`str`) of Claude's response. If you want the Message object instead, use `gen_msg`.

    Args:
        user (Optional[str], optional): The user's message content. Defaults to None.
        system (str, optional): The system message for Claude. Defaults to "".
        messages (Optional[List[MessageParam]], optional): A list of `anthropic.types.MessageParam`. Defaults to None.
        append (bool, optional): Whether to append the generated response (as an `anthropic.types.MessageParam`) to `messages`. Defaults to True.
        model (str, optional): The name of the model to use. Defaults to globals.DEFAULT_MODEL.
        api_key (Optional[str], optional): The API key to use for authentication. Defaults to None (if None, uses os.environ["ANTHROPIC_API_KEY]).
        max_tokens (int, optional): The maximum number of tokens to generate in the response. Defaults to 1024.
        temperature (float, optional): The temperature value for controlling the randomness of the generated response.
        loud (bool, optional): Whether to print verbose output. Defaults to True.
        **kwargs: Additional keyword arguments to pass to the underlying generation function.

    Raises:
        ValueError: If no prompt is provided (both `user` and `messages` are None).
        ValueError: If the last message in `messages` is from the user and `user` is also provided.
        ValueError: If Claude does not provide a response.

    Returns:
        str: The text content of Claude's generated response.

    Notes:
        - If `messages` is None, the `user` parameter must be provided as a string.
        - If `user` is provided and `messages` is not None, the `user` message is appended to the `messages` list.
        - The function raises a ValueError if the roles in the `messages` list are not alternating (e.g., user, assistant, user).
        - If `append` is True and the last message in `messages` is from the assistant, the generated response is appended to the existing assistant's content.
        - The function uses the `gen_msg` function internally to generate Claude's response.

    Example:
        >>> user_message = "Hello, Claude!"
        >>> response = gen(user=user_message)
        >>> print(response)
        "Hello! How can I assist you today?"
    """

    constructed_messages: List[MessageParam] = _construct_messages(
        user_message=user, messages=messages
    )
    output: Message = gen_msg(
        system=system,
        messages=constructed_messages,
        model=model,
        api_key=api_key,
        max_tokens=max_tokens,
        loud=loud,
        temperature=temperature,
        **kwargs,
    )
    if append == True:
        _append_assistant_message(messages=constructed_messages, output=output)
    return output.content[0].text


def gen_msg(
    messages: Optional[List[MessageParam]] = None,
    user: Optional[str] = None,
    system: str = "",
    model: str = globals.DEFAULT_MODEL,
    api_key: Optional[str] = None,
    max_tokens=1024,
    temperature=1.0,
    loud=True,
    **kwargs: Any,
) -> Message:
    """Generate a response from Claude using the Anthropic API.

    Args:
        messages (List[MessageParam], optional): A list of `anthropic.types.MessageParam`s representing the conversation history.
        user (str, optional): Instead of passing a `messages`, you can pass in a single user prompt.
        system (str, optional): The system message to set the context for Claude. Defaults to "".
        model (str, optional): The name of the model to use. Defaults to globals.DEFAULT_MODEL.
        api_key (Optional[str], optional): The API key to use for authentication. Defaults to None.
        max_tokens (int, optional): The maximum number of tokens to generate in the response. Defaults to 1024.
        temperature (float, optional): The temperature value for controlling the randomness of the generated response.
        loud (bool, optional): Whether to print verbose output. Defaults to True.
        **kwargs: Additional keyword arguments to pass to the Anthropic API.

    Returns:
        Message: The Message object produced by the Anthropic API, containing the generated response.

    Notes:
        - If the `model` parameter is not recognized, the function reverts to using the default model specified in `globals.DEFAULT_MODEL`.
        - If `api_key` is None, the function attempts to retrieve the API key from the environment variable "ANTHROPIC_API_KEY".
        - The function creates an instance of the Anthropic client using the provided `api_key`.
        - Stream not supported yet! If the `stream` keyword argument is provided, the function disables streaming and sets `stream` to False. (TODO: Support stream)
        - The function uses the `messages.create` method of the Anthropic client to generate Claude's response.
        - If `loud` is True, the generated message is printed using the `yellow` function for verbose output.

    Example:
        >>> messages = [
        ...     MessageParam(role="user", content="What is the capital of France?")
        ... ]
        >>> response = gen_msg(messages, system="You are a helpful assistant.")
        >>> print(response.content[0].text)
        The capital of France is Paris.
    """
    constructed_messages: List[MessageParam] = _construct_messages(
        user_message=user, messages=messages
    )

    backend: str = globals.MODELS[globals.DEFAULT_MODEL]
    if model in globals.MODELS:
        backend = globals.MODELS[model]
    else:
        red(
            var=f"gen() -- Caution! model string not recognized; reverting to {globals.DEFAULT_MODEL=}."
        )  # TODO: C'mon we can do better error logging than this

    if api_key is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
    client = Anthropic(
        api_key=api_key,
    )

    if "stream" in kwargs:
        red(var="Streaming not supported! Disabling...")
        kwargs["stream"] = False

    message: Message = client.messages.create(  # TODO: Enable streaming support
        max_tokens=max_tokens,
        messages=constructed_messages,
        system=system,
        model=backend,
        temperature=temperature,
        **kwargs,
    )
    if loud:
        yellow(var=message)

    return message


def gen_examples_list(
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

    model_output: str = gen(
        user=user,
        system=system,
        model=model,
        api_key=api_key,
        max_tokens=max_tokens,
        temperature=temperature,
        **kwargs,
    )
    return get_xml(tag="example", content=model_output)


def gen_examples(
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
    examples: List[str] = gen_examples_list(
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


def gen_prompt(
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
        gen(
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


def pretty_print(
    var: Any, loud: bool = True, model: str = "sonnet", **kwargs: Any
) -> str:
    """Pretty-print an arbitrary variable. By default, uses Sonnet (not globals.DEFAULT_MODEL).

    Args:
        var (Any): The variable to pretty-print.
        loud (bool, optional): Whether to print the pretty-printed output. Defaults to True.
        model (str, optional): The name of the model to use. Defaults to "sonnet".

    Returns:
        str: The pretty-printed representation of the variable.

    Raises:
        ValueError: If no <pretty/> tags are found in the generated output.

    Notes:
        - The function constructs a system prompt using the `globals.SYSTEM["pretty_print"]` template.
        - The function constructs a user prompt using the `globals.USER["pretty_print"]` template and the provided `var`.
        - The function calls the `gen` function to generate the pretty-printed output based on the system prompt, user prompt, and specified `model`.
        - The function uses the `get_xml` function to extract the content within the `<pretty>` tags from the generated output.
        - If no `<pretty/>` tags are found in the model output, the function raises a `ValueError`.
        - If multiple `<pretty>` tags are found in the model output, the function uses the last one as the pretty-printed output.
        - The function returns the pretty-printed output as a string.

    Example:
        >>> my_var = {"name": "John", "age": 30, "city": "New York"}
        >>> pretty_output = pretty_print(my_var)
        {
            "name": "John",
            "age": 30,
            "city": "New York"
        }
        >>> print(pretty_output)
        {
            "name": "John",
            "age": 30,
            "city": "New York"
        }
    """
    system = globals.SYSTEM["pretty_print"]
    user = globals.USER["pretty_print"].format(var=f"{var}")

    string: str = gen(
        user=user, system=system, model=model, loud=False, **kwargs
    )  # NOTE: We just don't log pretty print model outputs
    pretty: Union[List[str], str] = get_xml(tag="pretty", content=string)
    if len(pretty) == 0:
        raise ValueError(
            "`pretty_print`: XML parsing error! Number of <pretty/> tags is 0."
        )
    else:
        pretty = pretty[-1]
    if loud:
        print(pretty)
    return pretty

from anthropic import AsyncAnthropic
import os
from alana import yellow, red
from alana import globals
from alana.prompt import _append_assistant_message, _construct_messages
from typing import List, Optional, Callable, Any
from anthropic.types import Message, MessageParam

client = AsyncAnthropic(
    # This is the default and can be omitted
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)


async def agen_msg(
    messages: List[MessageParam],
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
    backend: str = globals.MODELS[globals.DEFAULT_MODEL]
    if model in globals.MODELS:
        backend = globals.MODELS[model]
    else:
        red(
            var=f"gen() -- Caution! model string not recognized; reverting to {globals.DEFAULT_MODEL=}."
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
                messages=messages,
                system=system,
                model=backend,
                temperature=temperature,
                **kwargs,
            )
        )
    else:
        async with client.messages.stream(
            max_tokens=max_tokens,
            messages=messages,
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


async def agen(user: Optional[str] = None, system: str = "", messages: Optional[List[MessageParam]] = None, append: bool = True, model: str = globals.DEFAULT_MODEL, api_key: Optional[str] = None, max_tokens=1024, temperature=1.0, stream_action: Optional[Callable] = lambda x: print(x, end="", flush=True), loud=False, **kwargs: Any) -> str:  # type: ignore
    """Experimental. Async version of gen. Invoke with `asyncio.run(agen)`"""
    messages: List[MessageParam] = _construct_messages(
        user_message=user, messages=messages
    )
    output: Message = await agen_msg(
        system=system,
        messages=messages,
        model=model,
        api_key=api_key,
        max_tokens=max_tokens,
        stream_action=stream_action,
        loud=loud,
        temperature=temperature,
        **kwargs,
    )
    if append == True:
        _append_assistant_message(messages=messages, output=output)
    return output.content[0].text

"""
`alana` includes five components:
    - color
    - prompt
    - (experimental) prompt_async
    - globals
    - aliases

`color` is a simple utilities library that provides color print using colorama.Fore.
`prompt` is the meat of `alana`, including functions for interacting with Anthropic.
(experimental) `prompt_async` uses AsyncAnthropic. Supports features like streaming.
`globals` contains model names and prompts.
`aliases` include alternate names for common functions.
"""

from alana.color import (
    red,
    blue,
    green,
    yellow,
    cyan,
    pink,
    heatmap,
    scatter,
    data_atlas,
)
from alana.prompt import (
    get_xml,
    get_xml_pattern,
    gen_examples,
    gen_examples_list,
    gen,
    gen_prompt,
    pretty_print,
    remove_xml,
    gen_msg,
    respond,
)
from alana.prompt_async import (
    agen,
    agen_msg,
    agen_examples,
    agen_examples_list,
    agen_prompt,
)
from alana.aliases import (
    grab,
    xml,
    n_shot_list,
    n_shot,
    few_shot_list,
    few_shot,
    rm_xml,
)
import alana.globals
import alana.color
import alana.prompt

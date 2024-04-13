from colorama import Fore, Style
from typing import Any, Optional
import logging

# A hacky utils library I put together for myself to write code faster. Please don't judge!
# Feedback always welcome.

# Debugging and logging!
def log(loud: bool, output: str, logger: Optional[logging.Logger] = None) -> None:
    if loud:
        print(output)
    if logger:
        logger.info(output)

def red(var: Any, loud: bool = True, logger: Optional[logging.Logger] = None) -> str:
    output = f"{Fore.RED} {var} {Style.RESET_ALL}"
    log(loud, output, logger)
    return output

def green(var: Any, loud: bool = True, logger: Optional[logging.Logger] = None) -> str:
    output = f"{Fore.GREEN} {var} {Style.RESET_ALL}"
    log(loud, output, logger)
    return output

def blue(var: Any, loud: bool = True, logger: Optional[logging.Logger] = None) -> str:
    output = f"{Fore.BLUE} {var} {Style.RESET_ALL}"
    log(loud, output, logger)
    return output

def yellow(var: Any, loud: bool = True, logger: Optional[logging.Logger] = None) -> str:
    output = f"{Fore.YELLOW} {var} {Style.RESET_ALL}"
    log(loud, output, logger)
    return output

def cyan(var: Any, loud: bool = True, logger: Optional[logging.Logger] = None) -> str:
    output = f"{Fore.CYAN} {var} {Style.RESET_ALL}"
    log(loud, output, logger)
    return output

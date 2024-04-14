from colorama import Fore, Style
from typing import Any, Optional
import logging

# A hacky utils library I put together for myself to write code faster. Please don't judge!
# Feedback always welcome.

# Debugging and logging!
def log(loud: bool, output: str, logger: Optional[logging.Logger] = None) -> None:
    """
    Log the output based on the provided parameters.

    Args:
        loud (bool): If True, print the output to the console.
        output (str): The string to be logged.
        logger (Optional[logging.Logger], optional): The logger to be used for logging.
            If provided, the output will be logged using this logger. Defaults to None.
    """
    if loud:
        print(output)
    if logger:
        logger.info(output)

def red(var: Any, loud: bool = True, logger: Optional[logging.Logger] = None) -> str:
    """Print var in red, like `alana.blue`"""
    output = f"{Fore.RED} {var} {Style.RESET_ALL}"
    log(loud, output, logger)
    return output

def green(var: Any, loud: bool = True, logger: Optional[logging.Logger] = None) -> str:
    """Print var in green, like `alana.blue`"""
    output = f"{Fore.GREEN} {var} {Style.RESET_ALL}"
    log(loud, output, logger)
    return output

def blue(var: Any, loud: bool = True, logger: Optional[logging.Logger] = None) -> str:
    """
    Print the given variable in blue color using colorama and return the colored string.

    Args:
        var (Any): The variable to be printed in red color.
        loud (bool, optional): If True, print the colored output to the console. Defaults to True.
        logger (Optional[logging.Logger], optional): The logger to be used for logging.
            If provided, the colored output will be logged using this logger. Defaults to None.

    Returns:
        str: The input variable formatted as a red-colored string.
    """
    output = f"{Fore.BLUE} {var} {Style.RESET_ALL}"
    log(loud, output, logger)
    return output

def yellow(var: Any, loud: bool = True, logger: Optional[logging.Logger] = None) -> str:
    """Print var in yellow, like `alana.blue`"""
    output = f"{Fore.YELLOW} {var} {Style.RESET_ALL}"
    log(loud, output, logger)
    return output

def cyan(var: Any, loud: bool = True, logger: Optional[logging.Logger] = None) -> str:
    """Print var in cyan, like `alana.blue`"""
    output = f"{Fore.CYAN} {var} {Style.RESET_ALL}"
    log(loud, output, logger)
    return output

def pink(var: Any, loud: bool = True, logger: Optional[logging.Logger] = None) -> str:
    """Print var in pink, like `alana.blue`"""
    output = f"{Fore.MAGENTA} {var} {Style.RESET_ALL}"
    log(loud, output, logger)
    return output

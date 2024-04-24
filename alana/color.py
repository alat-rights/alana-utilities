from colorama import Fore, Style
from typing import Any, Optional
import logging
import numpy as np

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


def _gen_figname(title: str) -> str:
    import random

    id = random.randint(1000, 10000)
    return title + "_" + str(object=id)


def heatmap(array: np.ndarray, title: Optional[str] = None, save: bool = False) -> None:
    import matplotlib.pyplot as plt

    plt.figure(figsize=(8, 8))
    plt.imshow(X=array, cmap="viridis", interpolation="nearest")
    plt.colorbar(label="Value")
    if title is None:
        title = "heatmap"
    plt.title(label=title)
    if save:
        name: str = _gen_figname(title=title)
        plt.savefig(name)


def scatter(
    x: np.ndarray,
    y: np.ndarray,
    x_label: str = "X",
    y_label: str = "Y",
    title: Optional[str] = None,
    save: bool = False,
) -> None:
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    if not title:
        title = f"Scatterplot of {y_label} over {x_label}"
    ax.set_title(label=title)
    if save:
        name = _gen_figname(title=title)
        plt.savefig(name)


# def gen_interactive_plot_dangerous(inputs = ) -> None:


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

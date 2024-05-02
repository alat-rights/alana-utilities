import os
from typing import Any, List, Dict, Optional
import logging
from colorama import Fore, Style
import numpy as np
from plotly.graph_objs._figure import Figure
from scipy.sparse._matrix import spmatrix

# Hacky utils. Lower standard of quality than the `prompt` module.
# Designed for quickly iterating in Colab.


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
        logger.info(msg=output)


def _make_filename(title: str, extension: str) -> str:
    filename = f"{title}.{extension}"
    counter = 1
    # Check if the file exists and update the filename if necessary
    while os.path.exists(path=filename):
        filename: str = f"{title}_{counter}.{extension}"
        counter += 1
    return filename


def heatmap(array: np.ndarray, title: Optional[str] = None, save: bool = False) -> None:
    import plotly.express as px

    if title is None:
        title = "heatmap"
    fig: Figure = px.imshow(
        img=array,
        labels=dict(x="Column", y="Row", color="Value"),
        x=np.arange(array.shape[1]),
        y=np.arange(array.shape[0]),
        color_continuous_scale="Viridis",
        title=title,
    )
    if save:
        filename = _make_filename(title, ".png")
        fig.write_image(filename)
    fig.show()


def scatter(
    x: np.ndarray,
    y: np.ndarray,
    x_label: str = "X",
    y_label: str = "Y",
    title: Optional[str] = None,
    save: bool = False,
) -> None:
    import plotly.express as px

    if title is None:
        title = f"Scatterplot of {y_label} over {x_label}"
    fig: Figure = px.scatter(x=x, y=y, labels={"x": x_label, "y": y_label}, title=title)
    if save:
        filename: str = _make_filename(title=title, extension=".png")
        fig.write_image(filename)
    fig.show()


def data_atlas(
    strings: List[str],
    color_data: Optional[List[Any]] = None,
    color_data_name: str = "color",
    variable_size=True,
    hover_data: Optional[Dict[str, List[Any]]] = None,
):
    """Mostly written by ChatGPT, but hey it works!"""
    import plotly.express as px
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.manifold import TSNE

    # Vectorization using TF-IDF
    vectorizer = TfidfVectorizer(stop_words="english")
    X: spmatrix = vectorizer.fit_transform(raw_documents=strings)

    # Dimensionality Reduction using t-SNE
    perplexity_value: float = max(
        len(strings) / 3, 5
    )  # Ensuring a minimum perplexity of 5
    tsne = TSNE(
        n_components=2, random_state=42, perplexity=perplexity_value, n_iter=1000
    )
    embedding = tsne.fit_transform(X.toarray())  # type: ignore https://docs.scipy.org/doc//scipy-1.3.1/reference/generated/scipy.sparse.spmatrix.toarray.html

    # Plotting the result using Plotly
    fig: Figure = px.scatter(
        x=embedding[:, 0],
        y=embedding[:, 1],
        hover_name=strings,
        size=(
            color_data if variable_size else None
        ),  # Visualizing the size by confidence scores
        color=color_data,  # Coloring points by confidence scores
        hover_data=hover_data,
        labels={
            "x": "t-SNE Dimension 1",
            "y": "t-SNE Dimension 2",
            "color": color_data_name,
        },
        title=f"t-SNE Projection of Data ({perplexity_value=})",
        color_continuous_scale=px.colors.diverging.Tealrose,  # Using a diverging color scale
        size_max=15,
        template="plotly_white",
    )

    fig.update_traces(
        marker=dict(line=dict(width=1, color="DarkSlateGrey"), opacity=0.8)
    )

    fig.update_layout(
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Rockwell"),
        title_font=dict(size=20, family="Helvetica", color="grey"),
        margin=dict(l=10, r=10, t=50, b=10),
        coloraxis_colorbar=dict(
            tickmode="array", tickvals=[0, 0.5, 1], ticks="outside"
        ),
    )

    fig.show()


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

"""Provide contract behavior handlers for deal."""

import functools
from collections.abc import Callable
from typing import ParamSpec, TypeVar, cast

import deal
from rich.console import Console


P = ParamSpec("P")
R = TypeVar("R")

console: Console = Console()


def full_trace(func: Callable[P, R]) -> Callable[P, R]:  # noqa: UP047
    """Print a colorized traceback using rich.

    deal swallows tracebacks from RaisesContractError.
    Attach this decorator if they're needed for debugging.
    """

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return func(*args, **kwargs)
        except deal.RaisesContractError:
            console.print_exception()
            raise

    return cast("Callable[P, R]", wrapper)

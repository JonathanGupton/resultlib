"""resultlib: a tiny, typed Result[T, E] utility."""

from .result import (
    Result,
    Ok,
    Err,
    ok,
    err,
)

__all__ = ["Result", "Ok", "Err", "ok", "err"]

__version__ = "0.1.0"

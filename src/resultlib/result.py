from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, TypeVar, Callable, NoReturn, cast

T = TypeVar("T")  # success type
E = TypeVar("E")  # error type
U = TypeVar("U")
F = TypeVar("F")

class Result(Generic[T, E]):
    def is_ok(self) -> bool: ...
    def is_err(self) -> bool: ...
    def unwrap(self) -> T: ...
    def unwrap_err(self) -> E: ...
    def map(self, f: Callable[[T], U]) -> "Result[U, E]": ...
    def map_err(self, f: Callable[[E], F]) -> "Result[T, F]": ...
    def and_then(self, f: Callable[[T], "Result[U, E]"]) -> "Result[U, E]": ...

@dataclass(frozen=True)
class Ok(Result[T, E]):
    value: T
    def is_ok(self) -> bool: return True
    def is_err(self) -> bool: return False
    def unwrap(self) -> T: return self.value
    def unwrap_err(self) -> NoReturn: raise RuntimeError("called unwrap_err on Ok")
    def map(self, f: Callable[[T], U]) -> "Result[U, E]": return Ok(f(self.value))
    def map_err(self, f: Callable[[E], F]) -> "Result[T, F]": return cast(Result[T, F], self)
    def and_then(self, f: Callable[[T], "Result[U, E]"]) -> "Result[U, E]": return f(self.value)

@dataclass(frozen=True)
class Err(Result[T, E]):
    error: E
    def is_ok(self) -> bool: return False
    def is_err(self) -> bool: return True
    def unwrap(self) -> NoReturn: raise RuntimeError(f"called unwrap on Err: {self.error}")
    def unwrap_err(self) -> E: return self.error
    def map(self, f: Callable[[T], U]) -> "Result[U, E]": return cast(Result[U, E], self)
    def map_err(self, f: Callable[[E], F]) -> "Result[T, F]": return Err(f(self.error))
    def and_then(self, f: Callable[[T], "Result[U, E]"]) -> "Result[U, E]": return cast(Result[U, E], self)

# helpers
def ok(value: T) -> Result[T, E]: return Ok(value)
def err(error: E) -> Result[T, E]: return Err(error)

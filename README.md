# resultlib

A tiny, typed `Result[T, E]` utility for Python inspired by Rust's `Result`. Zero runtime dependencies.

## Features

- `Ok[T]` and `Err[E]` variants with `map`, `map_err`, `and_then` (a.k.a. `flat_map`)
- Ergonomic helpers: `ok(value)` and `err(error)`
- Type-narrowing friendly methods: `is_ok()`, `is_err()`, `unwrap()`, `unwrap_err()`
- PEP 561 `py.typed` for type-checker support

## Quickstart

```python
from resultlib import ok, err, Result

def parse_int(s: str) -> Result[int, str]:
    try:
        return ok(int(s))
    except ValueError:
        return err(f"not an int: {s}")

parse_int("42").map(lambda n: n * 2).unwrap()      # -> 84
parse_int("nope").map(lambda n: n * 2).is_err()    # -> True

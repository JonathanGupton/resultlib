from __future__ import annotations

import os
from typing import cast

import pytest

from resultlib import Ok, Err, Result, ok, err


def test_is_ok_and_is_err_and_unwrap():
    r1: Result[int, str] = ok(123)
    r2: Result[int, str] = err("boom")

    assert r1.is_ok() and not r1.is_err()
    assert r2.is_err() and not r2.is_ok()

    assert r1.unwrap() == 123
    with pytest.raises(RuntimeError):
        _ = r2.unwrap()
    assert r2.unwrap_err() == "boom"
    with pytest.raises(RuntimeError):
        _ = r1.unwrap_err()


def test_map_map_err_and_then():
    r_ok = ok(10).map(lambda x: x + 1).and_then(lambda x: ok(x * 2))
    assert isinstance(r_ok, Ok)
    assert r_ok.unwrap() == 22

    r_err = err("oops").map(lambda x: cast(int, x) + 1).map_err(lambda e: f"{e}!")
    assert isinstance(r_err, Err)
    assert r_err.unwrap_err() == "oops!"


def test_structural_pattern_matching_on_result():
    # Prefer structural pattern matching for branches in tests
    r1: Result[int, str] = ok(7)
    r2: Result[int, str] = err("bad")

    def to_str(r: Result[int, str]) -> str:
        match r:
            case Ok(value=v):
                return f"ok:{v}"
            case Err(error=e):
                return f"err:{e}"
            case _:
                return "unknown"

    assert to_str(r1) == "ok:7"
    assert to_str(r2) == "err:bad"


@pytest.mark.parametrize("payload", [ok("x"), err("y")])
def test_type_stability_through_combinators(payload: Result[str, str]):
    r = payload.map(lambda s: s + s).map_err(lambda e: e + "!")
    match r:
        case Ok(value=v):
            assert v in ("xx",)  # Ok path
        case Err(error=e):
            assert e == "y!"     # Err path

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


@pytest.mark.postgres
def test_postgres_roundtrip_if_available():
    """
    Optional: uses TEST_PG_URL to connect to Postgres and store Ok/Err rows.
    Skips automatically if TEST_PG_URL is unset.
    """
    dsn = os.getenv("TEST_PG_URL")
    if not dsn:
        pytest.skip("TEST_PG_URL not set; skipping Postgres-backed test")

    try:
        import psycopg
    except Exception:
        pytest.skip("psycopg not available")

    with psycopg.connect(dsn, autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                create table if not exists okerr_results(
                    id bigserial primary key,
                    is_ok boolean not null,
                    value text null,
                    error text null
                )
                """
            )
            # Insert one Ok and one Err
            def insert(r: Result[str, str]) -> None:
                match r:
                    case Ok(value=v):
                        cur.execute(
                            "insert into okerr_results(is_ok, value, error) values (true, %s, null)",
                            (v,),
                        )
                    case Err(error=e):
                        cur.execute(
                            "insert into okerr_results(is_ok, value, error) values (false, null, %s)",
                            (e,),
                        )

            insert(ok("hello"))
            insert(err("boom"))

            cur.execute(
                "select count(*) filter (where is_ok), count(*) filter (where not is_ok) from okerr_results"
            )
            ok_count, err_count = cur.fetchone()
            assert ok_count >= 1
            assert err_count >= 1

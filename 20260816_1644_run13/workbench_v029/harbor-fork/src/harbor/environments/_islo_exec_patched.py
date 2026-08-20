"""Local-vendored copy of :func:`islo.custom.exec.exec_and_wait` with a wider
poll-retry policy.

Why this exists
---------------
``islo.custom.exec.exec_and_wait`` only retries on ``ApiError`` 5xx during
its ``get_exec_result`` poll loop. It does **not** catch ``httpx.TransportError``
(ReadTimeout, ReadError, RemoteProtocolError, ConnectError, …), so a single
transient transport hiccup on the polling endpoint kills an otherwise
healthy long-running trial. Observed empirically: trials running ~10 min
under content-filter gateways were dying at a high rate to single-poll
``httpx.ReadTimeout`` / ``httpx.ReadError`` events that had nothing to do
with the trial's actual work.

The fix is one extra ``except`` branch using the same
``_MAX_CONSECUTIVE_POLL_ERRORS`` counter the existing 5xx branch uses.

This wrapper preserves the exact signature and behavior of
``islo.custom.exec.exec_and_wait`` so callers can swap the import with no
other change.
"""
from __future__ import annotations

import asyncio
import time
import typing

import httpx

from islo.core.api_error import ApiError
from islo.custom.exec import ExecResult, _MAX_CONSECUTIVE_POLL_ERRORS, _TERMINAL_STATUSES

if typing.TYPE_CHECKING:
    from islo.base_client import AsyncBaseIslo


async def exec_and_wait(
    client: "AsyncBaseIslo",
    sandbox_name: str,
    command: list[str],
    *,
    workdir: str | None = None,
    env: dict[str, str | None] | None = None,
    user: str | None = None,
    timeout: float | None = None,
    poll_interval: float = 2.0,
) -> ExecResult:
    """Start a command in *sandbox_name* and poll until completion.

    Identical to ``islo.custom.exec.exec_and_wait`` except the poll loop
    also retries on ``httpx.TransportError`` (treated as transient, with
    the same ``_MAX_CONSECUTIVE_POLL_ERRORS`` cap as 5xx).
    """
    kwargs: dict[str, typing.Any] = {"command": command}
    if workdir is not None:
        kwargs["workdir"] = workdir
    if env is not None:
        kwargs["env"] = env
    if user is not None:
        kwargs["user"] = user

    resp = await client.sandboxes.exec_in_sandbox(sandbox_name, **kwargs)
    exec_id = resp.exec_id

    deadline = time.monotonic() + timeout if timeout is not None else None
    consecutive_errors = 0
    while deadline is None or time.monotonic() < deadline:
        try:
            result = await client.sandboxes.get_exec_result(sandbox_name, exec_id)
            consecutive_errors = 0
        except ApiError as e:
            if (
                e.status_code is not None
                and e.status_code >= 500
                and consecutive_errors < _MAX_CONSECUTIVE_POLL_ERRORS
            ):
                consecutive_errors += 1
                await asyncio.sleep(poll_interval)
                continue
            raise
        except httpx.TransportError:
            # Treat transport errors (ReadTimeout, ReadError, RemoteProtocolError,
            # ConnectError, etc.) the same as 5xx — transient by nature. Without
            # this, a single hiccup on the poll endpoint kills the trial.
            if consecutive_errors < _MAX_CONSECUTIVE_POLL_ERRORS:
                consecutive_errors += 1
                await asyncio.sleep(poll_interval)
                continue
            raise
        if result.status in _TERMINAL_STATUSES:
            return ExecResult(
                stdout=result.stdout or "",
                stderr=result.stderr or "",
                exit_code=result.exit_code if result.exit_code is not None else -1,
            )
        await asyncio.sleep(poll_interval)

    return ExecResult(stdout="", stderr="", exit_code=-1, timed_out=True)

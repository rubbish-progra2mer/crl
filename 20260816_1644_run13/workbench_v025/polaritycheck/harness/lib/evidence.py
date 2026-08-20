#!/usr/bin/env python3
"""Evidence hygiene — make it hard to report a number the instrument could not see.

Two mechanisms, both born from real measurement mistakes during this study
(capped search results read as censuses; truncated result sets read as full
enumerations):

* ``Count`` cannot be formatted without a *blindness statement* — an explicit
  declaration of what the instrument was structurally incapable of seeing
  (a cap, a filter, a stratum, a time window). If nothing was invisible, that
  must be claimed explicitly, and it should look like the strong claim it is.
* ``capped()`` raises by default when a result set comes back exactly at its
  limit: a set at its cap is the visible edge of an unknown remainder, not a
  complete answer.

Severity ordering the defaults encode: silent-and-plausible failure is worse
than silent-and-inert failure is worse than a loud crash. Hence ``capped()``
raises rather than warns unless the caller explicitly accepts the risk.
"""

from __future__ import annotations

import warnings
from dataclasses import dataclass, field


class SaturatedResultError(RuntimeError):
    """A result set came back exactly at its limit — it is a sample, not a census."""


def capped(
    items,
    limit: int | None,
    source: str,
    *,
    raise_on_saturation: bool = True,
):
    """Return `items`, but refuse to let a saturated result set pass silently.

    A result set whose length exactly equals its requested limit is almost never
    a complete answer — it is the visible edge of an unknown remainder.

    Raises by default. Pass ``raise_on_saturation=False`` to downgrade to a
    warning, which is the right choice only when you are *deliberately* sampling
    and will say so in the write-up.
    """
    n = len(items)
    if limit is not None and n >= limit:
        msg = (
            f"{source}: returned {n} items at limit {limit} — SATURATED. "
            f"This is a sample of unknown size, not a census. Either raise the "
            f"limit until it stops saturating, or record the cap in every count "
            f"derived from it."
        )
        if raise_on_saturation:
            raise SaturatedResultError(msg)
        warnings.warn(msg, stacklevel=2)
    return items


@dataclass
class Count:
    """A number that cannot be reported without saying what produced it blind.

    The blindness statement is REQUIRED; there is no default. ``value`` is what
    was seen. ``could_not_see`` is what the instrument was structurally
    incapable of seeing. If you cannot name one, say so explicitly with
    ``could_not_see="nothing — full enumeration of <frame>"``; that is a strong
    claim and should look like one.
    """

    value: int
    what: str
    could_not_see: str
    frame: str = ""
    caveats: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.could_not_see or not self.could_not_see.strip():
            raise ValueError(
                f"Count({self.value}, {self.what!r}) has no blindness statement. "
                "State what the instrument could not have seen, or claim full "
                "enumeration explicitly. A count without this is not evidence."
            )

    @property
    def is_census(self) -> bool:
        return self.could_not_see.strip().lower().startswith("nothing")

    def __str__(self) -> str:
        head = f"{self.value} {self.what}"
        if self.frame:
            head += f" (of {self.frame})"
        tail = (
            "full enumeration" if self.is_census
            else f"BLIND TO: {self.could_not_see}"
        )
        out = f"{head} — {tail}"
        for c in self.caveats:
            out += f"\n    caveat: {c}"
        return out

    def as_dict(self) -> dict:
        return {
            "value": self.value,
            "what": self.what,
            "could_not_see": self.could_not_see,
            "frame": self.frame,
            "is_census": self.is_census,
            "caveats": list(self.caveats),
        }


def denominator_check(examined: int, total_raised: int, label: str) -> dict:
    """Guard the read of a rate whose denominator may be incomplete."""
    untested = total_raised - examined
    rec = {
        "label": label,
        "examined": examined,
        "total_raised": total_raised,
        "untested": untested,
        "denominator_complete": untested == 0,
    }
    if untested > 0:
        rec["required_phrasing"] = (
            f"{examined} of {total_raised} tested; {untested} UNTESTED. "
            f"Any rate below is over the tested subset only and says nothing "
            f"about the remainder."
        )
    return rec


def _self_check() -> None:
    assert capped([1, 2, 3], 5, "ok") == [1, 2, 3]
    try:
        capped([1, 2, 3], 3, "saturated")
    except SaturatedResultError:
        pass
    else:  # pragma: no cover
        raise AssertionError("saturation must raise by default")

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        capped([1, 2], 2, "sampling", raise_on_saturation=False)
        assert len(w) == 1, "downgrade must still warn"

    try:
        Count(5, "repos", could_not_see="")
    except ValueError:
        pass
    else:  # pragma: no cover
        raise AssertionError("a blindness statement must be mandatory")

    c = Count(36, "repositories with cosine gates", frame="3 capped queries",
              could_not_see="anything past --limit 12 per query")
    assert not c.is_census and "BLIND TO" in str(c)
    assert Count(9, "gates", could_not_see="nothing — full enumeration of the frame").is_census

    d = denominator_check(14, 25, "sweep defence")
    assert d["untested"] == 11 and not d["denominator_complete"]
    assert "UNTESTED" in d["required_phrasing"]
    assert denominator_check(25, 25, "x")["denominator_complete"]
    print("harness.lib.evidence self-check: PASS")


if __name__ == "__main__":
    _self_check()

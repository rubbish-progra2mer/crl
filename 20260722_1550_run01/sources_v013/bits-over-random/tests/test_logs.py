import json

from bor import audit, from_csv, from_jsonl


def _write_jsonl(path, rows):
    with open(path, "w") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")


def test_alias_resolution(tmp_path):
    p = tmp_path / "log.jsonl"
    _write_jsonl(p, [
        {"pool_size": 600, "top_k": 40, "num_relevant": 6, "found": True},
        {"pool_size": 600, "top_k": 40, "num_relevant": 6, "found": False},
    ])
    recs = from_jsonl(p)
    assert len(recs) == 2
    assert recs[0].N == 600 and recs[0].K == 40 and recs[0].R == 6
    assert recs[0].hit is True and recs[1].hit is False


def test_explicit_mapping(tmp_path):
    p = tmp_path / "log.jsonl"
    _write_jsonl(p, [{"corpus": 100, "shown": 5, "ok": "yes", "rel": 3}])
    recs = from_jsonl(p, mapping={"N": "corpus", "K": "shown",
                                  "hit": "ok", "R": "rel"})
    assert recs[0].N == 100 and recs[0].K == 5
    assert recs[0].R == 3 and recs[0].hit is True


def test_R_frac_estimate(tmp_path):
    p = tmp_path / "log.jsonl"
    _write_jsonl(p, [{"pool_size": 1000, "top_k": 10, "found": 1}])
    recs = from_jsonl(p, R_frac=0.05)
    assert recs[0].R == 50


def test_missing_R_raises(tmp_path):
    p = tmp_path / "log.jsonl"
    _write_jsonl(p, [{"pool_size": 1000, "top_k": 10, "found": 1}])
    try:
        from_jsonl(p)
    except ValueError as e:
        assert "R_frac" in str(e)
    else:
        raise AssertionError("missing R should raise without default")


def test_strict_missing_field(tmp_path):
    p = tmp_path / "log.jsonl"
    _write_jsonl(p, [{"top_k": 10, "found": 1}])
    assert from_jsonl(p, R_frac=0.05) == []  # lenient: skip
    try:
        from_jsonl(p, R_frac=0.05, strict=True)
    except ValueError:
        pass
    else:
        raise AssertionError("strict mode should raise on missing N")


def test_csv(tmp_path):
    p = tmp_path / "log.csv"
    p.write_text("pool_size,top_k,num_relevant,found\n600,40,6,true\n600,40,6,false\n")
    recs = from_csv(p)
    result = audit(recs, n_bootstrap=100)
    assert result.n_queries == 2


def test_per_row_R_beats_fallbacks(tmp_path):
    p = tmp_path / "log.jsonl"
    _write_jsonl(p, [{"pool_size": 1000, "top_k": 10, "num_relevant": 7, "found": 1}])
    recs = from_jsonl(p, default_R=3, R_frac=0.05)
    assert recs[0].R == 7


def test_default_R_beats_R_frac(tmp_path):
    p = tmp_path / "log.jsonl"
    _write_jsonl(p, [{"pool_size": 1000, "top_k": 10, "found": 1}])
    recs = from_jsonl(p, default_R=3, R_frac=0.05)
    assert recs[0].R == 3

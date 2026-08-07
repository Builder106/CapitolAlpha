"""
Unit tests for new pipeline modules (fama_french.py and monitor.py).
"""

from pathlib import Path
import pandas as pd
import numpy as np
from pipeline.fama_french import compute_factor_adjusted_alpha
from pipeline.monitor import analyze_trade_deltas


def test_compute_factor_adjusted_alpha():
    df = pd.DataFrame({
        "roi_90d": [0.15, 0.18, 0.12, 0.20, 0.14]
    })
    bench = pd.Series([0.11, 0.11, 0.11, 0.11, 0.11])
    res = compute_factor_adjusted_alpha(df, bench)

    assert res["n_trades"] == 5
    assert res["capm_alpha"] > 0
    assert "fama_french_alpha" in res


test_compute_factor_adjusted_alpha()


def test_analyze_trade_deltas(tmp_path):
    csv_file = tmp_path / "test_trades.csv"
    df = pd.DataFrame({
        "member_name": ["Alice", "Bob"],
        "transaction_date": ["2024-01-01", "2024-01-02"],
        "type": ["Purchase", "Sale"]
    })
    df.to_csv(csv_file, index=False)

    summary = analyze_trade_deltas(csv_file)
    assert summary["status"] == "ok"
    assert summary["total_rows"] == 2
    assert summary["unique_legislators"] == 2

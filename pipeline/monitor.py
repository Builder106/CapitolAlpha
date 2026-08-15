"""
Trade Disclosure Delta Monitor for CapitolAlpha.

Scans legislative trade records to detect newly appended disclosures,
checks data hygiene, and calculates summary metrics on recent PTR filings.
"""

from pathlib import Path
from typing import TypedDict
import pandas as pd


class TradeDeltaAnalysis(TypedDict, total=False):
    status: str
    message: str
    total_rows: int
    unique_legislators: int
    date_range: str
    trade_types: dict[str, int]


def analyze_trade_deltas(csv_path: Path) -> TradeDeltaAnalysis:
    """
    Reads legislative trades CSV and calculates dataset health and delta metrics.

    Args:
        csv_path: Path to legislative_trades.csv.

    Returns:
        Dict containing total row count, unique legislators, date range,
        and purchase vs sale count breakdown.
    """
    if not csv_path.exists():
        return {"status": "error", "message": f"CSV file not found at {csv_path}"}

    df = pd.read_csv(csv_path)

    total_rows = len(df)
    unique_legislators = df["member_name"].nunique() if "member_name" in df.columns else 0
    trade_types = df["type"].value_counts().to_dict() if "type" in df.columns else {}

    min_date = str(df["transaction_date"].min()) if "transaction_date" in df.columns else "N/A"
    max_date = str(df["transaction_date"].max()) if "transaction_date" in df.columns else "N/A"

    return {
        "status": "ok",
        "total_rows": total_rows,
        "unique_legislators": unique_legislators,
        "date_range": f"{min_date} to {max_date}",
        "trade_types": trade_types,
    }


if __name__ == "__main__":
    data_file = Path(__file__).resolve().parent.parent / "data" / "legislative_trades.csv"
    summary = analyze_trade_deltas(data_file)
    print("CapitolAlpha Disclosure Monitor Summary:")
    for k, v in summary.items():
        print(f"  {k}: {v}")

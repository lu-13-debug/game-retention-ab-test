"""python -m game_ab.run"""

import argparse
import csv
import json
from pathlib import Path

import pandas as pd

from .analyze import analyze
from .report import render


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=root / "data/raw/cookie_cats.csv")
    parser.add_argument("--output", type=Path, default=root / "results")
    args = parser.parse_args()
    if not args.source.exists():
        parser.error("缺少原始数据；先运行 python download_data.py")
    metrics = analyze(pd.read_csv(args.source))
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    with (args.output / "group_summary.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle)
        writer.writerow(["group", "players", "d1_retained", "d1_rate", "d7_retained", "d7_rate", "rounds_median", "rounds_mean"])
        for group, data in metrics["groups"].items():
            writer.writerow([group, *(data[key] for key in ("players", "d1_retained", "d1_rate", "d7_retained", "d7_rate", "rounds_median", "rounds_mean"))])
    (args.output / "report.html").write_text(render(metrics), encoding="utf-8")
    print(json.dumps({"players": metrics["players"], "d7_effect_pp": metrics["effects"]["d7"]["rate_difference_pp"], "srm_p": metrics["srm"]["p_value"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

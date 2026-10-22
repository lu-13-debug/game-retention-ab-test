"""按原始分组（ITT）计算留存差异、实验分流和轮数。"""

import math

import pandas as pd
from scipy.stats import chi2, norm

EXPECTED = {"userid", "version", "sum_gamerounds", "retention_1", "retention_7"}
GROUPS = ("gate_30", "gate_40")


def _as_bool(series: pd.Series) -> pd.Series:
    values = series.astype("string").str.lower()
    if not values.isin(["true", "false", "1", "0"]).all():
        raise ValueError("留存字段只能包含 TRUE/FALSE 或 1/0")
    return values.isin(["true", "1"])


def analyze(frame: pd.DataFrame) -> dict:
    missing = EXPECTED - set(frame.columns)
    if missing:
        raise ValueError(f"缺少字段：{sorted(missing)}")
    data = frame.copy()
    if data.empty or data.isna().any().any() or data["userid"].duplicated().any():
        raise ValueError("数据为空、含缺失值或 userid 重复")
    if set(data["version"]) != set(GROUPS):
        raise ValueError("实验组必须同时包含 gate_30 和 gate_40")
    data["sum_gamerounds"] = pd.to_numeric(data["sum_gamerounds"], errors="raise")
    if (data["sum_gamerounds"] < 0).any():
        raise ValueError("游戏轮数不能为负")
    for field in ("retention_1", "retention_7"):
        data[field] = _as_bool(data[field])

    groups = {}
    for name in GROUPS:
        part = data.loc[data["version"] == name]
        n = len(part)
        d1 = int(part["retention_1"].sum())
        d7 = int(part["retention_7"].sum())
        groups[name] = {
            "players": n, "d1_retained": d1, "d1_rate": d1 / n,
            "d7_retained": d7, "d7_rate": d7 / n,
            "rounds_median": float(part["sum_gamerounds"].median()),
            "rounds_mean": float(part["sum_gamerounds"].mean()),
        }

    n0, n1 = (groups[name]["players"] for name in GROUPS)
    total = n0 + n1
    srm_chi2 = (n0 - total / 2) ** 2 / (total / 2) + (n1 - total / 2) ** 2 / (total / 2)
    effects = {}
    for key in ("d1", "d7"):
        c0, c1 = (groups[name][f"{key}_retained"] for name in GROUPS)
        p0, p1 = c0 / n0, c1 / n1
        difference = p1 - p0
        pooled = (c0 + c1) / total
        pooled_se = math.sqrt(pooled * (1 - pooled) * (1 / n0 + 1 / n1))
        z = difference / pooled_se if pooled_se else 0.0
        ci_se = math.sqrt(p0 * (1 - p0) / n0 + p1 * (1 - p1) / n1)
        effects[key] = {
            "rate_difference_pp": difference * 100,
            "z_p_value": float(2 * norm.sf(abs(z))) if pooled_se else 1.0,
            "difference_95ci_pp": [(difference - 1.96 * ci_se) * 100, (difference + 1.96 * ci_se) * 100],
        }
    return {
        "source": "Kaggle Mobile Games: A/B Testing / DataCamp Cookie Cats",
        "players": total, "groups": groups, "effects": effects,
        "srm": {"expected_ratio": "50:50", "chi_square": srm_chi2,
                "p_value": float(chi2.sf(srm_chi2, 1)), "flag_at_0_05": bool(chi2.sf(srm_chi2, 1) < 0.05)},
        "rounds_outliers_over_10000": int((data["sum_gamerounds"] > 10000).sum()),
        "decision_note": "仅在原实验预期为 1:1 分配时，分流检验才可用于判断异常；应核查实际分配方案和采集过程，再作上线因果决策。",
    }

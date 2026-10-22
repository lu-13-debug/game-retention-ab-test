"""生成无第三方前端依赖的离线报告。"""

from html import escape


def render(metrics: dict) -> str:
    groups = metrics["groups"]
    bars = []
    for idx, name in enumerate(("gate_30", "gate_40")):
        y = 45 + idx * 65
        rate = groups[name]["d7_rate"]
        bars.append(f'<text x="0" y="{y}" font-size="15">{name}</text><rect x="100" y="{y-17}" width="{rate*1600:.1f}" height="24" rx="4" fill="{["#16759d","#e59443"][idx]}"/><text x="{110+rate*1600:.1f}" y="{y}" font-size="14">{rate:.2%}</text>')
    d7 = metrics["effects"]["d7"]
    flag = "若原实验预期 1:1 分配，则触发分流异常提示" if metrics["srm"]["flag_at_0_05"] else "若原实验预期 1:1 分配，则未触发 5% 分流异常阈值"
    return f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>Cookie Cats 游戏留存 A/B 分析</title>
<style>body{{font:16px/1.65 Arial,"Microsoft YaHei",sans-serif;color:#1d3040;max-width:900px;margin:36px auto;padding:0 24px}}h1,h2{{color:#125779}}.card{{background:#eef6fa;padding:18px;border-radius:10px}}svg{{max-width:100%}}small{{color:#617181}}</style>
<h1>Cookie Cats 游戏留存 A/B 分析</h1><p>公开历史实验数据；关卡门槛 gate_30 与 gate_40。统计口径为按分配组分析（ITT），共有 {metrics["players"]:,} 名玩家。</p>
<h2>第 7 日留存</h2><svg viewBox="0 0 600 160" role="img" aria-label="两组第七日留存率">{''.join(bars)}</svg>
<div class="card"><b>gate_40 − gate_30：</b>{d7["rate_difference_pp"]:+.3f} 个百分点；双比例 z 检验 p={d7["z_p_value"]:.4g}；95% 区间 [{d7["difference_95ci_pp"][0]:+.3f}, {d7["difference_95ci_pp"][1]:+.3f}] 个百分点。</div>
<h2>实验完整性</h2><p>以 50:50 为假设的分流卡方检验 p={metrics["srm"]["p_value"]:.4g}；{escape(flag)}。超过 10,000 轮的极端记录 {metrics["rounds_outliers_over_10000"]} 条，保留在原分组留存统计中。</p>
<h2>结论边界</h2><p>{escape(metrics["decision_note"])} 数据没有付费、收入、DAU 或完整逐日事件，不能据此计算 ARPU、LTV 或变现收益。</p>
<small>来源：<a href="https://www.kaggle.com/datasets/yufengsui/mobile-games-ab-testing">Kaggle Cookie Cats 数据集</a>。</small></html>'''

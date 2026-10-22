# Cookie Cats 手游关卡 A/B 实验与玩家留存分析

使用公开的 Cookie Cats 历史实验数据，比较关卡门槛设在第 30 关与第 40 关时玩家次日、第 7 日留存的差异。项目涵盖数据校验、分组汇总、双比例检验、95% 区间、假设 1:1 分配时的分流比例核查，以及离线 HTML 报告。数据仅用于独立学习分析；成果是统计报告和决策建议，不是经营收益。

## 技术栈与软件

- **Python 3.12+、Pandas**：读取 CSV、检查一人一行和实验组、汇总留存及轮数。
- **SciPy**：正态近似双比例 z 检验与分流卡方检验。
- **Requests**：从 Kaggle 公共 API 下载并校验原始 CSV。
- **unittest、HTML/SVG**：手算样本测试和可离线打开的报告。
- Windows PowerShell、任一现代浏览器；不需要云服务、数据库或 GPU。

## 已复现成果

| 指标 | gate_30 | gate_40 |
|---|---:|---:|
| 玩家数 | 44,700 | 45,489 |
| 次日留存 | 44.82% | 44.23% |
| 第 7 日留存 | 19.02% | 18.20% |
| 14 日游戏轮数中位数 | 17 | 16 |

第 7 日留存差值（gate_40 − gate_30）为 **−0.820 个百分点**，双比例检验 p≈0.00155，95% 区间约 [−1.328, −0.312] 个百分点。以 **1:1 分配仅作假设** 的分流核查 p≈0.00861；原实验真实预期配比未公开，不能直接判定埋点故障。由于缺少付款数据，不能声称任何付费收益。

## 实现与文件

| 文件 | 工作 |
|---|---|
| `download_data.py` | 下载并校验原始 CSV 的 SHA-256 |
| `game_ab/analyze.py` | 校验、一人一行统计、留存差异、显著性及分流核查 |
| `game_ab/report.py` | 把真实计算结果写成 SVG/HTML 报告 |
| `game_ab/run.py` | 串联输入与输出；支持自定义路径 |
| `tests/test_game_ab.py` | 手算留存与无效分组边界测试 |
| `results/metrics.json`、`group_summary.csv`、`report.html` | 实际运行输出 |
| `data/README.md`、`复现步骤.md` | 数据出处、软件安装与逐步操作 |

## 运行

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe download_data.py
.\.venv\Scripts\python.exe -m game_ab.run
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

本地文件夹已放入初始 CSV，可直接跳过下载一步。GitHub 克隆版需要下载。详细的环境检查、文件说明、结果复核和错误处理见 [复现步骤.md](复现步骤.md)。原始数据来源见 [Kaggle 数据卡](https://www.kaggle.com/datasets/yufengsui/mobile-games-ab-testing)，参考的公开 [分析 Notebook](https://www.kaggle.com/code/yufengsui/datacamp-project-mobile-games-a-b-testing)。

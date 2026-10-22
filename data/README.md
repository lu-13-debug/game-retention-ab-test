# 数据来源与边界

- 原始来源：[Kaggle Mobile Games: A/B Testing](https://www.kaggle.com/datasets/yufengsui/mobile-games-ab-testing)，数据卡标明源自 DataCamp 的 Cookie Cats 项目。
- 本地文件：`data/raw/cookie_cats.csv`，90,189 行、5 列；SHA-256：`9f53027065840672e77303281289988371d4a6b67c7dcd3bd4e6306a2a263dc8`。
- 字段：`userid`、`version`（gate_30/gate_40）、`sum_gamerounds`、`retention_1`、`retention_7`。
- 从仓库克隆时原始 CSV 不随仓库上传；运行 `python download_data.py` 从公开数据入口获取并校验。若 Kaggle 改版，脚本会报校验不一致，避免悄悄替换数据。
- 数据卡许可证标记为 Unknown，因此 GitHub 只发布分析代码、聚合结果和下载入口。本地 CSV 供个人复现。
- 没有付款、收入、广告、逐日登录和完整关卡事件；不能计算 ARPU、LTV、DAU，也不能判断某位玩家是否真的遇到关卡门槛。

"""从 Kaggle 公共数据集 API 下载原始 CSV；不从第三方分析结果反推数字。"""

import hashlib
import io
from pathlib import Path
import zipfile

import requests

URL = "https://www.kaggle.com/api/v1/datasets/download/yufengsui/mobile-games-ab-testing"
EXPECTED_SHA256 = "9f53027065840672e77303281289988371d4a6b67c7dcd3bd4e6306a2a263dc8"


def main():
    target = Path(__file__).resolve().parent / "data/raw/cookie_cats.csv"
    target.parent.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.trust_env = False
    response = session.get(URL, timeout=120)
    response.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
        payload = archive.read("cookie_cats.csv")
    digest = hashlib.sha256(payload).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError(f"源数据版本与本项目不同，SHA-256={digest}")
    target.write_bytes(payload)
    print(f"已保存 {target}，{len(payload):,} 字节")


if __name__ == "__main__":
    main()

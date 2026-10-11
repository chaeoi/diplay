import subprocess
import datetime

commit_sha = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
commit_msg = subprocess.check_output(["git", "log", "-1", "--pretty=%B"]).decode().strip()
now_str = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

body = f"""## DiPlay 0.1.0

> **构建时间**：{now_str}
> **Git Commit**：`{commit_sha}`

### 📝 本次变更详报 (Changelog)
```text
{commit_msg}
```

---

### 🎯 核心架构与解耦说明 (Architecture & Scope)
本版本基于 [shihabal3amri/DiPlay](https://github.com/shihabal3amri/DiPlay) 进行架构解耦，专注于**通用 Android 车机（Android 7.1+）**的高效、低开销运行：
1. **比亚迪专有硬件依赖剥离**：
   - **切断 ADB CAN 信号嗅探**：停止向 `5555` 端口轮询车速、电量、挡位与胎压，彻底消除探针重试造成的 CPU/内存浪费；
   - **移除仪表盘/HUD 专有广播**：切断高德与 SOME-IP 专有投屏通道；
   - **关闭氛围灯与来电弹窗常驻守护**：杜绝向系统服务注入 `app_process`。
2. **独立上游更新隔离**：
   - 拦截并停用官方 GitHub Release 自动检查 Worker，确保定制 APK 不被官方原版覆盖。
3. **极简车机交互**：
   - 隐藏专有无效设置卡片，仅保留核心投屏、分辨率（DPI/安全边距）、刷新率与音频通道分配。
4. **特性开关集中治理 (`FeatureConfig.kt`)**：
   - 保留全部官方类结构，在入口处实施条件短路，确保未来 `git merge upstream/main` 实现 100% 自动无冲突合流。

---

### 📦 产物校验 (Verification)
| 文件名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `diplay-0.1.0.apk` | Android 安装包 | 通用车机安装包 (支持 arm64/armv7a/x86/x86_64) |
| `sha256sum.txt` | 校验摘要 | SHA-256 哈希校验文本 |
"""

with open("release_body.md", "w", encoding="utf-8") as f:
    f.write(body)

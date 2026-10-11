# DiPlay (定制精简与通用增强版)

本项目基于开源项目 [shihabal3amri/DiPlay](https://github.com/shihabal3amri/DiPlay) 进行二次开发。

针对**通用 Android 车机**进行了架构解耦、功能精简与稳定性优化：
- **剥离比亚迪专有强绑定**：切断了依赖网络 ADB 的比亚迪 CAN 信号窃取（车速/电量/胎压）、HUD 与仪表盘专有广播/SOME-IP 投屏、氛围灯控制、来电弹窗拦截等专有后台与卡片。
- **关闭官方自动更新检查**：杜绝因官方新版推送导致二开版本被误覆盖。
- **保留并调优通用 CarPlay 体验**：专注于通用 Android 车机免盒子、低延迟、即插即用的有线/无线 CarPlay 投屏能力。

---

## 🛠️ 二开架构与与上游（Upstream）同步机制

本项目在代码改造上遵循**“入口短路、配置解耦、不物理删除上游文件”**的原则，配置统一收敛在 `shared/.../FeatureConfig.kt` 中。

### 分支结构
- **`main`（当前主分支）**：你的定制化二开主分支。
- **`upstream/main`**：跟踪官方 GitHub 最新代码仓库。

### 一键合并官方最新更新
当官方发布新版本或修复底层 CarPlay 协议 bug 时，在本地执行以下命令即可平滑合并：

```bash
# 1. 获取官方最新更新
git fetch upstream

# 2. 合并官方 main 分支到当前主分支
git merge upstream/main -m "chore: sync upstream latest"
```
由于未物理删除官方上游代码文件，仅在顶层调用挂载 `FeatureConfig` 开关，大部分情况下 Git 可实现**自动无冲突合并（Auto-merge）**。

---

## ⚙️ 定制特性配置 (FeatureConfig)

所有特性开关位于 `shared/src/main/java/com/shilapi/xcertplay/FeatureConfig.kt`：

```kotlin
object FeatureConfig {
    // 是否启用比亚迪专有功能（ADB车辆数据、HUD/仪表投屏、来电拦截等，默认为 false）
    var enableBydFeatures: Boolean = false

    // 是否启用氛围灯随音乐变色（默认为 false）
    var enableAmbientLighting: Boolean = false

    // 是否启用仪表盘投屏（默认为 false）
    var enableClusterDisplay: Boolean = false

    // 是否启用官方在线更新检测（默认为 false，防止覆盖二次开发版本）
    var enableAutoUpdate: Boolean = false
}
```

---

## 🚀 核心功能支持情况

### 🟢 保持并增强的通用能力
1. **连接方式**：
   - 有线 USB 连接（支持 NCM 虚拟网卡通道、即插即用自动授权）。
   - 无线 Wi-Fi Direct (P2P) 连接。
   - 车机内置热点互联与局域网 (Same LAN) 连接模式。
2. **显示与交互**：
   - H.264 硬件解码、流畅多点触控反馈。
   - 自定义分辨率、DPI、FPS（最高 60 帧）及安全边距调节。
   - 随时间或系统主题自动切换日间/夜间模式。
3. **音频与语音**：
   - 多音频通道支持（音乐、导航播报、电话分离）。
   - 车机麦克风输入与软件 Opus 编码（支持 Siri、微信语音、电话通话）。
   - Speex 硬件/软件回声消除 (AEC)。
4. **车辆基础交互**：
   - 通用方向盘按键监听与切歌映射。
   - 车机 GPS 位置信息实时共享给 iPhone（高德/苹果地图定位更稳）。

### 🔴 已精简/屏蔽的专有功能
- 比亚迪网络 ADB 轮询与车辆探针（节约后台 CPU 与内存开销）。
- 比亚迪 SOME-IP / 高德 HUD 投屏。
- 比亚迪原厂氛围灯颜色注入。
- 比亚迪系统来电弹窗屏蔽守护进程。
- 官方自动更新检查与弹窗提醒。

---

## 📦 构建与运行

### 环境要求
- JDK 17+
- Android SDK 34+

### 构建 APK
```bash
# 构建 Debug 安装包
./gradlew :mobile:assembleDebug

# 输出路径：mobile/build/outputs/apk/debug/
```

---

## 📄 开源许可与致谢
- 基于 [xcertplay](https://github.com/shilapi/xcertplay) (GPL-3.0) 与 [DiPlay](https://github.com/shihabal3amri/DiPlay) (GPL-3.0)。
- 界面视觉继承自 [DiAuto](https://github.com/shihabal3amri/DiAuto) (AGPL-3.0)。
- CarPlay 及其标识归 Apple Inc. 所有。

# DiPlay 通用车机定制版

[English Documentation](README.en.md) · [Releases 下载](https://github.com/chaeoi/diplay/releases)

面向通用 Android 车机（Android 7.1+）的独立 CarPlay 协议接收端。基于 [shihabal3amri/DiPlay](https://github.com/shihabal3amri/DiPlay) 进行架构解耦与专有依赖裁剪。

---

## 为什么维护此分支

上游原版 DiPlay 深度绑定了比亚迪（BYD）车机生态，引入了大量强依赖网络 ADB（端口 5555）的私有服务与守护线程：
- 周期性轮询比亚迪私有 CAN 信号（车速、挡位、电池 SOC 与胎压）。
- 依赖特定 DiLink 固件的仪表盘（Cluster）及风挡 HUD 专有 SOME-IP / 高德地图广播协议。
- 通过 `app_process` 注入车身服务以控制氛围灯随专辑封面变色。
- 常驻后台的来电悬浮窗屏蔽服务。

在非比亚迪的通用 Android 车机（如后装车机、公版方案或其它品牌车机）上，这些服务不仅无法工作，还会因为持续的探针重试、后台线程争用和 ADB 失败重连带来额外的 CPU 与内存开销。

本分支专注于 **CarPlay 核心投屏通道的稳定性与通用性**：
1. **完全切断专有硬件与协议依赖**：置空比亚迪私有服务探针与后台常驻，消除通用车机上的无效开销。
2. **精简车机端交互设置**：隐藏所有不可用的专有配置卡片，仅保留核心投屏、分辨率、帧率与音频路由项。
3. **隔离官方版本检查**：关闭上游 GitHub Releases 自动检测与弹窗，防止定制 APK 被官方上游更新覆盖。
4. **全自动持续集成构建**：主干每次提交均通过 GitHub Actions 自动编译生成 Release 安装包，版本自 `0.1.0` 起独立迭代。

---

## 架构设计：与上游保持无痛同步

为了在上游持续修复底层 CarPlay 协议与音视频编解码 Bug 时能够平滑合流，本项目不物理删除上游任何专有实现类，而是通过位于 `shared/src/main/java/com/shilapi/xcertplay/FeatureConfig.kt` 的特性开关在调用入口处实施短路：

```kotlin
object FeatureConfig {
    // 比亚迪专有特性（ADB CAN 信号嗅探、HUD/仪表投屏、来电拦截），默认关闭
    var enableBydFeatures: Boolean = false

    // 氛围灯硬件注入控制，默认关闭
    var enableAmbientLighting: Boolean = false

    // 仪表盘投屏 Activity 路由，默认关闭
    var enableClusterDisplay: Boolean = false

    // 上游版本在线检查，默认关闭
    var enableAutoUpdate: Boolean = false
}
```

### 上游代码合并流程

本地 Git 仓库配置如下：
- `main`：本分支主干，包含所有通用解耦与界面裁剪改动。
- `upstream/main`：上游官方只读跟踪分支 (`https://github.com/shihabal3amri/DiPlay.git`)。

当上游发布协议更新或驱动修复时，直接在本地主分支执行合流：

```bash
git fetch upstream
git merge upstream/main -m "chore: merge upstream changes"
```

由于上游内部实现文件结构未被破坏，绝大多数协议层更新可由 Git 直接完成无冲突自动合并（Auto-merge）。

---

## 功能范畴与实现状态

### 完整保留并支持的通用特性
- **传输层**：
  - 有线 USB：基于 NCM (Network Control Model) 虚拟网卡通道，支持自动确认免插拔授权。
  - 无线连接：支持系统 Wi-Fi Direct (P2P)、车机热点（AP）与同局域网（Same LAN）三种模式。
- **音视频渲染**：
  - 视频解码：基于 MediaCodec 硬件加速解码 H.264，支持自定义输出分辨率、DPI、安全显示区域及最高 60 FPS 刷新率。
  - 音频管线：主音轨、语音导航与电话通话分离输出；支持 Speex 回声消除（AEC）与基于 Concentus 的软件 Opus 麦克风音频上行。
- **人机交互**：
  - 屏幕多点触控与坐标映射。
  - 无障碍方向盘切歌与通用媒体按键映射。
  - 车机板载 GPS 数据回传 iPhone（提升隧道与弱信号场景定位精度）。
  - 日夜模式：支持跟随系统主题、环境光强度或固定时间表自动切换。

### 已切断/移除的专有逻辑
- 网络 ADB 车辆探针（`BydVehicleSettingsBackend`、`BydVehicleCapabilityProbe`）。
- 仪表盘与 HUD 专有投屏通道（`BydNavigationOutputs`、`BydHudBridge`、`BydClusterBridge`）。
- 氛围灯封面律动工作线程（`AmbientLampSession`、`BydAmbientLightClient`）。
- 比亚迪来电弹窗抑制守护进程（`BydCallPopupGuard`）。
- 上游版本更新检测 Worker（`BackgroundUpdateWorker`）。

---

## 编译与安装

### 预编译包
直接从 [GitHub Releases](https://github.com/chaeoi/diplay/releases) 下载最新构建的 `diplay-v0.1.0-debug.apk` 并安装至车机。

### 本地源码构建

构建环境要求：
- JDK 17 或 21
- Android SDK（API Level 34+）

执行构建：

```bash
./gradlew :mobile:assembleDebug
```

生成文件位于 `mobile/build/outputs/apk/debug/`。

---

## 许可与致谢
- CarPlay 协议接收核心源自 [xcertplay](https://github.com/shilapi/xcertplay)（GPL-3.0 协议）与 [DiPlay](https://github.com/shihabal3amri/DiPlay)（GPL-3.0 协议）。
- 车机控制台界面源自 [DiAuto](https://github.com/shihabal3amri/DiAuto)（AGPL-3.0 协议）。
- CarPlay 是 Apple Inc. 的注册商标。本项目仅供技术研究与个人车机交互体验适配。

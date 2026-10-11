# DiPlay (Universal Android Head Unit Edition)

[中文说明文档](README.md) · [Releases & Downloads](https://github.com/chaeoi/diplay/releases)

A standalone CarPlay receiver for general Android automotive head units (Android 7.1+), based on [shihabal3amri/DiPlay](https://github.com/shihabal3amri/DiPlay).

---

## Overview & Motivation

The upstream DiPlay project is heavily geared towards BYD automotive head units, introducing various proprietary background services that rely on network ADB (port 5555):
- Periodic polling for proprietary BYD CAN signals (wheel speed, transmission gear, battery SOC, tyre pressure).
- Instrument cluster and HUD navigation projection using proprietary SOME-IP and Amap broadcast protocols.
- Ambient lighting color synchronization via `app_process` shell injection.
- Foreground call popup suppression guards.

On universal Android head units (aftermarket units, standard AOSP-based platforms, or other brands), these background services are unusable and lead to unnecessary CPU/memory overhead caused by continuous ADB connection retries.

This repository decouples those proprietary subsystems and focuses strictly on **core wired/wireless CarPlay stability, efficiency, and clean UI presentation**:
1. **Proprietary Vendor Decoupling**: Short-circuits vendor-specific ADB probes and background workers at the call boundary.
2. **Simplified Head Unit Interface**: Hides inapplicable settings cards and streamlines options down to projection, display, and audio routing.
3. **Upstream Update Isolation**: Disables upstream update checks to prevent custom builds from being overwritten.
4. **Automated Continuous Delivery**: Every commit to `main` automatically triggers an APK build and publishes a GitHub Release, starting with version `0.1.0`.

---

## Architecture & Upstream Synchronization

To allow smooth, conflict-free merges when upstream releases protocol fixes, this project avoids physically deleting upstream files. All feature gating is centralized in `shared/src/main/java/com/shilapi/xcertplay/FeatureConfig.kt`:

```kotlin
object FeatureConfig {
    var enableBydFeatures: Boolean = false
    var enableAmbientLighting: Boolean = false
    var enableClusterDisplay: Boolean = false
    var enableAutoUpdate: Boolean = false
}
```

### Syncing Upstream Changes

```bash
git fetch upstream
git merge upstream/main -m "chore: merge upstream changes"
```

Because upstream files remain structurally present, Git automatically handles most protocol-level merges without manual conflict resolution.

---

## Supported Features

### General Features Retained & Enhanced
- **Connectivity**:
  - Wired USB: NCM (Network Control Model) virtual network adapter with automatic device approval.
  - Wireless: Wi-Fi Direct (P2P), built-in vehicle AP hotspot, and existing local network (Same LAN) connections.
- **Media & Rendering**:
  - Video: H.264 hardware decoding via MediaCodec, configurable resolution, DPI, custom display margins, and up to 60 FPS.
  - Audio: Independent audio channels (Media, Speech, Alert), Speex Acoustic Echo Cancellation (AEC), and software Opus microphone encoding.
- **Vehicle Interaction**:
  - Multi-touch display input.
  - Accessibility-based steering wheel controls (track skip, Siri activation).
  - Head unit onboard GPS relaying to iPhone.
  - Day / Night appearance switching based on system theme or time schedule.

### Proprietary Subsystems Bypassed
- Network ADB vehicle telemetry probes (`BydVehicleSettingsBackend`, `BydVehicleCapabilityProbe`).
- Cluster & HUD display broadcasting (`BydNavigationOutputs`, `BydHudBridge`, `BydClusterBridge`).
- Ambient light color extractor & workers (`AmbientLampSession`, `BydAmbientLightClient`).
- Call popup suppression loop (`BydCallPopupGuard`).
- Upstream version checking worker (`BackgroundUpdateWorker`).

---

## Building from Source

Requirements:
- JDK 17 or 21
- Android SDK (API Level 34+)

Build the debug APK:

```bash
./gradlew :mobile:assembleDebug
```

Outputs are located in `mobile/build/outputs/apk/debug/`.

---

## License & Attribution
- Core CarPlay receiver derived from [xcertplay](https://github.com/shilapi/xcertplay) (GPL-3.0) and [DiPlay](https://github.com/shihabal3amri/DiPlay) (GPL-3.0).
- Automotive dashboard UI adapted from [DiAuto](https://github.com/shihabal3amri/DiAuto) (AGPL-3.0).
- CarPlay is a trademark of Apple Inc.

# DiPlay (Custom & General Android Head Unit Edition)

[中文说明文档 (Chinese)](README.md) | [Releases / Download](https://github.com/chaeoi/diplay/releases)

This is a customized fork based on [shihabal3amri/DiPlay](https://github.com/shihabal3amri/DiPlay).

It decouples proprietary automotive vendor features, streamlines the background workload, and focuses on delivering a reliable, standalone wired and wireless CarPlay receiver for **general Android head units**.

---

## 🚀 Key Improvements & Decoupling

1. **Stripped BYD-Specific Proprietary Dependencies**:
   - Short-circuited ADB vehicle probing (speed, gear, battery SOC, tyre pressure).
   - Removed BYD-specific HUD & instrument cluster SOME-IP / Amap broadcast adapters.
   - Disabled ambient lighting injection and BYD incoming call popup guard.
   - Reduced CPU/memory usage caused by background polling.
2. **Disabled Upstream Auto-Update Checks**:
   - Prevents your customized APK from being overwritten by official releases.
3. **Automated Release on Main Push**:
   - Starts versioning cleanly from `0.1.0`. Every push to `main` automatically builds and publishes an APK release without requiring manual tags.
4. **Optimized for Universal Android Head Units**:
   - Focused on core wired/wireless CarPlay protocol reliability.
   - Cleaned up settings UI to eliminate clutter.

---

## 🛠️ Upstream Synchronization Workflow

This project adopts the **Vendor Branch / Feature Flag** approach. Upstream source files are kept structurally intact so you can easily pull and merge upstream fixes.

```bash
# Fetch latest commits from upstream official repo
git fetch upstream

# Merge upstream main into your custom main branch
git merge upstream/main -m "chore: sync upstream latest"
```

---

## ⚙️ Configuration Flags (`FeatureConfig.kt`)

Located at `shared/src/main/java/com/shilapi/xcertplay/FeatureConfig.kt`:

```kotlin
object FeatureConfig {
    var enableBydFeatures: Boolean = false
    var enableAmbientLighting: Boolean = false
    var enableClusterDisplay: Boolean = false
    var enableAutoUpdate: Boolean = false
}
```

---

## 📦 Building

```bash
./gradlew :mobile:assembleDebug
```

---

## 📄 License & Attribution
- Core CarPlay receiver based on [xcertplay](https://github.com/shilapi/xcertplay) (GPL-3.0) and [DiPlay](https://github.com/shihabal3amri/DiPlay) (GPL-3.0).
- UI adapted from [DiAuto](https://github.com/shihabal3amri/DiAuto) (AGPL-3.0).
- CarPlay is a trademark of Apple Inc.

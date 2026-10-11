package com.shilapi.xcertplay

/**
 * 二开特性全局开关配置 (Feature Flags)
 *
 * 用于一键隔离或启用各模块功能：
 * 保持官方原始代码文件完整，便于后续 upstream rebase / merge 无冲突更新。
 */
object FeatureConfig {
    /**
     * 是否启用比亚迪 (BYD) 专有定制功能：
     * 包括：
     * 1. 车辆总线与 ADB 探针 (车速、电量 SOC、胎压等)
     * 2. 比亚迪专有仪表盘 (Cluster) 与 HUD 投屏 / 高德 SOME-IP 桥接
     * 3. 氛围灯律动 (Ambient Lighting)
     * 4. 比亚迪原车通话弹窗拦截 (BydCallPopupGuard)
     *
     * 设置为 false 时，所有比亚迪专有 UI 设置项被屏蔽，后台 ADB/广播任务自动短路。
     */
    var enableBydFeatures: Boolean = false

    /**
     * 是否启用氛围灯跟随音乐律动
     */
    var enableAmbientLighting: Boolean = false

    /**
     * 是否启用原车仪表盘 (Cluster Map / ADB Cluster) 投屏
     */
    var enableClusterDisplay: Boolean = false

    /**
     * 是否启用在线检查版本与自动更新功能
     */
    var enableAutoUpdate: Boolean = false
}

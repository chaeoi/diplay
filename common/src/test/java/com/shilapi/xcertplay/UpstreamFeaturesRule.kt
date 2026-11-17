package com.shilapi.xcertplay

import org.junit.rules.ExternalResource

/** Enable inherited feature paths for their tests, then restore the fork's configuration. */
class UpstreamFeaturesRule : ExternalResource() {
    private lateinit var previous: BooleanArray

    override fun before() {
        previous = booleanArrayOf(
            FeatureConfig.enableBydFeatures,
            FeatureConfig.enableAmbientLighting,
            FeatureConfig.enableClusterDisplay,
            FeatureConfig.enableAutoUpdate,
        )
        FeatureConfig.enableBydFeatures = true
        FeatureConfig.enableAmbientLighting = true
        FeatureConfig.enableClusterDisplay = true
        FeatureConfig.enableAutoUpdate = true
    }

    override fun after() {
        FeatureConfig.enableBydFeatures = previous[0]
        FeatureConfig.enableAmbientLighting = previous[1]
        FeatureConfig.enableClusterDisplay = previous[2]
        FeatureConfig.enableAutoUpdate = previous[3]
    }
}

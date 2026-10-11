package com.shilapi.xcertplay

import android.content.Context
import com.shilapi.xcertplay.hud.BydAdbAccess
import com.shilapi.xcertplay.hud.BydVehicleCapabilityProbe
import com.shilapi.xcertplay.hud.BydVehicleProbeOutcome

/** Test seam for the blocking ADB work launched by the host settings page. */
internal interface BydVehicleSettingsBackend {
    fun check(context: Context, mayAsk: Boolean): BydAdbAccess.Status
    fun checkState(context: Context, mayAsk: Boolean): BydAdbAccess.State
    fun probe(context: Context, persist: Boolean): BydVehicleProbeOutcome
    fun execute(name: String, block: () -> Unit)
}

internal object AndroidBydVehicleSettingsBackend : BydVehicleSettingsBackend {
    override fun check(context: Context, mayAsk: Boolean): BydAdbAccess.Status {
        if (!FeatureConfig.enableBydFeatures) {
            return BydAdbAccess.Status(BydAdbAccess.State.UNSUPPORTED)
        }
        return BydAdbAccess.check(context, mayAsk)
    }

    override fun checkState(context: Context, mayAsk: Boolean): BydAdbAccess.State {
        if (!FeatureConfig.enableBydFeatures) {
            return BydAdbAccess.State.UNSUPPORTED
        }
        return BydAdbAccess.checkState(context, mayAsk)
    }

    override fun probe(context: Context, persist: Boolean): BydVehicleProbeOutcome {
        if (!FeatureConfig.enableBydFeatures) {
            return BydVehicleProbeOutcome(BydAdbAccess.State.UNSUPPORTED)
        }
        return BydVehicleCapabilityProbe.probe(context, persist)
    }

    override fun execute(name: String, block: () -> Unit) {
        if (!FeatureConfig.enableBydFeatures) return
        Thread(block, name).start()
    }
}

/** Replaced only by Robolectric tests; production always uses [AndroidBydVehicleSettingsBackend]. */
internal object BydVehicleSettingsBackendProvider {
    @Volatile var current: BydVehicleSettingsBackend = AndroidBydVehicleSettingsBackend

    fun reset() {
        current = AndroidBydVehicleSettingsBackend
    }
}

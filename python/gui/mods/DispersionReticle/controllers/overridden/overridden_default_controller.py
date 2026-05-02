# -*- coding: utf-8 -*-
import BattleReplay
import BigWorld
import Math
import constants
from AvatarInputHandler.gun_marker_ctrl import _DefaultGunMarkerController, _MARKER_FLAG, _makeWorldMatrix
from aih_constants import GUN_MARKER_TYPE

from ...utils import logger
from ...utils.reticle_registry import ReticleRegistry


class OverriddenDefaultGunMarkerController(_DefaultGunMarkerController):

    def __init__(self, gunMarkerType, dataProvider, isServer, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(OverriddenDefaultGunMarkerController, self).__init__(gunMarkerType, dataProvider, enabledFlag=enabledFlag)
        self._isServer = isServer

    def isClientController(self):
        return not self._isServer

    def isServerController(self):
        return self._isServer

    def update(self, *args, **kwargs):
        if len(args) == 4 and not kwargs:
            try:
                return self._updateWg(*args)
            except Exception as e:
                logger.error('[overridden_default_controller] Custom update failed: %s', e)
        return super(OverriddenDefaultGunMarkerController, self).update(*args, **kwargs)

    def _updateWg(self, markerType, gunMarkerInfo, supportMarkersInfo, relaxTime):
        super(_DefaultGunMarkerController, self).update(markerType, gunMarkerInfo, supportMarkersInfo, relaxTime)

        positionMatrix = Math.Matrix()
        positionMatrix.setTranslate(gunMarkerInfo.position)
        self._updateMatrixProvider(positionMatrix, relaxTime)

        size = super(OverriddenDefaultGunMarkerController, self)._getMarkerSize(gunMarkerInfo)
        size = self._interceptReplayLogic(size)

        sizeMultiplier = ReticleRegistry.getReticleSizeMultiplierFor(markerType)
        size = self._interceptSize(size, gunMarkerInfo.position) * sizeMultiplier

        positionMatrixForScale = BigWorld.checkAndRecalculateIfPositionInExtremeProjection(positionMatrix)
        worldMatrix = _makeWorldMatrix(positionMatrixForScale)
        markerHelperScale = BigWorld.markerHelperScale

        self._DefaultGunMarkerController__currentSize = (
            markerHelperScale(worldMatrix, size) * self._DefaultGunMarkerController__screenRatio
        )
        self._DefaultGunMarkerController__currentSizeOffset = (
            markerHelperScale(worldMatrix, gunMarkerInfo.sizeOffset) * self._DefaultGunMarkerController__screenRatio
        )

        shouldUpdateExtendedReticleSize = self._shouldUpdateExtendedReticleSize()

        self._dataProvider.updateSizes(
            self._DefaultGunMarkerController__currentSize,
            self._DefaultGunMarkerController__currentSizeOffset,
            relaxTime,
            self._DefaultGunMarkerController__offsetInertness
        )

        if self._DefaultGunMarkerController__offsetInertness == self._OFFSET_DEFAULT_INERTNESS:
            self._DefaultGunMarkerController__offsetInertness = self._OFFSET_SLOWDOWN_INERTNESS

        if shouldUpdateExtendedReticleSize:
            self._interceptPostUpdate(self._DefaultGunMarkerController__currentSize)

    def _getMarkerSize(self, gunMarkerInfo):
        size = super(OverriddenDefaultGunMarkerController, self)._getMarkerSize(gunMarkerInfo)
        size = self._interceptSize(size, gunMarkerInfo.position)
        sizeMultiplier = ReticleRegistry.getReticleSizeMultiplierFor(self._gunMarkerType)
        return size * sizeMultiplier

    def _interceptReplayLogic(self, size):
        try:
            replayCtrl = BattleReplay.g_replayCtrl
            if replayCtrl.isPlaying and replayCtrl.isClientReady:
                replaySize = self._replayReader(replayCtrl)()
                if replaySize != -1.0:
                    size = replaySize
            elif replayCtrl.isRecording:
                if self._areBothModesEnabled():
                    if replayCtrl.isServerAim and self._gunMarkerType == GUN_MARKER_TYPE.SERVER:
                        self._replayWriter(replayCtrl)(size)
                elif self._gunMarkerType in (GUN_MARKER_TYPE.CLIENT, GUN_MARKER_TYPE.DUAL_ACC):
                    self._replayWriter(replayCtrl)(size)
        except Exception:
            pass
        return size

    def _interceptPostUpdate(self, size):
        pass

    def _interceptSize(self, size, pos):
        return size

    def _shouldUpdateExtendedReticleSize(self):
        dataProviderSizeCache = getattr(BigWorld.player(), '_mod_dataProviderSizeCache', None)
        if dataProviderSizeCache is None:
            return True

        lastTime = dataProviderSizeCache.get(id(self._dataProvider), None)
        if lastTime is None:
            return True

        try:
            return BigWorld.time() - lastTime >= constants.SERVER_TICK_LENGTH
        except Exception:
            return True

    def _isClientModeEnabled(self):
        return self._gunMarkersFlags & _MARKER_FLAG.CLIENT_MODE_ENABLED

    def _isServerModeEnabled(self):
        return self._gunMarkersFlags & _MARKER_FLAG.SERVER_MODE_ENABLED

    def _areBothModesEnabled(self):
        return self._isClientModeEnabled() and self._isServerModeEnabled()

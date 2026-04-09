# -*- coding: utf-8 -*-
from AvatarInputHandler.gun_marker_ctrl import _DefaultGunMarkerController, _MARKER_FLAG

from ...utils.reticle_registry import ReticleRegistry


class OverriddenDefaultGunMarkerController(_DefaultGunMarkerController):

    def __init__(self, gunMarkerType, dataProvider, isServer, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(OverriddenDefaultGunMarkerController, self).__init__(gunMarkerType, dataProvider, enabledFlag=enabledFlag)
        self._isServer = isServer

    def isClientController(self):
        return not self._isServer

    def isServerController(self):
        return self._isServer

    def _getMarkerSize(self, gunMarkerInfo):
        size = super(OverriddenDefaultGunMarkerController, self)._getMarkerSize(gunMarkerInfo)
        size = self._interceptSize(size, gunMarkerInfo.position)
        sizeMultiplier = ReticleRegistry.getReticleSizeMultiplierFor(self._gunMarkerType)
        return size * sizeMultiplier

    def _interceptSize(self, size, pos):
        return size

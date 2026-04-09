# -*- coding: utf-8 -*-
from AvatarInputHandler import aih_global_binding
from AvatarInputHandler.gun_marker_ctrl import _GunMarkersDPFactory
from aih_constants import GUN_MARKER_TYPE

from . import ReticleSide


class VanillaReticle(object):

    def __init__(self, reticleType, gunMarkerType, reticleSide, standardDataProviderID):
        self._reticleType = reticleType
        self._gunMarkerType = gunMarkerType
        self._reticleSide = reticleSide
        self._standardDataProviderID = standardDataProviderID
        self._standardDataProviderRW = aih_global_binding.bindRW(self._standardDataProviderID)

    @property
    def gunMarkerType(self):
        return self._gunMarkerType

    @property
    def reticleType(self):
        return self._reticleType

    @property
    def markerNames(self):
        return self._reticleType.markerNames

    def isServerReticle(self):
        return self._reticleSide == ReticleSide.SERVER

    def getStandardDataProvider(self):
        if self._standardDataProviderRW.__get__(self) is None:
            self._standardDataProviderRW.__set__(self, _GunMarkersDPFactory._makeDefaultProvider())
        return self._standardDataProviderRW.__get__(self)

    def createDefaultMarkers(self, gunMarkerFactory, markerType):
        if markerType != GUN_MARKER_TYPE.UNDEFINED:
            return (
                gunMarkerFactory._createArcadeMarker(self._gunMarkerType, self.markerNames.arcadeGunMarkerName),
                gunMarkerFactory._createSniperMarker(self._gunMarkerType, self.markerNames.sniperGunMarkerName)
            )
        return (
            gunMarkerFactory._createArcadeMarker(GUN_MARKER_TYPE.UNDEFINED, self.markerNames.arcadeGunMarkerName),
            gunMarkerFactory._createSniperMarker(GUN_MARKER_TYPE.UNDEFINED, self.markerNames.sniperGunMarkerName)
        )

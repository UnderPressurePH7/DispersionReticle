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

    def _effectiveMarkerType(self, markerType):
        if markerType != GUN_MARKER_TYPE.UNDEFINED:
            return self._gunMarkerType
        return GUN_MARKER_TYPE.UNDEFINED

    def _createArcadeSniperMarkers(self, gunMarkerFactory, markerType, arcadeMarkerName, sniperMarkerName):
        if arcadeMarkerName is None or sniperMarkerName is None:
            return ()

        effectiveMarkerType = self._effectiveMarkerType(markerType)
        return (
            gunMarkerFactory._createArcadeMarker(effectiveMarkerType, arcadeMarkerName),
            gunMarkerFactory._createSniperMarker(effectiveMarkerType, sniperMarkerName)
        )

    def createDefaultMarkers(self, gunMarkerFactory, markerType):
        return self._createArcadeSniperMarkers(
            gunMarkerFactory,
            markerType,
            self.markerNames.arcadeGunMarkerName,
            self.markerNames.sniperGunMarkerName
        )

    def createDualGunMarkers(self, gunMarkerFactory, markerType):
        return self._createArcadeSniperMarkers(
            gunMarkerFactory,
            markerType,
            self.markerNames.dualGunArcadeGunMarkerName,
            self.markerNames.dualGunSniperGunMarkerName
        )

    def createTwinGunMarkers(self, gunMarkerFactory, markerType):
        return self._createArcadeSniperMarkers(
            gunMarkerFactory,
            markerType,
            self.markerNames.twinGunArcadeGunMarkerName,
            self.markerNames.twinGunSniperGunMarkerName
        )

    def createAccuracyGunMarkers(self, gunMarkerFactory, markerType):
        return self._createArcadeSniperMarkers(
            gunMarkerFactory,
            markerType,
            self.markerNames.accuracyGunArcadeGunMarkerName,
            self.markerNames.accuracyGunSniperGunMarkerName
        )

    def createChargeGunMarkers(self, gunMarkerFactory, markerType):
        return self._createArcadeSniperMarkers(
            gunMarkerFactory,
            markerType,
            self.markerNames.chargeGunArcadeGunMarkerName,
            self.markerNames.chargeGunSniperGunMarkerName
        )

    def createLowChargeShotGunMarkers(self, gunMarkerFactory, markerType):
        return self._createArcadeSniperMarkers(
            gunMarkerFactory,
            markerType,
            self.markerNames.lowChargeShotArcadeGunMarkerName,
            self.markerNames.lowChargeShotSniperGunMarkerName
        )

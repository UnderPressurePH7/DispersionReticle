# -*- coding: utf-8 -*-
from gui.Scaleform.daapi.view.battle.shared.crosshair import gm_factory
from gui.Scaleform.genConsts.GUN_MARKER_VIEW_CONSTANTS import GUN_MARKER_VIEW_CONSTANTS as _CONSTANTS


class ReticleSide(object):
    CLIENT = 0
    SERVER = 1


class MarkerNames(object):

    def __init__(self, arcadeGunMarkerName, sniperGunMarkerName):
        self.arcadeGunMarkerName = arcadeGunMarkerName
        self.sniperGunMarkerName = sniperGunMarkerName

    def getMarkerNames(self):
        return (self.arcadeGunMarkerName, self.sniperGunMarkerName)

    @staticmethod
    def createStandardMarkerNames():
        return MarkerNames(
            arcadeGunMarkerName=_CONSTANTS.ARCADE_GUN_MARKER_NAME,
            sniperGunMarkerName=_CONSTANTS.SNIPER_GUN_MARKER_NAME
        )

    @staticmethod
    def createMarkerNames(suffix):
        return MarkerNames(
            arcadeGunMarkerName='arcadeGunMarker' + suffix,
            sniperGunMarkerName='sniperGunMarker' + suffix
        )


class ReticleLinkages(object):

    @staticmethod
    def greenLinkagesProvider(markerNames):
        return {
            markerNames.arcadeGunMarkerName: _CONSTANTS.GUN_MARKER_LINKAGE,
            markerNames.sniperGunMarkerName: _CONSTANTS.GUN_MARKER_LINKAGE
        }


class ReticleType(object):

    def __init__(self, reticleId, markerNames, markerLinkagesProvider):
        self._reticleId = reticleId
        self._markerNames = markerNames
        self._markerLinkagesProvider = markerLinkagesProvider
        self.refreshLinkages()

    def refreshLinkages(self):
        reticleLinkages = self._markerLinkagesProvider(self._markerNames)
        gm_factory._GUN_MARKER_LINKAGES.update(reticleLinkages)

    @property
    def reticleId(self):
        return self._reticleId

    @property
    def markerNames(self):
        return self._markerNames


class ReticleTypes(object):
    VANILLA = ReticleType(
        reticleId=1,
        markerNames=MarkerNames.createStandardMarkerNames(),
        markerLinkagesProvider=ReticleLinkages.greenLinkagesProvider
    )
    FOCUSED = ReticleType(
        reticleId=2,
        markerNames=MarkerNames.createMarkerNames('Focused'),
        markerLinkagesProvider=ReticleLinkages.greenLinkagesProvider
    )

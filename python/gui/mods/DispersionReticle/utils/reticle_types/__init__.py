# -*- coding: utf-8 -*-
from gui.Scaleform.daapi.view.battle.shared.crosshair import gm_factory
from gui.Scaleform.genConsts.GUN_MARKER_VIEW_CONSTANTS import GUN_MARKER_VIEW_CONSTANTS as _CONSTANTS


def _getConstant(name, default=None):
    return getattr(_CONSTANTS, name, default)


def _optionalLinkages(*items):
    result = {}
    for markerName, linkage in items:
        if markerName is not None and linkage is not None:
            result[markerName] = linkage
    return result


class ReticleSide(object):
    CLIENT = 0
    SERVER = 1


class MarkerNames(object):

    def __init__(self, arcadeGunMarkerName, sniperGunMarkerName,
                 dualGunArcadeGunMarkerName=None, dualGunSniperGunMarkerName=None,
                 twinGunArcadeGunMarkerName=None, twinGunSniperGunMarkerName=None,
                 accuracyGunArcadeGunMarkerName=None, accuracyGunSniperGunMarkerName=None,
                 chargeGunArcadeGunMarkerName=None, chargeGunSniperGunMarkerName=None,
                 lowChargeShotArcadeGunMarkerName=None, lowChargeShotSniperGunMarkerName=None):
        self.arcadeGunMarkerName = arcadeGunMarkerName
        self.sniperGunMarkerName = sniperGunMarkerName

        self.dualGunArcadeGunMarkerName = dualGunArcadeGunMarkerName
        self.dualGunSniperGunMarkerName = dualGunSniperGunMarkerName

        self.twinGunArcadeGunMarkerName = twinGunArcadeGunMarkerName
        self.twinGunSniperGunMarkerName = twinGunSniperGunMarkerName

        self.accuracyGunArcadeGunMarkerName = accuracyGunArcadeGunMarkerName
        self.accuracyGunSniperGunMarkerName = accuracyGunSniperGunMarkerName

        self.chargeGunArcadeGunMarkerName = chargeGunArcadeGunMarkerName
        self.chargeGunSniperGunMarkerName = chargeGunSniperGunMarkerName

        self.lowChargeShotArcadeGunMarkerName = lowChargeShotArcadeGunMarkerName
        self.lowChargeShotSniperGunMarkerName = lowChargeShotSniperGunMarkerName

    def getMarkerNames(self):
        return (
            self.arcadeGunMarkerName,
            self.sniperGunMarkerName,
            self.dualGunArcadeGunMarkerName,
            self.dualGunSniperGunMarkerName,
            self.twinGunArcadeGunMarkerName,
            self.twinGunSniperGunMarkerName,
            self.accuracyGunArcadeGunMarkerName,
            self.accuracyGunSniperGunMarkerName,
            self.chargeGunArcadeGunMarkerName,
            self.chargeGunSniperGunMarkerName,
            self.lowChargeShotArcadeGunMarkerName,
            self.lowChargeShotSniperGunMarkerName
        )

    @staticmethod
    def createStandardMarkerNames():
        return MarkerNames(
            arcadeGunMarkerName=_CONSTANTS.ARCADE_GUN_MARKER_NAME,
            sniperGunMarkerName=_CONSTANTS.SNIPER_GUN_MARKER_NAME,
            dualGunArcadeGunMarkerName=_getConstant('DUAL_GUN_ARCADE_MARKER_NAME'),
            dualGunSniperGunMarkerName=_getConstant('DUAL_GUN_SNIPER_MARKER_NAME'),
            twinGunArcadeGunMarkerName=_getConstant('TWIN_GUN_ARCADE_MARKER_NAME'),
            twinGunSniperGunMarkerName=_getConstant('TWIN_GUN_SNIPER_MARKER_NAME'),
            accuracyGunArcadeGunMarkerName=_getConstant('ACCURACY_GUN_ARCADE_MARKER_NAME'),
            accuracyGunSniperGunMarkerName=_getConstant('ACCURACY_GUN_SNIPER_MARKER_NAME'),
            chargeGunArcadeGunMarkerName=_getConstant('CHARGE_GUN_ARCADE_MARKER_NAME'),
            chargeGunSniperGunMarkerName=_getConstant('CHARGE_GUN_SNIPER_MARKER_NAME'),
            lowChargeShotArcadeGunMarkerName=_getConstant('LOW_CHARGE_SHOT_GUN_ARCADE_MARKER_NAME'),
            lowChargeShotSniperGunMarkerName=_getConstant('LOW_CHARGE_SHOT_GUN_SNIPER_MARKER_NAME')
        )

    @staticmethod
    def createMarkerNames(suffix):
        return MarkerNames(
            arcadeGunMarkerName='arcadeGunMarker' + suffix,
            sniperGunMarkerName='sniperGunMarker' + suffix,
            dualGunArcadeGunMarkerName='arcadeDualGunMarker' + suffix,
            dualGunSniperGunMarkerName='sniperDualGunMarker' + suffix,
            twinGunArcadeGunMarkerName='arcadeTwinGunMarker' + suffix,
            twinGunSniperGunMarkerName='sniperTwinGunMarker' + suffix,
            accuracyGunArcadeGunMarkerName='arcadeAccuracyGunMarker' + suffix,
            accuracyGunSniperGunMarkerName='sniperAccuracyGunMarker' + suffix,
            chargeGunArcadeGunMarkerName='arcadeChargeGunMarker' + suffix,
            chargeGunSniperGunMarkerName='sniperChargeGunMarker' + suffix,
            lowChargeShotArcadeGunMarkerName='arcadeLowChargeShotGunMarker' + suffix,
            lowChargeShotSniperGunMarkerName='sniperLowChargeShotGunMarker' + suffix
        )


class ReticleLinkages(object):

    @staticmethod
    def greenLinkagesProvider(markerNames):
        defaultLinkage = _CONSTANTS.GUN_MARKER_LINKAGE
        return _optionalLinkages(
            (markerNames.arcadeGunMarkerName, defaultLinkage),
            (markerNames.sniperGunMarkerName, defaultLinkage),
            (markerNames.dualGunArcadeGunMarkerName,
             _getConstant('DUAL_GUN_ARCADE_MARKER_LINKAGE', defaultLinkage)),
            (markerNames.dualGunSniperGunMarkerName,
             _getConstant('DUAL_GUN_SNIPER_MARKER_LINKAGE', defaultLinkage)),
            (markerNames.twinGunArcadeGunMarkerName,
             _getConstant('TWIN_GUN_MARKER_LINKAGE', defaultLinkage)),
            (markerNames.twinGunSniperGunMarkerName,
             _getConstant('TWIN_GUN_MARKER_LINKAGE', defaultLinkage)),
            (markerNames.accuracyGunArcadeGunMarkerName,
             _getConstant('ACCURACY_GUN_MARKER_LINKAGE', defaultLinkage)),
            (markerNames.accuracyGunSniperGunMarkerName,
             _getConstant('ACCURACY_GUN_MARKER_LINKAGE', defaultLinkage)),
            (markerNames.chargeGunArcadeGunMarkerName,
             _getConstant('CHARGE_GUN_MARKER_LINKAGE', defaultLinkage)),
            (markerNames.chargeGunSniperGunMarkerName,
             _getConstant('CHARGE_GUN_MARKER_LINKAGE', defaultLinkage)),
            (markerNames.lowChargeShotArcadeGunMarkerName,
             _getConstant('LOW_CHARGE_SHOT_GUN_MARKER_LINKAGE', defaultLinkage)),
            (markerNames.lowChargeShotSniperGunMarkerName,
             _getConstant('LOW_CHARGE_SHOT_GUN_MARKER_LINKAGE', defaultLinkage))
        )


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

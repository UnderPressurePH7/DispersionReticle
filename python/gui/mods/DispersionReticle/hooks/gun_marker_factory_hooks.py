# -*- coding: utf-8 -*-
from gui.Scaleform.daapi.view.battle.shared.crosshair import gm_factory
from gui.Scaleform.daapi.view.battle.shared.crosshair.gm_factory import (
    _ControlMarkersFactory,
    _OptionalMarkersFactory,
    _EquipmentMarkersFactory
)

from ..settings.config_param import g_configParams
from ..utils import logger
from ..utils.reticle_registry import ReticleRegistry


class _DispersionControlMarkersFactory(_ControlMarkersFactory):

    def _appendFocusedMarkers(self, result, createMethodName):
        if not g_configParams.circleEnabled.value:
            return result

        createMethod = getattr(ReticleRegistry.FOCUSED_CLIENT, createMethodName, None)
        if createMethod is None:
            return result

        return result + createMethod(self, self._getMarkerType())

    def _createDefaultMarkers(self):
        result = super(_DispersionControlMarkersFactory, self)._createDefaultMarkers()
        return self._appendFocusedMarkers(result, 'createDefaultMarkers')

    def _createDualGunMarkers(self):
        result = super(_DispersionControlMarkersFactory, self)._createDualGunMarkers()
        return self._appendFocusedMarkers(result, 'createDualGunMarkers')

    def _createTwinGunMarkers(self):
        result = super(_DispersionControlMarkersFactory, self)._createTwinGunMarkers()
        return self._appendFocusedMarkers(result, 'createTwinGunMarkers')

    def _createAccuracyGunMarkers(self):
        result = super(_DispersionControlMarkersFactory, self)._createAccuracyGunMarkers()
        return self._appendFocusedMarkers(result, 'createAccuracyGunMarkers')

    def _createChargeGunMarkers(self):
        result = super(_DispersionControlMarkersFactory, self)._createChargeGunMarkers()
        return self._appendFocusedMarkers(result, 'createChargeGunMarkers')

    def _createLowChargeShotGunMarkers(self):
        result = super(_DispersionControlMarkersFactory, self)._createLowChargeShotGunMarkers()
        return self._appendFocusedMarkers(result, 'createLowChargeShotGunMarkers')


_originalFactories = None


def install():
    global _originalFactories
    _originalFactories = gm_factory._FACTORIES_COLLECTION
    gm_factory._FACTORIES_COLLECTION = (
        _DispersionControlMarkersFactory,
        _OptionalMarkersFactory,
        _EquipmentMarkersFactory
    )
    logger.debug('[gun_marker_factory_hooks] Installed')


def uninstall():
    global _originalFactories
    if _originalFactories is not None:
        gm_factory._FACTORIES_COLLECTION = _originalFactories
        _originalFactories = None
        logger.debug('[gun_marker_factory_hooks] Uninstalled')

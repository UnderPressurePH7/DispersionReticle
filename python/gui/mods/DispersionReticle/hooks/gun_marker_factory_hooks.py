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


_loggedFocusedCreateMethods = set()


class _DispersionControlMarkersFactory(_ControlMarkersFactory):

    def _callBaseMarkers(self, createMethodName):
        createMethod = getattr(super(_DispersionControlMarkersFactory, self), createMethodName, None)
        if createMethod is None:
            return ()
        return createMethod()

    def _appendFocusedMarkers(self, result, createMethodName):
        if not g_configParams.circleEnabled.value:
            return result

        createMethod = getattr(ReticleRegistry.FOCUSED_CLIENT, createMethodName, None)
        if createMethod is None:
            return result

        focusedMarkers = tuple(createMethod(self, self._getMarkerType()))
        if createMethodName not in _loggedFocusedCreateMethods:
            _loggedFocusedCreateMethods.add(createMethodName)
            logger.debug(
                '[gun_marker_factory_hooks] Appended %s focused markers via %s',
                len(focusedMarkers),
                createMethodName
            )
        return tuple(result) + focusedMarkers

    def _createDefaultMarkers(self):
        result = self._callBaseMarkers('_createDefaultMarkers')
        return self._appendFocusedMarkers(result, 'createDefaultMarkers')

    def _createDualGunMarkers(self):
        result = self._callBaseMarkers('_createDualGunMarkers')
        return self._appendFocusedMarkers(result, 'createDualGunMarkers')

    def _createTwinGunMarkers(self):
        result = self._callBaseMarkers('_createTwinGunMarkers')
        return self._appendFocusedMarkers(result, 'createTwinGunMarkers')

    def _createAccuracyGunMarkers(self):
        result = self._callBaseMarkers('_createAccuracyGunMarkers')
        return self._appendFocusedMarkers(result, 'createAccuracyGunMarkers')

    def _createChargeGunMarkers(self):
        result = self._callBaseMarkers('_createChargeGunMarkers')
        return self._appendFocusedMarkers(result, 'createChargeGunMarkers')

    def _createLowChargeShotGunMarkers(self):
        result = self._callBaseMarkers('_createLowChargeShotGunMarkers')
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

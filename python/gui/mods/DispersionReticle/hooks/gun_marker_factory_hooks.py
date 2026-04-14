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

    def _createDefaultMarkers(self):
        markerType = self._getMarkerType()
        result = super(_DispersionControlMarkersFactory, self)._createDefaultMarkers()
        if g_configParams.circleEnabled.value:
            result += ReticleRegistry.FOCUSED_CLIENT.createDefaultMarkers(self, markerType)
        return result


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

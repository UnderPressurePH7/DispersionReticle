# -*- coding: utf-8 -*-
from gui.Scaleform.daapi.view.battle.shared.crosshair.gm_factory import _GunMarkersFactory

from ..utils import logger, overrideIn
from ..utils.reticle_registry import ReticleRegistry


def install():
    @overrideIn(_GunMarkersFactory)
    def _getMarkerDataProvider(func, self, markerType):
        for reticle in ReticleRegistry.ADDITIONAL_RETICLES:
            if markerType == reticle.gunMarkerType:
                return reticle.getStandardDataProvider()
        return func(self, markerType)

    logger.debug('[data_provider_hooks] Installed')

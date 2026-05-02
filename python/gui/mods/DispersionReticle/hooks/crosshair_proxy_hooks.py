# -*- coding: utf-8 -*-
from aih_constants import GUN_MARKER_TYPE
from gui.battle_control.controllers.crosshair_proxy import CrosshairDataProxy

from ..utils import logger, overrideIn
from ..utils.reticle_registry import ReticleRegistry


def install():
    @overrideIn(CrosshairDataProxy)
    def __setGunMarkerState(func, self, markerType, value):
        func(self, markerType, value)

        isServerUpdate = (markerType == GUN_MARKER_TYPE.SERVER)
        for reticle in ReticleRegistry.ADDITIONAL_RETICLES:
            if reticle.isServerReticle() == isServerUpdate:
                self.onGunMarkerStateChanged(reticle.gunMarkerType, *value)

    logger.debug('[crosshair_proxy_hooks] Installed')

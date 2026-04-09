# -*- coding: utf-8 -*-
import AvatarInputHandler

from ..utils import logger, overrideIn
from ..utils.reticle_registry import ReticleRegistry


def install():
    @overrideIn(AvatarInputHandler.AvatarInputHandler)
    def updateClientGunMarker(func, self, gunMarkerInfo, supportMarkersInfo, relaxTime):
        func(self, gunMarkerInfo, supportMarkersInfo, relaxTime)
        ctrl = self._AvatarInputHandler__curCtrl
        for reticle in ReticleRegistry.ADDITIONAL_RETICLES:
            if reticle.isServerReticle():
                continue
            try:
                ctrl.updateGunMarker(reticle.gunMarkerType, gunMarkerInfo, supportMarkersInfo, relaxTime)
            except Exception as e:
                logger.error('[aih_hooks] Error updating reticle %s: %s', reticle.gunMarkerType, e)

    logger.debug('[aih_hooks] Installed')

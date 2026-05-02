# -*- coding: utf-8 -*-
import AvatarInputHandler
from AvatarInputHandler import aih_global_binding
from aih_constants import GUN_MARKER_FLAG

from ..controllers import AihUpdateType
from ..utils import logger, overrideIn
from ..utils.reticle_registry import ReticleRegistry


class _Descriptors(object):
    gunMarkersFlags = aih_global_binding.bindRO(AvatarInputHandler._BINDING_ID.GUN_MARKERS_FLAGS)


_descriptors = _Descriptors()


def _areBothModesEnabled():
    return _isClientModeEnabled() and _isServerModeEnabled()


def _isClientModeEnabled():
    return _descriptors.gunMarkersFlags & GUN_MARKER_FLAG.CLIENT_MODE_ENABLED


def _isServerModeEnabled():
    return _descriptors.gunMarkersFlags & GUN_MARKER_FLAG.SERVER_MODE_ENABLED


def install():
    @overrideIn(AvatarInputHandler.AvatarInputHandler)
    def updateClientGunMarker(func, self, gunMarkerInfo, supportMarkersInfo, relaxTime):
        from ..controllers.wg_gun_marker_decorator import WgDispersionGunMarkersDecorator
        WgDispersionGunMarkersDecorator.currentUpdateType = AihUpdateType.CLIENT

        ctrl = getattr(self, '_AvatarInputHandler__curCtrl', None)
        if ctrl is None or not hasattr(ctrl, 'updateGunMarker'):
            return

        for reticle in ReticleRegistry.ALL_RETICLES:
            if _areBothModesEnabled() and reticle.isServerReticle():
                continue
            try:
                ctrl.updateGunMarker(reticle.gunMarkerType, gunMarkerInfo, supportMarkersInfo, relaxTime)
            except Exception as e:
                logger.error('[aih_hooks] Error updating reticle %s: %s', reticle.gunMarkerType, e)

    @overrideIn(AvatarInputHandler.AvatarInputHandler)
    def updateServerGunMarker(func, self, gunMarkerInfo, supportMarkersInfo, relaxTime):
        from ..controllers.wg_gun_marker_decorator import WgDispersionGunMarkersDecorator
        WgDispersionGunMarkersDecorator.currentUpdateType = AihUpdateType.SERVER

        ctrl = getattr(self, '_AvatarInputHandler__curCtrl', None)
        if ctrl is None or not hasattr(ctrl, 'updateGunMarker'):
            return

        for reticle in ReticleRegistry.ALL_RETICLES:
            if _areBothModesEnabled() and not reticle.isServerReticle():
                continue
            try:
                ctrl.updateGunMarker(reticle.gunMarkerType, gunMarkerInfo, supportMarkersInfo, relaxTime)
            except Exception as e:
                logger.error('[aih_hooks] Error updating reticle %s: %s', reticle.gunMarkerType, e)

    logger.debug('[aih_hooks] Installed')

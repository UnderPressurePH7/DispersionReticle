# -*- coding: utf-8 -*-
import BigWorld
from AvatarInputHandler.gun_marker_ctrl import _MARKER_FLAG

from ...utils import logger
from ..overridden.overridden_default_controller import OverriddenDefaultGunMarkerController
from . import getFocusedDispersionSize


_sizeDebugLogged = False
_sizeErrorLogged = False


class FocusedDefaultGunMarkerController(OverriddenDefaultGunMarkerController):

    def __init__(self, reticle, dataProvider, enabledFlag=_MARKER_FLAG.UNDEFINED):
        super(FocusedDefaultGunMarkerController, self).__init__(
            reticle.gunMarkerType,
            dataProvider,
            reticle.isServerReticle(),
            enabledFlag=enabledFlag
        )
        self._reticle = reticle

    def _interceptSize(self, size, pos):
        global _sizeDebugLogged, _sizeErrorLogged

        try:
            focusedSize = getFocusedDispersionSize(pos)
            if not _sizeDebugLogged:
                logger.debug('[focused] Marker size current=%s focused=%s', size, focusedSize)
                _sizeDebugLogged = True
            return focusedSize
        except Exception as e:
            if not _sizeErrorLogged:
                logger.error('[focused] Focused size calculation failed: %s', e)
                _sizeErrorLogged = True
            return size

    def _interceptPostUpdate(self, size):
        try:
            player = BigWorld.player()
            if player is not None:
                cache = getattr(player, '_mod_dataProviderSizeCache', None)
                if cache is None:
                    cache = {}
                    player._mod_dataProviderSizeCache = cache
                cache[id(self._dataProvider)] = BigWorld.time()
        except Exception as e:
            logger.error('[focused] _interceptPostUpdate cache write failed: %s', e)

    def _shouldUpdateExtendedReticleSize(self):
        return True

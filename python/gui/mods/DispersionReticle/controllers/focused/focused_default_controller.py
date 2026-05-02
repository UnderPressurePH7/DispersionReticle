# -*- coding: utf-8 -*-
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

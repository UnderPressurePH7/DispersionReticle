# -*- coding: utf-8 -*-
from AvatarInputHandler.gun_marker_ctrl import _MARKER_FLAG

from ..overridden.overridden_default_controller import OverriddenDefaultGunMarkerController
from . import getFocusedDispersionSize


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
        try:
            return getFocusedDispersionSize(pos)
        except Exception:
            return size

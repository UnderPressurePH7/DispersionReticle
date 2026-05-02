# -*- coding: utf-8 -*-
import BattleReplay
from AvatarInputHandler import gun_marker_ctrl

from ..utils import logger, overrideIn
from ..utils.reticle_registry import ReticleRegistry
from ..controllers.focused.focused_default_controller import FocusedDefaultGunMarkerController
from ..controllers.wg_gun_marker_decorator import WgDispersionGunMarkersDecorator


def install():
    @overrideIn(gun_marker_ctrl)
    def createGunMarker(func, isStrategic):
        decorator = func(isStrategic)
        if isStrategic:
            return decorator

        clientMarker = decorator._GunMarkersDecorator__clientMarker
        serverMarker = decorator._GunMarkersDecorator__serverMarker
        dualAccMarker = decorator._GunMarkersDecorator__dualAccMarker

        focusedClientController = FocusedDefaultGunMarkerController(
            ReticleRegistry.FOCUSED_CLIENT,
            ReticleRegistry.FOCUSED_CLIENT.getStandardDataProvider()
        )

        return WgDispersionGunMarkersDecorator(
            clientMarker, serverMarker, dualAccMarker, focusedClientController
        )

    @overrideIn(gun_marker_ctrl)
    def useServerGunMarker(func):
        if BattleReplay.g_replayCtrl.isPlaying:
            return False
        return func()

    @overrideIn(gun_marker_ctrl)
    def useClientGunMarker(func):
        if BattleReplay.g_replayCtrl.isPlaying:
            return True
        return func()

    @overrideIn(gun_marker_ctrl)
    def useDefaultGunMarkers(func):
        if gun_marker_ctrl.useClientGunMarker() and gun_marker_ctrl.useServerGunMarker():
            return False
        return func()

    logger.debug('[gun_marker_ctrl_hooks] Installed')

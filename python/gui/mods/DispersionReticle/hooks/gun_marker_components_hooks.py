# -*- coding: utf-8 -*-
from gui.Scaleform.daapi.view.battle.shared.crosshair.gm_components import GunMarkersComponents
from gui.Scaleform.genConsts.GUN_MARKER_VIEW_CONSTANTS import GUN_MARKER_VIEW_CONSTANTS as _CONSTANTS

from ..utils import logger, overrideIn
from ..utils.reticle_registry import ReticleRegistry


def _appendMarkerNames(result, markerNames):
    for name in markerNames.getMarkerNames():
        if name is not None and name not in result:
            result.append(name)


def _appendConstant(result, constName):
    name = getattr(_CONSTANTS, constName, None)
    if name is not None and name not in result:
        result.append(name)


def _buildPriority():
    result = []

    # Lower index is rendered later after reverse sort, so keep focused on top.
    _appendMarkerNames(result, ReticleRegistry.FOCUSED_CLIENT.markerNames)
    _appendMarkerNames(result, ReticleRegistry.VANILLA_CLIENT.markerNames)

    for constName in (
            'DUAL_GUN_ARCADE_MARKER_NAME',
            'DUAL_GUN_SNIPER_MARKER_NAME',
            'ARCADE_DUAL_ACC_GUN_MARKER_NAME',
            'SNIPER_DUAL_ACC_GUN_MARKER_NAME',
            'TWIN_GUN_ARCADE_MARKER_NAME',
            'TWIN_GUN_SNIPER_MARKER_NAME',
            'ACCURACY_GUN_ARCADE_MARKER_NAME',
            'ACCURACY_GUN_SNIPER_MARKER_NAME',
            'CHARGE_GUN_ARCADE_MARKER_NAME',
            'CHARGE_GUN_SNIPER_MARKER_NAME',
            'LOW_CHARGE_SHOT_GUN_ARCADE_MARKER_NAME',
            'LOW_CHARGE_SHOT_GUN_SNIPER_MARKER_NAME'):
        _appendConstant(result, constName)

    return result


def install():
    priority = _buildPriority()

    def positionInPriorityList(viewSetting):
        name = getattr(viewSetting, 'name', None)
        try:
            return priority.index(name)
        except ValueError:
            return 9999

    @overrideIn(GunMarkersComponents)
    def getViewSettings(func, self):
        viewSettings = func(self)
        viewSettings.sort(key=positionInPriorityList, reverse=True)
        return viewSettings

    logger.debug('[gun_marker_components_hooks] Installed')

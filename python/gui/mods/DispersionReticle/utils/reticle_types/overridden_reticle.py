# -*- coding: utf-8 -*-
from AvatarInputHandler.aih_global_binding import BINDING_ID, _Observable, _DEFAULT_VALUES
from gui.battle_control.controllers import crosshair_proxy

from .vanilla_reticle import VanillaReticle


_registeredIDs = []


def _nextFreeID():
    existing = BINDING_ID.RANGE
    base = max(existing) if existing else 6000
    return base + 1


class OverriddenReticle(VanillaReticle):

    def __init__(self, reticleType, gunMarkerType, reticleSide):
        nextID = _nextFreeID()

        BINDING_ID.RANGE += (nextID,)
        _DEFAULT_VALUES[nextID] = lambda: _Observable(None)
        crosshair_proxy._GUN_MARKERS_SET_IDS += (nextID,)
        _registeredIDs.append(nextID)

        super(OverriddenReticle, self).__init__(
            reticleType=reticleType,
            gunMarkerType=gunMarkerType,
            reticleSide=reticleSide,
            standardDataProviderID=nextID
        )


def cleanupOverriddenReticles():
    global _registeredIDs
    if not _registeredIDs:
        return
    ids = set(_registeredIDs)
    try:
        BINDING_ID.RANGE = tuple(i for i in BINDING_ID.RANGE if i not in ids)
    except Exception:
        pass
    for i in ids:
        _DEFAULT_VALUES.pop(i, None)
    try:
        crosshair_proxy._GUN_MARKERS_SET_IDS = tuple(
            i for i in crosshair_proxy._GUN_MARKERS_SET_IDS if i not in ids
        )
    except Exception:
        pass
    _registeredIDs = []

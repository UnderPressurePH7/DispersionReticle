# -*- coding: utf-8 -*-
from AvatarInputHandler.aih_global_binding import BINDING_ID, _Observable, _DEFAULT_VALUES
from gui.battle_control.controllers import crosshair_proxy

from .vanilla_reticle import VanillaReticle


class OverriddenReticle(VanillaReticle):

    NEXT_DATA_PROVIDER_ID = 6114

    def __init__(self, reticleType, gunMarkerType, reticleSide):
        nextStandardDataProviderID = OverriddenReticle.NEXT_DATA_PROVIDER_ID
        OverriddenReticle.NEXT_DATA_PROVIDER_ID += 1

        BINDING_ID.RANGE += (nextStandardDataProviderID,)

        _DEFAULT_VALUES.update({
            nextStandardDataProviderID: lambda: _Observable(None),
        })

        crosshair_proxy._GUN_MARKERS_SET_IDS += (nextStandardDataProviderID,)

        super(OverriddenReticle, self).__init__(
            reticleType=reticleType,
            gunMarkerType=gunMarkerType,
            reticleSide=reticleSide,
            standardDataProviderID=nextStandardDataProviderID
        )

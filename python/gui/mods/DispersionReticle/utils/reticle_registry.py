# -*- coding: utf-8 -*-
from AvatarInputHandler.aih_global_binding import BINDING_ID

from ..settings.config_param import g_configParams
from .reticle_types import ReticleSide, ReticleTypes
from .reticle_types.vanilla_reticle import VanillaReticle
from .reticle_types.overridden_reticle import OverriddenReticle


WOT_RETICLE_SCALE = 1.71


class ReticleRegistry(object):

    VANILLA_CLIENT = VanillaReticle(
        reticleType=ReticleTypes.VANILLA,
        gunMarkerType=1,
        reticleSide=ReticleSide.CLIENT,
        standardDataProviderID=BINDING_ID.CLIENT_GUN_MARKER_DATA_PROVIDER
    )

    FOCUSED_CLIENT = OverriddenReticle(
        reticleType=ReticleTypes.FOCUSED,
        gunMarkerType=6,
        reticleSide=ReticleSide.CLIENT
    )

    ADDITIONAL_RETICLES = [FOCUSED_CLIENT]
    ALL_RETICLES = [VANILLA_CLIENT] + ADDITIONAL_RETICLES

    @classmethod
    def isAdditionalReticle(cls, gunMarkerType):
        for reticle in cls.ADDITIONAL_RETICLES:
            if reticle.gunMarkerType == gunMarkerType:
                return True
        return False

    @classmethod
    def getReticleByMarkerType(cls, gunMarkerType):
        for reticle in cls.ALL_RETICLES:
            if reticle.gunMarkerType == gunMarkerType:
                return reticle
        return None

    @classmethod
    def getReticleSizeMultiplierFor(cls, gunMarkerType):
        if not g_configParams.reticleSizeEnabled.value:
            return 1.0
        sizeMultiplier = float(g_configParams.reticleSizePercent.value)
        return 1.0 / (1.0 + (WOT_RETICLE_SCALE - 1.0) * (1.0 - sizeMultiplier))

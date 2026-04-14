# -*- coding: utf-8 -*-
from .utils import logger


def initialize():
    from .flash.dispersion_flash import registerFlashComponents
    registerFlashComponents()

    from .hooks import install_hooks
    install_hooks()
    logger.info('[DispersionReticle] Initialized')


def finalize():
    from .flash.dispersion_flash import unregisterFlashComponents
    unregisterFlashComponents()

    from .hooks import uninstall_hooks
    uninstall_hooks()

    from .utils.reticle_types.overridden_reticle import cleanupOverriddenReticles
    cleanupOverriddenReticles()

    from .settings import g_config
    g_config.fini()
    logger.info('[DispersionReticle] Finalized')

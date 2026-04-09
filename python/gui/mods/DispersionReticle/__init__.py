# -*- coding: utf-8 -*-
from .utils import logger


def initialize():
    from .flash.dispersion_flash import registerFlashComponents
    registerFlashComponents()

    from .settings import g_config
    from .hooks import install_hooks
    install_hooks()
    logger.info('[DispersionReticle] Initialized')


def finalize():
    from .flash.dispersion_flash import unregisterFlashComponents
    unregisterFlashComponents()

    from .settings import g_config
    from .hooks import uninstall_hooks
    uninstall_hooks()
    g_config.fini()
    logger.info('[DispersionReticle] Finalized')

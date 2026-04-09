# -*- coding: utf-8 -*-
from ..utils import logger, restore_overrides


def install_hooks():
    try:
        from . import gun_marker_factory_hooks
        from . import data_provider_hooks
        from . import gun_marker_ctrl_hooks
        from . import crosshair_proxy_hooks
        from . import aih_hooks
        from . import crosshair_hooks

        gun_marker_factory_hooks.install()
        data_provider_hooks.install()
        gun_marker_ctrl_hooks.install()
        crosshair_proxy_hooks.install()
        aih_hooks.install()
        crosshair_hooks.install()
        logger.debug('[hooks] All hooks installed')
    except Exception as e:
        logger.error('[hooks] Failed to install hooks: %s', e)
        import traceback
        logger.error('[hooks] Traceback: %s', traceback.format_exc())


def uninstall_hooks():
    try:
        restore_overrides()
        logger.debug('[hooks] All hooks uninstalled')
    except Exception as e:
        logger.error('[hooks] Failed to uninstall hooks: %s', e)

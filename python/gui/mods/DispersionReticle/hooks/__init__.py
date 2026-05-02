# -*- coding: utf-8 -*-
from ..utils import logger, restore_overrides


_installedModules = []


def _getHookModules():
    from . import gun_marker_factory_hooks
    from . import gun_marker_components_hooks
    from . import data_provider_hooks
    from . import gun_marker_ctrl_hooks
    from . import crosshair_proxy_hooks
    from . import aih_hooks
    from . import crosshair_hooks
    return [
        gun_marker_factory_hooks,
        gun_marker_components_hooks,
        data_provider_hooks,
        gun_marker_ctrl_hooks,
        crosshair_proxy_hooks,
        aih_hooks,
        crosshair_hooks,
    ]


def install_hooks():
    global _installedModules
    modules = _getHookModules()
    installed = []
    try:
        for mod in modules:
            mod.install()
            installed.append(mod)
        _installedModules = installed
        logger.debug('[hooks] All hooks installed')
    except Exception as e:
        logger.error('[hooks] Install failed, rolling back: %s', e)
        import traceback
        logger.error('[hooks] Traceback: %s', traceback.format_exc())
        for mod in reversed(installed):
            try:
                if hasattr(mod, 'uninstall'):
                    mod.uninstall()
            except Exception as ee:
                logger.error('[hooks] Rollback error in %s: %s', mod.__name__, ee)
        try:
            restore_overrides()
        except Exception:
            pass
        _installedModules = []
        raise


def uninstall_hooks():
    global _installedModules
    try:
        for mod in reversed(_installedModules):
            try:
                if hasattr(mod, 'uninstall'):
                    mod.uninstall()
            except Exception as e:
                logger.error('[hooks] Uninstall error in %s: %s', mod.__name__, e)
        _installedModules = []
        restore_overrides()
        logger.debug('[hooks] All hooks uninstalled')
    except Exception as e:
        logger.error('[hooks] Failed to uninstall hooks: %s', e)

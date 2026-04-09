# -*- coding: utf-8 -*-
import BigWorld
from ..utils import logger, override, cancelCallbackSafe
from ..settings.config_param import g_configParams


_dispersionFlash = None
_updateCallbackId = None

_guiVisible = True
_statsPopupShown = False
_killCamActive = False
_isPlayerDead = False
_lastPushedVisible = None
_eventsSubscribed = False
_killCamCtrl = None
_interfaceScale = 1.0
_scalePushed = False
_interfaceScaleCtrl = None


def _computeVisible():
    return _guiVisible and (not _statsPopupShown) and (not _killCamActive) and (not _isPlayerDead)


def _pushVisibility():
    global _lastPushedVisible
    if _dispersionFlash is None or not _dispersionFlash.isCreated():
        return
    visible = _computeVisible()
    if visible == _lastPushedVisible:
        return
    _lastPushedVisible = visible
    try:
        _dispersionFlash.setReductionVisible(visible)
    except Exception as e:
        logger.error('[crosshair_hooks] Error pushing visibility: %s', e)


def _onGUIVisibility(event):
    global _guiVisible
    try:
        _guiVisible = bool(event.ctx.get('visible', True))
    except Exception:
        _guiVisible = True
    _pushVisibility()


def _onFullStats(event):
    global _statsPopupShown
    try:
        _statsPopupShown = bool(event.ctx.get('isDown', False))
    except Exception:
        _statsPopupShown = False
    _pushVisibility()


def _pushInterfaceScale():
    global _scalePushed
    if _dispersionFlash is None or not _dispersionFlash.isCreated():
        return
    try:
        _dispersionFlash.setInterfaceScale(_interfaceScale)
        _scalePushed = True
    except Exception as e:
        logger.error('[crosshair_hooks] Error pushing interface scale: %s', e)


def _onInterfaceScaleChanged(scale):
    global _interfaceScale
    try:
        _interfaceScale = float(scale)
    except Exception:
        _interfaceScale = 1.0
    _pushInterfaceScale()


def _onKillCamStateChanged(state, *a, **kw):
    global _killCamActive
    try:
        from gui.shared.events import DeathCamEvent
        _s = DeathCamEvent.State
        _killCamActive = (_s.STARTING.value <= state.value) and (state.value < _s.FINISHED.value)
    except Exception:
        _killCamActive = False
    _pushVisibility()


def _subscribeBattleEvents():
    global _eventsSubscribed, _killCamCtrl
    if _eventsSubscribed:
        return
    try:
        from gui.shared import g_eventBus, EVENT_BUS_SCOPE
        from gui.shared.events import GameEvent
        g_eventBus.addListener(GameEvent.GUI_VISIBILITY, _onGUIVisibility, scope=EVENT_BUS_SCOPE.BATTLE)
        g_eventBus.addListener(GameEvent.FULL_STATS, _onFullStats, scope=EVENT_BUS_SCOPE.BATTLE)
        _eventsSubscribed = True
    except Exception as e:
        logger.error('[crosshair_hooks] Error subscribing to event bus: %s', e)

    try:
        from helpers import dependency
        from skeletons.gui.battle_session import IBattleSessionProvider
        sessionProvider = dependency.instance(IBattleSessionProvider)
        killCamCtrl = getattr(sessionProvider.shared, 'killCamCtrl', None)
        if killCamCtrl is not None:
            killCamCtrl.onKillCamModeStateChanged += _onKillCamStateChanged
            _killCamCtrl = killCamCtrl
    except Exception as e:
        logger.error('[crosshair_hooks] Error subscribing to killCamCtrl: %s', e)

    global _interfaceScale, _interfaceScaleCtrl
    try:
        from helpers import dependency
        from skeletons.account_helpers.settings_core import ISettingsCore
        settingsCore = dependency.instance(ISettingsCore)
        ifaceScale = settingsCore.interfaceScale
        try:
            _interfaceScale = round(float(ifaceScale.get()), 2)
        except Exception:
            _interfaceScale = 1.0
        ifaceScale.onScaleChanged += _onInterfaceScaleChanged
        _interfaceScaleCtrl = ifaceScale
    except Exception as e:
        logger.error('[crosshair_hooks] Error subscribing to interfaceScale: %s', e)


def _unsubscribeBattleEvents():
    global _eventsSubscribed, _killCamCtrl
    if _eventsSubscribed:
        try:
            from gui.shared import g_eventBus, EVENT_BUS_SCOPE
            from gui.shared.events import GameEvent
            g_eventBus.removeListener(GameEvent.GUI_VISIBILITY, _onGUIVisibility, scope=EVENT_BUS_SCOPE.BATTLE)
            g_eventBus.removeListener(GameEvent.FULL_STATS, _onFullStats, scope=EVENT_BUS_SCOPE.BATTLE)
        except Exception as e:
            logger.error('[crosshair_hooks] Error unsubscribing from event bus: %s', e)
        _eventsSubscribed = False

    if _killCamCtrl is not None:
        try:
            _killCamCtrl.onKillCamModeStateChanged -= _onKillCamStateChanged
        except Exception:
            pass
        _killCamCtrl = None

    global _interfaceScaleCtrl
    if _interfaceScaleCtrl is not None:
        try:
            _interfaceScaleCtrl.onScaleChanged -= _onInterfaceScaleChanged
        except Exception:
            pass
        _interfaceScaleCtrl = None


def _resetVisibilityState():
    global _guiVisible, _statsPopupShown, _killCamActive, _isPlayerDead, _lastPushedVisible, _scalePushed
    _guiVisible = True
    _statsPopupShown = False
    _killCamActive = False
    _isPlayerDead = False
    _lastPushedVisible = None
    _scalePushed = False


def _getAimingPercent():
    try:
        player = BigWorld.player()
        if player is None:
            return 100.0

        gunRotator = getattr(player, 'gunRotator', None)
        if gunRotator is None:
            return 100.0

        currentAngle = getattr(gunRotator, 'dispersionAngle', 0.0)

        vehicleDesc = getattr(player, 'vehicleTypeDescriptor', None)
        if vehicleDesc is None:
            vehicleDesc = player._PlayerAvatar__getDetailedVehicleDescriptor()

        shotDispersionAngle = vehicleDesc.gun.shotDispersionAngle
        shotDispMultiplierFactor = player._PlayerAvatar__dispersionInfo[0]
        focusedAngle = shotDispersionAngle * shotDispMultiplierFactor

        if focusedAngle <= 0.0:
            return 100.0

        if currentAngle <= focusedAngle:
            return 100.0

        percent = (focusedAngle / currentAngle) * 100.0
        return max(0.0, min(100.0, percent))

    except Exception:
        return 100.0


def _periodicUpdate():
    global _updateCallbackId, _isPlayerDead

    try:
        if (not _scalePushed) and _dispersionFlash is not None and _dispersionFlash.isCreated():
            _pushInterfaceScale()

        if not _isPlayerDead:
            try:
                player = BigWorld.player()
                if player is not None and hasattr(player, 'isVehicleAlive') and not player.isVehicleAlive:
                    _isPlayerDead = True
                    _pushVisibility()
            except Exception:
                pass

        if (g_configParams.reductionEnabled.value
                and _dispersionFlash is not None
                and _dispersionFlash.isCreated()
                and _computeVisible()):
            aimingPercent = _getAimingPercent()
            from ..settings.translations import getTranslation
            aimedLabel = getTranslation('reduction.aimed')
            secSuffix = getTranslation('reduction.sec')

            if aimingPercent >= 99.5:
                timeLabel = ''
            else:
                try:
                    player = BigWorld.player()
                    aimingTime = player._PlayerAvatar__dispersionInfo[5]
                    remaining = aimingTime * (1.0 - aimingPercent / 100.0)
                    timeLabel = '%.1f %s' % (remaining, secSuffix)
                except Exception:
                    timeLabel = ''
            percentLabel = '%d%%' % int(aimingPercent)
            _dispersionFlash.updateReduction(aimingPercent, timeLabel, percentLabel, aimedLabel)

    except Exception as e:
        logger.error('[crosshair_hooks] Error in periodicUpdate: %s', e)

    _updateCallbackId = BigWorld.callback(0.1, _periodicUpdate)


def _startPeriodicUpdate():
    global _updateCallbackId
    _stopPeriodicUpdate()
    _updateCallbackId = BigWorld.callback(0.1, _periodicUpdate)


def _stopPeriodicUpdate():
    global _updateCallbackId
    cancelCallbackSafe(_updateCallbackId)
    _updateCallbackId = None


def install():
    from gui.Scaleform.daapi.view.battle.shared.crosshair.container import CrosshairPanelContainer
    from ..flash.dispersion_flash import DispersionFlash

    global _dispersionFlash
    _dispersionFlash = DispersionFlash()

    @override(CrosshairPanelContainer, '_populate')
    def populate(origFunc, self, *args, **kwargs):
        result = origFunc(self, *args, **kwargs)
        try:
            _resetVisibilityState()
            if _dispersionFlash is not None:
                _dispersionFlash.create()
            _subscribeBattleEvents()
            _startPeriodicUpdate()
        except Exception as e:
            logger.error('[crosshair_hooks] Error in populate: %s', e)
        return result

    @override(CrosshairPanelContainer, '_dispose')
    def dispose(origFunc, self, *args, **kwargs):
        try:
            _stopPeriodicUpdate()
            _unsubscribeBattleEvents()
            if _dispersionFlash is not None:
                _dispersionFlash.destroy()
        except Exception as e:
            logger.error('[crosshair_hooks] Error in dispose: %s', e)
        return origFunc(self, *args, **kwargs)

    from ..settings import g_config
    g_config.onConfigChanged += _onConfigChanged

    logger.debug('[crosshair_hooks] Installed')


def _onConfigChanged():
    _pushReductionConfig()


def _pushReductionConfig():
    if _dispersionFlash is None or not _dispersionFlash.isCreated():
        return
    try:
        _dispersionFlash.setReductionConfig(
            g_configParams.reductionEnabled.value,
            g_configParams.reductionStyle.value
        )
    except Exception as e:
        logger.error('[crosshair_hooks] Error pushing reduction config: %s', e)

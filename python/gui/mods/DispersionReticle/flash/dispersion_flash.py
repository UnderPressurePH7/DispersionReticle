# -*- coding: utf-8 -*-
import BigWorld
from ..utils import logger

try:
    import Settings
except ImportError:
    Settings = None

from frameworks.wulf import WindowLayer
from gui.Scaleform.framework import g_entitiesFactories, ScopeTemplates, ViewSettings
from gui.Scaleform.framework.entities.View import View
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent
from gui.Scaleform.framework.managers.loaders import SFViewLoadParams
from gui.shared.personality import ServicesLocator

PREFS_SECTION = 'DispersionReticle'

_INJECTOR_LINKAGE = 'DispersionReticleInjector'
_COMPONENT_LINKAGE = 'DispersionReticleComponent'
_SWF_PATH = 'DispersionReticle.swf'


class _InjectorView(View):
    _g_flash = None

    def _populate(self):
        super(_InjectorView, self)._populate()
        if _InjectorView._g_flash:
            _InjectorView._g_flash._onInjectorReady(self)

    def _dispose(self):
        if _InjectorView._g_flash:
            _InjectorView._g_flash._onInjectorDisposed()
        super(_InjectorView, self)._dispose()

    def py_onDragEnd(self, offsetX, offsetY):
        if _InjectorView._g_flash:
            _InjectorView._g_flash.onDragEnd(offsetX, offsetY)


class _ComponentView(BaseDAAPIComponent):
    _g_flash = None

    def _populate(self):
        super(_ComponentView, self)._populate()
        if _ComponentView._g_flash:
            _ComponentView._g_flash._onFlashReady(self)

    def _dispose(self):
        if _ComponentView._g_flash:
            _ComponentView._g_flash._onFlashDisposed()
        super(_ComponentView, self)._dispose()

    def as_setReductionData(self, aimingPercent, timeLabel, percentLabel, aimedLabel):
        if self._isDAAPIInited():
            self.flashObject.as_setReductionData(aimingPercent, timeLabel, percentLabel, aimedLabel)

    def as_setReductionConfig(self, enabled, style):
        if self._isDAAPIInited():
            self.flashObject.as_setReductionConfig(enabled, style)

    def as_setReductionVisible(self, visible):
        if self._isDAAPIInited():
            self.flashObject.as_setReductionVisible(bool(visible))

    def as_setReductionOffset(self, offsetX, offsetY):
        if self._isDAAPIInited():
            self.flashObject.as_setReductionOffset(offsetX, offsetY)

    def as_setInterfaceScale(self, scale):
        if self._isDAAPIInited():
            self.flashObject.as_setInterfaceScale(float(scale))


def registerFlashComponents():
    try:
        g_entitiesFactories.addSettings(ViewSettings(
            _INJECTOR_LINKAGE, _InjectorView, _SWF_PATH,
            WindowLayer.WINDOW, None, ScopeTemplates.GLOBAL_SCOPE
        ))
        g_entitiesFactories.addSettings(ViewSettings(
            _COMPONENT_LINKAGE, _ComponentView, None,
            WindowLayer.UNDEFINED, None, ScopeTemplates.DEFAULT_SCOPE
        ))
        logger.debug('[DispersionFlash] Flash components registered')
    except Exception as e:
        logger.error('[DispersionFlash] Failed to register: %s', e)


def unregisterFlashComponents():
    for linkage in (_INJECTOR_LINKAGE, _COMPONENT_LINKAGE):
        try:
            g_entitiesFactories.removeSettings(linkage)
        except Exception:
            pass


class DispersionFlash(object):

    def __init__(self):
        self._injectorView = None
        self._componentView = None
        self._flashReady = False
        self._isActive = False
        self._sessionId = 0

    def create(self):
        if self._isActive:
            return

        self._sessionId += 1
        self._isActive = True

        _InjectorView._g_flash = self
        _ComponentView._g_flash = self

        self._injectFlash()

    def destroy(self):
        self._sessionId += 1
        self._isActive = False

        _InjectorView._g_flash = None
        _ComponentView._g_flash = None

        self._injectorView = None
        self._componentView = None
        self._flashReady = False

    def isCreated(self):
        return self._flashReady and self._componentView is not None

    def _injectFlash(self, attempt=0):
        sessionId = self._sessionId
        try:
            app = ServicesLocator.appLoader.getDefBattleApp()
            if app:
                app.loadView(SFViewLoadParams(_INJECTOR_LINKAGE))
                logger.debug('[DispersionFlash] loadView called')
                return
        except Exception as e:
            logger.error('[DispersionFlash] loadView error: %s', e)

        if attempt < 30 and self._isActive and self._sessionId == sessionId:
            BigWorld.callback(0.5, lambda: self._injectFlash(attempt + 1))

    def _onInjectorReady(self, view):
        self._injectorView = view
        logger.debug('[DispersionFlash] Injector ready')

    def _onInjectorDisposed(self):
        self._injectorView = None

    def _onFlashReady(self, view):
        self._componentView = view
        self._flashReady = True
        self._loadPosition()
        self._pushInitialConfig()
        logger.debug('[DispersionFlash] Component ready')

    def _pushInitialConfig(self):
        from ..settings.config_param import g_configParams
        try:
            self.setReductionConfig(
                g_configParams.reductionEnabled.value,
                g_configParams.reductionStyle.value
            )
        except Exception as e:
            logger.error('[DispersionFlash] Error pushing initial config: %s', e)

    def _onFlashDisposed(self):
        self._componentView = None
        self._flashReady = False

    def updateReduction(self, aimingPercent, timeLabel, percentLabel, aimedLabel):
        if self.isCreated():
            self._componentView.as_setReductionData(aimingPercent, timeLabel, percentLabel, aimedLabel)

    def setReductionConfig(self, enabled, style):
        if self.isCreated():
            self._componentView.as_setReductionConfig(enabled, style)

    def setReductionVisible(self, visible):
        if self.isCreated():
            self._componentView.as_setReductionVisible(visible)

    def setInterfaceScale(self, scale):
        if self.isCreated():
            self._componentView.as_setInterfaceScale(scale)

    def _readPrefInt(self, key, default=0):
        try:
            if Settings is None:
                return default
            prefs = Settings.g_instance.userPrefs
            if prefs is None:
                return default
            section = prefs[PREFS_SECTION]
            if section is None:
                return default
            return section.readInt(key, default)
        except Exception:
            return default

    def _writePrefInt(self, key, value):
        try:
            if Settings is None:
                return
            prefs = Settings.g_instance.userPrefs
            if prefs is None:
                return
            section = prefs[PREFS_SECTION]
            if section is None:
                prefs.createSection(PREFS_SECTION)
                section = prefs[PREFS_SECTION]
            section.writeInt(key, int(value))
        except Exception as e:
            logger.error('[DispersionFlash] Error writing pref %s: %s', key, e)

    def _loadPosition(self):
        try:
            offsetX = self._readPrefInt('reductionOffX', 0)
            offsetY = self._readPrefInt('reductionOffY', 0)
            if self.isCreated() and (offsetX != 0 or offsetY != 0):
                self._componentView.as_setReductionOffset(offsetX, offsetY)
        except Exception as e:
            logger.error('[DispersionFlash] Error loading position: %s', e)

    def onDragEnd(self, offsetX, offsetY):
        try:
            self._writePrefInt('reductionOffX', offsetX)
            self._writePrefInt('reductionOffY', offsetY)
        except Exception as e:
            logger.error('[DispersionFlash] Error saving position: %s', e)

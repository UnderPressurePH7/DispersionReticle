# -*- coding: utf-8 -*-
import json
import sys
from ..utils import logger

import ResMgr
from helpers import getClientLanguage


class TranslationManager(object):

    def __init__(self):
        self._defaultTranslationsMap = {}
        self._translationsMap = {}
        self._currentLanguage = None
        self._translationCache = {}
        self._translationsLoaded = False
        self.fallbackLanguage = "en"
        self.translationPathTemplate = "mods/under_pressure.DispersionReticle/{}.json"

    def _safeJsonLoad(self, content, language):
        try:
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            return json.loads(content)
        except (ValueError, TypeError, UnicodeDecodeError) as e:
            logger.error("[TranslationManager] Failed to parse JSON for language %s: %s", language, e)
            return None

    def _loadLanguageFile(self, language):
        try:
            translationPath = self.translationPathTemplate.format(language)
            translationsRes = ResMgr.openSection(translationPath)

            if translationsRes is None:
                logger.debug("[TranslationManager] Translation file not found for: %s", language)
                return None

            content = translationsRes.asBinary
            if not content:
                logger.debug("[TranslationManager] Empty translation file for: %s", language)
                return None

            return self._safeJsonLoad(content, language)

        except Exception as e:
            logger.error("[TranslationManager] Error loading translation file for %s: %s", language, e)
            return None

    def _validateTranslations(self, translations, language):
        if not isinstance(translations, dict):
            logger.error("[TranslationManager] Invalid format for %s: expected dict, got %s",
                        language, type(translations).__name__)
            return False
        return True

    def loadTranslations(self, forceReload=False):
        if self._translationsLoaded and not forceReload:
            return True

        try:
            defaultTranslations = self._loadLanguageFile(self.fallbackLanguage)

            if defaultTranslations is None:
                self._defaultTranslationsMap = self._getHardcodedDefaults()
                self._translationsMap = self._defaultTranslationsMap.copy()
                self._translationsLoaded = True
                return True

            if not self._validateTranslations(defaultTranslations, self.fallbackLanguage):
                return False

            self._defaultTranslationsMap = defaultTranslations

            try:
                clientLanguage = getClientLanguage()
            except Exception:
                clientLanguage = self.fallbackLanguage

            self._currentLanguage = clientLanguage

            if clientLanguage != self.fallbackLanguage:
                clientTranslations = self._loadLanguageFile(clientLanguage)

                if clientTranslations is not None and self._validateTranslations(clientTranslations, clientLanguage):
                    self._translationsMap = clientTranslations
                else:
                    self._translationsMap = defaultTranslations.copy()
            else:
                self._translationsMap = defaultTranslations.copy()

            self._translationCache.clear()
            self._translationsLoaded = True
            return True

        except Exception as e:
            logger.error("[TranslationManager] Critical error during translation loading: %s", e)
            self._defaultTranslationsMap = self._getHardcodedDefaults()
            self._translationsMap = self._defaultTranslationsMap.copy()
            self._translationsLoaded = True
            return True

    def _getHardcodedDefaults(self):
        return {
            "modname": "Dispersion Reticle",
            "checked": "enabled",
            "unchecked": "disabled",
            "defaultValue": "default",
            "reductionStyle.new": "New (progress bar)",
            "reductionStyle.old": "Old (slider)",
            "circleEnabled.header": "Focused dispersion circle",
            "circleEnabled.body": "Show additional reticle that always displays the fully-aimed dispersion size",
            "reticleSizeEnabled.header": "Reticle size correction",
            "reticleSizeEnabled.body": "Enable reticle size correction for accurate dispersion display",
            "reticleSizePercent.header": "Reticle size multiplier",
            "reticleSizePercent.body": "0.0 = accurate (real) size, 1.0 = default WoT size",
            "reductionEnabled.header": "Reduction indicator",
            "reductionEnabled.body": "Show aiming reduction (convergence) indicator",
            "reductionStyle.header": "Indicator style",
            "reductionStyle.body": "Visual style of the reduction indicator",
            "reduction.aimed": "AIMED",
            "reduction.sec": "s"
        }

    def getCurrentLanguage(self):
        return self._currentLanguage or self.fallbackLanguage

    def initialize(self):
        try:
            self.loadTranslations()
        except Exception as e:
            logger.error("[TranslationManager] Critical error initializing translations: %s", e)


g_translationManager = TranslationManager()
g_translationManager.initialize()


class TranslationBase(object):

    def __init__(self, tokenName, manager=None):
        self._tokenName = tokenName
        self._cachedValue = None
        self._manager = manager or g_translationManager

    def __get__(self, instance, owner=None):
        if self._cachedValue is None:
            self._cachedValue = self._generateTranslation()
        return self._cachedValue

    def _generateTranslation(self):
        raise NotImplementedError

    def invalidateCache(self):
        self._cachedValue = None


class TranslationElement(TranslationBase):

    def _generateTranslation(self):
        if not self._manager._translationsLoaded:
            self._manager.loadTranslations()

        cached = self._manager._translationCache.get(self._tokenName)
        if cached is not None:
            return cached

        translation = None
        if self._tokenName in self._manager._translationsMap:
            translation = self._manager._translationsMap[self._tokenName]
        elif self._tokenName in self._manager._defaultTranslationsMap:
            translation = self._manager._defaultTranslationsMap[self._tokenName]
        else:
            translation = self._tokenName.replace('.', ' ').replace('_', ' ').title()

        self._manager._translationCache[self._tokenName] = translation
        return translation


class Translator(object):
    MOD_NAME = TranslationElement("modname")
    CHECKED = TranslationElement("checked")
    UNCHECKED = TranslationElement("unchecked")
    DEFAULT_VALUE = TranslationElement("defaultValue")

    REDUCTION_STYLE_NEW = TranslationElement("reductionStyle.new")
    REDUCTION_STYLE_OLD = TranslationElement("reductionStyle.old")

    CIRCLE_ENABLED_HEADER = TranslationElement("circleEnabled.header")
    CIRCLE_ENABLED_BODY = TranslationElement("circleEnabled.body")

    RETICLE_SIZE_ENABLED_HEADER = TranslationElement("reticleSizeEnabled.header")
    RETICLE_SIZE_ENABLED_BODY = TranslationElement("reticleSizeEnabled.body")
    RETICLE_SIZE_PERCENT_HEADER = TranslationElement("reticleSizePercent.header")
    RETICLE_SIZE_PERCENT_BODY = TranslationElement("reticleSizePercent.body")

    REDUCTION_ENABLED_HEADER = TranslationElement("reductionEnabled.header")
    REDUCTION_ENABLED_BODY = TranslationElement("reductionEnabled.body")
    REDUCTION_STYLE_HEADER = TranslationElement("reductionStyle.header")
    REDUCTION_STYLE_BODY = TranslationElement("reductionStyle.body")

    REDUCTION_AIMED = TranslationElement("reduction.aimed")
    REDUCTION_SEC = TranslationElement("reduction.sec")


def getTranslation(key):
    if not g_translationManager._translationsLoaded:
        g_translationManager.loadTranslations()

    if key in g_translationManager._translationsMap:
        return g_translationManager._translationsMap[key]
    elif key in g_translationManager._defaultTranslationsMap:
        return g_translationManager._defaultTranslationsMap[key]
    return key

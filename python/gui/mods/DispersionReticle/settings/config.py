# -*- coding: utf-8 -*-
import Event
from .config_file import ConfigFile
from .config_param import ConfigParams, g_configParams
from .config_template import Template
from .translations import Translator
from ..utils import logger

try:
    from gui.modsSettingsApi import g_modsSettingsApi
except ImportError:
    logger.error('[Config] Failed to import g_modsSettingsApi')
    g_modsSettingsApi = None

MOD_LINKAGE = 'me.under_pressure.dispersionreticle'


class Config(object):

    def __init__(self):
        self.configParams = g_configParams
        self.configTemplate = Template(self.configParams)
        self.configFile = ConfigFile(self.configParams)
        self._loadedSuccessfully = False
        self._finalized = False
        self.onConfigChanged = Event.Event()

        self._loadConfigFileToParams()

        if g_modsSettingsApi:
            self._registerMod()

    def fini(self):
        self._finalized = True
        self.onConfigChanged.clear()

    def _registerMod(self):
        if not g_modsSettingsApi:
            return

        try:
            self.configTemplate.setModDisplayName(Translator.MOD_NAME)

            # Column 1: Circle + Reticle Size
            self.configTemplate.addParameterToColumn1(
                'circleEnabled',
                header=Translator.CIRCLE_ENABLED_HEADER,
                body=Translator.CIRCLE_ENABLED_BODY
            )
            self.configTemplate.addParameterToColumn1(
                'reticleSizeEnabled',
                header=Translator.RETICLE_SIZE_ENABLED_HEADER,
                body=Translator.RETICLE_SIZE_ENABLED_BODY
            )
            self.configTemplate.addParameterToColumn1(
                'reticleSizePercent',
                header=Translator.RETICLE_SIZE_PERCENT_HEADER,
                body=Translator.RETICLE_SIZE_PERCENT_BODY
            )

            # Column 2: Reduction + Colors
            self.configTemplate.addParameterToColumn2(
                'reductionEnabled',
                header=Translator.REDUCTION_ENABLED_HEADER,
                body=Translator.REDUCTION_ENABLED_BODY
            )
            self.configTemplate.addParameterToColumn2(
                'reductionStyle',
                header=Translator.REDUCTION_STYLE_HEADER,
                body=Translator.REDUCTION_STYLE_BODY
            )

            template = self.configTemplate.generateTemplate()
            logger.debug('[Config] Template = %s', template)

            settings = g_modsSettingsApi.setModTemplate(
                MOD_LINKAGE,
                template,
                self._onSettingsChanged
            )

            if settings:
                self._applySettingsFromMsa(settings, save=False)

        except Exception as e:
            import traceback
            logger.error('[Config] Error registering mod template: %s', e)
            logger.error('[Config] Traceback: %s', traceback.format_exc())

    def _applySettingsFromMsa(self, settings, save=True):
        try:
            configItems = self.configParams.items()
            for paramName, value in settings.items():
                if paramName in configItems:
                    param = configItems[paramName]
                    try:
                        param.msaValue = value
                    except Exception as e:
                        logger.error('[Config] Error applying MSA setting %s = %s: %s',
                                     paramName, value, e)

            if save:
                self.configFile.save_config()

        except Exception as e:
            logger.error('[Config] Error applying MSA settings: %s', e)

    def _onSettingsChanged(self, linkage, newSettings):
        if linkage != MOD_LINKAGE:
            return

        if self._finalized:
            return

        if not self._loadedSuccessfully:
            self._loadConfigFileToParams()
            if not self._loadedSuccessfully:
                return

        try:
            configItems = self.configParams.items()
            for tokenName, value in newSettings.items():
                if tokenName in configItems:
                    param = configItems[tokenName]
                    try:
                        param.msaValue = value
                    except Exception as e:
                        logger.error('[Config] Error setting parameter %s to %s: %s',
                                     tokenName, value, e)

            self.configFile.save_config()
            self._notifyConfigChanged()

        except Exception as e:
            logger.error('[Config] Error updating settings from MSA: %s', e)

    def _notifyConfigChanged(self):
        try:
            self.onConfigChanged()
        except Exception as e:
            logger.error('[Config] Error firing onConfigChanged: %s', e)

    def _loadConfigFileToParams(self):
        self._loadedSuccessfully = False

        try:
            success = self.configFile.load_config()
            if success:
                self._loadedSuccessfully = True

            if not self.configFile.exists():
                self.configFile.save_config()

        except Exception as e:
            logger.error('[Config] Failed to load config: %s', e)
            configItems = self.configParams.items()
            for tokenName, param in configItems.items():
                param.value = param.defaultValue

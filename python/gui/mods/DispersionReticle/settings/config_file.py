# -*- coding: utf-8 -*-
import json
import os
from ..utils import logger, byteify


class ConfigFile(object):

    def __init__(self, configParams):
        self.configPath = os.path.join('mods', 'configs', 'under_pressure', 'dispersionreticle.json')
        self.configParams = configParams
        self._loadedConfigData = None
        self._extras = {}

    def setExtra(self, key, value):
        self._extras[key] = value

    def getExtra(self, key, default=None):
        if self._loadedConfigData and key in self._loadedConfigData:
            return self._loadedConfigData[key]
        return self._extras.get(key, default)

    def _ensureConfigExists(self):
        try:
            configDir = os.path.dirname(self.configPath)
            if not os.path.exists(configDir):
                os.makedirs(configDir)

            if not os.path.exists(self.configPath):
                return self._createDefaultConfig()
            return True
        except Exception as e:
            logger.error('[ConfigFile] Error ensuring config exists: %s', e)
            return False

    def _createDefaultConfig(self):
        try:
            configData = {}
            configItems = self.configParams.items()

            for tokenName, param in configItems.items():
                configData[tokenName] = param.defaultValue

            for k, v in self._extras.items():
                configData[k] = v

            with open(self.configPath, 'w') as f:
                json.dump(configData, f, indent=4, ensure_ascii=False)

            return os.path.exists(self.configPath)

        except Exception as e:
            logger.error('[ConfigFile] Error creating default config: %s', e)
            return False

    def load_config(self):
        try:
            if not self._ensureConfigExists():
                self._applyDefaults()
                return False

            with open(self.configPath, 'r') as f:
                content = f.read().strip()

            if not content:
                if not self._createDefaultConfig():
                    return False
                with open(self.configPath, 'r') as f:
                    content = f.read().strip()

            configData = byteify(json.loads(content))
            self._loadedConfigData = configData

            configItems = self.configParams.items()
            for tokenName, param in configItems.items():
                if tokenName in configData:
                    try:
                        param.value = configData[tokenName]
                    except Exception as e:
                        logger.error('[ConfigFile] Error loading parameter %s: %s', tokenName, e)
                        param.value = param.defaultValue
                else:
                    param.value = param.defaultValue

            return True

        except ValueError as e:
            logger.error('[ConfigFile] Invalid JSON in config file: %s', e)
            self._loadedConfigData = None
            self._applyDefaults()
            return False
        except Exception as e:
            logger.error('[ConfigFile] Error loading config: %s', e)
            self._loadedConfigData = None
            self._applyDefaults()
            return False

    def _applyDefaults(self):
        configItems = self.configParams.items()
        for tokenName, param in configItems.items():
            param.value = param.defaultValue

    def save_config(self):
        try:
            configDir = os.path.dirname(self.configPath)
            if not os.path.exists(configDir):
                os.makedirs(configDir)

            configData = {}
            configItems = self.configParams.items()
            for tokenName, param in configItems.items():
                configData[tokenName] = param.value

            for k, v in self._extras.items():
                configData[k] = v

            with open(self.configPath, 'w') as f:
                json.dump(configData, f, indent=4, ensure_ascii=False)

            self._loadedConfigData = configData
            return True

        except Exception as e:
            logger.error('[ConfigFile] Error saving config: %s', e)
            return False

    def exists(self):
        return os.path.exists(self.configPath)

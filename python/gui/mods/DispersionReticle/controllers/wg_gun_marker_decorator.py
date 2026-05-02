# -*- coding: utf-8 -*-
import Math
from AvatarInputHandler import aih_global_binding, gun_marker_ctrl
from AvatarInputHandler.gun_marker_ctrl import IGunMarkerController, _BINDING_ID, _MARKER_TYPE, _MARKER_FLAG
from aih_constants import GunMarkerState

from . import AihUpdateType
from ..utils.reticle_registry import ReticleRegistry


class WgDispersionGunMarkersDecorator(IGunMarkerController):
    __gunMarkersFlags = aih_global_binding.bindRW(_BINDING_ID.GUN_MARKERS_FLAGS)
    __clientState = aih_global_binding.bindRW(_BINDING_ID.CLIENT_GUN_MARKER_STATE)
    __serverState = aih_global_binding.bindRW(_BINDING_ID.SERVER_GUN_MARKER_STATE)
    __dualAccState = aih_global_binding.bindRW(_BINDING_ID.DUAL_ACC_GUN_MARKER_STATE)

    currentUpdateType = AihUpdateType.CLIENT

    def __init__(self, clientMarker, serverMarker, dualAccMarker, focusedClientController):
        super(WgDispersionGunMarkersDecorator, self).__init__()
        self.__clientController = clientMarker
        self.__serverController = serverMarker
        self.__dualAccController = dualAccMarker
        self.__focusedClientController = focusedClientController
        self._allControllers = (
            self.__clientController,
            self.__serverController,
            self.__dualAccController,
            self.__focusedClientController
        )

    @property
    def _focusedClientController(self):
        return self.__focusedClientController

    def create(self):
        for controller in self._allControllers:
            controller.create()

    def destroy(self):
        for controller in self._allControllers:
            controller.destroy()

    def enable(self):
        self.__clientController.enable()
        self.__clientController.setPosition(self._getStatePosition(self.__clientState, self.__clientController))

        self.__serverController.enable()
        self.__serverController.setPosition(self._getStatePosition(self.__serverState, self.__serverController))

        self.__dualAccController.enable()
        self.__dualAccController.setPosition(self._getStatePosition(self.__dualAccState, self.__dualAccController))

        self.__focusedClientController.enable()
        self.__focusedClientController.setPosition(self.__clientController.getPosition())

    def disable(self):
        for controller in self._allControllers:
            controller.disable()

    def reset(self):
        for controller in self._allControllers:
            controller.reset()

    def onRecreateDevice(self):
        for controller in self._allControllers:
            controller.onRecreateDevice()

    def getPosition(self, markerType=_MARKER_TYPE.CLIENT):
        for controller in self._allControllers:
            if markerType == controller._gunMarkerType:
                return controller.getPosition()
        gun_marker_ctrl._logger.warning('Gun maker control is not found by type: %d', markerType)
        return Math.Vector3()

    def setPosition(self, position, markerType=_MARKER_TYPE.CLIENT):
        for controller in self._allControllers:
            if markerType == controller._gunMarkerType:
                controller.setPosition(position)
                return
        gun_marker_ctrl._logger.warning('Gun maker control is not found by type: %d', markerType)

    def setFlag(self, positive, bit):
        if positive:
            self.__gunMarkersFlags |= bit
            if bit == _MARKER_FLAG.SERVER_MODE_ENABLED:
                self.__serverController.setPosition(self.__clientController.getPosition())
                self.__serverController.setSizes(self.__clientController.getSizes())
        else:
            self.__gunMarkersFlags &= ~bit

    def update(self, markerType, gunMarkerInfo, supportMarkersInfo, relaxTime):
        if markerType == _MARKER_TYPE.CLIENT:
            size = gunMarkerInfo.size
            if self._shouldUpdateController():
                self.__clientController.update(markerType, gunMarkerInfo, supportMarkersInfo, relaxTime)
                size = self.__clientController.getSizes()[0]
            if self.currentUpdateType == AihUpdateType.CLIENT:
                self.__clientState = (GunMarkerState.fromGunMarkerInfo(gunMarkerInfo, size), supportMarkersInfo)
        elif markerType == _MARKER_TYPE.SERVER:
            size = gunMarkerInfo.size
            if self._shouldUpdateController():
                self.__serverController.update(markerType, gunMarkerInfo, supportMarkersInfo, relaxTime)
                size = self.__serverController.getSizes()[0]
            if self.currentUpdateType == AihUpdateType.SERVER:
                self.__serverState = (GunMarkerState.fromGunMarkerInfo(gunMarkerInfo, size), supportMarkersInfo)
        elif markerType == _MARKER_TYPE.DUAL_ACC:
            self.__dualAccState = (GunMarkerState.fromGunMarkerInfo(gunMarkerInfo), supportMarkersInfo)
            if self._isClientModeEnabled():
                self.__dualAccController.update(markerType, gunMarkerInfo, supportMarkersInfo, relaxTime)
        elif markerType == ReticleRegistry.FOCUSED_CLIENT.gunMarkerType:
            if self._shouldUpdateController():
                self.__focusedClientController.update(markerType, gunMarkerInfo, supportMarkersInfo, relaxTime)
        else:
            gun_marker_ctrl._logger.warning('Gun maker control is not found by type: %d', markerType)

    def _shouldUpdateController(self):
        return self._areBothModesEnabled() \
            or (self._isClientModeEnabled() and self.currentUpdateType == AihUpdateType.CLIENT) \
            or (self._isServerModeEnabled() and self.currentUpdateType == AihUpdateType.SERVER)

    def _areBothModesEnabled(self):
        return self._isClientModeEnabled() and self._isServerModeEnabled()

    def _isClientModeEnabled(self):
        return self.__gunMarkersFlags & _MARKER_FLAG.CLIENT_MODE_ENABLED

    def _isServerModeEnabled(self):
        return self.__gunMarkersFlags & _MARKER_FLAG.SERVER_MODE_ENABLED

    def setVisible(self, flag):
        pass

    def getSizes(self):
        return (0.0, 0.0)

    def setSizes(self, newSizes):
        pass

    def _getStatePosition(self, state, controller):
        try:
            return state[0].position
        except Exception:
            return controller.getPosition()

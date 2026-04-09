# -*- coding: utf-8 -*-
from AvatarInputHandler.gun_marker_ctrl import _GunMarkersDecorator

from ..utils.reticle_registry import ReticleRegistry


class WgDispersionGunMarkersDecorator(_GunMarkersDecorator):

    def __init__(self, clientMarker, serverMarker, dualAccMarker, focusedClientController):
        super(WgDispersionGunMarkersDecorator, self).__init__(clientMarker, serverMarker, dualAccMarker)
        self.__focusedClientController = focusedClientController

    @property
    def _focusedClientController(self):
        return self.__focusedClientController

    def create(self):
        super(WgDispersionGunMarkersDecorator, self).create()
        self.__focusedClientController.create()

    def destroy(self):
        super(WgDispersionGunMarkersDecorator, self).destroy()
        self.__focusedClientController.destroy()

    def enable(self):
        super(WgDispersionGunMarkersDecorator, self).enable()
        self.__focusedClientController.enable()
        clientPos = self._GunMarkersDecorator__clientMarker.getPosition()
        self.__focusedClientController.setPosition(clientPos)

    def reset(self):
        super(WgDispersionGunMarkersDecorator, self).reset()
        self.__focusedClientController.reset()

    def onRecreateDevice(self):
        super(WgDispersionGunMarkersDecorator, self).onRecreateDevice()
        self.__focusedClientController.onRecreateDevice()

    def setFlag(self, positive, bit):
        super(WgDispersionGunMarkersDecorator, self).setFlag(positive, bit)

    def update(self, markerType, gunMarkerInfo, supportMarkersInfo, relaxTime):
        if markerType == ReticleRegistry.FOCUSED_CLIENT.gunMarkerType:
            self.__focusedClientController.update(markerType, gunMarkerInfo, supportMarkersInfo, relaxTime)
            return
        super(WgDispersionGunMarkersDecorator, self).update(markerType, gunMarkerInfo, supportMarkersInfo, relaxTime)

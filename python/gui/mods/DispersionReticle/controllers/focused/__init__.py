# -*- coding: utf-8 -*-
import BigWorld
from AvatarInputHandler import AimingSystems


def getSniperViewportPosition():
    gunRotator = BigWorld.player().gunRotator
    gunMatrix = AimingSystems.getPlayerGunMat(gunRotator.turretYaw, gunRotator.gunPitch)
    return gunMatrix.translation


def getFocusedDispersionSize(targetPos):
    playerAvatar = BigWorld.player()
    vehicleDesc = playerAvatar._PlayerAvatar__getDetailedVehicleDescriptor()

    gunPos = getSniperViewportPosition()

    shotDir = targetPos - gunPos
    shotDist = shotDir.length

    gunDispersionAngle = vehicleDesc.gun.shotDispersionAngle
    shotDispMultiplierFactor = playerAvatar._PlayerAvatar__dispersionInfo[0]
    dispersionAngle = gunDispersionAngle * shotDispMultiplierFactor

    return 2.0 * shotDist * dispersionAngle

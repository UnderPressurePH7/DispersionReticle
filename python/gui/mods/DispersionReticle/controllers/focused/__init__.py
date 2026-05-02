# -*- coding: utf-8 -*-
import BigWorld
from AvatarInputHandler import AimingSystems

from ...utils import logger


_dispersionFallbackLogged = False


def getSniperViewportPosition():
    gunRotator = BigWorld.player().gunRotator
    gunMatrix = AimingSystems.getPlayerGunMat(gunRotator.turretYaw, gunRotator.gunPitch)
    return gunMatrix.translation


def _getVehicleDescriptor(playerAvatar):
    vehicleDesc = getattr(playerAvatar, 'vehicleTypeDescriptor', None)
    if vehicleDesc is not None:
        return vehicleDesc

    getter = getattr(playerAvatar, '_PlayerAvatar__getDetailedVehicleDescriptor', None)
    if getter is not None:
        return getter()

    return None


def _getShotDispMultiplierFactor(playerAvatar):
    global _dispersionFallbackLogged

    dispersionInfo = getattr(playerAvatar, '_PlayerAvatar__dispersionInfo', None)
    if dispersionInfo is not None:
        try:
            return float(dispersionInfo[0])
        except Exception:
            pass

    if not _dispersionFallbackLogged:
        logger.debug('[focused] __dispersionInfo unavailable, using fully aimed multiplier=1.0')
        _dispersionFallbackLogged = True
    return 1.0


def _getDualAccuracyFactor():
    dualAccuracy = None

    try:
        from vehicles.mechanics.mechanic_constants import VehicleMechanic
        from vehicles.mechanics.mechanic_helpers import getPlayerVehicleMechanicComponent
        dualAccuracy = getPlayerVehicleMechanicComponent(VehicleMechanic.DUAL_ACCURACY)
    except Exception:
        try:
            from DualAccuracy import getPlayerVehicleDualAccuracy
            dualAccuracy = getPlayerVehicleDualAccuracy()
        except Exception:
            dualAccuracy = None

    if dualAccuracy is None:
        return 1.0

    try:
        return float(dualAccuracy.getCurrentDualAccuracyFactor())
    except Exception:
        return 1.0


def getFocusedDispersionAngle():
    playerAvatar = BigWorld.player()
    vehicleDesc = _getVehicleDescriptor(playerAvatar)
    shotDispMultiplierFactor = _getShotDispMultiplierFactor(playerAvatar)
    return vehicleDesc.gun.shotDispersionAngle * shotDispMultiplierFactor * _getDualAccuracyFactor()


def getFocusedDispersionSize(targetPos):
    playerAvatar = BigWorld.player()
    gunPos = getSniperViewportPosition()

    shotDir = targetPos - gunPos
    shotDist = shotDir.length

    dispersionAngle = getFocusedDispersionAngle()

    return 2.0 * shotDist * dispersionAngle

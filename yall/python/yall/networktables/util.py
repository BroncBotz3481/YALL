import math
from typing import List, Optional
from urllib.parse import urlunparse
from wpimath import geometry, units

from .geometry import AngularVelocity3d, Orientation3d


class LimelightUtils:
    """
    Utility classes to convert WPILib data to LimelightLib expected values.
    """

    @staticmethod
    def sanitizeName(name: Optional[str]) -> str:
        """
        Sanitize the Limelight name.

        Args:
            name (Optional[str]): Limelight name.

        Returns:
            str: The sanitized Limelight name or "limelight".
        """
        if not name:
            return "limelight"
        return name

    @staticmethod
    def getLimelightURLString(tableName: str, request: str) -> Optional[str]:
        """
        Get the URL for the Limelight.

        Args:
            tableName (str): Limelight name.
            request (str): URI to request from Limelight.

        Returns:
            Optional[str]: URL to request for Limelight, or None if URL is invalid.
        """
        sanitizedName = LimelightUtils.sanitizeName(tableName)
        urlString = f"http://{sanitizedName}.local:5807/{request}"
        try:
            url = urlunparse(
                ("http", f"{sanitizedName}.local", f":5807/{request}", "", "", "")
            )
            return url
        except Exception:
            print("bad LL URL")
        return None

    @staticmethod
    def toPose3d(inData: List[float]) -> Optional[geometry.Pose3d]:
        """
        Takes a 6-length array of pose data and converts it to a 3D pose object.
        Array format: [x, y, z, roll, pitch, yaw] where angles are in degrees.

        Args:
            inData (List[float]): Array containing pose data [x, y, z, roll, pitch, yaw].

        Returns:
            Optional[List[float]]: The 3D pose as a list, or None if invalid data.
        """
        if len(inData) < 6:
            # print("Bad LL 3D Pose Data!")
            return None
        return geometry.Pose3d(
            inData[0],
            inData[1],
            inData[2],
            geometry.Rotation3d(
                math.radians(inData[3]),
                math.radians(inData[4]),
                math.radians(inData[5]),
            ),
        )

    @staticmethod
    def toPose2d(inData: List[float]) -> Optional[geometry.Pose2d]:
        """
        Takes a 6-length array of Pose2d data and converts it to a 2D pose object.
        Uses only x, y, and yaw components, ignoring z, roll, and pitch.
        Array format: [x, y, z, roll, pitch, yaw] where angles are in degrees.

        Args:
            inData (List[float]): Array containing pose data [x, y, z, roll, pitch, yaw].

        Returns:
            Optional[List[float]]: The 2D pose as a list, or None if invalid data.
        """
        if len(inData) < 6:
            # print("Bad LL 2D Pose Data!")
            return None
        return geometry.Pose2d(inData[0], inData[1], math.radians(inData[5]))

    @staticmethod
    def toTranslation3d(translation: List[float]) -> geometry.Translation3d:
        """
        Takes a 3-length array of Translation3d data and converts it into a Translation3d.
        Array format: [x, y, z].

        Args:
            translation (List[float]): Array containing translation data [x, y, z] in meters.

        Returns:
            List[float]: The translation as a list of floats.
        """
        return geometry.Translation3d(translation[0], translation[1], translation[2])

    @staticmethod
    def toOrientation(orientation: List[float]) -> Orientation3d:
        """
        Takes a 6-length array of orientation data and converts it to a 3D orientation object.
        Array format: [yaw, yawrate, pitch, pitchrate, roll, rollrate] in degrees.

        Args:
            orientation (List[float]): Orientation data [yaw, yawrate, pitch, pitchrate, roll, rollrate] in degrees.

        Returns:
            List[float]: The orientation as a list.
        """
        obj: Orientation3d = Orientation3d()
        obj.initFromAngularVelocity(
            geometry.Rotation3d(
                math.radians(orientation[4]),
                math.radians(orientation[2]),
                math.radians(orientation[0]),
            ),
            AngularVelocity3d(orientation[1], orientation[3], orientation[5]),
        )

        return obj

    @staticmethod
    def orientation3dToArray(orientation: Orientation3d) -> List[float]:
        """
        Converts an orientation object to an array of [yaw, yawrate, pitch, pitchrate, roll, rollrate] in degrees.

        Args:
            orientation (List[float]): Orientation object to convert.

        Returns:
            List[float]: Array of [yaw, yawrate, pitch, pitchrate, roll, rollrate] in degrees.
        """
        return [
            orientation.orientation.Z(),
            orientation.angularVelocity.yaw,
            orientation.orientation.Y(),
            orientation.angularVelocity.pitch,
            orientation.orientation.X(),
            orientation.angularVelocity.roll,
        ]

    @staticmethod
    def pose3dToArray(pose: geometry.Pose3d) -> List[float]:
        """
        Converts a 3D pose object to an array of [x, y, z, roll, pitch, yaw].

        Args:
            pose (List[float]): Pose object to convert.

        Returns:
            List[float]: Array containing [x, y, z, roll, pitch, yaw].
        """
        return [
            pose.X(),
            pose.Y(),
            pose.Z(),
            pose.rotation().x_degrees,
            pose.rotation().y_degrees,
            pose.rotation().z_degrees,
        ]

    @staticmethod
    def pose2dToArray(pose: geometry.Pose2d) -> List[float]:
        """
        Converts a 2D pose object to an array of [x, y, 0, 0, 0, yaw].

        Args:
            pose (List[float]): Pose object to convert.

        Returns:
            List[float]: Array containing [x, y, 0, 0, 0, yaw].
        """
        return [
            pose.X(),
            pose.Y(),
            units.radiansToDegrees(0),
            units.radiansToDegrees(0),
            units.radiansToDegrees(0),
            pose.rotation().degrees(),
        ]

    @staticmethod
    def translation3dToArray(translation: geometry.Translation3d) -> List[float]:
        """
        Converts a 3D translation object to an array of [x, y, z].

        Args:
            translation (List[float]): Translation object to convert.

        Returns:
            List[float]: Array containing [x, y, z].
        """
        return [translation.X(), translation.Y(), translation.Z()]

    @staticmethod
    def extractArrayEntry(inData: List[float], position: int) -> float:
        """
        Return a double from a double array if it exists, else return 0.

        Args:
            inData (List[float]): Double array to extract from.
            position (int): Position to read.

        Returns:
            float: The value at the position or 0 if data isn't present.
        """
        if len(inData) <= position:
            return 0
        return inData[position]

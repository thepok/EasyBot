import time
from Driver import STSServoDriver
import serial
from enum import IntEnum

# (servo_id)
# (1)Gripper is open at position 2000 and closed at position 1400
# (2)Wrist is possible to rotate from 0 to 2700 to save the cable
# (3)Wrist joint is possible to bend from 1000 to 3200
# (4)Elbow joint is possible to bend from 1000 to 3200
# (5)Shoulder joint is able to bend from 900 to 3000 
# (6)Shoulder (base) rotator is possible to rotate from 600 to 3300


class ServoId(IntEnum):
    GRIPPER = 1
    WRIST_ROTATE = 2  # Rotates the gripper
    WRIST_BEND = 3    # Wrist joint bend
    ELBOW = 4         # Elbow joint
    SHOULDER = 5      # Shoulder joint
    BASE = 6          # Base rotation

class Robot:
    def __init__(self):
        self.driver = None
        for port in range(1, 10):
            try:
                self.driver = STSServoDriver(f"COM{port}")
                break
            except serial.SerialException:
                continue
        if not self.driver:
            raise Exception("No working COM port found")
        
        if not self.driver.ping(ServoId.GRIPPER):
            raise Exception("Gripper servo not responding")
            
        # Initialize position tracking
        self.positions = {
            ServoId.GRIPPER: self.driver.get_current_position(ServoId.GRIPPER),
            ServoId.WRIST_ROTATE: self.driver.get_current_position(ServoId.WRIST_ROTATE),
            ServoId.WRIST_BEND: self.driver.get_current_position(ServoId.WRIST_BEND),
            ServoId.ELBOW: self.driver.get_current_position(ServoId.ELBOW),
            ServoId.SHOULDER: self.driver.get_current_position(ServoId.SHOULDER),
            ServoId.BASE: self.driver.get_current_position(ServoId.BASE)
        }

    def _update_position(self, servo_id: ServoId, position: int):
        """Internal method to update tracked position and move servo"""
        self.positions[servo_id] = position
        self.driver.set_target_position(servo_id, position)

    def grab(self):
        """Close the gripper"""
        self._update_position(ServoId.GRIPPER, 1400)

    def release(self):
        """Open the gripper"""
        self._update_position(ServoId.GRIPPER, 2000)

    def rotate_wrist_to(self, degrees: int):
        """Rotate the wrist (0 to 2700)"""
        self._update_position(ServoId.WRIST_ROTATE, degrees)

    def rotate_elbow_to(self, degrees: int):
        """Rotate the elbow (1000 to 3200)"""
        self._update_position(ServoId.ELBOW, degrees)

    def extend(self, ticks: int):
        # Calculate new positions
        new_shoulder = self.positions[ServoId.SHOULDER] - ticks * 0.5
        new_elbow = self.positions[ServoId.ELBOW] + ticks
        new_wrist = self.positions[ServoId.WRIST_BEND] - ticks * 0.5
        
        # Update all positions
        self._update_position(ServoId.SHOULDER, int(new_shoulder))
        self._update_position(ServoId.ELBOW, int(new_elbow))
        self._update_position(ServoId.WRIST_BEND, int(new_wrist))

    def set_servo_position(self, servo_id: ServoId, position: int):
        self._update_position(servo_id, position)

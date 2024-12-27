import time
from Driver import STSServoDriver
import serial
from enum import IntEnum
from servo import Servo, ServoLimits

class ServoId(IntEnum):
    GRIPPER = 1
    WRIST_ROTATE = 2  # Rotates the gripper
    WRIST_BEND = 3    # Wrist joint bend
    ELBOW = 4         # Elbow joint
    SHOULDER = 5      # Shoulder joint
    BASE = 6          # Base rotation

class Robot:
    # Robot-specific servo configuration
    SERVO_LIMITS = {
        ServoId.GRIPPER: ServoLimits(1400, 2000, 2000),  # Default to open
        ServoId.WRIST_ROTATE: ServoLimits(0, 2700, 1350),
        ServoId.WRIST_BEND: ServoLimits(1000, 3200, 2100),
        ServoId.ELBOW: ServoLimits(1000, 3200, 2100),
        ServoId.SHOULDER: ServoLimits(900, 3000, 1950),
        ServoId.BASE: ServoLimits(600, 3300, 1950)
    }

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
            
        # Initialize servos with their limits
        self.servos = {
            servo_id: Servo(servo_id, self.driver, self.SERVO_LIMITS[servo_id])
            for servo_id in ServoId
        }

        self.reset_all_servos()

    def grab(self):
        """Close the gripper"""
        self.servos[ServoId.GRIPPER].set_position(1400)

    def release(self):
        """Open the gripper"""
        self.servos[ServoId.GRIPPER].set_position(2000)

    def rotate_wrist_to(self, position: int):
        """Rotate the wrist"""
        self.servos[ServoId.WRIST_ROTATE].set_position(position)

    def rotate_elbow_to(self, position: int):
        """Rotate the elbow"""
        self.servos[ServoId.ELBOW].set_position(position)

    def extend(self, ticks: int):
        """Coordinated movement to extend/retract the arm"""
        self.servos[ServoId.SHOULDER].move_relative(int(-ticks * 0.5))
        self.servos[ServoId.ELBOW].move_relative(ticks)
        self.servos[ServoId.WRIST_BEND].move_relative(int(-ticks * 0.5))

    def set_servo_position(self, servo_id: ServoId, position: int):
        """Set position of a specific servo"""
        self.servos[servo_id].set_position(position)

    def move_relative(self, servo_id: ServoId, offset: int):
        """Move a specific servo relative to its current position"""
        self.servos[servo_id].move_relative(offset)

    def reset_all_servos(self):
        """Reset all servos to their default positions"""
        for servo in self.servos.values():
            servo.reset_to_default()

    @property
    def positions(self):
        """Get current positions of all servos"""
        return {servo_id: servo.current_position for servo_id, servo in self.servos.items()}

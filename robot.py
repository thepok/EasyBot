import time
from Driver import STSServoDriver
import serial
from enum import IntEnum
from servo import Servo, ServoLimits
from servos import Servos

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
        ServoId.WRIST_ROTATE: ServoLimits(1500, 4000, 1500),
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
            
        # Initialize servos with their limits and store them as instance variables
        self.gripper = Servo(ServoId.GRIPPER, self.driver, self.SERVO_LIMITS[ServoId.GRIPPER], "Gripper")
        self.wrist_rotate = Servo(ServoId.WRIST_ROTATE, self.driver, self.SERVO_LIMITS[ServoId.WRIST_ROTATE], "Wrist Rotation")
        self.wrist_bend = Servo(ServoId.WRIST_BEND, self.driver, self.SERVO_LIMITS[ServoId.WRIST_BEND], "Wrist Bend")
        self.elbow = Servo(ServoId.ELBOW, self.driver, self.SERVO_LIMITS[ServoId.ELBOW], "Elbow")
        self.shoulder = Servo(ServoId.SHOULDER, self.driver, self.SERVO_LIMITS[ServoId.SHOULDER], "Shoulder")
        self.base = Servo(ServoId.BASE, self.driver, self.SERVO_LIMITS[ServoId.BASE], "Base")
        
        # Keep servos collection for group operations
        self.servos = Servos([
            self.gripper, self.wrist_rotate, self.wrist_bend,
            self.elbow, self.shoulder, self.base
        ])
        self.reset_all_servos()

    def grab(self):
        """Close the gripper"""
        self.gripper.set_position(1400)

    def release(self):
        """Open the gripper"""
        self.gripper.set_position(2000)

    def rotate_wrist_to(self, position: int):
        """Rotate the wrist"""
        self.wrist_rotate.set_position(position)

    def rotate_elbow_to(self, position: int):
        """Rotate the elbow"""
        self.elbow.set_position(position)

    def extend(self, ticks: int):
        """Coordinated movement to extend/retract the arm"""
        self.shoulder.move_relative(int(-ticks * 0.5))
        self.elbow.move_relative(ticks)
        self.wrist_bend.move_relative(int(-ticks * 0.5))

    def set_servo_position(self, servo_id: ServoId, position: int):
        """Set position of a specific servo"""
        self.servos.get_servo_by_id(servo_id).set_position(position)

    def move_relative(self, servo_id: ServoId, offset: int):
        """Move a specific servo relative to its current position"""
        self.servos.get_servo_by_id(servo_id).move_relative(offset)

    def reset_all_servos(self):
        """Reset all servos to their default positions"""
        self.servos.reset_all()

    @property
    def positions(self):
        """Get current positions of all servos"""
        return self.servos.get_positions_dict()

    def print_status(self):
        """Print a formatted table showing the status of all servos"""
        self.servos.print_status()

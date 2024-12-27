from dataclasses import dataclass
from Driver import STSServoDriver
from enum import IntEnum

@dataclass
class ServoLimits:
    min_pos: int
    max_pos: int
    default_pos: int

class Servo:
    def __init__(self, servo_id: int, driver: STSServoDriver, limits: ServoLimits, name: str = None):
        self.id = servo_id
        self.driver = driver
        self.limits = limits
        self.name = name if name is not None else f"Servo {servo_id}"

    @property
    def current_position(self) -> int:
        return self.driver.get_current_position(self.id)

    @property
    def target_position(self) -> int:
        """Get the target position the servo is moving to"""
        return self.driver.get_target_position(self.id)

    def set_position(self, position: int) -> None:
        """Set servo position while respecting limits"""
        clamped_position = max(self.limits.min_pos, min(position, self.limits.max_pos))
        self.driver.set_target_position(self.id, clamped_position)

    def move_relative(self, offset: int) -> None:
        """Move servo relative to current position"""
        self.set_position(self.current_position + offset)

    def reset_to_default(self) -> None:
        """Reset servo to its default position"""
        self.set_position(self.limits.default_pos)

    def is_at_min(self) -> bool:
        """Check if servo is at minimum position"""
        return self.current_position <= self.limits.min_pos

    def is_at_max(self) -> bool:
        """Check if servo is at maximum position"""
        return self.current_position >= self.limits.max_pos

    def get_movement_range(self) -> float:
        """Get percentage of total movement range available"""
        total_range = self.limits.max_pos - self.limits.min_pos
        current_from_min = self.current_position - self.limits.min_pos
        return (current_from_min / total_range) * 100

    @property
    def current_torque(self) -> int:
        """Get the current torque/current of the servo"""
        return self.driver.get_current_torque(self.id) 
from typing import List, Dict
from servo import Servo
from tabulate import tabulate
import os

class Servos:
    def __init__(self, servos: List[Servo]):
        self.servos = servos
        self._last_table_lines = 0  # Track number of lines in last printed table
        
    def __getitem__(self, index: int) -> Servo:
        """Get a servo by its position in the array (0-based indexing)"""
        try:
            return self.servos[index]
        except IndexError:
            raise IndexError(f"Servo index {index} is out of range. Valid indices are 0-{len(self.servos)-1}")
        
    def __len__(self) -> int:
        return len(self.servos)
        
    def __iter__(self):
        return iter(self.servos)
        
    def print_status(self) -> None:
        """Print a formatted table with the status of all servos"""
        # Clear previous output if it exists
        if self._last_table_lines > 0:
            # Move cursor up and clear lines
            print(f"\033[{self._last_table_lines}A\033[J", end="")
            
        headers = ["ID", "Name", "Position", "Min", "Max", "Default", "Range %", "Torque"]
        data = []
        
        for servo in self.servos:
            data.append([
                servo.id,
                servo.name,
                servo.current_position,
                servo.limits.min_pos,
                servo.limits.max_pos,
                servo.limits.default_pos,
                f"{servo.get_movement_range():.1f}%",
                servo.current_torque
            ])
            
        table = tabulate(data, headers=headers, tablefmt="grid")
        print(table)
        
        # Update line count (add 1 for the print statement itself)
        self._last_table_lines = len(table.split('\n'))
        
    def reset_all(self) -> None:
        """Reset all servos to their default positions"""
        for servo in self.servos:
            servo.reset_to_default()
            
    def get_positions_dict(self) -> Dict[int, int]:
        """Get a dictionary of servo IDs to current positions"""
        return {servo.id: servo.current_position for servo in self.servos}

    def get_servo_by_id(self, servo_id: int) -> Servo:
        """Get a servo by its logical ID (not array position).
        This is useful when you need to find a specific servo by its hardware ID.
        
        Args:
            servo_id: The hardware/logical ID of the servo
            
        Raises:
            ValueError: If no servo with the given ID exists
        """
        for servo in self.servos:
            if servo.id == servo_id:
                return servo
        raise ValueError(f"No servo found with ID {servo_id}")
        
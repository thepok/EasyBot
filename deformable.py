"""
[PROTOTYPE/DEBUG VERSION]
This module implements a deformable control system for robot servos that adapts to external forces.
This implementation is intended for idea generation, testing, and debugging purposes.

The DeformableController class provides a mechanism for making servos respond "softly" to external forces
by monitoring their torque levels and automatically adjusting their positions when resistance is detected.
This creates a more natural and safe interaction between the robot and its environment.

Key features:
- Continuous monitoring of servo torque levels
- Automatic position adjustment when resistance is detected
- Threaded implementation for non-blocking operation
- Configurable torque thresholds and adjustment steps

This behavior is particularly useful for:
- Safe human-robot interaction
- Preventing servo damage from excessive force
- Creating more natural movement patterns
- Handling unknown obstacles or resistance

Note: This is an experimental implementation meant for testing concepts and debugging.
It may need refinement for production use.
"""

from robot import Robot, ServoId
import time
from threading import Thread, Event


class DeformableController:
    def __init__(self, robot: Robot):
        self.robot = robot
        self.stop_event = Event()
        self.monitoring_thread = None
        self.TORQUE_THRESHOLD = 13
        self.ADJUSTMENT_STEP = 1  # How many units to adjust position when torque is high

    def start_monitoring(self):
        """Start the deformable behavior monitoring in a separate thread"""
        if self.monitoring_thread is None or not self.monitoring_thread.is_alive():
            self.stop_event.clear()
            self.monitoring_thread = Thread(target=self._monitor_loop)
            self.monitoring_thread.daemon = True
            self.monitoring_thread.start()

    def stop_monitoring(self):
        """Stop the deformable behavior monitoring"""
        self.stop_event.set()
        if self.monitoring_thread:
            self.monitoring_thread.join()

    def _monitor_loop(self):
        """Main monitoring loop that checks torque and adjusts positions"""
        while not self.stop_event.is_set():
            for servo in self.robot.servos.servos:
                try:
                    # Get current torque and positions
                    current_torque = self.robot.driver.get_current_torque(servo.id)
                    if current_torque is None:
                        continue

                    if current_torque > self.TORQUE_THRESHOLD:
                        current_pos = self.robot.driver.get_current_position(servo.id)
                        target_pos = self.robot.driver.get_target_position(servo.id)
                        
                        if current_pos is None or target_pos is None:
                            continue

                        # Calculate direction of adjustment (towards target)
                        direction = 1 if target_pos > current_pos else -1
                        
                        # Move slightly towards the target position
                        new_pos = current_pos + (direction * self.ADJUSTMENT_STEP)
                        
                        # Apply the new position
                        servo.set_position(new_pos)

                except Exception as e:
                    print(f"Error monitoring servo {servo.id}: {e}")

            self.robot.print_status()  # Use robot's built-in status printing
            time.sleep(0.1)  # Small delay to prevent excessive CPU usage


if __name__ == "__main__":
    # Example usage
    robot = Robot()
    controller = DeformableController(robot)
    controller.start_monitoring()
    
    # The monitoring will continue until the program is stopped
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        controller.stop_monitoring() 
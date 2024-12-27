import tkinter as tk
from robot import Robot, ServoId
import time


class RobotGUI:
    def __init__(self):
        self.robot = Robot()
        self.window = tk.Tk()
        self.window.title("Robot Control")
        
        # For tracking button press state
        self.pressed_button = None
        self.repeat_action = None
        self.is_repeating = False

        # Create controls for each joint
        self.create_joint_controls("Gripper", ServoId.GRIPPER)
        self.create_joint_controls("Wrist Rotation", ServoId.WRIST_ROTATE)
        self.create_joint_controls("Wrist Bend", ServoId.WRIST_BEND)
        self.create_joint_controls("Elbow", ServoId.ELBOW)
        self.create_joint_controls("Shoulder", ServoId.SHOULDER)
        self.create_joint_controls("Base", ServoId.BASE)

        # Create extend controls
        self.create_extend_controls()

        # Start updating status
        self.update_status()

    def update_status(self):
        self.robot.print_status()
        self.window.after(100, self.update_status)  # Update every 100ms

    def button_held(self):
        if self.repeat_action and self.is_repeating:
            self.repeat_action()
            # Schedule next repeat
            self.window.after(50, self.button_held)

    def on_button_press(self, button, action):
        self.pressed_button = button
        self.repeat_action = action
        self.is_repeating = True
        action()  # Execute immediately
        # Start repeating after a short delay
        self.window.after(50, self.button_held)

    def on_button_release(self, button):
        if button == self.pressed_button:
            self.pressed_button = None
            self.repeat_action = None
            self.is_repeating = False

    def create_extend_controls(self):
        frame = tk.Frame(self.window)
        frame.pack(pady=5)

        label = tk.Label(frame, text="Extend/Retract", width=15)
        label.pack(side=tk.LEFT)

        fine_retract_btn = tk.Button(frame, text="<<", width=2, height=2)
        fine_retract_btn.bind('<ButtonPress-1>', lambda e: self.on_button_press(fine_retract_btn, lambda: self.robot.extend(10)))
        fine_retract_btn.bind('<ButtonRelease-1>', lambda e: self.on_button_release(fine_retract_btn))
        fine_retract_btn.pack(side=tk.LEFT, padx=2)

        retract_btn = tk.Button(frame, text="-", width=5, height=2)
        retract_btn.bind('<ButtonPress-1>', lambda e: self.on_button_press(retract_btn, lambda: self.robot.extend(50)))
        retract_btn.bind('<ButtonRelease-1>', lambda e: self.on_button_release(retract_btn))
        retract_btn.pack(side=tk.LEFT, padx=2)

        extend_btn = tk.Button(frame, text="+", width=5, height=2)
        extend_btn.bind('<ButtonPress-1>', lambda e: self.on_button_press(extend_btn, lambda: self.robot.extend(-50)))
        extend_btn.bind('<ButtonRelease-1>', lambda e: self.on_button_release(extend_btn))
        extend_btn.pack(side=tk.LEFT, padx=2)

        fine_extend_btn = tk.Button(frame, text=">>", width=2, height=2)
        fine_extend_btn.bind('<ButtonPress-1>', lambda e: self.on_button_press(fine_extend_btn, lambda: self.robot.extend(-10)))
        fine_extend_btn.bind('<ButtonRelease-1>', lambda e: self.on_button_release(fine_extend_btn))
        fine_extend_btn.pack(side=tk.LEFT)

    def create_joint_controls(self, name: str, servo_id: ServoId):
        frame = tk.Frame(self.window)
        frame.pack(pady=5)

        label = tk.Label(frame, text=name, width=15)
        label.pack(side=tk.LEFT)

        fine_dec_btn = tk.Button(frame, text="<<", width=2, height=2)
        fine_dec_btn.bind('<ButtonPress-1>', 
            lambda e: self.on_button_press(fine_dec_btn,
                lambda: self.robot.set_servo_position(servo_id, self.robot.positions[servo_id] - 10)))
        fine_dec_btn.bind('<ButtonRelease-1>', lambda e: self.on_button_release(fine_dec_btn))
        fine_dec_btn.pack(side=tk.LEFT, padx=2)

        dec_btn = tk.Button(frame, text="-", width=5, height=2)
        dec_btn.bind('<ButtonPress-1>', 
            lambda e: self.on_button_press(dec_btn,
                lambda: self.robot.set_servo_position(servo_id, self.robot.positions[servo_id] - 100)))
        dec_btn.bind('<ButtonRelease-1>', lambda e: self.on_button_release(dec_btn))
        dec_btn.pack(side=tk.LEFT, padx=2)

        inc_btn = tk.Button(frame, text="+", width=5, height=2)
        inc_btn.bind('<ButtonPress-1>', 
            lambda e: self.on_button_press(inc_btn,
                lambda: self.robot.set_servo_position(servo_id, self.robot.positions[servo_id] + 100)))
        inc_btn.bind('<ButtonRelease-1>', lambda e: self.on_button_release(inc_btn))
        inc_btn.pack(side=tk.LEFT, padx=2)

        fine_inc_btn = tk.Button(frame, text=">>", width=2, height=2)
        fine_inc_btn.bind('<ButtonPress-1>', 
            lambda e: self.on_button_press(fine_inc_btn,
                lambda: self.robot.set_servo_position(servo_id, self.robot.positions[servo_id] + 10)))
        fine_inc_btn.bind('<ButtonRelease-1>', lambda e: self.on_button_release(fine_inc_btn))
        fine_inc_btn.pack(side=tk.LEFT)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    gui = RobotGUI()
    gui.run()

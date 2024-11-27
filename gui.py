import tkinter as tk
from robot import Robot, ServoId


class RobotGUI:
    def __init__(self):
        self.robot = Robot()
        self.window = tk.Tk()
        self.window.title("Robot Control")

        # Create controls for each joint
        self.create_joint_controls("Gripper", ServoId.GRIPPER)
        self.create_joint_controls("Wrist Rotation", ServoId.WRIST_ROTATE)
        self.create_joint_controls("Wrist Bend", ServoId.WRIST_BEND)
        self.create_joint_controls("Elbow", ServoId.ELBOW)
        self.create_joint_controls("Shoulder", ServoId.SHOULDER)
        self.create_joint_controls("Base", ServoId.BASE)

        # Create extend controls
        self.create_extend_controls()

    def create_extend_controls(self):
        frame = tk.Frame(self.window)
        frame.pack(pady=5)

        label = tk.Label(frame, text="Extend/Retract", width=15)
        label.pack(side=tk.LEFT)

        fine_retract_btn = tk.Button(
            frame,
            text="<<",
            command=lambda: self.robot.extend(10),
            width=2,
            height=2,
        )
        fine_retract_btn.pack(side=tk.LEFT, padx=2)

        retract_btn = tk.Button(
            frame,
            text="-",
            command=lambda: self.robot.extend(50),
            width=5,
            height=2,
        )
        retract_btn.pack(side=tk.LEFT, padx=2)

        extend_btn = tk.Button(
            frame,
            text="+", 
            command=lambda: self.robot.extend(-50),
            width=5,
            height=2,
        )
        extend_btn.pack(side=tk.LEFT, padx=2)

        fine_extend_btn = tk.Button(
            frame,
            text=">>",
            command=lambda: self.robot.extend(-10),
            width=2,
            height=2,
        )
        fine_extend_btn.pack(side=tk.LEFT)

    def create_joint_controls(self, name: str, servo_id: ServoId):
        frame = tk.Frame(self.window)
        frame.pack(pady=5)

        label = tk.Label(frame, text=name, width=15)
        label.pack(side=tk.LEFT)

        fine_dec_btn = tk.Button(
            frame,
            text="<<",
            command=lambda: self.robot.set_servo_position(servo_id, self.robot.positions[servo_id] - 10),
            width=2,
            height=2,
        )
        fine_dec_btn.pack(side=tk.LEFT, padx=2)

        dec_btn = tk.Button(
            frame,
            text="-",
            command=lambda: self.robot.set_servo_position(servo_id, self.robot.positions[servo_id] - 100),
            width=5,
            height=2,
        )
        dec_btn.pack(side=tk.LEFT, padx=2)

        inc_btn = tk.Button(
            frame,
            text="+",
            command=lambda: self.robot.set_servo_position(servo_id, self.robot.positions[servo_id] + 100),
            width=5,
            height=2,
        )
        inc_btn.pack(side=tk.LEFT, padx=2)

        fine_inc_btn = tk.Button(
            frame,
            text=">>",
            command=lambda: self.robot.set_servo_position(servo_id, self.robot.positions[servo_id] + 10),
            width=2,
            height=2,
        )
        fine_inc_btn.pack(side=tk.LEFT)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    gui = RobotGUI()
    gui.run()

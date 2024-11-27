import cv2
import base64
from openai import OpenAI
from tts import AudioGenerator
from robot import Robot
from pydantic import BaseModel


class Movement(BaseModel):
    servoID: int
    change: int

class Response(BaseModel):
    analysis: str
    done: bool
    movement: Movement | None



class Agent:
    def __init__(self, use_bot: bool = True):
        self.audio_generator = AudioGenerator()
        self.client = OpenAI()
        self.window_name = "Camera Feed"
        self.use_bot = use_bot
        if self.use_bot:
            self.robot = Robot()

    def encode_frame(self, frame):
        """Convert cv2 frame to base64 string"""
        _, buffer = cv2.imencode('.jpg', frame)
        return base64.b64encode(buffer).decode('utf-8')

    def get_camera_frame(self):
        """Get a single frame from the camera"""
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            raise RuntimeError("Failed to grab frame from camera")
        
        print(f"Frame size: {frame.shape[1]}x{frame.shape[0]}")
        
        return frame

    def analyze_frame(self, frame):
        """Get GPT-4V analysis of frame"""
        base64_frame = self.encode_frame(frame)
        
        response = self.client.beta.chat.completions.create(
            # model="gpt-4o-mini",
            model="gpt-4o",
            messages=[{
                "role": "user", 
                "content": [{
                    "type": "text",
                    "text": "Describe the contents of the image in detail."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_frame}",
                        "detail": "high"
                    }
                }]
            }],
            max_tokens=300
        )
        
        return response.choices[0].message.content

    def analyze_with_prompt(self, frame, command: str):
        """Send frame to GPT-4V with custom prompt"""
        response = self.client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": [{
                    "type": "text",
                    "text": command
                },
                {
                    "type": "image_url", 
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{self.encode_frame(frame)}",
                        "detail": "high"
                    }
                }]
            }],
            response_format=Response,
            temperature=0.7,
            max_tokens=300,
            timeout=30
        )
        parsed_response = response.choices[0].message.parsed
        print(parsed_response)
        return parsed_response

    def run(self, command: str):

        done = False
        while not done:
            """Get single frame analysis with custom prompt"""
            frame = self.get_camera_frame()
            response = self.analyze_with_prompt(frame, command)
            print("\nGPT-4V Analysis:")
            print(response)
            # self.audio_generator.say(response.analysis)
            if self.use_bot:
                if response.movement:
                    try:
                        self.robot.move_relative(response.movement.servoID, response.movement.change)
                    except Exception as e:
                        print(f"Error moving robot: {e}")
            done = response.done
        return response


if __name__ == '__main__':

    bot_description = """This is a 6-DOF (degrees of freedom) robotic arm with a gripper end effector. It communicates via serial over COM ports and uses position tracking for precise control. Each servo uses a position system where 4000 ticks represents a full 360-degree rotation.
Gripper (ServoID: 1)
Opens and closes the end effector
Positive change = Opens more
Negative change = Closes

2. Wrist Rotator (ServoID: 2)
Rotates the gripper around its axis
Higher number = Rotates clockwise (when looking down at gripper)

Wrist Bend (ServoID: 3)
Controls the up/down bend at the wrist joint
Higher number = Bends upward

Elbow (ServoID: 4)
Controls the elbow joint bend
Higher number = Bends upward (raises forearm)

Shoulder (ServoID: 5)
Controls the shoulder joint bend
Higher number = Bends upward (raises upper arm)

Base (ServoID: 6)
Rotates the entire arm at its base
Higher number = Rotates clockwise (when looking down at base)

The agent operates in a continuous loop until the task is complete:

1. Takes a picture from the camera
2. Sends the image to GPT-4V along with the command and bot description
3. GPT-4V analyzes the image and suggests a small movement (e.g. +-50 ticks)
4. The robot executes that movement
5. Loop repeats from step 1 until GPT-4V sets done=True

This allows GPT-4V to make small, iterative adjustments while getting visual feedback after each movement.

CURRENT COMMAND:
Close the gripper. Use stepamounts of +-50 ticks. Set Done to True when gripper is closed.
"""


    agent = Agent(use_bot=True)
    agent.run(bot_description)

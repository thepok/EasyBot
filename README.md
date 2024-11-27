# Robot Control GUI

A Python-based system for controlling a robotic arm with multiple servo joints, featuring both manual GUI control and AI-assisted vision-based control.

## Features

- Individual control of 6 servo joints:
  - Base rotation
  - Shoulder
  - Elbow
  - Wrist bend
  - Wrist rotation
  - Gripper
- Manual control via GUI with fine/coarse adjustments
- AI-assisted control using GPT-4V vision model
- Real-time camera feedback
- Text-to-speech feedback
- Extend/retract functionality
- Simple tkinter-based interface

## File Structure

- `agent.py` - AI vision control implementation
  - Integrates GPT-4V for visual analysis
  - Processes camera input
  - Controls robot based on AI feedback
  - Provides text-to-speech status updates

- `gui.py` - Manual GUI control implementation
  - Creates control buttons for each servo
  - Handles user input and robot control
  - Provides fine/coarse adjustment options
  
- `robot.py` - Robot control implementation
  - Defines `Robot` class for high-level control
  - Manages servo positions and movement
  - Implements extend/retract functionality
  
- `Driver.py` - Low-level servo communication
  - Implements `STSServoDriver` for direct servo control
  - Handles serial communication protocol
  - Manages servo registers and commands

## Usage

For manual control:

```bash
python gui.py
```

Each joint can be controlled with:
- `<<` / `>>` buttons for fine adjustments (±10 units)
- `-` / `+` buttons for coarse adjustments (±100 units)

The extend/retract feature uses:
- `<<` / `>>` for fine movements (±10 units)
- `-` / `+` for larger movements (±50 units)

## Hardware Notes

The robot uses Feetech STS series servos, communicating via TTL serial at 1Mbps. Each servo has:
- Position feedback
- Temperature monitoring
- Current sensing
- Configurable PID control



Thanks to https://github.com/matthieuvigne/STS_servos for the servo driver code i simply had to translate to python
Thanks to https://github.com/TheRobotStudio/SO-ARM100 for the great 3d printable open source arm design

# Robot Control GUI

A Python-based graphical user interface for controlling a robotic arm with multiple servo joints.

## Features

- Individual control of 6 servo joints:
  - Base rotation (600-3300 position range)
  - Shoulder (900-3000 position range)
  - Elbow (1000-3200 position range)
  - Wrist bend (1000-3200 position range)
  - Wrist rotation (0-2700 position range)
  - Gripper (1400-2000 position range, closed to open)
- Fine and coarse adjustment controls for each joint
- Extend/retract functionality
- Simple tkinter-based interface

## Requirements

- Python 3.x
- tkinter (usually comes with Python)
- pyserial (for servo communication)
- Custom modules:
  - `robot.py` - Robot control logic and servo definitions
  - `Driver.py` - Low-level servo driver implementation

## File Structure

- `gui.py` - Main GUI implementation using tkinter
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

Run the GUI:

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
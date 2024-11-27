import serial
import struct
from enum import IntEnum


class STSRegisters(IntEnum):
    FIRMWARE_MAJOR = 0x00
    FIRMWARE_MINOR = 0x01
    SERVO_MAJOR = 0x03
    SERVO_MINOR = 0x04
    ID = 0x05
    BAUDRATE = 0x06
    RESPONSE_DELAY = 0x07
    RESPONSE_STATUS_LEVEL = 0x08
    MINIMUM_ANGLE = 0x09
    MAXIMUM_ANGLE = 0x0B
    MAXIMUM_TEMPERATURE = 0x0D
    MAXIMUM_VOLTAGE = 0x0E
    MINIMUM_VOLTAGE = 0x0F
    MAXIMUM_TORQUE = 0x10
    UNLOADING_CONDITION = 0x13
    LED_ALARM_CONDITION = 0x14
    POS_PROPORTIONAL_GAIN = 0x15
    POS_DERIVATIVE_GAIN = 0x16
    POS_INTEGRAL_GAIN = 0x17
    MINIMUM_STARTUP_FORCE = 0x18
    CK_INSENSITIVE_AREA = 0x1A
    CCK_INSENSITIVE_AREA = 0x1B
    CURRENT_PROTECTION_TH = 0x1C
    ANGULAR_RESOLUTION = 0x1E
    POSITION_CORRECTION = 0x1F
    OPERATION_MODE = 0x21
    TORQUE_PROTECTION_TH = 0x22
    TORQUE_PROTECTION_TIME = 0x23
    OVERLOAD_TORQUE = 0x24
    SPEED_PROPORTIONAL_GAIN = 0x25
    OVERCURRENT_TIME = 0x26
    SPEED_INTEGRAL_GAIN = 0x27
    TORQUE_SWITCH = 0x28
    TARGET_ACCELERATION = 0x29
    TARGET_POSITION = 0x2A
    RUNNING_TIME = 0x2C
    RUNNING_SPEED = 0x2E
    TORQUE_LIMIT = 0x30
    WRITE_LOCK = 0x37
    CURRENT_POSITION = 0x38
    CURRENT_SPEED = 0x3A
    CURRENT_DRIVE_VOLTAGE = 0x3C
    CURRENT_VOLTAGE = 0x3E
    CURRENT_TEMPERATURE = 0x3F
    ASYNCHRONOUS_WRITE_ST = 0x40
    STATUS = 0x41
    MOVING_STATUS = 0x42
    CURRENT_CURRENT = 0x45


class STSMode(IntEnum):
    POSITION = 0
    VELOCITY = 1
    STEP = 3


class ServoType(IntEnum):
    UNKNOWN = 0
    STS = 1
    SCS = 2


class Instruction:
    PING = 0x01
    READ = 0x02
    WRITE = 0x03
    REGWRITE = 0x04
    ACTION = 0x05
    SYNCWRITE = 0x83
    RESET = 0x06


class STSServoDriver:
    def __init__(self, port, baudrate=1000000, timeout=1):
        self.serial = serial.Serial(port, baudrate, timeout=timeout)
        self.dir_pin = None  # Placeholder if a GPIO pin is used to control direction

    @staticmethod
    def calculate_checksum(packet):
        """Calculate checksum by summing bytes and taking the lower byte."""
        return (~sum(packet)) & 0xFF

    def send_packet(self, servo_id, instruction, parameters):
        """Send a packet to the servo."""
        packet = [0xFF, 0xFF, servo_id, len(parameters) + 2, instruction] + parameters
        packet.append(self.calculate_checksum(packet[2:]))
        self.serial.write(bytearray(packet))

    def receive_packet(self):
        """Receive a packet from the servo."""
        try:
            response = self.serial.read(2)  # Header
            if response != b'\xFF\xFF':
                raise ValueError("Invalid header")

            # Read the rest of the packet
            servo_id = self.serial.read(1)[0]
            length = self.serial.read(1)[0]
            error = self.serial.read(1)[0]
            params = self.serial.read(length - 2)
            checksum = self.serial.read(1)[0]

            # Validate checksum
            if checksum != self.calculate_checksum([servo_id, length, error] + list(params)):
                raise ValueError("Checksum error")

            return servo_id, error, params
        except Exception as e:
            print(f"Error reading packet: {e}")
            return None

    def ping(self, servo_id):
        """Ping a servo to see if it responds."""
        self.send_packet(servo_id, Instruction.PING, [])
        response = self.receive_packet()
        return response is not None

    def read_register(self, servo_id, register, length=1):
        """Read one or more bytes from a servo's register."""
        self.send_packet(servo_id, Instruction.READ, [register, length])
        response = self.receive_packet()
        if response:
            _, error, params = response
            return params if error == 0 else None
        return None

    def write_register(self, servo_id, register, values):
        """Write one or more bytes to a servo's register."""
        self.send_packet(servo_id, Instruction.WRITE, [register] + values)
        response = self.receive_packet()
        return response is not None

    def set_target_position(self, servo_id, position, speed=0x0FFF):
        """Set the target position of the servo."""
        position_bytes = list(struct.pack('<H', position))
        speed_bytes = list(struct.pack('<H', speed))
        self.write_register(servo_id, STSRegisters.TARGET_POSITION, position_bytes + speed_bytes)

    def get_current_position(self, servo_id):
        """Get the current position of the servo."""
        response = self.read_register(servo_id, STSRegisters.CURRENT_POSITION, 2)
        if response:
            return struct.unpack('<H', bytes(response))[0]
        return None
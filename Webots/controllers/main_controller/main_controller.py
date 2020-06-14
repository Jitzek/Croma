"""main_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Keyboard, Supervisor, Display
from RobotController import RobotController
from RobotControls import RobotControls
from socket_client import SocketClient
from VisionDisplay import VisionDisplay

ENABLE_SOCKET = True
ENABLE_VISION_DISPLAY = False
VISION_DISPLAY_NAME = 'vision_display'

# create the Robot instance.
robot = Robot()

# initialize vision display
vision_display = False
if ENABLE_VISION_DISPLAY:
    vision_display = VisionDisplay(robot.getDisplay(VISION_DISPLAY_NAME), robot.getCamera('camera'),  Display.RGB)

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# get the robot movement logic
rbc = RobotControls(robot, timestep)

# get the keyboard for user input
kb = robot.getKeyboard()
kb.enable(timestep)

socket = False
if ENABLE_SOCKET:
    socket = SocketClient('localhost', 4444)

# configure Controller class to handle all logic (robot movement and user input)
RobotController = RobotController(rbc, kb, timestep, vision_display=vision_display, socket=socket)

while robot.step(timestep) != -1:
    RobotController.Update()
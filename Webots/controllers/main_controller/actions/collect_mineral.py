from vision.mineral_recognition import MineralRecognition, DistanceFromMineral, MineralFlags as mf
from enum import Enum, unique, auto
from actions.grab_object import GrabObject

class Stage(Enum):
    GO_TO_MINERAL = auto()
    PICK_UP_MINERAL = auto()
    WEIGH_MINERAL = auto()

class CollectMineral:
    MAXIMUM_DISTANCE_NORMAL = 0.015
    MINIMUM_DISTANCE_NORMAL = 0.005

    MAXIMUM_DISTANCE_SMALL = 0.1
    MINIMUM_DISTANCE_SMALL = 0.01

    def __init__(self, rbc):
        self.rbc = rbc
        self.mr = MineralRecognition(self.rbc.Camera)
        self.dfm = DistanceFromMineral(self.rbc.Camera.getWidth(), self.rbc.Camera.getHeight(), 0.095)
        self.current_stage = Stage.GO_TO_MINERAL
        self.grab_object = GrabObject(self.rbc)

    def reset(self):
        self.current_stage = Stage.GO_TO_MINERAL
        self.grab_object.reset()

    def execute(self):
        data = self.mr.get_location_minerals(self.rbc.Camera.getImage())
        
        largest_match = self.mr.get_largest_location(data)
        if not largest_match:
            return False
        
        if self.current_stage == Stage.GO_TO_MINERAL:
            distance = self.dfm.getDistance(largest_match[2], largest_match[3])
            if self.goToPosition(largest_match[0], largest_match[2], distance, largest_match[4]):
                self.current_stage = Stage.PICK_UP_MINERAL
            return False
        
        if self.current_stage == Stage.PICK_UP_MINERAL:
            if not self.grab_object.execute():
                return False
        
        return True

    def goToPosition(self, x, width, distance, flag):
        X_DEV = int(self.rbc.Camera.getWidth()/10)

        max_x = self.rbc.Camera.getWidth()
        if x + width/2 < (max_x/2) - X_DEV:
            self.rbc.turnOnSpot(-3)
            return False
        if x + width/2 > (max_x/2) + X_DEV:
            self.rbc.turnOnSpot(3)
            return False
        if flag == mf.NORMAL or flag == mf.BIG:
            if distance < self.MINIMUM_DISTANCE_NORMAL:
                self.rbc.goStraight(-3)
                return False
            if distance > self.MAXIMUM_DISTANCE_NORMAL:
                self.rbc.goStraight(3)
                return False
        else:
            if distance < self.MINIMUM_DISTANCE_SMALL:
                self.rbc.goStraight(-3)
                return False
            if distance > self.MAXIMUM_DISTANCE_SMALL:
                self.rbc.goStraight(3)
                return False
        return True
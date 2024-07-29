import objectbase
import time

class Fire(objectbase.ObjectBase):
    def __init__(self, id, pos):
        super(Fire, self).__init__(id, pos)
        self.timecur = time.time()
        self.timesum = 1
        self.fireFlag = False

    def update(self):
        self.checkImageIndex()
    
    def checkImageIndex(self):
        if time.time() - self.timecur <= self.timesum:
            return
        self.preIndexTime = time.time()

        self.fireFlag = True
        self.updateIndex(0)
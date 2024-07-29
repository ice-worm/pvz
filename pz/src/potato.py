import objectbase
import time

class Potato(objectbase.ObjectBase):
    def __init__(self, id, pos):
        super(Potato, self).__init__(id, pos)
        self.preIndexTime = time.time()
        self.blast = self.pathIndex

    def checkImageIndex(self):
        if time.time() - self.preIndexTime <= self.getImageIndexCD():
            return
        self.preIndexTime = time.time()

        idx = self.pathIndex + 1
        if self.pathIndex == 1:
            idx -= 1
        self.blast = idx
        self.updateIndex(idx)
        self.pathIndex = 0

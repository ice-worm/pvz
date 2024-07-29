import zombiebase
import time

class Goast(zombiebase.ZombieBase):
    def __init__(self, id, pos):
        super(Goast, self).__init__(id, pos)
        self.timecur = time.time()
        self.goastBlock = False

    def checkImageIndex(self):
        if self.goastBlock:
            self.updateIndex(1)
        else:
            self.updateIndex(0)
import objectbase
import fire
import time

class Jalapeno(objectbase.ObjectBase):
    def __init__(self, id, pos):
        super(Jalapeno, self).__init__(id, pos)
        self.hasFire = False
    
    def hasSummon(self):
        return self.hasFire

    def preSummon(self):
        self.hasFire = True

    def doSummon(self):
        if self.hasSummon():
            return fire.Fire(10, (225, self.pos[1]+35))
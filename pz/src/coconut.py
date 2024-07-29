import objectbase
import coconutbullet

class CocoNut(objectbase.ObjectBase):
    def __init__(self, id, pos):
        super(CocoNut, self).__init__(id, pos)
        self.hasBullet = False
    
    def hasSummon(self):
        return self.hasBullet

    def preSummon(self):
        self.hasBullet = True

    def doSummon(self):
        if self.hasSummon():
            self.hasBullet = False
            return coconutbullet.CocoNutBullet(14, (self.pos[0]+self.size[0]-10, self.pos[1]+35))
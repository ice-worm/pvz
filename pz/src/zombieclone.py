import zombiebase

class ZombieClone(zombiebase.ZombieBase):
    def __init__(self, id, pos):
        super(ZombieClone, self).__init__(id, pos)
        self.numclone = 0
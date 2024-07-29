import objectbase

class Nut(objectbase.ObjectBase):
    def __init__(self, id, pos):
        super(Nut, self).__init__(id, pos)
        self.hasblocked = 0
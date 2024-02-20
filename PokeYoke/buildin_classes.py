class toni:
    def __init__(self, b):
        self.b = b
        self.sny = sanjay(self)

    def pr(self):
        print(self.b)


class sanjay:
    def __init__(self, inst_toni):
        self.inst_toni = inst_toni

    def z(self):
        print(self.inst_toni.b)


obj = toni('babu')
obj.sny.z()

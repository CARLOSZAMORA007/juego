import time
class RandomNumber():

    def __init__(self):
        self.a=9
        self.c=3
        self.m=time.time()
        self.xi=4
        self.min=0
        self.max=1
    
    def calculate_ri(self):
        self.xi= ((self.a*self.xi)+self.c)%self.m
        return self.xi/(self.m-1)
    
    def calculate_ni(self):
        return self.min+(self.max-self.min)*self.calculate_ri()
# Robot motion

class robot():
    """
    Robot class
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_fwd(self):
        if ((self.x > 0 and self.x < 2) and (self.y > 0 and self.y < 1)):
            self.y = self.y + 0.05
            return self.y
        
    def move_back(self):
        if ((self.x > 0 and self.x < 2) and (self.y > 0 and self.y < 1)):
            self.y = self.y - 0.05
            return self.y
        
    def move_right(self): 
        if ((self.x > 0 and self.x < 2) and (self.y > 0 and self.y < 1)):
            self.x = self.x + 0.05
            return self.x
        
    def move_left(self):
        if ((self.x > 0 and self.x < 2) and (self.y > 0 and self.y < 1)):
            self.x = self.x - 0.05
            return self.x
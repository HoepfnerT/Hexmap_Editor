# return a boolean, flips after %tsh many calls 
class Blink:
    def __init__(self, tsh): self.status, self.count, self.tsh = True, 0, tsh
    def toggle(self): 
        self.count += 1
        if self.count >= self.tsh: 
            self.count = 0
            self.status = not self.status
        return self.status
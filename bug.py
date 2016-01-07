import random, pygame, math

class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, v):
        return math.sqrt((self.x-v.x)**2 + (self.y-v.y)**2)


class Bug():
    def __init__(self, size, bug_col, splat_col, bug_speed):
        self.size = Vector(size[0], size[1]) # game window (width, height)

        self.bug_file = 'images/' + bug_col + '_bug.png'
        self.splat_file = 'images/' + splat_col + '_splat.png'

        self.image = pygame.image.load(self.bug_file)
        self.image = pygame.transform.scale(self.image, (30, 30))

        self._pos = Vector(random.random(), random.random()) # position on unit square
        self.ang = random.random() * 360 # in degrees
        self.speed = bug_speed / float(self.size.x)

        self.status = 'alive'

    @property
    def pos(self):
        # rescale to scale of game window
        return (self.size.x*self._pos.x, self.size.y*self._pos.y)

    def update_status(self, mouse):
        mouse = Vector(mouse[0] / float(self.size.x), mouse[1] / float(self.size.y))
        if self._pos.distance(mouse) < 0.03: # accuracy required to hit a bug
            self.status = 'dead'
            self.image = pygame.image.load(self.splat_file)
            self.image = pygame.transform.scale(self.image, (30, 30))

    def move(self):
        if self.status == 'alive':
            if random.random() < 0.03: # erratic-ness of bug
                self.ang = random.random() * 360
            else:
                self.ang += random.gauss(0.0, 5.0) # general wiggliness, (mean, sd)

            self.ang %= 360

            xnew = self._pos.x + self.speed * math.cos(self.ang * math.pi / float(180))
            ynew = self._pos.y + self.speed * math.sin(self.ang * math.pi / float(180))

            # action if bug hits wall
            if self._pos.x > 0.95:
                self.ang = 2*math.pi - self.ang
                xnew = 0.95
            if self._pos.x < 0.05:
                self.ang = 2*math.pi - self.ang
                xnew = 0.05
            if self._pos.y > 0.95:
                self.ang = 2*math.pi - self.ang
                ynew = 0.95
            if self._pos.y < 0.05:
                self.ang = 2*math.pi - self.ang
                ynew = 0.05

            self._pos.x = xnew
            self._pos.y = ynew

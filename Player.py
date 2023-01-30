# First we import the needed libraries and files with the classes inside
from pygame import mixer
import MapAndBlocks, PowerUps, Constants, pyxel, math, time

"""This is the class where the logic for the behaviour of the player will be implemented"""
class Mario():
    """Init magic method with all the attributes we need"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = Constants.SMALL_MARIO_WIDTH
        self.h = Constants.SMALL_MARIO_HEIGHT
        self.u = Constants.SMALL_MARIO_U
        self.v = Constants.SMALL_MARIO_V
        self.groundFloor = 232 - self.h
        self.lives = Constants.MARIO_LIVES
        self.score = 0

        self.__dx = 1
        self.__dy = 3
        self.__du = 1/8
        self.__gravity = 1

        self.right = True
        self.left = False
        self.jump = False
        self.jumpcounter = 0
        self.showplus10 = 0

    def draw(self):
        """This is a method that implements the how will Mario appear on the screen depending on the orientation"""
        # When we press the right button the orientation is to the right
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.right = True
            self.left = False
        # When we press the left button the orientation is to the left
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.right = False
            self.left = True
        if self.right:
            pyxel.blt(self.x, self.y, 0, self.u, self.v, self.w, self.h, 6)
        elif self.left:
            pyxel.blt(self.x, self.y, 0, self.u, self.v, -self.w, self.h, 6)

    def marioMove(self, map:MapAndBlocks.Map):
        """This a method that implements the core movement of the player it works heavily with the collision functions"""
        # This if statement checks if Mario is at the end of the map and restricts it movement
        if round(map.u) >= 62 and map.v == 96:
            self.dx = 0
            self.dy = 0
            self.du = 0

        # This if statement checks if Mario is on a solid surface and if it is not it applies gravity
        if self.y < self.groundFloor:
            self.y += self.gravity

        # This if statement checks if the user wants to move Mario to the right
        if pyxel.btn(pyxel.KEY_RIGHT):
            # This if statement checks if Mario is at the middle of the screen and if it is it moves the background instead of Mario
            if self.x == 128:
                map.u += self.du
                # The next two if statements check if Mario is at a certain point of the game where we need to move the
                # background art vertically since we have only a certain amount of width inside the art bank
                if round(map.u) == 200 and map.v == 0:
                    map.u = 0
                    map.v = 32
                if round(map.u) == 200 and map.v == 32:
                    map.u = 0
                    map.v = 64
            # If Mario is not at the middle of the screen he moves normally
            else:
                self.x += self.dx

        # This if statement checks if the user wants to move Mario to the left and moves him to left
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.dx

        # This if statement checks if the user wants Mario to jump
        if pyxel.btn(pyxel.KEY_UP):
            # Jump sounds
            jump_sound = mixer.Sound('music/small_jump.ogg')
            jump_sound.set_volume(0.2)
            jump_sound.play()
            # This if statement checks if Mario is on a solid surface i.e. the ground or on a block
            # if it is we are given permission to jump
            if self.y == self.groundFloor:
                self.jump = True
        # This if statement checks if Mario is allowed to jump and moves Mario up for a certain amount of time
        # represented by the jumpcounter - simulating a jump
        if self.jump and self.jumpcounter < 30:
            self.y -= self.dy
            self.jumpcounter += 1
        # This if statement checks if our time for the "jump" is over and if it is we forbid Mario to jump and we
        # reset the counter
        if self.jumpcounter == 30:
            self.jumpcounter = 0
            self.jump = False

    def marioCollisionBlock(self, blocks: list, publocks: list ,shroom:PowerUps.Shroom, marker, level):
        """This method is responsible for Mario's collision with block"""
        # Each time we calls this function we reset these attributes which are responsible for the interaction of Mario
        self.dx = 1
        self.dy = 3
        self.du = 1/8
        self.gravity = 1
        self.groundFloor = 232 - self.h
        # This if statement serves the purpose of allowing a marker to appear when Mario collects points
        if self.showplus10 >= 30:
            marker.x = -20
            marker.y = -20
            self.showplus10 = 0
        self.showplus10 += 1
        # This if statement checks if Mario is below some height i.e. Mario has fallen into a whole
        # if it has we reset the level with one less live
        if self.y > 240:
            level.u = 1
            level.v = 0
            self.u = Constants.SMALL_MARIO_U
            self.v = Constants.SMALL_MARIO_V
            self.w = Constants.SMALL_MARIO_WIDTH
            self.h = Constants.SMALL_MARIO_HEIGHT
            self.lives -= 1
            self.x = 10
            self.y = 232 - self.h

        # This for loop goes through a list with all the blocks we have
        for element in blocks:
            # This if statement checks if there is a block beneath Mario if there is we consider
            # that block as solid surface and we restrict gravity
            if self.y == element.y - self.h and (self.x > element.x - self.w and self.x < element.x + element.w):
                self.groundFloor = element.y - self.h

            # This next three for loops and if statements are responsible for removing the restriction
            # of gravity at certain points in the ground i.e. the wholes on the map
            for i in range(16):
                if math.floor(level.u) >= 130 + i and math.floor(level.u) <= 132 + i and level.v == 0:
                    if self.x <= 128 - 8*i and self.x >= 124 - 8*i:
                        self.groundFloor = 500
            for i in range(16):
                if math.floor(level.u) >= 166 + i and math.floor(level.u) <= 170 + i and level.v == 0:
                    if self.x <= 128 - 8*i and self.x >= 120 - 8*i:
                        if self.y > 102:
                            self.groundFloor = 500
            for i in range(16):
                if math.floor(level.u) >= 158 + i and math.floor(level.u) <= 160 + i and level.v == 32:
                    if self.x <= 128 - 8*i and self.x >= 124 - 8*i:
                        self.groundFloor = 500

            # This if statement checks if the user want Mario to move to the right
            if pyxel.btn(pyxel.KEY_RIGHT):
                # This if statement checks if there are any blocks to the right of Mario
                if (self.x + self.w == element.x and self.y >= element.y - self.h):
                    # This if statement checks if those blocks are above or beneath Mario if they are we do nothing
                    if (self.y - element.h >= element.y or self.y + self.h <= element.y):
                        pass
                    # Else we restrict the movement of Mario or the movement of the background
                    else:
                        self.dx = 0
                        self.du = 0

            # This if statement checks if the user want Mario to move to the left
            if pyxel.btn(pyxel.KEY_LEFT):
                # This if statement checks if there are any blocks to the left of Mario
                if (self.x - element.w == element.x and self.y >= element.y - self.h):
                    # This if statement checks if those blocks are above or beneath Mario if they are we do nothing
                    if (self.y - element.h >= element.y or self.y + self.h <= element.y):
                        pass
                    # Else we restrict the movement of Mario or the movement of the background
                    else:
                        self.dx = 0

            # This if statement checks if there are any blocks above Mario if there are and Mario tries to jump they restrict his jump
            if ((self.x + self.w > element.x and self.x < element.x + element.w) and self.y - 1 == element.y + element.h):
                self.jump = False
                self.jumpcounter = 0
                # This if statement checks if the block above Mario is a question mark block
                if element.u == 16 and element.v == 48:
                    # This changes the question mark block into a used question mark block
                    element.v = 64
                    # This if statement checks if the question mark block is among a list of some chosen blocks
                    # if it is when hit from below it spawns a mushroom power up
                    if element in publocks:
                        shroom.y = element.y - 16
                        shroom.x = element.x
                        shroom.grow = True
                    # Else it spawns a marker above the block that shows that point were collected
                    else:
                        marker.x = element.x
                        marker.y = element.y - 16
                        self.score += 10

                # Sound for hitting a block
                breaking_block_sound = mixer.Sound('music/brick_smash.ogg')
                breaking_block_sound.play()

    def marioCollisionEnemy(self, enemies: list, level: MapAndBlocks.Map):
        """This method is responsible for Mario's collision with enemies"""
        # This for loop goes through a list of all the enemies
        for element in enemies:
            # This if statement checks if Mario collides with an enemy from the left of from the right
            if (self.x == element.x - self.w and (self.y > element.y - self.h and self.y < element.y + self.h)) \
                    or (self.x == element.x + self.w and (self.y > element.y - self.h and self.y < element.y + self.h)):
                # This if statement checks if Mario is in a Big Mario form if it is it transforms him into small Mario form
                if self.h == 32:
                    killing_enemy = mixer.Sound('music/kick.ogg')
                    killing_enemy.play()
                    self.u = Constants.SMALL_MARIO_U
                    self.v = Constants.SMALL_MARIO_V
                    self.w = Constants.SMALL_MARIO_WIDTH
                    self.h = Constants.SMALL_MARIO_HEIGHT
                    self.y = self.y + Constants.SMALL_MARIO_HEIGHT
                # Else if it is small Mario it resets the level with one less live
                else:
                    killing_enemy = mixer.Sound('music/kick.ogg')
                    killing_enemy.play()
                    self.lives -= 1
                    level.u = 1
                    level.v = 0
                    self.x = 10
                    self.y = 232 - self.h
            # This if statement checks if Mario collides with an enemy from above if it does it adds points to the player
            # and gives Mario a little boost up then it removes the enemy
            elif (self.y == element.y - self.h and (self.x >= element.x - self.w and self.x <= element.x + self.w)):
                # KILLING THE ENEMY SOUND
                killing_enemy = mixer.Sound('music/kick.ogg')
                killing_enemy.play()
                self.score += 50
                self.jump = True
                self.jumpcounter = 15
                element.y = 300

    def marioCollisionPU(self, shroom):
        """This method is responsible for Mario's collision with power up objects"""
        # This if statement checks if Mario collides with any power up from any side
        if ((round(self.x) >= shroom.x - self.w and round(self.x) <= shroom.x + self.w) and (self.y >= shroom.y - self.h and self.y <= shroom.y + self.h)):
            # This if statement checks if Mario is in a small Mario form and if it is it transforms him into Big Mario form
            if self.h == 16:
                powerup_sound = mixer.Sound('music/powerup.ogg')
                powerup_sound.play()
                self.u = Constants.BIG_MARIO_U
                self.v = Constants.BIG_MARIO_V
                self.w = Constants.BIG_MARIO_WIDTH
                self.h = Constants.BIG_MARIO_HEIGHT
                self.y = self.y - 17
                shroom.y = 300
            # Else if Mario is in Big Mario form it adds points and removes the Power Up
            else:
                shroom.y = 300
                self.score += 300

    def changeSprite(self):
        """This method is responsible for Mario's running animation"""
        # This if statement checks if Mario is in small Mario form
        if self.h == 16:
            # If Mario moves to the left or to the right we change the sprite each second
            if (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_LEFT)) and self.y == self.groundFloor:
                # This if statement checks if the second is even and if it is we use the following sprite
                if round(time.time()) % 2 == 0:
                        self.u = 48
                        self.v = 112
                # This if statement checks if the second is odd and if it is we use the following sprite
                elif round(time.time()) % 2 != 0:
                    self.u = 48
                    self.v = 96
            # Otherwise we use the basic Mario sprite
            else:
                self.u = Constants.SMALL_MARIO_U
                self.v = Constants.SMALL_MARIO_V
            # This if statement checks if Mario is in the air and if it is we use the following sprite
            if self.y != self.groundFloor:
                self.u = 48
                self.v = 112
        # This if statement checks if Mario is in small Mario form
        if self.h == 32:
            # If Mario moves to the left or to the right we change the sprite each second
            if (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_LEFT)) and self.y == self.groundFloor:
                # This if statement checks if the second is even and if it is we use the following sprite
                if round(time.time()) % 2 == 0:
                    self.u = 0
                    self.v = 16
                # This if statement checks if the second is odd and if it is we use the following sprite
                elif round(time.time()) % 2 != 0:
                    self.u = 0
                    self.v = 48
            # Otherwise we use the basic Mario sprite
            else:
                self.u = Constants.BIG_MARIO_U
                self.v = Constants.BIG_MARIO_V
            # This if statement checks if Mario is in the air and if it is we use the following sprite
            if self.y != self.groundFloor:
                self.u = 0
                self.v = 16
############################ SETTERS FOR THE MARIO CLASS
    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        if type(x) != int and type(x) != float:
            raise TypeError
        if (x >= 0 and x <= 256):
            self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        if type(y) != int and type(y) != float:
            raise TypeError
        if y >= 0 and y <= 256:
            self.__y = y

    @property
    def w(self):
        return self.__w

    @w.setter
    def w(self, w):
        if type(w) != int:
            raise TypeError
        else:
            self.__w = w

    @property
    def h(self):
        return self.__h

    @h.setter
    def h(self, h):
        if type(h) != int:
            raise TypeError
        else:
            self.__h = h

    @property
    def u(self):
        return self.__u

    @u.setter
    def u(self, u):
        if type(u) != int:
            raise TypeError
        else:
            self.__u = u

    @property
    def v(self):
        return self.__v

    @v.setter
    def v(self, v):
        if type(v) != int:
            raise TypeError
        else:
            self.__v = v

    @property
    def groundFloor(self):
        return self.__groundFloor

    @groundFloor.setter
    def groundFloor(self, groundFloor):
        if type(groundFloor) != int:
            raise TypeError
        else:
            self.__groundFloor = groundFloor


    @property
    def lives(self):
        return self.__lives

    @lives.setter
    def lives(self, lives):
        if type(lives) != int:
            raise TypeError
        if lives >= 0 and lives <= 3:
            self.__lives = lives

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, score):
        if type(score) != int:
            raise TypeError
        else:
            self.__score = score

    @property
    def right(self):
        return self.__right

    @right.setter
    def right(self, right):
        if type(right) != bool:
            raise TypeError
        else:
            self.__right = right

    @property
    def left(self):
        return self.__left

    @left.setter
    def left(self, left):
        if type(left) != bool:
            raise TypeError
        else:
            self.__left = left

    @property
    def jump(self):
        return self.__jump

    @jump.setter
    def jump(self, jump):
        if type(jump) != bool:
            raise TypeError
        else:
            self.__jump = jump

    @property
    def jumpcounter(self):
        return self.__jumpcounter

    @jumpcounter.setter
    def jumpcounter(self, jumpcounter):
        if type(jumpcounter) != int:
            raise TypeError
        if jumpcounter >= 0 and jumpcounter <= 30 :
            self.__jumpcounter = jumpcounter

    @property
    def showplus10(self):
        return self.__showplus10

    @showplus10.setter
    def showplus10(self, showplus10):
        if type(showplus10) != int:
            raise TypeError
        if showplus10 >= 0 and showplus10 <= 30:
            self.__showplus10 = showplus10
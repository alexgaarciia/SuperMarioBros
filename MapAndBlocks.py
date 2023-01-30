# First off, we import the library that will be necessary for developing this part.
import pyxel


# The first thing is done in this part is the creation the class for the map or the level.
class Map:
    """This class stores all the data we need for describing the common characteristics of the map or level"""

    def __init__(self):
        """This is a method that contains all the fields necessary for the creation of the map"""
        self.tm = 0
        self.u = 0
        self.v = 0
        self.w = 32
        self.h = 32

    def draw(self):
        """This is a method that draws the map"""
        pyxel.bltm(0, 0, self.tm, self.u, self.v, self.w, self.h)

    # In this part we create the setters for the Map class. We defined all of them with properties and setters
    # because we want them to be read and written.
    @property
    def tm(self):
        return self.__tm

    @tm.setter
    def tm(self, tm):
        if type(tm) != int:
            raise TypeError
        else:
            self.__tm = tm

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
        if type(u) != int and type(u) != float:
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


# Moving on, the class for the markers of the text that show up while playing is created.
class Marker:
    """This class stores all the data we need for describing the common characteristics of the markers"""
    def __init__(self, x, y, text: str):
        """This is a method that contains the most important fields of the markers"""
        self.x = x
        self.y = y
        self.text = text

    def draw(self):
        """This is a method that draws the markers"""
        pyxel.text(self.x, self.y, self.text, pyxel.COLOR_WHITE)


# This part is of special importance, as the mother class for the blocks is described
class Block:
    """This class stores all the data we need for describing the common characteristics of all the types of blocks
     that will be used during the entire game"""
    def __init__(self, x, y, u, v):
        """This is a magic method used to describe the most important fields or attributes of the blocks. Among them, we
        can find some along the lines of: positions(x, y), positions in the image bank(u,v)..."""
        self.x = x
        self.y = y
        self.u = u
        self.v = v
        self.w = 16
        self.h = 16

    def draw(self):
        """This is a method that draws the blocks"""
        pyxel.blt(self.x, self.y, 0, self.u, self.v, 16, 16)

    # In this part we create the setters for the Block class. We defined all of them with properties and setters
    # because we want them to be read and written.
    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        if type(x) != int and type(x) != float:
            raise TypeError
        else:
            self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        if type(y) != int and type(y) != float:
            raise TypeError
        else:
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


# Finally, we create the classes of the blocks. Note that, for each of them, we will use inheritance, as they all are
# different types of blocks with the same behaviour. We put Block in the class header of each of the classes to use
# inheritance. This indicates that Block is the mother class and groundBlock, brickBlock, sblock, Qblock and Pipe are
# the child classes.
class groundBlock(Block):
    """This class stores all the data we need for creating this specific type of block, which is groundBlock"""
    def __init__(self, x, y, u=16, v=32):
        """This is a method that is a magic function used to declare the main attributes of groundBlock. We included as
        parameters the coordinates(x,y) and the positions in the image bank of pyxel(u, v)"""

        # We will need to rewrite the init method of the mother class if we wanted to add new attributes. Moreover, we
        # use superclass __init__ to avoid rewriting it from scratch. This means: go to the mother class, find the init
        # method and pass to it the value of the parameters.
        super().__init__(x, y, u, v)


# The same from above is done for every type of blocks present in the game.
class brickBlock(Block):
    def __init__(self, x, y, u=16, v=16):
        super().__init__(x, y, u, v)


class sblock(Block):
    def __init__(self, x, y, u=32, v=64):
        super().__init__(x, y, u, v)


class Pipe(Block):
    def __init__(self, x, y, u=0, v=160):
        super().__init__(x, y, u, v)
        self.w = 32
        self.h = 32

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.u, self.v, 32, self.h, 6)


class Qblock(Block):
    def __init__(self, x, y, u=16, v=48):
        super().__init__(x, y, u, v)


# This is a function that goes through a list of objects and moves them when the map moves.
def Interaction(somel: list, player):
    for element in somel:
        if pyxel.btn(pyxel.KEY_RIGHT):
            if player.x == 128 and player.dx != 0:
                element.x -= 1
        if element.x < -element.w:
            element.y = -40
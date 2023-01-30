# First off, we import the library that will be necessary for developing this part.
import pyxel


# The very first thing we do is creating the PowerUp class. This class will be very important, as it will be the mother
# class of the special objects. In other words, all the special objects will be based on the behavior of this class.
class PowerUp:
    """This class stores all the data we need for describing the common characteristics of the special objects"""

    def __init__(self, x, y, w, h=0):
        """This is a magic method that declares the principal attributes of the special objects. Among them, we can find
        some like the positions(x, y), the width(w) or the height(h)"""
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.dx = 1
        self.groundFloor = 216
        self.grow = False

    # In this part we create the setters for the PowerUp class. We defined all of them with properties and setters
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
    def dx(self):
        return self.__dx

    @dx.setter
    def dx(self, dx):
        if type(dx) != int:
            raise TypeError
        else:
            self.__dx = dx

    @property
    def grow(self):
        return self.__grow

    @grow.setter
    def grow(self, grow):
        if type(grow) != bool:
            raise TypeError
        else:
            self.__grow = grow


# Finally, we create the class of the special object that we decided to include. Note that, for this, we will use
# inheritance, as it has the same behavior as PowerUp. We put PowerUp in the class header of Shroom to use inheritance.
# This indicates that PowerUp is the mother class and Shroom is the child class.
class Shroom(PowerUp):
    """This class stores all the data we need for creating this specific type of special object, which is a Mushroom"""
    def __init__(self, x, y, w=16, h=0):
        """This is a method that is a magic function used to declare the main attributes of Shroom. We included as
        parameters the positions(x,y), the width(w) and height(h)"""

        # We will need to rewrite the init method of the mother class if we wanted to add new attributes. Moreover, we
        # use superclass __init__ to avoid rewriting it from scratch. This means: go to the mother class, find the init
        # method and pass to it the value of the parameters.
        super(Shroom, self).__init__(x, y, w, h)

    def draw(self):
        """This is a method that draws Goomba"""
        pyxel.blt(self.x, self.y, 0, 48, 48, self.w, self.h, 6)

    def movePU(self, blocks):
        """This is a method that answers for the movement of the mushroom when it is spawned"""
        self.groundFloor = 216

        # This 'if' statement is used to explain that if the mushroom is spawned, it sets its height to 0 and allows
        # it to grow.
        if self.x < -16:
            self.grow = False
            self.h = 0

        # This 'if' statement allows the special object to grow until full size.
        if self.grow:
            if self.h >= 0 and self.h < 16:
                self.h += 1

        # In here, once the mushroom is totally spawned, it begins to move.
        if self.h == 16:
            # A 'for' loop is applied for all the types of blocks.
            for element in blocks:
                # If it is on the block, the groundFloor changes to the height of the block so that it sits on it.
                if self.y == element.y - self.h and (self.x > element.x - self.w and self.x < element.x + element.w):
                    self.groundFloor = element.y - self.h

                # The two 'if' statements from below explains that special object must change its direction if it
                # if it collides with a block.
                if (self.x + self.w == element.x):
                    if ((self.y - self.h >= element.y or self.y + self.h <= element.y) and not (
                            element.u == 0 and element.v == 160)):
                        pass
                    else:
                        self.dx = -1
                if (self.x - element.w == element.x):
                    if ((self.y - self.h >= element.y or self.y + self.h <= element.y) and not (
                            element.u == 0 and element.v == 160)):
                        pass
                    else:
                        self.dx = 1

            # Contrary to Mario, the special objects must move by themselves, that is what is done below.
            self.x += self.dx

            # This statement applies gravity if it is not on a solid ground.
            if self.y < self.groundFloor:
                self.y += 1
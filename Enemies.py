# First off, we import the library that will be necessary for developing this part.
import pyxel


# The very first thing we do is creating the Enemy class. This class will be very important, as it will be the mother
# class of the different enemies. In other words, all the type of enemies will be based on the behavior of this class.
class Enemy:
    """This class stores all the data we need for describing the common characteristics of the enemies"""
    def __init__(self, x, y, w, h):
        """This is a magic method used to declare the principal attributes of the enemies. It includes some like the
        positions(x,y), the wight(w), the height(h), and the speed(dx)"""
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.dx = -1
        self.left = True
        self.right = False

    def moveEnemy(self, blocks):
        """This is a method that describes the movement of the enemies and their collisions with the blocks"""

        # We use a 'for loop' that will be used for describing the whole movement of the enemies. The elements refer to
        # all the types of blocks that were defined in the game. In our case, several types of blocks are taken into
        # account. We did this because we wanted all the code from below to be applied to every type of blocks.

        for element in blocks:
            # This 'if' statement is used to explain what should happen if the enemy is going to the right and hits an
            # element. If the position of the enemy is the same as the position of the block.
            if self.x + self.w == element.x:
                # This 'if' statement tells the program what to do if the block is above or under the enemy. If this
                # situation occurs, nothing happens.
                if (self.y - self.h >= element.y or self.y + self.h <= element.y)\
                        and not (element.u == 0 and element.v == 160):
                    pass

                # If what was exposed above doesn't happen, which means that there is an object in front of the enemy,
                # then it must change its direction. This is why we set self.dx to -1, so that it goes to the left.
                else:
                    self.dx = -1
                    self.left = True
                    self.right = False

            # This 'if' statement is used to explain what should happen if the enemy is going to the left and hits an
            # element. It happens exactly the same as if the enemy goes to the right but now we need the enemy to move
            # to the right, that is why we set self.dx = 1.
            if self.x - element.w == element.x:
                if ((self.y - self.h >= element.y or self.y + self.h <= element.y) and not (
                        element.u == 0 and element.v == 160)):
                    pass
                else:
                    self.dx = 1
                    self.left = False
                    self.right = True

        # Contrary to Mario, the enemies must move by themselves, that is what is done below.
        self.x += self.dx

    # In this part we create the setters for the Enemy class. We defined all of them with properties and setters
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
    def dx(self):
        return self.__dx

    @dx.setter
    def dx(self, dx):
        if type(dx) != int:
            raise TypeError
        else:
            self.__dx = dx

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


# Finally, we create the classes of the enemies. Note that, for each of them, we will use inheritance, as they all are
# different types of enemies with the same behaviour. We put Enemy in the class header of each of the classes to use
# inheritance. This indicates that Enemy is the mother class and Goomba/Koopa are the child classes.
class Goomba(Enemy):
    """This class stores all the data we need for creating this specific type of enemy, which is Goomba"""
    def __init__(self, x, y, w=16, h=16):
        """This is a method that is a magic function used to declare the main attributes of Goomba and also checks
        if the values provided make sense. We included as parameters the positions(x,y), the width(w) and height(h)"""

        # We will need to rewrite the init method of the mother class if we wanted to add new attributes. Moreover, we
        # use superclass __init__ to avoid rewriting it from scratch. This means: go to the mother class, find the init
        # method and pass to it the value of the parameters.
        super(Goomba, self).__init__(x, y, w, h)

    def draw(self):
        """This is a method that draws Goomba"""
        if self.right:
            pyxel.blt(self.x, self.y, 0, 48, 0, self.w, self.h, 6)
        else:
            pyxel.blt(self.x, self.y, 0, 48, 0, self.w, self.h, 6)


class Koopa(Enemy):
    """This class stores all the data we need for creating this specific type of enemy, which is Koopa"""
    def __init__(self, x, y, w=16, h=25):
        """This is a method that is a magic function used to declare the main attributes of Goomba and also checks
        if the values provided make sense. We included as parameters the positions(x,y), the width(w) and height(h)"""

        # The same happens in this class. We will need to rewrite the init method of the mother class, but we use the
        # superclass __init__ to avoid rewriting it from scratch.
        super(Koopa, self).__init__(x, y, w, h)

    def draw(self):
        """This is a method that draws Goomba"""
        if self.right:
            pyxel.blt(self.x, self.y, 0, 32, 32, -self.w, self.h, 6)
        else:
            pyxel.blt(self.x, self.y, 0, 32, 32, self.w, self.h, 6)
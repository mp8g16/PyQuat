"""The pyquat module defines a new python class intended as a number type which supports the
   binary operators "+,-,*,/,**" as well as the functions "str(),abs(),repr()" and
   includes additional methods "conj(),unit(),inv(),exp(),ln()"."""

import math

class Quat:
    """A new number class for Quaternions (q), q=a+bi+cj+dk. A Quaternion object may be
       generated with Quat(x) where x is either an int, float, list of length 4,
       Tuple of length 4, or another Quat object"""
    def __init__(self, value):
        type_error = "Quat expects either a Quat,list,or non complex number"
        value_error = "Quat expects input list or tuple to be of length 4"

        switcher = {Quat: lambda x: x.vector,
                    list: lambda x: x if len(x) == 4 else ValueError(value_error),
                    tuple: lambda x: x if len(x) == 4 else ValueError(value_error),
                    int: lambda x: [float(x), 0, 0, 0],
                    float: lambda x: [float(x), 0, 0, 0]
                    }

        func = switcher.get(type(value), lambda x: TypeError(type_error))

        if isinstance(func(value), Exception):
            raise func(value)

        self.vector = func(value)

    def __add__(self, other):
        """supports the "+" operator between a Quat with an int, float, list of length 4,
           tuple of length 4 or another Quat object"""
        other_vect = Quat(other).vector
        new_vect = [self.vector[i]+other_vect[i] for i in range(4)]
        return Quat(new_vect)

    def __sub__(self, other):
        """supports the "-" operator between a Quat with an int, float, list of length 4,
           tuple of length 4 or another Quat"""
        return self + (-other)

    def __mul__(self, other):
        """supports the "*" operator between a Quat with an int, float, list of length 4,
           tuple of length 4 or another Quat object"""
        a1, b1, c1, d1 = self.vector
        a2, b2, c2, d2 = Quat(other).vector
        new_vect = [0, 0, 0, 0]
        new_vect[0] = a1*a2 - b1*b2 - c1*c2 - d1*d2
        new_vect[1] = a1*b2 + b1*a2 + c1*d2 - d1*c2
        new_vect[2] = a1*c2 - b1*d2 + c1*a2 + d1*b2
        new_vect[3] = a1*d2 + b1*c2 - c1*b2 + d1*a2
        return Quat(new_vect)

    def __truediv__(self, other):
        """supports the "/" operator between a Quat with an int, float, list of length 4,
           tuple of length 4 or another Quat object"""
        return Quat(self)*Quat(other).inv()

#    def __pow__(self,other):
#         """supports the "**" operator between a Quat with an int, float, list of length 4,
#           tuple of length 4 or another Quat object"""

    def __radd__(self, other):
        return self+other

    def __rsub__(self, other):
        return Quat(other) - self

    def __pos__(self):
        return self

    def __neg__(self):
        return self*(-1)

    def __rmul__(self, other):
        return self*other

    def __rdiv__(self, other):
        return Quat(other)/self

    def __str__(self):
        """supports the str() function on a Quat"""
        bases = ["+", "i+", "j+", "k"]
        array = ["("+str("{:.2f}".format(float(self.vector[x])))+")"+bases[x] for x in range(4)]
        return "".join(array)

    def __repr__(self):
        return str(self)

    def __abs__(self):
        """supports the abs() function on a Quat"""
        return sum([x**2 for x in self.vector])**(1/2)

    def conj(self):
        """q.conj() returns the Quaternion conjugate of q"""
        return 2*self.vector[0]-self

    def unit(self):
        """q.unit() returns the unit Quaternion of q"""
        return (1/abs(self))*self

    def vect(self):
        """q.vect() returns a quaternion "v" with zero real componenet and complex
           components equal to q's complex parts. v = bi +cj +dk"""
        vector = self.vector
        return Quat([0, vector[1], vector[2], vector[3]])

    def scal(self):
        """q.scal() returns a quaternion "a" with all zero complex components and real
           component equal to q's real component."""
        return Quat([self.vector[0], 0, 0, 0])

    def inv(self):
        """q.inv() returns the Quaternion inverse of q"""
        return (abs(self)**-2)*(self.conj())

    def exp(self):
        """q.exp() returns e**q where e is the base of the natural logarithm
        not working"""
        vect = self.vect()
        if abs(vect) != 0:
            value = (math.exp(self.vector[0])*
                     (math.cos(abs(vect))+
                      vect.unit()*math.sin(abs(vect))))
        else:
            value = Quat(math.exp(self.vector[0]))
        return value

    def ln(self):
        """q.ln() returns ln(q) where ln() is the natural logarithm
        not working"""
        vect = self.vect()
        if abs(vect) != 0:
            value = math.log(abs(self)) + (vect.unit()*(math.acos(self.vector[0]/abs(self))))
        else:
            value = math.log(abs(self))
        return value
#
#    def angles():
#         """q.angles() returns the euler angles of a q"""
#
#    def rot_vec():
#
#
#    def rot_ang(self, roll, pitch, yaw):
#         """q.rotate(roll, pitch, yaw) rotates q by the given euler angles"""
#        return 0

#!/usr/bin/env python
"""
4/21/2017

In this script I experiment with groups. You derive off of 'group' to make 
a particular group. It knows how to give you 'elem's that you can use the 
operator on to combine them. 

"""

import abc
import collections as col
import math

#******************************************************************************
#  Probably want to put this in another module at some point
#******************************************************************************

class elem:
    """ elements in a group that can be operated on with * """
    __metaclass__ = abc.ABCMeta
    _ename = None
    _group = None

    def __init__(self, element_name, group):
        self._ename = element_name
        self._group = group 

    def ename(self):
        return self._ename

    def idx(self):
        return self._group._idxs[self._ename]

    def __mul__(self, elem):
        return self._group.op(self, elem)

    def __str__(self):
        return self._ename

class group:
    """Abstract base class for all groups"""

    __metaclass__ = abc.ABCMeta
    _elem_type = None
    _idxs = None 
    _identity = None 

    def the_set(self, gset):
        self._idxs = col.OrderedDict()
        self._max_name_len = 0
        for n, e in enumerate(gset):
            self._idxs[e] = n
            if len(e) > self._max_name_len:
                self._max_name_len = len(e)


    def the_identity(self, I):
        self._identity = I

    def idxs(self):
        return self._idxs

    def elem(self, element_name):
        """ returns one element by name """
        if element_name not in self.idxs().keys():
            raise 
        return elem(element_name, self)        

    def elems(self):
        """ returns list of all elements """
        els = []
        for key in self.idxs().keys():
            els.append(elem(key, self))
        return els
        

    @abc.abstractmethod
    def op(self, elem):
        return

    @abc.abstractmethod
    def inv_elem(self, element_rep):
        return 

    def is_closed(self):
        for elname1 in self.idxs().keys():
            for elname2 in self.idxs().keys():
                e1 = self.elem(elname1)
                e2 = self.elem(elname2)
                ee = self.op(e1, e2)
                if ee.ename() not in self.idxs().keys():
                    return False
        return True
        
    def __str__(self):
        mname = self._max_name_len
        s = "*" +" "*mname + "| " 
        dash = "-" + "-"*mname + "--" 
        for key in self.idxs().keys():
            l = len(key)
            s += " "*(mname - l)
            dash += "-"*(mname - l)
            s += key + " "
            dash += "-"*len(key) + "-" 
        s += "\n" + dash + "\n"

        for elname1 in self.idxs().keys():
            l = len(elname1)
            s += elname1 + " "*(mname - l + 1) + "| "
            for elname2 in self.idxs().keys():
                e1 = self.elem(elname1)
                e2 = self.elem(elname2)
                ee = self.op(e1, e2)
                le = len(ee.ename())
                s += " "*(mname - le)
                s += str(ee) + " "
            s += "\n"

        return s

#******************************************************************************
#                       Experimental Groups
#******************************************************************************

class group1(group):
    """ simple abelian """

    gset = ["I", "a", "b", "c"]
    identity = "I"

    _gmap = (("I", "a", "b", "c"),
             ("a", "b", "c", "I"),
             ("b", "c", "I", "a"),
             ("c", "I", "a", "b"))

    def __init__(self):
        # must set the set of elements and identity here
        self.the_set(self.gset)
        self.the_identity(self.identity)

        self._indxmap = {} 
        for m,p1 in enumerate(self._gmap):
            for n,p2 in enumerate(p1):
                self._indxmap[m,n] = p2
        print self._indxmap

    def op(self, elem1, elem2):
        name = self._indxmap[elem1.idx(),elem2.idx()]
        return elem(name, self)

    def inv_elem(self, element_name):
        if element_name not in self.idxs().keys():
            raise 
        for elname1 in self.idxs().keys():
            for elname2 in self.idxs().keys():
                e1 = self.elem(elname1)
                e2 = self.elem(elname2)
                ee = self.op(e1, e2)
                if ee.ename() == self.identity:
                    if e1.ename() == element_name:
                        return e2
        raise
         

class group2(group):

    gset = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    identity = "1"

    def __init__(self):
        # must set the set of elements here
        self.the_set(self.gset)
        self.the_identity(self.identity)

    def op(self, elem1, elem2):
        e1 = int(elem1.ename()) 
        e2 = int(elem2.ename()) 
        ee = e1*e2 % 11 
        return elem(str(ee), self)

    def inv_elem(self, element_name):
        return 

class group3(group):

    gset = ["1", "2", "3", "4", "5"]
    identity = "1"

    def __init__(self):
        # must set the set of elements here
        self.the_set(self.gset)
        self.the_identity(self.identity)

    def op(self, elem1, elem2):
        e1 = int(elem1.ename()) 
        e2 = int(elem2.ename()) 
        ee = e1*e2 % 6
        return elem(str(ee), self)

    def inv_elem(self, element_name):
        return 

class group4(group):

    identity = "1"

    def __init__(self):
        # must set the set of elements here
        gset = []
        for n in xrange(10):
            gset.append(str(2**(n)))
            
    
        self.the_set(gset)
        self.the_identity(self.identity)

    def op(self, elem1, elem2):
        e1 = int(elem1.ename()) 
        e2 = int(elem2.ename()) 
        le1 = math.log(e1,2)
        le2 = math.log(e2,2)
        lee = int(le1 + le2) % 4
        ee = 2**(lee) 
        return elem(str(ee), self)

    def inv_elem(self, element_name):
        return 

class group5(group):

    gset = ["0", "1", "2", "3", "4", "5"]
    identity = "0"

    def __init__(self):
        # must set the set of elements here
        self.the_set(self.gset)
        self.the_identity(self.identity)

    def op(self, elem1, elem2):
        e1 = int(elem1.ename()) 
        e2 = int(elem2.ename()) 
        ee = (e1 + e2) % 6 
        return elem(str(ee), self)

    def inv_elem(self, element_name):
        return 

class group6(group):

    gset = ["0000", "0001", "0010","0011", "0100", "0101", "0110", "0111",
            "1000", "1001", "1010","1011", "1100", "1101", "1110", "1111"]
    identity = "0000"

    def __init__(self):
        # must set the set of elements here
        self.the_set(self.gset)
        self.the_identity(self.identity)

    def op(self, elem1, elem2):
        e1 = int(elem1.ename(), 2) 
        e2 = int(elem2.ename(), 2) 
        ee = "{0:04b}".format(e1 ^ e2) 
        return elem(ee, self)

    def inv_elem(self, element_name):
        return 

class group7(group):
    gset = ["0000", "0011", "1100", "1111"]
    identity = "0000"

    def __init__(self):
        # must set the set of elements here
        self.the_set(self.gset)
        self.the_identity(self.identity)

    def op(self, elem1, elem2):
        e1 = int(elem1.ename(), 2) 
        e2 = int(elem2.ename(), 2) 
        ee = "{0:04b}".format(e1 ^ e2) 
        return elem(ee, self)

    def inv_elem(self, element_name):
        return 

class group8(group):
    gset = ["0001", "0010", "1101", "1110"]
    identity = "0000"

    def __init__(self):
        # must set the set of elements here
        self.the_set(self.gset)
        self.the_identity(self.identity)

    def op(self, elem1, elem2):
        e1 = int(elem1.ename(), 2) 
        e2 = int(elem2.ename(), 2) 
        ee = "{0:04b}".format(e1 ^ e2) 
        return elem(ee, self)

    def inv_elem(self, element_name):
        return 
#******************************************************************************
#                       Experimental Groups
#******************************************************************************

def gcd_int(a,b):
    while b:
        t = b
        b = a%b
        a = t
    return a


#a = 212 
#b = 56 
a = 8 
b = 20 
c = gcd_int(a, b)

print("gcd({0}, {1}) = {2}".format(a, b, c ))
    

g1 = group1()
I = g1.elem("I")
a = g1.elem("a")
b = g1.elem("b")
c = I*I
print c
print(g1)
print(g1.inv_elem('a'))

g2 = group2()
print(g2)
print(g2.is_closed())
print("")

g3 = group3()
print(g3)
print(g3.is_closed())
print("")

g4 = group4()
print(g4)
print(g4.is_closed())
print("")

g5 = group5()
print(g5)
print(g5.is_closed())
print("")

g6 = group6()
print(g6)
print("")

vec = g6.elems()
b0000 = vec[0]
b0011 = vec[3]
b1100 = vec[12]
b1111 = vec[15]

b0001 = vec[1]
b0010 = vec[2]
b0100 = vec[4]
b0101 = vec[5]

print "A coset decomposition of the the previous group (Not unique)"
print "Note that the combination of any two elements from the rows below"
print "are in the subset. The linear space is [4,2,2] (can't be corrected)"
print("")
print str(b0000) + " | " + str(b0011) + " " + str(b1100) + " " + str(b1111)
print "---------------------"
print str(b0000*b0001) + " | " + str(b0011*b0001) + " " + \
      str(b1100*b0001) + " " + str(b1111*b0001)
print str(b0000*b0100) + " | " + str(b0011*b0100) + " " + \
      str(b1100*b0100) + " " + str(b1111*b0100)
print str(b0000*b0101) + " | " + str(b0011*b0101) + " " + \
      str(b1100*b0101) + " " + str(b1111*b0101)

print("")
g7 = group7()
print(g7)
print("")



import abc
import collections as col
import math
import copy

#*****************************************************************************
# This is a representation of an object that needs each of the individual 
# methods overriden
#*****************************************************************************
class darst(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __hash__(self):
        return

    @abc.abstractmethod
    def __eq__(self, d):
        return

    @abc.abstractmethod
    def __str__(self):
        return

    @abc.abstractmethod
    def __mul__(self, d):
        return

#*****************************************************************************
# This is an isomorphic map that maps the different representations between
# one another
#*****************************************************************************
class iso_map(object):
    def __init__(self, imap):
        self._ld = {}
        self._rd = {}

        for m in imap:
            self._ld[m[0]] = m[1] 
            self._rd[m[1]] = m[0] 

    def get_key_left(self, rep1):
        if rep1 in self._ld.keys():
            return copy.deepcopy(self._ld[rep1])
        else:
            return None

    def get_key_right(self, rep2):
        if rep2 in self._rd.keys():
            return copy.deepcopy(self._rd[rep2])
        else:
            return None

#*****************************************************************************
#
#*****************************************************************************
class iso_name_map(iso_map):
    def __init__(self, imap):
        iso_map.__init__(self,imap)

    def get_by_name(self, name):
        return self.get_key_left(name)
            
    def get_by_rep(self, rep):
        return self.get_key_right(rep)

    def subset_iso(self, lnames):
        nimap = []
        for name in lnames:
            if name in self._ld.keys():
                nimap.append((name, self._ld[name]));
        return iso_name_map(nimap)

    def names(self):
        r = []
        for name in self._ld.keys():
            r.append(name)
        return r
            
#*****************************************************************************
#
#*****************************************************************************
class elem(object):
    def __init__(self, iso_n_map, name):
        self._iso_n_map = iso_n_map
        if(name not in self._iso_n_map.names()):
            raise ValueError("Unknown element")
        self._name = name
        
    def __mul__(self, elem):
        r1 = self._iso_n_map.get_by_name(self._name)
        r2 = self._iso_n_map.get_by_name(elem._name)
        r3 = r1*r2
        if(r3 == None):
            return None             
        else:
            return self.__class__(self._iso_n_map, self._iso_n_map.get_by_rep(r3))

    def __str__(self):
        return str(self._iso_n_map.get_by_name(self._name))

    def name(self):
        return self._name

#*****************************************************************************
#
#*****************************************************************************
class gset(object):
    def __init__(self, iso_n_map):
        self._iso_name_map = iso_n_map

    def elem(self, name):
        return elem(self._iso_name_map, name)

    def elems(self):
        le = []
        names = self._iso_name_map.names()
        for name in names:
            le.append(elem(self._iso_name_map, name))
        return le

    def names(self):
        return self._iso_name_map.names()

    def subset(self, values):
        """provide list of elements or lis of element names"""
        if isinstance(values[0], elem):
            names = []
            for el in values:
                names.append(el.name())
            inmap = self._iso_name_map.subset_iso(names)
            return self.__class__(inmap)
        else:  
            inmap = self._iso_name_map.subset_iso(values)
            return self.__class__(inmap)
        
         
    
            

#*****************************************************************************
#*****************************************************************************
# Examples
#*****************************************************************************
#*****************************************************************************
class rep_simple_abelian(darst):
    
    def __init__(self, string):
        """ In this case the representation is a string """
        self._idx = {"I":0, "a":1, "b":2, "c":3}
        self._map = {}
        self._map[(0,0)] = "I"
        self._map[(0,1)] = "a"
        self._map[(0,2)] = "b"
        self._map[(0,3)] = "c"
    
        self._map[(1,0)] = "a"
        self._map[(1,1)] = "b"
        self._map[(1,2)] = "c"
        self._map[(1,3)] = "I"

        self._map[(2,0)] = "b"
        self._map[(2,1)] = "c"
        self._map[(2,2)] = "I"
        self._map[(2,3)] = "a"

        self._map[(3,0)] = "c"
        self._map[(3,1)] = "I"
        self._map[(3,2)] = "a"
        self._map[(3,3)] = "b"

        self._rep = string

    def __hash__(self):
        return hash(self._rep)

    def __eq__(self, d):
        if(d == None):
            return False
        return self._rep == d._rep

    def __str__(self):
        return self._rep 

    def __mul__(self, d):
        r1 = self._idx[self._rep]
        r2 = self._idx[d._rep]
        r3 = self._map[(r1,r2)]
        return rep_simple_abelian(r3)
        

def main():
    imap = [("I", rep_simple_abelian("I")),
            ("a", rep_simple_abelian("a")),
            ("b", rep_simple_abelian("b")),
            ("c", rep_simple_abelian("c"))]

    iname_map = iso_name_map(imap)

    print("start")
    print(iname_map.names())

    g1 = gset(iname_map)

    I = g1.elem("I")
    a = g1.elem("a")
    print(a)
    b = g1.elem("b")
    print(b)
    e3 = a*b

    print(e3)
    print(e3*a)
    print(g1.names())
    print(g1.elems())

    print "next"
    gsub = g1.subset(["I","b"])
    e1 = gsub.elem("I")
    print(e1)
    e2 = gsub.elem("b")
    print(e2)
    print(e1*e1)
    print(e2*e2)
    print "next2"
    gsub2 = g1.subset([I, b])
    print(gsub2.names())
    e1 = gsub.elem("I")
    print(e1)
    e2 = gsub.elem("b")
    print(e2)
    print(e1*e1)
    print(e2*e2)


if __name__ == "__main__": 
    main()
 

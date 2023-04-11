# reed kuivila
# MPCS 51042
# final project - markov speach prediction
# hashtable module

from collections.abc import MutableMapping


class Hashtable(MutableMapping):
    # polynomial constant, used for _hash
    P_CONSTANT = 37

    def __init__(self, capacity, default_value, load_factor, growth_factor):
        self.capacity = capacity
        self._items = [None]*self.capacity
        self.default_value = default_value
        self.load_factor = load_factor
        self.growth_factor = growth_factor
        self.length = 0 


    def _hash(self, key):
        """
        This method takes in a string and returns an integer value
        between 0 and self.capacity.

        This particular hash function uses Horner's rule to compute a large polynomial.

        See https://www.cs.umd.edu/class/fall2019/cmsc420-0201/Lects/lect10-hash-basics.pdf
        """
        val = 0
        for letter in key:
            val = self.P_CONSTANT * val + ord(letter)
        return val % self.capacity


    def __setitem__(self, key, val, deleted = False):
        """move through list and set items if there is space"""
        index = self._hash(key)
        while self._items[index] is not None and self._items[index][0] != key:
            index += 1
            # handle wraparound 
            if index >= self.capacity:
                index = 0  

        if self._items[index] is None:
            self.length += 1
        self._items[index] = (key, val, deleted)

        # rehash if need be
        if (self.length / self.capacity) > self.load_factor:
            self.__rehash__()
        

    def __getitem__(self, key):
        """return values from hash"""
        index = self._hash(key)

        while self._items[index] is not None:
            # return item if not deleted
            if self._items[index][0] == key:# and self._items[index][2] == False:
                #self.length += 1
                return self._items[index][1]

            # increment index, handle wraparound
            index += 1
            index = index % self.capacity
        return self.default_value


    def __delitem__(self, key):
        """ set third tuple item to True, flagging that the item is deleted"""
        index = self._hash(key) 
        deleted = True

        while self._items[index] is not None:
            if self._items[index][0] == key and not self._items[index][2]:
                self._items[index] = self._items[index][0], self._items[index][1], deleted
                self.length -= 1
            self.__rehash__()
            return None

        index += 1
        raise KeyError(key)


    def __len__(self):
        """how many items are not none in the hash table"""
        return self.length


    def __rehash__(self):
        """put items back in """
        self.length = 0
        # store all items in a temp list
        temp = self._items.copy()
        # new capacity 
        self.capacity *= self.growth_factor
        # clear items in the list
        self._items = [None]*self.capacity
        
        for item in temp:
            if item and item[2] == False:
                key = item[0]
                val = item[1] 
                self[key] = val

 
    def __iter__(self):
        """
        You do not need to implement __iter__ for this assignment.
        This stub is needed to satisfy `MutableMapping` however.)

        Note, by not implementing __iter__ your implementation of Markov will
        not be able to use things that depend upon it,
        that shouldn't be a problem but you'll want to keep that in mind.
        """
        raise NotImplementedError("__iter__ not implemented")
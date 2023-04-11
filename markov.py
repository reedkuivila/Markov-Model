# reed kuivila
# MPCS 51042
# final project - markov speach prediction
# markov module

import math
from hashtable import Hashtable

HASH_CELLS = 57
TOO_FULL = 0.5
GROWTH_RATIO = 2

class Markov:
    def __init__(self, k, text, use_hashtable = True):
        """
        Construct a new k-order markov model using the text 'text'.
        """
        self.k = k
        self.text = text
        self.use_hashtable = use_hashtable
        self.distinct_values = len(set(self.text))

        if self.use_hashtable:
            # use hash table module
            self.hash = Hashtable(HASH_CELLS, 0, 0.5, 2)
        else:
            # use default dictionary
            self.hash = {}  

        # text 1 handles wrap around
        text1 = self.text + self.text[0:self.k]
        for i in range(len(self.text)):
            # handle case for K 
            key = text1[i:i + self.k]
            if key in self.hash:
                self.hash[key] += 1
            else: 
                self.hash[key] = 1

            # handle case for K +
            key1 = text1[i: i + self.k + 1]
            if key1 in self.hash:
                self.hash[key1] += 1
            else:
                self.hash[key1] = 1


    def log_probability(self, s):
        """
        Get the log probability of string "s", given the statistics of
        character sequences modeled by this particular Markov model
        This probability is *not* normalized by the length of the string.
        """
     
        # need to handle wrap around
        S = self.distinct_values
        log_prob = 0
        
        # handle wraparound
        s1 = s + s[0:self.k]

        for i in range(len(s)):
            # for K
            key = s1[i: i + self.k]
            # for K + 1
            key1 = s1[i: i + self.k + 1]

            if key in self.hash:
                N = self.hash[key]
            else:# key not in self.hash:
                N = 0

            if key1 in self.hash:
                M = self.hash[key1]
            else: 
                M = 0

            log_prob += math.log((M+1)/(N+S))

        return log_prob


def identify_speaker(speech1, speech2, speech3, k, use_hashtable):
    """
    Given sample text from two speakers (1 and 2), and text from an
    unidentified speaker (3), return a tuple with the *normalized* log probabilities
    of each of the speakers uttering that text under a "order" order
    character-based Markov model, and a conclusion of which speaker
    uttered the unidentified text based on the two probabilities.
    """

    if use_hashtable:
        # instantiate markov models for each speaker w hash table
        speaker1 = Markov(k, speech1, True)
        speaker2 = Markov(k, speech2, True)
    else: 
        # instantiate markov models for each speaker w default dictionary
        speaker1 = Markov(k, speech1, False)
        speaker2 = Markov(k, speech2, False)

    # calculate probabilities for each speaker
    p1 = speaker1.log_probability(speech3)/len(speech3)
    p2 = speaker2.log_probability(speech3)/len(speech3)
 
    # compare each probability
    if p1 > p2:
        return (p1, p2, "A")
    else:
        return (p1, p2, "B")
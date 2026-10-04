# Your names: Simone Pastore 35049968 and Bryan Hamerski 35082532
#
#
#
#

# no other modules allowed
import random,time,sys




class Dictionary:



    #### To complete
    def __init__(self, filename = None):    # filename=None allows filename to have a default value if no filename is found
        self.__words = []
        self.__index = -1   # stores the index found by a search; -1 means "not found"
        self.__steps = 0
        self.__scores = []  # stores the scrabble score for each word
        random.seed(8)                 #same random sequence every time the program runs
        if filename is None:
            self.__name = "N/A"         #default name if there is no filename
        else:
            self.__name = filename[:-4]    #stores the file name without ".txt"

            try:
                file = open(filename, "r")          #opens file in read mode (if file is found)
            except FileNotFoundError:
                print(f"File {filename} does not exist!")
                sys.exit(0)

            print(f"Load {filename}")

            for line in file:
                self.__words.append(line.strip())    #adds each word to the empty list

            file.close()

    def get_name(self):
        return self.__name

    def get_size(self):
        return len(self.__words)

    def get_steps(self):
        return self.__steps

    def insert(self, word):            #appends a new word into the word list
        self.__words.append(word)

    def display(self, score = False):   #iterates through the unsorted list of words and prints them each on their own line
        if score: 
            for i in range(self.get_size()):
                print(self.__words[i], self.__scores[i])
        else:
            for word in self.__words:
                print(word)

    def get_random_list(self, n):
        random_words = []

        for i in range(n):
            random_words.append(self.__words[random.randint(0, self.get_size() - 1)])

        return random_words
    
    def selection_sort(self):    #provided to you
        """Perfom selection sort, must return the time it takes to sort the list of words
        Remark: Routine works 'in-place'"""
        t1 = time.process_time() #capture time
        n=self.get_size()
        for out in range(n-1):        #outer loop
            #find minimum between out+1 and n-1
            imin=out
            for i in range(out+1,n):  #inner loop
                if self.__words[i]<self.__words[imin]: 
                    imin=i #update  minimum index
            #swap (3 step here)
            temp=self.__words[imin]
            self.__words[imin]=self.__words[out]
            self.__words[out]=temp
        t2 = time.process_time() #capture time
        return t2-t1

    def shuffle(self):
        t1 = time.process_time()   # records time before shuffling
        n = len(self.__words)
        for out in range(n-1, 0, -1):   # Fisher-Yates: move backward and swap with a random earlier position
            index = random.randint(0, out)
            self.__words[index], self.__words[out] = self.__words[out], self.__words[index]
        t2 = time.process_time()   # records time after shuffling
        return t2 - t1   # returns the elapsed shuffle time

    def get_index(self):
        return self.__index    # Return the index found by the most recent search

    def lsearch(self, word):
        for i in range(self.get_size()):
            if self.__words[i] == word:
                self.__index = i
                return True

        self.__index = -1     # word was not found anywhere in the list
        return False

    def bsearch(self, word):
        self.__steps = 0
        lower = 0
        upper = self.get_size() - 1

        while lower <= upper:
            mid = lower + (upper-lower)//2
            self.__steps += 1

            if self.__words[mid] == word:
                self.__index = mid
                return True
            elif self.__words[mid] < word:
                lower = mid + 1
            else:
                upper = mid -1

        self.__index = lower
        return False

    def insertion_sort(self):
        t1 = time.process_time()
        n = len(self.__words)
        for out in range(1,n):        # outer loop
            temp = self.__words[out]  # save the word being inserted 
            i = out
            while i > 0 and self.__words[i-1]>temp:
                self.__words[i] = self.__words[i-1]   # shift key
                i = i-1
            self.__words[i] = temp    # insertion
        t2 = time.process_time()
        return t2 - t1

    def enhanced_insertion_sort(self):
        t1 = time.process_time()
        n = len(self.__words)
        for out in range(1,n):
            temp = self.__words[out]

            # binary search to find the insertion position
            lower = 0
            upper = out - 1
            while lower <= upper:
                mid = lower + (upper-lower)//2
                if self.__words[mid] < temp:
                    lower = mid + 1
                else:
                    upper = mid - 1

            # shift larger words one position to the right
            i = out
            while i > lower:
                self.__words[i] = self.__words[i - 1]
                i = i - 1
            self.__words[lower] = temp   # insert word into correct position
            
        t2 = time.process_time()
        return t2 - t1

    def save(self, filename):
       
        file = open(filename, "w")
        for word in self.__words:                  #loops through words and adds them to new file
            file.write(word + "\n")
        file.close()
        print(f"Save {filename}")

    def spell_check(self, filename):
        try:
            file = open(filename, "r")   # opens the text file in read mode
        except FileNotFoundError:
            print(f"File {filename} does not exist!")
            return

        punc = "’!()-[]{};:'\",<>./?@#$%^&*_~"   # punctuation to remove from word edges

        for line in file:                     # read the file one line at a time
            for word in line.split():         # split each line into individual words

                # Create cleaned lowercase version for dictionary searching
                clean_word = word.lower()
                clean_word = clean_word.lstrip(punc)
                clean_word = clean_word.rstrip(punc)

                status = self.bsearch(clean_word)   # binary search requires sorted dictionary

                if status:
                    print(word, end=" ")            # found: print original word normally
                else:
                    print("(" + word + ")", end=" ")   # not found: flag original word

            print()   # move to next output line after finishing this input line

        file.close()


    def anagram(self, word):
        anagram_list = []                   #creates empty anagram list
        word = self.sort_word(word)          #sorts inputted word
        
        for dictionary_word in self.__words:
            if len(dictionary_word) == len(word):              #checks dictionary for words of same length as inputted word
                if self.sort_word(dictionary_word) == word:               #checks if sorted word in dictionary = sorted inputted word
                    anagram_list.append(dictionary_word)                     #appends to anagram list if previosu comments are true.

        return anagram_list

    def crack_lock(self, lock):
        result = Dictionary()         # new dictionary with possible words

        c = 1
        for options in lock:
            c = c * len(options)

        for attempt in range(6*c):
            candidate = ""

            for options in lock:
                index = random.randint(0, len(options) - 1)
                candidate = candidate + options[index]

            if self.bsearch(candidate):

                if not result.lsearch(candidate):
                    result.insert(candidate)

        return result
        
        
    
    @staticmethod  # provided to you
    def get_word_combination(word, combs=['']):
        """ return a list that contains all the letter combinations (all length) of the input 'word' """
        if len(word) == 0:
            return combs
        head, tail = word[0], word[1:]
        combs = combs + list(map(lambda x: x+head, combs))
        return Dictionary.get_word_combination(tail, combs)

    @staticmethod
    def sort_word(word):
        """Return the letters in word sorted alphabetically."""
        letters = list(word)   # convert string into a list so letters can be swapped
        n = len(letters)

        # Selection sort the letters
        for out in range(n-1):
            imin = out
            for i in range(out + 1, n):
                if letters[i] < letters[imin]:
                    imin = i
            # Swap smallest letter into the current position
            temp = letters[imin]
            letters[imin] = letters[out]
            letters[out] = temp
        # Build the sorted string one letter at a time
        sorted_word = ""

        for letter in letters:
            sorted_word = sorted_word + letter

        return sorted_word

    def compute_score_scrabble(self):
        self.__scores = []
        for word in self.__words:
            score = 0

            for letter in word:
                if letter in "eainrtlsu":
                        score = score + 1
                elif letter in "dg":
                    score = score + 2
                elif letter in "bcmp":
                    score = score + 3
                elif letter in "fhvwy":
                    score = score + 4
                elif letter == "k":
                    score = score + 5
                elif letter in "jx":
                    score = score + 8
                elif letter in "qz":
                    score = score + 10

            self.__scores.append(score)

    def score_sort(self):
        n = len(self.__scores)

        # insertion sort
        for out in range(1, n):
            temp_score = self.__scores[out]   # save score being inserted
            temp_word = self.__words[out]     # save its matching word
            i = out

            while i > 0 and self.__scores[i - 1] > temp_score:
                self.__scores[i] = self.__scores[i - 1]
                self.__words[i] = self.__words[i - 1]
                i = i - 1

            self.__scores[i] = temp_score
            self.__words[i] = temp_word

########################################################################
########################################################################


def main():

    ### step-1 test constructor
    name=input("Enter dictionary name (from file 'name'.txt): ")    
    dict1=Dictionary(name+".txt")

    ### step-2 test get_name, get_size, get_random_list        
    print('Name main dictionary:',dict1.get_name())   
    print('Size main dictionary:',dict1.get_size()) 
    print("Five random words:",end=" ")
    rlist=dict1.get_random_list(5) # 5 means the number of random words we want
    for w in rlist: print(w,end=" ")
    print("\n")

    ### step-3 test constructor again
    dict2=Dictionary()
    print('Name extracted dictionary:',dict2.get_name())
    
    ### step-4 test insert and display
    for w in rlist: dict2.insert(w)
    print('Display extracted dictionary:')
    dict2.display()

    ### step-5 test shuffle 
    t=dict2.shuffle()
    print('\nExtracted dictionary shuffled in %ss:'%t)
    print('Display extracted dictionary:')
    dict2.display()

    ### step-6 test linear search
    word="morning"
    print("\nLinear search for the word '%s' in extracted dictionary"%word)
    status=dict2.lsearch(word)
    print("Is '%s' found: %s at index %s"%(word,status,dict2.get_index()))

    ### step-7 sort extracted using selection sort (provided to you)
    t=dict2.selection_sort()
    print('\nExtracted dictionary sorted in %ss:'%t)
    print('Display extracted dictionary:')
    dict2.display()

    ### step-8 test binary search (find it)
    words=["morning","night"]
    for word in words:
        print("\nBinary search for the word '%s' in extracted dictionary"%word)
        status=dict2.bsearch(word) # binary search
        if (status):  # found it!!
            print("Is '%s' found: %s at index %s"%(word,status,dict2.get_index()))
        else:          # Nope did not find it
            print("'%s' is not found so it must be inserted at index %s"%(word,dict2.get_index()))
    


## call the main function if this file is directly executed
if __name__=="__main__":
    main()

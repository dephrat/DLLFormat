#Helper functions
def get_int(s):
    try:
        return True, int(s)
    except ValueError:
        return False, 0
        
def display_all(current):
    display_all_wrapped(current, 0, 0)
    
def display_all_wrapped(current, lvls, idx):
    print(" " * lvls + str(idx) + " " + current.get_text())
    nxts = current.get_next()
    for i, nxt in enumerate(nxts):
        display_all_wrapped(nxt, lvls + 1, i)
    
def save(start, file_name):
    file = open(file_name, "w")
    file_text = save_wrapped(start, 0, 0)
    file.write(file_text)
    
def save_wrapped(current, lvls, idx): # returns string parent[child1,child2,...,childn,],
    parent_text = "," + current.get_text() + '['
    child_text = ""
    nxts = current.get_next()
    for i, nxt in enumerate(nxts):
        child_text += save_wrapped(nxt, lvls + 1, i)
    #child_text = "[" + child_text + "]"
    return parent_text + child_text + "]"
    
def load(file_name):
    file = open(file_name, "r")
    tree_string = file.read()
    return load_wrapped(tree_string)
    
def load_wrapped(tree_string): #parent will be loaded and returned using the information here
# parent will be fully loaded using tree_string, which contains parent[child1,child2,...,childn,], or parent,
    parent = DLL()
    try:
        parent_text = ''
        assert(tree_string[0] == ',' and tree_string[len(tree_string) - 1] == ']')
        i = 1
        while tree_string[i] != '[':
            parent_text += tree_string[i]
            i += 1
        parent.set_text(parent_text)
        i += 1
        while i < len(tree_string) - 1: # if no children, the contents of this loop won't run
            assert(tree_string[i] == ',')
            start_idx = i 
            child_text = ''
            i += 1 #now reading child's name
            while tree_string[i] != '[':
                i += 1
            bracket_balance = 1
            i += 1 #now searching for brackets
            while bracket_balance > 0:
                if tree_string[i] == '[':
                    bracket_balance += 1
                elif tree_string[i] == ']':
                    bracket_balance -= 1
                i += 1
            # now we've reached the end of the child, either comma for next or ]
            parent.next.append(load_wrapped(tree_string[start_idx:i]))
    except:
        print('Error, probably bad input')
    finally:
        return parent

#Class definition
class DLL():
    #def __init__(self):
    def __init__(self):
        self.next = []
        self.prev = None
        self.text = ''
    def set_text(self, _text):
        self.text = _text
    def get_text(self):
        return self.text
    # no set_prev method, we'll do it manually when adding new DLLs.
    def get_prev(self):
        return self.prev
    def add_next(self, _next): #_next is a string
        nxt = DLL()
        nxt.set_text(_next)
        nxt.prev = self
        self.next.append(nxt)
    def remove_next(self, _next, _all=False):
        #for nxt in self.next:
        #    if nxt.get_text() == _next:
        #        self.next.remove(nxt)
        #        if _all == False:
        #            return
        size = len(self.next)
        for i in range(size):
            if self.next[size - i - 1].get_text() == _next:
                self.next.pop(size - i - 1)
                if _all == False:
                    return
    def get_next(self):
        return self.next
    def display_next(self):
        ret = []
        for nxt in self.next:
            ret.append(nxt.get_text())
        return ret


start = DLL()
current = start
cmds = ["help", "help go", "exit", "set", "text", "prev", "add", "list", "list all", "list start", "save", "load", "go"]
#changes: 
#implement remove - removes an indexed next node; optionally promote and keep the children
#modify add/set, don't allow any of ',' '[' ']' because it interferes with loading
#   in future versions, find a way around this, e.g. by not using strings to save.
#replace "" with '' everywhere in the code
#test save and load with empty cases
go_cmds = ['start', 'prev', 'index (in list)', 'cancel']
#Input!!!
while True:
    cmd = input()
    if cmd == "test": #This is just for testing purposes
        #print("Not testing anything at the moment!")
        #file_name = input("Save as2: ")
        #save2(start, file_name)
        file_name = input("File name: ")
        start = load(file_name)
        current = start
    elif cmd == "help":
        for c in cmds:
            print(" " + c)
    elif cmd == "help go":
        for g in go_cmds:
            print(" " + g)
    elif cmd == "exit":
        break
    elif cmd == "set":
        text = input('Text: ')
        current.set_text(text)
    elif cmd == "text":
        print('Text: ' + current.get_text())
    elif cmd == "prev":
        prev = current.get_prev()
        if prev == None:
            print("None")
        else:
            print("Prev: " + prev.get_text())
    #elif cmd == "add next":
    #    text = input('Text: ')
    #    current.add_next(text)
    elif cmd == "add":
        text = input('Text: ')
        while text != "":
            current.add_next(text)
            text = input('Text: ')
    elif cmd == "list":
        nxts = current.display_next()
        for i, n in enumerate(nxts):
            print(str(i) + " " + n)
    elif cmd == "list all":
        display_all(current)
    elif cmd == "list start":
        display_all(start)
    elif cmd == "save":
        file_name = input("Save as: ")
        save(start, file_name)
    elif cmd == "load":
        sureness = input("Current progress will be lost. Continue? (y/n) ")
        if sureness != 'y' and sureness != 'n':
            print("Unrecognized input. Cancelling by default.")
        else:
            file_name = input("File name: ")
            start = load(file_name)
            current = start
    elif cmd == "go":
        where = input('Where: ')
        if where == "start":
            current = start
            print("Now in: " + current.get_text())
        elif where == "prev":
            prev = current.get_prev()
            if prev == None:
                print("None")
            else:
                current = prev
                print("Now in: " + current.get_text())
        elif where == "cancel":
            print("Cancelling 'go' operation.")
        else:
            index = get_int(where)
            if index[0] == True:
                nxts = current.get_next()
                if index[1] >= 0 and index[1] < len(nxts):
                    current = nxts[index[1]]
                    print("Now in: " + str(index[1]) + " " + current.get_text())
                else:
                    print("No such item, try again.")
            else:
                print("Unknown location: Use 'help go' to see a list of available locations.")
    else:
        print("Unrecognized command. Use 'help' to see a list of commands.")
        

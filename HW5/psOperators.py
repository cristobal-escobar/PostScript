from psItems import Value, ArrayValue, FunctionValue
class Operators:
    def __init__(self, scoperule):
        #stack variables
        self.opstack = []  #assuming top of the stack is the end of the list
        self.dictstack = []  #assuming top of the stack is the end of the list
        self.scope = scoperule
        
        #The builtin operators supported by our interpreter
        self.builtin_operators = {
             # TO-DO in part1
             # include the key value pairs where he keys are the PostScrip opertor names and the values are the function values that implement that operator. 
             # Make sure **not to call the functions** 
             "add":self.add,
             "sub": self.sub,
             "mul": self.mul,
             "mod": self.mod,
             "eq": self.eq,
             "lt": self.lt,
             "gt": self.gt,
             "array": self.array,
             "length": self.length,
             "getinterval": self.getinterval,
             "putinterval": self.putinterval,
             "aload": self.aload,
             "astore": self.astore,
             "pop": self.pop,
             "stack": self.stack,
             "dup": self.dup,
             "copy": self.copy,
             "count": self.count,
             "clear": self.clear,
             "exch": self.exch,
             "roll": self.roll,
            #  "dict": self.psDict,
            #  "begin": self.begin,
            #  "end": self.end,
             "def": self.psDef,
             "if": self.psIf,
             "ifelse": self.psIfelse,
             "repeat": self.repeat,
             "forall": self.forall,
             "for":self.psFor

        }
    #-------  Operand Stack Operators --------------
    """
        Helper function. Pops the top value from opstack and returns it.
    """
    def opPop(self):
        if self.opstack:
            popValue = self.opstack[-1]
            self.opstack.pop()
            return popValue
        else:
            print("opstack is empty")
            return None
    """
       Helper function. Pushes the given value to the opstack.
    """
    def opPush(self,value):
        self.opstack.append(value)
        
    #------- Dict Stack Operators --------------
    
    """
       Helper function. Pops the top dictionary from dictstack and returns it.
    """   
    def dictPop(self):
        if self.dictstack:
            popDict = self.dictstack[-1]
            self.dictstack.pop()
            return popDict
        else:
            print("dictstack is empty")
            return None
    """
       Helper function. Pushes the given dictionary onto the dictstack. 
    """   
    def dictPush(self,d):
        # size = len(self.dictstack) -1
        if d[1] == {}: #or size < 0:
            self.dictstack.append(d)
        else:
            for key,value in d[1].items():
                self.dictstack[-1][1][key] = value
                          
                    
            # for key,value in d[1].items():
            #     k = key
            #     v = value
            # theK = k[1:]
            # if self.lookup(theK) is None:
            #     self.dictstack.append(d)
            # else:
            #     dictLen = len(self.dictstack) - 1
            #     while (dictLen >= 0):
            #         if k in self.dictstack[dictLen][1].keys(): 
            #             self.dictstack[dictLen][1][k] = value
            #         dictLen -= 1

    """
       Helper function. Adds name:value pair to the top dictionary in the dictstack.
       (Note: If the dictstack is empty, first adds an empty dictionary to the dictstack then adds the name:value to that. 
    """   
    def define(self,name, value):
        if not self.dictstack:
            self.dictPush((0, {}))
            self.dictstack[0][1][name] = value
        else:
            self.dictstack[-1][1][name] = value
            # self.dictPush({name:value}) 

    """
       Helper function. Searches the dictstack for a variable or function and returns its value. 
       (Starts searching at the top of the dictstack; if name is not found returns None and prints an error message.
        Make sure to add '/' to the begining of the name.)
    """
    def lookup(self,name):
        newName = '/' + name
        count = len(self.dictstack) - 1
        if self.scope == "dynamic":
            while(count >= 0):
                if newName in self.dictstack[count][1]:
                    return self.dictstack[count][1][newName]
                count -= 1
            print("name not found!")
            return None
        else:
            def staticLookup(target, size):
                if target in self.dictstack[size][1]:
                    return self.dictstack[size][1][target]
                else:
                    if size == 0:
                        print("name not found!")
                        return None
                    else:
                        return staticLookup(target, self.dictstack[size][0])
            return staticLookup(newName, count)
        
    #------- Arithmetic Operators --------------
    
    """
       Pops 2 values from opstack; checks if they are numerical (int); adds them; then pushes the result back to opstack. 
    """   
    def add(self):
        if len(self.opstack) > 1:
            op1 = self.opPop() # top value
            op2 = self.opPop() # bottom value
            if isinstance(op1,int) and isinstance(op2,int):
                self.opPush(op1 + op2)
            else:
                print("Error: add - one of the operands is not a number value")
                self.opPush(op2)  # bottom value
                self.opPush(op1)   # top value
        else:
            print("Error: add expects 2 operands")
 
    """
       Pop 2 values from opstack; checks if they are numerical (int); subtracts them; and pushes the result back to opstack. 
    """   
    def sub(self):
        if len(self.opstack) > 1:
            op1 = self.opPop() # top value
            op2 = self.opPop() # bottom value
            if isinstance(op1,int) and isinstance(op2,int):
                self.opPush(op2 - op1)
            else:
                print("Error: sub - one of the operands is not a number value")
                self.opPush(op2)  # bottom value
                self.opPush(op1)   # top value
        else:
            print("Error: sub expects 2 operands")

    """
        Pops 2 values from opstack; checks if they are numerical (int); multiplies them; and pushes the result back to opstack. 
    """    
    def mul(self):
        if len(self.opstack) > 1:
            op1 = self.opPop() # top value
            op2 = self.opPop() # bottom value
            if isinstance(op1,int) and isinstance(op2,int):
                self.opPush(op1 * op2)
            else:
                print("Error: mul - one of the operands is not a number value")
                self.opPush(op2)  # bottom value
                self.opPush(op1)   # top value
        else:
            print("Error: mul expects 2 operands")

    """
        Pops 2 values from stack; checks if they are int values; calculates the remainder of dividing the bottom value by the top one; 
        pushes the result back to opstack.
    """ 
    def mod(self):
        if len(self.opstack) > 1:
            op1 = self.opPop() # top value
            op2 = self.opPop() # bottom value
            if isinstance(op1,int) and isinstance(op2,int):
                self.opPush(op2 % op1)
            else:
                print("Error: mod - one of the operands is not a number value")
                self.opPush(op2)  # bottom value
                self.opPush(op1)   # top value
        else:
            print("Error: mod expects 2 operands")

    #---------- Comparison Operators  -----------------
    """
       Pops the top two values from the opstack; pushes "True" is they are equal, otherwise pushes "False"
    """ 
    def eq(self):
        if len(self.opstack) > 1:
            op1 = self.opPop() # top value
            op2 = self.opPop() # bottom value
            if op1 == op2:
                self.opPush(True)
            else:
                self.opPush(False)
        else:
            print("Error: eq expects 2 operands")

    """
       Pops the top two values from the opstack; pushes "True" if the bottom value is less than the top value, otherwise pushes "False"
    """ 
    def lt(self):
        if len(self.opstack) > 1:
            op1 = self.opPop() # top value
            op2 = self.opPop() # bottom value
            if op2 < op1:
                self.opPush(True)
            else:
                self.opPush(False)
        else:
            print("Error: lt expects 2 operands")

    """
       Pops the top two values from the opstack; pushes "True" if the bottom value is greater than the top value, otherwise pushes "False"
    """ 
    def gt(self):
        if len(self.opstack) > 1:
            op1 = self.opPop() # top value
            op2 = self.opPop() # bottom value
            if op2 > op1:
                self.opPush(True)
            else:
                self.opPush(False)
        else:
            print("Error: gt expects 2 operands")

    # ------- Array Operators --------------
    """ 
       Pops the array length (an int value) from the opstack and initializes an array constant (ArrayValue) having the given length. 
       Initializes the elements in the value of the ArrayValue to None. Pushes the ArrayValue to the opstack.
    """
    def array(self):
        if len(self.opstack) > 0:
            # self.length()
            arrLength = self.opPop()
            arrayConst = ArrayValue([])
            i = 0
            while (i < arrLength):
                arrayConst.value.append(None)
                i += 1
            self.opPush(arrayConst)
        else:
            print("Error: array expects 1 operand")

    """ 
       Pops an array value from the operand opstack and calculates the length of it. Pushes the length back onto the opstack.
       The `length` method should support ArrayValue values.
    """
    def length(self):
        if len(self.opstack) > 0:
            arrValue = self.opPop()
            if isinstance(arrValue,ArrayValue):
                arrLen = len(arrValue.value)
            else:
                arrLen = len(arrValue)
            self.opPush(arrLen)
        else:
            print("Error: length expects 1 operand")
    """ 
        Pops the `count` (int), an (zero-based) start `index`, and an array constant (ArrayValue) from the operand stack.  
        Pushes the slice of the array of length `count` starting at `index` onto the opstack.(i.e., from `index` to `index`+`count`) 
        If the end index of the slice goes beyond the array length, will give an error. 
    """
    def getinterval(self):
        if len(self.opstack) > 2:
            count = self.opPop()
            index = self.opPop()
            arr = self.opPop()
            if isinstance(count, int) and isinstance(index, int) and isinstance(arr, ArrayValue):
                arrLen = len(arr.value)
                end = index + count
                if index < arrLen and end <= arrLen:
                    newList = arr.value[index:end]
                    self.opPush(ArrayValue(newList))
                else:
                    print("Error: index is out of bounds")
            else:
                print("one or more operands are not the expected type")
        else:
            print("Error: getinterval expects 3 operands")

    """ 
        Pops an array constant (ArrayValue), start `index` (int), and another array constant (ArrayValue) from the operand stack.  
        Replaces the slice in the bottom ArrayValue starting at `index` with the top ArrayValue (the one we popped first). 
        The result is not pushed onto the stack.
        The index is 0-based. If the end index of the slice goes beyond the array length, will give an error. 
    """
    def putinterval(self):
        if len(self.opstack) > 2:
            arr1 = self.opPop()
            index = self.opPop()
            arr2 = self.opPop()
            arrLen2 = len(arr2.value)
            arrLen1 = len(arr1.value)
            if index < arrLen2:
                i = 0
                while(i < arrLen1):
                    arr2.value[index] = arr1.value[i]
                    i += 1
                    index += 1
            else:
                print("Error: index is out of bounds")

        else:
            print("Error: getinterval expects 3 operands")
            

    """ 
        Pops an array constant (ArrayValue) from the operand stack.  
        Pushes all values in the array constant to the opstack in order (the first value in the array should be pushed first). 
        Pushes the orginal array value back on to the stack. 
    """
    def aload(self):
        if self.opstack:
            arrConst = self.opPop()
            if isinstance(arrConst, ArrayValue):
                i = 0
                newList = []
                while (i < len(arrConst.value)):
                    newList.append(arrConst.value[i])
                    i += 1
                j = 0
                while (j < len(newList)):
                    self.opPush(newList[j])
                    j += 1
                self.opPush(arrConst)
            else:
                print("element found in opstack is not an ArrayValue type")
        else:
            print("aload requires at least an array in opstack")
        
    """ 
        Pops an array constant (ArrayValue) from the operand stack.  
        Pops as many elements as the length of the array from the operand stack and stores them in the array constant. 
        The value which was on the top of the opstack will be the last element in the array. 
        Pushes the array value back onto the operand stack. 
    """
    def astore(self):
        if self.opstack:
            arrConst = self.opPop()
            if isinstance(arrConst, ArrayValue):
                i = 0
                newList = []
                while (i < len(arrConst.value)):
                    newList.append(self.opPop())
                    i += 1
                j = 1
                while (j < len(newList) + 1):
                    arrConst.value[j - 1] = newList[-j]
                    j += 1
                self.opPush(arrConst)
            else:
                print("element found in opstack is not an ArrayValue type")
        else:
            print("aload requires at least an array in opstack")

    #------- Stack Manipulation and Print Operators --------------

    """
       This function implements the Postscript "pop operator". Calls self.opPop() to pop the top value from the opstack and discards the value. 
    """
    def pop (self):
        self.opPop()

    """
       Prints the opstack. The end of the list is the top of the stack. 
    """
    def stack(self):
        i = len(self.opstack) - 1
        print("===**opstack**===")
        while(i >= 0):
            print("{}\n".format(self.opstack[i]))
            i -= 1

        print( "===**dictstack**===")
        i = len(self.dictstack) - 1
        while(i >= 0):
            print("---- {}---- {} ----".format(i, self.dictstack[i][0]))
            for key, values in self.dictstack[i][1].items():
                print("{}   {}".format(key, values))
            i -= 1
        print("=================")

    """
       Copies the top element in opstack.
    """
    def dup(self):
        if self.opstack:
            newElem = self.opstack[-1]
            self.opPush(newElem)

    """
       Pops an integer count from opstack, copies count number of values in the opstack. 
    """
    def copy(self):
        if self.opstack:
            newL = []
            num = self.opPop()
            i = 1
            if len(self.opstack) >= num:
                while (i <= num):
                    newL.append(self.opstack[-i])
                    i += 1
                i = 1
                while(i <= num):
                    self.opPush(newL[-i])
                    i += 1
            else:
                print("count number is bigger then opstack length")

    """
        Counts the number of elements in the opstack and pushes the count onto the top of the opstack.
    """
    def count(self):
        n = len(self.opstack)
        self.opPush(n)

    """
       Clears the opstack.
    """
    def clear(self):
        while(self.opstack):
            self.opPop()
        
    """
       swaps the top two elements in opstack
    """
    def exch(self):
        if len(self.opstack) >=2:
            value1 = self.opPop()
            value2 = self.opPop()
            self.opPush(value1)
            self.opPush(value2)

    """
        Implements roll operator.
        Pops two integer values (m, n) from opstack; 
        Rolls the top m values in opstack n times (if n is positive roll clockwise, otherwise roll counter-clockwise)
    """
    def roll(self):
        if len(self.opstack) > 2:
            n = self.opPop()
            m = self.opPop()
            mValues = []
            if m <= len(self.opstack):
                if n < 0:
                    j = 0
                    while j < (m + n):
                        i = 0
                        while i < m:
                            mValues.append(self.opPop())
                            i += 1
                        i = 0
                        while i < m:
                            self.opPush(mValues[-i])
                            i += 1
                        mValues = []
                        j += 1
                else:
                    j = 0
                    while j < n:
                        i = 0
                        while i < m:
                            mValues.append(self.opPop())
                            i += 1
                        i = 0
                        while i < m:
                            self.opPush(mValues[-i])
                            i += 1
                        mValues = []
                        j += 1
                        
            else:
                print("m value is bigger then opstack length")
    """
       Pops an integer from the opstack (size argument) and pushes an  empty dictionary onto the opstack.
    """
    # def psDict(self):
    #     if self.opstack:
    #         i = self.opPop()
    #         self.opPush({})
    #     else:
    #         print("opstack is empty")

    # """
    #    Pops the dictionary at the top of the opstack; pushes it to the dictstack.
    # """
    # def begin(self):
    #     if self.opstack:
    #         newDict = self.opPop()
    #         self.dictPush(newDict)
    #     else:
    #         print("opstack is empty")
    # """
    #    Removes the top dictionary from dictstack.
    # """
    # def end(self):
    #     if self.dictstack:
    #         self.dictPop()
    #     else:
    #         print("dickstack is empty")

    """
       Pops a name and a value from opstack, adds the name:value pair to the top dictionary by calling define.  
    """
    def psDef(self):
        if len(self.opstack) > 1:
            value = self.opPop()
            name = self.opPop()
            if isinstance(name, str):
                if name[0] == '/':
                    self.define(name, value)
                else:
                    print("a '/' is needed before variable name")
            else:
                print("given operand name is not a string") 
        else:
            print("def requires 2 operands")

    # ------- if/ifelse Operators --------------
    """
       Implements if operator. 
       Pops the `ifbody` and the `condition` from opstack. 
       If the condition is True, evaluates the `ifbody`.  
    """
    def psIf(self):
        # TO-DO in part2
        ifbody = self.opPop()
        condition = self.opPop()
        if condition:
            self.dictPush((self.dictstack[-1][0], {}))
            ifbody.apply(self)
            self.dictPop()

    """
       Implements ifelse operator. 
       Pops the `elsebody`, `ifbody`, and the condition from opstack. 
       If the condition is True, evaluate `ifbody`, otherwise evaluate `elsebody`. 
    """
    def psIfelse(self):
        # TO-DO in part2
        elsebody = self.opPop()
        ifbody = self.opPop()
        condition = self.opPop()
        if isinstance(condition, bool):
            self.dictPush((self.dictstack[-1][0], {}))
            if condition == True:
                # if isinstance
                ifbody.apply(self)
            else:
                elsebody.apply(self)
        else:
            print("Condition must be a boolean value")
        self.dictPop()

    #------- Loop Operators --------------
    """
       Implements repeat operator.   
       Pops the `loop_body` (FunctionValue) and loop `count` (int) arguments from opstack; 
       Evaluates (applies) the `loopbody` `count` times. 
       Will be completed in part-2. 
    """  
    def repeat(self):
        #TO-DO in part2
        body = self.opPop()
        count = self.opPop()
        self.dictPush((self.dictstack[-1][0], {}))
        while (count > 0):
            body.apply(self)
            count -= 1
        self.dictPop()
        
    """
       Implements forall operator.   
       Pops a `codearray` (FunctionValue) and an `array` (ArrayValue) from opstack; 
       Evaluates (applies) the `codearray` on every value in the `array`.  
       Will be completed in part-2. 
    """ 
    def forall(self):
        # TO-DO in part2
        codearray = self.opPop()
        arr = self.opPop()
        self.dictPush((self.dictstack[-1][0], {}))
        for v in arr.value:
            self.opPush(v)
            codearray.apply(self)
        self.dictPop()
    
    def psFor(self):
        codearray = self.opPop()
        finalValue = self.opPop()
        incrValue = self.opPop()
        initialValue = self.opPop()
        self.dictPush((self.dictstack[-1][0], {}))
        if incrValue > 0:
            while(initialValue <= finalValue):
                self.opPush(initialValue)
                codearray.apply(self)
                initialValue = initialValue + incrValue
        elif incrValue < 0:
            while(initialValue >= finalValue):
                self.opPush(initialValue)
                codearray.apply(self)
                initialValue = initialValue + incrValue
        self.dictPop()

    #--- used in the setup of unittests 
    def clearBoth(self):
        self.opstack[:] = []
        self.dictstack[:] = []

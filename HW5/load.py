import sys
from psParser import read
from psOperators import Operators
from psItems import ArrayValue, Literal, Name, Array,Block
from colors import *


testinput1 = """
    /x 4 def
    /g { x stack } def
    /f { /x 7 def g } def
    f
    """

testinput2 = """
    /x 40 def
    [1 2 3 4] dup 3 [x] putinterval /x exch def
    /g { x stack } def
    /f { /x [10 20 30 40] def g } def
    f
    """

testinput3 = """
    /m 50 def
    /n 100 def
    /egg1 {/m 25 def n} def
    /chic
    	{ /n 1 def
	      /egg2 { n stack} def
	      n m
	      egg1
          m
	      egg2
	    } def
    n
    chic
        """

testinput4 = """
    /x 10 def
    /A { x } def
    /C { /x 40 def A stack } def
    /B { /x 30 def /A { x 2 mul } def C } def
    B
    """

testinput5 = """
    /x 2 def
    /n 5  def
    /A { 0 1 1 10 { add } for} def
    /C { /n 3 def /x 40 def A stack } def
    /B { /x 30 def /A { x } def C } def
    B
    """

testinput6 = """
    /myfalse {1 2 eq} def
    /out true def 
    /xand { true eq {pop myfalse} {pop true} ifelse dup /x exch def stack} def 
    /myput { out dup /x exch def xand } def 
    /f { /out myfalse def myput } def 
    myfalse  f
    """

testinput7 = """
    /x [1 2 3 4] def
    /A { 0  x {add} forall } def
    /C { /x [10 20 30 40 50] def A stack } def
    /B { /x [6 7 8 9] def /A { x } def C } def
    B
    """

testinput8 = """
    /x 2 3 4 5 4 array astore def
    /a 10 def  
    /A { x } def
    /C { /x [a 2 mul a 3 mul dup a 4 mul] def A  a x stack } def
    /B { /x [6 7 8 9] def /A { x } def /a 5 def C } def
    B
    """

"""
 ***** ADD YOUR TESTS HERE  *****
"""
testinput9 = """
     /x 7 def
    /y 2 def
    /z [1 2 3 4] def
    /A {z {x add y mul} forall} def
    /B {/x 10 def /y 3 def A stack} def
    B
"""

testinput10 = """
    /x 5 def
    /y 10 def
    /A {x y add} def
    /B {/x 2 def A stack} def
    /C {/x 20 def /y 30 def B} def
    C
"""

testinput11 = """
    /x 3 def
    /y 4 def
    /z [10 20 30] def
    /A {z {x mul y add} forall} def
    /B {/x 2 def /y 5 def A stack} def
    B
"""

testinput12 = """
    /x 5 def
    /y 3 def
    /z true def
    /A {x y add} def
    /B {/x 2 def /z false def A stack} def
    /C {/y 10 def /z true def B} def
    C
"""

""" Make sure to add your test inputs to the below list as well!"""
tests = [testinput1,testinput2,testinput3,testinput4,testinput5,testinput6,testinput7,testinput8,
          testinput9, testinput10, testinput11, testinput12]

# program start
if __name__ == '__main__':
    
    psstacks_s = Operators("static")  
    psstacks_d = Operators("dynamic")  
    testnum = 1
    for testcase in tests:
        try:
            print("\n-- TEST {} --".format(testnum))
            expr_list = read(testcase)
            print("\nSTATIC")
            # interpret using static scoping rule
            for expr in expr_list:
                expr.evaluate(psstacks_s) 
            print("\nDYNAMIC")
            # interpret using dynamic scoping rule
            for expr in expr_list:
                expr.evaluate(psstacks_d)    
            # clear the Stack objects 
            psstacks_s.clearBoth()
            psstacks_d.clearBoth()
        except (SyntaxError, NameError, TypeError, Exception) as err:
            print(type(err).__name__ + ':', err)
        testnum += 1
        # clear the Stack objects 
        psstacks_s.clearBoth()
        psstacks_d.clearBoth()
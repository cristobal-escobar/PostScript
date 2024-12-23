import unittest
from psParser import read
from psItems import  Literal, Name, Array, Block, Value, ArrayValue, FunctionValue
from psOperators import Operators



class HW4Tests(unittest.TestCase):

    def setUp(self):
        #create the Stack object
        self.psstacks = Operators('static')
        #clear the opstack and the dictstack
        self.psstacks.clearBoth() 
        # self.psstacks.dictstack.append({})

        self.opstack_output= {
            'test1': [6, 2], 
            'test2': [True, True, False, True], 
            'test3': [1, 10], 
            'test4': [10, 1], 
            'test5': [100, 10, 1], 
            'test6': [2, 2], 
            'test7': [ArrayValue([1, 2, 3, 4, 5, 6, 7])], 
            'test8': [ArrayValue([1, 2, 3, 4, 5, ArrayValue([6, 3, 4]), ArrayValue([True])])], 
            'test9': [4, 6], 
            'test10': [ArrayValue([4, 5, 6]), ArrayValue([8, 9, 10])], 
            'test11': [ArrayValue([1, 2, 3, 40, 50, 60, 70, 8, 9, 10]), ArrayValue([1, 2, 3, 4, 5, 6, 40, 50, 60, 70])], 
            'test12': [True], 
            'test13': [1, 2, ArrayValue([3, 4, 5, 6])], 
            'test14': [ArrayValue([1, 2, 3, 4]), False], 
            'test15': [1, 2, 3, 4, 5, 3, 4, 5, 8], 
            'test16': [ArrayValue([1, 2, 6, 7, 8, 9, 3, 4, 5])], 
            'test17': [ArrayValue([1, 2, 7, 8, 9, 3, 4, 5, 6])], 
            'test18': [5], 
            'test19': [2], 
            'test20': [256], 
            'test21': [4, 8, 12, 16], 
            'test22': [16, 14, 12, 10, 8, 6, 4, 2], 
            'test23': [1, 4, 9, 16], 
            'test24': [ArrayValue([1, 4, 9, 16])], 
            'test25': [9], 
            'test26': [10], 
            'test27': [10, 3, 10, 20, 1, 2], 
            'test28': [True], 
            'test29': [False, True, 10], 
            'test30': [120], 
            'test31': [720], 
            'test32': [720], 
            'test33': [1, 2, 3, 4, 5, True],
            'test34': [165],
            'test35': [720], 
            'test36': [30], 
            'test37': [True, True, True],
            'test38': [10, 20, 30, 40, 50, 60, 70, 80, 90],
            'test39': [2, 2, 6, 4, 10, 6, 14, 8, 18, 10], 
            'test40': [32], 
            'test41': [True], 
            'test42': [5040]}

    def compareObjectData(self,obj1,obj2):
        if type(obj1) != type(obj2):
            return False
        if isinstance(obj1,Literal):
            return obj1.value == obj2.value
        elif isinstance(obj1,Array) or isinstance(obj1,Block):
            for i in range(0,len(obj1.value)):
                if self.compareObjectData(obj1.value[i],obj2.value[i])== False:
                    return False
            return True
        elif isinstance(obj1,Name):
            return obj1.var_name == obj2.var_name
        elif isinstance(obj1,ArrayValue):
            for i in range(0,len(obj1.value)):
                if self.compareObjectData(obj1.value[i],obj2.value[i])== False:
                    return False
            return True
        elif isinstance(obj1,FunctionValue) :
            for i in range(0,len(obj1.value)):
                if self.compareObjectData(obj1.value[i],obj2.value[i])== False:
                    return False
            return True
        else:
            return obj1 == obj2


    def test_input1(self):
        testinput1 = """
            /x 10 def
 /A { x } def
 /C { /x 40 def A stack } def
 /B { /x 30 def /A { x 2 mul } def C } def
 B
 """
        test_case = 'test{}'.format(1)
        expr_list = read(testinput1)
        for expr in expr_list:
            expr.evaluate(self.psstacks)
        # self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
        self.psstacks.stack()
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input2(self):
        testinput2 = """
            10 20 lt
            20 15 gt
            [1 2 3 4] [1 2 3 4] eq
            [1 2 3 4] dup eq 
        """
        test_case = 'test{}'.format(2)
        expr_list = read(testinput2)
        for expr in expr_list:
            expr.evaluate(self.psstacks)
        self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input3(self):
        testinput3 = """
            /x 1 def
            x
            /x 10 def
            x
        """
        
        test_case = 'test{}'.format(3)
        expr_list = read(testinput3)
        for expr in expr_list:
            expr.evaluate(self.psstacks)
        self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))


    def test_input4(self):
        testinput4 = """
            /x 1 def
            1 dict begin /x 10 def x end
            x
        """
        test_case = 'test{}'.format(4)
        expr_list = read(testinput4)
        for expr in expr_list:
            expr.evaluate(self.psstacks)
        self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input5(self):
        testinput5 = """
            /x 1 def
            1 dict begin /x 10 def  
                1 dict begin /x 100 def x end 
                x 
            end
            x
        """
        test_case = 'test{}'.format(5)
        expr_list = read(testinput5)
        for expr in expr_list:
            expr.evaluate(self.psstacks)
        self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input6(self):
        testinput6 = """
            /x 1 def
            /y 2 def
            1 dict begin /x 10 def  
                1 dict begin /x 100 def y end 
                y
            end
        """ 
        test_case = 'test{}'.format(6)
        expr_list = read(testinput6)
        for expr in expr_list:
            expr.evaluate(self.psstacks)
        self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input7(self):
        testinput7 = """
            /x 3 def 
            /y 4 def
            [1 2 x x 1 add 5 x x add x y add ] 
        """
        test_case = 'test{}'.format(7)
        expr_list = read(testinput7)
        for expr in expr_list:
            expr.evaluate(self.psstacks)
        self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input8(self):
        testinput8 = """
            /x 3 def 
            /y 4 def
            [1 2 x x 1 add 5 [x x add x y] [true]] 
        """
        test_case = 'test{}'.format(8)
        expr_list = read(testinput8)
        for expr in expr_list:
            expr.evaluate(self.psstacks)
        self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input9(self):
        testinput9 = """
            [1 2 3 4] length
            [1 2 3 [4 5] 6 [false] ] length
        """
        test_case = 'test{}'.format(9)
        expr_list = read(testinput9)
        for expr in expr_list:
            expr.evaluate(self.psstacks)
        self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input10(self):
        testinput10 = """
            [1 2 3 4 5 6 7 8 9 10] 3 3 getinterval
            [1 2 3 4 5 6 7 8 9 10] 7 3 getinterval
        """
        test_case = 'test{}'.format(10)
        expr_list = read(testinput10)
        for expr in expr_list:
            expr.evaluate(self.psstacks)
        self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input11(self):
        testinput11 = """
            [1 2 3 4 5 6 7 8 9 10] dup 3 [40 50 60 70]   putinterval
            [1 2 3 4 5 6 7 8 9 10] dup 6 [40 50 60 70]   putinterval
        """
        test_case = 'test{}'.format(11)
        expr_list = read(testinput11)
        for expr in expr_list:
            expr.evaluate(self.psstacks)
        self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
        for i in range(0,len(self.opstack_output[test_case])):
            self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input12(self):
            testinput12 = """
                [1 2 3 4 5 6] aload pop add add add add add 21 eq
            """
            test_case = 'test{}'.format(12)
            expr_list = read(testinput12)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input13(self):
            testinput13 = """
                1 2 3 4 5 6 4 array astore 
            """
            test_case = 'test{}'.format(13)
            expr_list = read(testinput13)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input14(self):
            testinput14 = """
                [1 2 3 4] dup /arr exch def 
                [1 2 3 4] arr eq
            """
            test_case = 'test{}'.format(14)
            expr_list = read(testinput14)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input15(self):
            testinput15 = """
                1 2 3 4 5 3 copy count
            """
            test_case = 'test{}'.format(15)
            expr_list = read(testinput15)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input16(self):
            testinput16 = """
                1 2 3 4 5 6 7 8 9 7 4 roll 9 array astore
            """
            test_case = 'test{}'.format(16)
            expr_list = read(testinput16)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input17(self):
            testinput17 = """
                1 2 3 4 5 6 7 8 9 7 -4 roll 9 array astore
            """
            test_case = 'test{}'.format(17)
            expr_list = read(testinput17)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))


    def test_input18(self):
            testinput18 = """
                /isNeg { 0 lt } def  -5 dup isNeg { -1 mul } if
            """
            test_case = 'test{}'.format(18)
            expr_list = read(testinput18)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input19(self):
            testinput19 = """
                /isNeg { 0 lt } def  -1 dup isNeg { -2 mul } { 3 mul} ifelse
            """
            test_case = 'test{}'.format(19)
            expr_list = read(testinput19)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))


    def test_input20(self):
            testinput20 = """
                1 8 {2 mul } repeat 
            """
            test_case = 'test{}'.format(20)
            expr_list = read(testinput20)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input21(self):
            testinput21 = """
                2 2 8 {2 mul } for 
            """
            test_case = 'test{}'.format(21)
            expr_list = read(testinput21)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input22(self):
            testinput22 = """
                8 -1  1 {2 mul } for 
            """
            test_case = 'test{}'.format(22)
            expr_list = read(testinput22)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input23(self):
            testinput23 = """
                [1 2 3 4] {dup mul } forall
            """
            test_case = 'test{}'.format(23)
            expr_list = read(testinput23)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input24(self):
            testinput24 = """
                1 2 3 4 4 array astore /arr exch def arr {dup mul } forall arr astore pop arr
            """
            test_case = 'test{}'.format(24)
            expr_list = read(testinput24)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input25(self):
            testinput25 = """
                /x 4 def 
                /square {dup mul} def
                [x 1 x sub 1] /arr exch def  
                arr 1 1 getinterval aload pop dup
                0 gt 
                {2 mul} {square} ifelse
            """
            test_case = 'test{}'.format(25)
            expr_list = read(testinput25)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input26(self):
            testinput26 = """
                /x 10 def
                /y 20 def
                /x 0 def
                /y 2 def
                5 { x y add /x exch def } repeat 
                x
            """
            test_case = 'test{}'.format(26)
            expr_list = read(testinput26)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input27(self):
            testinput27 = """
                /x 1 def
                /y 2 def
                1 dict begin
                /x 10 def
                1 dict begin /y 3 def x y end
                /y 20 def
                x y
                end
                x y
            """
            test_case = 'test{}'.format(27)
            expr_list = read(testinput27)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input28(self):
            testinput28 = """
                1 2 3 4 5  15 5 { exch sub} repeat 0 eq
            """
            test_case = 'test{}'.format(28)
            expr_list = read(testinput28)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input29(self):
            testinput29 = """
                [1 2 3 4] {2 mod 0 eq} forall 
                {
                    { /x 1 def }
                    { /x 10 def }
                    ifelse
                } if
                x
            """
            test_case = 'test{}'.format(29)
            expr_list = read(testinput29)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input30(self):
            testinput30 = """
                /n 5 def
                /fact {
                    0 dict begin
                    /n exch def
                    n 2 lt
                    { 1}
                    {n 1 sub fact n mul }
                    ifelse
                    end
                } def
                n fact
            """
            test_case = 'test{}'.format(30)
            expr_list = read(testinput30)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input31(self):
            testinput31 = """
                /fact {
                    0 dict
                    begin
                        /n exch def
                        1
                        n { n mul /n n 1 sub def } repeat
                    end
                } def
                6 fact
            """
            test_case = 'test{}'.format(31)
            expr_list = read(testinput31)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input32(self):
            testinput32 = """
                /fact {
                    0 dict
                    begin
                        /n exch def
                        1
                        n -1 1 { mul /n n 1 sub def } for 
                    end
                } def
                6 fact
            """
            test_case = 'test{}'.format(32)
            expr_list = read(testinput32)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input33(self):
            testinput33 = """
                1 2 3 4 5 count copy 15 1 1 5 {pop exch sub} for 0 eq
            """
            test_case = 'test{}'.format(33)
            expr_list = read(testinput33)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input34(self):
            testinput34 = """
                /x 1 def
                /y 2 def
                /x 10 def
                /y 20 def
                0 x 1 y {add} for
            """
            test_case = 'test{}'.format(34)
            expr_list = read(testinput34)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input35(self):
            testinput35 = """
            /fact {
                    0 dict
                    begin
                        /n exch def
                        1
                        n -1 1 { mul /n n 1 sub def } for 
                    end
                } def
                6 fact
            """
            test_case = 'test{}'.format(35)
            expr_list = read(testinput35)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input36(self):
            testinput36 = """
                /sumArray {0 exch aload pop count n sub {add} repeat } def
                /x 5 def
                /y 10 def
                /n 1 def
                [x y x y add] sumArray
            """
            test_case = 'test{}'.format(36)
            expr_list = read(testinput36)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input37(self):
            testinput37 = """
                [ 1 2 3 4 5 6 7 8 9 ] 6 3 getinterval aload pop
                [ 7 8 9 1 2 3 4 5 6 ] 0 3 getinterval aload pop
                /x exch def /y exch def /z exch def
                x eq count 1 roll y eq count 1 roll z eq count 1 roll
            """
            test_case = 'test{}'.format(37)
            expr_list = read(testinput37)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))


    def test_input38(self):
            testinput38 = """
                /zero 0 def
                /lt0 {zero lt} def
                [-10 -20 30 -40 50 60 -70 80 -90] { 
                  dup lt0 {-1 mul} if
                } forall
            """
            test_case = 'test{}'.format(38) 
            expr_list = read(testinput38)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input39(self):
            testinput39 = """
                /num 2 def
                /even {num mod} def
                1 1 10 {
                   dup even 0 eq {1 mul } {num mul} ifelse 
                    } for
            """
            test_case = 'test{}'.format(39)
            expr_list = read(testinput39)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input40(self):
            testinput40 = """               
                /x 3 def
                /y 2 def
                /z 1 def
                /condition {x y mul z mul sub 0 eq} def
                [1 y add dup 2 sub 3 4 5] {
                    condition {
                        1 add
                    } {
                        2 mul
                    } ifelse
                } forall

            """
            test_case = 'test{}'.format(40) 
            expr_list = read(testinput40)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input41(self):
            testinput41 = """
                /is_sequence {
                dup length 1 sub 0 exch {
                    1 index exch getinterval              
                    1 index 1 index 1 add getinterval      
                    sub dup 0 lt { -1 mul } if            
                    0 eq {true}{false} ifelse            
                    exch pop                              
                    exch
                } repeat
                pop false  
                } def

                [1 3 22 35 45 226 453 786 999 10101] is_sequence

            """
            test_case = 'test{}'.format(41) 
            expr_list = read(testinput41)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

    def test_input42(self):
            testinput42 = """
            /factorial {
            /n exch def
            
            /result 1 def         
            n -1 1 {
                result mul /result exch def               
                1 sub
            } for
            pop result
            } def

            7 factorial
            """
            test_case = 'test{}'.format(42) 
            expr_list = read(testinput42)
            for expr in expr_list:
                expr.evaluate(self.psstacks)
            self.assertEqual(len(self.psstacks.opstack),len(self.opstack_output[test_case]))
            for i in range(0,len(self.opstack_output[test_case])):
                self.assertTrue(self.compareObjectData(self.psstacks.opstack[i], self.opstack_output[test_case][i]))

if __name__ == '__main__':
    unittest.main()


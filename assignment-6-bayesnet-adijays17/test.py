from bayesnet import BayesNet, BayesNode
from student_code import ask
import unittest

class BayesTest(unittest.TestCase):

    def makeHeadacheNet(self):

        bn = BayesNet()
        bn.add(BayesNode('F',None,{'':0.02}))
        bn.add(BayesNode('C',None,{'':0.1}))
        bn.add(BayesNode('H',['F','C'],{(False,False):0.05,(False,True):0.75,(True,False):0.9,(True,True):0.99}))
        bn.add(BayesNode('B', ['F'], {True:0.9,False:0.001}))
        return bn

    def test1(self):
        bn = self.makeHeadacheNet()
        a = ask('C', True, {'H':True}, bn)
        print('P(C|H)=',a)
        self.assertAlmostEqual( 0.5558992487847989, a)

    def test2(self):
        bn = self.makeHeadacheNet()
        a = ask('C', False, {'H':True}, bn)
        print('P(C*|H)=',a)
        self.assertAlmostEqual( 0.4441007512152011, a)

    def test3(self):
        bn = self.makeHeadacheNet()
        a = ask('C', True, {'H':True, 'B':True}, bn)
        print('P(C|H,B)=',a)
        self.assertAlmostEqual( 0.11259375227554067, a)

    def test4(self):
        bn = self.makeHeadacheNet()
        a = ask('C', False, {'H':True, 'B':True}, bn)
        print('P(C*|H)=',a)
        self.assertAlmostEqual( 0.8874062, a)

if __name__== "__main__":
	unittest.main()

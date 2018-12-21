from bayesnet import BayesNet, BayesNode
from student_code import ask
import unittest

class BayesTest(unittest.TestCase):

    def makeCustomNet(self):

        bn = BayesNet()
        bn.add(BayesNode('C',None,{'':0.1}))
        bn.add(BayesNode('F',None,{'':0.01}))
        bn.add(BayesNode('Z',['C'],{True:0.5,False:0.5}))
        bn.add(BayesNode('V',['F'],{True:0.8,False:0.2}))
        bn.add(BayesNode('S', ['C','F'], {(False,False):0.3,(False,True):0.2,(True,False):0.1,(True,True):0.8}))
        bn.add(BayesNode('N',['S'],{True:0.2,False:0.7}))
        bn.add(BayesNode('W',['S'],{True:0.05,False:0.9}))

        return bn

    def test2(self):
        bn = self.makeCustomNet()
        a = ask('S', True, {'C':True}, bn)
        print('P(S|C)=',a)

    # def test3(self):
    #     bn = self.makeCustomNet()
    #     a = ask('V', True, {'C':True}, bn)
    #     print('P(V|C)=',a)

    # def test4(self):
    #     bn = self.makeCustomNet()
    #     a = ask('N', True, {'C':True}, bn)
    #     print('P(N|C)=',a)

if __name__== "__main__":
	unittest.main()

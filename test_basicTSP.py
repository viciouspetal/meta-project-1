from unittest import TestCase
from TSP_toStudents import *

class TestBasicTSP(TestCase):
    def test_uniformCrossover(self):
        testIndA = [5,1,4,6,7,8,2,3]
        testIndB = [6,7,5,2,8,3,4,1]

        self.uniformCrossover(testIndA, testIndB)
        self.fail()



if __name__ == '__main__':
    subject = TestBasicTSP()
    subject.test_uniformCrossover()
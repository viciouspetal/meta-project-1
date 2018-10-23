import time
from TSP_toStudents import *

def main():
    maxMenu = 6
    iterationNumber = 1
    maxIterations = 4

    for i in range(1, maxMenu + 1):
        for j in range(1, maxIterations+1):
            BasicTSP.menuChoice = i
            data_input_file = sys.argv[1]

            print('==================================  {0}.{1}  ================================='.format(i, j))
            print('{0} iterations, population {1}, mutation rate {2}'.format(300, 100, 0.3))

            start_time = time.time()
            ga = BasicTSP(sys.argv[1], 100, 0.3, 300)
            ga.search()
            print("Process took %s seconds" % int(time.time() - start_time))

    print('######################################################################################################')
    for i in range(1, maxMenu + 1):
        for j in range(1, maxIterations+1):
            BasicTSP.menuChoice = i
            data_input_file = sys.argv[1]

            print('==================================  {0}.{1}  ================================='.format(i, j))
            print('{0} iterations, population {1}, mutation rate {2}'.format(300, 100, 0.5))

            start_time = time.time()
            ga = BasicTSP(sys.argv[1], 100, 0.5, 300)
            ga.search()
            print("Process took %s seconds" % int(time.time() - start_time))
    print('######################################################################################################')

    for i in range(1, maxMenu + 1):
        for j in range(1, maxIterations+1):
            BasicTSP.menuChoice = i
            data_input_file = sys.argv[1]

            print('==================================  {0}.{1}  ================================='.format(i, j))
            print('{0} iterations, population {1}, mutation rate {2}'.format(300, 100, 0.7))

            start_time = time.time()
            ga = BasicTSP(sys.argv[1], 100, 0.7, 300)
            ga.search()
            print("Process took %s seconds" % int(time.time() - start_time))
    print('######################################################################################################')

    for i in range(1, maxMenu + 1):
        for j in range(1, maxIterations+1):
            BasicTSP.menuChoice = i
            data_input_file = sys.argv[1]

            print('==================================  {0}.{1}  ================================='.format(i, j))
            print('{0} iterations, population {1}, mutation rate {2}'.format(300, 150, 0.1))

            start_time = time.time()
            ga = BasicTSP(sys.argv[1], 150, 0.1, 300)
            ga.search()
            print("Process took %s seconds" % int(time.time() - start_time))
    print('######################################################################################################')

    for i in range(1, maxMenu + 1):
        for j in range(1, maxIterations+1):
            BasicTSP.menuChoice = i
            data_input_file = sys.argv[1]

            print('==================================  {0}.{1}  ================================='.format(i, j))
            print('{0} iterations, population {1}, mutation rate {2}'.format(300, 150, 0.3))

            start_time = time.time()
            ga = BasicTSP(sys.argv[1], 150, 0.3, 300)
            ga.search()
            print("Process took %s seconds" % int(time.time() - start_time))
    print('######################################################################################################')

    for i in range(1, maxMenu + 1):
        for j in range(1, maxIterations+1):
            BasicTSP.menuChoice = i
            data_input_file = sys.argv[1]

            print('==================================  {0}.{1}  ================================='.format(i, j))
            print('{0} iterations, population {1}, mutation rate {2}'.format(300, 150, 0.5))

            start_time = time.time()
            ga = BasicTSP(sys.argv[1], 150, 0.5, 300)
            ga.search()
            print("Process took %s seconds" % int(time.time() - start_time))
    print('######################################################################################################')

    for i in range(1, maxMenu + 1):
        for j in range(1, maxIterations+1):
            BasicTSP.menuChoice = i
            data_input_file = sys.argv[1]

            print('==================================  {0}.{1}  ================================='.format(i, j))
            print('{0} iterations, population {1}, mutation rate {2}'.format(300, 150, 0.7))

            start_time = time.time()
            ga = BasicTSP(sys.argv[1], 150, 0.7, 300)
            ga.search()
            print("Process took %s seconds" % int(time.time() - start_time))
    print('######################################################################################################')

    for i in range(1, maxMenu + 1):
        for j in range(1, maxIterations+1):
            BasicTSP.menuChoice = i
            data_input_file = sys.argv[1]

            print('==================================  {0}.{1}  ================================='.format(i, j))
            print('{0} iterations, population {1}, mutation rate {2}'.format(300, 50, 0.3))

            start_time = time.time()
            ga = BasicTSP(sys.argv[1], 100, 0.3, 300)
            ga.search()
            print("Process took %s seconds" % int(time.time() - start_time))

    print('######################################################################################################')
    for i in range(1, maxMenu + 1):
        for j in range(1, maxIterations+1):
            BasicTSP.menuChoice = i
            data_input_file = sys.argv[1]

            print('==================================  {0}.{1}  ================================='.format(i, j))
            print('{0} iterations, population {1}, mutation rate {2}'.format(300, 50, 0.5))

            start_time = time.time()
            ga = BasicTSP(sys.argv[1], 100, 0.5, 300)
            ga.search()
            print("Process took %s seconds" % int(time.time() - start_time))
    print('######################################################################################################')

    for i in range(1, maxMenu + 1):
        for j in range(1, maxIterations+1):
            BasicTSP.menuChoice = i
            data_input_file = sys.argv[1]

            print('==================================  {0}.{1}  ================================='.format(i, j))
            print('{0} iterations, population {1}, mutation rate {2}'.format(300, 50, 0.7))

            start_time = time.time()
            ga = BasicTSP(sys.argv[1], 100, 0.7, 300)
            ga.search()
            print("Process took %s seconds" % int(time.time() - start_time))
    print('######################################################################################################')

if __name__ == '__main__':
    main()
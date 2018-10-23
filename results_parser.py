from reader import Reader
import re

def main():
    reader = Reader('change-to-filename')
    lines = reader.read()

    iterationSeparationPattern = re.compile('==================================  \d.\d  =================================')
    changeOfParamPattern = re.compile('######################################################################################################')
    parametersPattern = re.compile('\d* iterations, population \d*, mutation rate \d.\d')
    bestInitialPattern = re.compile('Best initial sol: \d*.\d*')
    newBestInIteration = re.compile('iteration:  \d* best:')
    sectionTerminatorPattern = re.compile('Process took \d* seconds')
    bestSolutionPattern = re.compile('Best Solution:*\d*')

    section=[]
    currentSectionKey = ''
    configParams = ''
    bestResults = []

    for i in range(0,len(lines)):
        if(iterationSeparationPattern.match(lines[i])):
            currentSectionKey = lines[i].replace('=', '').replace(',', ';').replace('\n', '').replace('\r', '')

        elif bestInitialPattern.match(lines[i]):
            line = lines[i].replace('Best initial sol:', '').replace(' ', '').replace('\n', '').replace('\r', '')
            num=float(line)
            bestResults.append(num)
        elif newBestInIteration.match(lines[i]):
            line = lines[i].replace('iteration:', '').replace(' ', ''). replace('best:', '').replace('\r', '').replace('\n', '')
            num=float(line)
            section.append(num)
        elif bestSolutionPattern.match(lines[i]):
            line = lines[i].replace('Best Solution:', '').replace(' ', '').replace('\r', '').replace('\n', '')
            num=float(line)

            bestResults.append(num)
        elif sectionTerminatorPattern.match(lines[i]):
            line = lines[i].replace('Process took', '').replace('seconds', '').replace(' ', '').replace('\r', '').replace('\n', '')
            timeNum = float(line)
            process_best_results(currentSectionKey, bestResults, configParams, timeNum)
            #processSection(currentSectionKey, bestResults, configParams)
            section = []
            bestResults= []
        elif parametersPattern.match(lines[i]):
            configParams = lines[i].replace('\n', '').replace('\r', '')


def process_best_results(sectionKey, section, configParams, timeNum):
    initialResult = max(section)
    bestResult = min(section)
    print('{0}, {1}'. format(sectionKey, configParams))
    print('Initial Best,{0}, Exec Time,{1}'.format(initialResult, timeNum))
    print('Best result,{0}'.format(bestResult))
    print('Improvement(%),{0}'.format(((initialResult-bestResult)/initialResult)*100))

def processSection(sectionKey, section, configParams):
    sumOfSection = sum(map(float,section))
    countOfSection = len(section)
    print('{0}, {1},'. format(sectionKey, configParams))
    print('Count of section is, {0},'.format(countOfSection))
    print('sum of section, {0},'.format(sumOfSection))
    print('Average Result is, {0},'.format(sumOfSection/countOfSection))


if __name__ == "__main__":
    main()
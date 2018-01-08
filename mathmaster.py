import time
import json
import sys
import copy
import math
import multiprocessing

results = {"Exact":[], "Close":[]}
numWorkers = 6
numParens = 4

def main():
    start_time = time.time()
    count = pCount = 0
    pa_init = parens()
    pa = []
    for i in range(len(pa_init)):
        if len(pa_init[i]) > 2:
            pa.append(pa_init[i])

    print "Number of Paren Combinations %d" % len(pa)
    print "Highest Number of Paren Pairs %d" % numParens
    print "Number of workers %d" % numWorkers

    while pCount < len(pa):
        jobs = []
        for i in range(numWorkers):
            if (i + pCount) < len(pa):
                p = multiprocessing.Process(target=processUnit, args=(pa[pCount + i], pCount + i))
                jobs.append(p)
                p.start()

        for job in jobs:
            job.join()

        print("Batch finished in %s seconds ---" % (time.time() - start_time))
        start_time = time.time()
        pCount = pCount + numWorkers

    print("\nWriting to file.")
    with open('math.json', 'w') as outfile:
        json.dump(results, outfile, indent=4)

def processUnit(parenFormat, pCount):
    diff = 99999999999
    found = False
    count = 0
    closest = 0
    print "Starting Worker %d" % pCount

    while count < 1679616:
        arr = [int(d) for d in str("%08d" % (convert_base(count, 6),))]
        spaces = []

        if parenSpeedup(parenFormat, arr):
            count = count + 1
            continue

        for i in arr:
            spaces.append(switch_operator(i))

        s = copy.deepcopy(spaces)
        result = evaluate(s, parenFormat)

        if result == 10958:
            print "\n--------Success!!-----------"
            i = 0
            numbers = [1,2,3,4,5,6,7,8,9]
            equation = [None]*17

            while i < 17:
                if i%2 == 0:
                    equation[i] = numbers.pop(0)
                if i%2 == 1:
                    equation[i] = spaces.pop(0)
                i = i+1

            found = True
            closest = copy.deepcopy(result)
            diff = 0

            print(equation)
            print(parenFormat)
            print count

            results["Exact"].append({'result':result,'equation': equation, 'parens': parenFormat, 'count': count})

        elif (not result % 1 == 0) and math.floor(result) == 10958 or math.ceil(result) == 10958:
            i = 0
            numbers = [1,2,3,4,5,6,7,8,9]
            equation = [None]*17
            t = copy.deepcopy(spaces)

            while i < 17:
                if i%2 == 0:
                    equation[i] = numbers.pop(0)
                if i%2 == 1:
                    equation[i] = t.pop(0)
                i = i+1
            # print(equation)
            # print(parenFormat)
            # print result
            results['Close'].append({'result':result,'equation': equation, 'parens': parenFormat, 'count': count})

        if abs(result - 10958) < diff and not found:
            closest = copy.deepcopy(result)
            diff = abs(closest - 10958)
            i = 0
            numbers = [1,2,3,4,5,6,7,8,9]
            closest_equation = [None]*17

            while i < 17:
                if i%2 == 0:
                    closest_equation[i] = numbers.pop(0)
                if i%2 == 1:
                    closest_equation[i] = spaces.pop(0)
                i = i+1

            pc = parenFormat

        count = count+1

    print "----------\nEnding worker %d" % pCount
    print closest_equation
    print pc
    print closest
    print "----------"

def add(n, k):
    try:
        return n+float(k)
    except:
        return -999999999999999999

def sub(n,k):
    try:
        return n-float(k)
    except:
        return -999999999999999999

def multi(n,k):
    try:
        return n*float(k)
    except:
        return -999999999999999999

def divi(n,k):
    try:
        return n/float(k)
    except:
        return -999999999999999999

def powwa(n,k):
    try:
        return pow(n,float(k))
    except:
        return -999999999999999999

def cat(n,k):
    if n%2 == 0 or (n+1)%2 == 0:
        n = int(n)
    if k%2 == 0 or (k+1)%2 == 0:
        k = int(k)
    try:
        return float(str(n) + str(k))
    except:
        return -999999999999999999

def switch_operator(x):
    return {
        0: '+',
        1: '-',
        2: '*',
        3: '/',
        4: '^',
        5: '||',
    }[x]

def convert_base(number, base):
    if number > 0:
        if base < 2:
            return False
        remainders = []
        while number > 0:
            remainders.append(str(number % base))
            number //= base
        remainders.reverse()
        return int(''.join(remainders))
    return 0

def parens():
    count = 0
    parens = {}

    for i in range(9):
        j = 1
        for j in range (9):
            if j - i > 0:
                parens[count] = []
                parens[count].append((i*2,j*2, j*2-i*2))
                count = count+1

    for g in range(2,numParens):
        for k in range(len(parens)):
            i = 0
            for i in range(9):
                j = 1
                for j in range (9):
                    match = False
                    if j - i > 0:
                        temp = [(i*2,j*2, j*2-i*2)]
                        for e in parens[k]:
                            temp.append(e)

                        temp.sort(paren_cmp);
                        if isLegalParen(temp):
                            for check in parens:
                                if check == temp:
                                    match = True
                                    break
                            if not match:
                                sys.stdout.write('Completed %d\r' % len(parens))
                                sys.stdout.flush()
                                parens[count] = temp
                                parens[count].sort(paren_cmp);
                                count = count+1
    return parens

def isLegalParen(temp):
    count = 0

    if temp[0][0] != 0 and temp[0][1] != 16:
        for e1 in temp:
            for e2 in temp:
                if e1 != e2:
                    if not (not(e1[0] == e2[0] and e1[1] == e2[1]) and ((e1[0] >= e2[0] and e1[1] <= e2[1]) or (e1[0] <= e2[0] and e1[1] >= e2[1]))):
                        return False
                else:
                    count = count + 1
    else:
        return False

    if count > len(temp):
        return False

    return True

def evaluate(operators, p):
    numbers = [1,2,3,4,5,6,7,8,9]
    equation = [None]*17
    parens = copy.deepcopy(p)

    i = 0
    while i < 17:
        if i%2 == 0:
            equation[i] = numbers.pop(0)
        if i%2 == 1:
            equation[i] = operators.pop(0)
        i = i+1

    if len(parens) > 1:
        if parens[0][2] < parens[1][2]:
            equation = partition(equation, parens[0][0], parens[0][1])
            equation = partition(equation, parens[1][0], parens[1][1] - parens[0][2])
        elif parens[0][0] == parens[1][0]:
            if parens[0][1] > parens[1][1]:
                equation = partition(equation, parens[1][0], parens[1][1])
                equation = partition(equation, parens[0][0], parens[0][1] - parens[1][2])
            else:
                equation = partition(equation, parens[0][0], parens[0][1])
                equation = partition(equation, parens[1][0], parens[1][1] - parens[0][2])
        else:
            equation = partition(equation, parens[0][0], parens[0][1])
            equation = partition(equation, parens[1][0]- parens[0][2], parens[1][1] - parens[0][2])
    else:
        equation = partition(equation, parens[0][0], parens[0][1])

    if len(equation) > 1:
        return cemdas(equation)

    return equation[0]

def partition(alist, p1, p2):
    i = 0
    arr = []

    while i < len(alist):
        if i >= p1 and i <= (p2):
            arr.append(alist[i])
        i = i+1
    del alist[p1:p2 + 1]
    alist.insert(p1,cemdas(arr))
    return alist

def cemdas(equation):
    i = 0
    while i < len(equation):
        if equation[i] == '||':
            res = cat(equation[i-1], equation[i+1])
            del equation[i-1]
            del equation[i-1]
            del equation[i-1]

            equation.insert(i-1, res)
            i = 0
        i = i+1
    i = 0
    while i < len(equation):
        if equation[i] == '^':
            res = powwa(equation[i-1], equation[i+1])
            del equation[i-1]
            del equation[i-1]
            del equation[i-1]

            equation.insert(i-1, res)
            i = 0
        i = i+1
    i = 0
    while i < len(equation):
        if equation[i] == '*':
            res = multi(equation[i-1], equation[i+1])
            del equation[i-1]
            del equation[i-1]
            del equation[i-1]

            equation.insert(i-1, res)
            i = 0
        elif equation[i] == '/':
            res = divi(equation[i-1], equation[i+1])
            del equation[i-1]
            del equation[i-1]
            del equation[i-1]

            equation.insert(i-1, res)
            i = 0
        i = i+1
    i = 0
    while i < len(equation):
        if equation[i] == '+':
            res = add(equation[i-1], equation[i+1])
            del equation[i-1]
            del equation[i-1]
            del equation[i-1]

            equation.insert(i-1, res)
            i = 0
        elif equation[i] == '-':
            res = sub(equation[i-1], equation[i+1])
            del equation[i-1]
            del equation[i-1]
            del equation[i-1]

            equation.insert(i-1, res)
            i = 0
        i = i+1
    return equation[0]

def paren_cmp(a,b):
    if a[0] > b[0]:
        return -1
    elif a[0] == b[0]:
        if a[1] > b[1]:
            return -1
        else:
            return 1
    else:
        return 1

def parenSpeedup(parenFormat, arr):
    count = 0
    for i in range(len(parenFormat)):
        if parenFormat[i][0] - 2 > 0 and arr[parenFormat[i][0] - 2] == 5:
            return True
        if len(arr) - 1 > parenFormat[i][1]/2 and arr[parenFormat[i][1]/2] == 5:
            return True;
        if not parenFormat[i][0] - 2 > 0 and len(arr) - 1 > parenFormat[i][1]/2 and arr[parenFormat[i][1]/2] < 2:
            count = count + 1
        elif not len(arr) - 1 > parenFormat[i][1]/2 and parenFormat[i][0] - 2 > 0 and arr[parenFormat[i][0] - 2] < 2:
            count = count + 1
        elif parenFormat[i][0] - 2 > 0 and len(arr) - 1 > parenFormat[i][1]/2 and arr[parenFormat[i][0] - 2] < 2 and arr[parenFormat[i][1]/2] < 2:
            count = count + 1

    if count == len(parenFormat):
        return True

    return False


if __name__ == "__main__":
    main()

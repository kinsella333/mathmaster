import time
import json
import sys
import copy

def main():
    start_time = time.time()
    count = pCount = overallCounter = 0
    p = parens()

    while pCount < 71:
        count = 0
        while count < 1679615:
            arr = [int(d) for d in str("%08d" % (convert_base(count, 6),))]
            spaces = []

            for i in arr:
                spaces.append(switch_operator(i))

            result = evaluate(spaces, p[pCount])
            count = count+1
            overallCounter = overallCounter+1

            if result == 10958:
                print "success"
                print spaces
                print p[pCount]
                pCount = 100
                break;

            sys.stdout.write('%d> Completed: %.2f%%\r' % (pCount, multi(100,divi(overallCounter,(1679616.0*72.0)))))
            sys.stdout.flush()

        pCount = pCount+1


    # print("\nWriting to file.")
    # with open('math.json', 'w') as outfile:
    #     json.dump(p, outfile, indent=4)
    # print("\n")

    print("--- %s seconds ---" % (time.time() - start_time))

def add(n, k):
    try:
        return n+k
    except:
        return -9999999999999

def sub(n,k):
    try:
        return n-k
    except:
        return -9999999999999

def multi(n,k):
    try:
        return n*k
    except:
        return -9999999999999

def divi(n,k):
    try:
        return n/float(k)
    except:
        return -9999999999999

def powwa(n,k):
    try:
        return pow(n,k)
    except:
        return -9999999999999

def cat(n,k):
    try:
        return int(str(n) + str(k))
    except:
        return -9999999999999

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
    j = 1
    count = 0
    parens = {}
    for k in range(2):
        i = 0
        for i in range(9):
            j = 0
            for j in range (10):
                if j - i > 1:
                    parens[count] = []
                    if k == 0:
                        parens[count].append((i,j, j-i))
                        count = count+1
                    elif k == 1 and not(i == parens[count - 36][0][0] and j == parens[count - 36][0][1]) and ((i >= parens[count - 36][0][0] and j <= parens[count - 36][0][1]) or (i <= parens[count - 36][0][0] and j >= parens[count - 36][0][1])):
                        parens[count].append((i,j, j-i))
                        parens[count].append((parens[count - 36][0][0], parens[count - 36][0][1], parens[count - 36][0][1] - parens[count - 36][0][0]))
                        count = count+1
                j = j+1
            i = i+1
        k = k+1
    return parens

def evaluate(operators, parens):
    numbers = [1,2,3,4,5,6,7,8,9]
    equation = [None]*17

    i = 0
    while i < 17:
        if i%2 == 0:
            equation[i] = numbers.pop(0)
        if i%2 == 1:
            equation[i] = operators.pop(0)
        i = i+1

    if len(parens) > 1:
        if parens[0][2] > parens[1][2]:
            equation = partition(equation, parens[1][0], parens[1][1])
            equation = partition(equation, parens[2][0], parens[2][1])
        else:
            equation = partition(equation, parens[2][0], parens[2][1])
            equation = partition(equation, parens[1][0], parens[1][1])
    else:
        equation = partition(equation, parens[0][0], parens[0][1])

    return cemdas(equation)

def partition(alist, p1, p2):
    i = 0
    arr = []
    while i < 17:
        if i >= p1 and i%2 == 1 and i <= p2:
            arr.append(alist[i])
        elif i >= p1 and i%2 == 0 and i <= p2+1:
            arr.append(alist[i])
        i = i+1

    del alist[p1:p2+1]
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
        i = i+1
    i = 0
    while i < len(equation):
        if equation[i] == '/':
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
        i = i+1
    i = 0
    while i < len(equation):
        if equation[i] == '-':
            res = sub(equation[i-1], equation[i+1])
            del equation[i-1]
            del equation[i-1]
            del equation[i-1]

            equation.insert(i-1, res)
            i = 0
        i = i+1
    return equation[0]

if __name__ == "__main__":
    main()

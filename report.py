import json
import string
import copy

with open('math.json') as data_file:
    math = json.load(data_file)

arr = list()
final = list()

for i in range(len(math['Exact'])):
    if(math['Exact'][i]['result'] == 10958):
        temp = copy.deepcopy(math['Exact'][i]['equation'])

        if len(math['Exact'][i]['parens']) > 1:
            if math['Exact'][i]['parens'][0][1] >= math['Exact'][i]['parens'][1][1]:
                temp.insert(math['Exact'][i]['parens'][0][1] + 1, ')')
                temp.insert(math['Exact'][i]['parens'][1][1] + 1, ')')
                if math['Exact'][i]['parens'][0][0] >= math['Exact'][i]['parens'][1][0]:
                    temp.insert(math['Exact'][i]['parens'][0][0], '(')
                    temp.insert(math['Exact'][i]['parens'][1][0], '(')
                else:
                    temp.insert(math['Exact'][i]['parens'][1][0], '(')
                    temp.insert(math['Exact'][i]['parens'][0][0], '(')

            else:
                temp.insert(math['Exact'][i]['parens'][1][1] + 1, ')')
                temp.insert(math['Exact'][i]['parens'][0][1] + 1, ')')
                if math['Exact'][i]['parens'][0][0] >= math['Exact'][i]['parens'][1][0]:
                    temp.insert(math['Exact'][i]['parens'][0][0], '(')
                    temp.insert(math['Exact'][i]['parens'][1][0], '(')
                else:
                    temp.insert(math['Exact'][i]['parens'][1][0], '(')
                    temp.insert(math['Exact'][i]['parens'][0][0], '(')
        else:
            temp.insert(math['Exact'][i]['parens'][0][1] + 1, ')')
            temp.insert(math['Exact'][i]['parens'][0][0], '(')

        arr.append({"raw":math['Exact'][i]['equation'],"paren":temp})

        for g in range(len(arr)):
            if ''.join(str(e) for e in math['Exact'][i]['equation']) == ''.join(str(e) for e in arr[g]['raw']) and not (''.join(str(e) for e in temp) == ''.join(str(e) for e in arr[g]['paren'])):
                break
            elif len(arr) - 1 == g:
                final.append({"raw":math['Exact'][i]['equation'],"final":temp, "parens": math['Exact'][i]["parens"]})
                break

closest = 0
diff = 9999999999
for i in range(len(math['Close'])):
    if abs(math['Close'][i]['result'] - 10958) < diff:
        diff = abs(math['Close'][i]['result'] - 10958)
        closest = math['Close'][i]['result']

for k in range(len(final)):
    print ''.join(str(e) for e in final[k]['final'])

print "\n"
print "Total Matches Cleaned: %d" % len(final)
print "Total Exact Matches(With Duplicates): %d" % len(math['Exact'])
print "Total Close Calls: %d" % len(math['Close'])
print "Closest: %f with a Difference: %f" % (closest,diff)

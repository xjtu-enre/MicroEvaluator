import pyfpgrowth
from evaluator.microevaluator.interaction_complexity.transaction import genTransaction_singleservice

'''
transactions = [[1, 2, 5],
                [2, 4],
                [2, 3],
                [1, 2, 4],
                [1, 3],
                [2, 3],
                [1, 3],
                [1, 2, 3, 5],
                [1, 2, 3]]


transactions =[
[1,2,3],
[1,2,4],
[1,3,4],
[1,2,3,5],
[1,3,5],
[2,4,5],
[1,2,3,4]]


transactions =[
["1-2","2-3"],
["1-2","2-4"],
]
'''


def genProbabilityDSM(rules):
    servicelist = list()
    for pre in rules:
        if pre not in servicelist:
            servicelist.append(pre)
        for post in rules[pre]:
            if post not in servicelist:
                servicelist.append(post)

    DSM = list()
    title = [" "]
    title.extend(servicelist)
    DSM.append(title)

    for service1 in servicelist:
        tmp = [service1]
        for service2 in servicelist:
            if service1 in rules and service2 in rules[service1]:
                tmp.append(rules[service1][service2])
            else:
                tmp.append(" ")
        DSM.append(tmp)

    '''
    print("Probability DSM:")
    for row in DSM:
        print (row)
    '''
    return (DSM)


def calculateCycle(DSM):
    cyclelist = list()
    sum = 0
    if len(DSM) == 0:
        return 0
    for i in range(1, len(DSM)):
        for j in range(i+1, len(DSM[i])):
            if DSM[i][j] != ' ' and DSM[j][i] != ' ':
                sum += 1
                cyclelist.append([DSM[0][i], DSM[0][j]])
    #print(cyclelist)
    return sum, cyclelist


# fenmu is the number of service whose idd is not equal to 0
def calculateDD_A(DSM):
    odd_dict = dict()
    idd_dict = dict()
    servicelist = DSM[0][1:len(DSM[0])]

    for i in range(1, len(DSM)):
        tmp = 0
        for j in range(1, len(DSM[i])):
            if DSM[i][j] != " ":
                tmp += DSM[i][j]
        odd_dict[servicelist[i-1]] = tmp #no average:  sum()/len()

    for j in range(1, len(DSM)):
        tmp = 0
        for i in range(1, len(DSM[j])):
            if DSM[i][j] != " ":
                tmp += DSM[i][j]
        idd_dict[servicelist[j-1]] = tmp #no average:  sum()/len()



    sum = 0
    for i in range(1, len(DSM)):
        for j in range(1, len(DSM[i])):
            if DSM[i][j] != " ":
                sum += DSM[i][j]

    out_number = 0
    for i in range(1, len(DSM)):
        for j in range(1, len(DSM[i])):
            if DSM[i][j] != " ":
                out_number += 1
                break

    in_number = 0
    for j in range(1, len(DSM)):
        for i in range(1, len(DSM[j])):
            if DSM[i][j] != " ":
                in_number += 1
                break
    odd = sum / float(out_number)
    idd = sum / float(in_number)
    return odd, idd, odd_dict, idd_dict


# fenmu is the number of service
def calculateDD_B(DSM, servicenumber):
    sum = 0
    if len(DSM) == 0:
        return 0

    for i in range(1, len(DSM)):
        for j in range(1, len(DSM[i])):
            if DSM[i][j] != " ":
                sum += DSM[i][j]
    odd = sum / float(servicenumber)
    idd = odd
    return odd, idd


def generate_rules(servicefilename, tracefilename, min_support, min_confidence):
    [transactions, service_number, servicelist] = genTransaction_singleservice(servicefilename, tracefilename)
    transaction_len = len(transactions)

    frequentpatterns = pyfpgrowth.find_frequent_patterns(transactions, int(min_support * transaction_len))

    # {(left): ((right), confidence)}
    rules = pyfpgrowth.generate_association_rules(frequentpatterns, min_confidence)
    print(rules)

    new_single_rules = dict()
    for pre in rules: #pre=(left)
        post = rules[pre] #post = ((right), conf)
        print(pre, post)
        if isinstance(pre, tuple) and isinstance(post, tuple) and len(pre) == 1 and len(post[0]) == 1:
            newpre = pre[0]
            newpost = post[0][0]
            cof = post[1]
            if newpre not in new_single_rules:
                new_single_rules[newpre] = dict()
            new_single_rules[newpre][newpost] = cof
    '''
    print("frequent items:")
    for key in frequentpatterns:
        print (key,  frequentpatterns[key])
    '''
    # print("xxxxxxx", rules)
    # print("xxxxxxx", new_single_rules)
    return new_single_rules,service_number, servicelist

'''
api calculate_odd_idd_cycle
'''


def readrules(rulesfile):
    adict = dict()      #[service1][service2]=freq
    aset = set()
    import csv
    with open(rulesfile, 'r', newline='') as fp:
        reader = csv.reader(fp, delimiter=",")
        for each in reader:
            [service1, service2, freq] = each
            if service1 not in adict:
                adict[service1] = dict()
            adict[service1][service2]= float(freq)
            aset.add(service1)
            aset.add(service2)
    service_number = len(aset)
    print(service_number)
    return adict, service_number, aset



def calculate_odd_idd_cycle(rulesfile, servicefilename, tracefilename, min_support, min_confidence):
    if rulesfile == "none":
        [rules,service_number, servicelist] = generate_rules(servicefilename, tracefilename, min_support, min_confidence)
    else:
        [rules,service_number, servicelist] = readrules(rulesfile)
    '''
    print("rules=")
    for key in rules:
        for value in rules[key]:
            print(key, "->", value, "confidence/freq=", rules[key][value])
    print("rules=", rules)
    '''
    DSM = genProbabilityDSM(rules)
    #print(DSM)
    [odd1, idd1, odd_dict, idd_dict] = calculateDD_A(DSM)
    [odd2, idd2] = calculateDD_B(DSM, service_number)
    [cycle, cycle_list] = calculateCycle(DSM)
    #print("odd1, idd1, odd2, idd2, cycle: ", odd1, idd1, odd2, idd2, cycle)
    return "%.4f" % odd1, "%.4f" % idd1, odd2, idd2, cycle, DSM, odd_dict, idd_dict, cycle_list, servicelist

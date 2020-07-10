import pandas as pd
from efficient_apriori import apriori
from datetime import datetime
from Test import get_trans

def time(s1, s2):
    s1,s2 = str(s1), str(s2)
    hour1=int(s1[0:2])
    hour2 = int(s2[0:2])
    min1 = int(s1[3:5])
    min2 = int(s2[3:5])
    second1= int(s1[6:8])
    second2 = int(s2[6:8])
    return (hour2 - hour1) * 3600 + (min2 - min1) * 60 + (second2-second1)

def read_transaction(file):
    data = pd.read_excel(file, sheet_name="test")
    transactions = []
    invoice_item = set()
    # Description
    for i in range(len(data)):
        invoice_item.add(data['Description'][i])
        if (i < len(data) - 1 and data['InvoiceNo'][i] != data['InvoiceNo'][i + 1]):
            transactions.append(list(invoice_item))
            invoice_item = set()
        if (i == len(data) - 1):
            transactions.append(list(invoice_item))
    # print(transactions)
    # print(len(transactions))
    return transactions
print("Reading transactions.........................")
time1 = datetime.now().time()
print("Begin reading trans at: ", time1 )
transactions = read_transaction("E:\\Kì 8\\Kho khai phá dữ liệu\\hai.xlsx")
# transactions=get_trans.get_transaction()
print("Sum trans:", len(transactions))
# print("Trans: ", transactions)
print("Loaded transaction.")
time2 = datetime.now().time()
print("Begin Apriori at: ",time2)
len_rule = 4 # do dai luat
min_support = 0.05
min_confidence = 0.7
itemsets, rules = apriori(transactions, min_support=min_support, min_confidence=min_confidence, max_length=len_rule)
print("Sum rules: ", len(rules))
list_rule =[]

rules_rhs_2 = filter(lambda rule: (len(rule.lhs) + len(rule.rhs)) == 2, rules)
# rules_rhs = filter(lambda rule: len(rule.lhs) == 1 and len(rule.rhs) == 3, rules)
l_2 = list(rules_rhs_2)
sum_rules_2 = len(l_2)
list_rule.append(l_2)

rules_rhs_3 = filter(lambda rule: (len(rule.lhs) + len(rule.rhs)) == 3, rules)
# rules_rhs = filter(lambda rule: len(rule.lhs) == 1 and len(rule.rhs) == 3, rules)
l_3 = list(rules_rhs_3)
sum_rules_3 = len(l_3)
list_rule.append(l_3)

rules_rhs_4 = filter(lambda rule: (len(rule.lhs) + len(rule.rhs)) == len_rule, rules)
# rules_rhs = filter(lambda rule: len(rule.lhs) == 1 and len(rule.rhs) == 3, rules)
l_4 = list(rules_rhs_4)
sum_rules_4 = len(l_4)
list_rule.append(l_4)

# sum_rules = len(sorted(rules_rhs, key=lambda rule: rule.lift))
for i in range(len(list_rule)):
    gen_rule = {'X': [],
              'Y': [],
              'Support': [],
              'Confident': [],
    }
# for rule in sorted(rules_rhs, key=lambda rule: rule.lift):
    for rule in sorted(list_rule[i], key=lambda rule: rule.lhs):
        # print(rule)  # Prints the rule and its confidence, support, lift, ...
        # print(list(rule.lhs))
        # print(list(rule.rhs))
        gen_rule['X'].append(list(rule.lhs))
        gen_rule['Y'].append(list(rule.rhs))
        gen_rule['Support'].append(rule.support)
        gen_rule['Confident'].append(rule.confidence)
    df = pd.DataFrame(gen_rule)
    filename ="E:\Kì 8\Kho khai phá dữ liệu\Rule\Library\\" +"liabrary_" + str(i+2) + "_" + str(min_support) +"_" +str( min_confidence)+  ".xlsx"
    df.to_excel(filename)


print("Số luật 2 tìm được là: ", sum_rules_2)
print("Số luật 3 tìm được là: ", sum_rules_3)
print("Số luật 4 tìm được là: ", sum_rules_4)
print("Thoi gian load dataset: ", time(time1,time2) , "giay")
print("Thoi gian chay thuat toan: ", time(time2,datetime.now().time()), " giay")
print("Sum trans:", len(transactions))
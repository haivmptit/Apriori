import pandas as pd
from datetime import datetime
from Test import apriori
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

def read_transaction(file): # tên file
    data = pd.read_excel(file, sheet_name="test") # Sheet_100k
    transactions = []
    invoice_item = set() # mã hóa đơn
    print(len(data))
    for i in range(len(data)):
        item = data['Description'][i]
        invoice_item.add(item.strip()) # loại bỏ kí tự cách ở đầu và cuối tên mặt hàng
        if (i < len(data) - 1 and data['InvoiceNo'][i] != data['InvoiceNo'][i + 1]):
            transactions.append(list(invoice_item))
            invoice_item = set()
        if (i == len(data) - 1):
            transactions.append(list(invoice_item)) # thêm một transaction và tập transaction
    return transactions
print("Reading transactions.........................")
time1 = datetime.now().time()
print("Begin reading trans at: ", time1 )
transactions = read_transaction("E:\\Kì 8\\Kho khai phá dữ liệu\\hai.xlsx")
# transactions=get_trans.get_transaction()
print("Sum trans:", len(transactions))
# print("Trans: ", transactions)
# f = open('Transactions.txt', 'w')
# f.write(str(transactions))

print("Loaded transaction.")
time2 = datetime.now().time()
print("Begin Apriori at: ",time2 )
min_support = 0.05
min_confidence = 0.7
apri = apriori.Apriori(transactions, min_support = min_support, min_confidence= min_confidence, len_max=4)
frequent_itemsets=apri.create_frequent_itemsets() # sinh frequent itemsets
print("Đã tạo xong frequent_itemsets at: ", datetime.now().time())
# print("Len a: ", len(frequent_itemsets))
for j in range(len(frequent_itemsets)):
    time3 = datetime.now().time()
    apri.list_frequent_itemsets = []
    rules, l_support,l_conf= apri.gen_rules(frequent_itemsets[j]) #sinh các rule
    time4 = datetime.now().time()
    gen_rule = {'X': [],
                'Y': [],
                'Support': [],
                'Confident': [],
    }
    for i in range(len(rules)):
        gen_rule['X'].append(rules[i][0])
        gen_rule['Y'].append(rules[i][1])
        gen_rule['Support'].append(l_support[i])
        gen_rule['Confident'].append(l_conf[i])
        # print("Rule:", rules[i][0], "===>", rules[i][1])
        # print("Support: ", l_support[i])
        # print("Confident: ", l_conf[i])
        # print("###################################################################################")
    df = pd.DataFrame(gen_rule)
    filename = "E:\Kì 8\Kho khai phá dữ liệu\Rule\\" +"self_" + str(j + 2) + "_" + str(min_support) + "_" + str(
        min_confidence) + ".xlsx"
    df.to_excel(filename)
    print("So rule ở level %d : " %(j+2),len(rules))
    print("Thoi gian gen rules %d: " %(j+2), time(time3, time4), "giay")

# print("Số luật tìm được là: ", len(rules))
print("Thoi gian load dataset: ", time(time1,time2) , "giay")

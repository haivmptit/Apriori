from datetime import datetime
import more_itertools


class Apriori:
    def __init__(self, transactions, min_support, min_confidence, len_max):
        self.transactions = transactions # tập các transactions
        self.min_support = min_support # min_support
        self.min_confidence = min_confidence # min_confidence
        self.len_max = len_max # độ dài luật max
        self.tran_number = len(transactions) # số transaction
        self.list_frequent_itemsets = [] # danh sách các frequent itemsets
        self.l_conf = [] # danh sách các confident
        self.temp = [] # danh sách các vế trái của frequent itemset
        self.l_support = [] # danh sách các support

    def time(self, s1, s2):
        s1, s2 = str(s1), str(s2)
        hour1 = int(s1[0:2])
        hour2 = int(s2[0:2])
        min1 = int(s1[3:5])
        min2 = int(s2[3:5])
        second1 = int(s1[6:8])
        second2 = int(s2[6:8])
        return (hour2 - hour1) * 3600 + (min2 - min1) * 60 + (second2 - second1)

    def init_itemsets(self):  # len(itemset)  = 1
        itemsets = set()  # khởi tạo tập itemset rỗng
        for i in self.transactions:
            for item in i:
                itemsets.add(item)
        results = []
        for i in list(itemsets):
            results.append([i])
        return results

    def create_new_candidate(self, itemsets):
        # tạo danh sách các tổ hợp candidate itemset độ dài k+1 từ tập itemsets độ dài k
        len_itemset = len(itemsets[0]) + 1
        # print('len: ', len_itemset)
        items = set()
        for i in itemsets:
            for item in i:
                items.add(item)
        items = list(items)
        m = more_itertools.distinct_combinations(items, len_itemset) # sinh tổ hợp các candidate itemset
        candidate_itemsets = []
        for i in m:
            candidate_itemsets.append(list(i))
        return candidate_itemsets

    # return  caculate_supported itemset
    def frequent_itemset(self, candidate_itemsets):
        frequent_itemsets = []
        for i in candidate_itemsets:  # remove itemset have min_supported < self.support
            if self.support_itemset(i) >= self.min_support:
                frequent_itemsets.append(i)
        return frequent_itemsets

    def create_frequent_itemsets(self):
        if (self.len_max < 1):
            print("Số item trong Frequent set phải lớn hơn 1 :) ")
        else:
            time1 = datetime.now().time()  # thời gian bắt đầu  sinh frequente itemset.
            frequent_itemset = [] # khởi tạo danh sách các frequent_itemsets
            itemset = self.init_itemsets()  # khởi tạo danh sách các item
            frequent_itemsets = self.frequent_itemset(itemset)  # lấy danh sách các frequent itemset độ dài 1
            for i in range(self.len_max - 1):  # xét các tập frequent itemset có độ dài nhỏ hơn hoặc bằng len_max
                new_candidates = self.create_new_candidate(frequent_itemsets)  # tạo mới danh sách các candidate itemsets
                frequent_itemsets = self.frequent_itemset(new_candidates) # lấy danh sách các frequent itemset từ tập candidate itemset
                if (len(frequent_itemsets) == 0):
                    print("Độ dài tối đa của frequente itemset là : %d" % (i + 1))
                    time2 = datetime.now().time()
                    print("Time supported_itemsets len %d: " % (i + 2), self.time(time1, time2))
                    return frequent_itemset
                    break
                else:
                    frequent_itemset.append(frequent_itemsets)
                    time2 = datetime.now().time() # thời gian kết thúc tạo ra một frequente itemset độ dài (i+2)
                    print("Time supported_itemsets len %d: " % (i + 2), self.time(time1, time2))
            return frequent_itemset

    def create_frequent_itemset_max(self):
        itemset = self.init_itemsets()
        frequent_itemsets = self.frequent_itemset(itemset)
        print("Len new_item 1 :", len(itemset))
        print("new_items 1: ", itemset)
        print("Len supported_itemset 1: ", len(frequent_itemsets))
        print("frequent_itemset 1: ", frequent_itemsets)
        i = 0
        while (True):
            new_candidates = self.create_new_candidate(frequent_itemsets)  # tạo mới danh sách các item
            frequent_itemsets = self.frequent_itemset(new_candidates)
            if len(frequent_itemsets) > 0:
                print(
                    "================================================================================================")
                print("Len new_item %d :" % (i + 2), len(new_candidates))
                print("new_items %d : " % (i + 2), new_candidates)
                print("Len supported_itemset %d : " % (i + 2), len(frequent_itemsets))
                print("frequent_itemset %d : " % (i + 2), frequent_itemsets)
                i += 1
            else:
                return i + 1, frequent_itemsets

    def support_itemset(self, itemset):  # tinh support cua itemset
        dem = 0
        for i in self.transactions:
            if all(itemm in i for itemm in itemset):
                dem += 1
        return dem / self.tran_number

    def confident_itemset(self, X, Y): # X là vế trái, Y là vế phải
        XY = []
        XY.extend(X)
        XY.extend(Y)
        #XY là hợp của X và Y
        #kết quả làm tròn đến 3 chữ số thập phân
        return round(float(self.support_itemset(XY) / self.support_itemset(X)), 3)

    def confident_supported_itemset(self, left, right):  # XY la 1 supported_itemset.
        self.rules(left, right)
        if len(left) == 1: # nếu độ dài của vế trái = 1 thì kết thúc
            pass
        else:
            # duyệt các tổ hợp luật được sinh ra khi rút 1 phần tử từ vế trái sang vế phải
            for i in more_itertools.distinct_combinations(left, 1):
                x, y = left.copy(), right.copy()
                y.append(list(i)[0])
                x.remove(list(i)[0])
                if self.confident_itemset(x, y) >= self.min_confidence: #so sánh  độ tin cậy của luật với confidence
                    self.confident_supported_itemset(x, y) # nếu thỏa mãn thì tiếp  tục sinh luật.

    def rules(self, left, right):
        if len(right) > 0:
            for i in self.temp: #Kiểm tra xem luật đã được duyệt hay chưa
                if all(itemm in i for itemm in left) and len(left) == len(i):
                    return
            self.list_frequent_itemsets.append([left, right])
            self.l_conf.append(self.confident_itemset(left, right)) # thêm độ tin cậy và danh sách độ tin cậy
            c = []
            c.extend(left)
            c.extend(right)
            self.l_support.append(self.support_itemset(c)) # thêm độ phổ biến (support) vào danh sách support
            self.temp.append(left)

    def gen_rules(self, frequent_itemsets):
        for itemset in frequent_itemsets: # duyệt lần lượt frequent_itemset
            self.temp = []
            left = itemset.copy() #khởi tạo vế trái gồm các phần tử trong frequent_itemset
            right = []
            self.confident_supported_itemset(left, right)
        return self.list_frequent_itemsets, self.l_support, self.l_conf

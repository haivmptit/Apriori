import pandas as pd
def get_rule(file): # tên file.
    data = pd.read_excel(file, sheet_name="Sheet1") # đọc nội dung file
    X = [] # vế trái
    Y = [] # vế phải
    for i in range(len(data)):
        x,y = data['X'][i], data['Y'][i]
        x,y = x[1:-1], y[1:-1]
        x =[i.strip() for i in x.split(",")]
        y =[i.strip() for i in y.split(",")]
        X.append(x) # thêm các vế trái của từng rule vào X
        Y.append(y) # thêm các vế phải của từng rule vào Y
    return X, Y

file1 = 'E:\Kì 8\Kho khai phá dữ liệu\Rule\\self_3_0.015_0.7.xlsx' # rules tự cài đặt
file2 = 'E:\Kì 8\Kho khai phá dữ liệu\Rule\\Library\\liabrary_3_0.015_0.7.xlsx' #rules sử dụng thư viện.
X1, Y1 = get_rule(file1) # lấy tất cả các luật từ file1
X2, Y2 = get_rule(file2) # lấy tất cả các luật từ file2
if(len(X1) != len(X2)):
    print("Số lượng rule tại 2 file khác nhau. Vui lòng kiểm tra lại :v")
else:
    count_rule, count_same = len(X1), 0 # khởi tạo tổng các rule có trong mỗi file, tổng các rule giống nhau.
    for i in range(count_rule): #duyệt từng dòng trong file.
        demX = 0 # khởi tạo bộ đếm vế trái =0
        demY = 0  #khởi tạo bộ đếm vế phải =0
        for j in X2: #duyệt lần lượt các vế trái X2
            if all(x in j for x in X1[i]):
                if len(j) == len(X1[i]): # nếu tìm được vế trái X1 = X2 tại dòng i
                    demX += 1
                    break
        for j in Y2: #duyệt lần lượt các vế phải Y2
            if all(y in j for y in Y1[i]):
                if len(j) == len(Y1[i]): # nếu tìm được vế phải Y1 = Y2 tại dòng i
                    demY += 1
                    break
        if demX == 1 and demY == 1: # kiểm tra nếu vế trái và phải tại cùng 1 dòng trùng nhau ở 2 file
            count_same +=1 # biến đếm các rule giống nhau sẽ tăng thêm 1.
    print("Tổng số luật kết hợp là: ", len(X1))
    print("Độ chính xác các luật là: ", round(float(count_same/len(X1)) , 3)*100 , "%")
import pandas as pd 

#accountlist = pd.read_excel('../list/test.xlsx')
data = pd.read_excel('/Users/junha_lee/Documents/Junha/Study/Bigbase/ProjectRegistry/final_revision/pattern_normalization/windows7.xlsx')

#Registry에 대한 정보만 저장
process_name = []
operation = []
path = []


for i in range(0, len(data)):
    if 'reg' in data['Operation'].values[i].lower():
        try:
            path.append(str(data['Path'].values[i]))
            process_name.append(data['ProcessName'].values[i].lower())
            operation.append(data['Operation'].values[i].lower())
        except:
            print(data['Path'].values[i])




# op1 - regoperation - op2만 count
def category_count_1(pn,op1,op2):
    
    operation1 = []
    path1 = []
    
    for i in range(0, len(process_name)):
        if str(pn) == str(process_name[i]):
            operation1.append(operation[i])
            path1.append(path[i].lower())
    

    path_set = []
    
    count_1=0
    
    for i in range(1, len(operation1)):
        if operation1[i-1] == op1 and operation1[i] == op2 and path1[i-1]==path1[i]:
            path_set.append(path1[i])
            count_1 += 1
    
    for i in range(1, len(operation1)-1):
        if operation1[i-1] == op1 and operation1[i+1] == op2 and path1[i-1] in path1[i] and path1[i+1]==path1[i-1]:
            path_set.append(path1[i-1])
            count_1 += 1
    
    path_set = set(path_set)
    
    return count_1, len(path_set)




def category_pattern_operation_1(pn,op1,op2):
    
    #주어진 ProcessName에 대한 operation과 path 저장
    operation1 = []
    path1 = []
    
    for i in range(0, len(process_name)):
        if str(pn) == str(process_name[i]):
            operation1.append(operation[i])
            path1.append(path[i].lower())
       
    registry_operation = []
    
    for i in range(1, len(path1)-1):
        if operation1[i-1] == op1 and operation1[i+1] == op2 and path1[i-1] in path1[i] and path1[i+1] == path1[i-1]:
            registry_operation.append(operation1[i])
    
    pattern_operation = list(set(registry_operation))
 
    return pattern_operation






def pattern_count_1(pn,op,op1,op2):
    

    #주어진 ProcessName에 대한 operation과 path 저장
    operation1 = []
    path1 = []
    
    for i in range(0, len(process_name)):
        if pn == str(process_name[i]):
            operation1.append(operation[i])
            path1.append(path[i].lower())
    
     
    #op이 주어지면 앞에는 op1, 뒤에는 op2인 경우를 count
    p_count_1 = 0
    
    path_set = []
    
    
    if len(op) == 0:
        for i in range(1,len(operation1)):
            if operation1[i-1] == op1 and operation1[i] == op2 and path1[i-1]==path1[i]:
                path_set.append(path1[i])
                p_count_1 += 1
    else:   
        for i in range(1, len(path1)-1):
            if op == operation1[i] and operation1[i-1] == op1 and operation1[i+1] == op2 and path1[i-1] in path1[i] and path1[i+1]==path1[i-1]:
                path_set.append(path1[i-1])
                p_count_1 += 1
                
    path_set = set(path_set)
    
    return p_count_1, len(path_set)



def category_count_2(pn):
    
    #주어진 ProcessName에 대한 operation과 path 저장
    operation2 = []
    path2 = []
    
    for i in range(0, len(process_name)):
        if str(pn) == str(process_name[i]):
            operation2.append(operation[i])
            path2.append(path[i].lower())
            
    path_set = []
       
    count_2 = 0
    
    for i in range(1, len(operation2)):
        if operation2[i] == operation2[i-1] and path2[i].lower() == path2[i-1].lower() :
            path_set.append(path2[i-1])
            count_2 += 1
            
    path_set = set(path_set)
    
    return count_2, len(path_set)



def category_pattern_operation_2(pn):
    
    #주어진 ProcessName에 대한 operation과 path 저장
    operation2 = []
    path2 = []
    
    for i in range(0, len(process_name)):
        if str(pn) == str(process_name[i]):
            operation2.append(operation[i])
            path2.append(path[i].lower())
       
    registry_operation = []
    
    for i in range(1, len(operation2)):
        if operation2[i] == operation2[i-1] and path2[i].lower() == path2[i-1].lower() :
            registry_operation.append(operation2[i])
                
    operations = list(set(registry_operation))      
    
    return operations



       
def pattern_count_2(pn,op):
    
    #주어진 ProcessName에 대한 operation과 path 저장
    operation2 = []
    path2 = []
    
    for i in range(0, len(process_name)):
        if str(pn) == str(process_name[i]):
            operation2.append(operation[i])
            path2.append(path[i].lower())
    
    p_count_2 = 0
    
    path_set = []
    
    for i in range(1, len(operation2)):
        if str(op) == operation2[i-1] == operation2[i] and path2[i-1].lower()==path2[i].lower():
            path_set.append(path2[i-1])
            p_count_2 += 1
            
    path_set = set(path_set)
    
    return p_count_2, len(path_set)
            

#input으로 경로가 들어가면 해당 경로에 대해 op1-op2 pair가 몇인지 count
def pair_count(path_in_all_path,operation,path,op1,op2):
     
    #input으로 경로를 받았을 경우, op에 해당 경로에 대해 수행된 모든 op1, op2 만 저장
    op = []
    
    for i in range(0, len(operation)):
        if path[i].lower() == path_in_all_path.lower():
            if operation[i].lower() == op1 or operation[i].lower() == op2:
                op.append(operation[i])
    
    
    op_count = 0
    
    if op[0] == op1:
        
        if op[len(op)-1] == op1:
            del op[len(op)-1]
            
        for i in range(0, len(op)-1):
            if op[i].lower() == op1 and op[i+1].lower() == op2:
                op_count += 1
        
    elif op[0] == op2:
        
        if op[len(op)-1] == op2:
            del op[len(op)-1]    
    
        for i in range(0, len(op)-1):
            if op[i].lower() == op2 and op[i+1].lower() == op1:
                op_count += 1


    return op_count
    
 
 
def category_count_3(pn,op1,op2):
    
    #주어진 ProcessName에 대한 operation과 path 저장
    operation1 = []
    path1 = []
    
    for i in range(0, len(process_name)):
        if str(pn) == str(process_name[i]):
            operation1.append(operation[i])
            path1.append(path[i].lower())
       
 
    #op1 또는 op2가 한번이라도 수행된 모든 경로 저장.
    open_close_path = []
    
    for i in range(0, len(operation1)):
        if operation1[i] == op1 or operation1[i] == op2:
            open_close_path.append(path1[i].lower())
            
    #open_close_path에서 중복제거
    all_path = list(set(open_close_path))
    
    count_result = []
    
    for i in range(0, len(all_path)):
        count_result.append(pair_count(all_path[i],operation1,path1,op1,op2))
        
    count_1=0
    count_1 = sum(count_result)
    
    return count_1
 




    
if __name__ == '__main__':
    
    
#Registry operation 변수 설정
reg_open = 'regopenkey'
reg_close = 'regclosekey'
reg_createk = 'regcreatekey'
reg_deletek = 'regdeletekey'
reg_setv = 'regsetvalue'
reg_deletev = 'regdeletevalue'




pn = list(set(process_name))





for i in range(0, len(pn)):
    print(str(pn[i])+' : category 1 count : ' +str(category_count_1(pn[i],reg_open,reg_close)))
    print(str(pn[i])+' : category 2 count : ' +str(category_count_2(pn[i])))
    print(str(pn[i])+' : category 3 count : ' +str((category_count_3(pn[i],reg_createk,reg_deletek)+category_count_3(pn[i],reg_setv,reg_deletev))))
    print(str(pn[i])+' : category 1 operation : '+str(category_pattern_operation_1(pn[i],reg_open,reg_close)))
    print(str(pn[i])+' : cateogry 2 operation : '+str(category_pattern_operation_2(pn[i])))

   
#category1_pattern = ['','regopenkey','regclosekey','regqueryvalue','regquerykey','regenumvalue','regenumkey','regsetvalue','regdeletekey','regdeletevalue','regsetinfokey','regquerykeysecurity']
#category2_pattern = ['regopenkey','regclosekey','regqueryvalue','regquerykey','regenumkey','regenumvalue','regsetvalue','regquerykeysecurity','regcreatekey']
#
#
#for i in range(0, len(pn)):
#    print(str(pn[i])+' sum : '+str(category_count_1(pn[i], reg_open, reg_close)))
#    for j in range(0, len(category1_pattern)):
#        print(str(pn[i])+' :  open -'+category1_pattern[j]+'- close : '+str(pattern_count_1(pn[i],category1_pattern[j],reg_open,reg_close)))
#
#
#for i in range(0, len(pn)):
#    print(str(pn[i])+' sum : '+str(category_count_2(pn[i])))
#    for j in range(0, len(category2_pattern)):
#        print(str(pn[i])+' :  '+category2_pattern[j]+'  : '+str(pattern_count_2(pn[i],category2_pattern[j])))


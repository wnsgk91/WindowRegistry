import pandas as pd 



def pattern_detector(data):
        
    process_name = []
    operation = []
    path = []

    #엑셀 파일의 데이터를 list에 담기    
    for i in range(0, len(data)):
        if 'reg' in str(data['Operation'].values[i]).lower():
            try:
                path.append(str(data['Path'].values[i]))
                process_name.append(str(data['ProcessName'].values[i].lower()))
                operation.append(str(data['Operation'].values[i].lower()))
            except:
                print(data['Path'].values[i])
        print i
    
    #프로세스들의 set
    pn = list(set(process_name))
    
    result = []

    #프로세스별로 loop
    for j in range(0, len(pn)):

        pn_operation = []
        pn_path = []

        for i in range(0, len(process_name)):
            if pn[j] == process_name[i]:
                pn_operation.append(operation[i])
                pn_path.append(path[i])

        n=0
        while(n < len(pn_operation)):
           
            if pn_operation[n] == 'regopenkey' or pn_operation[n] == 'regcreatekey':
                
               
                op_path = pn_path[n]
               
                value = 0
                
                #regopenkey가 나타났을 경우, 데이터의 마지막까지 해당 경로에 대해 regclosekey가 존재하면 value = 1
                if pn_operation[n] == 'regopenkey':
                    
                    for i in range(n+1, len(pn_operation)):
                        
                        if pn_operation[i] == 'regopenkey' and pn_path[i] == op_path:
                            break
                       
                        elif pn_operation[i] == 'regclosekey' and pn_path[i] == op_path:
                            value = 1
                           
                    if value == 1 :
                        pattern = []
                       
                        #
                        index = n
                        while(pn_operation[index] != 'regclosekey' or pn_path[index] != op_path):
                           
                            if op_path in pn_path[index]:
                                pattern.append(pn_operation[index])
                           
                            index += 1
                               
                        pattern.append('regclosekey')        
                        result.append(pattern)
                        
                elif pn_operation[n] == 'regcreatekey':
                    
                    for i in range(n+1, len(pn_operation)):
                        
                        if pn_operation[i] == 'regcreatekey' and pn_path[i] == op_path:
                            break
                       
                        elif pn_operation[i] == 'regdeletekey' and pn_path[i] == op_path:
                            value = 1
                           
                    if value == 1 :
                        pattern = []
                       
                       
                        index = n
                        while(pn_operation[index] != 'regdeletekey' or pn_path[index] != op_path):
                           
                            if op_path in pn_path[index]:
                                pattern.append(pn_operation[index])
                           
                            index += 1
                               
                        pattern.append('regdeletekey')        
                        result.append(pattern)                   
            print str(j)+'/'+ str(len(pn)) + str(n)       
            n += 1

    return result




       


def pattern_count(result):
    
    patterns = []
    
    for i in range (0, len(result)):
        patterns.append(str(result[i]))
    
    pattern_count = {}
    
    for pattern in patterns:
        if pattern in pattern_count.keys():
            pattern_count[pattern] += 1
        else:
            pattern_count[pattern] = 1
    
    
    final_data = pd.DataFrame.from_dict({'pattern':pattern_count.keys(),'count':pattern_count.values()})
    
    final_data.to_csv('/Users/junha_lee/Documents/Junha/Study/Bigbase/ProjectRegistry/final_revision/pattern_normalization/data/windows7/원본_pattern_result.csv')     

    return pattern_count


    
if __name__ == '__main__':
   
    data = pd.read_csv('/Users/junha_lee/Documents/Junha/Study/Bigbase/ProjectRegistry/final_revision/pattern_normalization/data/windows7/windows7_registry.csv')
    
  
    pattern_count(pattern_detector(data))

    
    
    
import pandas as pd 



def internal_deduplication(data):
    
    process_name = []
    operation = []
    path = []

    
    for i in range(0, len(data)):
        if 'reg' in str(data['Operation'].values[i]).lower():
            try:
                path.append(str(data['Path'].values[i]).lower())
                process_name.append(str(data['ProcessName'].values[i].lower()))
                operation.append(str(data['Operation'].values[i].lower()))
            except:
                print(data['Path'].values[i])
    
    
    pn = list(set(process_name))      
    
    sample = {'ProcessName':[],'Operation':[],'Path':[]}
    
    result = pd.DataFrame.from_dict(sample)
    
    for num in range(0, len(pn)):
        
        new_operation = []
        new_path = []
        
        pn_operation = []
        pn_path = []
        
        for j in range(0, len(process_name)):
            
            if pn[num] == process_name[j]:
                pn_operation.append(operation[j])
                pn_path.append(path[j])
        
        read = []
        for k in range(0, len(pn_operation)):
            new_operation.append('')
            new_path.append('')
            read.append(0)
                    
        i=0
        while(i<len(pn_operation)):
            if pn_operation[i] == 'regopenkey' or pn_operation[i] == 'regcreatekey':
                if read[i] == 0:
                    
                    temp_path = pn_path[i]
                    temp = []
                    n = i
                    val = 0
                    
                    if pn_operation[i] == 'regopenkey':
                        
                        for k in range(n+1, len(pn_operation)):
                            if pn_operation[k] == 'regopenkey' and pn_path[k] == temp_path:
                                break
                            elif pn_operation[k] == 'regclosekey' and pn_path[k] == temp_path:
                                val = 1

                        if val == 1:
                            ns = []
                            while(pn_operation[n] != 'regclosekey' or pn_path[n] != temp_path):
                                
                                if temp_path in pn_path[n]:
                                    temp.append({pn_operation[n]:pn_path[n]})
                                    ns.append(n)
                                n += 1
                            temp.append({pn_operation[n]:pn_path[n]})
                            ns.append(n)                            
                            
                            
                            for k in range(0, len(temp)):
                                
                                if k == 0:
                                    new_operation[ns[k]] = temp[k].keys()[0]
                                    new_path[ns[k]] = temp[k].values()[0]
                                    read[ns[k]] = 1
                                
                                if temp[k].keys()[0] != temp[k-1].keys()[0] or temp[k].values()[0] != temp[k-1].values()[0]:
                                    new_operation[ns[k]] = temp[k].keys()[0]
                                    new_path[ns[k]] = temp[k].values()[0]                                 
                                    read[ns[k]] = 1
                                
                                else:
                                    new_operation[ns[k]] = None
                                    new_path[ns[k]] = None                                 
                                    read[ns[k]] = 1
                        
                        # val == 0 
                        elif read[i] == 0:
                            new_operation[i] = pn_operation[i]
                            new_path[i] = pn_path[i]
                            read[i] = 1  
                            
                    elif pn_operation[i] == 'regcreatekey':
                        
                        for k in range(n+1, len(pn_operation)):
                            if pn_operation[k] == 'regcreatekey' and pn_path[k] == temp_path:
                                break
                            elif pn_operation[k] == 'regdeletekey' and pn_path[k] == temp_path:
                                val = 1

                        if val == 1:
                            ns = []
                            while(pn_operation[n] != 'regdeletekey' or pn_path[n] != temp_path):
                                
                                if temp_path in pn_path[n]:
                                    temp.append({pn_operation[n]:pn_path[n]})
                                    ns.append(n)
                                n += 1
                            temp.append({pn_operation[n]:pn_path[n]})
                            ns.append(n)                            
                            
                            
                            for k in range(0, len(temp)):
                                
                                if k == 0:
                                    new_operation[ns[k]] = temp[k].keys()[0]
                                    new_path[ns[k]] = temp[k].values()[0]
                                    read[ns[k]] = 1
                                
                                if temp[k].keys()[0] != temp[k-1].keys()[0] or temp[k].values()[0] != temp[k-1].values()[0]:
                                    new_operation[ns[k]] = temp[k].keys()[0]
                                    new_path[ns[k]] = temp[k].values()[0]                                 
                                    read[ns[k]] = 1
                                
                                else:
                                    new_operation[ns[k]] = None
                                    new_path[ns[k]] = None                                 
                                    read[ns[k]] = 1
                        
                        # val == 0 
                        elif read[i] == 0:
                            new_operation[i] = pn_operation[i]
                            new_path[i] = pn_path[i]
                            read[i] = 1  
                            
                            
            elif read[i] == 0 :
                new_operation[i] = pn_operation[i]
                new_path[i] = pn_path[i]
                read[i] = 1
            print i
            i += 1
            
        deduplicated_data = {'ProcessName':pn[num], 'Operation':new_operation,'Path':new_path}

        deduplication = pd.DataFrame.from_dict(deduplicated_data)
        result = pd.concat([result,deduplication])
        
    final_process = []
    final_path = []
    final_operation = []
    
    for i in range(0, len(result)):
        if 'reg' in str(result['Operation'].values[i]).lower():
            try:
                final_path.append(str(result['Path'].values[i]).lower())
                final_process.append(str(result['ProcessName'].values[i].lower()))
                final_operation.append(str(result['Operation'].values[i].lower()))
            except:
                print(result['Path'].values[i])
    
    final_data = pd.DataFrame.from_dict({'ProcessName':final_process,'Operation':final_operation,'Path':final_path})
                  
    final_data.to_csv('/Users/junha_lee/Documents/Junha/Study/Bigbase/ProjectRegistry/final_revision/pattern_normalization/data//windows8/global_deduplication.csv',index=False)           
    data = pd.read_csv('/Users/junha_lee/Documents/Junha/Study/Bigbase/ProjectRegistry/final_revision/pattern_normalization/data/windows8/global_deduplication.csv')
    
#    final_data.to_excel('/Users/junha_lee/Documents/Junha/Study/Bigbase/ProjectRegistry/final_revision/pattern_normalization/pattern_result/windows10/outer_global_deduplication.xlsx',index=False)           
#    data = pd.read_excel('/Users/junha_lee/Documents/Junha/Study/Bigbase/ProjectRegistry/final_revision/pattern_normalization/pattern_result/windows10/outer_global_deduplication.xlsx')
            
    sample = {'ProcessName':[],'Operation':[],'Path':[]}
    
    result = pd.DataFrame.from_dict(sample)    
    
    for num in range(0, len(pn)):

        operation = []
        path = []
        
        # load data
        for i in range(0, len(data)):
            if 'reg' in str(data['Operation'].values[i]).lower() and data['ProcessName'][i].lower() == pn[num]:
                path.append(str(data['Path'].values[i]).lower())
                operation.append(str(data['Operation'].values[i].lower()))     
        
        new_operation = []
        new_path = []
        
        i=0
        
        while(i<len(operation)):
    
            if operation[i] == 'regopenkey':
                
                ops = []
                n = i
                
                while(operation[n] != 'regclosekey' or path[n] != path[i]):
                    ops.append({operation[n]:path[n]})
                    index = n
                    if n<len(operation)-1:
                        n += 1
                    else : 
                        new_operation.append(operation[i])
                        new_path.append(path[i])
                        break
                
                if index+1 < len(operation):
                    i = index+1
                    ops.append({operation[i]:path[i]})
        
                    new_ops = []
                    
                    for k in range(0, len(ops)):
                        if ops[k].keys()[0] == 'regsetvalue' or ops[k].keys()[0] == 'regsetinfokey' or ops[k].keys()[0] == 'regdeletevalue' or ops[k] not in new_ops:
                            new_ops.append(ops[k])
                    
                    for k in range(0, len(new_ops)):
                        new_operation.append(new_ops[k].keys()[0])
                        new_path.append(new_ops[k].values()[0])
                
            else :
                new_operation.append(operation[i])
                new_path.append(path[i])
            print i
            i += 1
            
        deduplicated_data = {'ProcessName':pn[num], 'Operation':new_operation,'Path':new_path}

        deduplication = pd.DataFrame.from_dict(deduplicated_data)
        result = pd.concat([result,deduplication])
    
    result.to_csv('/Users/junha_lee/Documents/Junha/Study/Bigbase/ProjectRegistry/final_revision/pattern_normalization/data/windows7/internal_deduplication.csv',index=False)           

    return result




    
if __name__ == '__main__':
    
    data = pd.read_csv('/Users/junha_lee/Documents/Junha/Study/Bigbase/ProjectRegistry/final_revision/pattern_normalization/data/windows7/windows7_registry.csv')


    
    internal_deduplication(data)
















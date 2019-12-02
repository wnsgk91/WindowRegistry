import pandas as pd 



def pattern_detector(data):
        
    process_name = []
    operation = []
    path = []

    
    for i in range(0, len(data)):
        if 'reg' in data['Operation'].values[i].lower():
            try:
                path.append(str(data['Path'][i]).lower())
                process_name.append(str(data['ProcessName'][i].lower()))
                operation.append(str(data['Operation'][i].lower()))
            except:
                print(data['Path'][i])
    
    
    pn = list(set(process_name))
    
    result = []

    for j in range(0, len(pn)):

        pn_operation = []
        pn_path = []

        for i in range(0, len(process_name)):
            if pn[j] == process_name[i]:
                pn_operation.append(operation[i])
                pn_path.append(path[i])

        n=0
        while(n < len(pn_operation)):
           
            if pn_operation[n] == 'regopenkey' or pn_operation == 'regcreatekey':
                
               
                op_path = pn_path[n]
               
                value = 0

                if pn_operation[n] == 'regopenkey':
                    for i in range(n+1, len(pn_operation)):
                        
                        if pn_operation[i] == 'regopenkey' and pn_path[i] == op_path:
                            break
                        
                        elif pn_operation[i] == 'regclosekey' and pn_path[i] == op_path:
                            value = 1
                           
                    if value == 1 :
                        pattern = []
                       
                       
                        index = n
                        while(pn_operation[index] != 'regclosekey' or pn_path[index] != op_path):
                           
                            if op_path in pn_path[index]:
                                pattern.append({pn_operation[index]:pn_path[index]})
                           
                            index += 1
                               
                        pattern.append({'regclosekey':op_path})        
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
                                pattern.append({pn_operation[index]:pn_path[index]})
                           
                            index += 1
                               
                        pattern.append({'regdeletekey':op_path})        
                        result.append(pattern)                    
                                        
            n += 1

    return result







def outer_deduplication(data):
    
    process_name = []
    operation = []
    path = []
    
    sample = {'ProcessName':[],'Operation':[],'Path':[]}
    
    result = pd.DataFrame.from_dict(sample)

    
    for i in range(0, len(data)):
        if 'reg' in str(data['Operation'].values[i]).lower():
            try:
                path.append(str(data['Path'].values[i]).lower())
                process_name.append(str(data['ProcessName'].values[i].lower()))
                operation.append(str(data['Operation'].values[i].lower()))
            except:
                print(data['Path'].values[i])
    
    
    pn = list(set(process_name))
    

    
    for num in range(0, len(pn)):
        
        new_operation = []
        new_path = []
        
        pn_operation = []
        pn_path = []
        
        for j in range(0, len(process_name)):
            
            if pn[num] == process_name[j]:
                pn_operation.append(operation[j])
                pn_path.append(path[j])
            print str(num)+'  ' +str(j)
                
        patterns = []
        
        pn_data = pd.DataFrame.from_dict({'ProcessName':pn[num], 'Operation':pn_operation, 'Path':pn_path})

        patterns = pattern_detector(pn_data)

        check_pattern = []
        
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

                            check = 0
                            
                            for k in range(0, len(patterns)):
                                if list(temp) == patterns[k]:
                                    check += 1
                                    
                            if check > 1 and temp not in check_pattern:
                                for k in range(0, len(temp)-1):
                                    new_operation[ns[k]] = temp[k].keys()[0]
                                    new_path[ns[k]] = temp[k].values()[0]
                                    read[ns[k]] = 1
                                new_operation[ns[len(temp)-1]] = None
                                new_path[ns[len(temp)-1]] = None
                                read[ns[len(temp)-1]] = 1
                                check_pattern.append(temp)
                                patterns.remove(temp)
                                
                            elif check == 1 and temp not in check_pattern:
                                for k in range(0, len(temp)):
                                    new_operation[ns[k]] = temp[k].keys()[0]
                                    new_path[ns[k]] = temp[k].values()[0]
                                    read[ns[k]] = 1
                                patterns.remove(temp)
                            
                            elif check > 1 and temp in check_pattern:
                                for k in range(1, len(temp)-1):
                                    new_operation[ns[k]] = temp[k].keys()[0]
                                    new_path[ns[k]] = temp[k].values()[0]
                                    read[ns[k]] = 1
                                new_operation[ns[len(temp)-1]] = None
                                new_path[ns[len(temp)-1]] = None
                                read[ns[len(temp)-1]] = 1     
                                new_operation[ns[0]] = None
                                new_path[ns[0]] = None
                                read[ns[0]] = 1
                                patterns.remove(temp)
                                
                            elif check == 1 and temp in check_pattern:
                                for k in range(1, len(temp)):
                                    new_operation[ns[k]] = temp[k].keys()[0]
                                    new_path[ns[k]] = temp[k].values()[0]
                                    read[ns[k]] = 1
                                new_operation[ns[0]] = None
                                new_path[ns[0]] = None
                                read[ns[0]] = 1
                                patterns.remove(temp)
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
                            
                            check = 0
                            
                            for k in range(0, len(patterns)):
                                if list(temp) == patterns[k]:
                                    check += 1
                                    
                            if check > 1 and temp not in check_pattern:
                                for k in range(0, len(temp)-1):
                                    new_operation[ns[k]] = temp[k].keys()[0]
                                    new_path[ns[k]] = temp[k].values()[0]
                                    read[ns[k]] = 1
                                new_operation[ns[len(temp)-1]] = None
                                new_path[ns[len(temp)-1]] = None
                                read[ns[len(temp)-1]] = 1
                                check_pattern.append(temp)
                                patterns.remove(temp)
                                
                            elif check == 1 and temp not in check_pattern:
                                for k in range(0, len(temp)):
                                    new_operation[ns[k]] = temp[k].keys()[0]
                                    new_path[ns[k]] = temp[k].values()[0]
                                    read[ns[k]] = 1
                                patterns.remove(temp)
                            
                            elif check > 1 and temp in check_pattern:
                                for k in range(1, len(temp)-1):
                                    new_operation[ns[k]] = temp[k].keys()[0]
                                    new_path[ns[k]] = temp[k].values()[0]
                                    read[ns[k]] = 1
                                new_operation[ns[len(temp)-1]] = None
                                new_path[ns[len(temp)-1]] = None
                                read[ns[len(temp)-1]] = 1     
                                new_operation[ns[0]] = None
                                new_path[ns[0]] = None
                                read[ns[0]] = 1
                                patterns.remove(temp)
                                
                            elif check == 1 and temp in check_pattern:
                                for k in range(1, len(temp)):
                                    new_operation[ns[k]] = temp[k].keys()[0]
                                    new_path[ns[k]] = temp[k].values()[0]
                                    read[ns[k]] = 1
                                new_operation[ns[0]] = None
                                new_path[ns[0]] = None
                                read[ns[0]] = 1
                                patterns.remove(temp)
                    
                        # val == 0 
                        elif read[i] == 0:
                            new_operation[i] = pn_operation[i]
                            new_path[i] = pn_path[i]
                            read[i] = 1  
                            
                        
            elif read[i] == 0 :
                new_operation[i] = pn_operation[i]
                new_path[i] = pn_path[i]
                read[i] = 1
            print str(num)+'/'+str(len(pn))+' '+ str(i)
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
                
#    final_data.to_excel('/Users/junha_lee/Documents/Junha/Study/Bigbase/ProjectRegistry/final_revision/pattern_normalization/pattern_result/windows8/outer_deduplication.xlsx',index=False)           
    final_data.to_csv('/Users/junha_lee/Documents/Junha/Study/Bigbase/ProjectRegistry/final_revision/pattern_normalization/data/windows8/final_deduplication.csv',index=False)           

    return final_data
 

 
if __name__ == '__main__':

    o_data = pd.read_csv('/Users/junha_lee/Documents/Junha/Study/Bigbase/ProjectRegistry/final_revision/pattern_normalization/data/windows7/windows7_registry.csv')
    data = pd.read_csv('/Users/junha_lee/Documents/Junha/Study/Bigbase/ProjectRegistry/final_revision/pattern_normalization/data/windows7/final_deduplication.csv')
#    data = pd.read_excel('/Users/junha_lee/Documents/Junha/Study/Bigbase/ProjectRegistry/final_revision/pattern_normalization/pattern_result/windows10/internal_deduplication.xlsx')
#    data = pd.read_excel('/Users/junha_lee/Documents/Junha/Study/Bigbase/ProjectRegistry/final_revision/pattern_normalization/test.xlsx')
    

    outer_deduplication(data)
    
   
    
process = list(data['ProcessName'])


pn = list(set(process))




for i in range(0, len(pn)):
    count = 0
    for j in range(0, len(process)):
        if pn[i] == process[j]: count += 1
    print count

    
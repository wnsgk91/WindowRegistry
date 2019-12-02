 
    import pandas as pd 
    
    #### 수집한 데이터
    data = pd.read_csv('/Users/junha_lee/Documents/Junha/Study/Bigbase/ProjectRegistry/final_revision/pattern_normalization/data/windows7/windows7.csv')
    
    
    
    #### 5,000,000로 자르기
    
    time = []
    process_name = []
    operation = []
    path = []
    duration = []
    
    for i in range(0, 5000000):
        try:
            time.append(data['Time of Day'][i])
            process_name.append(str(data['Process Name'][i]).lower())
            path.append(str(data['Path'][i]).lower())
            operation.append(str(data['Operation'][i]).lower())
            duration.append(data['Duration'][i])
        except:
            print i
    
    f_data = pd.DataFrame.from_dict({'Time of Day':time, 'ProcessName':process_name, 'Path':path, 'Operation':operation,'Duration':duration})
    f_data.to_csv('/Users/junha_lee/Documents/Junha/Study/Bigbase/ProjectRegistry/final_revision/pattern_normalization/data/windows7/windows7_f.csv')
            
    
    
    #### registry filtering
    
    f_data = pd.read_csv('/Users/junha_lee/Documents/Junha/Study/Bigbase/ProjectRegistry/final_revision/pattern_normalization/data/windows7/windows7_f.csv')

    
    duration = []
    process_name = []
    path = []
    operation = []
    
    for i in range(0, len(f_data)):
        if 'reg' in f_data['Operation'][i].lower():
            path.append(str(f_data['Path'][i]))
            process_name.append(str(f_data['ProcessName'][i]))
            operation.append(str(f_data['Operation'][i]))
            duration.append(f_data['Duration'][i])

                
    r_data = pd.DataFrame.from_dict({'ProcessName':process_name, 'Path':path,'Operation':operation,'Duration':duration})
    r_data.to_csv('/Users/junha_lee/Documents/Junha/Study/Bigbase/ProjectRegistry/final_revision/pattern_normalization/data/windows7/windows7_registry.csv')
    
    


    
    data = pd.read_csv('/Users/junha_lee/Documents/Junha/Study/Bigbase/ProjectRegistry/final_revision/pattern_normalization/data/windows7/windows7_f.csv')
  

    duration = []
    process_name = []
    path = []
    operation = []
    
    for i in range(0, len(data)):
        if 'reg' not in data['Operation'][i].lower():
            path.append(str(data['Path'][i]))
            process_name.append(str(data['ProcessName'][i]))
            operation.append(str(data['Operation'][i]))
            duration.append(data['Duration'][i])

    pn = list(set(process_name))
    ops = list(set(operation))
    
    
    for i in range(0, len(ops)):
        count = 0
        du = 0
        for j in range(0, len(operation)):
            if ops[i] == operation[j]:
                count += 1
                du += duration[j]
        print du
#        print float(count)/float(len(data))
                
        
    
    duration = []
    process_name = []
    path = []
    operation = []
    
    for i in range(0, len(data)):
        path.append(str(data['Path'][i]))
        process_name.append(str(data['ProcessName'][i]))
        operation.append(str(data['Operation'][i]))
        duration.append(data['Duration'][i])

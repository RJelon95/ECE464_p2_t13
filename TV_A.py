def TV_A(N, seed):
    TV_A = []   #store TV to list

        
    for i in range(seed, 255): 
        TV = bin(i)     #convert int to binary string
        TV = TV.replace("0b", "")   #eliminate "0b"
        
        while (len(TV) < N):
            TV = ''.join(('0',TV))   #pad zeros to get length 
        
        TV_A.append(TV)
    
    if seed != 0:
        for i in range(seed):
            TV = bin(i)     #convert int to binary string
            TV = TV.replace("0b", "")   #eliminate "0b"
        
            while (len(TV) < N):
                TV = ''.join(('0',TV))   #pad zeros to get length 
        
            TV_A.append(TV)
    
    #write to txt file
    outputFile  = open("TV_A.txt", "w") 
    outStr = ""

    for i in range(255):
        outStr = TV_A[i][0:N]   #cut off N bits to ensure proper size
        outputFile.write(outStr + "\n")

    outputFile.close()


    return TV_A
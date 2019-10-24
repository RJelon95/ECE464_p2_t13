#returns list of test vectors, in the order (seed, N) U [0, seed]
#given arguments N inputs, Seed starting value of the counter
#outputs test vectors to a .txt file, "TV_A.txt"
def TV_A(N, seed):
    TV_A = []   #store TV to list
    outputFile  = open("TV_A.txt", "w") #write TV to this file
    idx = 0 #list index


    for i in range(seed, pow(2,N)):
        
        TV = bin(i)     #convert int to binary string
        
        if TV.__contains__("0b"):    #get rid of the '0b'
            TV = TV.replace("0b", "")
        
        while (len(TV) < N):
            TV = ''.join(('0',TV))   #append with zeros if necessary


        list.insert(TV_A, idx, TV)
        outputFile.write(TV + "\n")
        idx = idx + 1


    if seed != 0:   #make sure we come back to get all N - seed vectors
        for j in range (seed):
            TV = bin(j)
            if TV.__contains__("0b"):    #get rid of the '0b'
                TV = TV.replace("0b", "")
        
            while (len(TV) < N):
                TV = ''.join(('0',TV))   #append with zeros if necessary


            list.insert(TV_A, idx, TV)
            outputFile.write(str(TV) + "\n")
            idx = idx + 1
    

    outputFile.close()

    return TV_A

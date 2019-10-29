#LFSR is a sequence of N D-FF, with an XOR at the Nth D-FF
#returns: list of 255 test vectors of length N
#N: inputs to circuit
# seed: inital seed for the LFSR 
def TV_D(N, seed):
    state_prev = []
    state = [] #store N states here, temporarily
    TV_D = []   #store final TV sequence here, permanently

    #construct LFSR:

    s0 = bin(seed)
    s0 = s0.replace("0b", "")   #remove "b0"
    
    while (len(s0) < 8):
        s0 = ''.join(('0',s0))   #prepend with zeros to get to 8 bit length

    for i in range (8):
        state_prev.append(s0[i])    #get initial seed value

    state = state_prev.copy()
    TV = ""

    while len(s0) < N:
            s0 = ''.join((s0,s0))
    while len(s0) != N:
        s0=s0[1:]
    TV_D.append(s0)

    #LFSR with XOR between two last D-FF
    for i in range (254):
        for j in range(8):
            if j == 0:
               
                state[j] = state_prev[7]
            if j == 6:
                state[j] = str(int(state_prev[j+1])^int(state_prev[j-1]))
            else:
                state[j] = state_prev[j-1]
            TV+=str(state[j])
        state_prev = state.copy()

        while len(TV) < N:
            TV = ''.join((TV,TV))
        while len(TV) != N:
            TV=TV[1:]
        TV_D.append(TV)
        TV = ""

    #write to txt file
    outputFile  = open("TV_D.txt", "w") 
    outStr = ""
    for i in range(255):
        outStr = TV_D[i]
        outputFile.write(outStr + "\n")

    outputFile.close()
         
    return TV_D
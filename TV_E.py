#LFSR is a sequence of N D-FF, with an XOR at the Nth D-FF

#N: number of inputs to the circuit
#seed: initial seed for LFSR
#batch_low/high: range of test vectors to return

def TV_E(N, seed):
    state_prev = []
    state = [] #store N states here, temporarily
    TV_E = []   #store final TV sequence here, permanently

    #construct LFSR:

    s0 = bin(seed)
    s0 = s0.replace("0b", "")   #remove "b0"

    while (len(s0) < 8):
        s0 = ''.join(('0',s0))   #append with zeros if necessary to get to 8 bits

    #populate initial seed in state machine
    for i in range(8):
        state_prev.append(int(s0[i]))
        state.append(int(s0[i]))
    TV_E.append(s0)



    #perform LFSR for test vectors with multi-seed behavior

    for i in range(2*255):    #do for range 2*255 circuit inputs so we don't run out of space
        stateStr = ""
        for j in range(8):
            if j == 0:
                state[j] = state_prev[7]
            #XOR operation between two last D-FF
            if j == 6:
                state[j] = str(int(state_prev[j-1])^int(state_prev[j+1]))
            else:
                state[j] = state_prev[j-1]

            stateStr += str(state[j])
        state_prev = state.copy()
        TV_E.append(stateStr)



    
    #now, concatentate TV_E with its subsequent results to get the multi-seed behavior:
    TV_E_multiSeed = [] #store here
    idx = 0 #keeping track of which seed to shift over
    seedStr = ""

    for i in range (255):
        TV_E_multiSeed.append(str(TV_E[i]))
        seedStr = str(TV_E_multiSeed[i])
        while len(TV_E_multiSeed[i]) < N:
            seedStr = ''.join((TV_E[i+1],TV_E[i]))
            
        TV_E_multiSeed[i] = seedStr
        seedStr = ""

       
    #chop TV to reach N inputs:
    for i in range(255):
        while len(TV_E_multiSeed[i]) != N:
            TV_E_multiSeed[i] = TV_E_multiSeed[i][1:]
    
    #write to txt file
    outputFile  = open("TV_E.txt", "w") 
    outStr = ""
    for i in range(255):
        outStr = TV_E_multiSeed[i]
        outputFile.write(outStr + "\n")

    outputFile.close()
    return TV_E_multiSeed  
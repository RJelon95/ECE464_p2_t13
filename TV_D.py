#LFSR is a sequence of N D-FF, with an XOR at the Nth D-FF

#returns: list of 2^N test vectors of length N
def TV_D(N, seed):
    state_prev = []
    state = [] #store N states here, temporarily
    TV_D = []   #store final TV sequence here, permanently

    #construct LFSR:

    s0 = bin(seed)
    s0 = s0.replace("0b", "")   #remove "b0"

    while (len(s0) < N):
        s0 = ''.join(('0',s0))   #append with zeros if necessary

    #populate initial seed:1

    for i in range(N):
        state_prev.append(int(s0[i]))
        state.append(int(s0[i]))

    TV_D.append(s0)

    #perform LFSR 2
    for i in range(pow(2,N) - seed):
        TV_D.append("")
        
        for j in range(N):
            if j == 0:
                state[j] = state_prev[N-1]

            #XOR operation between two last D-FF
            if j == N -2:
                state[j] = str(int(state_prev[N-3])^int(state_prev[N-1]))
            else:
                state[j] = state_prev[j-1]
            TV_D[i+1] += str(state[j])
        state_prev = state.copy()

    print("finished!")  #debugging purposes
    return TV_D

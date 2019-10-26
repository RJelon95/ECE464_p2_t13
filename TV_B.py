def TV_B(N, seed):
    outputFile  = open("TV_B.txt", "w") 
    TV_B = []
    s0 = bin(int(seed))

    for i in range(0, 255):
        bits = ''
        for j in range(0, -(-N//8)):
            bits = s0[2:].rjust(8, '0') + bits
        cutoff = abs(len(bits) - N)
        TV_B.insert(i,bits[cutoff:])
        s0 = bin(int(s0,2) + 1)
        outputFile.write(TV_B[i] + '\n')
    outputFile.close()
    return TV_B



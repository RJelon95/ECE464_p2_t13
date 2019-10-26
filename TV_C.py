def TV_C(N, seed):
    outputFile  = open("TV_C.txt", "w") 
    TV_C = []
    x = 0


    for i in range(0, 255):
        bits = ''
        for j in range(0, -(-N//8)):
            s0 = bin(int(seed) + i)
            i = i + 1
            s0 = s0[2:].rjust(8, '0')
            bits = s0 + bits
        cutoff = len(bits) - N
        TV_C.insert(i, bits[cutoff:len(bits)])
        outputFile.write(TV_C[x] + '\n')
        x = x + 1
    outputFile.close()
    return TV_C
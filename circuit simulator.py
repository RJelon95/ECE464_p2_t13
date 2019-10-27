from __future__ import print_function
import os
import copy
import math

inputCount = 0  #global input line counter

# Function List:
# TV_A: Generates TV_A to .txt file, "TV_A.txt"
# TV_B: Generates TV_B to .txt file, "TV_B.txt"
# TV_C: Generates TV_C to .txt file, "TV_C.txt"
# TV_D: Generates TV_D to .txt file, "TV_D.txt"
# TV_E: Generates TV_E to .txt file, "TV_E.txt"

# 1. netRead: read the benchmark file and build circuit dictionary
# 2. gateCalc: function that will work on the logic of each gate and returns the output
# 3. inputRead: function that will update the circuit dictionary made in netRead filling in the inputs wires
# 4. basic_sim: simulator: returns the circuit dictionary with all the lines updated considering the good circuit
# 5. fault_det: fault simulator: returns the circuit dictionary with all the lines updated considering the fault
# 6. main: The main function

# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: Generates TV_A to .txt file, "TV_A.txt"
# returns list of 255 TV_A vectors
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

# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: Generates TV_B to .txt file, "TV_B.txt"
# returns list of 255 TV_B vectors
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

# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: Generates TV_C to .txt file, "TV_C.txt"
# returns list of 255 TV_C vectors
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

# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: Generates TV_D to .txt file, "TV_D.txt"
# returns list of 255 TV_D vectors
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

# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: Generates TV_E to .txt file, "TV_E.txt"
# returns list of 255 TV_E vectors

#LFSR is a sequence of N D-FF, with an XOR at the Nth D-FF

#N: number of inputs to the circuit
#seed: initial seed for LFSR
#batch_low/high: range of test vectors to return

def TV_E(N, seed):
    state_prev = []
    state = [] #store N states here, temporarily
    TV_E = []   #store final TV sequence here, permanently
    seed = int(seed)   #cast input to int
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

# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: Reading in the Circuit gate-level netlist file: this function takes as input the benchmark file and returns as output
#           the circuit dictionary that will be using throughout the code

def netRead(netName):
    global inputCount #reference global counter
    
    # Opening the netlist file:
    netFile = open(netName, "r")

    # temporary variables
    inputs = []  # array of the input wires
    outputs = []  # array of the output wires
    gates = []  # array of the gate list
    inputBits = 0  # the number of inputs needed in this given circuit

    # main variable to hold the circuit netlist, this is a dictionary in Python, where:
    # key = wire name; value = a list of attributes of the wire
    circuit = {}

    # Reading in the netlist file line by line
    for line in netFile:

        # NOT Reading any empty lines
        if (line == "\n"):
            continue

        # Removing spaces and newlines
        line = line.replace(" ", "")
        line = line.replace("\n", "")

        # NOT Reading any comments
        if (line[0] == "#"):
            continue

        # @ Here it should just be in one of these formats:
        # INPUT(x)
        # OUTPUT(y)
        # z=LOGIC(a,b,c,...)

        # Read a INPUT wire and add to circuit:
        if (line[0:5] == "INPUT"):
            # Removing everything but the line variable name
            line = line.replace("INPUT", "")
            line = line.replace("(", "")
            line = line.replace(")", "")
            inputCount += 1 #global input line counter

            # Format the variable name to wire_*VAR_NAME*
            line = "wire_" + line

            # Error detection: line being made already exists
            if line in circuit:
                msg = "NETLIST ERROR: INPUT LINE \"" + line + "\" ALREADY EXISTS PREVIOUSLY IN NETLIST"
                print(msg + "\n")
                return msg

            # Appending to the inputs array and update the inputBits
            inputs.append(line)

            # add this wire as an entry to the circuit dictionary
            circuit[line] = ["INPUT", line, False, 'U']

            inputBits += 1
            continue

        # Read an OUTPUT wire and add to the output array list
        # Note that the same wire should also appear somewhere else as a GATE output
        if line[0:6] == "OUTPUT":
            # Removing everything but the numbers
            line = line.replace("OUTPUT", "")
            line = line.replace("(", "")
            line = line.replace(")", "")

            # Appending to the output array
            outputs.append("wire_" + line)
            continue

        # Read a gate output wire, and add to the circuit dictionary
        lineSpliced = line.split("=")  # splicing the line at the equals sign to get the gate output wire
        gateOut = "wire_" + lineSpliced[0]

        # Error detection: line being made already exists
        if gateOut in circuit:
            msg = "NETLIST ERROR: GATE OUTPUT LINE \"" + gateOut + "\" ALREADY EXISTS PREVIOUSLY IN NETLIST"
            print(msg + "\n")
            return msg

        # Appending the dest name to the gate list
        gates.append(gateOut)

        lineSpliced = lineSpliced[1].split("(")  # splicing the line again at the "("  to get the gate logic
        logic = lineSpliced[0].upper()

        lineSpliced[1] = lineSpliced[1].replace(")", "")
        terms = lineSpliced[1].split(",")  # Splicing the the line again at each comma to the get the gate terminals
        # Turning each term into an integer before putting it into the circuit dictionary
        terms = ["wire_" + x for x in terms]

        # add the gate output wire to the circuit dictionary with the dest as the key
        circuit[gateOut] = [logic, terms, False, 'U']

    # now after each wire is built into the circuit dictionary,
    # add a few more non-wire items: input width, input array, output array, gate list
    # for convenience

    circuit["INPUT_WIDTH"] = ["input width:", inputBits]
    circuit["INPUTS"] = ["Input list", inputs]
    circuit["OUTPUTS"] = ["Output list", outputs]
    circuit["GATES"] = ["Gate list", gates]

    return circuit
# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: calculates the output value for each logic gate. Takes as inputs the name of the gate to analyze and the
#           circuit dictionary updated by the inputRead function (i.e. with inputs values)
def gateCalc(circuit, node):
    # terminal will contain all the input wires of this logic gate (node)
    terminals = list(circuit[node][1])

    # If the node is an Inverter gate output, solve and return the output
    if circuit[node][0] == "NOT":
        if circuit[terminals[0]][3] == '0':
            circuit[node][3] = '1'
        elif circuit[terminals[0]][3] == '1':
            circuit[node][3] = '0'
        elif circuit[terminals[0]][3] == "U":
            circuit[node][3] = "U"
        else:  # Should not be able to come here
            return -1
        return circuit

    # If the node is an Buffer gate output, solve and return the output
    elif circuit[node][0] == "BUFF":
        if circuit[terminals[0]][3] == '0':
            circuit[node][3] = '0'
        elif circuit[terminals[0]][3] == '1':
            circuit[node][3] = '1'
        elif circuit[terminals[0]][3] == "U":
            circuit[node][3] = "U"
        else:  # Should not be able to come here
            return -1
        return circuit

    # If the node is an AND gate output, solve and return the output
    elif circuit[node][0] == "AND":
        # Initialize the output to 1
        circuit[node][3] = '1'
        # Initialize also a flag that detects a U to false
        unknownTerm = False  # This will become True if at least one unknown terminal is found

        # if there is a 0 at any input terminal, AND output is 0. If there is an unknown terminal, mark the flag
        # Otherwise, keep it at 1
        for term in terminals:
            if circuit[term][3] == '0':
                circuit[node][3] = '0'
                break
            if circuit[term][3] == "U":
                unknownTerm = True

        if unknownTerm:
            if circuit[node][3] == '1':
                circuit[node][3] = "U"
        return circuit

    # If the node is a NAND gate output, solve and return the output
    elif circuit[node][0] == "NAND":
        # Initialize the output to 0
        circuit[node][3] = '0'
        # Initialize also a variable that detects a U to false
        unknownTerm = False  # This will become True if at least one unknown terminal is found

        # if there is a 0 terminal, NAND changes the output to 1. If there is an unknown terminal, it
        # changes to "U" Otherwise, keep it at 0
        for term in terminals:
            if circuit[term][3] == '0':
                circuit[node][3] = '1'
                break
            if circuit[term][3] == "U":
                unknownTerm = True
                break

        if unknownTerm:
            if circuit[node][3] == '0':
                circuit[node][3] = "U"
        return circuit

    # If the node is an OR gate output, solve and return the output
    elif circuit[node][0] == "OR":
        # Initialize the output to 0
        circuit[node][3] = '0'
        # Initialize also a variable that detects a U to false
        unknownTerm = False  # This will become True if at least one unknown terminal is found

        # if there is a 1 terminal, OR changes the output to 1. Otherwise, keep it at 0
        for term in terminals:
            if circuit[term][3] == '1':
                circuit[node][3] = '1'
                break
            if circuit[term][3] == "U":
                unknownTerm = True

        if unknownTerm:
            if circuit[node][3] == '0':
                circuit[node][3] = "U"
        return circuit

    # If the node is an NOR gate output, solve and return the output
    if circuit[node][0] == "NOR":
        # Initialize the output to 1
        circuit[node][3] = '1'
        # Initialize also a variable that detects a U to false
        unknownTerm = False  # This will become True if at least one unknown terminal is found

        # if there is a 1 terminal, NOR changes the output to 0. Otherwise, keep it at 1
        for term in terminals:
            if circuit[term][3] == '1':
                circuit[node][3] = '0'
                break
            if circuit[term][3] == "U":
                unknownTerm = True
        if unknownTerm:
            if circuit[node][3] == '1':
                circuit[node][3] = "U"
        return circuit

    # If the node is an XOR gate output, solve and return the output
    if circuit[node][0] == "XOR":
        # Initialize a variable to zero, to count how many 1's in the terms
        count = 0

        # if there are an odd number of 1 terminals, XOR outputs 1. Otherwise, it should output 0
        for term in terminals:
            if circuit[term][3] == '1':
                count += 1  # For each 1 bit, add one count
            if circuit[term][3] == "U":
                circuit[node][3] = "U"
                return circuit

        # check how many 1's we counted
        if count % 2 == 1:  # if odd number of 1s, the output is 1.
            circuit[node][3] = '1'
        else:  # Otherwise, the output is 0
            circuit[node][3] = '0'
        return circuit

    # If the node is an XNOR gate output, solve and return the output
    elif circuit[node][0] == "XNOR":
        # Initialize a variable to zero, to count how many 1's in the terms
        count = 0

        # if there are an odd number of 1 terminals, XNOR outputs 0. Otherwise, it outputs 1
        for term in terminals:
            if circuit[term][3] == '1':
                count += 1  # For each 1 bit, add one count
            if circuit[term][3] == "U":
                circuit[node][3] = "U"
                return circuit

        # check how many 1's we counted
        if count % 2 == 1:  # if odd number of 1s, the output is 0.
            circuit[node][3] = '0'
        else:  # Otherwise, the output is 1
            circuit[node][3] = '1'
        return circuit

    # Error detection... should not be able to get at this point
    return circuit[node][0]
# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: Updating the circuit dictionary with the input lines
def inputRead(circuit, line):
    # Checking if input bits are enough for the circuit
    if len(line) < circuit["INPUT_WIDTH"][1]:
        return -1

    # Getting the proper number of bits:
    line = line[(len(line) - circuit["INPUT_WIDTH"][1]):(len(line))]

    # Adding the inputs to the dictionary
    # Since the for loop will start at the most significant bit, we start at input width N
    i = circuit["INPUT_WIDTH"][1] - 1
    inputs = list(circuit["INPUTS"][1])
    # dictionary item: [(bool) If accessed, (int) the value of each line, (int) layer number, (str) origin of U value]
    for bitVal in line:
        bitVal = bitVal.upper() # in the case user input lower-case u
        circuit[inputs[i]][3] = bitVal # put the bit value as the line value
        circuit[inputs[i]][2] = True  # and make it so that this line is accessed

        # In case the input has an invalid character (i.e. not "0", "1" or "U"), return an error flag
        if bitVal != "0" and bitVal != "1" and bitVal != "U":
            return -2
        i -= 1 # continuing the increments

    return circuit
# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: the circuit simulator: takes the circuit updated with input lines and returns the circuit with all the
#           lines updated, calling the gateCald for each gate
def basic_sim(circuit):
    # QUEUE and DEQUEUE
    # Creating a queue, using a list, containing all of the gates in the circuit
    queue = list(circuit["GATES"][1])

    # iterate until there are no more elements in queue
    while len(queue) != 0:

        # Remove the first element of the queue and assign it to a variable for us to use
        curr = queue[0]
        queue.remove(curr)

        # initialize a flag, used to check if every terminal has been accessed
        term_has_value = True

        # Check if the terminals have been accessed
        for term in circuit[curr][1]:
            if not circuit[term][2]:
                term_has_value = False
                break

        if term_has_value:
            circuit[curr][2] = True
            circuit = gateCalc(circuit, curr)

            # ERROR Detection if LOGIC does not exist
            if isinstance(circuit, str):
                print(circuit)
                return circuit


        else:
            # If the terminals have not been accessed yet, append the current node at the end of the queue
            queue.append(curr)

    return circuit
# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: fault_det takes the fault under exam and the circuit dictionary just updated with the inputs current values
#           it returns the final circuit dictionary, where all the wires are updated considering the fault
def fault_det(circuit,fault):

    # splitting the fault line at each '-' to get all the fault parameters in a list
    faultSpliced = fault.split("-")

    # create a queue containing all the gates in the circuit
    queue = list(circuit["GATES"][1])

    # initialize modified flag to False
    modified = False

    # iterate until there are no more elements in queue
    while len(queue) != 0:

        # create the wire name from the first element of the fault parameters list, in a way that it is comparable
        # with the elements in the circuit dictionary
        node = "wire_" + faultSpliced[0]

        # if we have previously modified the value of a line to simulate the fail, restore it for the new gate analyzed
        if modified:
            circuit[line][3] = save

        # restore the flag value to False
        modified = False

        # save the first gate of queue in a current variable to be used in this iteration and
        # remove that gate from queue
        curr = queue[0]
        queue.remove(curr)

        # save in a list all the inputs of the circuit
        inputs = list(circuit["INPUTS"][1])

        # if the fault is an input, replace its value in circuit with its STUCK-AT value
        if node in inputs:
            circuit[node][3] = fault[-1]

        # if the faulty gate is the same gate analyzed in this iteration: put the value of the faulty
        # line at its STUCK-AT value and
        # - return the circuit if that line is the gate output
        # - compute the gate output calling the gateCalc if that line is one of the gate inputs

        if (curr == node):
            if (faultSpliced[1] == "SA"):      # if the second element of faultSpliced is "SA", then the fault is
                                               # at the gate output (input signals already analyzed)
                circuit[node][3] = fault[-1]
                circuit[node][2] = True
                continue

            if (faultSpliced[1] == "IN"):      # if the second element of faultSpliced is "IN", then the fault is
                                               # at one of the gate inputs

                line = "wire_" + faultSpliced[2]
                save = copy.deepcopy(circuit[line][3])  # save a copy of the value of the line we are going to modify
                circuit[line][3] = fault[-1]
                modified = True           # update the modified flag so that at the next iteration we'll restore
                                          # the modified line


        # initialize a flag, used to check if every terminal has been accessed
        term_has_value = True

        # Check if the terminals have been accessed
        for term in circuit[curr][1]:
            if not circuit[term][2]:
                term_has_value = False
                break

        # if all the input terminals of the gate have been accessed, call the gateCalc to calculate the gate output
        if term_has_value:
            circuit[curr][2] = True
            circuit = gateCalc(circuit, curr)
        # otherwise append again the current node at the end of the queue
        else:
            queue.append(curr)


    return circuit


# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: Main Function
def main():

    # Used for file access
    script_dir = os.path.dirname(__file__)

    # Select circuit benchmark file
    while True:
        print("\n Read circuit benchmark file:")
        userInput = input()
        cktFile = os.path.join(script_dir, userInput)
        if not os.path.isfile(cktFile):
            print("File does not exist. \n")
        else:
            break

    # Select fault list file
    while True:
        print("\n Read fault list file:")
        userInput = input()
        fltFile = os.path.join(script_dir, userInput)
        if not os.path.isfile(fltFile):
            print("File does not exist. \n")
        else:
            break

    # Select test vector file, press Enter to use the test vectors in ETV_set3
    #commented out: user input of test vector files; will be covered 
    '''while True:
        inputName = "AutoInFile"
        print("\n Read test vector input file. Press enter to use ETV_set3 or enter your file name:")
        userInput = input()
        if userInput == "":
            break
        else:
            inputName = os.path.join(script_dir, userInput)
            if not os.path.isfile(inputName):
                print("File does not exist. \n")
            else:
                break
    '''
    
    # Select the output file
    while True:
        print("\n Write output file:")
        userInput = input()
        outputName = os.path.join(script_dir, userInput)
        if userInput == "":
            print("Enter a non empty file name. \n")
        else:
            break

    # Generate the circuit dictionary
    circuit = netRead(cktFile)

    print("Please enter a seed: ")
    seed = input()
    
    print("Please enter a batch size in [1,10]: ")
    batch = input()
    


    TV_A(inputCount, seed)
    TV_B(inputCount, seed)
    TV_C(inputCount, seed)
    TV_D(inputCount, seed)
    TV_E(inputCount, seed)
    
    tvFile = open("TV_E.txt", "r") 
    outFile = open(outputName, "w")

    outFile.write("\n# fault sim result")
    outFile.write("\n# input: " + cktFile)
    outFile.write("\n# input: " + "TV_E.txt")
    outFile.write("\n# input: " + fltFile)

    # temporary empty list of detected and undetected faults
    detect_list = []
    undetect_list = []

    # read each test vector at a time
    for tv in tvFile:

        # Do nothing else if empty lines ...
        if (tv == "\n"):
            continue
        # ... or any comments
        if (tv[0] == "#"):
            continue

        # Removing newlines and spaces
        tv = tv.replace("\n", "")
        tv = tv.replace(" ", "")

        # Since the inputRead takes the inputs in the opposite order, we reverse it before giving it to the inputRead
        tv_rev = tv[::-1]

        #print("\n-----> READING TEST VECTOR " + tv)

        # at each new test vector, reset the circuit
        circuit = inputRead(circuit, tv_rev)

        # save a copy of the circuit with updated inputs and call the good circuit simulator to get the good circuit
        good_circuit=copy.deepcopy(circuit)
        good_circuit = basic_sim(good_circuit)

        # Saving the outputs resulting from the good circuit
        good_out=list(good_circuit[out][3] for out in good_circuit["OUTPUTS"][1])

        #print("\ntv = {0} -> {1} (good)".format(tv, ''.join(good_out)))
        outFile.write("\n\ntv = {0} -> {1} (good)".format(tv, ''.join(good_out)))

        # Check the validity of the test vectors format
        if circuit == -1:
            print("INPUT ERROR: INSUFFICIENT BITS")
            outFile.write(" -> INPUT ERROR: INSUFFICIENT BITS" + "\n")
            print("...move on to next input\n")
            continue
        elif circuit == -2:
            print("INPUT ERROR: INVALID INPUT VALUE/S")
            outFile.write(" -> INPUT ERROR: INVALID INPUT VALUE/S" + "\n")
            print("...move on to next input\n")
            continue

        faultFile = open(fltFile, "r")

        # initialize the fault list
        fault_list = []

        for fault in faultFile:

            # Do nothing else if empty lines, ...
            if (fault == "\n"):
                continue
            # ... or any comments
            if (fault[0] == "#"):
                continue

            # Removing newlines and spaces
            fault = fault.replace("\n", "")
            fault = fault.replace(" ", "")

            # Append each fault in the fault file to the fault list
            fault_list.append(fault)

            # Save a copy of the circuit with updated inputs and call the bad circuit simulator to get the bad circuit
            bad_circuit = copy.deepcopy(circuit)
            bad_circuit = fault_det(bad_circuit,fault)

            # Saving the outputs resulting from the bad circuit
            bad_out=list(bad_circuit[out][3] for out in bad_circuit["OUTPUTS"][1])

            # Compare good and bad outputs: if they are different -> show detection ad append fault to detected list
            if good_out!= bad_out:
                    #print("detect:")
                    #print("{0}: {1} -> {2}".format(fault, tv, ''.join(bad_out)))
                    outFile.write("\ndetected:")
                    outFile.write("\n{0}: {1} -> {2}".format(fault, tv,''.join(bad_out)))
                    if not ( fault  in detect_list ):
                         detect_list.append(fault)

    # Append to the undetected list each fault of the fault list that has not been appended to the detected list
    for term in fault_list:
        if not(term in detect_list):
            undetect_list.append(term)

    num_det=len(detect_list)
    num_undet=len(undetect_list)
    num_tot=len(fault_list)
    
    #commented out print statements
    '''
    print("\nfault list:")
    print(fault_list)
    print("detect list:")
    print(detect_list)
    print("undetect list:")
    print(undetect_list)
    print("\nTOTAL DETECTED FAULTS: {0}".format(num_det))
    print("UNDETECTED FAULTS: {0}".format(num_undet))
    print(undetect_list)
    print("\nfault coverage: {0}/{1} = {2}%".format(num_det,num_tot,num_det/num_tot*100))
    '''

    outFile.write("\n\n\ntotal detected faults: {0}".format(num_det))
    outFile.write("\n\nundetected faults: {0}\n".format(num_undet))
    outFile.write("\n".join(undetect_list))
    outFile.write("\n\nfault coverage: {0}/{1} = {2}%".format(num_det,num_tot,num_det/num_tot*100))


if __name__ == "__main__":
    main()

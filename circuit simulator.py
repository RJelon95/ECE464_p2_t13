from __future__ import print_function

import copy
import os

inputCount = 0  # global input line counter


# Function List:
# TV_E: Generates TV_E to .txt file, "TV_E.txt"
# 1. netRead: read the benchmark file and build circuit dictionary
# 2. gateCalc: function that will work on the logic of each gate and returns the output
# 3. inputRead: function that will update the circuit dictionary made in netRead filling in the inputs wires
# 4. basic_sim: simulator: returns the circuit dictionary with all the lines updated considering the good circuit
# 5. fault_det: fault simulator: returns the circuit dictionary with all the lines updated considering the fault
# 6. main: The main function

# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: Generates TV_E to .txt file, "TV_E.txt"
# returns list of 255 TV_E vectors

# LFSR is a sequence of N D-FF, with an XOR at the Nth D-FF

# N: number of inputs to the circuit
# seed: initial seed for LFSR
# batch_low/high: range of test vectors to return

def TV_E(N, seed):
    state_prev = []
    state = []  # store N states here, temporarily
    TV_E = []  # store final TV sequence here, permanently
    seed = int(seed)  # cast input to int
    # construct LFSR:

    s0 = bin(seed)
    s0 = s0.replace("0b", "")  # remove "b0"

    while (len(s0) < 8):
        s0 = ''.join(('0', s0))  # append with zeros if necessary to get to 8 bits

    # populate initial seed in state machine
    for i in range(8):
        state_prev.append(int(s0[i]))
        state.append(int(s0[i]))
    TV_E.append(s0)

    # perform LFSR for test vectors with multi-seed behavior

    for i in range(2 * 255):  # do for range 2*255 circuit inputs so we don't run out of space
        stateStr = ""
        for j in range(8):
            if j == 0:
                state[j] = state_prev[7]
            # XOR operation between two last D-FF
            if j == 6:
                state[j] = str(int(state_prev[j - 1]) ^ int(state_prev[j + 1]))
            else:
                state[j] = state_prev[j - 1]

            stateStr += str(state[j])
        state_prev = state.copy()
        TV_E.append(stateStr)

    # now, concatentate TV_E with its subsequent results to get the multi-seed behavior:
    TV_E_multiSeed = []  # store here
    idx = 0  # keeping track of which seed to shift over
    seedStr = ""
    joinIdx = 1
    for i in range(255):
        TV_E_multiSeed.append(str(TV_E[i]))
        seedStr = str(TV_E_multiSeed[i])
        while len(TV_E_multiSeed[i]) < N:
            TV_E_multiSeed[i] = TV_E[joinIdx + 1] + TV_E_multiSeed[i]
            joinIdx += 1
        joinIdx = 1

        seedStr = ""

    # chop TV to reach N inputs:
    for i in range(255):
        while len(TV_E_multiSeed[i]) != N:
            TV_E_multiSeed[i] = TV_E_multiSeed[i][1:]

    # write to txt file
    outputFile = open("TV_E.txt", "w")
    outStr = ""
    for i in range(255):
        outStr = TV_E_multiSeed[i]
        outputFile.write(outStr + "\n")

    outputFile.close()

    return TV_E_multiSeed


def TV_C(N, seed):
    outputFile = open("TV_C.txt", "w")
    TV_C = []
    x = 0

    for i in range(0, 255):
        bits = ''
        for j in range(0, -(-N // 8)):
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


# LFSR is a sequence of N D-FF, with an XOR at the Nth D-FF
# returns: list of 255 test vectors of length N
# N: inputs to circuit
# seed: inital seed for the LFSR
def TV_D(N, seed):
    state_prev = []
    state = []  # store N states here, temporarily
    TV_D = []  # store final TV sequence here, permanently

    # construct LFSR:

    s0 = bin(seed)
    s0 = s0.replace("0b", "")  # remove "b0"

    while (len(s0) < 8):
        s0 = ''.join(('0', s0))  # prepend with zeros to get to 8 bit length

    for i in range(8):
        state_prev.append(s0[i])  # get initial seed value

    state = state_prev.copy()
    TV = ""

    while len(s0) < N:
        s0 = ''.join((s0, s0))
    while len(s0) != N:
        s0 = s0[1:]
    TV_D.append(s0)

    # LFSR with XOR between two last D-FF
    for i in range(254):
        for j in range(8):
            if j == 0:
                state[j] = state_prev[7]
            if j == 6:
                state[j] = str(int(state_prev[j + 1]) ^ int(state_prev[j - 1]))
            else:
                state[j] = state_prev[j - 1]
            TV += str(state[j])
        state_prev = state.copy()

        while len(TV) < N:
            TV = ''.join((TV, TV))
        while len(TV) != N:
            TV = TV[1:]
        TV_D.append(TV)
        TV = ""

    # write to txt file
    outputFile = open("TV_D.txt", "w")
    outStr = ""
    for i in range(255):
        outStr = TV_D[i]
        outputFile.write(outStr + "\n")

    outputFile.close()

    return TV_D


def TV_A(N, seed):
    TV_A = []  # store TV to list

    for i in range(seed, 255):
        TV = bin(i)  # convert int to binary string
        TV = TV.replace("0b", "")  # eliminate "0b"

        while (len(TV) < N):
            TV = ''.join(('0', TV))  # pad zeros to get length

        TV_A.append(TV)

    if seed != 0:
        for i in range(seed):
            TV = bin(i)  # convert int to binary string
            TV = TV.replace("0b", "")  # eliminate "0b"

            while (len(TV) < N):
                TV = ''.join(('0', TV))  # pad zeros to get length

            TV_A.append(TV)

    # write to txt file
    outputFile = open("TV_A.txt", "w")
    outStr = ""

    for i in range(255):
        outStr = TV_A[i][0:N]  # cut off N bits to ensure proper size
        outputFile.write(outStr + "\n")

    outputFile.close()

    return TV_A


def TV_B(N, seed):
    outputFile = open("TV_B.txt", "w")
    TV_B = []
    s0 = bin(int(seed))

    for i in range(0, 255):
        bits = ''
        for j in range(0, -(-N // 8)):
            bits = s0[2:].rjust(8, '0') + bits
        cutoff = abs(len(bits) - N)
        TV_B.insert(i, bits[cutoff:])
        s0 = bin(int(s0, 2) + 1)
        outputFile.write(TV_B[i] + '\n')
    outputFile.close()
    return TV_B


# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: Reading in the Circuit gate-level netlist file: this function takes as input the benchmark file and returns as output
#           the circuit dictionary that will be using throughout the code

def netRead(netName):
    global inputCount  # reference global counter

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
            inputCount += 1  # global input line counter

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
        bitVal = bitVal.upper()  # in the case user input lower-case u
        circuit[inputs[i]][3] = bitVal  # put the bit value as the line value
        circuit[inputs[i]][2] = True  # and make it so that this line is accessed

        # In case the input has an invalid character (i.e. not "0", "1" or "U"), return an error flag
        #    if bitVal != "0" and bitVal != "1" and bitVal != "U":
        #        return -2
        i -= 1  # continuing the increments

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
def fault_det(circuit, fault):
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
            if (faultSpliced[1] == "SA"):  # if the second element of faultSpliced is "SA", then the fault is
                # at the gate output (input signals already analyzed)
                circuit[node][3] = fault[-1]
                circuit[node][2] = True
                continue

            if (faultSpliced[1] == "IN"):  # if the second element of faultSpliced is "IN", then the fault is
                # at one of the gate inputs

                line = "wire_" + faultSpliced[2]
                save = copy.deepcopy(circuit[line][3])  # save a copy of the value of the line we are going to modify
                circuit[line][3] = fault[-1]
                modified = True  # update the modified flag so that at the next iteration we'll restore
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

    # Select the output file
    while True:
        userInput = "output.txt"
        outputName = os.path.join(script_dir, userInput)
        if userInput == "":
            print("Enter a non empty file name. \n")
        else:
            break

    # Generate the circuit dictionary
    circuit = netRead(cktFile)

    print("Please enter a seed: ")
    seed = input()
    seed = int(seed)

    print("Please enter a batch size in [1,10]: ")
    batch = input()
    batch = int(batch)

    TV_A_list = TV_A(inputCount, seed)
    TV_B_list = TV_B(inputCount, seed)
    TV_C_list = TV_C(inputCount, seed)
    TV_D_list = TV_D(inputCount, seed)
    TV_E_list = TV_E(inputCount, seed)

    # cut list to batch size needed:
    TV_A_list = TV_A_list[:batch * 25]
    TV_B_list = TV_B_list[:batch * 25]
    TV_C_list = TV_C_list[:batch * 25]
    TV_D_list = TV_D_list[:batch * 25]
    TV_E_list = TV_E_list[:batch * 25]

    testLength = len(TV_A_list) + len(TV_B_list) + len(TV_C_list) + len(TV_D_list) + len(TV_E_list)

    vector_list = [TV_A_list, TV_B_list, TV_C_list, TV_D_list, TV_E_list]
    output_list = ["TV_A.txt", "TV_B.txt", "TV_C.txt", "TV_D.txt", "TV_E.txt"]

    hitRate = []
    detectRate = 0

    j = 0  # index of which TV list we are using
    A_detectionRate = []
    A_detectionRate.append(0)  # append a zero at the beginning, because we need something to add to our first term
    detect = 0  # counter for number of detections for each batch
    inputName = output_list[j]

    faultFile = open(fltFile, "r")

    # initialize the fault list
    fault_list = []

    # read in fault list
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

    # save this number because we will remove elements from the fault list later
    totalFaults = len(fault_list)

    # loop through the fault list and do a simulation for each test vector
    for i in range(len(TV_A_list)):

        tvFile = open(inputName, "r")
        outFile = open(outputName, "w")

        # temporary empty list of detected and undetected faults
        detect_list = []
        undetect_list = []

        # vectors must be reversed in order
        tv_rev = vector_list[j][i][::-1]

        # at each new test vector, reset the circuit
        circuit = inputRead(circuit, tv_rev)

        # save a copy of the circuit with updated inputs and call the good circuit simulator to get the good circuit
        good_circuit = copy.deepcopy(circuit)
        good_circuit = basic_sim(good_circuit)

        # Saving the outputs resulting from the good circuit
        good_out = list(good_circuit[out][3] for out in good_circuit["OUTPUTS"][1])

        # Append to the undetected list each fault of the fault list that has not been appended to the detected list
        for term in fault_list:
            # Save a copy of the circuit with updated inputs and call the bad circuit simulator to get the bad circuit
            # bad_circuit = copy.deepcopy(circuit)
            blank = []

            bad_circuit = dict(blank)
            bad_circuit.update(circuit)

            bad_circuit = fault_det(bad_circuit, fault)

            # Saving the outputs resulting from the bad circuit
            bad_out = list(bad_circuit[out][3] for out in bad_circuit["OUTPUTS"][1])

            # Compare good and bad outputs: if they are different -> show detection and append fault to detected list
            if good_out != bad_out:
                if not (fault in detect_list):
                    detect_list.append(fault)
                    fault_list.remove(
                        term)  # remove the detected fault from the list - we want to save time in our next loop
                    detect += 1  # increment detection counter

            if not (term in detect_list):
                undetect_list.append(term)

        # at this point we have looped through the fault list; save the batch calculations
        detectRate = detect / totalFaults * 100
        detect = 0
        A_detectionRate.append(detectRate + A_detectionRate[-1])

        # reached end of the loop, go back up to finish for all 25 test vectors in this method

    # remove the initial zero we appended
    A_detectionRate.remove(0)
    print("Finished " + inputName + " test vector list, results are as follows: ")
    print('\n'.join(map(str, A_detectionRate)))
    fault_list.clear()
    faultFile.close()

    # write to txt file
    outputFile = open("A_results.txt", "w")
    outStr = ""
    for i in range(25):
        outStr = A_detectionRate[i]
        outputFile.write(str(outStr) + "\n")

    outputFile.close()

    ###########################################################################################
    # calculating for TV_B
    ###########################################################################################
    j += 1  # index of which TV list we are using
    B_detectionRate = []
    B_detectionRate.append(0)  # append a zero at the beginning, because we need something to add to our first term
    detect = 0  # counter for number of detections for each batch
    inputName = output_list[j]

    faultFile = open(fltFile, "r")

    # initialize the fault list
    fault_list = []

    # read in fault list
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

    # save this number because we will remove elements from the fault list later
    totalFaults = len(fault_list)

    # loop through the fault list and do a simulation for each test vector
    for i in range(len(TV_A_list)):

        tvFile = open(inputName, "r")
        outFile = open(outputName, "w")

        # temporary empty list of detected and undetected faults
        detect_list = []
        undetect_list = []

        # vectors must be reversed in order
        tv_rev = vector_list[j][i][::-1]

        # at each new test vector, reset the circuit
        circuit = inputRead(circuit, tv_rev)

        # save a copy of the circuit with updated inputs and call the good circuit simulator to get the good circuit
        good_circuit = copy.deepcopy(circuit)
        good_circuit = basic_sim(good_circuit)

        # Saving the outputs resulting from the good circuit
        good_out = list(good_circuit[out][3] for out in good_circuit["OUTPUTS"][1])

        # Append to the undetected list each fault of the fault list that has not been appended to the detected list
        for term in fault_list:
            # Save a copy of the circuit with updated inputs and call the bad circuit simulator to get the bad circuit
            # bad_circuit = copy.deepcopy(circuit)
            # bad_circuit = fault_det(bad_circuit,fault)

            blank = []

            bad_circuit = dict(blank)
            bad_circuit.update(circuit)

            bad_circuit = fault_det(bad_circuit, fault)

            # Saving the outputs resulting from the bad circuit
            bad_out = list(bad_circuit[out][3] for out in bad_circuit["OUTPUTS"][1])

            # Compare good and bad outputs: if they are different -> show detection and append fault to detected list
            if good_out != bad_out:
                if not (fault in detect_list):
                    detect_list.append(fault)
                    fault_list.remove(
                        term)  # remove the detected fault from the list - we want to save time in our next loop
                    detect += 1  # increment detection counter

            if not (term in detect_list):
                undetect_list.append(term)

        # at this point we have looped through the fault list; save the batch calculations
        detectRate = detect / totalFaults * 100
        detect = 0
        B_detectionRate.append(detectRate + B_detectionRate[-1])

        # reached end of the loop, go back up to finish for all 25 test vectors in this method

    # remove the initial zero we appended
    B_detectionRate.remove(0)
    print("Finished " + inputName + " test vector list, results are as follows: ")
    print('\n'.join(map(str, B_detectionRate)))
    fault_list.clear()
    faultFile.close()

    # write to txt file
    outputFile = open("B_results.txt", "w")
    outStr = ""
    for i in range(25):
        outStr = B_detectionRate[i]
        outputFile.write(str(outStr) + "\n")

    outputFile.close()

    ########################################################################################
    # calculating for TV_C
    ########################################################################################

    j += 1  # index of which TV list we are using
    C_detectionRate = []
    C_detectionRate.append(0)  # append a zero at the beginning, because we need something to add to our first term
    detect = 0  # counter for number of detections for each batch
    inputName = output_list[j]

    faultFile = open(fltFile, "r")

    # initialize the fault list
    fault_list = []

    # read in fault list
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

    # save this number because we will remove elements from the fault list later
    totalFaults = len(fault_list)

    # loop through the fault list and do a simulation for each test vector
    for i in range(len(TV_A_list)):

        tvFile = open(inputName, "r")
        outFile = open(outputName, "w")

        # temporary empty list of detected and undetected faults
        detect_list = []
        undetect_list = []

        # vectors must be reversed in order
        tv_rev = vector_list[j][i][::-1]

        # at each new test vector, reset the circuit
        circuit = inputRead(circuit, tv_rev)

        # save a copy of the circuit with updated inputs and call the good circuit simulator to get the good circuit
        good_circuit = copy.deepcopy(circuit)
        good_circuit = basic_sim(good_circuit)

        # Saving the outputs resulting from the good circuit
        good_out = list(good_circuit[out][3] for out in good_circuit["OUTPUTS"][1])

        # Append to the undetected list each fault of the fault list that has not been appended to the detected list
        for term in fault_list:
            # Save a copy of the circuit with updated inputs and call the bad circuit simulator to get the bad circuit
            # bad_circuit = copy.deepcopy(circuit)
            # bad_circuit = fault_det(bad_circuit,fault)

            blank = []

            bad_circuit = dict(blank)
            bad_circuit.update(circuit)

            bad_circuit = fault_det(bad_circuit, fault)

            # Saving the outputs resulting from the bad circuit
            bad_out = list(bad_circuit[out][3] for out in bad_circuit["OUTPUTS"][1])

            # Compare good and bad outputs: if they are different -> show detection and append fault to detected list
            if good_out != bad_out:
                if not (fault in detect_list):
                    detect_list.append(fault)
                    fault_list.remove(
                        term)  # remove the detected fault from the list - we want to save time in our next loop
                    detect += 1  # increment detection counter

            if not (term in detect_list):
                undetect_list.append(term)

        # at this point we have looped through the fault list; save the batch calculations
        detectRate = detect / totalFaults * 100
        detect = 0
        C_detectionRate.append(detectRate + C_detectionRate[-1])

        # reached end of the loop, go back up to finish for all 25 test vectors in this method

    # remove the initial zero we appended
    C_detectionRate.remove(0)
    print("Finished " + inputName + " test vector list, results are as follows: ")
    print('\n'.join(map(str, C_detectionRate)))
    fault_list.clear()
    faultFile.close()

    # write to txt file
    outputFile = open("C_results.txt", "w")
    outStr = ""
    for i in range(25):
        outStr = C_detectionRate[i]
        outputFile.write(str(outStr) + "\n")

    outputFile.close()

    ######################
    # calculating for TV_D
    ######################

    j += 1  # index of which TV list we are using
    D_detectionRate = []
    D_detectionRate.append(0)  # append a zero at the beginning, because we need something to add to our first term
    detect = 0  # counter for number of detections for each batch
    inputName = output_list[j]

    faultFile = open(fltFile, "r")

    # initialize the fault list
    fault_list = []

    # read in fault list
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

    # save this number because we will remove elements from the fault list later
    totalFaults = len(fault_list)

    # loop through the fault list and do a simulation for each test vector
    for i in range(len(TV_A_list)):

        tvFile = open(inputName, "r")
        outFile = open(outputName, "w")

        # temporary empty list of detected and undetected faults
        detect_list = []
        undetect_list = []

        # vectors must be reversed in order
        tv_rev = vector_list[j][i][::-1]

        # at each new test vector, reset the circuit
        circuit = inputRead(circuit, tv_rev)

        # save a copy of the circuit with updated inputs and call the good circuit simulator to get the good circuit
        good_circuit = copy.deepcopy(circuit)
        good_circuit = basic_sim(good_circuit)

        # Saving the outputs resulting from the good circuit
        good_out = list(good_circuit[out][3] for out in good_circuit["OUTPUTS"][1])

        # Append to the undetected list each fault of the fault list that has not been appended to the detected list
        for term in fault_list:
            # Save a copy of the circuit with updated inputs and call the bad circuit simulator to get the bad circuit
            # bad_circuit = copy.deepcopy(circuit)
            # bad_circuit = fault_det(bad_circuit,fault)
            blank = []

            bad_circuit = dict(blank)
            bad_circuit.update(circuit)

            bad_circuit = fault_det(bad_circuit, fault)

            # Saving the outputs resulting from the bad circuit
            bad_out = list(bad_circuit[out][3] for out in bad_circuit["OUTPUTS"][1])

            # Compare good and bad outputs: if they are different -> show detection and append fault to detected list
            if good_out != bad_out:
                if not (fault in detect_list):
                    detect_list.append(fault)
                    fault_list.remove(
                        term)  # remove the detected fault from the list - we want to save time in our next loop
                    detect += 1  # increment detection counter

            if not (term in detect_list):
                undetect_list.append(term)

        # at this point we have looped through the fault list; save the batch calculations
        detectRate = detect / totalFaults * 100
        detect = 0
        D_detectionRate.append(detectRate + D_detectionRate[-1])

        # reached end of the loop, go back up to finish for all 25 test vectors in this method

    # remove the initial zero we appended
    D_detectionRate.remove(0)
    print("Finished " + inputName + " test vector list, results are as follows: ")
    print('\n'.join(map(str, D_detectionRate)))
    fault_list.clear()
    faultFile.close()

    # write to txt file
    outputFile = open("D_results.txt", "w")
    outStr = ""
    for i in range(25):
        outStr = D_detectionRate[i]
        outputFile.write(str(outStr) + "\n")

    outputFile.close()

    ######################
    # calculating for TV_E
    ######################

    j += 1  # index of which TV list we are using
    E_detectionRate = []
    E_detectionRate.append(0)  # append a zero at the beginning, because we need something to add to our first term
    detect = 0  # counter for number of detections for each batch
    inputName = output_list[j]

    faultFile = open(fltFile, "r")

    # initialize the fault list
    fault_list = []

    # read in fault list
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

    # save this number because we will remove elements from the fault list later
    totalFaults = len(fault_list)

    # loop through the fault list and do a simulation for each test vector
    for i in range(len(TV_A_list)):

        tvFile = open(inputName, "r")
        outFile = open(outputName, "w")

        # temporary empty list of detected and undetected faults
        detect_list = []
        undetect_list = []

        # vectors must be reversed in order
        tv_rev = vector_list[j][i][::-1]

        # at each new test vector, reset the circuit
        circuit = inputRead(circuit, tv_rev)

        # save a copy of the circuit with updated inputs and call the good circuit simulator to get the good circuit
        good_circuit = copy.deepcopy(circuit)
        good_circuit = basic_sim(good_circuit)

        # Saving the outputs resulting from the good circuit
        good_out = list(good_circuit[out][3] for out in good_circuit["OUTPUTS"][1])

        # Append to the undetected list each fault of the fault list that has not been appended to the detected list
        for term in fault_list:
            # Save a copy of the circuit with updated inputs and call the bad circuit simulator to get the bad circuit
            # bad_circuit = copy.deepcopy(circuit)
            # bad_circuit = fault_det(bad_circuit,fault)
            blank = []

            bad_circuit = dict(blank)
            bad_circuit.update(circuit)

            bad_circuit = fault_det(bad_circuit, fault)

            # Saving the outputs resulting from the bad circuit
            bad_out = list(bad_circuit[out][3] for out in bad_circuit["OUTPUTS"][1])

            # Compare good and bad outputs: if they are different -> show detection and append fault to detected list
            if good_out != bad_out:
                if not (fault in detect_list):
                    detect_list.append(fault)
                    fault_list.remove(
                        term)  # remove the detected fault from the list - we want to save time in our next loop
                    detect += 1  # increment detection counter

            if not (term in detect_list):
                undetect_list.append(term)

        # at this point we have looped through the fault list; save the batch calculations
        detectRate = detect / totalFaults * 100
        detect = 0
        E_detectionRate.append(detectRate + E_detectionRate[-1])

        # reached end of the loop, go back up to finish for all 25 test vectors in this method

    # remove the initial zero we appended
    E_detectionRate.remove(0)
    print("Finished " + inputName + " test vector list, results are as follows: ")
    print('\n'.join(map(str, E_detectionRate)))
    fault_list.clear()
    faultFile.close()

    # write to txt file
    outputFile = open("E_results.txt", "w")
    outStr = ""
    for i in range(25):
        outStr = E_detectionRate[i]
        outputFile.write(str(outStr) + "\n")

    outputFile.close()
    filenames = ['A_results.txt', 'B_results.txt', 'C_results.txt', 'D_results.txt', 'E_results.txt', ]
    with open('output.txt', 'w') as writer:
        readers = [open(filename) for filename in filenames]
        for lines in zip(*readers):
            print(', '.join([line.strip() for line in lines]), file=writer)
    import csv
    with open('output.txt', 'r') as in_file:
        stripped = (line.strip() for line in in_file)
        lines = (line.split(",") for line in stripped if line)
        with open('output.csv', 'w', newline='') as out_file:
            writer = csv.writer(out_file)
            writer.writerow(('TV_A', 'TV_B', 'TV_C', 'TV_D', 'TV_E'))
            writer.writerows(lines)

if __name__ == "__main__":
    main()

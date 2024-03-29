from __future__ import print_function
import os
import copy
import math


# Function List:
# 1. netRead: read the benchmark file and build circuit dictionary
# 2. gateCalc: function that will work on the logic of each gate and returns the output
# 3. inputRead: function that will update the circuit dictionary made in netRead filling in the inputs wires
# 4. basic_sim: simulator: returns the circuit dictionary with all the lines updated considering the good circuit
# 5. fault_det: fault simulator: returns the circuit dictionary with all the lines updated considering the fault
# 6. main: The main function



# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: Reading in the Circuit gate-level netlist file: this function takes as input the benchmark file and returns as output
#           the circuit dictionary that will be using throughout the code

def netRead(netName):
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

    print("Welcome to the Fault Coverage of Pseudo-Random TVs software")
    print("1)Test Vector Generation")
    print("2)Fault Coverage Simulation")
    print("3)Avg Fault Coverage data generation")
    print("4)Exit")
    choice = input("Enter your choice [1-4]: ")
    try:
        choice = int(choice)
    except ValueError:
        print("Wrong integer. Please try again.")
    if choice == 1:
        #def tv_opt():
            print("Option 1: ")
            print("1)Test Vector generation.")
            print("2)Main Menu")
            print("3)Exit")

            while 1:
                choice2 = input("Enter your choice [1-3]: ")
                try:
                    choice2 = int(choice2)
                except ValueError:
                    print("Wrong integer. Please try again.")
                if choice2 == 1:
                    #our TVs
                    input("Press Enter to continue...")
                    main()
                elif choice2 == 2:
                    main()
                elif choice2 == 3:
                    exit()
                else:
                    print("Wrong integer. Please try again.")
                    #tv_opt()

    elif choice == 2:
        i = 0
        while i < 1:
            batchNum = input("Choose a batch size in [1, 10]:")
            try:
                batchNum = int(batchNum)
            except ValueError:
                print('Raw input data. Returning to the menu to avoid crash.')
                main()
            i = 1
            if batchNum > 10 or batchNum < 1:
                print("Wrong Number, please try again.")
                i = 0
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
        while True:
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

        # If the user chose to use the test vectors in ETV_set3, generate them in a file
        if inputName == "AutoInFile":

            inputFile = open(inputName, "w")
            n_input=circuit["INPUT_WIDTH"][1]
            i = math.ceil(n_input/2)
            in1="00"*i
            in2="11"*i
            in3="01"*i
            in4="10"*i
            if n_input % 2 == 1:
                 in1=in1[:-1]
                 in2=in2[:-1]
                 in3=in3[:-1]
                 in4=in4[:-1]
            inputFile.write(in1)
            inputFile.write("\n{0}".format(in2))
            inputFile.write("\n{0}".format(in3))
            inputFile.write("\n{0}".format(in4))
            inputFile.close()


        tvFile = open(inputName, "r")
        outFile = open(outputName, "w")

        outFile.write("\n# fault sim result")
        outFile.write("\n# input: " + cktFile)
        outFile.write("\n# input: " + inputName)
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

            print("\n-----> READING TEST VECTOR " + tv)

            # at each new test vector, reset the circuit
            circuit = inputRead(circuit, tv_rev)

            # save a copy of the circuit with updated inputs and call the good circuit simulator to get the good circuit
            good_circuit=copy.deepcopy(circuit)
            good_circuit = basic_sim(good_circuit)

            # Saving the outputs resulting from the good circuit
            good_out=list(good_circuit[out][3] for out in good_circuit["OUTPUTS"][1])

            print("\ntv = {0} -> {1} (good)".format(tv, ''.join(good_out)))
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
                        print("detect:")
                        print("{0}: {1} -> {2}".format(fault, tv, ''.join(bad_out)))
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


        outFile.write("\n\n\ntotal detected faults: {0}".format(num_det))
        outFile.write("\n\nundetected faults: {0}\n".format(num_undet))
        outFile.write("\n".join(undetect_list))
        outFile.write("\n\nfault coverage: {0}/{1} = {2}%".format(num_det,num_tot,num_det/num_tot*100))
        input("Press Enter to continue...")
        main()
    elif choice == 3:
        print("Number 3 selected. No attempt has been done for that part.")
        input("Press Enter to continue...")
        main()
    elif choice == 4:
        print("Good Bye!")
        exit()
    else:
        print("Wrong integer. Please try again.")
        main()

if __name__ == "__main__":
    main()
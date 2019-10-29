filenames = ['A_results.txt', 'B_results.txt','C_results.txt','D_results.txt','E_results.txt',]
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
        writer.writerow(('TV_A', 'TV_B','TV_C','TV_D','TV_E'))
        writer.writerows(lines)
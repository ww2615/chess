import csv

# This file requires moves_index.csv
# filters all moves with time format 600+0
filemax = 93
timeformat = "600+0"
fileindex = 1
wr = open(timeformat +"_"+ str(fileindex) + '.csv', mode = 'a+', newline = '')
writer = csv.writer(wr, delimiter = ',')
header = ["Result", "WhiteElo", "BlackElo", "ECO", "TimeControl", "Termination",
                     "Color", "MoveNum", "Move", "Type", "Eval", "EvalDiff", "Time", "TimeSpent"]
writer.writerow(header)
line = 0
for i in range(1, filemax + 1):
    fname = "moves/moves_" + str(i) + ".csv"
    readf = open(fname, mode = "r")
    reader = csv.reader(readf)
    readerline = 0
    for r in reader:
        readerline += 1
        if(readerline == 1):
            continue
        if(r[4] != timeformat):
            continue
        else:
            writer.writerow(r)
            line += 1
        if(line == 5000000):
            line = 0
            wr.close()
            fileindex += 1
            wr = open(timeformat + "_"+str(fileindex) + '.csv', mode = 'a+', newline = '')
            writer = csv.writer(wr, delimiter = ',')
            writer.writerow(header)
    readf.close()
wr.close()

import csv
from datetime import datetime as dt
from datetime import timedelta

readpgn = open("pgn_1.csv", mode = "r")
moves = open('moves_1.csv', mode = 'a+', newline = '')

csv_reader = csv.reader(readpgn)
csv_writer = csv.writer(moves, delimiter = ',')
fileindex = 1
count = 0
line_count = 0
starttime = dt.now()
FMT = "%H:%M:%S"
header = ["Result", "WhiteElo", "BlackElo", "ECO", "TimeControl", "Termination",
                     "Color", "MoveNum", "Move", "Type", "Eval", "EvalDiff", "Time", "TimeSpent"]
csv_writer.writerow(header)
for r in csv_reader:
    # intended to skip the headers
    if(count == 0):
        count += 1
        continue
    # every line will be 
    # 0         1           2           3          4               5            6
    # result    whiteelo    blackelo    opening    timecontrol     terminatiom  color
    # 7          8       9       10      11          12      13        14  
    # movenum    move    type    eval    evaldiff    time    timediff  thinktime    
    # line = 14
    l = 14
    count += 1
    str_incre = r[8]
    x = str_incre.split("+")
    incre = 0
    if(x[1].isdigit()):
        incre = int(x[1])
    # incre = time added after every move
    pgn = r[10]
    move_list = r[10].split("}")
    move_list = move_list[:-1]
    # the last index = r[0]
    prevline = [""] * l * 2

    for move in move_list:
        line = [""] * l
        
        eval = move.split("{")
        num = eval[0].split(" ")
        ind = 0
        if(len(num) != 3):
            ind += 1
            
        black = "..." in num[ind]
        dot_index = num[ind].index(".")
        move_num = num[ind][:dot_index]
        
        options = ["normal", "blunder", "brilliant", "dubious", 
                   "interesting", "mistake", "good"]
        opt_ind = 0
        opt_key = num[ind + 1]
        if("??" in opt_key):
            opt_ind = 1
        elif("!!" in opt_key):
            opt_ind = 2
        elif("?!" in opt_key):
            opt_ind = 3
        elif("!?" in opt_key):
            opt_ind = 4
        elif("?" in opt_key):
            opt_ind = 5
        elif("!" in opt_key):
            opt_ind = 6
        val = ""
        clk = ""
        if("%eval" in eval[1]):
            ind = eval[1].index("%eval")
            s = eval[1][ind + 6: ind + 14]
            s = s[:s.index("]")]
            val = s
        if("%clk" in eval[1]):
            ind = eval[1].index("%clk")
            s = eval[1][ind + 5:]
            s = s[:s.index("]")]
            clk = s
        line[0] = r[0]
        line[1] = r[3]
        line[2] = r[4]
        line[3] = r[7]
        line[4] = r[8]
        line[5] = r[9]
        line[6] = "w"
        line[7] = move_num
        line[8] = opt_key
        line[9] = options[opt_ind]
        line[10] = val
        line[11] = 0
        line[12] = clk
        line[13] = 0
        ind = 0
        if(black):
            line[6] = "b"
            ind += l
        if("#" not in line[10] and line[10] != ""):
            f = 0.0
            if(black and "#" not in prevline[10] and prevline[10] != ""):
                f = float(line[10]) - float(prevline[10])
            elif(not black and '#' not in prevline[10 + l] and prevline[10 + l] != ""):
                f = float(line[10]) - float(prevline[10 + l])
            line[11] = str(round(f, 2))
        if(black and line[12] != "" and prevline[12 + l] != ""):
            tdelta = dt.strptime(prevline[12 + l], FMT) + timedelta(seconds = incre)
            tdelta -= dt.strptime(line[12], FMT)
            line[13] = str(tdelta)
        if(not black and line[12] != "" and prevline[12] != ""):
            tdelta = dt.strptime(prevline[12], FMT) + timedelta(seconds = incre)
            tdelta -= dt.strptime(line[12], FMT)
            line[13] = str(tdelta)
        for i in range(0, 14):
            prevline[i + ind] = line[i]
        csv_writer.writerow(line)
        line_count += 1
        if(line_count % 1000000 == 0):
            print(line_count, dt.now() - starttime)
        if(line_count % 5000000 == 0):
            fileindex += 1
            moves.close()
            if(fileindex == 3):
                break
            d = 'moves_' + str(fileindex) + '.csv'
            moves = open(d, mode = 'a+', newline = '')
            csv_writer = csv.writer(moves, delimiter = ',')
            csv_writer.writerow(header)
        if(fileindex == 3):
            break
    # intended to test results.

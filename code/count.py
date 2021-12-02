import csv

# This File requires pgn_1.csv
# It returns two files with two distributions
# elocount.csv with bins 0-100, 100-200, ... , 3400-3500 and the count
# timecount.csv with every time format played and the count

readpgn = open("pgn_1.csv", mode = "r")
elocsv = open("elocount.csv", mode = "a+")
timecsv = open("timecount.csv", mode = "a+")

reader = csv.reader(readpgn)
elowriter = csv.writer(elocsv)
timewriter = csv.writer(timecsv)

elo = list(range(0, 3500, 100))
count = [0] * len(elo)
timelist = []
timecount = []
line = 0

for r in reader:
    if(line == 0):
        line += 1
        continue
    el = (int(r[3]) + int(r[4])) / 2
    ind = int(el / 100)
    count[ind] += 1
    if(r[8] not in timelist):
        timelist.append(r[8])
        timecount.append(1)
    else:
        ind = timelist.index(r[8])
        timecount[ind] += 1
    line += 1
readpgn.close()
elowriter.writerow(elo)
elowriter.writerow(count)
elocsv.close()
timewriter.writerow(timelist)
timewriter.writerow(timecount)
timecsv.close()

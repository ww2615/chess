import csv
from datetime import datetime as dt

readpgn = open("pgn_1.csv", mode = "r")
elocsv = open("elocount.csv", mode = "a+")
timecsv = open("timecount.csv", mode = "a+")

reader = csv.reader(readpgn)
elowriter = csv.writer(elocsv)
timewriter = csv.writer(timecsv)

starttime = dt.now()

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
    if(line % 100000 == 0):
        print(line, dt.now() - starttime)
readpgn.close()
elowriter.writerow(elo)
elowriter.writerow(count)
elocsv.close()
timewriter.writerow(timelist)
timewriter.writerow(timecount)
timecsv.close()

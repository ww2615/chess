import csv
import pandas
from datetime import datetime

clk = "%clk"
eval = "%eval"
game_csv = open('pgn_1.csv', mode = 'w', newline = '')

csv_writer = csv.writer(game_csv, delimiter = ',')

keywords = ['Result', 'UTCDate', 'UTCTime', 'WhiteElo', 'BlackElo', 
            'WhiteRatingDiff', 'BlackRatingDiff', 'ECO', 'TimeControl', 'Termination', 'pgn']
readpgn = open("E:\LichessData\lichess_db_standard_rated_2021-10.pgn")
csv_writer.writerow(keywords)
line = []
count = 1
filemax = 1
fileindex = 1
max = 88092721
starttime = datetime.now()

while(count < max):
    notcomplete = True
    line = [""] * 11
    while(notcomplete): 
        rl = readpgn.readline()
        rl = rl[1:-2]
        header = rl.split(" ", 1)[0]
        s = ""
        if(header in keywords):
            s = rl.split(" ", 1)[1]
            s = s[1:-1]
            ind = keywords.index(header)
            line[ind] = s
        if(header == "Termination"):
            line[10] = ""
            if(s == "Abandoned"):
                line[10] = ""
            else:
                rl = readpgn.readline()
                rl = readpgn.readline()
                if clk in rl:
                    if eval in rl:
                        line[10] = rl
                    else:
                        line[10] = ""
            notcomplete = False
    if(line[10] != ""):
        csv_writer.writerow(line)
        filemax += 1
    count += 1
    if(count%5000000 == 0):
        print(count, datetime.now() - starttime)
    if(filemax%10000000 == 0):
        fileindex += 1
        game_csv.close()
        dir = 'pgn_' + str(fileindex) + '.csv'
        game_csv = open(dir, mode = 'w', newline = '')
        csv_writer = csv.writer(game_csv, delimiter = ',')
        csv_writer.writerow(keywords)
readpgn.close()
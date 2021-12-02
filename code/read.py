import csv
import pandas

clk = "%clk"
eval = "%eval"
game_csv = open('data_1.csv', mode = 'w', newline = '')
csv_writer = csv.writer(game_csv, delimiter = ',')

keywords = ['Result', 'UTCDate', 'UTCTime', 'WhiteElo', 'BlackElo',
            'WhiteRatingDiff', 'BlackRatingDiff', 'ECO', 'TimeControl', 'Termination', 'Evaluation']
readpgn = open("E:\LichessData\lichess_db_standard_rated_2021-10.pgn")
csv_writer.writerow(keywords)
line = []
count = 1
fileindex = 1
max = 88092721

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
            line[10] = "No"
            if(s == "Abandoned"):
                line[10] = "No"
            else:
                rl = readpgn.readline()
                rl = readpgn.readline()
                if clk in rl:
                    if eval in rl:
                        line[10] = "Yes"
                    else:
                        line[10] = "No"
            notcomplete = False
    csv_writer.writerow(line)
    count += 1
    if(count%10000000 == 0):
        fileindex += 1
        game_csv.close()
        dir = 'data_' + str(fileindex) + '.csv'
        game_csv = open(dir, mode = 'w', newline = '')
        csv_writer = csv.writer(game_csv, delimiter = ',')
        csv_writer.writerow(keywords)
readpgn.close()

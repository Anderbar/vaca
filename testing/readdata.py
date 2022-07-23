import csv

with open('testdata.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)

    for row in reader:
        print(row)
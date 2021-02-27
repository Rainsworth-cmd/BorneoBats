import numpy as np
import os
import csv

path="C:/Users/Dannis/PycharmProjects/Test/TestFolder"
f = open('bronebat.csv','w',newline='', encoding='utf-8');

csv_writer = csv.writer(f);
header = ["link","family","genus","specificEpithet","country","stateProvince","verbatimLocality","decimalLatitude","decimalLongitude","eventDate","eventTime","recordedBy","scientificName"];
csv_writer.writerow(header);

def iter_files(rootDir):
    records = [];

    #遍历根目录
    for root,dirs,files in os.walk(rootDir):
        count = 1;
        for file in files:
            record = ["", "", "", "", "", "", "", "", "", "","","",""]
            file_name = os.path.join(root,file)
            print(file_name)
            arr = file_name.split('\\');
            name = arr[1].split('.')[0];
            #print(name)
            if name == 'H cervinus':
                record[1] = "Hipposideros";
                record[2] = "Hipposideridae";
                record[3] = "cervinus";
                record[12] = "fawn leaf-nosed bat";
            elif name == "H diadema":
                record[1] = 'Hipposideros';
                record[2] = 'Hipposideridae';
                record[3] = 'diadema';
                record[12] = "diadem leaf-nosed bat";
            elif name == 'H dyacorum':
                record[1] = 'Hipposideros';
                record[2] = 'Hipposideridae';
                record[3] = 'dyacorum';
                record[12] = "Dayak roundleaf bat";
            elif name == 'H  galeritus 1 and 2':
                record[1] = 'Hipposideros';
                record[2] = 'Hipposideridae';
                record[3] = 'galeritus';
                record[12] = "Cantor's roundleaf bat";
            elif name == 'K minuta':
                record[1] = 'Kerivoula';
                record[2] = 'Vespertilionidae';
                record[3] = 'minuta';
                record[12] = "least woolly bat";
            elif name == 'R sedulous':
                record[1] = 'Rhinolophus';
                record[2] = 'Rhinolophidae';
                record[3] = 'sedulous';
                record[12] = "lesser woolly horseshoe bat";
            elif name =='R trifoliatus':
                record[1] = 'Rhinolophus';
                record[2] = 'Rhinolophidae';
                record[3] = 'trifoliatus';
                record[12] = "trefoil horseshoe bat";
            else:# change to elif name == 'R ridleyi' if fixed the error
                record[1] = 'Hipposideros';
                record[2] = 'Hipposideridae';
                record[3] = 'ridleyi';
                record[12] = "Ridley's leaf-nosed bat";
            record[4] = "Brunei";
            if (len(arr) == 3):
                time = arr[2].split();
                if (len(time) == 2):
                    record[9] = time[0];
                    #print(len(record));
                    record[10] = time[1].split('.')[0];
                else:
                    record[3] = arr[2];
            #print(record)
            records.append(record);
            count = count + 1;
    print(records);
    return records;

records = iter_files(path);
for i in range(len(records)):
    csv_writer.writerow(records[i]);


f.close()
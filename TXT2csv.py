import json
import pandas as pd
import csv
import os
import codecs


def generate_dict_from_file(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as source_file:
        for line in source_file:
            try:
                dic = json.loads(line)
                yield dic
            except Exception as e:
                print("*****"* 20)
                print(e)
                pass
def write_csv(output_dir,name, result_csv):
    f = open(os.path.join(output_dir, name), 'a+', encoding='utf-8-sig', newline='')
    f_csv = csv.writer(f)
    f_csv.writerow(result_csv)
    f.close()


if __name__ == '__main__':
    inputfile = r'D:\BaiduNetdiskWorkspace\Geotree of Geodetector\TheThird Tree\Py\download_full.txt'
    otfpath = r'D:\BaiduNetdiskWorkspace\Geotree of Geodetector\TheThird Tree\Py'
    for dic_ in generate_dict_from_file(inputfile):
        csv_result = list(dic_.values())
        write_csv(otfpath,'CSV_download_full.csv', csv_result)

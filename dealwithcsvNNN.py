import os
import pandas as pd
import re


def parse_information(sentense,flag):
    regulation = re.compile('\d+')
    if flag:
        if sentense.split(",")[-1].strip() == 'Peoples R China':
            country = 'china'
            province = sentense.split(',')[-2].strip()  #####判断是不是还有更下一级的城市
            flag = re.findall(regulation, province)
            if len(flag) > 0:
                return province.split()[0] + "," + country
            else:
                ### 首先判断是不是存在城市
                city = sentense.split(',')[-3].strip()
                if len(city.split()) == 1:
                    return city + "," + province.split()[0] + "," + country
                elif len(city.split()) == 2 and len(re.findall(regulation, city)):
                    # print(city.split()[0] ,province.split()[0] , country)
                    return city.split()[0] + "," + province.split()[0] + "," + country
                else:
                    return province.split()[0] + "," + country

        elif 'usa' in sentense.split(',')[-1] or 'USA' in sentense.split(',')[-1]:
            pass
            country = "usa"
            city = sentense.split(',')[-2].strip()
            return city + "," + country
        else:
            # print(sentense)
            country = sentense.split(',')[-1].strip()
            procince = sentense.split(',')[-2].strip()
            resultList = []
            for i in procince.split():
                if len(re.findall(regulation, i)) > 0:
                    pass
                else:
                    resultList.append(i)
            province = " ".join(resultList)
            if country == 'Canada' or country == 'Germany':
                city = sentense.split(',')[-3].strip()
                return city + "," + province + "," + country
            elif country == 'Brazil' and len(sentense.split(',')[-3].strip()) == 1:
                city = " ".join(sentense.split(',')[-3].strip().split()[1:])
                return city + "," + province + "," + country
            elif country == "Australia" and '&' not in sentense.split(',')[-3]:
                city = sentense.split(',')[-3].strip()
                return city + "," + province + "," + country
            else:
                return province + "," + country
            pass
    else:
        if ";;" in sentense:
            print(sentense)
            sentense_new = []
            for text in sentense.split(','):
                if len(text.split(';;')[0]) > 1:
                    sentense_new.append(text.split(';;')[0])
            if sentense_new[-1] == ' ':
                sentense_new = sentense_new[:-1]
            print(len(sentense_new),sentense_new )
            province =""
            city = ""
            if len(sentense_new) > 2 and sentense_new[-1] != ' ':
                province = sentense_new[-1].split(' ')[1]
                if len(sentense_new[-2]) <= 5 and sentense_new[-2][0] == ' ':
                    city = sentense_new[-2].split(' ')[1]


            print('中国' + province + city)
            return '中国' + province + city
            pass
        else:
            print(sentense)
            data = sentense.split(',')
            province =""
            city = ""
            if len(data) >3 and data[-1] == ' ':
                province = data[-2].split(' ')[1]
                if len(data[-3]) <= 5 and data[-3][0] == ' ':
                    city = data[-3].split(' ')[1]
            print('中国' + province + city)
            return '中国' + province + city
            pass


momo = []
# 按行记录地名
def record_name (i,res_list,df):
    # 记录地名
    if len(res_list):
        unique_place = res_list[0]
        print(res_list)
        print('----------unique_place---------', unique_place)
        df['PlaceName'][i] = unique_place
        # print('表', df['PlaceName'][i])

        # momo.append(mo)
        # print('momo', momo)

    else:
        print('-----------空-----------')
        df['PlaceName'][i] = 'None'
        # momo.append('None')


if __name__ == '__main__':
    # filepath = r'E:\TheThird Tree\Py\Result1331\result.csv'
    filepath =r'E:\TheThird Tree\Py\Result1331\result1331.csv'
    df = pd.read_csv(filepath, encoding='utf-8')
    df['PlaceName'] = ''
    flag = False
    momo = []
    for i in range(df.shape[0]):
        print('i',i)
        if isinstance(df.loc[i, 'address_ch'],float):
            flag = True
            res_list = []
            text_information = str(df.loc[i, 'address_en']).split('[')

            for sentences in text_information[1:]:
                print('sentences',sentences)
                res = parse_information(sentences, flag)
                res_list.append(res)
                # 记录地名
                record_name(i,res_list,df)
            flag = False
            pass
        else:
            res_list = []
            splitData = df.loc[i, 'address_ch'].split('中国.')
            if len(splitData) ==1:
                splitDatasecond = splitData[0].split('.')

                if len(splitDatasecond) == 2:
                    res = parse_information(splitDatasecond[0],flag)
                    # print('此地无银三百两',res)
                    # break
                    res_list.append(res)
                    record_name(i,res_list,df)

                else:
                    for data in splitDatasecond[:-1]:
                        res = parse_information(data,flag)
                        res_list.append(res)
                        # 记录地名
                        record_name(i,res_list,df)

                pass
            elif len(splitData) == 2:

                if len(splitData[1]) >1:
                    for data in splitData:
                        res = parse_information(data,flag)
                        res_list.append(res)
                        # 记录地名
                        record_name(i,res_list,df)
                else:
                    print(splitData)
                    splitDatasecond = splitData[0].split('.')
                    if len(splitDatasecond) == 1:
                        res = parse_information(splitDatasecond[0], flag)
                        res_list.append(res)
                        record_name(i,res_list,df)
                        # print('此地无银三百两',res)
                        # break
                    else:
                        for data in splitData[:-1]:
                            res = parse_information(data, flag)
                            res_list.append(res)
                            # 记录地名
                            record_name(i,res_list,df)
                pass
            else:
                for data in splitData[:-1]:
                    res = parse_information(data, flag)
                    res_list.append(res)
                    # 记录地名
                    record_name(i,res_list,df)
                pass

# data = pd.DataFrame({'name': momo})
# data.to_csv("momo.csv", sep=',')

df.to_csv('000.csv', encoding='utf-8-sig')

# TODO 代码运行正常 共有2篇地名缺失（939篇） 已补充

# TODO WOS直接导出时用这个
'''
def parse_second(sentense):
    regulation = re.compile('\d+')

    if sentense.split(",")[-1].strip() == 'Peoples R China':
        pass
        country = 'china'
        province = sentense.split(',')[-2].strip()  #####判断是不是还有更下一级的城市
        # print(sentense)
        flag = re.findall(regulation, province)
        if len(flag) > 0:
            return province.split()[0] +"," + country
        else:
            ### 首先判断是不是存在城市
            city = sentense.split(',')[-3].strip()
            if len(city.split()) ==1:
                return city + "," + province.split()[0] + "," + country
            elif len(city.split()) ==2 and len(re.findall(regulation, city)):
                # print(city.split()[0] ,province.split()[0] , country)
                return city.split()[0] + "," + province.split()[0] + "," + country
            else:
                return province.split()[0] + "," + country

    elif 'usa' in sentense.split(',')[-1] or 'USA' in sentense.split(',')[-1]:
        pass
        country = "usa"
        city = sentense.split(',')[-2].strip()
        return city + "," + country
    else:
        # print(sentense)
        country = sentense.split(',')[-1].strip()
        procince = sentense.split(',')[-2].strip()
        resultList = []
        for i in procince.split():
            if len(re.findall(regulation, i)) > 0:
                pass
            else:
                resultList.append(i)
        province = " ".join(resultList)
        if country == 'Canada' or country == 'Germany':
            city = sentense.split(',')[-3].strip()
            return city + "," + province + "," + country
        elif country == 'Brazil' and len(sentense.split(',')[-3].strip())==1:
            city = " ".join(sentense.split(',')[-3].strip().split()[1:])
            return city + "," + province + "," + country
        elif country =="Australia" and '&' not in sentense.split(',')[-3]:
            city = sentense.split(',')[-3].strip()
            return city + "," + province + "," + country
        else:
            return province + "," + country
        pass



def parse_first(text):
    
    # 1.判断传进来的数据是什么，str 或者list
    
    if isinstance(text, list):
        result = []
        for text_information in text.split(';'):
            result.append(parse_second(text_information))
        return result
    elif isinstance(text, str):
        result = []
        result.append(parse_second(text))
        return result
    pass


df = pd.read_csv(filepath, header=0,encoding='utf-8')
autherList = df.address_en.tolist()
momo=[]
for information in autherList:
    #split(';')[1:]
    print(information )
    if information[0] == '[':
        text = information.split('[')[1]
        print(text)
    else:
        text = information.split('.')[0]
        print(text)

    result = parse_first(text)
    res = list(filter(None, result))   ### 人名字也是有;分隔，后面完善[A:B:C] 等等
    print('res', res)
    print("*****"*20)
    momo.extend(res)
    # print('momo', momo)

data = pd.DataFrame({'name': momo})
data.to_csv("Place_result.csv", sep=',')
'''

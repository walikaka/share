# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 22:40
# @Author  : walikaka
# @Software: PyCharm
import json
import os
import time
import requests
import codecs
from lxml import etree
import random
import re
'''
    1.返回的结果是引文的结果，与网页上显示的结果不一致（与网页源代码也不一致）
    2.有些文章的字段不一样，需要使用节点轴选择 text()=""
    3.使用'''''' 解决有些格式问题
'''
requests.packages.urllib3.disable_warnings()
requests.adapters.DEFAULT_RETRIES = 5

'''
    TS=(geodetector OR geographic detector OR geographical detector OR geo-detector)
'''
def jsonDump(dic, filepath, filename):
    #首先把数据保存为json格式
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    with codecs.open(os.path.join(filepath, filename) + '.json', 'a', 'utf-8') as out_file:
        json.dump(dic, out_file, ensure_ascii=False)
        out_file.write('\n')


headers1 = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'Connection': 'close',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Host": "apps.webofknowledge.com",
    "Upgrade-Insecure-Requests": "1",
    #TODO 检索页面Network-ALL-Cookie 可能需要每天更换
    # 'cookies': '_gcl_au=1.1.2097316149.1609943677; _hjid=f1d35f7b-9b18-4ad9-9cb8-4f97c2a560f0; td_cookie=206984184; CUSTOMER="CAS Institute of Geographic Sci and Nat Resources Research"; E_GROUP_NAME="ID Set 2007"; bm_sz=0FED63A137B51B3D61C9FFA795DEDA38~YAAQHNrARQyAv/t2AQAAEgrH/wrc7+fT09fbk1dULwMgNo3pFzDbWIEZ1VZ5nNXD0m72/15SKJCJuHlih5sPwErQRSottMAPuk9IhsdWW0VYTeJKmkq13Na9N+le+yjemnxom0FGb4ILqHujdq7/FYq1AeayRMdSHQIg4nrlxPepWTCeYN4ixaeIc8wmlSdpmcIvJvYWCg==; dotmatics.elementalKey=SLsLWlMhrHnTjDerSrlG; _hjTLDTest=1; SID="6AvqF45Vsra1TIL74Sl"; ak_bmsc=28FC29A4AB57130143E7E855A51617C645C0DA0CF47A0000B00E00601580DB76~plcxZMFZiK1x+5qwEUILkzTbdx+iuEcoKWQO+Je4Nwt18FDiJz5djIbdUmJVoHMm73FE9pYsJcHoqbOA1Wo1nYfdvCjZc1Yd36LsUhxXR8/QTMguZEVm3wiSiPCySU4mzJlXCNJ6hvuX3MVEHzWBSqhTW3tKW/sL6AablqGY4+SNWaKYUUKuXHNouApExD3MYGsBZvTPgA5fzoi52SGmWAHB3OHrSCPvSGh9fpxC2w0BycLhNaFJ5OSj7L3Lp9e39I; _sp_ses.630e=*; _hjAbsoluteSessionInProgress=1; JSESSIONID=8D96FF9E6F76AC01203AC8826D6B25D4; bm_sv=5CF99C88640B97E317B7DA118B360435~lLQw6UJXArYZBYhL3ew7fjwlvaYXO5/MDosEVSz7+ip9Zf1DSY5sAzG25yAO9LJTh4oFt+NeMSMJ/PGWUhxzqiuZrn4bXUc64td7oPrK5QeycmpVZ44ETgm4KtK69Do/ODiA9Po0Mp491E3CoCXmvgv3E/JpF9LgHEVR2x0y5N4=; RT="z=1&dm=webofknowledge.com&si=3222f658-9042-499b-bafb-b6ab2a4ab29c&ss=kjwnh68p&sl=9&tt=mep&obo=3&rl=1"; _sp_id.630e=082a599d-e010-4263-8505-7b3cd12146b7.1609943678.19.1610617809.1610611291.06d050ca-beb6-4909-a0fb-83332a700a2f; _abck=37C5102B40CCD029CF8E8E1BFA64CA98~0~YAAQDNrARc48u/t2AQAAsWhNAAXGe/EgaPZsXwVqtNDVBXzdsWhXum0wEaXnphC1HjbglJLwxs96/vOmxI9SdwcL9MZCXLcV3ZbXuziEp+4fVGf038UA+PFt6cdcg9IIWTIQ0SI9lsLFUIDnRw+G1wDTOFgxGg6AOGjZ3m/PJFqwx0FmMIB8thUcJxIrNXV0hhw3eVO5Qe9yPTd4N7pZZPSkeZllM+jJ5/T4zfVxfLUEtwPD+6PAu31VgAXj7PIH4s7PdU/K459S2HyYrWHCOaLlMF1GiLwQ1xk9r/kJDWlCW64JFdGi2bv8R5ndZP1VMSY1VA3WY+iXmNe9wOz0LfODpxOfLod0zEHjd+C3~-1~-1~-1'
    'cookies':'_gcl_au=1.1.1446020117.1625122872; _hjid=8377b553-18b9-4256-8893-673fc587ae3d; dotmatics.elementalKey=SLsLWlMhrHnTjDerSrlG; bm_sz=9A3E08B2728788D5D91545DAD089CDF1~YAAQJetGaKa5mZZ7AQAAdOO9IQ2Rl1wcxh8bKyeY5mnkoLw8HOSnBIsCdbrNt8HdmTjlGVCSkzL5JZ5VM002UX9sc47WaR7g55kfAETIeFzzrZ8fZKSeaoI8NfKqhP6CBsjaho9oSuefwxZZyn7WAVMg+Dy1kcFVl7m4Sj+yHce4BcxSnOgNWD2PM9biIaDpqFbAe0LM1A4=; SID="8DwNi8O9lQvCcuovu2v"; CUSTOMER="CAS Institute of Geographic Sci and Nat Resources Research"; E_GROUP_NAME="ID Set 2007"; ak_bmsc=89FF305D95B9F15542A05230624CD32D~000000000000000000000000000000~YAAQJetGaF/ImZZ7AQAAUvXJIQ2fvXi7HSh3bPqx1E5nVtgVENHoTSB5Q+ks+zJ+3pfK+PKUKxcjjk+Uigu410N0l5Y/e5ydYwjSKxcAW34d1RFhIj4M94yUxhLb4yZrpLolPsS5dhYKcDNAvYK+GNiU2a0F4OMvRliVDI2o7xQr/8KB669JqYryQZ29cviPxYUjsL4YviMoStycpQh8Vr30jeuJf1iH901Tc922z2bSTQUzWY3QSg5sHea340Wum8R1MLZhrlnMdJNS4x46ANB1aEpJJ0751F/5mzDHpO4paDc1dHC9NKfG9Smkf1IFiveOQzZufh/bdlhqT+2hxRsR4HWrGekfCZ2NJEK3xETOlYwiCuddHQ6FSkXtT1Aq1Ln8Ycjt2/lPBeWCb7HAdwunHQ==; _sp_ses.630e=*; _hjIncludedInPageviewSample=1; _hjAbsoluteSessionInProgress=0; _abck=7937E62FED6EC1BE632240DE41F727AC~0~YAAQJetGaAjJmZZ7AQAAIUzKIQYH0TnTr9uMR0zj5k1Izt9Qf4xAZn3qtSX6ur+m8B6gVQiCv7Aw6soOCEECIBNEYs8W9Gy0CeKP2sBVghTpe4ui/9PWb1sCc33kWzBnHkmjglu6sPQr0uI9a3IuCEDYBPLyOwLUgsZdzqi9HIKrvJPirMpRzdtET92X5oCg4DBwG6cUr/A5oIV7szgyWSE0ngcLTY6fSVe05bXdDORhlD9kaJgOHHVCgQtXqCKJFgiKsYImYsGr1gcKOq67ZaQjaAMH9GrMUKWDad2tEURLIFzZJJyRnlDrZVnw1Kl2gnnpKfBzKDWHJI/HbzIJVpOif/xtt0SQArXorqYEworTSjS0VAD/P12YajOgiGL5DgibWW1hxAX3lI2501EzeAYx66oY/yNdM2YWY0JUrGU=~-1~-1~-1; bm_sv=61A1F1DE5314574A931A57F8FC988DB5~Ehc6IYt+K4eOnlkzDBf4b6+thN1BZB8/q07gb3Xk2tB67EnA2rktT9dNa/AtL0yv/2J0sdlmgtmnuOKxdBDj5cf+Xbm7pgRJGpQiRvBbPtsb+JRXmXkSVf+KRjGQBVks1TU6bH/jq8RQLrTam0IW66fF4VGIj6kcd4xXHinBNQc=; _sp_id.630e=cd06382d-1e92-44d4-a5dc-d0eba9130ceb.1625122873.14.1632654522.1632631414.207472b0-10fd-4880-a51e-696278f4f9de; JSESSIONID=D410ECCC847FA3A2C359A9DF8DCE5E9B; RT="z=1&dm=webofknowledge.com&si=b13a25ac-522c-44d4-a926-a37465f9eda8&ss=ku14b4iq&sl=5&tt=dis&bcn=%2F%2F684d0d3d.akstat.io%2F&ld=1fb9&ul=1gyk"'


}

headers2 = {
    "user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    'connection': 'close',
    #TODO 详情页面Network-ALL-Cookie 可能需要每天更换
    # 'cookie': '_gcl_au=1.1.2097316149.1609943677; _hjid=f1d35f7b-9b18-4ad9-9cb8-4f97c2a560f0; td_cookie=206984184; CUSTOMER="CAS Institute of Geographic Sci and Nat Resources Research"; E_GROUP_NAME="ID Set 2007"; bm_sz=0FED63A137B51B3D61C9FFA795DEDA38~YAAQHNrARQyAv/t2AQAAEgrH/wrc7+fT09fbk1dULwMgNo3pFzDbWIEZ1VZ5nNXD0m72/15SKJCJuHlih5sPwErQRSottMAPuk9IhsdWW0VYTeJKmkq13Na9N+le+yjemnxom0FGb4ILqHujdq7/FYq1AeayRMdSHQIg4nrlxPepWTCeYN4ixaeIc8wmlSdpmcIvJvYWCg==; dotmatics.elementalKey=SLsLWlMhrHnTjDerSrlG; _hjTLDTest=1; SID="6AvqF45Vsra1TIL74Sl"; ak_bmsc=28FC29A4AB57130143E7E855A51617C645C0DA0CF47A0000B00E00601580DB76~plcxZMFZiK1x+5qwEUILkzTbdx+iuEcoKWQO+Je4Nwt18FDiJz5djIbdUmJVoHMm73FE9pYsJcHoqbOA1Wo1nYfdvCjZc1Yd36LsUhxXR8/QTMguZEVm3wiSiPCySU4mzJlXCNJ6hvuX3MVEHzWBSqhTW3tKW/sL6AablqGY4+SNWaKYUUKuXHNouApExD3MYGsBZvTPgA5fzoi52SGmWAHB3OHrSCPvSGh9fpxC2w0BycLhNaFJ5OSj7L3Lp9e39I; _sp_ses.630e=*; _hjAbsoluteSessionInProgress=1; RT="z=1&dm=webofknowledge.com&si=3222f658-9042-499b-bafb-b6ab2a4ab29c&ss=kjwnh68p&sl=a&tt=qgi&obo=3&rl=1"; JSESSIONID=42A59DF2E2AAEBBB111EC955DDCDEC2E; bm_sv=5CF99C88640B97E317B7DA118B360435~lLQw6UJXArYZBYhL3ew7fjwlvaYXO5/MDosEVSz7+ip9Zf1DSY5sAzG25yAO9LJTh4oFt+NeMSMJ/PGWUhxzqiuZrn4bXUc64td7oPrK5QeycmpVZ44ETgm4KtK69Do/P8+JDnF6JXy7eie7B8cDVV3Qe4fiSCYlFBYzYCWHTGc=; _sp_id.630e=082a599d-e010-4263-8505-7b3cd12146b7.1609943678.19.1610617875.1610611291.06d050ca-beb6-4909-a0fb-83332a700a2f; _abck=37C5102B40CCD029CF8E8E1BFA64CA98~0~YAAQDNrARQ0+u/t2AQAAKm1OAAWbaoUFnjOd6Nwjkk3zc1NiUON+gy8kF/YjnsFvG/yvMYcMspNubCG6EIDosluxpnl2MnxNJf1EUpjcucTd/sr6oVCxQ7uGFI0p7rufXLHndB3yRQ/9TWT3t9XJJ4kGdTfmTwYp4VIhIyjbZzu5bvXEghyc0AscdeNpvTERdTeik7A+z/ntUN7LC+P35LyEmF4KT3xrofpxE1o2gEKMaXe7354Zt7cv3lG5pHVjXlf9qPxeinePAAPOJ9FtmzAyH3nM3LdkkEl24tB9x5HXrSDzFriNSrwBj1kS6/F6p3EoBsFAf7vBErzTRBIFJTUbCT25nIH8cg2s5uX0~-1~-1~-1'
    'cookie':'_gcl_au=1.1.1446020117.1625122872; _hjid=8377b553-18b9-4256-8893-673fc587ae3d; dotmatics.elementalKey=SLsLWlMhrHnTjDerSrlG; bm_sz=9A3E08B2728788D5D91545DAD089CDF1~YAAQJetGaKa5mZZ7AQAAdOO9IQ2Rl1wcxh8bKyeY5mnkoLw8HOSnBIsCdbrNt8HdmTjlGVCSkzL5JZ5VM002UX9sc47WaR7g55kfAETIeFzzrZ8fZKSeaoI8NfKqhP6CBsjaho9oSuefwxZZyn7WAVMg+Dy1kcFVl7m4Sj+yHce4BcxSnOgNWD2PM9biIaDpqFbAe0LM1A4=; SID="8DwNi8O9lQvCcuovu2v"; CUSTOMER="CAS Institute of Geographic Sci and Nat Resources Research"; E_GROUP_NAME="ID Set 2007"; ak_bmsc=89FF305D95B9F15542A05230624CD32D~000000000000000000000000000000~YAAQJetGaF/ImZZ7AQAAUvXJIQ2fvXi7HSh3bPqx1E5nVtgVENHoTSB5Q+ks+zJ+3pfK+PKUKxcjjk+Uigu410N0l5Y/e5ydYwjSKxcAW34d1RFhIj4M94yUxhLb4yZrpLolPsS5dhYKcDNAvYK+GNiU2a0F4OMvRliVDI2o7xQr/8KB669JqYryQZ29cviPxYUjsL4YviMoStycpQh8Vr30jeuJf1iH901Tc922z2bSTQUzWY3QSg5sHea340Wum8R1MLZhrlnMdJNS4x46ANB1aEpJJ0751F/5mzDHpO4paDc1dHC9NKfG9Smkf1IFiveOQzZufh/bdlhqT+2hxRsR4HWrGekfCZ2NJEK3xETOlYwiCuddHQ6FSkXtT1Aq1Ln8Ycjt2/lPBeWCb7HAdwunHQ==; _sp_ses.630e=*; _hjIncludedInPageviewSample=1; _hjAbsoluteSessionInProgress=0; _abck=7937E62FED6EC1BE632240DE41F727AC~0~YAAQJetGaAjJmZZ7AQAAIUzKIQYH0TnTr9uMR0zj5k1Izt9Qf4xAZn3qtSX6ur+m8B6gVQiCv7Aw6soOCEECIBNEYs8W9Gy0CeKP2sBVghTpe4ui/9PWb1sCc33kWzBnHkmjglu6sPQr0uI9a3IuCEDYBPLyOwLUgsZdzqi9HIKrvJPirMpRzdtET92X5oCg4DBwG6cUr/A5oIV7szgyWSE0ngcLTY6fSVe05bXdDORhlD9kaJgOHHVCgQtXqCKJFgiKsYImYsGr1gcKOq67ZaQjaAMH9GrMUKWDad2tEURLIFzZJJyRnlDrZVnw1Kl2gnnpKfBzKDWHJI/HbzIJVpOif/xtt0SQArXorqYEworTSjS0VAD/P12YajOgiGL5DgibWW1hxAX3lI2501EzeAYx66oY/yNdM2YWY0JUrGU=~-1~-1~-1; JSESSIONID=FDF7B9265FFA871B65B3753F95FBB5FE; bm_sv=61A1F1DE5314574A931A57F8FC988DB5~Ehc6IYt+K4eOnlkzDBf4b6+thN1BZB8/q07gb3Xk2tB67EnA2rktT9dNa/AtL0yv/2J0sdlmgtmnuOKxdBDj5cf+Xbm7pgRJGpQiRvBbPtsb+JRXmXkSVf+KRjGQBVksBFw0A/nEb4R3yVC0uT64i+Mh8Fjf0y4ufmr3m4O3qc8=; _sp_id.630e=cd06382d-1e92-44d4-a5dc-d0eba9130ceb.1625122873.14.1632654526.1632631414.207472b0-10fd-4880-a51e-696278f4f9de; RT="z=1&dm=webofknowledge.com&si=b13a25ac-522c-44d4-a926-a37465f9eda8&ss=ku14b4iq&sl=6&tt=faz&bcn=%2F%2F684d0d3d.akstat.io%2F&ld=1ir2&nu=81sgm2yn&cl=2r31&ul=2r3b"'


}


def parse_url(url, title, site, site_url, flag):
    ### 解析不出来就换一下 cookies
    print(url)
    if flag:
        # time.sleep(random.uniform(0.5, 1))
        response = requests.get(url, headers=headers2, verify=False, timeout=15)
        if response.status_code == 200:
            text = response.text
            html = etree.HTML(text)

            author_en = ";".join(html.xpath('.//div[@class="block-record-info"][1]/p[@class="FR_field"][1]/a/text()'))
            print("author_en: %s"%author_en)
            author_ch = ";".join(html.xpath('.//div[@class="block-record-info"][1]/p[@class="FR_field"][2]/a/text()'))
            print("author_ch: %s"%author_ch)
            # journal_en = html.xpath('.//div[@class="block-record-info block-record-info-source"]/p[@class="sourceTitle"][1]/value/text()')[0]
            journal_en = "".join(html.xpath(
                './/div[@class="block-record-info block-record-info-source"]/p[@class="sourceTitle"]//text()')).strip()

            print("journal_en: %s"%journal_en)
            journal_ch = "".join(html.xpath('.//div[@class="block-record-info block-record-info-source"]/p[@class="sourceTitle"][2]//text()')).strip()

            print("journal_ch %s"%journal_ch)
            # article_palce = "".join(html.xpath('.//div[@class="block-record-info block-record-info-source"]/div[@class="block-record-info-source-values"]//text()')).strip().replace('\n','')
            # print(article_palce)
            # pub_num = html.xpath('.//div[@class="block-record-info block-record-info-source"]/p[@class="FR_field"][1]/text()')[1].strip()
            # print(pub_num)
            publish_year = ''.join(html.xpath('//span[text()="Published:"]/following-sibling::*/text()')).strip()
            print("publish_year: %s"%publish_year)
            doc_type = ''.join(html.xpath('//span[text()="Document Type:"]/../text()')).strip()
            print("doc_type: %s"%doc_type)
            abstract_en = ''.join([i.strip() for i in html.xpath('//div[text()="Abstract"]/../p[1]//text()')])
            print("abstract_en: %s"%abstract_en)
            abstract_ch = ''.join(html.xpath('//span[text()="Abstract:"]/../text()')).strip()
            print("abstract_ch: %s"%abstract_ch)
            times_cited = ''.join(html.xpath('//span[text()="All Times Cited Counts"]/../p[1]//text()')).strip()
            print(" times_cited: %s" %times_cited)

            #### 分类讨论一下
            keywords = ''.join([i.strip() for i in html.xpath('//span[text()="Author Keywords:"]/..//text()')]).strip()
            result = keywords.split('Author Keywords:')
            keywords_ch = ""
            keywords_en = ""
            if len(result) == 2:
                keywords_ch = result[1]
            elif len(result) ==3:
                keywords_ch = result[2]
                keywords_en = result[1]
            print("keywords_ch: %s"%keywords_ch)
            print("keywords_en: %s" % keywords_en)
            # keywords_ch = ("".join(html.xpath('.//div[@class="block-record-info"][3]/p[@class="FR_field"][2]/text()'))).strip()
            # print(keywords_ch)
            address_en = ''.join([i.strip() for i in html.xpath('//div[text()="Author Information"]/../p[1]//text()')]).strip().replace('Addresses:','')
            print("address_en: %s"%address_en)
            address_ch = ''.join([i.strip() for i in html.xpath('//div[text()="Author Information"]/../p[2]//text()')]).strip().replace('Addresses:','')
            if '@' in address_ch:
                address_ch = address_en
                address_en = ""
            print("address_ch: %s"%address_ch)
            research_areas = ''.join(html.xpath('//span[text()="Research Areas:"]/../text()')).strip()
            print("research_areas: %s"%research_areas)
            dic = {
                "url": url,
                "title": title,
                "site": site,
                "site_url" : site_url,
                "author_en" : author_en,
                "author_ch" : author_ch,
                "journal_en" : journal_en,
                "journal_ch" : journal_ch,
                # "article_palce" : article_palce,
                # "pub_num" : pub_num,
                "publish_year" :publish_year,
                "doc_type": doc_type,
                "abstract_en" : abstract_en,
                "abstract_ch" :abstract_ch,
                "keywords_en" : keywords_en,
                "keywords_ch" : keywords_ch,
                "address_en" : address_en,
                "address_ch" : address_ch,
                "research_areas" : research_areas,
                # 中文文献无WOS分类
                "wos_categories": "",
                "times_cited": times_cited,
            }
            jsonDump(dic, filepath, 'knowledge')
    else:
        ##### 有两种结构需要分开讨论,
        ### 后面补充和完善一下
        # time.sleep(random.uniform(0.5, 1))
        response = requests.get(url, headers=headers2, verify=False, timeout=15)
        if response.status_code == 200:
            text = response.text
            html = etree.HTML(text)
            author_en = "".join([i.strip() for i in html.xpath('//span[text()="By:"]/following-sibling::*//text()')])
            print("author_en: %s" % author_en)
            regulation = re.compile('\d+')
            re_flag = re.findall(regulation, author_en)
            if len(re_flag) > 0:
                # journal_en = html.xpath('.//div[@class="block-record-info block-record-info-source"]/p/span[@class="sourceTitle"]/value/text()')[0]

                journal_en ="".join(html.xpath('.//div[@class="block-record-info block-record-info-source"]/p/span[@class="sourceTitle"]//text()')).strip()
                print("journal_en: %s" % journal_en)
                doi = ''.join(html.xpath('//span[text()="DOI:"]/following-sibling::*/text()')).strip()
                print("doi: %s" % doi)
                publish_year = ''.join(html.xpath('//span[text()="Published:" or text()="Early Access: "]/following-sibling::*/text()')).strip().replace('\n','')
                print("publish_year: %s" % publish_year)
                doc_type = ''.join(html.xpath('//span[text()="Document Type:"]/../text()')).strip()
                print("doc_type: %s" % doc_type)
                abstract = ''.join([i.strip() for i in html.xpath('//div[text()="Abstract"]/..//text()')]).replace('Abstract', '')
                print("abstract: %s" % abstract)
                keywords = ';'.join(html.xpath('//span[text()="Author Keywords:" or text()="KeyWords Plus:" or text()="Author Keywords:"]/following-sibling::*/text()')).strip()
                print("keywords: %s" % keywords)
                #### 根据兄弟节点进行匹配
                ###  ‘’‘ ’‘’解决换行的问题
                address = '\n'.join(html.xpath('''//span[text()="Addresses:
        "]/../following-sibling::table[1]//tr/td[2]/a/text()'''))
                print("address: %s" % address)
                research_areas = ''.join(html.xpath('//span[text()="Research Areas:"]/../text()')).strip()
                print("research_areas: %s" % research_areas)
                wos_categories = ''.join(html.xpath('//span[text()="Web of Science Categories:"]/../text()')).strip()
                print("wos_categories: %s" % wos_categories)
                dic = {
                    "url": url,
                    "title": title,
                    "site": site,
                    "site_url": site_url,
                    "author_en": author_en,
                    "author_ch": "",
                    "journal_en": journal_en,
                    "journal_ch": "",
                    "publish_year": publish_year,
                    "doc_type": doc_type,
                    "abstract_en": abstract,
                    "abstract_ch": "",
                    "keywords_en": keywords,
                    "keywords_ch": "",
                    "address_en": address,
                    "address_ch": "",
                    "research_areas": research_areas,
                    "wos_categories": wos_categories,

                }
                jsonDump(dic, filepath, 'knowledge')
            else:
                # journal_en = html.xpath('.//div[@class="block-record-info block-record-info-source"]/p[@class="sourceTitle"]/value/text()')[0]
                journal_en = "".join(html.xpath('.//div[@class="block-record-info block-record-info-source"]/p[@class="sourceTitle"]//text()')).strip()

                print("journal_en: %s" % journal_en)
                doi = ''.join(html.xpath('//span[text()="DOI:"]/../text()')).strip()
                print("doi: %s" % doi)
                publish_year = ''.join(html.xpath('//span[text()="Published:" or text()="Early Access: "]/following-sibling::*/text()')).strip()
                print("publish_year: %s" % publish_year)
                doc_type = ''.join(html.xpath('//span[text()="Document Type:"]/../text()')).strip()
                print("doc_type: %s" % doc_type)
                # abstract = ''.join(html.xpath('//div[text()="Abstract"]//following-sibling::div//text()')).strip()
                abstract = ''.join([i.strip() for i in html.xpath('//div[text()="Abstract"]/..//text()')]).replace('Abstract', '')
                print("abstract: %s" % abstract)
                keywords = ''.join([i.strip() for i in html.xpath('//span[text()="Keyword List:" or text()="KeyWords Plus:" or text()="Author Keywords:"]/..//text()')]).replace('Keyword List:', '')
                print("keywords: %s" % keywords)
                address = ''.join([i.strip() for i in html.xpath('//span[text()="Addresses:"]/..//text()')]).replace('Addresses:', '')
                print("address: %s" % address)
                research_areas = ''.join(html.xpath('//span[text()="Research Areas:"]/../text()')).strip()
                print("research_areas: %s" % research_areas)
                wos_categories = ""

                dic = {
                    "url": url,
                    "title": title,
                    "site": site,
                    "site_url": site_url,
                    "author_en": author_en,
                    "author_ch": "",
                    "journal_en": journal_en,
                    "journal_ch": "",
                    "publish_year": publish_year,
                    "doc_type": doc_type,
                    "abstract_en": abstract,
                    "abstract_ch": "",
                    "keywords_en": keywords,
                    "keywords_ch": "",
                    "address_en": address,
                    "address_ch": "",
                    "research_areas": research_areas,
                    "wos_categories": wos_categories,

                }

                jsonDump(dic, filepath, 'knowledge')


def get_url(url, filepath):
    print(url)
    # time.sleep(random.uniform(1, 3))
    s = requests.Session()
    s.keep_alive = False
    # try:
    response = requests.get(url, headers=headers1, verify=False, timeout=15)
    print('11',response)
    if response.status_code == 200:
        text = response.text
        html = etree.HTML(text)
        descs = html.xpath('.//div[@class="search-results"]/div[@class="search-results-item"]')
        #### 先判断是不是专利，
        for desc in descs:
            flag_type = desc.xpath('.//div[@class="search-results-data-cite"]/text()')
            if len(flag_type) > 0:  ####用来判断是文章或者是专利
                pass
                url = desc.xpath('./div[@class="search-results-content"]/div/div[1]/div/a/@href')
                if len(url) > 0:
                    url = "http://apps.webofknowledge.com" + url[0]
                    title = desc.xpath('./div[@class="search-results-content"]/div/div[1]/div/a/value//text()')
                    title = ''.join(title)
                    title = title.replace('\n', '')
                    ### 增加flag字段用于判断是中国人写的还是外国人写的
                    flag = False
                else:
                    url = "http://apps.webofknowledge.com" + desc.xpath('./div[@class="search-results-content"]/div/div[1]/a/@href')[0]
                    title1 = desc.xpath('./div[@class="search-results-content"]/div/div[1]/a/value/text()')
                    title1 = (''.join(title1)).replace('\n', '')
                    title2 = desc.xpath('./div[@class="search-results-content"]/div/div[2]/div/a/value/text()')
                    title2 = (''.join(title2)).replace('\n', '')
                    title = title1 + ';' + title2
                    flag = True
                site = desc.xpath('.//div[@class="search-results-data-cite"]/a/text()')
                if len(site) > 0:
                    site = site[0]
                    site_url = "http://apps.webofknowledge.com" + desc.xpath('.//div[@class="search-results-data-cite"]/a/@href')[0]
                else:
                    site = 0
                    site_url = ""
                parse_url(url, title, site, site_url, flag)
            else:
                # 写入专利
                url = "http://apps.webofknowledge.com" + desc.xpath('./div[@class="search-results-content"]/div/div[1]/div/a/@href')[0]
                title = desc.xpath('./div[@class="search-results-content"]/div/div[1]/div/a/value//text()')
                title = ''.join(title)
                title = title.replace('\n', '')
                patent_number = desc.xpath('./div[@class="search-results-content"]/div/div[2]/span[@class="data_bold"]/value//text()')[0]
                The_patente = "".join(desc.xpath('./div[@class="search-results-content"]/div/div[3]//text()')[1:])
                Invention = ("".join(desc.xpath('./div[@class="search-results-content"]/div/div[4]//text()')[1:])).replace("; et al.","").replace("; 等.","")
                dic = {
                    "url" : url,
                    "title" : title,
                    "patent_number" : patent_number,
                    "The_patente" : The_patente ,
                    "Invention" : Invention ,
                }
                print(dic)
                jsonDump(dic, filepath, 'patent')

if __name__ == '__main__':
    filepath = r'D:\BaiduNetdiskWorkspace\Geotree of Geodetector\TheThird Tree\Py'
    # filepath = r'D:\graduate_project\other\liang'
    #TODO SID=8AUOBgKBVOPpfCHaxzW要根据时间换上最新的，不然抓取不到数据
    # url = "http://apps.webofknowledge.com/summary.do?product=UA&colName=&qid=3&SID=6AvqF45Vsra1TIL74Sl&search_mode=GeneralSearch&formValue(summary_mode)=GeneralSearch&update_back2search_link_param=yes&page={}"
    url ='https://apps.webofknowledge.com/Search.do?product=WOS&SID=8DwNi8O9lQvCcuovu2v&search_mode=GeneralSearch&prID=3140ccfb-2a03-4da9-a2d0-cfc6633069f2'

    # TODO 页码改为总页数+1
    for i in range(1, 2):  ### 总共54页 左闭右开
        get_url(url.format(i), filepath)

# TODO timeout URL
# http://apps.webofknowledge.com/full_record.do?product=UA&search_mode=CitingArticles&qid=32&SID=5C42Q9ByDRez988Gboh&page=3&doc=119
# 16(751) 26(1279)

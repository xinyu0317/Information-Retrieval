import os
import json
from os.path import dirname, abspath
import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning

from gne import GeneralNewsExtractor
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

path = dirname(abspath(__file__)) + '/data/'

cookies = {
    'TADCID': 'S-RCEEVrSy6DkhzNABQCFdpBzzOuRA-9xvCxaMyI12zGUbdGCodxYx1tN9CpwABYWbhKwSbso3QS1zcAj24SIdPnGP3vZ5tDp4M',
    'TAUnique': '%1%enc%3A7EZKNwcZtQelkq8zGrs0%2FVyHEpm0XUU50hMQk%2FSPQ8dd2WxKjWsMvw%3D%3D',
    'TASSK': 'enc%3AAI7M16a2hd0f4Bi7YswMgXxOlEWoO7qyeOWkHvjCfURZntBX%2BptWIXfGPAeYwKHQ9wtjhsv5UYAj3T7LDznuYyvymgNw2%2BG3%2FzMBTG%2FVvKtjV0FG%2FbkbdESsYq7vyWew9w%3D%3D',
    'ServerPool': 'B',
    'PMC': 'V2*MS.3*MD.20220411*LD.20220411',
    'TART': '%1%enc%3ApZKvMxq7NP36bjB3sFUHJJvM9FdhPceBRvp9ImI97M3Q2%2BaCUA1%2B%2BYWN2jyFoQ9OnY8ZtEhTBI0%3D',
    'TATravelInfo': 'V2*A.2*MG.-1*HP.2*FL.3*RS.1',
    'TASID': '3574D39F90FA49B982E1992FBEE2B58B',
    'TAReturnTo': '%1%%2FTravel_Guide-g187147-Paris_Ile_de_France.html',
    'ak_bmsc': '1911306E300DE16F9220B63DFC7BD79C~000000000000000000000000000000~YAAQr2EXAl3qqfl/AQAArkTGGw+zqUYSMkm+JRYikVYd1iqPR96GAvkSGVHwJTSFsYFNquOGzOuhYZWoViI6lpdqNfDbhr8eYVYI2T7qrT86/jRW1Omp7Pzcsif9ag8zqZ0pOl7aOc11odSYRMzeyvUWs+eWrS0qYHDH4W/Z27MedjIDF8b56sO5+VGkYYRUerPdqFSRWSyDu1k59cd/nXF0i5oidgFk+A8iHPmgKSovaOyDtVrsk6hJMwS/CFMnF/bkLLUy6kqeXTRt6idry4p22jXndsTtvj5FjFqOne+/iAF/J0RMbeZDN9yy/3p282epuBAVgSVtCivxh+QvgxcymHkjgLvw5BZUhzJnJrJt1OV2hLTolXEbvKppQSnGxGcjwsCMauugfL7WC4/o',
    '__vt': 'FZncnPmg7vv6X1AQABQCIf6-ytF7QiW7ovfhqc-AvRykGTETsfxZ_2SPun37Zoq6frL-31FD3-18hsFi_Cvv_iFko5fpmSB9OqODRGVJB2_NNh5zYzrwc8y612PfNbONXDhjJjlI1jWja7o5SqSbU8pK',
    'PAC': 'AFUABe20K6ur_pGuswRG_A2nAis-6YOewLmeDXwy_IoTDrDFmcSn12gG23xy8T08vhN0ByuCoBMFq26FHb4hgEfWQ3bs1XHS_u0UQ9Dkg9b0PsaXOsmoev59Jrhn8mwN5-chzgMr7KwYApuf7Jl76g4EVHrDFusjxMy2nEzj7Y7SQJ8ypcUPeoM0mO8EYdqf0g%3D%3D',
    'roybatty': 'TNI1625!AJMaKc5Vd5t6%2BrMmqcPgbTjC2%2FwVMJk%2BHOvM3vWGJsPUgW3zN1LcY2wsXSXLcVf6luEh7VPyoVMX0l4z9fnfccpUIZRPngZKrDIyjBWzbKQB5vbFnWIYAlqD17wbSYc7q8IFk8UIIzT7JOsY2dySieKNdFKjlU8ZUg38x6MlSmSt%2C1',
    'TASession': 'V2ID.3574D39F90FA49B982E1992FBEE2B58B*SQ.7*LS.DemandLoadAjax*GR.50*TCPAR.93*TBR.5*EXEX.4*ABTR.80*PHTB.50*FS.37*CPU.62*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*FA.1*DF.0*TRA.true*LD.187147*EAU._',
    'TAUD': 'LA-1649733593557-1*RDD-1-2022_04_12*LG-2228668-2.1.F.*LD-2228669-.....',
    'bm_sv': '1ACC3F5FD6FF338D6DC6C647A81A9079~LRushzM5bT9y56ZFdrF32yzAuLdo1zmrLcdY/70OcYI5NrblvznAgSF9wDDOZ6V7GBpNpsUO/eZv+Kus4PcF/SIdf47ojl7JPEEmfVpdoqEkfqUfckAwv1DTdXOiT/N+1PNA+I7cH9QTus9crnWg1L4Zi22UbmA0Nc3eg5jtmLY=',
}

headers = {
    'Host': 'www.tripadvisor.com',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'TADCID=S-RCEEVrSy6DkhzNABQCFdpBzzOuRA-9xvCxaMyI12zGUbdGCodxYx1tN9CpwABYWbhKwSbso3QS1zcAj24SIdPnGP3vZ5tDp4M; TAUnique=%1%enc%3A7EZKNwcZtQelkq8zGrs0%2FVyHEpm0XUU50hMQk%2FSPQ8dd2WxKjWsMvw%3D%3D; TASSK=enc%3AAI7M16a2hd0f4Bi7YswMgXxOlEWoO7qyeOWkHvjCfURZntBX%2BptWIXfGPAeYwKHQ9wtjhsv5UYAj3T7LDznuYyvymgNw2%2BG3%2FzMBTG%2FVvKtjV0FG%2FbkbdESsYq7vyWew9w%3D%3D; ServerPool=B; PMC=V2*MS.3*MD.20220411*LD.20220411; TART=%1%enc%3ApZKvMxq7NP36bjB3sFUHJJvM9FdhPceBRvp9ImI97M3Q2%2BaCUA1%2B%2BYWN2jyFoQ9OnY8ZtEhTBI0%3D; TATravelInfo=V2*A.2*MG.-1*HP.2*FL.3*RS.1; TASID=3574D39F90FA49B982E1992FBEE2B58B; TAReturnTo=%1%%2FTravel_Guide-g187147-Paris_Ile_de_France.html; ak_bmsc=1911306E300DE16F9220B63DFC7BD79C~000000000000000000000000000000~YAAQr2EXAl3qqfl/AQAArkTGGw+zqUYSMkm+JRYikVYd1iqPR96GAvkSGVHwJTSFsYFNquOGzOuhYZWoViI6lpdqNfDbhr8eYVYI2T7qrT86/jRW1Omp7Pzcsif9ag8zqZ0pOl7aOc11odSYRMzeyvUWs+eWrS0qYHDH4W/Z27MedjIDF8b56sO5+VGkYYRUerPdqFSRWSyDu1k59cd/nXF0i5oidgFk+A8iHPmgKSovaOyDtVrsk6hJMwS/CFMnF/bkLLUy6kqeXTRt6idry4p22jXndsTtvj5FjFqOne+/iAF/J0RMbeZDN9yy/3p282epuBAVgSVtCivxh+QvgxcymHkjgLvw5BZUhzJnJrJt1OV2hLTolXEbvKppQSnGxGcjwsCMauugfL7WC4/o; __vt=FZncnPmg7vv6X1AQABQCIf6-ytF7QiW7ovfhqc-AvRykGTETsfxZ_2SPun37Zoq6frL-31FD3-18hsFi_Cvv_iFko5fpmSB9OqODRGVJB2_NNh5zYzrwc8y612PfNbONXDhjJjlI1jWja7o5SqSbU8pK; PAC=AFUABe20K6ur_pGuswRG_A2nAis-6YOewLmeDXwy_IoTDrDFmcSn12gG23xy8T08vhN0ByuCoBMFq26FHb4hgEfWQ3bs1XHS_u0UQ9Dkg9b0PsaXOsmoev59Jrhn8mwN5-chzgMr7KwYApuf7Jl76g4EVHrDFusjxMy2nEzj7Y7SQJ8ypcUPeoM0mO8EYdqf0g%3D%3D; roybatty=TNI1625!AJMaKc5Vd5t6%2BrMmqcPgbTjC2%2FwVMJk%2BHOvM3vWGJsPUgW3zN1LcY2wsXSXLcVf6luEh7VPyoVMX0l4z9fnfccpUIZRPngZKrDIyjBWzbKQB5vbFnWIYAlqD17wbSYc7q8IFk8UIIzT7JOsY2dySieKNdFKjlU8ZUg38x6MlSmSt%2C1; TASession=V2ID.3574D39F90FA49B982E1992FBEE2B58B*SQ.7*LS.DemandLoadAjax*GR.50*TCPAR.93*TBR.5*EXEX.4*ABTR.80*PHTB.50*FS.37*CPU.62*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*FA.1*DF.0*TRA.true*LD.187147*EAU._; TAUD=LA-1649733593557-1*RDD-1-2022_04_12*LG-2228668-2.1.F.*LD-2228669-.....; bm_sv=1ACC3F5FD6FF338D6DC6C647A81A9079~LRushzM5bT9y56ZFdrF32yzAuLdo1zmrLcdY/70OcYI5NrblvznAgSF9wDDOZ6V7GBpNpsUO/eZv+Kus4PcF/SIdf47ojl7JPEEmfVpdoqEkfqUfckAwv1DTdXOiT/N+1PNA+I7cH9QTus9crnWg1L4Zi22UbmA0Nc3eg5jtmLY=',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'zh-CN,zh;q=0.9',
}

def write_data(path:str,filename:str,data:str):
    isExists=os.path.exists(path)
    filesisExists=os.path.exists(path+filename)
    if filesisExists:
        filename = "dup" + filename
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(path)
    with open(path+filename, "a") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
            file.write(data + "\n")

response = requests.get('https://www.tripadvisor.com/Travel_Guide-g303506-Rio_de_Janeiro_State_of_Rio_de_Janeir', headers=headers, cookies=cookies,verify=False)
soup = BeautifulSoup(response.text, 'lxml', from_encoding='utf-8')
select = soup.select('#BODYCON > div.modules-triplist-city-page-list > ul > a')
head_select = soup.select('#BODYCON > div.modules-triplist-city-page-featured > a')
head_select2 = soup.select('#BODYCON > div.modules-triplist-city-page-featured > div.side-pane > a')
select.extend(head_select)
select.extend(head_select2)
result_list = list()
i = 0
for a in select:
    i=i+1
    # if i<24:
    #     continue
    response = requests.get('https://www.tripadvisor.com'+a.attrs['href'],
                            headers=headers, cookies=cookies, verify=False)
    result_soup = BeautifulSoup(response.text, 'lxml', from_encoding='utf-8')
    # result = dict()
    extractor = GeneralNewsExtractor()
    html = response.text
    result = extractor.extract(html)
    author = result_soup.select('#BODYCON > div.guide > div.guide-header > div > div.list-hero > div.hero-bottom-container > div.hero-bottom > div > div > p > a > span.name')[0].text.lstrip()
    list_description = result_soup.select('#BODYCON > div.guide > div.guide-header > div > div.list-header-bottom > div.header-main > p')[0].text.lstrip()
    try:
        tips = result_soup.select('#ANCHOR_TIPS > div.tips-container')[0].text.lstrip()
        result['tips'] = tips
    except:
        pass
    index = result_soup.select('#BODYCON > div.guide > div.guide-content > div.guide-content-left > div > div')
    index_list = [a.text.lstrip() for a in index]
    ditail_list = result_soup.select('#ANCHOR_POIS > li')
    content = list()
    for b in ditail_list:
        temp_title = b.select('div.header')[0].text.lstrip()
        temp_author = b.select('div.avatar')[0].text.lstrip()
        temp_content = b.select('div.item-details-content')[0].text.lstrip()
        content.append(temp_title+':'+temp_author + temp_content)
    result['author'] = author
    result['content'] = content
    result['description'] = list_description
    result['index'] = index_list
    result.pop('images')
    result.pop('publish_time')
    write_data('./data/', result['title']+'.txt', json.dumps(result))
    print(i)
    pass
# #BODYCON > div.modules-triplist-city-page-list > ul > a:nth-child(18)

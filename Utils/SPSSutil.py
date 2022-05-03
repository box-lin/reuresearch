import os
import os.path


def get_apkapi(fname_lower)->str:
    api_idx = fname_lower.find("api")
    apkapi = fname_lower[api_idx+3:api_idx+5]
    return apkapi

def get_apktyp(fname_lower)->str:
    keywords = {'benign', 'malware'}
    for word in keywords:
        if fname_lower.find(word) >= 0 :
            return word
    return"Notyp" #this is impossible

def get_apkyear(fname_lower)->str: 
    keywords = set()
    for i in range(2010, 2020):
        keywords.add(str(i))
    for word in keywords:
        if fname_lower.find(word) >= 0:
            return word 
    return "Noyear"

def get_apiyear(apiyear):
    dic = {"19":"2013", "20":"2014", "21":"2014", "22":"2015", "23":"2015", "24":"2016",
           "25": "2016", "26": "2017", "27": "2017", "28":"2018"}
    return dic[apiyear] # impossible keyerror


def get_minSDK_dic(sdk_path):
    apksdk = {}
    for parent,dirnames, filenames in os.walk(sdk_path):
        for fname in filenames:
            fname_lower = fname.lower() 
            address = os.path.join(parent,fname)  
            # read the txt
            f = open(address, 'r')
            info = f.read()
            f.close()
            for line in info.splitlines():
                lst = line.split()
                
                typ = lst[0]
                apkyear = lst[1]
                apkname = lst[2]
                sdk = lst[3]
                
                apksdk[(apkname, apkyear, typ)] = sdk
    return apksdk



# serve for 2018-2019 benign (install and run) and malware installation
def get_dic():
    dic = {}
    apis = [i for i in range(27,18, -1)]
    apis.remove(20)
    # upper level
    for apkyear in range(2018,2020):
        apkyear = str(apkyear)
        # api and apiyear same level
        for api in apis:
            api = str(api)
            apiyear = get_apiyear(api)
            # minsdk the lowest level
            for minsdk in range(0, 29): 
                minsdk = str(minsdk) 
                tupkey = (minsdk, api, apkyear, apiyear)
                dic[tupkey] = [0,0]
    return dic

# apkyear 2010-2019
def get_dic_full():
    dic = {}
    apis = [i for i in range(27,18, -1)]
    apis.remove(20)
    # upper level
    for apkyear in range(2010,2020):
        apkyear = str(apkyear)
        # api and apiyear same level
        for api in apis:
            api = str(api)
            apiyear = get_apiyear(api)
            # minsdk the lowest level
            for minsdk in range(0, 29): 
                minsdk = str(minsdk) 
                tupkey = (minsdk, api, apkyear, apiyear)
                dic[tupkey] = [0,0]
    return dic


"""_take a table with value [#success, #fail] transform to [#total, 0]_
"""
def transform(givenTable):
    table = {}
    for tupkey, stats in givenTable.items():
        sucCnt, failCnt = stats 
        total = sucCnt + failCnt
        table[tupkey] = [total, 0]
    return table


def originalTablePrint(table):
    for lst, stat in table.items():
        sucCnt, failCnt = stat 
        total = sucCnt + failCnt
        failRate = float(failCnt/total) if total != 0 else 0
        print("{}\t Success,Fail: {} failRate: {}".format(lst, stat, failRate)) 

def specificTablePrint(table):
    for lst, stat in table.items():
        total, failCnt = stat 
        failRate = float(failCnt/total) if total != 0 else 0 
        print("{}\t failRate: {}".format(lst, failRate))  

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

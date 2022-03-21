
from BarStatIns import INCOMPAT_MSG


INCOMPAT_MSG_KEYWORDS = {'verifyerror', 'security', 'native', 'nullpointer', 'activitynotfound', 'noclass', 'unsatisfiedlink', 
                         }

def get_year(address):
    name = address.lower()
    bidx = name.find('benign')
    midx = name.find('malware')
    if bidx > 0:
        return name[bidx:bidx+len('benign')+4]
    elif midx > 0:
        if name.find('2018') or name.find('2019'):
            return name[midx:midx+len('malware')+4]
        else:
            year = name[midx:midx+len('malware')+5]
            year.replace('-','')
            return year
    return 'None'

def collect_fail_msg(info, address):
    year = get_year(address)
    paragraphs = info.split('\n\n')
    for line in paragraphs[1].splitlines():
        if line.startswith('Failure'):
            lst = line.split()
            
            msg = lst[1][1:-2]
            cnt = int(lst[2])
            
            if msg in INCOMPAT_MSG:
                # increase the cnt
                try:
                    YEAR_MSG_COUNT[year][msg] += cnt
                # not exit key yet, assign cnt
                except:
                    YEAR_MSG_COUNT[year][msg] = cnt
                    
                YEAR_TOTAL[year] += cnt
                FAIL_MSG.add(msg)

if __name__ == '__main__':
    dir = sys.argv[1]
    for parent, dirnames, filenames in os.walk(dir):
        for fname in filenames:
            address = os.path.join(parent,fname)
            f = open(address, 'r')
            info = f.read()
            f.close()
            collect_fail_msg(info,address)
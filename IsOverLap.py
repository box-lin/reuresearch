import sys
import collections


def is_overlap(apk1, apk2):
    overlap = apk1.intersection(apk2)
    if overlap:
        print("Numbers of overlaps between two files: ", len(overlap))
       
        # enable this if you want to see the overlap apks
        #print("Overlap founded: ", overlap)
    

def contains_dup(apk_lst, fname):
    """[Check if such apk_lst contains duplicates, print some message to console.]

    Args:
        apk_lst ([List]): [List with all apk numbers]
        fname ([string]): [Name of the file]

    Returns:
        [Bool]: [Return true or false]
    """
    len_apk_lst = len(apk_lst)
    len_distinct_apk = len(set(apk_lst))
    
    if len_apk_lst!= len_distinct_apk:
        print(fname + " contains duplicated apks: ", len_apk_lst  - len_distinct_apk)
        dup_freq = collections.Counter(apk_lst)
        dup_lst = []
        for apk, freq in dup_freq.items():
            if freq > 1:
                tup = (apk, freq)
                dup_lst.append(tup)
        # enable this if you want to see detial duplicates
        # print(fname + " duplicates: ", dup_lst)
        return True
    else:
        print(fname + " contains duplicated apks: ",  0)
        return False
        
def get_apks_num(f, fname):
    """[summary]

    Args:
        f ([type]) 
        fname ([string])

    Returns:
        [type]: [description]
    """
    apks = []
    line = f.readline()
    while line:
        if line.startswith('======================================'):
            lst = line.split()
            apks.append(lst[4])
        line = f.readline()
    print(fname + " apks collected, total: ", len(apks))
    return apks

if __name__ == "__main__":
    
    # file1
    fname1 = sys.argv[1]
    f1 = open(fname1,  errors="ignore")
    f1_apks_lst = get_apks_num(f1, fname1)
    contains_dup(f1_apks_lst, fname1)
    
    # file2
    fname2 = sys.argv[2]
    f2 = open(fname2,  errors="ignore")
    f2_apks_lst = get_apks_num(f2, fname2)
    contains_dup(f2_apks_lst, fname2)
    
    # check overlaps
    is_overlap(set(f1_apks_lst), set(f2_apks_lst))

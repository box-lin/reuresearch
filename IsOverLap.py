import sys
import collections


def is_overlap(apk1, apk2):
    overlap = apk1.intersection(apk2)
    if overlap:
        print("Overlap founded: ", overlap)
    

def contains_dup(apk_lst, fname):
    """[Check if such apk_lst contains duplicates, print some message to console.]

    Args:
        apk_lst ([List]): [List with all apk numbers]
        fname ([string]): [Name of the file]

    Returns:
        [Bool]: [Return true or false]
    """
    if len(apk_lst) != len(set(apk_lst)):
        print(fname + " contains duplicated apks: ", len(apk_lst) - len(set(apk_lst)))
        dup_freq = collections.Counter(apk_lst)
        dup_lst = []
        for apk, freq in dup_freq.items():
            if freq > 1:
                tup = (apk, freq)
                dup_lst.append(tup)
        print(fname + " duplicates: ", dup_lst)
        return True
    else:
        print(fname + " it self doesnt have duplicates!")
        return False
        
def get_apks_num(f):
    """[summary]

    Args:
        f ([type]): [description]

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
    return apks

if __name__ == "__main__":
    
    # file1
    fname1 = sys.argv[1]
    f1 = open(fname1,  errors="ignore")
    f1_apks_lst = get_apks_num(f1)
    x = contains_dup(f1_apks_lst, fname1)
    
    # file2
    fname2 = sys.argv[2]
    f2 = open(fname2,  errors="ignore")
    f2_apks_lst = get_apks_num(f2)
    y = contains_dup(f2_apks_lst, fname2)
    

    # if no duplicate in both file, check if overlaps
    if not x and not y:
        is_overlap(set(f1_apks_lst), set(f2_apks_lst))
    else:
        print("Program stopped, since one or more file contains duplicates, you may want to fix it first.")
        
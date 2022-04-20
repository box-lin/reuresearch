""" 
: [Usage] : python parseMinSdk.py folder_address apktype apkyear
  [Args 1]: folder address
  [args 2]: type of apks  e.g. malware or benign
  [Args 3]  year of apks

          -  Traverse through a folder where folder should contain a collections of .apk
          -  Save the result in this format in a txt file
          
          txt file name: apktype-apkyear-minsdk.txt    e.g. malware-2010-minsdk.txt 
          
          txt content:
            apktype apkyear apkname minsdk  
"""

import subprocess
import os, sys

# to make sure apks are distinct 
data = set()

def write():
    os.system("mkdir -p minsdkdata")
    typapk = sys.argv[2]
    apkyear = sys.argv[3]
    txtname = typapk + '-' + apkyear + 'minsdk.txt'
    output = open('./minsdkdata/' + txtname, 'w')
    
    for apkname, minsdklevel in data:
        output.write(typapk + " " + apkyear + " " +  apkname + " " + minsdklevel + "\n")
    output.close()

def main():
    for parent, dirnames, filenames in os.walk(sys.argv[1]):
        for fname in filenames:
            glbl_address = os.path.join(parent, fname)
            # run this apk by: bash getminsdk.sh glbl_address
            cmd = "bash getminsdk.sh " + glbl_address
            try:
                minsdk = str(int(subprocess.check_output(cmd, shell=True),16))
            except:
	        # if the return value is not convertable to int, disregard and continue
                print(glbl_address, "fail getminsdk return:", subprocess.check_output(cmd,shell=True)) 
                continue
            tup = (fname, minsdk)
            data.add(tup)
    write()
    
if __name__ == "__main__":
    main()


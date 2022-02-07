import os
import subprocess
import sys
import re
import collections



def classify(log_address, apk_sdk_dict):

    # Failures in a dict, {failure:{sdk:{apk1, apk2...}}}
    FAILURE = collections.defaultdict(dict)
    SUCCESS = set()
    failure_cnt = 0
    
    def check_install(paragraph):
        lines = paragraph.splitlines()
        # the fist line, 4th index after split is the apk number.
        apk = lines[0].split()[4]


        # look for successful keywords
        A = paragraph.find('Success') >= 0 
        B = paragraph.find('installed successfully') >= 0 and paragraph.find('unnstalled successfully')

        if A and B:
            SUCCESS.add(apk)
            return

        # otherwise look for the failures
        for l in lines:
            fail_idx = l.find('Failure')
            if fail_idx >= 0:
                # strip the failure line
                message = l.strip()
                cursdk = apk_sdk_dict[apk]
                if message not in FAILURE:
                    FAILURE[message] = {cursdk:set(apk)}
                else:
                    if cursdk not in FAILURE[message]:
                        failure_cnt += 1
                        FAILURE[message][cursdk] = set(apk)
                    else:
                        if apk not in FAILURE[message][cursdk]: failure_cnt+=1
                        FAILURE[message][cursdk].add(apk)


    

    f = open(log_address)
    # NOTE split paragraph reference: https://stackoverflow.com/questions/53240763/python-how-to-separate-paragraphs-from-text
    content = f.read().split('\n\n')
    for paragraph in content:
        if paragraph.startswith("====================================== Install INDIVIDUAL APP:"):
            check_install(paragraph)
   
    
    # Write the result and also print to the console.
    successes_cnt = len(SUCCESS)
    total_apk = successes_cnt + failure_cnt

    # BUG these two value not equal if contains duplicate apk
    print(total_apk, len(apk_sdk_dict))


    os.system("mkdir -p installEffect")

    output = open('./installEffect/' + apks_folder + '-res.txt', 'w')

    output.write('======================= ' + apks_folder + '-res.txt' + '=======================')
    print('======================= ' + apks_folder + '-res.txt' + '=======================')


    output.write('In  {}  apps :      successful: {}        failed: {}'.format(str(total_apk), str(successes_cnt), str(failure_cnt)))
    print('In  {}  apps :      successful: {}        failed: {}'.format(str(total_apk), str(successes_cnt), str(failure_cnt)))

    num = 1
    for failure, sdk_apk in FAILURE.items():
        output.write('<{}>   The Effect {}'.format(str(num), failure))
        print('<{}>   The Effect {}'.format(str(num), failure))

        for sdk, apk in sorted(sdk_apk.items()):
            fail_sdk_len = len(val)
            output.write(' --SDK {} : {}'.format(sdk, fail_sdk_len))
            print(' --SDK {} : {}'.format(sdk, fail_sdk_len))
            for item in apk:
                output.write('                   ' + item)
                print('                   ' + item)
        num += 1
    
    output.close()

def file_name(file_dir):
    """
    return a list of apk name from the given directory
    """
    L=[]
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.apk':
                L.append(os.path.join(file))
                # NOTE contains the root folder if needed
                # L.append(os.path.join(root, file))
    return L

def get_all_sdk_from_apk(file_dir, names):
    """ [Returns a dictionary with {apk:sdk}]
    """
    res = {}
    for name in names:
        cmd = './getanysdk.sh ' + file_dir + '/' + name

        # NOTE reference: https://stackoverflow.com/questions/3503879/assign-output-of-os-system-to-a-variable-and-prevent-it-from-being-displayed-on
        # ...\n included must remove \n.
        sdk = subprocess.check_output(cmd, shell=True)
        sdk = sdk[:-1]
        res[name] = int(sdk, 16)
    return res


if __name__ == "__main__":
    
    apks_folder = sys.argv[1]

    # command for run the shell cript to install apk and generate the logs 
    generate installation log
    cmd_install_log = "./installAndroZooApks.sh " + apks_folder 

    # mk directory if needed
    os.system("mkdir -p InstallLog")
    
    # save the log to the directory
    log_address = directory_name + '/' + 'installLog-' + str(apks_folder)
    save_cmd = cmd_install_log + ' > ' + log_address
    os.system(save_cmd)

    # generate dictionary for apk:sdk 
    apk_names = file_name(apks_folder)
    apk_to_sdk = get_all_sdk_from_apk(apks_folder, apk_names)
   
    # classify the installation results from the log.
    classify(log_address, apk_to_sdk)

 

    

    
    
   
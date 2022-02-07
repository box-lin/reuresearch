#!/bin/bash
dataset=$1
avdname=${2:-"Nexus-One-10"}
port=${3:-"5572"}
did="emulator-$port"


timeout() {

    time=$1

    # start the command in a subshell to avoid problem with pipes
    command="/bin/sh -c \"$2\""

    expect -c "set echo \"-noecho\"; set timeout $time; spawn -noecho $command; expect timeout { exit 1 } eof { exit 0 }"    

    if [ $? = 1 ] ; then
        echo "Timeout after ${time} seconds"
    fi

}
tryInstall()
{
    finaldir=$1

    > list.alreadytriedinstall.$cate

    k=1

    bash ./setupEmuSafe.sh $avdname $port
    sleep 3
    #pidemu=`ps axf | grep -v "grep" | grep "$avd -scale .3 -no-boot-anim -no-window -port $port" | awk '{print $1}'`
    pidemu=`ps axf | grep -v "grep" | grep "$avd -scale .3 -port $port" | awk '{print $1}'`

	for fnapk in $finaldir/*.apk;
	do
		if [ `grep -a -c ${fnapk##*/} list.alreadytriedinstall.$cate` -ge 1 ];then
			echo "$fnapk already installed or tried so, skipped."
			continue
		fi

		tgtp=`./getpackage.sh $fnapk | awk '{print $2}'`


		adb -s $did shell pm list packages -3 | cut -d':' -f2 | tr '\r' ' ' | xargs -r -n1 -t adb uninstall
		adb -s $did shell "rm -rf /data/app/*" 1>/dev/null 2>&1
		#rm -rf /home/zyzhang/.android/avd/${avdname}.avd/userdata*
		#rm -rf /home/zyzhang/.android/avd/${avdname}.avd/cache*
		#rm -rf /home/zyzhang/.android/avd/${avdname}.avd/data
		#rm -rf /home/zyzhang/.android/avd/${avdname}.avd/snapshots
		
		echo
		echo "====================================== Install INDIVIDUAL APP: ${fnapk##*/} ==========================="

		#ret=`timeout 120 '~/bin/apkinstall $fnapk $did'`
		ret=`bash ./apkinstall $fnapk $did`
		n1=`echo $ret | grep -a -c "Success"`
		if [ $n1 -lt 1 ];then 
		    echo "installing $fnapk failed. Skipping it"
		    echo "$ret  #"
		    adb -s $did shell "pm uninstall $tgtp" 1>/dev/null 2>&1
		    adb -s $did shell "rm -rf /data/app/${tgtp}*" 1>/dev/null 2>&1
		    continue
		fi
		
		echo "$fnapk installed successfully; now uninstall it"
		bash ./apkuninstall $fnapk $did
		#ret=`~/bin/apkuninstall $fnapk $did`
		#n1=`echo $ret | grep -a -c "Success"`

#		if [ $n1 -lt 1 ];then 
#		    echo "uninstalling $fnapk failed. Skipping it"
#		    echo "$ret"
#		    adb -s $did shell "pm uninstall $tgtp" 1>/dev/null 2>&1
#		    adb -s $did shell "rm -rf /data/app/${tgtp}*" 1>/dev/null 2>&1
#		    continue
#		fi

		#adb -s $did shell "pm uninstall $tgtp" 1>/dev/null 2>&1
		#adb -s $did shell "rm -rf /data/app/${tgtp}*" 1>/dev/null 2>&1
		echo "$fnapk unnstalled successfully"
		#echo

		echo "${fnapk##*/}" >> list.alreadytriedinstall.$cate
	done
	kill -9 $pidemu

    #pidavd=`ps axf | grep -v "grep" | grep "$avd -scale .3 -port $port" | awk '{print $1}'`
	#kill -9 $pidavd
	
}

for cate in "$dataset"
    do
        c=0
        echo "================================="
        echo "=================================try installing dataset: $cate"
        echo "================================="
        echo
        echo

        tryInstall $cate
    done
exit 0

#!/bin/bash

for i in "$@"
do
	#echo -e $i"\t"
	out1=`aapt list -a $i | grep targetSdk`
	if [ `echo ${out1} | grep -a -c "Sdk"` -lt 1 ];then
        out2=`aapt list -a $i | grep minSdkVersion`
        if [ `echo ${out2} | grep -a -c "Sdk"` -lt 1 ];then
            echo 0
        else
            echo ${out2##*)}
        fi
    else
        echo ${out1##*)}
	fi
done
exit 0

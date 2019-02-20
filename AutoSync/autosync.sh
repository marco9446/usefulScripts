#!/bin/bash


local_rp=~/RavazDrive/
external_rp="/Volumes/RavazPortable/RavazDrive/"

local_rk=~/RavazDrive/Ravaz_key/
external_rk="/Volumes/RAVA_KEY/"

exitcode=1 
#do check if usb flash is mounted

function notify {
    /usr/local/bin/terminal-notifier -message "$2" -title "$1";
}

if test -e $external_rp ;then 
    exitcode=0
    notify '🔄 Sicronization started' 'Start syncronizing RavazPortable'
    /usr/local/bin/unison  -batch -ignore="Path .DS_Store"  $local_rp $external_rp -fat ;
    date > ${external_rp}last_syncronization.txt
    notify '✅ Sicronization finished' 'Stop syncronizing RavazPortable'
fi 

if test -e $external_rk ;then 
    exitcode=0
    notify '🔄 Sicronization started' 'Start syncronizing Ravaz_Key'
    /usr/local/bin/unison  -batch -ignore="Path .DS_Store"  $local_rk $external_rk -fat ;
    rsync -u ~/RavazDrive/DocumentsCrypt $external_rk;
    date > ${external_rk}last_syncronization.txt
    notify '✅ Sicronization finished' 'Stop syncronizing Ravaz_Key'
fi 

#if the flash is not mounted exit with exitcode=1 
exit $exitcode

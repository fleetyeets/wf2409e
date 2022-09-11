['netis(WF2409E)'] $> cat /bin/russia_storage.sh
[+] cat /bin/russia_storage.sh Payload sent
["SUCCESS"]
[+] Getting output...
#!/bin/sh
FTPD_FILE=/var/stupid-ftpd.conf
PART1=""


eval `flash get USER_NAME`
eval `flash get USER_PASSWORD`

if [ "$1" = "commftp" ]
then

\teval `flash get FTP_SERVER_ENABLE`
\tif [ "$FTP_SERVER_ENABLE" = "0" ]
then
\t\t#umount /var/sys
\t\tkillall stupid-ftpd
\t\texit 0
\tfi

        PART1=""

        for part in a b c d e f g h i j k l m n o p q r s t u v w x y z
        do
                for index in 0 1 2 3 4 5 6 7 8 9
                do
\t\t\t\t\t\t#add by liuai for debug SSK.
\t\t\t\t\t\tif [ $index = 0 ]
then
\t\t\t\t\t\t\tppart=$part
\t\t\t\t\t\telse
\t\t\t\t\t\t\tppart=$part$index
\t\t\t\t\t\tfi
                        if [ -e "/var/sd$ppart" ]
then
                                PART1="/var/sd$ppart"_dir
                                MOUNT_DISK=`cat /proc/mounts |grep "$PART1"`
                                if [ "$MOUNT_DISK" != "" ]
then
                                        break

                                fi
                        fi
                done
                if [ "$PART1" != "" ]
 then
                        break

                fi
        done
\tif [ "$PART1" = "" ]
 then
               exit 0\t\t
        fi
        killall stupid-ftpd
        #echo "mode=demon" >$FTPD_FILE
        #echo "serverroot=/bin/stupid-ftpd" >>$FTPD_FILE
        #echo "changeroottype=real" >>$FTPD_FILE
        #echo "maxusers=2" >>$FTPD_FILE
        #echo "log=/var/ftp_log" >>$FTPD_FILE
        #echo "login-timeout=30" >>$FTPD_FILE
        #echo "timeout=3000" >>$FTPD_FILE
        #echo "banmsg=Go away !" >>$FTPD_FILE
        #eval `flash get WEBHARD_FTPPORT`
       # if [ -e "$PART1" ]
then
\t/bin/stupid-ftpd-common.sh 21 9 300 300
\t/bin/stupid-ftpd-user.sh "$PART1" 9 A
\t/bin/stupid-ftpd -f "$FTPD_FILE"
        #fi
        exit 0


fi


if [ "$1" = "mount" ]
then
\t#killall udp_mount
        /bin/mount -t sysfs none /sys
        echo "/bin/igd_hotplug" > /proc/sys/kernel/hotplug
         if [ -e "/bin/udp_mount" ]
then
\t\tkillall udp_mount
\t\tudp_mount &
\t\techo " already run udp_mount,it \'s ok ...."
\tfi
\texit 0
fi

if [ "$1" = "kill-unmount" ]
then
\t/bin/checkmount.sh
\texit 0
fi

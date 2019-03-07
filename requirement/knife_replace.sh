#!/usr/bin/bash
Author=central

ps_path=/ffs/run/boardcfg/0/B/mcu-fctl/addons/l2-ps.tgz
ps_631_path=/ffs/run/boardcfg/1/A/mcu-aspa/addons/l2-ps.tgz
lo_path=/ffs/run/boardcfg/0/B/mcu-fctl/addons/l2-lo.tgz
lo_631_path=/ffs/run/boardcfg/1/A/mcu-aspa/addons/l2-lo.tgz
cprt_path=/ffs/run/boardcfg/0/A/mcu-fctl/addons/cp-rt.tgz
ndoeoam_path=/ffs/run/boardcfg/0/A/mcu-fctl/addons/CloudNodeOam.tgz
profile_path=/opt/nokia/SS_MzOam/cloud-siteoam/siteoam/profiles/5G18A/
cp_cl_path=/opt/nokia/SS_CPLANE/bin/cp_cl
cp_nb_path=/opt/nokia/SS_CPLANE/bin/cp_nb
cp_if_path=/opt/nokia/SS_CPLANE/bin/cp_if
cp_ue_path=/opt/nokia/SS_CPLANE/bin/cp_ue
test_path=/tmp/b.a

function replace(){
	echo "your current $1 md5 value is: "
	md5sum $2
	echo "new $1 md5 value is: "
	md5sum $1
	cp $1 $2
	echo "crasign ing..."
	crasign $2
	echo "crasign done"
	echo "after replace your package, md5 value is: "
	md5sum $2
}	

function Cprt(){
	mkdir /tmp/cp
	tar zxvf /ffs/run/boardcfg/0/A/mcu-fctl/addons/cp-rt.tgz -C /tmp/cp
	echo "your old Cprt md5 value is: "
	md5sum /tmp/cp/opt/cp-rt/Cprt
	echo "new Cprt md5 is: "
	md5sum $1
	cp $1 /tmp/cp/opt/cp-rt/Cprt
	echo "after replace Cprt, md5 is: "
	md5sum /tmp/cp/opt/cp-rt/Cprt
	cd /tmp/cp
	tar zcvf cp-rt.tgz *
	echo "and cp-rt.tgz md5 is: "
	md5sum cp-rt.tgz
	cp cp-rt.tgz /user/toor4nsn/
	echo "cp-rt.tgz under ~ is: "
	md5sum /user/toor4nsn/cp-rt.tgz


}
function cu_cp(){
	echo "start to replace your $1"
	echo "echo your current \$2 md5 value is: ">>aa.sh
	echo "md5sum \$2">>aa.sh
	echo "echo new \$1 md5 value is: ">>aa.sh
	echo "md5sum \$1 ">>aa.sh 
	echo "cp \$1 \$2">>aa.sh
	echo "echo after replace your \$1, md5 value is: ">>aa.sh
	echo "md5sum \$2">>aa.sh
	echo "sudo chown root:root \$2">>aa.sh
	echo "sudo chmod +x \$2">>aa.sh
	echo "ls -alh \$2">>aa.sh

	
}
function backup_du(){
        echo "you are going to backup $1"
	if [ ! -x "/user/toor4nsn/backupdu" ]; then
        	mkdir ~/backupdu
	fi
	echo "backuping..."
	cp $1 ~/backupdu/
	echo "done. please find your backup $1 under /user/toor4nsn/backupdu/ "

}

function usage(){
	echo "###################################################################################"
	echo "usage: bash knife_replace.sh package_name option"
	echo "for du example: bash knife_replace.sh l2-lo.tgz lo"
	echo "for cu example: bash knife_replace.sh cp_if cpif"
	echo "for backup example: bash knife_replace.sh a bkps"
	echo "==================================================================================="
	echo "-h help    :usage  "
	echo "lo         :replace lo at /ffs/run/boardcfg/0/B/mcu-fctl/addons/l2-lo.tgz"
	echo "lo631      :replace lo at /ffs/run/boardcfg/1/A/mcu-aspa/addons/l2-lo.tgz"
	echo "ps         :replace ps at /ffs/run/boardcfg/0/B/mcu-fctl/addons/l2-ps.tgz "
	echo "ps631      :replace ps at /ffs/run/boardcfg/1/A/mcu-aspa/addons/l2-ps.tgz"
	echo "cprt       :replace cprt at /ffs/run/boardcfg/0/A/mcu-fctl/addons/cp-rt.tgz"
	echo "cpcl    	 :replace cpcl at /opt/nokia/SS_CPLANE/bin/cp_cl"
	echo "cpif    	 :replace cpif at /opt/nokia/SS_CPLANE/bin/cp_if"
	echo "cpnb    	 :replace cpnb at /opt/nokia/SS_CPLANE/bin/cp_nb"
	echo "cpue    	 :replace cpue at /opt/nokia/SS_CPLANE/bin/cp_ue"
	echo "profile    :replace profile at /opt/nokia/SS_MzOam/cloud-siteoam/siteoam/profiles/5G18A/"
	echo "bklo       :backup  for /ffs/run/boardcfg/1/A/mcu-aspa/addons/l2-lo.tgz"
	echo "bkps       :backup  for /ffs/run/boardcfg/1/A/mcu-aspa/addons/l2-ps.tgz"
	echo "bkcprt     :backup  for /ffs/run/boardcfg/0/A/mcu-fctl/addons/cp-rt.tgz"   
	echo "cp         :replace Cprt bin file"
	echo "###################################################################################"
}

case $2 in 
    -h|help )
		usage
		exit 0;
		;;
    lo )
		replace $1 $lo_path
		;;
	lo631 )
		replace $1 $lo_631_path
		;;
    ps )
		replace $1 $ps_path
		;;
	ps631 )
		replace $1 $ps_631_path
		;;
    cprt )
		replace $1 $cprt_path
		;;
    nodeoam )
		replace $1 $ndoeoam_path
		;;
    -t )
		test_cu_cp $1 $test_path
		scp aa.sh $1 cpif-0.local:/home/robot/
		ssh cpif-0.local " sh aa.sh $1 $test_path   && exit"
		rm aa.sh
		;;
	cpcl )
		cu_cp $1 $cp_cl_path
		scp aa.sh $1 cpcl-0.local:/home/robot/
		ssh cpcl-0.local " sh aa.sh $1 $cp_cl_path && exit"
		rm aa.sh
		;;
	cpif )
		cu_cp $1 $cp_if_path
		scp aa.sh $1 cpif-0.local:/home/robot/
		ssh cpif-0.local " sh aa.sh $1 $cp_if_path && exit"
		rm aa.sh
		;;
	cpnb )
		cu_cp $1 $cp_nb_path
		scp aa.sh $1 cpnb-0.local:/home/robot/
		ssh cpnb-0.local " sh aa.sh $1 $cp_nb_path && exit"
		rm aa.sh
		;;
	cpue )
		cu_cp $1 $cp_ue_path
		scp aa.sh $1 cpue-0.local:/home/robot/
		ssh cpue-0.local " sh aa.sh $1 $cp_ue_path && exit"
		rm aa.sh
		;;
	profile )
		replace $1 $profile_path$1
		;;
	bkps )
		backup_du $ps_631_path
		;;
	bklo )
		backup_du $lo_631_path
		;;
	bkcprt )
		backup_du $cprt_path
		;;
	cp )
		Cprt $1
		;;
    * )
	usage
	;;
esac

    

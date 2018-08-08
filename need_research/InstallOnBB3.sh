#!/bin/bash

package_name=$2
version=$1
image_name=RCP2.0_BB3_Image_$version

function kill_current_session()
{
    echo "@@ Kill current session to exit Controller. "
    session_id=`tty`
    echo $session_id
    echo ${session_id#/dev/}
    pkill -9 -t ${session_id#/dev/}

}
source /opt/backups/CN2_SG01_RCP_CI/cn2sg01rcpcirc/cn2sg01rcpcirc

echo "@@ Delete image with same name first."
image_list=`openstack image list | grep RCP2.0_BB3_Image_ | awk '{print $2}'`
echo $image_list
arr=$(echo $image_list|tr " " "\n")
for image_tmp in $arr; do
    echo "Delete exist image: "$image_tmp
    rsl=`openstack image delete $image_tmp`
    echo "====delete image rst==$rsl=="
    sleep 10s
done

echo "@@ Start create new BB3 image."
cd /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/
ls
env |grep USER
echo "@@ openstack image create --disk-format=qcow2 --container-format=bare $image_name  --file=$package_name"

openstack image create --disk-format=qcow2 --container-format=bare $image_name  --file=$package_name
sleep 20s
echo "---wait 20s after new image created---"

image_status=`openstack image list | grep $image_name | awk '{print $6}'`
while [ "$image_status" != "active" ]
do
    echo "@@ Image is under creating,please wait.... "
    sleep 30s
    image_status=`openstack image list | grep $image_name | awk '{print $6}'`
    echo $image_status
    echo "---image status---"
done

echo "@@ Check the new image is created successfully. "
openstack image list

echo "@@ change image name in evn file"
#sed -i "s/image: .*/image: $image_name/g" /home/unit_4/menhe/rcp/SCT_Heat_Files/HeatTemplates/5gbts_heat.env
sed -i "s/image: .*/image: $image_name/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_heat.env
sed -i "s/image: .*/image: $image_name/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_heat.env
sed -i "s/image: .*/image: $image_name/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_heat.env

echo "@@ modify 5gbts_ext_net.env in 5G18A"
sed -i "s/vnf_name: .*/vnf_name: test-548/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_ext_net.env
sed -i "/- name: oam/,+8 d" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_ext_net.env
sed -i "s/number_of_networks: .*/number_of_networks: 2/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_ext_net.env
#sed -i "s/cidr: 10.106.240.72\/29/cidr: 10.106.240.73\/29/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_ext_net.env
sed -i "s/sid: 2324/sid: 3022/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_ext_net.env
sed -i "s/provider: physnet1/provider: physnet-1/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_ext_net.env
sed -i "s/sid: 2306/sid: 2210/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_ext_net.env
sed -i "s/provider: physnet0/provider: physnet-0/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_ext_net.env

echo "@@ modify 5gbts_ext_net.env in 5G18ASA"
sed -i "s/vnf_name: .*/vnf_name: test-548/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_ext_net.env
sed -i "/- name: oam/,+8 d" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_ext_net.env
sed -i "s/number_of_networks: .*/number_of_networks: 2/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_ext_net.env
#sed -i "s/cidr: 10.106.240.72\/29/cidr: 10.106.240.73\/29/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_ext_net.env
sed -i "s/sid: 2324/sid: 3022/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_ext_net.env
sed -i "s/sid: 2306/sid: 2210/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_ext_net.env

echo "@@ modify 5gbts_ext_net.env in 5G19"
sed -i "s/vnf_name: .*/vnf_name: test-683/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_ext_net.env
sed -i "/- name: oam/,+8 d" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_ext_net.env
sed -i "s/number_of_networks: .*/number_of_networks: 8/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_ext_net.env
sed -i "s/sid: 1310/sid: 3022/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_ext_net.env
sed -i "s/provider: physnet0/provider: physnet-1/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_ext_net.env
sed -i "s/sid: 1311/sid: 3023/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_ext_net.env
#sed -i "s/provider: physnet0/provider: physnet-1/" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_ext_net.env
sed -i "s/sid: 1312/sid: 3024/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_ext_net.env
#sed -i "s/provider: physnet0/provider: physnet-1/" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_ext_net.env
sed -i "s/sid: 1313/sid: 3686/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_ext_net.env
#sed -i "s/provider: physnet0/provider: physnet-1/" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_ext_net.env
sed -i "s/sid: 1314/sid: 3687/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_ext_net.env
#sed -i "s/provider: physnet0/provider: physnet-1/" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_ext_net.env
sed -i "s/sid: 1315/sid: 2210/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_ext_net.env
sed -i "69s/provider: physnet-1/provider: physnet-0/" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_ext_net.env
sed -i "s/sid: 1316/sid: 2211/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_ext_net.env
sed -i "79s/provider: physnet-1/provider: physnet-0/" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_ext_net.env
sed -i "s/sid: 1317/sid: 2212/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_ext_net.env
sed -i "89s/provider: physnet-1/provider: physnet-0/" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_ext_net.env

echo "@@ modify 5gbts_heat.env in 5G18A"
sed -i "s/vnf_name: .*/vnf_name: test-548/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_heat.env
sed -i "s/oam_network: .*/oam_network: b20b7b52-c197-4380-8942-bd0ac9941c2a/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_heat.env
sed -i "s/oam_ip: .*/oam_ip: 10.57.207.20/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_heat.env
sed -i "s/_nokadmin: .*/_nokadmin: \!/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_heat.env
sed -i "s/_nokfsoperator: .*/_nokfsoperator: \!/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_heat.env
sed -i "s/root: .*/root: \!/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_heat.env
sed -i "s/oam: .*/oam: 5gbts_548_oam/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_heat.env
sed -i "s/cpcn: .*/cpcn: 5gbts_548_cpcn/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_heat.env
sed -i "s/cpif: .*/cpif: 5gbts_548_cpif/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_heat.env
sed -i "s/cpcl: .*/cpcl: 5gbts_548_cpcl/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_heat.env
sed -i "s/cpnb: .*/cpnb: 5gbts_548_cpnb/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_heat.env
sed -i "s/cpue: .*/cpue: 5gbts_548_cpue/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_heat.env
sed -i "s/upue: .*/upue: 5gbts_548_upue/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_heat.env
sed -i "s/uvm: .*/uvm: 5gbts_548_uvm/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_heat.env
sed -i "s/db: .*/db: 5gbts_548_db/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_heat.env
sed -i "s/internal_provider_networks: physnet0/internal_provider_networks: physnet-0/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_heat.env


echo "@@ modify 5gbts_heat.env in 5G18ASA"
sed -i "s/vnf_name: .*/vnf_name: test-548/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_heat.env
sed -i "s/oam_network: .*/oam_network: b20b7b52-c197-4380-8942-bd0ac9941c2a/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_heat.env
sed -i "s/oam_ip: .*/oam_ip: 10.57.207.20/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_heat.env
sed -i "s/_nokadmin: .*/_nokadmin: \!/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_heat.env
sed -i "s/_nokfsoperator: .*/_nokfsoperator: \!/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_heat.env
sed -i "s/root: .*/root: \!/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_heat.env
sed -i "s/oam: .*/oam: 5gbts_548_oam/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_heat.env
sed -i "s/cpcn: .*/cpcn: 5gbts_548_cpcn/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_heat.env
sed -i "s/cpif: .*/cpif: 5gbts_548_cpif/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_heat.env
sed -i "s/cpcl: .*/cpcl: 5gbts_548_cpcl/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_heat.env
sed -i "s/cpnb: .*/cpnb: 5gbts_548_cpnb/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_heat.env
sed -i "s/cpue: .*/cpue: 5gbts_548_cpue/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_heat.env
sed -i "s/upue: .*/upue: 5gbts_548_upue/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_heat.env

echo "@@ modify 5gbts_heat.env in 5G19"
sed -i "s/vnf_name: .*/vnf_name: test-683/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_heat.env
sed -i "s/oam_network: .*/oam_network: b20b7b52-c197-4380-8942-bd0ac9941c2a/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_heat.env
sed -i "s/oam_ip: .*/oam_ip: 10.57.207.20/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_heat.env
sed -i "s/_nokadmin: .*/_nokadmin: \!/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_heat.env
sed -i "s/_nokfsoperator: .*/_nokfsoperator: \!/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_heat.env
sed -i "s/root: .*/root: \!/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_heat.env
sed -i "s/oam: .*/oam: 5gbts_683_oam/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_heat.env
sed -i "s/cpcn: .*/cpcn: 5gbts_683_cpcn/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_heat.env
sed -i "s/cpif: .*/cpif: 5gbts_683_cpif/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_heat.env
sed -i "s/cpcl: .*/cpcl: 5gbts_683_cpcl/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_heat.env
sed -i "s/cpnrt: .*/cpnrt: 5gbts_683_cpnrt/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_heat.env
sed -i "s/cpnb: .*/cpnb: 5gbts_683_cpnb/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_heat.env
sed -i "s/cpue: .*/cpue: 5gbts_683_cpue/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_heat.env
sed -i "s/upue: .*/upue: 5gbts_683_upue/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_heat.env
sed -i "s/uvm: .*/uvm: 5gbts_683_uvm/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_heat.env
sed -i "s/db: .*/db: 5gbts_683_db/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_heat.env
sed -i "s/internal_provider_networks: physnet0/internal_provider_networks: physnet-0/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_heat.env
sed -i "s/internal_e1_provider_networks: physnet0/internal_e1_provider_networks: physnet-0/g" /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_heat.env

cp /opt/backups/CN2_SG01_RCP_CI/envfiles/5grac.env /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/
cp /opt/backups/CN2_SG01_RCP_CI/envfiles/01.env /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/
#cp /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_heat.env /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_heat_zone.env
cp /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_heat.yaml /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_heat_zone.yaml
sed -i '$a\  availability-zone: reserve' /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_heat.env
#sed -i '$a\  availability-zone: zone_test' /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_heat_zone.env
#sed -i 's/default: "nova"/default: "zone_test"/g' /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18A/5gbts_heat_zone.yaml

cp /opt/backups/CN2_SG01_RCP_CI/envfiles/5grac.env /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/
cp /opt/backups/CN2_SG01_RCP_CI/envfiles/01.env /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/
#cp /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_heat.env /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_heat_zone.env
cp /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_heat.yaml /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_heat_zone.yaml
sed -i '$a\  availability-zone: reserve' /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_heat.env
#sed -i '$a\  availability-zone: zone_test' /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_heat_zone.env
sed -i 's/default: "nova"/default: "zone_test"/g' /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_heat_zone.yaml

cp /opt/backups/CN2_SG01_RCP_CI/envfiles/5grac_683.env /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/
cp /opt/backups/CN2_SG01_RCP_CI/envfiles/01.env /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/
#sed -i '$a\  availability-zone: reserve' /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_heat.env
#cp /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_heat.env /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_heat_zone.env
cp /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_heat.yaml /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_heat_zone.yaml
#sed -i '$a\  availability-zone: zone_test' /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G18ASA/5gbts_heat_zone.env
sed -i 's/default: "nova"/default: "zone_test"/g' /opt/backups/CN2_SG01_RCP_CI/InstallBB3/target/HeatTemplates/NCIR/5G19/5gbts_heat_zone.yaml

source /opt/backups/CN2_SG01_RCP_CI/cn2sg01rcpcirc/cn2sg01rcpcirc

echo "@@ Start to delete stack sequence like this: 1)delete 5GRAC Stack--> 2)delete ext_net Stack --> 3)delete flavor Stack ."
echo "@@ Existing 5GRAC Stack name is: "
stack_name=`openstack stack list |grep "stack_*" | awk '{print $4}'`
echo $stack_name
stack_old_status=`openstack stack list | grep $stack_name | awk '{print $6}'`

if [[ -n $stack_name ]]; then
    echo "@@ Start delete the existing 5GRAC stack. "
    env |grep USER
    openstack stack delete --yes $stack_name
    delete_status=`openstack stack list | grep $stack_name | awk '{print $6}'`
    while [ "$delete_status" == "DELETE_IN_PROGRESS" ] 
    do
        echo "@@ 5GRAC Stack is under deleting,please wait.... "
        sleep 30s
        delete_status=`openstack stack list | grep $stack_name | awk '{print $6}'`
        echo $delete_status
        echo "----" 
    done
    delete_status=`openstack stack list | grep $stack_name | awk '{print $6}'`
    echo "--The delete_status is--"
    echo $delete_status
    if [[ -z "$delete_status" ]];then
        echo "@@ Delete 5GRAC Stack Successfully. "
    elif [ "$delete_status" == "DELETE_FAILED" ];then
        echo "@@ Delete 5GRAC Stack Failed,we will do delete once again. "
        openstack stack delete --yes $stack_name
        sleep 30s
    else
        echo "@@ Delete 5GRAC Stack Failed,the Stack status cannot be recognized,we will do delete once again.. "
        openstack stack delete --yes $stack_name
        sleep 30s
    fi
    echo "@@ Re-Check the stack list whether is empty. "
  openstack stack list

else
    echo "@@ No 5GRAC stack exist. "
fi
echo "-----done 5GRAC Stack delete.-----"

echo "@@ Existing ext_net Stack name is: "
ext_net_name=`openstack stack list | grep "ext_net_*" |  awk '{print $4}'`
echo $ext_net_name

if [[ -n $ext_net_name ]]; then
    echo "@@ Start delete the existing ext_net stack. "
    openstack stack delete --yes $ext_net_name

    delete_status=`openstack stack list | grep $ext_net_name | awk '{print $6}'`
    while [ "$delete_status" == "DELETE_IN_PROGRESS" ] 
    do
        echo "@@ ext_net Stack is under deleting,please wait.... "
        sleep 30s
        delete_status=`openstack stack list | grep $ext_net_name | awk '{print $6}'`
        echo $delete_status
        echo "----" 
    done
    delete_status=`openstack stack list | grep $ext_net_name | awk '{print $6}'`
    echo "--The delete_status is--"
    echo $delete_status
    if [[ -z "$delete_status" ]];then
        echo "@@ Delete ext_net Stack Successfully. "
    elif [ "$delete_status" == "DELETE_FAILED" ];then
        echo "@@ Delete ext_net Stack Failed,we will do delete once again. "
        openstack stack delete --yes $ext_net_name
        sleep 30s
    else
        echo "@@ Delete flavor Stack Failed,the Stack status cannot be recognized,we will do delete once again.. "
        openstack stack delete --yes $ext_net_name
        sleep 30s
    fi
        
    echo "@@ Re-Check the stack list whether is empty. "
    openstack stack list

else
    echo "@@ No ext_net stack exist. "
fi
echo "-----done ext_net Stack delete.-----"


echo "@@ Existing flavors Stack name is: "
flavor_name=`openstack stack list | grep "flavor_*" |  awk '{print $4}'`
echo $flavor_name

if [[ -n $flavor_name ]]; then
    echo "@@ Start delete the existing flavor stack. "
    openstack stack delete --yes $flavor_name

    delete_status=`openstack stack list | grep $flavor_name | awk '{print $6}'`
    while [ "$delete_status" == "DELETE_IN_PROGRESS" ] 
    do
        echo "@@ flavor Stack is under deleting,please wait.... "
        sleep 30s
        delete_status=`openstack stack list | grep $flavor_name | awk '{print $6}'`
        echo $delete_status
        echo "----" 
    done
    delete_status=`openstack stack list | grep $flavor_name | awk '{print $6}'`
    echo "--The delete_status is--"
    echo $delete_status
    if [[ -z "$delete_status" ]];then
        echo "@@ Delete flavor Stack Successfully. "
    elif [ "$delete_status" == "DELETE_FAILED" ];then
        echo "@@ Delete flavor Stack Failed,we will do delete once again. "
        openstack stack delete --yes $flavor_name
        sleep 30s
    else
        echo "@@ Delete flavor Stack Failed,the Stack status cannot be recognized,we will do delete once again.. "
        openstack stack delete --yes $flavor_name
        sleep 30s
    fi
        
    echo "@@ Re-Check the stack list whether is empty. "
    openstack stack list

else
    echo "@@ No Flavor stack exist. "
fi
echo "-----done flavor Stack delete.-----"

session_id=`tty`
echo $session_id
echo ${session_id#/dev/}
pkill -9 -t ${session_id#/dev/}

exit

#2018-02-24 created by Yang Liyong A
#2018-10-29 modify by Wang jianfeng ,chang to Configerparse and Enum

from enum import Enum,unique
from ssh_yly_new import *


class HW_IP(Enum):
    gNB_Asik_SSHInfo = eval(get_configInfo("HW info", "ASIK"))
    gNB_OAM_SSHInfo = eval(get_configInfo("HW info", "OAM"))
    RRU = eval(get_configInfo("HW info", "RRU"))
    LTEemu = eval(get_configInfo("HW info", "LTEemu"))
    EPC = eval(get_configInfo("HW info", "EPC"))
    ASIK = gNB_Asik_SSHInfo["ip"]
    OAM = gNB_OAM_SSHInfo["ip"]
    ABIL1_XEON_A = get_configInfo("HW info", "ABIL1_XEON_A")
    ABIL1_XEON_B = get_configInfo("HW info", "ABIL1_XEON_B")
    ABIL1_Loner = get_configInfo("HW info", "ABIL1_Loner")
    ABIL2_XEON_A = get_configInfo("HW info", "ABIL2_XEON_A")
    ABIL2_XEON_B = get_configInfo("HW info", "ABIL2_XEON_B")
    ABIL2_Loner = get_configInfo("HW info", "ABIL2_Loner")
    UPUE = get_configInfo("HW info", "UPUE")
    CPIF = get_configInfo("HW info", "CPIF")
    CPCL = get_configInfo("HW info", "CPCL")
    CPUE = get_configInfo("HW info", "CPUE")
    CPNB = get_configInfo("HW info", "CPNB")

    ASIK_DEFAULT = get_configInfo('ASIK Log','ASIK_DEFAULT')
    NODEOAM = get_configInfo('ASIK Log','NODEOAM')
    OAMAGENT = get_configInfo('ASIK Log','OAMAGENT')
    CPRT = get_configInfo('ASIK Log','CPRT')
    JOUR = get_configInfo('ASIK Log', 'JOUR')
    SLAVE = get_configInfo('ASIK Log', 'SLAVE')
    SLAVE2 = get_configInfo('ASIK Log', 'SLAVE2')
    L2LO1 = get_configInfo('ASIK Log', 'L2LO1')
    L2LO2 = get_configInfo('ASIK Log', 'L2LO2')
    ASIKL2L1 = get_configInfo('ASIK Log', 'ASIKL2L1')
    SYSCOM = get_configInfo('Platform Log', 'SYSCOM')
    CPRT = get_configInfo('ASIK Log', 'CPRT')


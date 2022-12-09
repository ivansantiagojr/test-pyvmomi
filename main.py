from pyVmomi import vim
from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
import argparse
import atexit
import ssl


context = ssl._create_unverified_context()


def validate_options():
    parser = argparse.ArgumentParser(description="Input parameters")
    parser.add_argument(
        "-s", "--source_host", dest="shost", help="The ESXi source host IP"
    )
    parser.add_argument("-u", "--username", dest="username", help="The ESXi username")
    parser.add_argument(
        "-p", "--password", dest="password", help="The ESXi host password"
    )

    args = parser.parse_args()

    return args


def main():
    opts = validate_options()
    si = SmartConnect(
        host=opts.shost, user=opts.username, pwd=opts.password, sslContext=context
    )

    atexit.register(Disconnect, si)

    content = si.RetrieveContent()

    hostid = si.content.rootFolder.childEntity[0].hostFolder.childEntity[0].host[0]
    hardware = hostid.hardware
    cpuobj = hardware.cpuPkg[0]

    print(
        f"The CPU vendor is {cpuobj.vendor} and the model is{cpuobj.description}")

    systemInfo = hardware.systemInfo

    print(f"The server hardware is {systemInfo.vendor} {systemInfo.model}")

    memoryInfo = hardware.memorySize

    print(f"The memory size is {(memoryInfo) / (1024 * 1024 * 1024)} GB" )


if __name__ == "__main__":

    main()

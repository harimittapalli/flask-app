import re, os, requests, urllib3

http = urllib3.PoolManager()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
username='snow-user-name'
password='snow-passwd'


def nagios_stat(host):
    #nagios URL with API Key update it with ur URL and API key
    nagios_url="https://nagios-host/nagiosxi/api/v1/objects/hoststatus?apikey=yourapikey&pretty=1&name=lk:"
    host = host
    url=nagios_url+host
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    response = requests.get(url, headers=headers, verify=False)
    nag_data = response.json()
    return nag_data

def nagios_stat_ip(host):
    nagios_url="https://nagios-host/nagiosxi/api/v1/objects/hoststatus?apikey=yourapikey&pretty=1&address="
    host = host
    url=nagios_url+host
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    response = requests.get(url, headers=headers, verify=False)
    nag_data = response.json()
    return nag_data

def status(host):
    #SNOW URL change instance with ur snow instance name
    url = 'https://instance.service-now.com/api/now/table/cmdb_ci?sysparm_display_value=true&name='
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    host = host.strip()
    host_name=host
    url = url + host_name
    response = requests.get(url, auth=(username, password), headers=headers)
    data = response.json()
    return data

def status_ip(host):
    url = 'https://instance.service-now.com/api/now/table/cmdb_ci?sysparm_display_value=true&ip_address='
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    host = host.strip()
    host_name=host
    url = url + host_name
    response = requests.get(url, auth=(username, password), headers=headers)
    data = response.json()
    return data

def rel_incidents(sys_id):
    url = 'https://instance.service-now.com/api/now/table/incident?sysparm_display_value=true&active=true&cmdb_ci='
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    cmdb_ci=sys_id
    url= url+cmdb_ci

    response = requests.get(url, auth=(username, password), headers=headers)
    inc_data = response.json()

    return inc_data

##################################
###Dashboard
#################################
#it is yet to be implemented.
#the idea is to display Pie charts or bar charts based on thehost group in nagios.
#will implent this soon.
#adding a test comment

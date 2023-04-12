import xml.etree.ElementTree as ET
import requests as r
import datetime
from dateutil.relativedelta import relativedelta
import configparser


config = configparser.ConfigParser()
config.read("config.ini")

USERNAME = config.get('credentials', 'USERNAME')
PASSWORD = config.get('credentials', 'PASSWORD')

assetIds = []

def get_vmdr_xml_data():

    current_date = datetime.datetime.now().date()

    lastCheckedIn_date = current_date - relativedelta(days=7)

    xml_payload = '''<ServiceRequest>
    <preferences>
        <limitResults>1000</limitResults>
    </preferences>
    <filters>
        <Criteria field="tagName" operator="EQUALS">Cloud Agent</Criteria>
        <Criteria field="lastCheckedIn" operator="LESSER">{0}</Criteria>
    </filters>
</ServiceRequest>'''.format(lastCheckedIn_date)

    url = "https://qualysapi.qg1.apps.qualys.in/qps/rest/2.0/search/am/hostasset"


    auth = (USERNAME, PASSWORD)

    headers = {"Content-Type":"text/xml"}

    response = r.post(url, auth=auth, headers=headers , data=xml_payload)

    vmdr_data = response.content.decode('utf-8')

    with open('vmdr_data_latest.xml',"w") as f:
        f.write(vmdr_data)
    return(vmdr_data)
    return(lastCheckedIn_date)

def extract_assetId():

    # Parse the XML data
    tree = ET.parse("vmdr_data_latest.xml")

    root = tree.getroot()

    for lastId in root.findall('.//HostAsset/id'):
        assetIds.append(lastId.text)

def uninstall_cloud_agents(asset):

    url = "https://qualysapi.qg1.apps.qualys.in/qps/rest/2.0/uninstall/am/asset/"+asset

    auth = (USERNAME, PASSWORD)

    headers = {"Content-Type":"text/xml"}

    with open("uninstall_post.xml","rb") as f:
        xml_payload = f.read()

    response = r.post(url, auth=auth, headers=headers , data=xml_payload)

    uninstall_data = response.content.decode('utf-8')

    with open('agents_uninstalled.txt',"a") as f:
        f.write(f"\n\nAgent uninstalled on {asset}\n{uninstall_data}")


if __name__ == "__main__":
    get_vmdr_xml_data()
    extract_assetId()
    for assetId in assetIds:
        print(assetId)
        #uninstall_cloud_agents(assetId)
        #with open("uninstalled_logs.txt","a") as f:
            #current_time = datetime.datetime.now()
            #f.write(f"agent in {assetId} is uninstalled on {current_time}")'''







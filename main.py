import requests
import xmltodict
import os
import xml.etree.ElementTree as ET
import shutil
from colorama import Fore, Style, init

clear = lambda: os.system('cls')


logs = []

def centerprint(text):
    cols, _ = shutil.get_terminal_size()
    padding = (cols - len(text)) // 2
    print(' ' * padding + text)

def ValidXml(xml_string):
    try:
        ET.fromstring(xml_string)
        return True
    except ET.ParseError:
        return False

def Download(image_id):
    clear()
    id = image_id.lower()
    if id != "clear" and id.isdigit():
        url = f'https://assetdelivery.roblox.com/v1/asset/?id={id}'
        response = requests.get(url)
        if response.status_code == 200:
            xml_data = response.content
            if not ValidXml(xml_data):
                download_decal(id)
            else:
                parsed_xml = xmltodict.parse(xml_data)
                result_url = parsed_xml['roblox']['Item']['Properties']['Content']['url']
                result = result_url.split('=')[1]
                download_decal(result)
    elif id == "clear":
        logs.clear()
            


def download_decal(decalid):
    url2 = f'https://assetdelivery.roblox.com/v1/asset/?id={decalid}'
    responsen = requests.get(url2)

    if responsen.status_code == 200:
        with open(f"{decalid}.png", "wb") as f:
            f.write(responsen.content)
            log = f"{Fore.GREEN}[{responsen.status_code}] {Style.RESET_ALL} Downloaded:{decalid}.png | {Fore.BLUE}LOG {Style.RESET_ALL}| "
            logs.append(log)
    else:
        print("Failed to download asset.")


while True:
    clear()

    for log in logs:
        centerprint(log)
    
    data = input(f"{Fore.GREEN}[DOWNLOADER]{Style.RESET_ALL} Enter image id >")
    Download(data)

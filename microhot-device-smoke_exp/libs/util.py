import hashlib
import json
import multiprocessing
import random
import subprocess

from requests_toolbelt import MultipartEncoder
import requests
from libs.logging_conf import Logger



def format_json(jsonstr):
    return json.dumps(jsonstr,indent=4,sort_keys=True)


def getToken(param=None, userId=USERID):
    md5instance = hashlib.md5()
    if param is None:
        param = '{}'
    plain_str = param + userId + ENCRYPTER
    Logger.logger.debug("string needs to be encrypted is: %s ",plain_str)

    md5instance.update(plain_str.encode())
    return md5instance.hexdigest()


def loadPkgVersion(deviceType,pkgversion):
    if deviceType == '3':
        packagepath = '/mnt/code/pkg/3band'
    if deviceType == '4':
        packagepath = '/mnt/code/pkg/4band'
    if deviceType == '2':
        packagepath = '/mnt/code/pkg/kakou'

    pkg_file_name = pkgversion + '.tar.gz'
    pkg_version_file = packagepath + '/' + pkg_file_name
    Logger.logger.debug("package version file path is: " + pkg_version_file)

    return pkg_file_name,pkg_version_file


def genTokenHeader(param=None):
    headers = {}
    token = getToken(param=param,userId=USERID)
    headers['tokenId'] = USERID
    headers['token'] = token
    headers['content-type'] = 'application/json;charset=utf-8'
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0'
    Logger.logger.debug("token header is: " + str(headers))

    return headers


def loadpkg(deviceType,pkg_version,uploadurl):
    package_file = loadPkgVersion(deviceType, pkg_version)

    multi_content = MultipartEncoder(
        fields={'file': (package_file[0], open(package_file[1], 'rb'), 'application/gzip')}
    )
    Logger.logger.debug("send upload file request to " + uploadurl)

    res = requests.post(uploadurl, data=multi_content,
                        headers={'Content-Type': multi_content.content_type})
    Logger.logger.debug("upload package file status is: "+ str(res.status_code))
    Logger.logger.debug("upload package file response is: "+ str(res.content))

    return res.status_code,res.content.decode('utf-8')

def pinger(job_q, results_q ):
    while True:
        ip = job_q.get()
        if ip is None: break
        counter1 = '-c1'
        counter10 = '-c10'
        wait = '-W10'
        output_message1 = "1 packets transmitted, 1 received"
        output_message10 = "10 packets transmitted, 0 received"

        p1 = subprocess.Popen(['ping', counter1, wait, ip], stdout=subprocess.PIPE)
        result1 = p1.stdout.read().decode('utf8')
        if result1.find(output_message1) != -1:
            pass
        else:
            p10 = subprocess.Popen(['ping', counter10, wait, ip], stdout=subprocess.PIPE)
            result10 = p10.stdout.read().decode('utf8')
            if result10.find(output_message10) != -1:
                results_q.put(ip)
            else:
                pass

def get_multiprocessing_ip(ip_band):
    ip_format = ip_band+'{0}'
    pool_size = 255
    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()

    pool = [ multiprocessing.Process(target=pinger, args=(jobs,results))
                 for i in range(pool_size) ]
    for p in pool:
        p.start()
    for i in range(3,255):
        jobs.put(ip_format.format(i))
    for p in pool:
        jobs.put(None)
    for p in pool:
        p.join()

    return results


def get_ip(ip_band,dhcp_ip):
    not_alive_ip_queue = get_multiprocessing_ip(ip_band)
    ip_list = list()
    while not not_alive_ip_queue.empty():
        ip = not_alive_ip_queue.get()
        ip_list.append(ip)
    if dhcp_ip in ip_list:
        ip_list.remove(dhcp_ip)
    choice_ip = random.choice(ip_list)
    Logger.logger.debug("The available ip address is: %s", choice_ip)
    return choice_ip
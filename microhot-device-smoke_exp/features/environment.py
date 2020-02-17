import os.path
import json
import yaml
from behave import use_fixture
from behave import fixture


@fixture
def setup_account_config(context):
    config = context.configuration
    context.account = config['microhot_device']['account']
    context.hotdeviceIP = config['microhot_device']['hotdeviceIP']
    context.password = config['microhot_device']['PASSWORD']
    context.ip_band = config['microhot_device']['default_band']
    context.machine_password = config['microhot_device']['MACHINE_PASSWORD']
    context.default_gateway = config['microhot_device']['default_gateway']
    context.gateway_66 = config['microhot_device']['gateway_66']


def _get_folder(folder_name):
    datafolder_path = str.split(os.path.abspath(__file__), 'feature')[0]
    data_folder = os.path.join(datafolder_path, folder_name)
    return data_folder


def load_data_fullpath(folder,data_file_name):
    data_file = os.path.join(folder,data_file_name)
    with open(data_file, 'r') as f:
        data = json.load(f)
        return data

def load_data(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
        return data


def _get_filename(data_file_name):
    return data_file_name.split('.')[0]


def get_request_data(folder):
    request_data_map = dict()
    for (path, dirs, files) in os.walk(folder):
        for file in files:
            fpath = os.path.join(path, file)
            file_name = _get_filename(file)
            body_data = load_data(fpath)
            request_data_map[file_name] = body_data
    return request_data_map


def load_config_yaml():
    config_folder = _get_folder('config')
    config_file_path = os.path.join(config_folder,'config.yaml')
    with open(config_file_path, 'r') as stream:
        try:
            return yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)


def before_feature(context,feature):
    folder_name = _get_folder('data')
    context.request_data = get_request_data(folder_name)


def after_feature(context,feature):
    context.request_data = {}
    context.configuration = {}


def before_all(context):
    userdata = context.config.userdata
    IP  = userdata.get("IP")
    deviceId   = userdata.get("deviceId")
    pkg_version  = userdata.get("pkg_version")
    devicetype = userdata.get("devicetype")
    context.command = ParseCommand(IP,deviceId,pkg_version,devicetype)
    context.IP = context.command.getIP()
    context.version = context.command.getPkgVersion()
    context.devicetype = context.command.getDeviceType()
    context.deviceId = context.command.getDeviceId()
    context.configuration = load_config_yaml()
    use_fixture(setup_account_config, context)


class ParseCommand():

    def __init__(self,IP,deviceId,pkg_version,devicetype):
        self.IP = IP
        self.deviceId = deviceId
        self.pkg_version = pkg_version
        self.devicetype = devicetype

    def getIP(self):
        return self.IP

    def getDeviceId(self):
        return self.deviceId

    def getPkgVersion(self):
        return self.pkg_version

    def getDeviceType(self):
        return self.devicetype
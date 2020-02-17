class DeviceCmccData(object):

    def __init__(self, body):
        self.body = body

    def setJsonNodeValue(self,**kwargs):
        for key,value in kwargs.items():
            if key == 'pci':
                self.body['params'][3]['msg']['opDeviceParameter'][0]['Frequency'][0]['pci'] = value
        return self.body


class DeviceCmccSend(object):

    def __init__(self, body):
        self.body = body

    def setJsonNodeValue(self,**kwargs):
        for key,value in kwargs.items():
            if key == 'cmd':
                self.body['params'][3]['msg']['cmd'] = value
        return self.body


class VersionManagementAdd(object):

    def __init__(self, body):
        self.body = body

    def setJsonNodeValue(self,**kwargs):
        for key,value in kwargs.items():
            if key == 'md5':
                self.body['md5'] = value
            if key == 'versionNum':
                self.body['versionNum'] = value
            if key == 'versionUrl':
                self.body['versionUrl'] = value
        return self.body


class VersionManagementPush(object):

    def __init__(self, body):
        self.body = body

    def setJsonNodeValue(self,**kwargs):
        for key,value in kwargs.items():
            if key == 'versionId':
                self.body['versionId'] = value
            if key == 'deviceId':
                self.body['deviceList'][0] = value
            if key == 'deviceForm':
                self.body['deviceForm'] = value
        return self.body


class VersionManagementQueryPushRecord(object):

    def __init__(self, body):
        self.body = body

    def setJsonNodeValue(self,**kwargs):
        for key,value in kwargs.items():
            if key == 'versionId':
                self.body['versionId'] = value
            if key == 'versionPushId':
                self.body['versionPushId'] = value
        return self.body


class ThreeGCableReceivingRequest(object):

    def __init__(self, body):
        self.body = body

    def setJsonNodeValue(self,**kwargs):
        for key,value in kwargs.items():
            if key == 'activeNow':
                self.body['activeNow'] = value
            if key == 'style':
                self.body['data']['ipMode'] = value
        return self.body


class StaticCableReceivingRequest(object):

    def __init__(self, body):
        self.body = body

    def setJsonNodeValue(self,**kwargs):
        for key,value in kwargs.items():
            if key == 'gateway':
                self.body['data']['gateway'] = value
            if key == 'deviceIp':
                self.body['data']['deviceIp'] = value
            if key == 'activeNow':
                self.body['activeNow'] = value
            if key == 'ipMode':
                self.body['data']['ipMode'] = value
        return self.body


class ModifyDeviceSettingRequest(object):

    def __init__(self, body):
        self.body = body

    def setJsonNodeValue(self,**kwargs):
        for key,value in kwargs.items():
            if key == 'devName':
                self.body['data']['devName'] = value
            if key == 'location':
                self.body['data']['location'] = value
            if key == 'serverip':
                self.body['data']['serverip'] = value
            if key == 'serverport':
                self.body['data']['serverport'] = value
            if key == 'height':
                self.body['data']['devpos']['height'] = value
            if key == 'provinceCode':
                self.body['data']['provinceCode'] = value
            if key == 'cityCode':
                self.body['data']['cityCode'] = value
            if key == 'areaCode':
                self.body['data']['areaCode'] = value
            if key == 'townCode':
                self.body['data']['townCode'] = value
            if key == 'devId':
                self.body['data']['devId'] = value
        return self.body


class QueryVersion(object):

    def __init__(self, body):
        self.body = body

    def setJsonNodeValue(self,**kwargs):
        for key,value in kwargs.items():
            if key == 'versionNum':
                self.body['versionNum'] = value
        return self.body


class ResetSettingRequest(object):

    def __init__(self, body):
        self.body = body

    def setJsonNodeValue(self,**kwargs):
        for key,value in kwargs.items():
            if key == 'devId':
                self.body['data']['devId'] = value
        return self.body


class UpdateDeviceConfigRequest(object):

    def __init__(self, body):
        self.body = body

    def setJsonNodeValue(self,**kwargs):
        for key,value in kwargs.items():
            if key == 'tacMin':
                self.body['opDeviceParameter'][0]['commonParameter']['tacMin'] = value
            if key == 'imsiReportInterval':
                self.body['opDeviceParameter'][0]['commonParameter']['imsiReportInterval'] = value
            if key == 'redirected_earfcn':
                self.body['opDeviceParameter'][0]['commonParameter']['redirected_earfcn'] = value
            if key == 'redirectedEarfcnFrameOffset':
                self.body['opDeviceParameter'][0]['commonParameter']['redirectedEarfcnFrameOffset'] = value
            if key == 'qRxLevMin':
                self.body['opDeviceParameter'][0]['commonParameter']['tacMin'] = value
            if key == 'interFreq':
                self.body['opDeviceParameter'][0]['commonParameter']['interFreq'] = value
            if key == 'activeNow':
                self.body['activeNow'] = value
        return self.body


class RequestMap(object):

    def __init__(self):
        self.request_name = []
        self.request_context = {}

    def add_request_content(self,name,req_context):
        if name not in self.request_name:
            self.request_context[name] = req_context

    def get_request_content(self,name):
        return self.request_context[name]





import configparser
import re
import sys
import traceback
import pexpect
from behave import *
from hamcrest import *


from libs.api_requests import *
from libs.request_data_config import *
from libs.util import *


@given("Operator prepares all the necessary context for ubus interface")
def step_impl(context):

    context.threeG_cable_lmt_receiving = context.request_data['3G-cable-style']
    context.manual_cable_lmt_receiving = context.request_data['manual-cable-style']
    context.get_device_info = context.request_data['device_info']
    context.get_device_status = context.request_data['device_status']
    context.http_restart = context.request_data['ubus_restart_template']
    context.request_template_json = context.request_data['ubus_request_template']
    context.modify_device_setting = context.request_data['modify_device_setting']
    context.update_device_config = context.request_data['modify_device_config']
    context.open_device_address = "http://" + context.IP + ":8086/ubus"
    context.available_ip = None
    context.ssh_ip = None
    context.default_list = ["00000000000000000000000000000000","web_lmt","param"]
    context.max_try = 3
    context.device_network_3G_http_request = None
    context.device_basic_info_request = None
    context.device_status_request = None
    context.update_device_setting_http_request = None
    context.default_device_setting = context.request_data['ubus_device_setting_default']

    model = getattr(context, "model", None)
    if not model:
        context.model = RequestMap()


@then("Compose the 3G cable receiving request to LMT")
def step_impl(context):

    threeG_lmt_receiving = context.threeG_cable_lmt_receiving
    for row in context.table:
        activetag = int(row['activeNow'])
        style = row['style']
        req_name = row['request_name']
        update_device = context.request_template_json
        update_device['params'] = []
        update_device['params'].extend(context.default_list)
        threeG_cable_receiving_object = ThreeGCableReceivingRequest(threeG_lmt_receiving)
        threeG_cable_receiving_request = threeG_cable_receiving_object.setJsonNodeValue(activeNow=activetag,style=style)
        threeG_cable_http = _compose_ubus_request_http(json.dumps(threeG_cable_receiving_request))
        update_device['params'].append(threeG_cable_http)
        tmp_str = re.sub("(:\s+)", ":", json.dumps(update_device))
        context.device_network_3G_http_request = re.sub("(,\s+)", ",", tmp_str)

        context.model.add_request_content(req_name,context.device_network_3G_http_request)
        Logger.logger.debug("send 3g lmt receiving response is: %s",context.device_network_3G_http_request)

        break


# @then('Send the restart request and expect "{response}" in response before recovery')
# def step_impl(context,response):
#
#     restart_device_request = json.dumps(context.restart_device).replace(" ", "")
#     ubus_command = _compose_ubus_request(restart_device_request)
#     Logger.logger.debug("ubus command is: %s", ubus_command)
#     context.client.sendline(ubus_command)
#     context.client.expect(['root@OpenWrt:~#',pexpect.EOF,pexpect.TIMEOUT])
#     request_output = context.client.before.decode('utf8')
#     Logger.logger.debug("restart to LMT response message is: %s.",request_output)
#     context.response_json = _get_response_json(request_output)
#
#     try:
#         assert_that(context.response_json['message']['msg'], equal_to(response))
#     except AssertionError as e:
        # _grant_app_rights(context)
        # _recover_srv_trx_file(context)
        # _generate_md5(context)
        # traceback.print_exc(e)


@then("Compose the request of sending manual cable request to LMT")
def step_impl(context):

    manual_cable_lmt_receiving = context.manual_cable_lmt_receiving
    for row in context.table:
        activetag = int(row['activeNow'])
        default_tag = row['default']
        ipMode = row['ipMode']
        req_name = row['request_name']

        update_device = context.request_template_json
        update_device['params'] = []
        update_device['params'].extend(context.default_list)
        cable_static_receiving_object = StaticCableReceivingRequest(manual_cable_lmt_receiving)
        if default_tag == 'no':
            context.device_manual_cable_static_http_request = cable_static_receiving_object.\
                setJsonNodeValue(activeNow=activetag,
                                deviceIp=context.available_ip,
                                gateway=context.gateway_66)
        elif default_tag == 'yes':
            context.device_manual_cable_static_http_request  = cable_static_receiving_object.\
                setJsonNodeValue(activeNow=activetag,
                                deviceIp=context.IP,
                                gateway=context.gateway_66,
                                ipMode=ipMode)
        ubus_command = _compose_ubus_request_http(json.dumps(context.device_manual_cable_static_http_request ))
        update_device['params'].append(ubus_command)
        tmp_str = re.sub("(:\s+)",":",json.dumps(update_device))
        context.device_manual_cable_static_http_request  = re.sub("(,\s+)",",",tmp_str)

        context.model.add_request_content(req_name, context.device_manual_cable_static_http_request )
        Logger.logger.debug("send manual cable static receiving response is: %s", context.device_manual_cable_static_http_request )

        break


@then("Compose the request of set v4.0.0 ifcfg")
def step_impl(context):

    manual_cable_lmt_receiving = context.manual_cable_lmt_receiving
    for row in context.table:
        activetag = int(row['activeNow'])
        ipMode = row['ipMode']
        req_name = row['request_name']

        update_device = context.request_template_json
        update_device['params'] = []
        update_device['params'].extend(context.default_list)
        cable_static_receiving_object = StaticCableReceivingRequest(manual_cable_lmt_receiving)

        context.manual_cable_static_http_request = cable_static_receiving_object. \
            setJsonNodeValue(activeNow=activetag,
                             deviceIp=context.hotdeviceIP,
                             gateway=context.default_gateway,
                             ipMode=ipMode)
        ubus_command = _compose_ubus_request_http(json.dumps(context.manual_cable_static_http_request))
        update_device['params'].append(ubus_command)
        tmp_str = re.sub("(:\s+)", ":", json.dumps(update_device))
        context.manual_cable_static_http_request = re.sub("(,\s+)", ",", tmp_str)

        context.model.add_request_content(req_name, context.manual_cable_static_http_request)
        Logger.logger.debug("send v4.0.0 cable static receiving response is: %s",
                            context.manual_cable_static_http_request)

        break


@then(
    'Compose the request of update device config "{tacMin}","{imsiReportInterval}","{redirectedearfcn}",'
    '"{redirectedEarfcnFrameOffset}","{qRxLevMin}","{interFreq}","{activeNow}"')
def step_impl(context, tacMin, imsiReportInterval, redirectedearfcn, redirectedEarfcnFrameOffset, qRxLevMin,
              interFreq,activeNow):

    global update_device_http_request
    update_device_request_template = context.request_template_json
    update_device_config = context.update_device_config
    update_device_request_template['params'] = []
    update_device_request_template['params'].extend(context.default_list)
    update_device_config_request_object = UpdateDeviceConfigRequest(update_device_config)
    update_device_request = update_device_config_request_object.\
        setJsonNodeValue(tacMin=int(tacMin),
                        imsiReportInterval=int(imsiReportInterval),
                        redirected_earfcn=int(redirectedearfcn),
                        redirectedEarfcnFrameOffset=int(redirectedEarfcnFrameOffset),
                        qRxLevMin=int(qRxLevMin),
                        interFreq=int(interFreq),
                        activeNow=int(activeNow))
    ubus_command = _compose_ubus_request_http(json.dumps(update_device_request))
    update_device_request_template['params'].append(ubus_command)
    tmp_str = re.sub("(:\s+)", ":", json.dumps(update_device_request_template))
    update_device_http_request = re.sub("(,\s+)", ",", tmp_str)
    Logger.logger.debug("update_device_http_request is %s.", update_device_http_request)


@then('Send the device http request and expect "{response}" in response')
def step_impl(context,response):

    for row in context.table:
        statictag = row['static']
        req_name = row['request_name']
        if statictag == "yes":
            context.open_device_address = "http://" + context.available_ip + ":8086/ubus"
        if statictag == "no":
            context.open_device_address = "http://" + context.IP + ":8086/ubus"
        Logger.logger.debug("send request url is: %s.",context.open_device_address)
        response_json = api_post(context.open_device_address,context.model.get_request_content(req_name))
        context.response_json = _get_response_json_http(response_json[0].content.decode('utf8'))
        Logger.logger.debug("set device response is %s.",context.response_json)
        assert_that(json.dumps(context.response_json),contains_string(response))

        break


@step("generate the md5 for security")
def step_impl(context):

    time.sleep(5)
    Logger.logger.debug("You are generation the md5 for security.")
    context.client.sendline("cd /root")
    time.sleep(2)
    context.client.expect(['root@OpenWrt:~#',pexpect.TIMEOUT])
    context.client.sendline("sh appmd5update.sh /app")
    time.sleep(2)
    context.client.expect(['root@OpenWrt:~#',pexpect.TIMEOUT])
    Logger.logger.debug("check md5 result is %s.",context.client.before.decode('utf8'))


@then("Delete the factoryflag if it exists")
def step_impl(context):

    Logger.logger.debug("You are deleting the factoryflag.")
    context.client.sendline("cd /data")
    time.sleep(2)
    context.client.expect(['root@OpenWrt:~#',pexpect.TIMEOUT])
    context.client.sendline("rm -rf factoryflag")
    time.sleep(2)
    context.client.expect(['root@OpenWrt:~#',pexpect.TIMEOUT])


@step('Set /app/config/ifcfg to "{style}"')
def step_impl(context,style):

    sed_command = "sed -i 's/^BOOTPROTO=\(\w\+\)/BOOTPROTO="+style+"/' ifcfg"
    delete_fifth_line = "sed -i '5d' ifcfg"
    try:
        context.client.sendline("cd /app/config")
        time.sleep(1)
        context.client.expect(['root@OpenWrt:/app/config#', pexpect.TIMEOUT])
        context.client.sendline(delete_fifth_line)
        time.sleep(1)
        context.client.expect(['root@OpenWrt:/app/config#', pexpect.TIMEOUT])
        context.client.sendline(sed_command)
        time.sleep(1)
        context.client.expect(['root@OpenWrt:/app/config#', pexpect.TIMEOUT])
    except Exception as e:
        traceback.print_exc(e)


@then('Check the parameter BOOTPROTO is configured to "{connect_style}" at /app/config/ifcfg file')
def step_impl(context,connect_style):

    ifcfg_config = "ifcfg"
    connect_style = connect_style.split(',')
    expected_content = 'BOOTPROTO='+connect_style[0]

    try:
        context.client.sendline("cd /app/config")
        context.client.expect(['root@OpenWrt:/app/config#',pexpect.TIMEOUT])
        context.client.sendline("ls")
        context.client.expect(['root@OpenWrt:/app/config#', pexpect.TIMEOUT])
        ls_config_output = context.client.before.decode('utf8')
        Logger.logger.debug("ls /app/config content is %s.", ls_config_output)
        if ls_config_output.find(ifcfg_config) != -1:
            delete_fifth_line = "sed -i 5d ifcfg"
            context.client.sendline(delete_fifth_line)
            context.client.expect(['root@OpenWrt:/app/config#', pexpect.TIMEOUT])
            context.client.sendline("cat ifcfg")
            context.client.expect(['root@OpenWrt:/app/config#', pexpect.TIMEOUT])
            cat_ifcfg_output = context.client.before.decode('utf8')
            Logger.logger.debug("cat ifcfg content after request is: %s",cat_ifcfg_output)
            if connect_style[0] != 'static':
                assert_that(cat_ifcfg_output, contains_string(expected_content))
            elif connect_style[1] == 'set':
                expected_device_ip = 'IPADD=' + context.available_ip
                assert_that(cat_ifcfg_output, contains_string(expected_content))
                assert_that(cat_ifcfg_output, contains_string(expected_device_ip))
    except Exception as e:
        traceback.print_exc(e)


@then('Check the parameter BOOTPROTO is configured to "{connect_style}" at /app/config/ifcfg file with new cline')
def step_impl(context,connect_style):

    expected_content = 'BOOTPROTO=' + connect_style
    context.client.sendline("cd /app/config")
    context.client.expect(['root@OpenWrt:/app/config#', pexpect.TIMEOUT])
    context.client.sendline("cat ifcfg")
    time.sleep(2)
    context.client.expect(['root@OpenWrt:/app/config#', pexpect.TIMEOUT])
    cat_ifcfg_output = context.client.before.decode('ascii')
    Logger.logger.debug("cat ifcfg content after request is: %s", cat_ifcfg_output)
    assert_that(cat_ifcfg_output, is_in(expected_content))


@step("Sleep for a while to let device shutdown")
def step_impl(context):

    for row in context.table:
        style = row['style']
        if style == 'default':
            context.ssh_ip = context.IP
        elif style == 'static':
            context.ssh_ip = context.available_ip

        closed_message = "Connection to " + context.ssh_ip + " closed"
        test_connection = "ssh " + context.ssh_ip
        Logger.logger.debug("connection IP address is: %s",test_connection)
        time.sleep(30)
        ssh = pexpect.spawn(test_connection)
        time.sleep(5)
        context.client.expect([closed_message, pexpect.TIMEOUT])
        host_prompt = context.client.before.decode('utf8')
        Logger.logger.debug("The device is disconnected, the prompted message is: %s",host_prompt)
        ssh.close()

        break


@then("Wait for specific time for the device to startup")
def step_impl(context):

    test_connection = "ssh " + context.hotdeviceIP
    for row in context.table:
        sleeptime = row['time']
        expected_keywords = row['key_words'].split(',')
        time.sleep(int(sleeptime))
        context.client.sendline(test_connection)
        time.sleep(2)
        context.client.expect(['root@openwrt:/www#', pexpect.TIMEOUT])
        prompt_message = context.client.before.decode('utf8')
        Logger.logger.debug("Wait for %s seconds, the device connection message is : %s", sleeptime, prompt_message)

        if prompt_message.find(expected_keywords[0]) != -1 or prompt_message.find(expected_keywords[1]) != -1:
            Logger.logger.debug("Device startup successfully.")
            break
        else:
            Logger.logger.debug("Device is starting up.")


@then("Wait for specific time for the device to startup for V4.0.1")
def step_impl(context):

    for row in context.table:
        sleeptime = row['time']
        style = row['style']
        if style == 'static':
            context.ssh_ip = context.available_ip
        if style == 'default':
            context.ssh_ip = context.IP
        time.sleep(int(sleeptime))
        ping_result = _ping_device_startup(context.ssh_ip)
        if ping_result == True:
            Logger.logger.debug("Ping device successfully.")
            time.sleep(10)
            break
        else:
            Logger.logger.debug("Device is starting up.")


@then("Compose the device basic info request to LMT")
def step_impl(context):

    get_deice_basic_info_request = context.get_device_info
    for row in context.table:
        req_name = row['request_name']
        update_device = context.request_template_json
        update_device['params'] = []
        update_device['params'].extend(context.default_list)

        device_basic_info_http = _compose_ubus_request_http(json.dumps(get_deice_basic_info_request))
        update_device['params'].append(device_basic_info_http)
        tmp_str = re.sub("(:\s+)", ":", json.dumps(update_device))
        context.device_basic_info_request = re.sub("(,\s+)", ",", tmp_str)

        context.model.add_request_content(req_name,context.device_basic_info_request)
        Logger.logger.debug("send device info receiving response is: %s",context.device_basic_info_request)

        break


@then("Compose the device status request to LMT")
def step_impl(context):

    get_deice_status_request = context.get_device_status

    for row in context.table:
        req_name = row['request_name']
        update_device = context.request_template_json
        update_device['params'] = []
        update_device['params'].extend(context.default_list)

        device_status_http = _compose_ubus_request_http(json.dumps(get_deice_status_request))
        update_device['params'].append(device_status_http)
        tmp_str = re.sub("(:\s+)", ":", json.dumps(update_device))
        context.device_status_request = re.sub("(,\s+)", ",", tmp_str)

        context.model.add_request_content(req_name, context.device_status_request)
        Logger.logger.debug("send device status response is: %s", context.device_status_request)

        break


@then("Load the srv_trx.conf file")
def step_impl(context):

    config = configparser.ConfigParser()
    context.client.sendline("cd /app/config")
    time.sleep(2)

    context.srv_trx = None
    context.client.expect(['root@OpenWrt:/app/config#', pexpect.TIMEOUT])
    context.client.sendline("cat srv_trx.conf")
    time.sleep(3)
    context.client.expect(['root@OpenWrt:/app/config#', pexpect.TIMEOUT])
    try:
        srv_trx = context.client.before.decode('utf8')
        srv_trx_ini = re.sub("(^[\d\D]*)srv_trx.conf", "", srv_trx)
        Logger.logger.debug("srv_trx content is: %s",srv_trx_ini)
        config.read_string(srv_trx_ini)
        context.srv_trx = config
        Logger.logger.debug("device_name value is: %s.", context.srv_trx['SYSCFG']['device_name'])
    except Exception as e:
        _grant_app_rights(context)
        _recover_srv_trx_file(context)
        _generate_md5(context)
        _delete_factoryflag(context)
        traceback.print_exc(e)


@step("delete the binary code of srv_trx.conf")
def step_impl(context):

    try:
        sed_command_delete = "sed -i '/create_time=/q' srv_trx.conf"
        context.client.sendline("cd /app/config")
        context.client.expect(['root@OpenWrt:/app/config#', pexpect.TIMEOUT])
        context.client.sendline(sed_command_delete)
        context.client.expect(['root@OpenWrt:/app/config#', pexpect.TIMEOUT])
        Logger.logger.debug("srv_trx.conf file is clean")
    except Exception as e:
        _grant_app_rights(context)
        _generate_md5(context)
        _delete_factoryflag(context)
        traceback.print_exc(e)


@then("Check the deivceId,devicename,devicestyle,devicetype,fixture_version,software_version of the device")
def step_impl(context):

    try:
        fixture_version = _get_fixture_version(context)
        software_version = _get_software_version(context)
        deviceId = context.srv_trx['SYSCFG']['client_id']
        devicename = context.srv_trx['SYSCFG']['device_name']
        devicetype = context.srv_trx['SYSCFG']['devType']
        deviceform = context.srv_trx['SYSCFG']['devForm']

        assert_that(context.response_json['message']['data']['devId'],equal_to(deviceId))
        assert_that(context.response_json['message']['data']['devName'],equal_to(devicename))
        assert_that(context.response_json['message']['data']['devType'],equal_to(devicetype))
        assert_that(context.response_json['message']['data']['devForm'],equal_to(deviceform))
        assert_that(context.response_json['message']['data']['app_version'],equal_to(software_version))
        assert_that(context.response_json['message']['data']['hw_version'],equal_to(fixture_version))
    except AssertionError as e:
        traceback.print_exc(e)


@then("Check the device status content")
def step_impl(context):

    m_card_status = [item for item in context.response_json['message']['data']['deviceMonitorList']
                     if item['operationType'] == "M"]
    m_card_node = m_card_status[0]
    Logger.logger.debug("M catchCount should greater_than_or_equal_to 0, it's value is : %s.",
                        m_card_node['catchCount'])

    try:
        assert_that(m_card_node['catchCount'], greater_than_or_equal_to(0))
        Logger.logger.debug("M memory should greater_than 0, it's value is : %s.", m_card_node['memory'])
        assert_that(m_card_node['memory'],greater_than(0))
        Logger.logger.debug("M disk should greater_than_or_equal_to 0, it's value is : %s.", m_card_node['disk'])
        assert_that(m_card_node['disk'],greater_than(0))
        Logger.logger.debug("M temperature should greater_than 0, it's value is : %s.", m_card_node['temperature'])
        assert_that(m_card_node['temperature'],greater_than(0))
        Logger.logger.debug("M duration should greater_than 0, it's value is : %s.", m_card_node['duration'])
        assert_that(m_card_node['duration'],greater_than(0))
        Logger.logger.debug("M power should greater_than 0, it's value is : %s.", m_card_node['power'])
        assert_that(m_card_node['power'],greater_than(0))
        Logger.logger.debug("M stationedInBobbi should greater_than_or_equal_to 0, it's value is : %s.",
                            m_card_node['stationedInBobbi'])
        assert_that(m_card_node['stationedInBobbi'],greater_than_or_equal_to(0))
        Logger.logger.debug("M sync_status should greater_than_or_equal_to 0, it's value is : %s.",
                            m_card_node['sync_status'])
        assert_that(m_card_node['sync_status'],greater_than_or_equal_to(0))
        Logger.logger.debug("M criminalCodeStatus should greater_than_or_equal_to 0, it's value is : %s.",
                            m_card_node['criminalCodeStatus'])
        assert_that(int(m_card_node['criminalCodeStatus']),greater_than_or_equal_to(0))
        Logger.logger.debug("M sweepStatus should greater_than_or_equal_to 0, it's value is : %s.",
                            m_card_node['sweepStatus'])
        assert_that(int(m_card_node['sweepStatus']),greater_than_or_equal_to(0))

        u_card_status = [item for item in context.response_json['message']['data']['deviceMonitorList']
                         if item['operationType'] == "U"]
        u_card_node = u_card_status[0]
        Logger.logger.debug("U catchCount should greater_than_or_equal_to 0, it's value is : %s.",
                            u_card_node['catchCount'])
        assert_that(int(u_card_node['catchCount']),greater_than_or_equal_to(0))
        Logger.logger.debug("U memory should greater_than 0, it's value is : %s.", u_card_node['memory'])
        assert_that(u_card_node['memory'],greater_than(0))
        Logger.logger.debug("U disk should greater_than_or_equal_to 0, it's value is : %s.", u_card_node['disk'])
        assert_that(u_card_node['disk'],greater_than(0))
        Logger.logger.debug("U temperature should greater_than 0, it's value is : %s.", u_card_node['temperature'])
        assert_that(u_card_node['temperature'],greater_than(0))
        Logger.logger.debug("U duration should greater_than 0, it's value is : %s.", u_card_node['duration'])
        assert_that(u_card_node['duration'],greater_than(0))
        Logger.logger.debug("U power should greater_than 0, it's value is : %s.", u_card_node['power'])
        assert_that(u_card_node['power'],greater_than(0))
        Logger.logger.debug("U stationedInBobbi should greater_than_or_equal_to 0, it's value is : %s.",
                            m_card_node['stationedInBobbi'])
        assert_that(m_card_node['stationedInBobbi'], greater_than_or_equal_to(0))
        Logger.logger.debug("U criminalCodeStatus should greater_than_or_equal_to 0, it's value is : %s.",
                            m_card_node['criminalCodeStatus'])
        assert_that(int(m_card_node['criminalCodeStatus']), greater_than_or_equal_to(0))
        Logger.logger.debug("U sweepStatus should greater_than_or_equal_to 0, it's value is : %s.",
                            m_card_node['sweepStatus'])
        assert_that(int(m_card_node['sweepStatus']), greater_than_or_equal_to(0))


        t_card_status = [item for item in context.response_json['message']['data']['deviceMonitorList']
                         if item['operationType'] == "T"]
        t_card_node = t_card_status[0]
        Logger.logger.debug("T catchCount should greater_than_or_equal_to 0, it's value is : %s.",
                            t_card_node['catchCount'])
        assert_that(int(t_card_node['catchCount']),greater_than_or_equal_to(0))
        Logger.logger.debug("T memory should greater_than 0, it's value is : %s.", t_card_node['memory'])
        assert_that(t_card_node['memory'],greater_than(0))
        Logger.logger.debug("T disk should greater_than_or_equal_to 0, it's value is : %s.", t_card_node['disk'])
        assert_that(t_card_node['disk'],greater_than(0))
        Logger.logger.debug("T temperature should greater_than 0, it's value is : %s.", t_card_node['temperature'])
        assert_that(t_card_node['temperature'],greater_than(0))
        Logger.logger.debug("T duration should greater_than 0, it's value is : %s.", t_card_node['duration'])
        assert_that(t_card_node['duration'],greater_than(0))
        Logger.logger.debug("T power should greater_than 0, it's value is : %s.", t_card_node['power'])
        assert_that(t_card_node['power'],greater_than(0))
        Logger.logger.debug("T stationedInBobbi should be greater_than_or_equal_to 0, it's value is : %s.",
                            m_card_node['stationedInBobbi'])
        assert_that(m_card_node['stationedInBobbi'], greater_than_or_equal_to(0))
        Logger.logger.debug("T criminalCodeStatus should be greater_than_or_equal_to 0, it's value is : %s.",
                            m_card_node['criminalCodeStatus'])
        assert_that(int(m_card_node['criminalCodeStatus']), greater_than_or_equal_to(0))
        Logger.logger.debug("T sweepStatus should  be greater_than_or_equal_to 0, it's value is : %s.",
                            m_card_node['sweepStatus'])
        assert_that(int(m_card_node['sweepStatus']), greater_than_or_equal_to(0))
    except AssertionError as error:
        traceback.format_exc(error)


@then(
    'Compose the request with "{devName}","{location}","{serverip}","{serverport}","{height}","{provinceCode}",'
    '"{cityCode}","{areaCode}","{townCode}"')
def step_impl(context, devName, location, serverip, serverport, height, provinceCode, cityCode, areaCode, townCode):

    modify_device_setting = context.modify_device_setting

    for row in context.table:
        req_name = row['request_name']
        Logger.logger.debug("location is %s.",location)
        update_device = context.request_template_json
        update_device['params'] = []
        update_device['params'].extend(context.default_list)
        modify_device_object = ModifyDeviceSettingRequest(modify_device_setting)
        modify_device_request = modify_device_object.setJsonNodeValue\
            (devName=devName, location=location,serverip=serverip,serverport=int(serverport),
             height=height,provinceCode=provinceCode,devId=context.deviceId,
             cityCode=cityCode,areaCode=areaCode,townCode=townCode)
        update_device_setting = _compose_ubus_request_http(json.dumps(modify_device_request))
        update_device['params'].append(update_device_setting)
        tmp_str = re.sub("(:\s+)",":",json.dumps(update_device))
        context.update_device_setting_http_request = re.sub("(,\s+)",",",tmp_str)

        context.model.add_request_content(req_name, context.update_device_setting_http_request)
        Logger.logger.debug("update_device_setting_http_request is %s.",context.update_device_setting_http_request)

        break


@then(
    'Check the parameters of "{devName}","{location}","{serverip}","{serverport}","{height}","{provinceCode}",'
    '"{cityCode}","{areaCode}","{townCode}" are modified at srv_trx.conf file')
def step_impl(context, devName, location, serverip, serverport, height, provinceCode, cityCode, areaCode, townCode):

    server_address = "tcp://" + serverip + ":" + serverport
    try:
        Logger.logger.debug("device_name value is: %s.", context.srv_trx['SYSCFG']['device_name'])
        assert_that(context.srv_trx['SYSCFG']['device_name'],equal_to(devName))
        Logger.logger.debug("location value is: %s.", context.srv_trx['SYSCFG']['location'])
        assert_that(context.srv_trx['SYSCFG']['location'],equal_to(location))
        Logger.logger.debug("server_addr value is: %s.", context.srv_trx['SYSCFG']['server_addr'])
        assert_that(context.srv_trx['SYSCFG']['server_addr'],equal_to(server_address))
        Logger.logger.debug("height value is: %s.", context.srv_trx['SYSCFG']['height'])
        assert_that(int(context.srv_trx['SYSCFG']['height']),equal_to(int(height)))
        Logger.logger.debug("provinceCode value is: %s.", context.srv_trx['SYSCFG']['provinceCode'])
        assert_that(int(context.srv_trx['SYSCFG']['provinceCode']),equal_to(int(provinceCode)))
        Logger.logger.debug("cityCode value is: %s.", context.srv_trx['SYSCFG']['cityCode'])
        assert_that(int(context.srv_trx['SYSCFG']['cityCode']),equal_to(int(cityCode)))
        Logger.logger.debug("areaCode value is: %s.", context.srv_trx['SYSCFG']['areaCode'])
        assert_that(int(context.srv_trx['SYSCFG']['areaCode']),equal_to(int(areaCode)))
        Logger.logger.debug("townCode value is: %s.", context.srv_trx['SYSCFG']['townCode'])
        assert_that(int(context.srv_trx['SYSCFG']['townCode']),equal_to(int(townCode)))
    except AssertionError as e:
        traceback.print_exc(e)


@then(
    'Check the parameters of "{tacMin}","{imsiReportInterval}","{redirectedearfcn}","{redirectedEarfcnFrameOffset}",'
    '"{qRxLevMin}","{interFreq}","{activeNow}" are modified at srv_trx.conf file')
def step_impl(context, tacMin, imsiReportInterval, redirectedearfcn, redirectedEarfcnFrameOffset, qRxLevMin,
              interFreq,activeNow):

    try:
        Logger.logger.debug("CMCC tacMin value is: %s.",context.srv_trx['CMCC']['tacMin'])
        assert_that(context.srv_trx['CMCC']['tacMin'], equal_to(tacMin))
        Logger.logger.debug("CMCC imsiReportInterval value is: %s.", context.srv_trx['CMCC']['imsiReportInterval'])
        assert_that(context.srv_trx['CMCC']['imsiReportInterval'], equal_to(imsiReportInterval))
        Logger.logger.debug("CMCC redirected_earfcn value is: %s.", context.srv_trx['CMCC']['redirected_earfcn'])
        assert_that(context.srv_trx['CMCC']['redirected_earfcn'], equal_to(redirectedearfcn))
        Logger.logger.debug("CMCC redirectedEarfcnFrameOffset value is: %s.", context.srv_trx['CMCC']['redirectedEarfcnFrameOffset'])
        assert_that(context.srv_trx['CMCC']['redirectedEarfcnFrameOffset'], equal_to(redirectedEarfcnFrameOffset))
        Logger.logger.debug("CMCC qRxLevMin value is: %s.",context.srv_trx['CMCC']['qRxLevMin'])
        assert_that(context.srv_trx['CMCC']['qRxLevMin'], equal_to(qRxLevMin))
        Logger.logger.debug("CMCC interFreq value is: %s.", context.srv_trx['CMCC']['interFreq'])
        assert_that(context.srv_trx['CMCC']['interFreq'], equal_to(interFreq))
    except AssertionError as e:
        traceback.print_exc(e)


@then('Send the update device config request and expect "{response}" in response')
def step_impl(context,response):

    update_device_config_response = api_post(context.open_device_address,update_device_http_request)
    Logger.logger.debug("update device config response is %s.",update_device_config_response[0].content)

    try:
        assert_that(str(update_device_config_response[0].content.decode('utf8')),contains_string(response))
    except AssertionError as e:
        traceback.print_exc(e)


@step("backup the ifcfg file")
def step_impl(context):

    context.client.sendline("cd /app/config")
    context.client.expect(['root@OpenWrt:/app/config#', pexpect.TIMEOUT])
    context.client.sendline("cp ifcfg ifcfg.bak")
    context.client.expect(['root@OpenWrt:/app/config#', pexpect.TIMEOUT])


@step("recover the ifcfg file")
def step_impl(context):

    time.sleep(5)
    Logger.logger.debug("You are recovering the ifcfg file.")
    context.client.sendline("cd /app/config")
    time.sleep(2)
    context.client.expect(['root@OpenWrt:/app/config#', pexpect.TIMEOUT])
    context.client.sendline("rm -rf ifcfg")
    time.sleep(2)
    context.client.expect(['root@OpenWrt:/app/config#', pexpect.TIMEOUT])
    context.client.sendline("mv ifcfg.bak ifcfg")
    time.sleep(2)
    context.client.expect(['root@OpenWrt:/app/config#', pexpect.TIMEOUT])


@then('Send the restart request and expect "{response}" in response')
def step_impl(context,response):

    for row in context.table:
        try:
            statictag = row['static']
            if statictag == "yes":
                context.open_device_address = "http://" + context.available_ip + ":8086/ubus"
            if statictag == "no":
                context.open_device_address = "http://" + context.IP + ":8086/ubus"
            Logger.logger.debug("http restart request is: %s", context.http_restart)
            restart_device_config_response = api_post(context.open_device_address, context.http_restart)
            Logger.logger.debug("restart device config response is %s.", restart_device_config_response[0].content)
            assert_that(str(restart_device_config_response[0].content.decode('utf8')),contains_string(response))
        except Exception as e:
            traceback.print_exc(e)
        break


@then('Send the reset device setting request and expect "{response}" in response')
def step_impl(context,response):

    for row in context.table:
        try:
            statictag = row['static']
            if statictag == "yes":
                context.open_device_address = "http://" + context.available_ip + ":8086/ubus"
            if statictag == "no":
                context.open_device_address = "http://" + context.IP + ":8086/ubus"
            context.default_device_setting = _compose_reset_setting_payload(context)
            reset_device_setting_response = api_post(context.open_device_address, context.default_device_setting)
            Logger.logger.debug("reset device setting request payload is: %s.",context.default_device_setting)
            Logger.logger.debug("reset device setting response is %s.", reset_device_setting_response[0].content)
            assert_that(str(reset_device_setting_response[0].content.decode('utf8')),contains_string(response))
        except Exception as e:
            traceback.print_exc(e)
        break


@then("exit current ssh session")
def step_impl(context):

    context.client.close()


def _get_response_json(reponse_output):

    first_str = reponse_output.replace("\\", "").replace(" ", "").replace("\r\n", "")
    second_str = re.sub("(^[\d\D]*)message\":\"", "{\"message\":", first_str)
    response_json_str = re.sub("}\"}$","}}",second_str)
    Logger.logger.debug("the response json is: %s.", response_json_str)
    return json.loads(response_json_str)


def _get_response_json_http(reponse_output):

    res_str = reponse_output.replace("\\", "")
    second_str = re.sub("(^[\d\D]*)message\":\"", "{\"message\":", res_str)
    response_json_str = re.sub("}\"}]}$","}}",second_str)
    Logger.logger.debug("the response json is: %s.", response_json_str)
    return json.loads(response_json_str)


def _get_fixture_version(context):

    try:
        context.client.sendline("cd /etc")
        time.sleep(1)
        context.client.expect(['root@OpenWrt:/etc#', pexpect.TIMEOUT])
        context.client.sendline("cat os_version")
        time.sleep(1)
        context.client.expect(['root@OpenWrt:/etc#', pexpect.TIMEOUT])
        osVersion = context.client.before.decode('utf8')
        os_version_content = re.sub("(^[\d\D]*)os_version", "", osVersion)
        Logger.logger.debug("the fixture version is: %s.", os_version_content)
    except:
        return None
    else:
        return re.sub("\r\n","",os_version_content)


def _get_software_version(context):

    context.client.sendline("cd /app")
    context.client.expect(['root@OpenWrt:/app#', pexpect.TIMEOUT])
    context.client.sendline("cat appVersions.ini")
    context.client.expect(['root@OpenWrt:/app#', pexpect.TIMEOUT])
    appVersion = context.client.before.decode('utf8')
    appVersion_ini = re.sub("(^[\d\D]*)appVersions.ini", "", appVersion)
    Logger.logger.debug("the appVersions.ini is: %s.", appVersion_ini)
    return  re.sub("\r\n","",appVersion_ini)


def _compose_ubus_request(raw_request):

    slash_qute = raw_request.replace('"','\\"')
    request_content = "'{\"msg\":\"" + slash_qute + "\"}'"
    ubus_command_str = "ubus call web_lmt param " + request_content
    return ubus_command_str


def _compose_ubus_request_http(raw_request):

    msg = {}
    msg["msg"] = raw_request
    return msg


def _ping_device_startup(ip):

    counter = '-c10'
    wait = '-W15'
    output_message = "10 packets transmitted, 10 received"
    p = subprocess.Popen(['ping', counter, wait, ip], stdout=subprocess.PIPE)
    result = p.stdout.read().decode('utf8')
    print('ping 10 times message is: %s', result)
    if result.find(output_message) != -1:
        return True
    else:
        return False


def _delete_factoryflag(context):

    Logger.logger.debug("You are deleting the factoryflag.")
    context.client.sendline("cd /data")
    time.sleep(2)
    context.client.expect(['root@OpenWrt:~#',pexpect.TIMEOUT])
    context.client.sendline("rm -rf factoryflag")
    time.sleep(2)
    context.client.expect(['root@OpenWrt:~#',pexpect.TIMEOUT])


def _grant_app_rights(context):

    Logger.logger.debug("Start to grant wr rights to /app folder.")
    context.client.sendline("cd /root")
    context.client.expect(['root@OpenWrt:~#', pexpect.TIMEOUT])
    context.client.sendline("sh update_filesystem_mode.sh /app")
    context.client.expect(['root@OpenWrt:~#', pexpect.TIMEOUT])


def _recover_srv_trx_file(context):

    Logger.logger.debug("You are recovering the srv_trx.conf file.")
    context.client.sendline("cd /app/config")
    context.client.expect(['root@OpenWrt:/app/config#', pexpect.TIMEOUT])
    context.client.sendline("rm -rf srv_trx.conf")
    context.client.expect(['root@OpenWrt:/app/config#', pexpect.TIMEOUT])
    Logger.logger.debug("You are renaming srv_trx.conf.bak to srv_trx.conf")
    context.client.sendline("mv srv_trx.conf.bak srv_trx.conf")
    context.client.expect(['root@OpenWrt:/app/config#', pexpect.TIMEOUT])


def _generate_md5(context):

    Logger.logger.debug("You are generating the md5 for security.")
    context.client.sendline("cd /root")
    context.client.expect(['root@OpenWrt:~#',pexpect.TIMEOUT])
    context.client.sendline("sh appmd5update.sh /app")
    context.client.expect(['root@OpenWrt:~#',pexpect.TIMEOUT])


def _compose_reset_setting_payload(context):

    reset_setting_template = context.default_device_setting
    reset_setting_payload_object = ResetSettingRequest(reset_setting_template)
    context.reset_setting_http = reset_setting_payload_object. \
        setJsonNodeValue(devId=context.deviceId)

    update_device = context.request_template_json
    update_device['params'] = []
    update_device['params'].extend(context.default_list)

    device_status_http = _compose_ubus_request_http(json.dumps(context.reset_setting_http))
    update_device['params'].append(device_status_http)
    tmp_str = re.sub("(:\s+)", ":", json.dumps(update_device))
    return re.sub("(,\s+)", ",", tmp_str)

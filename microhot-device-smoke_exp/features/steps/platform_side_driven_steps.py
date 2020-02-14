from behave import *
from hamcrest import *
from libs.api_requests import *
from libs.request_data_config import *
from libs.util import *
from libs.logging_conf import Logger


def _parseQueryPushRecordStatus(response_content):

    response = json.loads(response_content.decode('utf8'))
    Logger.logger.debug("query push record status result is: %s",response)
    reponse_body = response['data']['list'][0]
    upgrade_status = reponse_body['upgradeStatus']

    return upgrade_status

@given("Operator prepares all the necessary context for testing platform")
def step_impl(context):

    config = context.configuration
    context.detect_platform_baseurl = config['detect_code']['base_url']
    context.upload_url = context.detect_platform_baseurl + config['detect_code']['version_management']['upload']
    context.add_url = context.detect_platform_baseurl + config['detect_code']['version_management']['add']
    context.push_url = context.detect_platform_baseurl + config['detect_code']['version_management']['push']
    context.querypush_url = context.detect_platform_baseurl + config['detect_code']['version_management']['querypush']
    context.download_url_base = context.detect_platform_baseurl + config['detect_code']['version_management'][
        'download']
    context.query_url = context.detect_platform_baseurl + config['detect_code']['version_management']['query']
    context.query_push_record_url = context.detect_platform_baseurl + config['detect_code']['version_management'][
        'query_push_record']
    context.delete_versionid_url = context.detect_platform_baseurl + \
                                   config['detect_code']['version_management']['delete_versionid']
    context.max_try = 2
    context.add_max_try = 4

    context.add_request = context.request_data['add']
    context.query_request = context.request_data['query']
    context.push_request = context.request_data['push']
    context.query_push_record_request = context.request_data['query_push_record']


@given('Operator upload package in detect-code platform, expect "{response_code}" with filename and md5 in response')
def step_impl(context,response_code):

    try:
        upload_pkg_response = loadpkg(context.devicetype, context.version, context.upload_url)
        res_code = upload_pkg_response[0]
        res_content = json.loads(upload_pkg_response[1])

        context.fileName = res_content['data']['fileName']
        context.md5 = res_content['data']['md5']

        assert_that(str(res_code),equal_to(response_code))
    except AssertionError as e:
        traceback.print_exc(e)


@then('Operator add new package to detect-code platform, expect "{response_code}" in response')
def step_impl(context,response_code):

    context.download_url = context.download_url_base + context.fileName
    add_request_data = VersionManagementAdd(context.add_request)
    add_request = add_request_data.setJsonNodeValue(md5=context.md5,versionNum=context.version,
                                                    versionUrl=context.download_url)
    Logger.logger.debug("add package request payload is : {}".format(format_json(add_request)))

    stringify_add_request = json.dumps(add_request).replace(" ","")
    add_pkg_header = genTokenHeader(stringify_add_request)
    Logger.logger.debug("add package request header is: " + str(add_pkg_header))

    for i in range(context.add_max_try):
        exist_result = _check_version_exist(context)
        if exist_result is True:
            add_package_response = soft_api_post(context.add_url, stringify_add_request, add_pkg_header)
            res_code = add_package_response.status_code
            Logger.logger.debug("Add package result is successfully, response code is %s !",res_code)
            break
        elif exist_result is False :
            Logger.logger.debug("add package failed then wait 180 seconds.")
            time.sleep(180)
            continue

    version_status = _check_version_exist(context)
    if version_status == True:
        Logger.logger.debug("After tried so many times, upload package status is %s.", version_status)
        assert_that(int(version_status), equal_to(False))


@then('Operator get the packageVersionId, expect "{response_code}" in response')
def step_impl(context, response_code):

    stringify_query_request = json.dumps(context.query_request).replace(" ", "")
    query_pkg_header = genTokenHeader(stringify_query_request)
    Logger.logger.debug("query package request header is: " + str(query_pkg_header))
    query_packageVersionId_response = api_post(context.query_url,stringify_query_request,query_pkg_header)
    context.query_response = json.loads(query_packageVersionId_response[0].content.decode('utf8'))

    assert_that(str(query_packageVersionId_response[0].status_code), equal_to(response_code))


@then("Compose request body with deviceId and versionId mapping")
def step_impl(context):

    packageVersion_mapping_list = context.query_response['data']['list']
    packageVersionId_list = [item for item in packageVersion_mapping_list \
                             if item['versionNum'] == context.version]
    context.packageVersionId = packageVersionId_list[0]['id']
    Logger.logger.debug("Version id is: " + str(context.packageVersionId))

    push_request_data = VersionManagementPush(context.push_request)
    context.push_request = push_request_data.setJsonNodeValue(
        versionId=context.packageVersionId,deviceId=context.deviceId)
    Logger.logger.debug("push package request payload is : {}".format(format_json(context.push_request)))


@when('Operator push new version package to specific deviceId, expect "{response_code}" in response')
def step_impl(context,response_code):

    stringify_push_request = json.dumps(context.push_request).replace(" ", "")
    push_pkg_header = genTokenHeader(stringify_push_request)
    Logger.logger.debug("push package request header is: " + str(push_pkg_header))
    push_package_response = api_post(context.push_url, stringify_push_request, push_pkg_header)
    Logger.logger.debug("push package to device result is: " + str(push_package_response[0].status_code))

    assert_that(str(push_package_response[0].status_code), equal_to(response_code))


@then('Operator query with versionId to get versionPushId, expect "{response_code}" in response')
def step_impl(context, response_code):

    querypush_url = context.querypush_url + context.packageVersionId
    querypush_header = genTokenHeader()
    querypush_request = {}
    querypush_response = api_post(querypush_url, querypush_request, querypush_header)
    querypush_response_decoded = json.loads(querypush_response[0].content.decode('utf-8'))
    context.versionPushId = querypush_response_decoded['data'][0]['id']
    Logger.logger.debug("versionPushId result is: " + str(context.versionPushId))
    assert_that(str(querypush_response[0].status_code), equal_to(response_code))


@then('Operator query upgrade result api with versionId and versionPushId, expect "{response_code}" in response')
def step_impl(context,response_code):

    query_push_record_request_data = VersionManagementQueryPushRecord(context.query_push_record_request)
    query_push_record_request = query_push_record_request_data.setJsonNodeValue(
        versionId=context.packageVersionId, versionPushId=context.versionPushId)
    Logger.logger.debug("query push record request payload is : {}".format(format_json(query_push_record_request)))

    context.stringify_query_push_record_request = json.dumps(query_push_record_request).replace(" ", "")
    context.query_push_record_request_header = genTokenHeader(context.stringify_query_push_record_request)
    Logger.logger.debug("query push record request header is: " + str(context.query_push_record_request_header))
    query_push_record_response = api_post(
        context.query_push_record_url, context.stringify_query_push_record_request,
        context.query_push_record_request_header)
    Logger.logger.debug("query push record response result is: " + str(query_push_record_response[0].status_code))

    assert_that(str(query_push_record_response[0].status_code), equal_to(response_code))


@then("Wait for specific time period, the upgradeStatus should be as expected")
def step_impl(context):

    for row in context.table:
        sleeptime = row['time']
        expected_status_list = row['upgrade_status'].split(',')

        time.sleep(int(sleeptime))

        try:
            query_push_record_response = api_post(
                context.query_push_record_url, context.stringify_query_push_record_request,
                context.query_push_record_request_header)

            Logger.logger.debug("query push record response is %s.",query_push_record_response[0].content)
            context.upgradeStatus = _parseQueryPushRecordStatus(query_push_record_response[0].content)
            Logger.logger.debug("upgrade response is: " + str(query_push_record_response[0].content.decode('utf8')))
            Logger.logger.debug("wait for another %s seconds then query push record response status is: %s"
                             ,sleeptime,context.upgradeStatus)
            if context.upgradeStatus == 'FINISH':
                break
            else:
                assert_that(context.upgradeStatus,is_in(expected_status_list))
        except Exception as e:
            _delete_uploaded_version(context)
            traceback.print_exc(e)
            break


@then('delete the uploaded version and expect "{response}" in response')
def step_impl(context,response):

    delete_versionid_url = context.delete_versionid_url + context.packageVersionId
    Logger.logger.debug("delete versionid url is: %s.",delete_versionid_url)
    deleteversion_header = genTokenHeader()
    deleteversion_request = {}
    deleteversion_response = api_post(delete_versionid_url, deleteversion_request, deleteversion_header)
    deleteversion_response_status = deleteversion_response[0].status_code
    deleteverion_response_decoded = json.loads(deleteversion_response[0].content.decode('utf-8'))

    assert_that(int(deleteversion_response_status), equal_to(200))
    assert_that(deleteverion_response_decoded['msg'],equal_to(response))


def _check_version_exist(context):

    query_version_request_data = QueryVersion(context.query_request)
    query_version_request = query_version_request_data.setJsonNodeValue(
        versionNum=context.version)
    Logger.logger.debug("query version payload is : {}".format(format_json(query_version_request)))

    stringify_query_version_request = json.dumps(query_version_request).replace(" ", "")
    query_pkg_header = genTokenHeader(stringify_query_version_request)
    Logger.logger.debug("query package request header is: %s",str(query_pkg_header))
    query_version_response = api_post(context.query_url, stringify_query_version_request, query_pkg_header)
    Logger.logger.debug("query version response  is: %s.",query_version_response[0].content.decode('utf8'))
    query_version_json = json.loads(query_version_response[0].content.decode('utf8'))
    version_list = query_version_json['data']['list']
    Logger.logger.debug("query version response list  is: %s.",version_list)
    if version_list.__len__() != 0:
        return False
    else:
        return True


def _delete_uploaded_version(context):

    delete_versionid_url = context.delete_versionid_url + context.packageVersionId
    Logger.logger.debug("delete versionid url is: %s.",delete_versionid_url)
    deleteversion_header = genTokenHeader()
    deleteversion_request = {}
    deleteversion_response = api_post(delete_versionid_url, deleteversion_request, deleteversion_header)
    deleteversion_response_status = deleteversion_response[0].status_code

    assert_that(int(deleteversion_response_status), equal_to(200))




from datetime import datetime
import os
import time

import pexpect
from behave import *
from hamcrest import assert_that, is_in

from libs.logging_conf import Logger

use_step_matcher("re")


@then("check the deamon\.log can catch IMSI")
def step_impl(context):

    context.client.sendline("cd log")
    context.client.expect(['root@OpenWrt:~/Logger#', pexpect.TIMEOUT])

    for row in context.table:
        sleeptime = row['time']
        expected_status_list = row['catch_status'].split(',')

        time.sleep(int(sleeptime))
        context.client.sendline("cat deamon.log")
        time.sleep(2)
        context.client.expect(['root@OpenWrt:~/log#', pexpect.TIMEOUT])
        context.deamonlog = context.client.before.decode('utf8')
        check_result = _check_catch_imsi(context.deamonlog)
        Logger.logger.debug("catch imsi status is: " + str(check_result))
        Logger.logger.debug("wait for another %s seconds then query catch imis status is: %s"
                         , sleeptime, str(check_result))
        assert_that(str(check_result), is_in(expected_status_list))

        if check_result == True:
            Logger.logger.debug("device can catch the IMIS successfully.")

            break


def _check_catch_imsi(log_content):

    date_string = datetime.now()
    now_time = date_string.strftime('%Y-%m-%d')

    catch_content = ""
    with open("deamon.log",'w') as f:
        f.write(log_content)

    with open("deamon.log") as df:
        for line in df:
            message = line.split(" ")
            content = " ".join(message[3:-1])
            if message[0] == now_time and content.find('IMSI:') != -1:
                catch_info = message[0]+","+message[1]+","+content.lstrip()+'\r\n'
                Logger.logger.debug("catched imsi is: %s",catch_info)
                catch_content += catch_info
    os.remove("deamon.log")

    if catch_content.find("IMSI:") != -1:
        return True
    else:
        return False

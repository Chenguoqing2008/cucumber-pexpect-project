import pexpect
from behave import *
from hamcrest import *

from libs.api_requests import *
from libs.util import *


@when('Operator Login the micro hot-device wifi-interface')
def step_impl(context):

    context.available_ip = None
    for row in context.table:
        style = row['static']
        if style == 'yes':
            context.available_ip = get_ip(context.ip_band, context.IP)
        else:
            context.available_ip = context.IP

        ssh_command = "ssh webUI@"+context.IP
        ssh = pexpect.spawn(ssh_command)
        index = ssh.expect(['password:', 'continue connecting',pexpect.EOF, pexpect.TIMEOUT])
        if index == 0:
            ssh.sendline("admin")
            ssh.expect("root@openwrt:/www#")
            Logger.logger.debug('login micro-hot device wifi successfully.')
        elif index == 1:
            ssh.sendline("yes")
            ssh.expect("password:")
            ssh.sendline("admin")
            ssh.expect("root@openwrt:/www#")
            Logger.logger.debug('login micro-hot device wifi successfully.')
        context.client = ssh

        break


@when("Set the proper user to login")
def step_impl(context):

    for row in context.table:
        style = row['static']
        if style == 'yes':
            if context.available_ip is None:
                context.available_ip = get_ip(context.ip_band, context.IP)
            elif context.available_ip is not None:
                pass
        elif style == "no":
            context.available_ip = context.IP
    _delete_known_hosts()
    ssh_clean = pexpect.spawn("ssh-keygen -t rsa")
    ssh_clean.expect(["Enter file in which to save the key",pexpect.TIMEOUT])
    ssh_clean.sendline("\r\n")
    ssh_clean.expect(["Enter passphrase", pexpect.TIMEOUT])
    ssh_clean.sendline("\r\n")
    ssh_clean.expect(["Enter same passphrase again",pexpect.TIMEOUT])
    ssh_clean.sendline("\r\n")
    ssh_clean.expect(["randomart image",pexpect.TIMEOUT])
    Logger.logger.debug("generate ssh key info is: %s",ssh_clean.before.decode('utf8'))
    ssh_clean.close()


@step("wifi-interface jump to real micro hot-device")
def step_impl(context):

    deamon_file = 'deamon.sh'

    for i in range(context.max_try):
        context.client.sendline('ssh '+ context.hotdeviceIP)
        index = context.client.expect(["(y/n)","(yes/no)","password", pexpect.TIMEOUT])
        Logger.logger.debug("wifi-interface login prompt message is: "+context.client.before.decode('utf8'))
        if index == 0:
            context.client.sendline('y')
            context.client.expect(["password",pexpect.TIMEOUT])
            context.client.sendline(context.password)
            context.client.expect(["root@OpenWrt:~#",pexpect.TIMEOUT])
            Logger.logger.debug("jump to micro-hot logo: " + context.client.before.decode('utf8'))
        elif index == 1:
            context.client.sendline('yes')
            context.client.expect(["password",pexpect.TIMEOUT])
            context.client.sendline(context.password)
            context.client.expect(["root@OpenWrt:~#",pexpect.TIMEOUT])
            Logger.logger.debug("jump to micro-hot logo: " + context.client.before.decode('utf8'))
            Logger.logger.debug('log into hot-device successfully')
        elif index == 2:
            context.client.sendline(context.password)
            context.client.expect(["root@OpenWrt:~#",pexpect.TIMEOUT])
            Logger.logger.debug("jump to micro-hot logo: " + context.client.before.decode('utf8'))
        else:
            continue

    context.client.sendline("cd /root")
    context.client.expect(["root@OpenWrt:~#", pexpect.TIMEOUT])
    context.client.sendline('ls')
    context.client.expect(["root@OpenWrt:~#",pexpect.TIMEOUT])
    ls_output = context.client.before.decode('utf8')
    Logger.logger.debug("login ls content is %s.",ls_output)

    assert_that(ls_output,contains_string(deamon_file))
    Logger.logger.debug('log into hot-device successfully')


@then("login real micro hot-device")
def step_impl(context):

    Logger.logger.debug("available IP address is: %s", context.available_ip)
    deamon_file = 'deamon.sh'
    time.sleep(10)
    for row in context.table:
        style = row['style']
        if style == 'static':
            context.ssh_ip = context.available_ip
        if style == 'default':
            context.ssh_ip = context.IP
    ssh_command = "ssh " + context.ssh_ip
    Logger.logger.debug("connecting IP is: %s",context.ssh_ip)
    ssh = pexpect.spawn(ssh_command)
    time.sleep(45)
    refuse_tag = ssh.expect(["Connection refused","No route to host","want to continue connecting",
                             "password",pexpect.TIMEOUT])
    for i in range(5):
        if refuse_tag == 0:
            time.sleep(15)
            ssh.sendline(ssh_command)
            refuse_tag = ssh.expect(["Connection refused","No route to host",pexpect.TIMEOUT])
            continue
        elif refuse_tag == 1:
            time.sleep(15)
            ssh.sendline(ssh_command)
            refuse_tag = ssh.expect(["Connection refused", "No route to host", pexpect.TIMEOUT])
            continue
        elif refuse_tag == 2 or refuse_tag == 3:
            break

    confirm_index = ssh.expect(["(y/n)","(yes/no)","password",pexpect.TIMEOUT])
    Logger.logger.debug("confirm message is: %s.",ssh.before.decode('utf8'))
    Logger.logger.debug("confirm_index is %s", confirm_index)
    if confirm_index == 0:
        ssh.sendline('y')
        ssh.expect(["password", pexpect.TIMEOUT])
        ssh.sendline(context.password)
        ssh.expect(["root@OpenWrt:~#", pexpect.TIMEOUT])
        Logger.logger.debug("login to hot device logo: " + ssh.before.decode('utf8'))
    elif confirm_index == 1:
        ssh.sendline('yes')
        ssh.expect(["password", pexpect.TIMEOUT])
        ssh.sendline(context.password)
        ssh.expect(["root@OpenWrt:~#", pexpect.TIMEOUT])
        Logger.logger.debug("login to hot device logo: " + ssh.before.decode('utf8'))
    elif confirm_index == 2:
        ssh.sendline(context.password)
        ssh.expect(["root@OpenWrt:~#", pexpect.TIMEOUT])
        Logger.logger.debug("login to hot device logo: " + ssh.before.decode('utf8'))

    ssh.sendline("cd /root")
    ssh.expect(["root@OpenWrt:~#", pexpect.TIMEOUT])
    ssh.sendline('ls')
    ssh.expect(["root@OpenWrt:~#", pexpect.TIMEOUT])
    ls_output = ssh.before.decode('utf8')
    Logger.logger.debug("login ls content is %s.", ls_output)
    assert_that(ls_output, contains_string(deamon_file))
    Logger.logger.debug('log into hot-device successfully')

    context.client = ssh


@then("Delete the known_hosts for conflicting")
def step_impl(context):

    context.client.sendline("rm -rf ~/.ssh/known_hosts")
    context.client.expect(["root@openwrt:/www#",pexpect.TIMEOUT])
    Logger.logger.debug('Reset the known_hosts file.')


@then("Check the package version is correct")
def step_impl(context):

    context.client.sendline("cd /app")
    Logger.logger.debug("you have entered the micro-hot device /app folder")
    context.client.expect(['root@OpenWrt:/app#',pexpect.TIMEOUT])
    context.client.sendline("cat appVersions.ini")
    context.client.expect(['root@OpenWrt:/app#', pexpect.EOF, pexpect.TIMEOUT])
    cat_version_output = context.client.before.decode('utf8')
    device_version = cat_version_output.split('\r\n')[1]

    assert_that(device_version,equal_to(context.version))


@then("Wait for some time for preparing deleting known_hosts")
def step_impl(context):

    known_message = 'known_hosts'
    password_message = 'password'
    connection_message = 'connecting'
    test_connection = "ssh " + context.hotdeviceIP
    for row in context.table:
        sleeptime = row['time']
        time.sleep(int(sleeptime))
        context.client.sendline(test_connection)
        time.sleep(2)
        context.client.expect(["root@openwrt:/www#", pexpect.TIMEOUT])
        prompt_message = context.client.before.decode('utf8')
        Logger.logger.debug("Prompt out message of deleting known_hosts is:" + prompt_message)
        if prompt_message.find(known_message) != -1 or \
                prompt_message.find(password_message) != -1 or prompt_message.find(connection_message) != -1:
            break


@then("grant /app folder wr rights")
def step_impl(context):

    context.client.sendline("cd /root")
    time.sleep(2)
    prompt_index = context.client.expect(['root@OpenWrt:~#','root@openwrt:/www#',pexpect.TIMEOUT])
    time.sleep(10)
    if prompt_index == 0:
        Logger.logger.debug("prompt index is: %s.",prompt_index)
        Logger.logger.debug("Start to grant wr rights to /app folder.")
    elif prompt_index == 1:
        Logger.logger.debug("prompt index is: %s.", prompt_index)
        context.execute_steps(u"""
               Then  wifi-interface jump to real micro hot-device
           """)
        context.client.sendline("cd /root")
        context.client.expect(['root@OpenWrt:~#', pexpect.TIMEOUT])
        Logger.logger.debug("ssh connecting have been reset.")
        Logger.logger.debug("Start to grant wr rights to /app folder.")
    context.client.sendline("sh update_filesystem_mode.sh /app")
    time.sleep(5)
    index = context.client.expect(['root@OpenWrt:~#',"(y/n)","(yes/no)",pexpect.TIMEOUT])
    Logger.logger.debug("index value is: %s",index)
    if index == 1:
        context.client.sendline("y")
        context.client.expect(['root@OpenWrt:~#', pexpect.TIMEOUT])
        context.client.sendline("mount")
    if index == 2:
        context.client.sendline("yes")
        context.client.expect(['root@OpenWrt:~#', pexpect.TIMEOUT])


@then("Update ifcfg file to default dhcp")
def step_impl(context):

    dhcp = 'dhcp'
    ipadd = context.hotdeviceIP
    gateway = context.default_gateway
    Logger.logger.debug("ipadd is: %s.",ipadd)
    Logger.logger.debug("gateway is: %s.",gateway)

    sed_command_dhcp = \
        "sed -i 's/^BOOTPROTO=\(\w\+\)/BOOTPROTO=" + dhcp + "/' ifcfg"
    sed_command_ipadd = "sed -i '2c IDAPP="+ipadd+"' ifcfg"
    sed_command_gateway = "sed -i '3c GATEWAY="+gateway+"' ifcfg"

    context.client.sendline("cd /app/config")
    context.client.expect(['root@OpenWrt:/app/config#', pexpect.TIMEOUT])
    context.client.sendline(sed_command_dhcp)
    context.client.expect(['root@OpenWrt:/app/config#', pexpect.TIMEOUT])
    context.client.sendline(sed_command_ipadd)
    context.client.expect(['root@OpenWrt:/app/config#', pexpect.TIMEOUT])
    context.client.sendline(sed_command_gateway)
    context.client.expect(['root@OpenWrt:/app/config#', pexpect.TIMEOUT])
    context.client.sendline("cat ifcfg")
    context.client.expect(['root@OpenWrt:/app/config#', pexpect.TIMEOUT])
    Logger.logger.debug("the default dhcp content is: %s", context.client.before.decode('utf8'))


def _delete_known_hosts():
    subprocess.call(['rm -rf /root/.ssh/*'],shell=True)

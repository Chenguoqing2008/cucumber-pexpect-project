Feature: Smoke testing of ubus interface functionality

  Background: Operator needs to a smoke testing of micro-hot device
    Given Operator prepares all the necessary context for ubus interface


  @V4.0.0
  Scenario: Smoke testing the platform receiving style of 3G, waiting for take effect(V4.0.0)
    When  Operator login the micro hot-device wifi-interface
      | static |
      | no     |
    Then  Delete the known_hosts for conflicting
    Then  wifi-interface jump to real micro hot-device
    Then  Delete the factoryflag if it exists
    Then  Compose the 3G cable receiving request to LMT
      | activeNow | style | request_name |
      | 0         | none  | 3G_request   |
    Then  Send the device http request and expect "Success" in response
      | request_name | static |
      | 3G_request   | no     |
    Then  exit current ssh session
    When  Operator login the micro hot-device wifi-interface
      | static |
      | no     |
    Then  Delete the known_hosts for conflicting
    Then  wifi-interface jump to real micro hot-device
    Then  grant /app folder wr rights
    Then  Check the parameter BOOTPROTO is configured to "none" at /app/config/ifcfg file
    Then  Set /app/config/ifcfg to "static"
    Then  generate the md5 for security
    Then  Delete the factoryflag if it exists
    Then  Send the restart request and expect "Success" in response
     | static |
     | no     |
    And   Sleep for a while to let device shutdown
      | style   |
      | default |
    Then  Wait for specific time for the device to startup
      | time | key_words           |
      | 20   | password,connecting |
      | 20   | password,connecting |
      | 20   | password,connecting |
      | 20   | password,connecting |
      | 20   | password,connecting |
      | 20   | password,connecting |
    When  Operator login the micro hot-device wifi-interface
      | static |
      | no     |
    Then  Delete the known_hosts for conflicting
    Then  wifi-interface jump to real micro hot-device
    Then  exit current ssh session


  @V4.0.1
  Scenario: Smoke testing the platform receiving style of 3G, waiting for take effect(V4.0.1)
     When  Set the proper user to login
      | static|
      | no    |
     Then  login real micro hot-device
      | style   |
      | default |
     Then  Delete the factoryflag if it exists
     Then  Compose the 3G cable receiving request to LMT
      | activeNow | style | request_name |
      | 0         | none  | 3G_request   |
     Then  Send the device http request and expect "Success" in response
      | request_name | static |
      | 3G_request   | no     |
     Then  grant /app folder wr rights
     Then  Check the parameter BOOTPROTO is configured to "none" at /app/config/ifcfg file
     Then  generate the md5 for security
     Then  Delete the factoryflag if it exists
     Then  Compose the request of sending manual cable request to LMT
      | activeNow | default | ipMode | request_name         |
      | 1         | yes     | static | cable_static_default |
     Then  Send the device http request and expect "Success" in response
      | request_name         | static |
      | cable_static_default | no     |
     And   Sleep for a while to let device shutdown
      | style   |
      | default |
     Then  Wait for specific time for the device to startup for V4.0.1
      | time | style   |
      | 20   | default |
      | 20   | default |
      | 20   | default |
      | 20   | default |
      | 20   | default |
      | 20   | default |
      | 20   | default |
     When  Set the proper user to login
      | static|
      | no    |
     Then  login real micro hot-device
      | style  |
      | default|
     Then  exit current ssh session


  @V4.0.1
  Scenario: Smoke testing the platform receiving style of cable, waiting for take effect(V4.0.1)
     When  Set the proper user to login
      | static|
      | no    |
     Then  login real micro hot-device
      | style   |
      | default |
     Then  Delete the factoryflag if it exists
     Then  Compose the 3G cable receiving request to LMT
      | activeNow | style | request_name |
      | 0         | dhcp  | cable_request|
     Then  Send the device http request and expect "Success" in response
      | request_name | static |
      | cable_request| no     |
     Then  grant /app folder wr rights
     Then  Check the parameter BOOTPROTO is configured to "dhcp" at /app/config/ifcfg file
     Then  generate the md5 for security
     Then  Delete the factoryflag if it exists
     Then  Compose the request of sending manual cable request to LMT
      | activeNow | default | ipMode | request_name         |
      | 1         | yes     | static | cable_static_default |
     Then  Send the device http request and expect "Success" in response
      | request_name         | static |
      | cable_static_default | no     |
     And   Sleep for a while to let device shutdown
      | style   |
      | default |
     Then  Wait for specific time for the device to startup for V4.0.1
      | time | style   |
      | 20   | default |
      | 20   | default |
      | 20   | default |
      | 20   | default |
      | 20   | default |
      | 20   | default |
      | 20   | default |
     When  Set the proper user to login
      | static|
      | no    |
     Then  login real micro hot-device
      | style  |
      | default|
     Then  exit current ssh session


  @V4.0.1
  Scenario: Smoke testing the platform receiving style of cable static, waiting for take effect(V4.0.1)
     When  Set the proper user to login
      | static |
      | yes    |
     Then  login real micro hot-device
      | style   |
      | default |
     Then  Delete the factoryflag if it exists
     Then  Compose the request of sending manual cable request to LMT
      | activeNow | default | ipMode | request_name |
      | 0         | no      | static | cable_static |
     Then  Send the device http request and expect "Success" in response
      | request_name | static |
      | cable_static | no     |
     Then  grant /app folder wr rights
     Then  Check the parameter BOOTPROTO is configured to "static,set" at /app/config/ifcfg file
     Then  generate the md5 for security
     Then  Delete the factoryflag if it exists
     Then  Compose the request of sending manual cable request to LMT
      | activeNow | default | ipMode | request_name         |
      | 1         | yes     | static | cable_static_default |
     Then  Send the device http request and expect "Success" in response
      | request_name         | static |
      | cable_static_default | no     |
     And   Sleep for a while to let device shutdown
      | style   |
      | default |
     Then  Wait for specific time for the device to startup for V4.0.1
      | time | style   |
      | 20   | default |
      | 20   | default |
      | 20   | default |
      | 20   | default |
      | 20   | default |
      | 20   | default |
      | 20   | default |
     When  Set the proper user to login
      | static|
      | no    |
     Then  login real micro hot-device
      | style  |
      | default|
     Then  exit current ssh session


  @V4.0.1
  Scenario: Smoke testing the platform receiving style of cable static, take effect instantly(V4.0.1)
    When  Set the proper user to login
      | static |
      | yes    |
    Then  login real micro hot-device
      | style   |
      | default |
    Then  Delete the factoryflag if it exists
    Then  Compose the request of sending manual cable request to LMT
      | activeNow | default | ipMode | request_name |
      | 1         | no      | static | cable_static |
    Then  Send the device http request and expect "Success" in response
      | request_name | static |
      | cable_static | no     |
    And   Sleep for a while to let device shutdown
      | style   |
      | default |
    Then  Wait for specific time for the device to startup for V4.0.1
      | time | style  |
      | 20   | static |
      | 20   | static |
      | 20   | static |
      | 20   | static |
      | 20   | static |
      | 20   | static |
    When  Set the proper user to login
      | static |
      | yes    |
    Then  login real micro hot-device
      | style  |
      | static |
    Then  grant /app folder wr rights
    Then  Check the parameter BOOTPROTO is configured to "static,set" at /app/config/ifcfg file
    Then  generate the md5 for security
    Then  Delete the factoryflag if it exists
    Then  Compose the request of sending manual cable request to LMT
      | activeNow | default | ipMode | request_name         |
      | 1         | yes     | static | cable_static_default |
    Then  Send the device http request and expect "Success" in response
      | request_name         | static |
      | cable_static_default | yes    |
    And   Sleep for a while to let device shutdown
      | style   |
      | static  |
    Then  Wait for specific time for the device to startup for V4.0.1
      | time | style   |
      | 20   | default |
      | 20   | default |
      | 20   | default |
      | 20   | default |
      | 20   | default |
      | 20   | default |
      | 20   | default |
    When  Set the proper user to login
      | static |
      | no     |
    Then  login real micro hot-device
      | style   |
      | default |
    Then  exit current ssh session


  @V4.0.0
  Scenario: Smoke testing of viewing device basic info(V4.0.0)
    When  Operator login the micro hot-device wifi-interface
      | static |
      | no     |
    Then  Delete the known_hosts for conflicting
    Then  wifi-interface jump to real micro hot-device
    Then  Delete the factoryflag if it exists
    Then  Compose the device basic info request to LMT
      | request_name |
      | basic_info   |
    Then  Send the device http request and expect "Success" in response
      | request_name | static |
      | basic_info   | no     |
    Then  grant /app folder wr rights
    And   delete the binary code of srv_trx.conf
    Then  Load the srv_trx.conf file
    Then  generate the md5 for security
    Then  Delete the factoryflag if it exists
    Then  Check the deivceId,devicename,devicestyle,devicetype,fixture_version,software_version of the device
    Then  exit current ssh session


  @V4.0.1
  Scenario: Smoke testing of viewing device basic info(V4.0.1)
    When  Set the proper user to login
      | static|
      | no    |
    Then  login real micro hot-device
      | style  |
      | default|
    Then  Delete the factoryflag if it exists
    Then  Compose the device basic info request to LMT
      | request_name |
      | basic_info   |
    Then  Send the device http request and expect "Success" in response
      | request_name | static |
      | basic_info   | no     |
    Then  grant /app folder wr rights
    And   delete the binary code of srv_trx.conf
    Then  Load the srv_trx.conf file
    Then  generate the md5 for security
    Then  Delete the factoryflag if it exists
    Then  Check the deivceId,devicename,devicestyle,devicetype,fixture_version,software_version of the device


  @V4.0.0
  Scenario: Smoke testing of viewing device status info(V4.0.0)
    When  Operator login the micro hot-device wifi-interface
      | static|
      | no    |
    Then  Delete the known_hosts for conflicting
    Then  wifi-interface jump to real micro hot-device
    Then  Compose the device status request to LMT
      | request_name |
      | device_status|
    Then  Send the device http request and expect "Success" in response
      | request_name | static |
      | device_status| no     |
    Then  Check the device status content
    Then  exit current ssh session


  @V4.0.1
  Scenario: Smoke testing of viewing device status info(V4.0.1)
    When  Set the proper user to login
      | static|
      | no    |
    Then  login real micro hot-device
      | style  |
      | default|
    Then  Delete the factoryflag if it exists
    Then  Compose the device status request to LMT
      | request_name |
      | device_status|
    Then  Send the device http request and expect "Success" in response
      | request_name | static |
      | device_status| no     |
    Then  Check the device status content
    Then  exit current ssh session


  @V4.0.0
  Scenario: Smoke testing of device restart(V4.0.0)
    When  Operator login the micro hot-device wifi-interface
      | static|
      | no    |
    Then  Delete the known_hosts for conflicting
    Then  wifi-interface jump to real micro hot-device
    Then  Delete the factoryflag if it exists
    Then  Send the restart request and expect "Success" in response
     | static |
     | no     |
    And   Sleep for a while to let device shutdown
      | style   |
      | default |
    Then  Wait for specific time for the device to startup
      | time | key_words           |
      | 20   | password,connecting |
      | 20   | password,connecting |
      | 20   | password,connecting |
      | 20   | password,connecting |
      | 20   | password,connecting |
      | 20   | password,connecting |
    When  Operator login the micro hot-device wifi-interface
      | static|
      | no    |
    Then  Delete the known_hosts for conflicting
    Then  wifi-interface jump to real micro hot-device
    Then  exit current ssh session


  @V4.0.1
  Scenario: Smoke testing of device restart(V4.0.1)
    When  Set the proper user to login
      | static|
      | no    |
    Then  login real micro hot-device
      | style  |
      | default|
    Then  Delete the factoryflag if it exists
    Then  Send the restart request and expect "Success" in response
     | static |
     | no     |
    And   Sleep for a while to let device shutdown
      | style   |
      | default |
    Then  Wait for specific time for the device to startup for V4.0.1
      | time | style   |
      | 20   | default |
      | 20   | default |
      | 20   | default |
      | 20   | default |
      | 20   | default |
      | 20   | default |
      | 20   | default |
    When  Set the proper user to login
      | static|
      | no    |
    Then  login real micro hot-device
      | style  |
      | default|
    Then  exit current ssh session


  @V4.0.0
  Scenario Outline: Smoke testing of modify device setting and wait for taking effect(V4.0.0)
    When  Operator login the micro hot-device wifi-interface
      | static|
      | no    |
    Then  Delete the known_hosts for conflicting
    Then  wifi-interface jump to real micro hot-device
    Then  Delete the factoryflag if it exists
    Then  Compose the request with "<devName>","<location>","<serverip>","<serverport>","<height>","<provinceCode>","<cityCode>","<areaCode>","<townCode>"
      | request_name   |
      | device_setting |
    Then  Send the device http request and expect "Success" in response
      | request_name   | static |
      | device_setting | no     |
    Then  exit current ssh session
    When  Operator login the micro hot-device wifi-interface
      | static|
      | no    |
    Then  Delete the known_hosts for conflicting
    Then  wifi-interface jump to real micro hot-device
    Then  Delete the factoryflag if it exists
    Then  grant /app folder wr rights
    And   delete the binary code of srv_trx.conf
    Then  Load the srv_trx.conf file
    Then  Check the parameters of "<devName>","<location>","<serverip>","<serverport>","<height>","<provinceCode>","<cityCode>","<areaCode>","<townCode>" are modified at srv_trx.conf file
    Then  generate the md5 for security
    Then  Send the reset device setting request and expect "Success" in response
     | static |
     | no     |
    Then  Send the restart request and expect "Success" in response
     | static |
     | no     |
    And   Sleep for a while to let device shutdown
      | style   |
      | default |
    Then  Wait for some time for preparing deleting known_hosts
      | time |
      | 20   |
      | 20   |
      | 20   |
    Then  Delete the known_hosts for conflicting
    Then  Wait for specific time for the device to startup
      | time | key_words           |
      | 15   | password,connecting |
      | 15   | password,connecting |
      | 15   | password,connecting |
    Then  wifi-interface jump to real micro hot-device
    Then  exit current ssh session

    Examples:
      | devName     | location                  | serverip        | serverport | height | provinceCode | cityCode | areaCode | townCode |
      | test_device | GuangDong Shenzhen FuTian | 113.108.109.101 | 7703       | 100    | 43           | 4304     | 430408   | 430408100|


  @V4.0.1
  Scenario Outline: Smoke testing of modify device setting and wait for taking effect(V4.0.1)
    When  Set the proper user to login
      | static|
      | no    |
    Then  login real micro hot-device
      | style  |
      | default|
    Then  Delete the factoryflag if it exists
    Then  Compose the request with "<devName>","<location>","<serverip>","<serverport>","<height>","<provinceCode>","<cityCode>","<areaCode>","<townCode>"
      | request_name   |
      | device_setting |
    Then  Send the device http request and expect "Success" in response
      | request_name   | static |
      | device_setting | no     |
    Then  exit current ssh session
    When  Set the proper user to login
      | static|
      | no    |
    Then  login real micro hot-device
      | style  |
      | default|
    Then  grant /app folder wr rights
    And   delete the binary code of srv_trx.conf
    Then  Load the srv_trx.conf file
    Then  Check the parameters of "<devName>","<location>","<serverip>","<serverport>","<height>","<provinceCode>","<cityCode>","<areaCode>","<townCode>" are modified at srv_trx.conf file
    Then  generate the md5 for security
    Then  Send the reset device setting request and expect "Success" in response
     | static |
     | no     |
    Then  Send the restart request and expect "Success" in response
     | static |
     | no     |
    And   Sleep for a while to let device shutdown
      | style   |
      | default |
    Then  Wait for specific time for the device to startup for V4.0.1
      | time | style  |
      | 30   | dhcp   |
      | 30   | dhcp   |
      | 30   | dhcp   |
      | 30   | dhcp   |
      | 30   | dhcp   |
      | 30   | dhcp   |
    When  Set the proper user to login
      | static|
      | no    |
    Then  login real micro hot-device
      | style  |
      | default|
    Then  Delete the factoryflag if it exists
    Then  exit current ssh session

    Examples:
      | devName      | location                 | serverip        | serverport | height | provinceCode | cityCode | areaCode | townCode  |
      | debug_device | GuangDong Shenzhen BaoAn | 113.108.119.102 | 7704       | 101    | 41           | 4103     | 410304   | 410403004 |


  @V4.0.0
  Scenario Outline: Smoke testing of modify device setting and take effect instantly(V4.0.0)
    When  Operator login the micro hot-device wifi-interface
      | static|
      | no    |
    Then  Delete the known_hosts for conflicting
    Then  wifi-interface jump to real micro hot-device
    Then  Delete the factoryflag if it exists
    Then  Compose the request with "<devName>","<location>","<serverip>","<serverport>","<height>","<provinceCode>","<cityCode>","<areaCode>","<townCode>"
      | request_name   |
      | device_setting |
    Then  Send the device http request and expect "Success" in response
      | request_name   | static |
      | device_setting | no     |
    Then  Send the restart request and expect "Success" in response
     | static |
     | no     |
    And   Sleep for a while to let device shutdown
      | style   |
      | default |
    Then  Wait for some time for preparing deleting known_hosts
      | time |
      | 20   |
      | 20   |
      | 20   |
    Then  Delete the known_hosts for conflicting
    Then  Wait for specific time for the device to startup
      | time | key_words           |
      | 15   | password,connecting |
      | 15   | password,connecting |
      | 15   | password,connecting |
      | 15   | password,connecting |
      | 15   | password,connecting |
    Then  wifi-interface jump to real micro hot-device
    Then  grant /app folder wr rights
    And   delete the binary code of srv_trx.conf
    Then  Load the srv_trx.conf file
    Then  Check the parameters of "<devName>","<location>","<serverip>","<serverport>","<height>","<provinceCode>","<cityCode>","<areaCode>","<townCode>" are modified at srv_trx.conf file
    Then  generate the md5 for security
    Then  Delete the factoryflag if it exists
    Then  Send the reset device setting request and expect "Success" in response
     | static |
     | no     |
    Then  Send the restart request and expect "Success" in response
     | static |
     | no     |
    And   Sleep for a while to let device shutdown
      | style   |
      | default |
    Then  Wait for some time for preparing deleting known_hosts
      | time |
      | 20   |
      | 20   |
      | 20   |
    Then  Delete the known_hosts for conflicting
    Then  Wait for specific time for the device to startup
      | time | key_words           |
      | 15   | password,connecting |
      | 15   | password,connecting |
      | 15   | password,connecting |
      | 15   | password,connecting |
      | 15   | password,connecting |
    Then  wifi-interface jump to real micro hot-device
    Then  exit current ssh session

    Examples:
      | devName    | location                 | serverip        | serverport | height | provinceCode | cityCode | areaCode | townCode  |
      | GDB_device | GuangDong Shenzhen LuoHu | 113.108.110.101 | 7705       | 102    | 36           | 3604     | 360423   | 360423102 |


  @V4.0.1
  Scenario Outline: Smoke testing of modify device setting and take effect instantly(V4.0.1)
    When  Set the proper user to login
      | static|
      | no    |
    Then  login real micro hot-device
      | style  |
      | default|
    Then  Delete the factoryflag if it exists
      Then  Compose the request with "<devName>","<location>","<serverip>","<serverport>","<height>","<provinceCode>","<cityCode>","<areaCode>","<townCode>"
      | request_name   |
      | device_setting |
    Then  Send the device http request and expect "Success" in response
      | request_name   | static |
      | device_setting | no     |
    Then  Send the restart request and expect "Success" in response
     | static |
     | no     |
    And   Sleep for a while to let device shutdown
      | style  |
      | default|
    Then  Wait for specific time for the device to startup for V4.0.1
      | time | style  |
      | 30   | dhcp   |
      | 30   | dhcp   |
      | 30   | dhcp   |
      | 30   | dhcp   |
      | 30   | dhcp   |
      | 30   | dhcp   |
    When  Set the proper user to login
      | static|
      | no    |
    Then  login real micro hot-device
      | style  |
      | default|
    Then  grant /app folder wr rights
    And   delete the binary code of srv_trx.conf
    Then  Load the srv_trx.conf file
    Then  Check the parameters of "<devName>","<location>","<serverip>","<serverport>","<height>","<provinceCode>","<cityCode>","<areaCode>","<townCode>" are modified at srv_trx.conf file
    Then  generate the md5 for security
    Then  Delete the factoryflag if it exists
    Then  Send the reset device setting request and expect "Success" in response
     | static |
     | no     |
    Then  Send the restart request and expect "Success" in response
      | static |
      | no     |
    And   Sleep for a while to let device shutdown
      | style  |
      | default|
    Then  Wait for specific time for the device to startup for V4.0.1
      | time | style  |
      | 30   | dhcp   |
      | 30   | dhcp   |
      | 30   | dhcp   |
      | 30   | dhcp   |
      | 30   | dhcp   |
      | 30   | dhcp   |
    When  Set the proper user to login
      | static|
      | no    |
    Then  login real micro hot-device
      | style  |
      | default|
    Then  Delete the factoryflag if it exists
    Then  exit current ssh session

    Examples:
      | devName     | location                   | serverip        | serverport | height | provinceCode | cityCode | areaCode | townCode  |
      | mock_device | GuangDong Shenzhen YanTian | 113.108.111.101 | 7706       | 103    | 52           | 5204     | 520422   | 520422101 |


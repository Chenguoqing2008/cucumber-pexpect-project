Feature: Smoke testing of ubus interface functionality
  """
  group the parameter to three parts:
  1. tacMin imsiReportInterval redirected_earfcn redirectedEarfcnFrameOffset qRxLevMin interFreq
  2. tacPeriod tacMax measRptInterval bandWidth syncMode radioSwitch
  3. downFrequency pci priority rsrp powerLevel frameOffset plmn
  """

  Background: Operator needs to a smoke testing of micro-hot device
    Given Operator prepares all the necessary context for ubus interface

#  @V4.0.0
#  Scenario Outline: Smoke testing of modify basic config and take effect instantly(V4.0.0)
#    When  Operator login the micro hot-device wifi-interface
#      | static|
#      | no    |
#    Then  Delete the known_hosts for conflicting
#    Then  wifi-interface jump to real micro hot-device
#    Then  grant /app folder wr rights
#    And   backup the srv_trx.conf file
#    Then  generate the md5 for security
#    Then  Compose the request with "<devName>","<location>","<serverip>","<serverport>","<height>","<provinceCode>","<cityCode>","<areaCode>","<townCode>"
#    Then  Send the update device config request and expect "Success" in response
#    Then  Compose the request of restart
#    Then  Send the restart request and expect "Success" in response
#    And   Sleep for a while to let device shutdown
#    Then  Wait for some time for preparing deleting known_hosts
#      | time |
#      | 15   |
#      | 15   |
#      | 15   |
#    Then  Delete the known_hosts for conflicting
#    Then  Wait for specific time for the device to startup
#      | time | key_words           |
#      | 5    | password,connecting |
#      | 5    | password,connecting |
#      | 5    | password,connecting |
#    Then  wifi-interface jump to real micro hot-device
#    Then  grant /app folder wr rights
#    Then  Load the srv_trx.conf file
#    Then  Check the parameters of "<devName>","<location>","<serverip>","<serverport>","<height>","<provinceCode>","<cityCode>","<areaCode>","<townCode>" are modified at srv_trx.conf file
#    And   recover the srv_trx.conf file
#    Then  generate the md5 for security
#    Then  reboot the device
#    And   Sleep for a while to let device shutdown
#    Then  Wait for some time for preparing deleting known_hosts
#      | time |
#      | 15   |
#      | 15   |
#      | 15   |
#    Then  Delete the known_hosts for conflicting
#    Then  Wait for specific time for the device to startup
#      | time | key_words           |
#      | 10   | password,connecting |
#      | 10   | password,connecting |
#      | 10   | password,connecting |
#    Then  wifi-interface jump to real micro hot-device
#    Then  Close the ssh client session
#
#    Examples:
#      | devName    | location                 | serverip        | serverport | height | provinceCode | cityCode | areaCode | townCode |
#      | GDB_device | GuangDong Shenzhen LuoHu | 113.108.110.101 | 7705       | 102.00 | 402          | 302      | 422      | 722      |


  @V4.0.1
  Scenario Outline: Smoke testing device config of carrier of CMCC of group 1 parameters,waiting for take effect (V4.0.1)
    When  Set the proper user to login
      | static|
      | no    |
    Then  login real micro hot-device
      | style  |
      | default|
    Then  Delete the factoryflag if it exists
    Then  Compose the request of update device config "<tacMin>","<imsiReportInterval>","<redirectedearfcn>","<redirectedEarfcnFrameOffset>","<qRxLevMin>","<interFreq>","<activeNow>"
    Then  Send the update device config request and expect "Success" in response
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
    Then  Check the parameters of "<tacMin>","<imsiReportInterval>","<redirectedearfcn>","<redirectedEarfcnFrameOffset>","<qRxLevMin>","<interFreq>","<activeNow>" are modified at srv_trx.conf file
    Then  generate the md5 for security
    Then  Delete the factoryflag if it exists
    Then  exit current ssh session

    Examples:
      | tacMin | imsiReportInterval | redirectedearfcn | redirectedEarfcnFrameOffset | qRxLevMin | interFreq | activeNow |
      | 0      | 0                  | 10000            | -1000                       | -70       | 0         | 0         |
#      | 30000  | 1800               | 2000             | 0                           | -70       | 10000     | 0         |
#      | 65530  | 3600               | 38400            | 1000                        | -22       | 39000     | 0         |




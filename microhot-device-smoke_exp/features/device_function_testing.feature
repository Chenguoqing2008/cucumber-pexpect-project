Feature: Smoke testing when new package is updated to "/mnt/code" folder

  Background: Operator needs to a smoke testing of micro-hot device
    Given Operator prepares all the necessary context for testing platform

  @V4.0.0
  Scenario: Operator needs to check if the device can catch IMSI or not(V4.0.0)
     When  Operator login the micro hot-device wifi-interface
      | static|
      | no    |
     Then  Delete the known_hosts for conflicting
     Then  wifi-interface jump to real micro hot-device
     Then  check the deamon.log can catch IMSI
     | time | catch_status |
     | 45   | True,False   |
     | 45   | True,False   |
     | 45   | True,False   |
     | 45   | True,False   |
     | 45   | True,False   |
     | 45   | True,False   |
     | 45   | True,False   |
     | 45   | True,False   |
     | 30   | True         |
     Then  exit current ssh session


  @V4.0.1
  Scenario: Operator needs to check if the device can catch IMSI or not(V4.0.1)
    When  Set the proper user to login
      | static|
      | no    |
    Then  login real micro hot-device
      | style  |
      | default|
    Then  check the deamon.log can catch IMSI
     | time | catch_status |
     | 45   | True,False   |
     | 45   | True,False   |
     | 45   | True,False   |
     | 45   | True,False   |
     | 45   | True,False   |
     | 45   | True,False   |
     | 45   | True,False   |
     | 45   | True,False   |
     | 30   | True         |
    Then  exit current ssh session












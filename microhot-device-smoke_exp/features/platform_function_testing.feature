Feature: Smoke testing of platform_driven functionality

  Background: Operator needs to a smoke testing of micro-hot device
    Given Operator prepares all the necessary context for testing platform


  @V4.0.0
  Scenario: Upgrade package in detect-code platform then check the result at device(V4.0.0)
     Given  Operator upload package in detect-code platform, expect "200" with filename and md5 in response
     Then   Operator add new package to detect-code platform, expect "200" in response
     Then   Operator get the packageVersionId, expect "200" in response
     Then   Compose request body with deviceId and versionId mapping
     When   Operator push new version package to specific deviceId, expect "200" in response
     Then   Operator query with versionId to get versionPushId, expect "200" in response
     Then   Operator query upgrade result api with versionId and versionPushId, expect "200" in response
     Then   Wait for specific time period, the upgradeStatus should be as expected
            """
            Wait is a status of waiting response from device. If client wait for some time and still no response,
            then i take this upgrade status as failure.
            """
      | time| upgrade_status       |
      | 60  | EXECUTION,WAIT,START |
      | 60  | EXECUTION,WAIT,START |
      | 60  | EXECUTION,WAIT,START |
      | 90  | EXECUTION,FINISH     |
      | 90  | EXECUTION,FINISH     |
      | 90  | EXECUTION,FINISH     |
      | 60  | FINISH               |
     When  Operator login the micro hot-device wifi-interface
      | static|
      | no    |
     Then  Delete the known_hosts for conflicting
     Then  wifi-interface jump to real micro hot-device
     Then  Check the package version is correct
     Then  exit current ssh session
     Then  delete the uploaded version and expect "success." in response


  @V4.0.1
  Scenario: Upgrade package in detect-code platform then check the result at device(V4.0.1)
     Given  Operator upload package in detect-code platform, expect "200" with filename and md5 in response
     Then   Operator add new package to detect-code platform, expect "200" in response
     Then   Operator get the packageVersionId, expect "200" in response
     Then   Compose request body with deviceId and versionId mapping
     When   Operator push new version package to specific deviceId, expect "200" in response
     Then   Operator query with versionId to get versionPushId, expect "200" in response
     Then   Operator query upgrade result api with versionId and versionPushId, expect "200" in response
     Then   Wait for specific time period, the upgradeStatus should be as expected
            """
            Wait is a status of waiting response from device. If client wait for some time and still no response,
            then i take this upgrade status as failure.
            """
      | time| upgrade_status       |
      | 60  | EXECUTION,WAIT,START |
      | 60  | EXECUTION,WAIT,START |
      | 60  | EXECUTION,WAIT,START |
      | 90  | EXECUTION,FINISH     |
      | 90  | EXECUTION,FINISH     |
      | 90  | EXECUTION,FINISH     |
      | 60  | FINISH               |
    When  Set the proper user to login
      | static|
      | no    |
    Then  login real micro hot-device
      | style  |
      | default|
     Then  Check the package version is correct
     Then  exit current ssh session
     Then  delete the uploaded version and expect "success." in response












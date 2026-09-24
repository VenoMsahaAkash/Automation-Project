Feature: Embedded Device Web Automation


  Background:
    Given the embedded device web application is available
    And I open the device login page


  Scenario: Successful login and dashboard validation

    When I enter username "admin"
    And I enter password "admin123"
    And I click the Login button

    Then I should see the device dashboard
    And the device status should be "ONLINE"


  Scenario: Change device operating mode

    Given I am logged in

    When I select device mode "POWER_SAVE"
    And I click the Apply Mode button

    Then the device mode should be "POWER_SAVE"


  Scenario: Enable the device feature

    Given I am logged in

    When I click the feature button

    Then the feature status should be "ENABLED"


  Scenario: Invalid login

    When I enter username "wrong"
    And I enter password "wrong"
    And I click the Login button

    Then I should see the login error "Invalid username or password"


  Scenario: Logout

    Given I am logged in

    When I click the Logout link

    Then I should return to the login page
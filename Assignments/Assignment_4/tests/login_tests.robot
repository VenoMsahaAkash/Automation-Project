*** Settings ***
Library    SeleniumLibrary
Resource    ../resources/common_keywords.robot
Resource    ../resources/variables.robot

Suite Setup       Open Application
Suite Teardown    Close Application

*** Test Cases ***
Verify Login Page
    [Tags]    smoke    login
    Page Should Contain Element    xpath=//input[@name='username']
    Page Should Contain Element    xpath=//input[@name='password']
    Log    Login page verified successfully

Login With Valid Credentials
    [Tags]    regression    login
    Input Text    xpath=//input[@name='username']    ${USERNAME}
    Input Text    xpath=//input[@name='password']    ${PASSWORD}
    Log    Login credentials entered
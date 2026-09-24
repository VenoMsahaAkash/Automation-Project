*** Settings ***
Library    SeleniumLibrary
Resource    ../resources/common_keywords.robot

*** Test Cases ***
Data Driven Login Test
    [Template]    Login With Credentials
    user1    password1
    user2    password2
    user3    password3

*** Keywords ***
Login With Credentials
    [Arguments]    ${username}    ${password}
    Input Text    xpath=//input[@name='username']    ${username}
    Input Text    xpath=//input[@name='password']    ${password}
    Log    Testing user: ${username}
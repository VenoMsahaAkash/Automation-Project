*** Settings ***
Library    SeleniumLibrary
Resource    variables.robot

*** Keywords ***

Open Application
    Open Browser    ${BASE_URL}    ${BROWSER}
    Maximize Browser Window
    Log    Application opened successfully

Close Application
    Close All Browsers
    Log    Application closed successfully

Login To Application
    [Arguments]    ${username}    ${password}

    Input Text    xpath=//input[@name='username']    ${username}
    Input Text    xpath=//input[@name='password']    ${password}

    Log    Login details entered

Verify Login Page
    Page Should Contain Element    xpath=//input[@name='username']
    Page Should Contain Element    xpath=//input[@name='password']
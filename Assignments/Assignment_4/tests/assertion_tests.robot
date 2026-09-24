*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
Verify Page Element
    Open Browser    https://example.com    chrome

    Page Should Contain Element    xpath=//body

    Close Browser
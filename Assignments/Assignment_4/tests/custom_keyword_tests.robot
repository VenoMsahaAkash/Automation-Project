*** Settings ***
Library    ../libraries/custom_library.py

*** Test Cases ***
Calculate Sum
    ${result}=    Calculate Sum    10    20
    Should Be Equal As Integers    ${result}    30

Reverse Text
    ${result}=    Reverse Text    Robot
    Should Be Equal    ${result}    toboR

Multiply Numbers
    ${result}=    Multiply Numbers    5    4
    Should Be Equal As Integers    ${result}    20
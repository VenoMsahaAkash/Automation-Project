*** Settings ***
Library    RequestsLibrary
Library    BuiltIn

*** Test Cases ***
Verify API Response
    Create Session    api    https://jsonplaceholder.typicode.com
    ${response}=    GET On Session    api    /posts/1
    Should Be Equal As Integers    ${response.status_code}    200
    ${data}=    Set Variable    ${response.json()}
    Should Be Equal As Integers    ${data}[id]    1
    Log    API Response: ${data}
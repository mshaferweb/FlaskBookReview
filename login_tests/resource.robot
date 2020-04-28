*** Settings ***

Documentation     A resource file with reusable keywords and variables.
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported SeleniumLibrary.
Library           SeleniumLibrary
Library           RequestsLibrary
Library           Collections

Variables         myvariables.py

*** Variables ***
${SERVER}         localhost:5000
${BROWSER}        Chrome
#${BROWSER}        Headless Chrome
${DELAY}          0.2
${VALID USER}     demo1
${VALID PASSWORD}    mode
${LOGIN URL}      http://${SERVER}/
${LOGGED OUT URL}   http://${SERVER}/logout
${LOGGED IN URL}    http://${SERVER}/login
${REGISTER URL}    http://${SERVER}/register
${BOOKS URL}    http://${SERVER}/books
${REVIEW URL}    http://${SERVER}/review
${API URL}    http://${SERVER}/api
${ERROR URL}      http://${SERVER}/error

*** Keywords ***
Open Browser To Login Page
    Open Browser    ${LOGIN URL}    ${BROWSER}
#    Maximize Browser Window
    Set Selenium Speed    ${DELAY}
    Login Page Should Be Open

Login Page Should Be Open
    Title Should Be    Books

Go To Login Page
    Go To    ${LOGIN URL}
    Login Page Should Be Open

Input Login Username
    [Arguments]    ${username}
    Input Text    id:lusername    ${username}${CURRENT_TIME}

Input Login Password
    [Arguments]    ${password}
    Input Text    id:lpassword    ${password}

Input Reg Username
    [Arguments]    ${username}
    Input Text    id:rusername    ${username}${CURRENT_TIME}

Input Reg Password
    [Arguments]    ${password}
    Input Text    id:rpassword    ${password}

Input Book
    [Arguments]    ${book}
    Input Text    id:books    ${book}

Input Book Review
    [Arguments]    ${review}
    Input Text    id:review    ${review}

Input Book Rating
    [Arguments]    ${rating}
    Input Text    id:rating    ${rating}

Submit Credentials
    Click Button    create

Submit Login
    Click Button    login

Switch Register
    Click Link   	switch

Submit Books Search
    Click Button    search_books

Submit Book Review
    Click Button    submit_review

Register Page Should Be Open
    [Arguments]    ${username}
    Location Should Be    ${REGISTER URL}
    Title Should Be    Books
    Page Should Not Contain     Error
    Page Should Contain      Hello, ${username}${CURRENT_TIME}!

Logged In Page Should Be Open
    Location Should Be    ${LOGGED IN URL}
    Title Should Be    Books

Books Result Page Should Open
    [Arguments]    ${book}
    Location Should Be    ${BOOKS URL}
    Page should Contain   ${book}
    Title Should Be    Books

Books Result Page Should Open Multi
    [Arguments]    ${book1}     ${book2}
    Location Should Be    ${BOOKS URL}
    Page should Contain   ${book1}
    Page should Contain   ${book2}
    Title Should Be    Books

Click On Book Link
    [Arguments]    ${isbn}
    Click Link   	/books/${isbn}


Book Detail Page Should Open
    [Arguments]    ${isbn}
    Location Should Be    ${BOOKS URL}/${isbn}
    Page should Contain   ${isbn}
    Title Should Be    Books

Review Page Should Open
    [Arguments]    ${review}
    Location Should Be    ${REVIEW URL}
    Page should Contain   ${review}
    Title Should Be    Books

Click Logout
    Click Link   	logout
    Location Should be      ${LOGGED OUT URL}

Make HTTP Request
    [Arguments]    ${isbn}
    Create Session     bookapi      ${API URL}
    ${resp}=        Get Request    bookapi  /${isbn}
    Status Should Be  200            ${resp}
    LOG     ${resp.json()}
    ${all data members}=    Set Variable     ${resp.json()['books'][0]}
    LOG     ${all data members}
    dictionary should contain value    ${all data members}     ${isbn}


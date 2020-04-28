*** Settings ***
Documentation     A test suite validating books application.
...
...               This test has a workflow that is created using keywords in
...               the imported resource file.
Resource          resource.robot

*** Test Cases ***

Valid Register
    Open Browser To Login Page
    Switch Register
    Input Reg Username    demo2
    Input Reg Password    mode2
    Submit Credentials
    Register Page Should Be Open    demo2
    [Teardown]    Close Browser

Valid User Login
    Open Browser To Login Page
    Input Login Username    demo2
    Input Login Password    mode2
    Submit Login
    Logged In Page Should Be Open
    [Teardown]    Close Browser

Valid User Logout
    Open Browser To Login Page
    Input Login Username    demo2
    Input Login Password    mode2
    Submit Login
    Logged In Page Should Be Open
    Click Logout
    [Teardown]    Close Browser

Search for Book by ISBN
    Open Browser To Login Page
    Input Login Username    demo2
    Input Login Password    mode2
    Submit Login
    Logged In Page Should Be Open
    Input Book   0743454553
    Submit Books Search
    Books Result Page Should Open   0743454553
    [Teardown]    Close Browser

Search for Book by Partial ISBN
    Open Browser To Login Page
    Input Login Username    demo2
    Input Login Password    mode2
    Submit Login
    Logged In Page Should Be Open
    Input Book   21922
    Submit Books Search
    Books Result Page Should Open   21922
    [Teardown]    Close Browser


Search for Book by Title
    Open Browser To Login Page
    Input Login Username    demo2
    Input Login Password    mode2
    Submit Login
    Logged In Page Should Be Open
    Input Book    Lightning Thief
    Submit Books Search
    Books Result Page Should Open    Lightning Thief
    [Teardown]    Close Browser


Search for Book by Author
    Open Browser To Login Page
    Input Login Username    demo2
    Input Login Password    mode2
    Submit Login
    Logged In Page Should Be Open
    Input Book    James Duncan
    Submit Books Search
    Books Result Page Should Open    James Duncan
    [Teardown]    Close Browser


Search for Book Non Existent
    Open Browser To Login Page
    Input Login Username    demo2
    Input Login Password    mode2
    Submit Login
    Logged In Page Should Be Open
    Input Book    This book doesn't exist
    Submit Books Search
    Books Result Page Should Open    No book found
    [Teardown]    Close Browser



Search for Book by Partial Title Multiple Results
    Open Browser To Login Page
    Input Login Username    demo2
    Input Login Password    mode2
    Submit Login
    Logged In Page Should Be Open
    Input Book    a
    Submit Books Search
    Books Result Page Should Open Multi    Krondor: The Betrayal  The Dark Is Rising
    [Teardown]    Close Browser


Search for Book by Title and Click to Book
    Open Browser To Login Page
    Input Login Username    demo2
    Input Login Password    mode2
    Submit Login
    Logged In Page Should Be Open
    Input Book    Daisy Miller
    Submit Books Search
    Books Result Page Should Open    Daisy Miller
    Click On Book Link      1592243002
    Book Detail Page Should Open    1592243002
    [Teardown]    Close Browser


Search for Book by Title Click to Book and Submit Review
    Open Browser To Login Page
    Input Login Username    demo2
    Input Login Password    mode2
    Submit Login
    Logged In Page Should Be Open
    Input Book    Daisy Miller
    Submit Books Search
    Books Result Page Should Open    Daisy Miller
    Click On Book Link      1592243002
    Book Detail Page Should Open    1592243002
    Input Book Review    Daisy Miller is a great book ${CURRENT_TIME}
    Input Book Rating    5
    Submit Book Review
    Review Page Should Open    Daisy Miller is a great book ${CURRENT_TIME}
    [Teardown]    Close Browser

Review Submission Review_greater than 5
    Open Browser To Login Page
    Input Login Username    demo2
    Input Login Password    mode2
    Submit Login
    Logged In Page Should Be Open
    Input Book    Daisy Miller
    Submit Books Search
    Books Result Page Should Open    Daisy Miller
    Click On Book Link      1592243002
    Book Detail Page Should Open    1592243002
    Input Book Review    Daisy Miller is a great book ${CURRENT_TIME}
    Input Book Rating    6
    Submit Book Review
    Review Page Should Open    Rating needs to be between 1 and 5
    [Teardown]    Close Browser

User Cant Submit Multiple Reviews Same Book
    Open Browser To Login Page
    Input Login Username    demo2
    Input Login Password    mode2
    Submit Login
    Logged In Page Should Be Open
    Input Book    Daisy Miller
    Submit Books Search
    Books Result Page Should Open    Daisy Miller
    Click On Book Link      1592243002
    Book Detail Page Should Open    1592243002
    Input Book Review    Daisy Miller is a great book ${CURRENT_TIME}
    Input Book Rating    5
    Submit Book Review
    Review Page Should Open    User cant submit two reviews for the same book
    [Teardown]    Close Browser

Make HTTP Request for JSON Book Result
    Make HTTP Request   1592243002
*** Test Cases ***
Login Test 1
    Open Browser    http://site.com    chrome
    Sleep    5s
    Click Element    /html/body/div[2]/button
    Input Text      //*[@id="email"]    user@example.com

Login Test 2
    Open Browser    http://site.com    chrome
    Sleep    5s
    Click Element    /html/body/div[2]/button
    Input Text      //*[@id="email"]    user@example.com

Logout Test
    Sleep    3s
    Click Element    /html/body/nav/button[3]
    Sleep    2s

*** Settings ***
Library  OperatingSystem
Library  JSONLibrary
Library  Process

*** Test Cases ***
Create Binary File
    ${result}=     RUN PROCESS  python3    cli.py  bin-create  root/   bin1     content
    ${json}=   Convert String to JSON  ${result.stdout}
    should be true  ${json['success']}

Delete Binary File
    ${result}=     RUN PROCESS  python3    cli.py  bin-delete  root/bin1
    ${json}=   Convert String to JSON  ${result.stdout}
    should be true  ${json['success']}

Create Directory
    ${result}=     RUN PROCESS  python3    cli.py  dir-create  root/   dir76
    ${json}=   Convert String to JSON  ${result.stdout}
    should be true  ${json['success']}

Create Log File
    ${result}=     RUN PROCESS  python3    cli.py  log-create  root/   log1
    ${json}=   Convert String to JSON  ${result.stdout}
    should be true  ${json['success']}

Delete Log File
    ${result}=     RUN PROCESS  python3    cli.py  log-delete   root/log1
    ${json}=   Convert String to JSON  ${result.stdout}
    should be true  ${json['success']}

Create Buffer File
    ${result}=     RUN PROCESS  python3    cli.py  buff-create  root/   buff1
    ${json}=   Convert String to JSON  ${result.stdout}
    should be true  ${json['success']}

Delete Buffer File
    ${result}=     RUN PROCESS  python3    cli.py  buff-delete  root/buff1
    ${json}=   Convert String to JSON  ${result.stdout}
    should be true  ${json['success']}

Create Directory With Same Name
    ${result}=     RUN PROCESS  python3    cli.py  dir-create  root/   dir76
    Log  ${result.stdout}
    ${json}=   Convert String to JSON  ${result.stdout}
    should be equal as strings  ${json["error_message"]}    Directory creation failed

Delete Directory
    ${result}=     RUN PROCESS  python3    cli.py  dir-delete  root/dir76
    ${json}=   Convert String to JSON  ${result.stdout}
    should be true  ${json['success']}

Create File With Same Name
    ${result}=     RUN PROCESS  python3    cli.py  log-create  root/   log1
    ${json}=   Convert String to JSON  ${result.stdout}
    should be equal as strings  ${json["error_message"]}    File creation failed


Create Directory With With Wrong Path
    ${result}=     RUN PROCESS  python3    cli.py  dir-create  root/asdfsd/asdasd   dir76
    ${json}=   Convert String to JSON  ${result.stdout}
    should be equal as strings  ${json["error_message"]}    Directory creation failed

Delete Not Existing File
    ${result}=     RUN PROCESS  python3    cli.py  log-delete  root/sdfsdf/sdfsdf
    ${json}=   Convert String to JSON  ${result.stdout}
    should be equal as strings  ${json['error_message']}   LogFile not found

Delete Not Existing Directory
    ${result}=     RUN PROCESS  python3    cli.py  dir-delete  root/sdfsdf/sdfsdf
    ${json}=   Convert String to JSON  ${result.stdout}
    should be equal as strings  ${json['error_message']}   Directory not found

Delete Wrong File Type
    RUN PROCESS  python3    app.py  log-create  root/   log1
    ${result}=     RUN PROCESS  python3    cli.py  buff-delete  root/log1
    ${json}=   Convert String to JSON  ${result.stdout}
    should be equal as strings  ${json['error_message']}   BufferFile not found

Log Line To LogFile
    ${result}=  RUN PROCESS  python3    cli.py  log-log  root/log1  line
    ${json}=   Convert String to JSON  ${result.stdout}
    should be true  ${json['success']}

Log Line To Not LogFile
    RUN PROCESS  python3    cli.py  buff-create  root/   buff1
    ${result}=  RUN PROCESS  python3    cli.py  log-log  root/buff1  line
    ${json}=   Convert String to JSON  ${result.stdout}
    should be equal as strings  ${json['error_message']}    File do not supports logging

Push Element To BufferFile
    ${result}=  RUN PROCESS  python3    cli.py  buff-push  root/buff1  element1
    ${json}=   Convert String to JSON  ${result.stdout}
    should be true  ${json['success']}


    *** Keywords ***
Read And Parse Output
    [Arguments]  ${path}
    ${file_content}=  Get File  ${path}
    ${json}=          Load JSON From String  ${file_content}
    Should Be True    ${json['success']}
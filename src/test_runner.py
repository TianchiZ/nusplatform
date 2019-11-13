import os
import json
#import pytest


def store_content(shownCode, editedCode):
    # testExample.py - shownCode
    # example.py     - editedCode
    os.popen("mkdir -p /tmp/myProject").read()
    with open('/tmp/myProject/example.py', 'w') as outFile:
        outFile.write(editedCode)
    with open('/tmp/myProject/testExample.py', 'w') as outFile:
        outFile.write(shownCode)


def execute():
    # To access custom packages
    os.environ['PATH'] = os.environ['PATH'] + ":" + "/var/task/bin"

    #set_command = "cp /var/task/ansi2html.sh /tmp/ansi2html.sh && chmod 777 /tmp/ansi2html.sh"
    #os.popen(set_command).read()

    # Get text feedback of unit test results
    runUnitTest = 'cd /tmp/myProject/; python3 -m unittest -v testExample.py 2>&1'
    unitTestResults = os.popen(runUnitTest).read()

    # Get html feedback of unit test results
    command = "cd /tmp/myProject/; python3 -m unittest -v testExample.py 2>&1 | \
                /tmp/ansi2html.sh > /tmp/myProject/unitTestResults.html"
    os.popen(command).read()
    htmlOutput = "<h2>Python unittest results</h2><br/>"
    htmlOutput += os.popen("cat /tmp/myProject/unitTestResults.html").read()

    # Get JSON feedback of unit test results
    command = "python3 -m pytest --json-report -v /tmp/myProject/testExample.py \
            --json-report-summary --json-report-file /tmp/myProject/unitTestResults.json"
    os.popen(command).read()
    jsonOutput = json.loads(os.popen("cat /tmp/myProject/unitTestResults.json").read())

    # Get isComplete
    if ("summary" in jsonOutput):
        if("failed" in jsonOutput["summary"]):
            isComplete = False
        elif(jsonOutput["summary"].get("total", 0) == jsonOutput["summary"].get("passed", 1)):
            isComplete = True
        else:
            isComplete = False
    else:
        isComplete = False

    # Form the response
    results = {
        "isComplete": isComplete,
        "htmlFeedback": htmlOutput,
        "jsonFeedback": jsonOutput,
        "textFeedback": unitTestResults
    }

    return json.dumps(results)

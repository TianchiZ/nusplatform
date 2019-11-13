import json
import get_contents
import test_runner
import os


def lambda_handler(event, context):
    method = event.get('httpMethod', {})
    indexPage = get_contents.getIndexPage()

    set_command = "cp /var/task/ansi2html.sh /tmp/ansi2html.sh && chmod 777 /tmp/ansi2html.sh"
    os.popen(set_command).read()

    if method == 'GET':
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'text/html',
            },
            "body": indexPage
        }
    if method == 'POST':
        bodyContent = event.get('body', {})
        parsedBodyContent = json.loads(bodyContent)
        shownCode = parsedBodyContent["shown"]["0"]
        editedCode = parsedBodyContent["editable"]["0"]
        #hidden = parsedBodyContent["hidden"]["0"]
        test_runner.store_content(shownCode, editedCode)
        unitTestResults = test_runner.execute()
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'text/html',
            },
            "body": unitTestResults
        }

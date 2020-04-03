""" exit codes for checker """

OK = 101  # operation has been finished sucessfully
CORRUPT = 102  # service is working, but there is no correct flag (only for "get" ops)
MUMBLE = 103  # service is working incorrect (iex: not responding to the protocol)
DOWN = 104  # service not working (iex: no tcp connection can be initialized)
CHECKER_ERROR = 110  # something gone wrong with args or with remote part of checker

# yandex cloud error response
YC_ERROR = {
    'statusCode': CHECKER_ERROR,
    'headers': {
        'Content-Type': 'text/plain'
    },
    'isBase64Encoded': False,
    'body': ""
}
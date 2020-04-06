import requests

#your IAM token
iam_token = ""

folder_id = ""

url = "https://vpc.api.cloud.yandex.net/vpc/v1/networks"



headers = {
    "Authorization": "Bearer {}".format(iam_token)
}


#parameters for GET
params = {
    "folderId": folder_id
    #key: value
}


#parameters for POST
data = {
    "folderId": folder_id
    #key: value
}

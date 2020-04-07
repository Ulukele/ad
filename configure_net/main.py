import requests
import os

#your IAM token
iam_token = os.environ.get('YANDEX_CLOUD_IAM_TOKEN')

#where nets should be created
folder_id = ""

url = "https://vpc.api.cloud.yandex.net/vpc/v1/networks"



headers = {
    "Authorization": "Bearer {}".format(iam_token)
}


#parameters for GET
params = {
    'folderId': folder_id
    #key: value
}


#parameters for POST
data = {
    'folderId': folder_id
    #key: value
}


TEAM = "team-{}"
DESCRIPTION = "net created for {}"
SUBNET_CIDR = "192.168.50.0/24"


def create_subnet(network_id, name="subnet-1", description=""):

    data_ = data.copy()
    data_['networkId'] = network_id
    data_['v4CidrBlocks'] = [
        SUBNET_CIDR
    ]
    data_['name'] = name
    data_['description'] = description

    return requests.post(url=url, headers=headers, json=data_)

def create_net(name, description=""):

    data_ = data.copy()
    data_['name'] = name
    data_['description'] = description

    return requests.post(url=url, headers=headers, json=data_)

def get_nets_list():

    response = requests.get(url=url, headers=headers, params=params)

    if response.status_code == 200:
        response_json = response.json()
        return response_json['networks']
    else:
        return []


if __name__ == '__main__':

    while(True):
        try:
            teams_num = int(input('how many teams: '))
            break
        except:
            print('you should write a number')

    for net in range(teams_num):
        
        name = TEAM.format(net)
        description = DESCRIPTION.format(name)
        response = create_net(name, description)
        if response.status_code != 200:
            print('=========')
            print('Error with {}:'.format(name))
            print(response)
            print(response.text)
            print('=========')
        else:
            print('net for {} created successfully'.format(name))

    nets = get_nets_list()

    for net in nets:
        if net['name'][:4] == 'team':
            response = create_subnet(net['id'])
            if response.status_code != 200:
                print(response)
                print(response.text)
            else:
                print('subnetnet for net: {} created successfully'.format(net['id']))
        else:
            print('subnet for {} not created because its not team net'.format(net['name']))
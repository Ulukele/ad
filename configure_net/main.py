import requests
import os

from conf_params import *


#your IAM token
iam_token = os.environ.get('YANDEX_CLOUD_IAM_TOKEN')


headers = {
    "Authorization": "Bearer {}".format(iam_token)
}


def create_vm(subnet_id):

    #edit VM parameters here

    """
    platformId (more info in yandex cloud documentation):
        Intel Broadwell: standard-v1
        Intel Cascade Lake: standard-v2
        Intel Broadwell with NVIDIA Tesla V100: gpu-standard-v1
    """

    """
    resourcesSpec. Computing parameters
        memory: in bytes
        cores: (min 1, max 32)
        coreFraction: in percents
        gpus (optional)
    """

    """
    bootDiskSpec. Disk configuration
        mode (optional)
        deviceName (optional)
        autoDelete (optional)
        diskSpec:
            name (optional)
            description (optional)
            typeId (optional): HDD or SSD
            size: in bytes (min: 4194304; max: 4398046511104)
            imageId (optional)
            snapshotId (optional)
        diskId - can be used instead of 'diskSpec'
    """

    """
    networkInterfaceSpecs[]. Network configuration
        subnetId the only required parameter
    """

    """
    schedulingPolicy
        preemptible the only parameter 
    """

    
    data = {
        'folderId': FOLDER_ID,
        'zoneId': ZONE_ID,
        'platformId': "standard-v1",
        'resourcesSpec': {
            'memory': "1073741824",
            'cores': "1",
            'coreFraction': "5",
        },
        'bootDiskSpec': {
            'size': '4194304'
        },
        'networkInterfaceSpecs': [
            {
                'subnetId': subnet_id
            }
        ],
        'schedulingPolicy': {
            'preemptible': True
        }
    }


def create_subnet(network_id, name="subnet-1", description=""):

    data = {
        'folderId': FOLDER_ID,
        'networkId': network_id,
        'v4CidrBlocks': [
            SUBNET_CIDR
        ],
        'name': name,
        'description': description
    }

    return requests.post(url=URL_VPC, headers=headers, json=data)

def create_net(name, description=""):

    data = {
        'folderId': FOLDER_ID,
        'name': name,
        'description': description
    }

    return requests.post(url=URL_VPC, headers=headers, json=data)

def get_nets_list():


    params = {
        'folderId': FOLDER_ID
    }

    response = requests.get(url=URL_VPC, headers=headers, params=params)

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
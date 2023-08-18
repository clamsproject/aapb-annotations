import json
import os
from urllib.parse import urljoin

import requests


def download_golds(gold_dir_url=None, folder_name=None):
    import tempfile
    # code adapt from Angela Lam's

    if folder_name is None:
        folder_name = tempfile.TemporaryDirectory().name
    # Create a new directory to store the downloaded files on local computer
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    # Check if the directory is empty
    if not (len(os.listdir(folder_name)) == 0):
        raise Exception("The folder '" + folder_name + "' already exists and is not empty")

    # Send a GET request to the repository URL and extract the HTML content
    response = requests.get(gold_dir_url)
    
    # github responses with JSON? wow
    payload = json.loads(response.text)['payload']
    links = [i['path'] for i in payload['tree']['items']]

    # Download each file in the links list into the created folder
    for link in links:
        raw_url = urljoin('https://raw.githubusercontent.com/',
                          '/'.join((payload['repo']['ownerLogin'],
                                    payload['repo']['name'],
                                    payload['refInfo']['name'],
                                    link)))
        file_name = os.path.basename(link)
        file_path = os.path.join(folder_name, file_name)
        with open(file_path, 'wb') as file:
            response = requests.get(raw_url)
            file.write(response.content)
    return folder_name

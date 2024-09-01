import json, os, time
from azure.cosmos import CosmosClient, PartitionKey
from azure.storage.filedatalake import DataLakeServiceClient
import datetime

import config

HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']
DATABASE_ID = config.settings['database_id']
CONTAINER_ID = config.settings['container_id']
ADLS_ACCOUNT_NAME = config.settings['adls_account_name']
ADLS_ACCESS_KEY = config.settings['adls_access_key']
ADLS_FILE_SYSTEM = config.settings['adls_file_system']

src_json_path = '/home/mike/Desktop/C&F_Azure/jsons'
json_files = [filename for filename in os.listdir(src_json_path) if filename.endswith('.json')]

src_media_path = '/home/mike/Desktop/C&F_Azure/media'
media_files = [filename for filename in os.listdir(src_media_path) if filename.endswith('.mp4') or filename.endswith('.jpg')]

azure_storage = 'https://20240901candf.blob.core.windows.net'
remote_file_path = 'media/'

#media uploader
account_url = f"https://{ADLS_ACCOUNT_NAME}.dfs.core.windows.net"
service_client = DataLakeServiceClient(account_url, credential={'account_name': ADLS_ACCOUNT_NAME, 'account_key': ADLS_ACCESS_KEY})
file_system_client = service_client.get_file_system_client(ADLS_FILE_SYSTEM)

def dataLoader(file_data):
    client = CosmosClient(HOST, MASTER_KEY)
    database_name = DATABASE_ID
    container_name = CONTAINER_ID
    database = client.create_database_if_not_exists(id=database_name)
    container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/id"),
        offer_throughput=400
    )
    container.create_item(body=file_data)

def mediaUploader(media_file, data):
    file_client = file_system_client.get_file_client(f'{remote_file_path}{media_file}')
    file_client.upload_data(data, overwrite=True)

json_files_amount = str(len(json_files))
num = 1
for json_file in json_files:
    print(f"[{str(num)}/{json_files_amount}] {json_file} uploaded.")
    with open(f'{src_json_path}/{json_file}') as file:
        file_data = json.load(file)
        dataLoader(file_data)
    num += 1

media_files_amount = str(len(media_files))
num = 1
for media_file in media_files:
    with open(f'{src_media_path}/{media_file}', 'rb') as data:
        print(f"[{str(num)}/{media_files_amount}] {media_file} uploaded.")
        mediaUploader(media_file, data)
    num += 1
import os

settings = {
    'host': os.environ.get('ACCOUNT_HOST', 'https://20240901-cosmosdb-candf.documents.azure.com:443/'),
    'master_key': os.environ.get('ACCOUNT_KEY', ''),
    'database_id': os.environ.get('COSMOS_DATABASE', 'candf'),
    'container_id': os.environ.get('COSMOS_CONTAINER', 'instagram_posts'),
    'adls_account_name': os.environ.get('ADLS_ACCOUNT_NAME', '20240901candf'),
    'adls_access_key': os.environ.get('ADLS_ACCESS_KEY', ''),
    'adls_file_system': os.environ.get('ADLS_FILE_SYSTEM', 'instagram'),
}
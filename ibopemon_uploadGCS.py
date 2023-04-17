from google.cloud import storage
import glob
import os

# Get the current working directory
cwd = os.getcwd()
os.chdir('c:\\projects\\sno\\data\export\\')
print("Current working directory: {0}".format(cwd))

path_to_private_key = 'C:\\key\\datalab-sno.json'
client = storage.Client.from_service_account_json(json_credentials_path=path_to_private_key)
bucket = storage.Bucket(client, 'klienta_informcentro_monitor')

for str_path_file in glob.glob('**'):
    print(f'Uploading {str_path_file}')
    # The name of file on GCS once uploaded
    blob = bucket.blob(str_path_file)
    # The content that will be uploaded
    blob.upload_from_filename(str_path_file)
    print(f'Path in GCS: {str_path_file}')
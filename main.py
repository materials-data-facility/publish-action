# main.py
import sys
import boto3

from mdf_connect_client import MDFConnectClient
import mdf_toolbox
import os

current_working_directory = os.getcwd()

_, globus_auth_client_id, globus_auth_secret, \
   paths_to_publish, mdf_source_id, mdf_title, mdf_authors, mdf_affiliations, \
    mdf_publication_year, staging_object_store_url, is_test_str, aws_access_key_id, \
    aws_secret_access_key, s3_bucket_id, s3_bucket_path = sys.argv 

is_test = is_test_str == "true"

s3 = boto3.client('s3',
                  endpoint_url=staging_object_store_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)


def upload_s3(bucket_id, object_path, file):
    print(f"Uploading {file}")
    with open(file, "rb") as f:
        s3.upload_fileobj(f, bucket_id, object_path)

    url = s3.generate_presigned_url(
    ClientMethod='get_object', 
    Params={
        'Bucket': bucket_id,
        'Key': object_path
    })

    return url

def mdf_publish(source_urls):
    auths = mdf_toolbox.confidential_login(client_id=globus_auth_client_id,
                                        client_secret=globus_auth_secret,
                                        services=["mdf_connect", "mdf_connect_dev"],
                                        make_clients=True)

    mdfcc = MDFConnectClient(authorizer=auths['mdf_connect'])

    mdfcc.create_dc_block(title=mdf_title, authors=mdf_authors, affiliations=mdf_affiliations, publication_year=mdf_publication_year)

    mdfcc.set_test(is_test)

    for url in source_urls:
        mdfcc.add_data_source(url)

    mdfcc.add_service("mdf_publish")

    if mdf_source_id:
        mdfcc.set_incremental_update(mdf_source_id)

    print("MDF Submission: ", mdfcc.get_submission())

    is_update = bool(mdf_source_id)

    submit_response = mdfcc.submit_dataset(update=is_update)

    print("MDF Submit Update Response: ", submit_response)

    if not submit_response['success']:
        print(f"Submission Failed: {submit_response['error']}")
        sys.exit(1)


def list_files(path, recursive=False):
    """
    Recursively list files in a directory.

    Args:
    path: The directory to list files in.
    recursive: Whether to recursively list files in subdirectories.

    Returns:
    A list of file paths.
    """
    files = []
    if os.path.isfile(path):
        files.append(path)
    elif os.path.isdir(path):
        for item in os.listdir(path):
          item_path = os.path.join(path, item)
          if os.path.isfile(item_path):
            files.append(item_path)
          elif recursive and os.path.isdir(item_path):
            files += list_files(item_path, recursive)
    return files

def main():
    print('Input Data:-')
    print(f'Globus Auth Client ID: {globus_auth_client_id}')
    print(f'Globus Auth Secret: {globus_auth_secret}')
    print(f'Paths to Publish: {paths_to_publish}')
    print(f'MDF Source ID: {mdf_source_id}')
    print(f'MDF Title: {mdf_title}')
    print(f'MDF Authors: {mdf_authors}')
    print(f'MDF Affiliations: {mdf_affiliations}')
    print(f'MDF Publication Year: {mdf_publication_year}')
    print(f'Staging Object Store URL: {staging_object_store_url}')
    print(f'Is Test: {is_test_str} -> {is_test}')
    print(f'AWS Access Key ID: {aws_access_key_id}')
    print(f'AWS Secret Access Key: {aws_secret_access_key}')
    print(f'S3 Bucket ID: {s3_bucket_id}')
    print(f'S3 Bucket Path: {s3_bucket_path}')

    path_list = [path.lstrip() for path in paths_to_publish.split(",")]

    source_urls = []
    for path in path_list:
        print(f"Searchiung in {path}")
        files = list_files(path, recursive=True)
        print(f"Files = {files}")
        for file in files: 
            source_urls.append(upload_s3(s3_bucket_id, f"{s3_bucket_path}{file}", file))

    mdf_publish(source_urls)

if __name__ == "__main__": 
    main()
    print("Publish success")
    sys.exit(0)
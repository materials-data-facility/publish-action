# main.py
import sys
import boto3

from mdf_connect_client import MDFConnectClient
import mdf_toolbox
import os


_, globus_auth_client_id, globus_auth_secret, \
    mdf_source_id, mdf_title, mdf_authors, mdf_affiliations, \
    mdf_publication_year, related_dois, paths_to_publish, is_test_str, \
    staging_object_store_url, aws_access_key_id, \
    aws_secret_access_key, s3_bucket_id, s3_bucket_path = sys.argv 

is_test = is_test_str == "true"

s3 = boto3.client('s3',
                  endpoint_url=staging_object_store_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)


# Set the output value by writing to the outputs in the Environment File, mimicking the behavior defined here:
#  https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-an-output-parameter
def set_github_action_output(output_name, output_value):
    f = open(os.path.abspath(os.environ["GITHUB_OUTPUT"]), "a")
    f.write(f'{output_name}={output_value}')
    f.close()    

def transform_list(list_str: str) -> list[str]:
    return [entry.lstrip() for entry in list_str.split(",")]

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

def mdf_publish(source_urls) -> str:
    auths = mdf_toolbox.confidential_login(client_id=globus_auth_client_id,
                                        client_secret=globus_auth_secret,
                                        services=["mdf_connect", "mdf_connect_dev"],
                                        make_clients=True)

    mdfcc = MDFConnectClient(authorizer=auths['mdf_connect'])

    mdfcc.create_dc_block(title=mdf_title, authors=transform_list(mdf_authors),
                          affiliations=transform_list(mdf_affiliations),
                          related_dois=transform_list(related_dois),
                          publication_year=mdf_publication_year)

    mdfcc.set_test(is_test)

    for url in source_urls:
        mdfcc.add_data_source(url)

    mdfcc.add_service("mdf_publish")

    # If they provide us with a source ID then assume this is an update to that dataset
    is_update = bool(mdf_source_id)


    if is_update:
        mdfcc.set_incremental_update(mdf_source_id)


    print(mdfcc.get_submission())
    submit_response = mdfcc.submit_dataset(update=is_update)

    print("MDF Submit Update Response: ", submit_response)

    if not submit_response['success']:
        print(f"Submission Failed: {submit_response['error']}")
        sys.exit(1)

    return submit_response['source_id']


def list_files(path, recursive=False):
    """
    Recursively list files in a directory. Works with a single file or a directory.
    If you provide a directory it will return the list of files in that directory. If
    you provide a filename then it just adds that file

    Args:
    path: The filenam or directory to list files in.
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

    # Construct the list of files we will want to upload to MDF. Don't be 
    # confused by leading spaces in the list
    path_list = [path.lstrip() for path in paths_to_publish.split(",")]

    # Construct pre-signed URLs for each file by uploading to our staging bucket
    source_urls = []
    for path in path_list:
        files = list_files(path, recursive=True)
        for file in files: 
            source_urls.append(upload_s3(s3_bucket_id, f"{s3_bucket_path}{file}", file))

    source_id = mdf_publish(source_urls)
    return source_id

if __name__ == "__main__": 
    source_id = main()
    set_github_action_output('source_id', source_id)

    print(f"Publish success - SourceID = {source_id}")
    sys.exit(0)

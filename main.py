# main.py
import sys
import boto3
from mdf_connect_client import MDFConnectClient
import mdf_toolbox

_, globus_auth_client_id, globus_auth_secret, \
    files_to_publish, mdf_source_id, mdf_title, mdf_authors, mdf_affiliations, \
    mdf_publication_year, staging_object_store_url, aws_access_key_id, \
    aws_secret_access_key, s3_bucket_id, s3_bucket_path = sys.argv 

s3 = boto3.client('s3',
                  endpoint_url=staging_object_store_url,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)


def upload_s3(bucket_id, object_path, file):
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

    for url in source_urls:
        mdfcc.add_data_source(url)

    mdfcc.add_service("mdf_publish")

    if mdf_source_id:
        mdfcc.set_incremental_update(mdf_source_id)

    print("MDF Submission: ", mdfcc.get_submission())

    if mdf_source_id:
        submit_response = mdfcc.submit_dataset(update=True)
        print("MDF Submit Update Response: ", submit_response)
        if submit_response["status_code"] != "200":
            sys.exit(1)
    else:
        submit_response = mdfcc.submit_dataset()
        print("MDF Submit Original Response: ", submit_response)
        if submit_response["status_code"] != "200":
            sys.exit(1)

def main():
    print('Input Data:-')
    print(f'Globus Auth Client ID: {globus_auth_client_id}')
    print(f'Globus Auth Secret: {globus_auth_secret}')
    print(f'Files to Publish: {files_to_publish}')
    print(f'MDF Source ID: {mdf_source_id}')
    print(f'MDF Title: {mdf_title}')
    print(f'MDF Authors: {mdf_authors}')
    print(f'MDF Affiliations: {mdf_affiliations}')
    print(f'MDF Publication Year: {mdf_publication_year}')
    print(f'Staging Object Store URL: {staging_object_store_url}')
    print(f'AWS Access Key ID: {aws_access_key_id}')
    print(f'AWS Secret Access Key: {aws_secret_access_key}')
    print(f'S3 Bucket ID: {s3_bucket_id}')
    print(f'S3 Bucket Path: {s3_bucket_path}')

    files_list = files_to_publish.split(",")


    source_urls = []
    for file in files_list:
        source_urls.append(upload_s3(s3_bucket_id, f"{s3_bucket_path}{file}", file))

    mdf_publish(source_urls)

if __name__ == "__main__": 
    main()
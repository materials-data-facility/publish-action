# main.py
import sys
import boto3

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

    print(source_urls)




 
if __name__ == "__main__": 
    main()
# main.py
import sys

def main():

    # Get action inputs
    _, globus_auth_client_id, globus_auth_secret, \
    files_to_publish, mdf_source_id, mdf_title, mdf_authors, mdf_affiliations, \
    mdf_publication_year, staging_object_store_url, aws_access_key_id, \
    aws_secret_access_key, s3_bucket_id, s3_bucket_path = sys.argv 

    logs = []
    logs.append('Input Data:-')
    logs.append(f'Globus Auth Client ID: {globus_auth_client_id}')
    logs.append(f'Globus Auth Secret: {globus_auth_secret}')
    logs.append(f'Files to Publish: {files_to_publish}')
    logs.append(f'MDF Source ID: {mdf_source_id}')
    logs.append(f'MDF Title: {mdf_title}')
    logs.append(f'MDF Authors: {mdf_authors}')
    logs.append(f'MDF Affiliations: {mdf_affiliations}')
    logs.append(f'MDF Publication Year: {mdf_publication_year}')
    logs.append(f'Staging Object Store URL: {staging_object_store_url}')
    logs.append(f'AWS Access Key ID: {aws_access_key_id}')
    logs.append(f'AWS Secret Access Key: {aws_secret_access_key}')
    logs.append(f'S3 Bucket ID: {s3_bucket_id}')
    logs.append(f'S3 Bucket Path: {s3_bucket_path}')

    # # Process data
    # if source_format == 'csv':
    #     df = pd.read_csv(source_url)
    # elif source_format == 'json':
    #     df = pd.read_json(source_url)
    
    # if transform == 'normalize':
    #     df = normalize(df)
    # elif transform == 'aggregate':
    #     df = aggregate(df)
    
    # # Output results 
    # if output_format == 'csv':
    #     out_csv = df.to_csv()
    #     Path('/results/out.csv').write_text(out_csv)
    #     print(f'::set-output name=results_url::https://store/results/out.csv') 
    # elif output_format == 'json':
    #     out_json = df.to_json()
    #     Path('/results/out.json').write_text(out_json)
    #     print(f'::set-output name=results_url::https://store/results/out.json') 
    
    # # Output metrics
    # row_count = len(df)

    output_logs = "\n".join(logs)
    print(f'::set-output name=logs::{output_logs}')
 
if __name__ == "__main__": 
    main()
# publish-action
GitHub Action to Publish Dataset to Materials Data Facility by uploading files to an
Object Store staging area.

## Arguments:
| Argument | Description |
| -------- | ----------- |
|  globus_auth_client_id| ID for Globus client that has MDF publish permissions|
|  globus_auth_secret| Client secret |
|  mdf_source_id| Provide the source ID of existing dataset if this is an update. |
|  mdf_title| Dataset title |
|  mdf_authors| List of dataset authors |
|  mdf_affiliations| Coresponding list of author affiliations |
|  mdf_publication_year| Publication year |
|  paths_to_publish| Comma seperated list of paths in this repo to publish. Can be a file or a directory|
|  is_test| Set to `true` if you want to publish to test MDF index and not prod |
|  staging_object_store_url| Objectstore endpoint URL |
|  aws_access_key_id| Access key to object store|
|  aws_secret_access_key| Object store secret |
|  s3_bucket_id| Bucket name to write staging files |
|  s3_bucket_path| Path within bucket to write staging files |

## How to use:

Here is an example GitHub action workflow:
```yaml
name: Publish HDF Data to S3 and MDF

env:
  AWS_ENDPOINT_URL: ${{ secrets.AWS_S3_ENDPOINT }}
  AWS_S3_BUCKET: ${{ secrets.AWS_S3_BUCKET }}
  AWS_S3_BUCKET_PATH: ${{ secrets. AWS_S3_BUCKET_PATH }}
  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
  GLOBUS_CLIENT_ID: ${{ secrets.GLOBUS_CLIENT_ID }}
  GLOBUS_CLIENT_SECRET: ${{ secrets.GLOBUS_CLIENT_SECRET }}
  AWS_S3_USE_PATH_STYLE_ENDPOINT: true
  AWS_EC2_METADATA_DISABLED: true

on:
  release:
    types: [published]

jobs:
  push_publish_job:
    runs-on: ubuntu-latest
    name: Job to Push Data to Object Store and Publish to MDF
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Push and Publish Step
        uses: materials-data-facility/publish-action@v1.1
        id: push_publish
        with:
          globus_auth_client_id: ${{ env.GLOBUS_CLIENT_ID }}
          globus_auth_secret: ${{ env.GLOBUS_CLIENT_SECRET }}
          mdf_source_id: "_test_shriram_readme_file_qmc_v1.1"
          mdf_title: "Readme File for QMC Data"
          mdf_authors: "Shriram, Ben"
          mdf_affiliations: "UIUC, NCSA"
          mdf_publication_year: "2023"

          paths_to_publish: "README.md, 0_interlayer_energy/data"

          is_test: true
          
          staging_object_store_url: ${{ env.AWS_ENDPOINT_URL }}
          aws_access_key_id: ${{ env.AWS_ACCESS_KEY_ID }}
          aws_secret_access_key: ${{ env.AWS_SECRET_ACCESS_KEY }}
          s3_bucket_id: ${{ env.AWS_S3_BUCKET }}
          s3_bucket_path: ${{ env.AWS_S3_BUCKET_PATH }}

```





import boto3  # Python Amazon SDK library. 
import configparser ## Library used to read config files.

def delete_iamrole(config):
        iam = boto3.client('iam', aws_access_key_id=config.get('AWS', 'KEY'),
                   aws_secret_access_key=config.get('AWS', 'SECRET'),
                   region_name='us-west-2'
                   )
        iam.detach_role_policy(RoleName=config.get("IAM_ROLE", "ROLE_NAME"), PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess")
        iam.delete_role(RoleName=config.get("IAM_ROLE", "ROLE_NAME"))



def delete_cluster(config):
    redshift = boto3.client('redshift', region_name="us-west-2", aws_access_key_id=config.get('AWS', 'KEY'),
                                aws_secret_access_key=config.get('AWS', 'SECRET'))
    redshift.delete_cluster( ClusterIdentifier=config.get("DWH", "CLUSTER_IDENTIFIER"),  SkipFinalClusterSnapshot=True)


def main():
    config = configparser.ConfigParser()
    config.read_file(open('dwh.cfg'))

    delete_iamrole(config)
    delete_cluster(config)

    

if __name__ == "__main__":
    main()
import pandas as pd
import json  
import boto3 # Python Amazon SDK library. 
import configparser ## Library used to read config files.


def prettyRedshiftProps(props):
    pd.set_option('display.max_colwidth', -1)
    keysToShow = ["ClusterIdentifier", "NodeType", "ClusterStatus", "MasterUsername", "DBName", "Endpoint",
                  "NumberOfNodes", 'VpcId']
    x = [(k, v) for k, v in props.items() if k in keysToShow]
    return pd.DataFrame(data=x, columns=["Key", "Value"])


def create_iam_role(config):
    """  Create IAM role with name configured in props file.This role has AmazonS3ReadOnlyAccess"""
    try:
        print("Creating a new IAM Role")
        iam = boto3.client('iam', aws_access_key_id=config.get('AWS', 'KEY'),
                   aws_secret_access_key=config.get('AWS', 'SECRET'),
                   region_name='us-west-2'
                   )

        dwhRole = iam.create_role(   Path='/', RoleName=config.get("IAM_ROLE", "ROLE_NAME"),
                   Description="Allows Redshift clusters to call AWS services on your behalf.",
                   AssumeRolePolicyDocument=json.dumps({
                   'Statement': [{
                    'Action': 'sts:AssumeRole',
                    'Effect': 'Allow',
                    'Principal': {
                    'Service': 'redshift.amazonaws.com'
                    }
                }],
                'Version': '2012-10-17'
                })
               )
        print('Attaching Policy')
        iam.attach_role_policy(RoleName=config.get("IAM_ROLE", "ROLE_NAME"),
                       PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
                       )['ResponseMetadata']['HTTPStatusCode']
        iam = boto3.client('iam', aws_access_key_id=config.get('AWS', 'KEY'), aws_secret_access_key=config.get('AWS', 'SECRET'),
                   region_name='us-west-2')
        roleArn = iam.get_role(RoleName=config.get("IAM_ROLE", "ROLE_NAME"))['Role']['Arn']
        print(roleArn)
        return roleArn
       
    except Exception as e:
        print(e)

        


def create_redshift_cluster(config, roleArn):
    """  Create redshift cluster with cluster properties configured in props file ( dwh.cfg )"""
    try:
        redshift = boto3.client('redshift', region_name="us-west-2", aws_access_key_id=config.get('AWS', 'KEY'),
                                aws_secret_access_key=config.get('AWS', 'SECRET'))
        response = redshift.create_cluster(
                  # HW
                   ClusterType = config.get("DWH", "CLUSTER_TYPE"),
                   NodeType=config.get("DWH", "NODE_TYPE"),
                   NumberOfNodes=int(config.get("DWH", "NUM_NODES")),
                   # Identifiers & Credentials
                   DBName = config.get("CLUSTER", "DB_NAME"),
                   ClusterIdentifier=config.get("DWH", "CLUSTER_IDENTIFIER"),
                   MasterUsername=config.get("CLUSTER", "DB_USER"),
                   MasterUserPassword=config.get("CLUSTER", "DB_PASSWORD"),
                   # Roles(for s3 access)
                   IamRoles =[roleArn]
          )
        myClusterProps = redshift.describe_clusters(ClusterIdentifier=config.get("DWH", "CLUSTER_IDENTIFIER"))['Clusters'][0]
        prettyRedshiftProps(myClusterProps)
      
    except Exception as e:
        print(e)


def main():
    """ Load config from dwh.cfg and create an IAM role and a redshift cluster on AWS using these configurations """
    config = configparser.ConfigParser()
    config.read_file(open('dwh.cfg'))

    KEY = config.get('AWS', 'KEY')
    SECRET = config.get('AWS', 'SECRET')
    CLUSTER_TYPE = config.get("DWH", "CLUSTER_TYPE")
    NUM_NODES = config.get("DWH", "NUM_NODES")
    NODE_TYPE = config.get("DWH", "NODE_TYPE")
    CLUSTER_IDENTIFIER = config.get("DWH", "CLUSTER_IDENTIFIER")
    DB_NAME = config.get("CLUSTER", "DB_NAME")
    DB_USER = config.get("CLUSTER", "DB_USER")
    DB_PASSWORD = config.get("CLUSTER", "DB_PASSWORD")
    DB_PORT = config.get("CLUSTER", "DB_PORT")
    

    df = pd.DataFrame({
      "Param": ["CLUSTER_TYPE", "NUM_NODES", "NODE_TYPE", "CLUSTER_IDENTIFIER", "DB_NAME", "DB_USER", "DB_PASSWORD",
              "DB_PORT"],
      "Value": [CLUSTER_TYPE, NUM_NODES, NODE_TYPE, CLUSTER_IDENTIFIER, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT]
     })
    print("1.Loading data from config files..........");
    print(df)
    print("2.Creating IAM Role..........");
    roleArn = create_iam_role(config)
    print("3.Creating Redshift cluster............")
    create_redshift_cluster(config,roleArn)


if __name__ == "__main__":
    main()

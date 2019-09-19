import boto3  # Python Amazon SDK library. 
import configparser ## Library used to read config files.


def readS3Data(config):
    s3 = boto3.resource('s3',
                       region_name="us-west-2",
                       aws_access_key_id=config.get('AWS', 'KEY'),
                       aws_secret_access_key=config.get('AWS', 'SECRET')
                   )
    sampleDbBucket =  s3.Bucket("awssampledbuswest2")
    for obj in sampleDbBucket.objects.filter(Prefix="ssbgz"):
       print(obj)


    
def main():
    config = configparser.ConfigParser()
    config.read_file(open('dwh.cfg'))

    readS3Data(config)
   

if __name__ == "__main__":
    main()
from airflow.hooks.postgres_hook import PostgresHook
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'
    copy_sql = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        JSON '{}'
        COMPUPDATE OFF
    """
    
    @apply_defaults
    def __init__(self,
                 table = "",
                 s3_path = "",
                 redshift_conn_id = "",
                 aws_conn_id="",
                 region_name="",
                 json_path="",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_conn_id = aws_conn_id
        self.table = table
        self.s3_path = s3_path
        self.region_name=region_name
        self.json_path=json_path
        
        
        
        
    def execute(self, context):
        aws = AwsHook(self.aws_conn_id)
        credentials = aws.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.log.info(f"Credentials access_key {credentials.access_key}")
        self.log.info(f"Credentials secret_key {credentials.secret_key}")
        self.log.info(f"Region_name {self.region_name}")
        self.log.info(f"Redshift {redshift}")
        self.log.info("TABLE {}".format(self.table))
        self.log.info("s3_path {}".format(self.s3_path))
        self.log.info("json_path {}".format(self.json_path))
        self.log.info("Deleting table {}".format(self.table))
        redshift.run("DELETE FROM {}".format(self.table))
        self.log.info("Deleted table : {}".format(self.table))
        
        formatted_copy_sql = StageToRedshiftOperator.copy_sql.format(
                self.table, 
                self.s3_path, 
                credentials.access_key,
                credentials.secret_key, 
                self.json_path
            )
        
        self.log.info("formatted_copy_sql  : {}".format(formatted_copy_sql))
        redshift.run(formatted_copy_sql)
        self.log.info("Copied successfully from app logs into staging table : {}".format(self.table))
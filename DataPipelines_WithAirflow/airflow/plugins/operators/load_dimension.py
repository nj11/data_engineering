from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):
   ''' Reusable operator to load data into dimension tables in data warehouse '''
    ui_color = '#80BD9E'

    insert_sql = """
        TRUNCATE TABLE {};
        INSERT INTO {}
        {};
        COMMIT;
    """
    
    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 load_sql_stmt="",
                 insert_mode="append",
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.load_sql_stmt = load_sql_stmt
        self.insert_mode = insert_mode
        
                
    def execute(self, context):
        '''On run, delete dim table and reload data from insert SQL query and table name passed as an argument '''
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        if self.insert_mode == "truncate_insert":
            self.log.info("Insert mode is truncate_insert Deleting table : {}".format(self.table))
            redshift.run("DELETE FROM {}".format(self.table))
            self.log.info("Deleted table : {}".format(self.table))
        else:
            self.log.info("Insert_mode = append. Appending data to Redshift  table: {} ..."\
                            .format(self.table))
            
        
        self.log.info(f"Loading dimension table {self.table} in Redshift")
        formatted_sql = LoadDimensionOperator.insert_sql.format(
            self.table,
            self.table,
            self.load_sql_stmt
        )
        redshift.run(formatted_sql)
        
        self.log.info(f"Loading dimension table {self.table} in Redshift")
        

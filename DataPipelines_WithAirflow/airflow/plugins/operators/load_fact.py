from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):
    ''' Reusable operator to load data into fact tables in data warehouse '''
    ui_color = '#F98866'
    insert_sql = """
        INSERT INTO {}
        {};
        COMMIT;
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 load_sql_stmt="",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.load_sql_stmt = load_sql_stmt
        
        
    def execute(self, context):
        '''On run, delete fact table and reload data from insert SQL query and table name passed as an argument '''
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        redshift.run("DELETE FROM {}".format(self.table))
        self.log.info("Deleted table : {}".format(self.table))
        self.log.info("Loading fact table : {}".format(self.table))
        formatted_sql = LoadFactOperator.insert_sql.format(
            self.table,
            self.load_sql_stmt
        )
        redshift.run(formatted_sql)

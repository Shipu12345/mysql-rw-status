from config import MysqlConfig
from mysql import connector


class Connections:
    def get_mysql_conn(self, config: MysqlConfig):

        self.conn = connector.connect(host=config.host, user=config.user, passwd=config.passwd, database=config.database, ssl_disabled=True)
        return self.conn

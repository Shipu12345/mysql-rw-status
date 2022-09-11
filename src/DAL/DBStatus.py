from src.connections import Connections


class DBStatus:
    def __init__(self, conn: Connections) -> None:
        self.conn = conn

    def check_mysql_status(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
                select  user() as user, 
                        @@hostname as host, 
                        @@read_only as read_only, 
                        @@super_read_only as super_read_only
        
            """
            )

        data_dict={}
        query_result = cursor.fetchall()

        for i in range(len(query_result)):
            data_dict= {
                            'user': query_result[i][0],
                            'host': query_result[i][1],      
                            'read_only': query_result[i][2],  
                            'super_read_only': query_result[i][3]     
                        }
            
        return data_dict
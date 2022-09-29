import typer




class MysqlConfig:
    def __init__(self, host=None, port=None, user=None, passwd=None, database=None) -> None:
        if not host :
            typer.secho(
                f'Error: No host provided',
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
        
        else:
            self.host = host
            self.port = port
            self.user = user
            self.passwd = passwd
            self.database = database

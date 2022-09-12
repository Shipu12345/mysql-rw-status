"""
Enables CLI for the package
"""

from asyncio import tasks
from typing import Optional
import typer
from pathlib import Path
from typing import Optional
from src import ERRORS, __app_name__, __version__
import datetime

# from todo.todo_ import Status, Priority
from typing import List, Optional
from config import MysqlConfig
from src.connections import Connections
from src.DAL.DBStatus import DBStatus
import time
import os
from pynput import keyboard
from threading import Thread



app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.command()
def fetch_pass(
    passw: str = typer.Option("", "--pass", "-P"),
) -> None:
    return passw


@app.command()
def fetch_host(host: str = typer.Option("127.0.0.1", "--host", "-h")) -> None:
    return host


@app.command()
def fetch_port(
    port: str = typer.Option("3306", "--port", "-p"),
) -> None:
    return port


@app.command()
def fetch_database(
    database: str = typer.Option("mysql", "--database", "-d"),
) -> None:
    return database


def space_lenth(str_key, str_val):
    if len(str_key) < len(str_val):
        str_len = len(str_val) - len(str_key) + 1
        str_len_val = 1
    else:
        str_len_val = len(str_key) - len(str_val) + 1
        str_len = 0

    return str_len // 2, str_len_val // 2


@app.command(name="table")
def show_table(
    user: str = typer.Option("root", "--user", "-u"), passw=fetch_pass(), host=fetch_host(), port=fetch_port(), database=fetch_database()
) -> None:

    typer.secho(f"-----Press 'Esc' to stop the loop...-----", fg=typer.colors.GREEN, bold=True)

    def on_press(key, abortKey='esc'):    
        try:
            k = key.char  # single-char keys
        except:
            k = key.name  # other keys    

        
        typer.secho(f"----- pressed {k}! -----", fg=typer.colors.MAGENTA, bold=True)
        if k == abortKey:
            typer.secho(f"----- Aborted! -----", fg=typer.colors.RED, bold=True)
            return False  # stop listener

    def db_status_loop(user, passw, host, port, database):
        x=-1
        bottom_line =False
        while True:
            x+=1
            try:
                mysql_ob = MysqlConfig(user=user, passwd=passw, host=host, port=port, database=database)
                mysql_conn = Connections().get_mysql_conn(mysql_ob)
                db_status = DBStatus(mysql_conn)
                start_time = time.time()
                data_dict = db_status.check_mysql_status()
                end_time = time.time()
                elasped_time = end_time - start_time
            except:
                typer.secho(
                    f'Error: "{ERRORS[1]}"',
                    fg=typer.colors.RED,
                )
                raise typer.Exit(1)

            start_time = datetime.datetime.fromtimestamp(start_time)
            start_time_str = start_time.strftime("%d-%m-%y %H:%M:%S")
            terminal_width, _ = os.get_terminal_size(0)
            terminal_width -=10

            if mysql_conn.is_connected():
                status = "Okay"
            else:
                status = "Down"

            elasped_time_str = f"{float(elasped_time*1000) :2f}"

            start_time_str_space, start_time_str_space_val = space_lenth("Start Time", start_time_str)
            status_space, status_space_val = space_lenth("Status", status)
            elasped_time_str_space, elasped_time_str_space_val = space_lenth("Response Time", elasped_time_str)

            user_str_space, user_str_space_val = space_lenth("User", data_dict["user"])
            host_str_space, host_str_space_val = space_lenth("Host", data_dict["host"])
            port_str_space, port_str_space_val = space_lenth("Port", port)
            read_only_str_space, read_only_str_space_val = space_lenth("Read Only", str(data_dict["read_only"]))
            super_read_only_str_space, super_read_only_str_space_val = space_lenth("Super Read Only", str(data_dict["super_read_only"]))

            columns = (
                f"{' '*start_time_str_space}Start Time{' '*start_time_str_space}",
                f"|{' '*status_space}Status{' '*status_space}",
                f"|{' '*elasped_time_str_space}Response Time{' '*elasped_time_str_space} ",
                f"|{' '*user_str_space}User{' '*user_str_space}",
                f"|{' '*host_str_space}Host{' '*host_str_space}",
                f"|{' '*port_str_space}Port{' '*port_str_space}",
                f"|{' '*read_only_str_space}read_only{' '*read_only_str_space}",
                f"|{' '*super_read_only_str_space}Super Read Only{' '*super_read_only_str_space}",
            )

            headers = "".join(columns)

            if x%10==0:
                print('\n')
                typer.secho(headers, fg=typer.colors.BRIGHT_CYAN, bold=True)
                typer.secho("-" * terminal_width, fg=typer.colors.BLUE)
                x=1
                bottom_line = True

            typer.secho(f"{' '*start_time_str_space_val}{start_time_str}{' '*start_time_str_space_val} |", fg=typer.colors.BLUE, bold=True, nl=False)
            if status == "Okay":
                typer.secho(f"{' '*status_space_val}{status}{' '*status_space_val}|", fg=typer.colors.BLUE, bold=True, nl=False)
            else:
                typer.secho(f"{' '*status_space_val}{status}{' '*status_space_val}|", fg=typer.colors.RED, bold=True, nl=False)

            typer.secho(
                f"{' '*elasped_time_str_space_val}{float(elasped_time*1000) :2f}{' '*elasped_time_str_space_val}|",
                fg=typer.colors.BLUE,
                bold=True,
                nl=False,
            )
            typer.secho(f"{' '*user_str_space_val}{data_dict['user']}{' '*user_str_space_val} |", fg=typer.colors.BLUE, bold=True, nl=False)
            typer.secho(f"{' '*host_str_space_val}{data_dict['host']}{' '*host_str_space_val}|", fg=typer.colors.BLUE, bold=True, nl=False)
            typer.secho(f"{' '*port_str_space_val}{port}{' '*port_str_space_val}|", fg=typer.colors.BLUE, bold=True, nl=False)
            typer.secho(
                f"{' '*read_only_str_space_val}{str(data_dict['read_only'])}{' '*read_only_str_space_val}|", fg=typer.colors.BLUE, bold=True, nl=False
            )
            typer.secho(
                f"{' '*super_read_only_str_space_val}{str(data_dict['super_read_only'])}{' '*super_read_only_str_space_val}",
                fg=typer.colors.BLUE,
                bold=True,
                nl=False,
            )

            print()
            if x != 1 and bottom_line:
                typer.secho("-" * terminal_width + "\n", fg=typer.colors.BRIGHT_BLUE)
    
            bottom_line = False
            time.sleep(1)


    while True:
        listener = keyboard.Listener(on_press=on_press)
        listener.start()  # start to listen on a separate thread

        # start thread with loop
        Thread(target=db_status_loop, args=(user, passw, host, port, database), name='db_status_loop', daemon=True).start()

        listener.join() # wait for abortKey
        break;

 
        


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return

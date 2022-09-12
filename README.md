# mysql-rw-status
To check mysql read/write status and server status.


Installation: (Linux machines only)

    1. Install  Pipenv.

        !pip install pipenv

    2. Initialize pipenv.

        !pipenv install 
    
    3. Open pivenv venv. 

        !pipenv shell
    

To Run:

    1. !python3 main.py table -u [user] -P [password] -h [host] -p [port] -d [database]

    2. Use --help for any queries.


As per Pasha Bhai's Requirements, I need to do following tasks.

    1. Show Server Status (OK/NOT Found, Server Address)
    2. For Reading and Writing.
    3. Response time and Request Time.

In Addition I will try,
    
    1. to publish it as module.
    2. make it accessable deeper to table wise.
    3. read write ratio to it.
    
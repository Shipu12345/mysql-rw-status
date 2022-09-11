"""
    Runnable file for the package
"""



__app_name__ = "mysql-response-status"
__version__ = "0.0.1"

(
    SUCCESS,
    ACCESS_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
) = range(4)

ERRORS = {
    ACCESS_ERROR: "Connection Can not Be Setted, please check provided credentials.",
    DB_READ_ERROR: "Database read error",
    DB_WRITE_ERROR: "Database write error",
}
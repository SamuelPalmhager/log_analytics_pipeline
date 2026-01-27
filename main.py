from log_analytics import log_creator
from etl import etl

def main():
    log_creator("test")
    etl("test")

main()
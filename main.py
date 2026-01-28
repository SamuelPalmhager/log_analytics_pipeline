
import sys
from log_analytics import log_creator
from etl import etl
from analytics import analytics


def main():
    # Collect arguments from command line, skip the script name
    arg = sys.argv[1]
    log_creator(arg)
    etl(arg)
    analytics(arg)    

if __name__ == "__main__":
    main()
    
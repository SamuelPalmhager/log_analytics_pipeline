
import sys
from producer.log_analytics import log_creator
from pipeline.etl import etl
from analytics.analysis import perform_analysis


def main():
    # Collect arguments from command line, skip the script name
    arg = sys.argv[1]
    log_creator(arg)
    etl(arg)
    perform_analysis(arg)    

if __name__ == "__main__":
    main()
    
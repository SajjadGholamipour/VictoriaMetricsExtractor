#!/usr/bin/env python3

import argparse
import requests
import datetime

def is_rfc3339_time(time_str):
    """
    To check input start and end time is compatible with RFC3339
    """
    try:
        datetime.datetime.fromisoformat(time_str)
        return True
    except ValueError:
        return False

def rfc3339_to_timestamp(rfc3339_time_str):
    """
    To convert RFC3339 based start and end time to timestamp
    """
    dt = datetime.datetime.fromisoformat(rfc3339_time_str)
    return int(dt.timestamp())

def export_metrics_json(url, selectors, start, end, output_file):
    """
    Export metrics from VictoriaMetrics API endpoint to a json file.
    """
    # Convert RFC3339 based start and end time to timestamp
    if is_rfc3339_time(str(start)):
       start = rfc3339_to_timestamp(str(start))
    if is_rfc3339_time(str(end)):
       end = rfc3339_to_timestamp(str(end))

    # Set the query parameters for the metrics you want to export to json
    params = {
        'match[]': selectors,
        'start': start,
        'end': end
    }
    # Send a GET request to the VictoriaMetrics API endpoint
    response = requests.get(url, params=params)

    # Write the response to a JSON file
    with open(output_file, 'w') as f:
        f.write(response.text)

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Export metrics from VictoriaMetrics API endpoint to a json file')
    parser.add_argument('url', type=str, help='VictoriaMetrics API endpoint URL')
    parser.add_argument('selectors', type=str, nargs='+', help='Metric selectors to export')
    parser.add_argument('--start', type=str, default='1h0m', help='Start time for export i.e. 2023-05-11T01:20:30')
    parser.add_argument('--end', type=str, default='0h1m', help='End time for export i.e. 2023-05-11T02:30:10')
    parser.add_argument('--output', type=str, default='store.json', help='Output file for exported metrics')
    args = parser.parse_args()

    # Call the export_metrics_csv function with the command-line arguments
    export_metrics_json(args.url, args.selectors, args.start, args.end, args.output)

#!/usr/bin/env python3

import argparse
import requests
import json
import time
import random
import subprocess

def run_docker_container(image_name, container_name, port_mapping,volume_name):
    """
    Create a container with specified parameters
    """
    cmd = f'docker run -it -d --name {container_name} --rm -v {volume_name} -v /etc/localtime:/etc/localtime:ro -p {port_mapping} {image_name}'
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return process.returncode, stdout, stderr

def import_metrics(file_path):
    """
    Import metrics from a JSON file to VictoriaMetrics import API endpoint.
    """
    # Create a temporary VictoriaMetrics container
    timestamp=int(time.time())
    rand_port = random.randint(8000, 8100)
    image_name = 'victoriametrics/victoria-metrics:v1.90.0'
    container_name = str('test-VM-'+str(timestamp))
    port_mapping = str(rand_port)+':8428'
    volume_name = str('victoria-metrics-data'+str(timestamp)+':/victoria-metrics-data')
    returncode, stdout, stderr = run_docker_container(image_name, container_name, port_mapping, volume_name)
    print(f'Return code: {returncode}')
    print(f'Stdout: {stdout.decode()}')
    print("Victoria Metics container created successfully!")
    print("Importing...")

    # Open the JSON file and parse the metrics
    if returncode == 0:
        url = str('http://localhost:'+str(rand_port))
        endpoint = str(url+'/api/v1/import')
        time.sleep(10)
        with open(file_path) as f:
             # Send a POST request to the VictoriaMetrics import API endpoint for metrics
             response = requests.post(endpoint, data=f.read())
             print(f'Response Status Code: {response.status_code}')
             if response.text=="" :
                 print("Import successful. Temporary Victoria Metrics URL is:" + str(url)+'.')

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Import metrics from a JSON file to VictoriaMetrics import API endpoint')
    parser.add_argument('file', type=str, help='Path to JSON file containing metrics')
    args = parser.parse_args()

    # Call the import_metrics function with the command-line arguments
    import_metrics(args.file)

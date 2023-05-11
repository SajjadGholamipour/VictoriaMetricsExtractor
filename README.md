#  Victoria Metrics Extractor
In this repository we created a metrics extractor tool to store some Victoria metrics for further investigation or comparison to other times. For example in high loads or disaster times.

## Execution
To execute this script, after downloading, do following steps:

`~$ chmod +x store.py`

`~$ mv store.py /usr/local/bin/store`

`~$ chmod +x restore.py`

`~$ mv restore.py /usr/local/bin/restore`

After doing these steps, commands are runnable from anywhere. 
## Usage
### Store command
To store some metrics from a Victoria Metrics API endpoint, store command will be used as follows:

`store <http://Victoria-Metrics-API-Endpoint> <metrics dictionaty> --start <start date time> --end <end date time> --output <output path>`

**start** and **end** date times have two input types:
* timestamp i.e 1683797286
* RFC3339 i.e. 2023-05-11T01:45:2

**Example**

`~$ store http://localhost:8428/api/v1/export {'{__name__="process_cpu_seconds_total",job="victoriametrics",instance="victoriametrics:8428"}','{__name__="process_resident_memory_bytes",job="victoriametrics",instance="victoriametrics:8428"}'} --start '2023-05-11T01:45:29' --end '2023-05-11T07:45:29' --output 'output.json'`

### Restore command
To restore saved metrics from a file, restore command will be used as follows:

`~$ restore <file path>`

This command restore metrics to a temporary Victoria Metrics service that is deployed with docker container. In other words, each time this command is executed, a new Victoria Metrics container is created and the data is imported into it.

**Example**

`~$ restore stored-data.json`

****Sample Output****

Return code: 0
Stdout: 7ad524a38770bc82a7937649ebc1821243071ff931bf62e84b0ccdbdfc3e5218
Victoria Metics container created successfully!
Importing...
Response Status Code: 204
Import successful. Temporary Victoria Metrics URL is:http://localhost:8052.


## Test Environment
* OS: Ubuntu v22.04
* Python: v3.10.6
* Victoria Metrics: v1.90.0

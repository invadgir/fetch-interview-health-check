# Fetch Interview Health Checker

This repository contains a solution for the "Fetch Take-Home Exercise — Site Reliability Engineering" assignment. The project is written in Python and is designed to monitor a set of HTTP endpoints by periodically checking their health and logging their cumulative availability percentage.

## Project Overview

The solution performs the following functions:
- **Configuration Parsing:** Reads a YAML file containing a list of endpoints.
- **Health Checks:** Sends HTTP requests to each endpoint every 15 seconds, measuring response status and latency.
- **Aggregation:** Aggregates the results by domain and calculates the overall availability percentage.
- **Logging:** Outputs detailed logs of each health check cycle.

## Requirements

- **Python 3.6+**  
  Ensure that you have Python 3.6 or higher installed.

- **Dependencies:**  
  The project uses the following open source libraries:
  - [PyYAML](https://pyyaml.org/) for parsing YAML files.
  - [Requests](https://docs.python-requests.org/) for making HTTP requests.

## Setup and Installation

### 1. Clone the Repository

Clone the repository to your local machine using Git:

```bash
git clone https://github.com/invadgir/fetch-interview.git
cd fetch-interview

### 2. Create a Virtual Environment (Recommended)

Create and activate a virtual environment to isolate dependencies:

On macOS/Linux:
python3 -m venv venv
source venv/bin/activate


On Windows:
python3 -m venv venv
venv\Scripts\activate

### 3. install dependencies

Install the required packages using pip:

```bash
pip install -r requirements.txt


If a requirements.txt is not provided, install dependencies manually:

```bash
pip install pyyaml requests


## Running the Application

The main script is named health-check.py and it requires a YAML configuration file as an argument.

### 1. Prepare the YAML Configuration File
Create a file named endpoints.yaml with your endpoint configurations. An example format: Please see template_endpoint.yaml

### 2.  Run the Script


Run the script by passing the path to your YAML file:
python health-check.py endpoints.yaml
You should see log output detailing the parsed endpoints, individual endpoint health checks (with status codes and latencies), and aggregated availability percentages for each domain. The script runs indefinitely until you press CTRL+C to exit.


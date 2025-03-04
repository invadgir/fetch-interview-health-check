import argparse
import yaml
import requests
import time
from urllib.parse import urlparse
import sys

print("Starting health-check.py script...")

def parse_config(file_path):
    """Read and parse the YAML config file; return a list of endpoint configurations."""
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            print(f"[INFO] Successfully parsed config file: {file_path}")
            return config
    except FileNotFoundError:
        print(f"[ERROR] Config file not found: {file_path}")
        sys.exit(1)
    except yaml.YAMLError as exc:
        print(f"[ERROR] YAML parse error: {exc}")
        sys.exit(1)
    except Exception as exc:
        print(f"[ERROR] Unexpected error: {exc}")
        sys.exit(1)

def check_endpoint(endpoint_config):
    """
    Send an HTTP request to the endpoint and measure latency.
    Returns a tuple: (domain, is_up, latency)
    """
    method = endpoint_config.get('method', 'GET')
    url = endpoint_config.get('url')
    if not url:
        print(f"[WARNING] Missing 'url' in config: {endpoint_config}")
        return None, False, None

    headers = endpoint_config.get('headers', {})
    body = endpoint_config.get('body', None)

    start_time = time.time()
    try:
        response = requests.request(method, url, headers=headers, data=body, timeout=2)
        latency = (time.time() - start_time) * 1000  # in milliseconds
        is_up = (200 <= response.status_code < 300) and (latency < 500)
        #testing endpoints
        #print(f"[DEBUG] {endpoint_config.get('name', 'Unnamed')} - Response: {response.status_code}, Latency: {latency:.2f} ms")
    except Exception as e:
        print(f"[ERROR] Error checking {endpoint_config.get('name', 'Unnamed')}: {e}")
        latency = None
        is_up = False

    domain = urlparse(url).netloc
    return domain, is_up, latency

def main():
    # Parse the config file path from command-line arguments
    parser = argparse.ArgumentParser(description="HTTP Endpoints Health Checker")
    parser.add_argument('config_file', help="Path to the YAML configuration file")
    args = parser.parse_args()

    # Load endpoints from the YAML file
    endpoints = parse_config(args.config_file)
    if not isinstance(endpoints, list):
        print("[ERROR] Config file must contain a list of endpoints.")
        sys.exit(1)
    
    print("[INFO] Loaded endpoints:")
    for ep in endpoints:
        print(f"  [INFO] {ep.get('name', 'Unnamed')} - {ep.get('url')}")
    
    # Dictionary to hold cumulative stats per domain
    domain_stats = {}
    try:
        while True:
            print(f"\n[INFO] Starting health check cycle at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            for endpoint in endpoints:
                domain, is_up, latency = check_endpoint(endpoint)
                if domain is None:
                    continue
                if domain not in domain_stats:
                    domain_stats[domain] = {'total': 0, 'up': 0}
                domain_stats[domain]['total'] += 1
                if is_up:
                    domain_stats[domain]['up'] += 1

            # Log aggregated availability for each domain
            print("Cycle results:")
            output = []
            for domain, stats in domain_stats.items():
                availability = round(100 * stats['up'] / stats['total'])
                output.append(f"{domain} has {availability}% availability percentage")
            print("  ".join(output))
            print("[INFO] Cycle complete. Waiting 15 seconds for next cycle...\n")
            time.sleep(15)
    except KeyboardInterrupt:
        print("\n[INFO] Exiting gracefully due to keyboard interrupt.")
    except Exception as exc:
        print(f"[ERROR] Unexpected error in main loop: {exc}")
           
if __name__ == "__main__":
    main()

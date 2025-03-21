import os
import requests
import time

def ping_url(url, delay, max_trials):
    trials = 0
    while trials < max_trials:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Website {url} is reachable.")
                return True
        except requests.ConnectionError:
            print(f"Website {url} is unreachable. Retrying in {delay} seconds....")
            time.sleep(delay)
            trials += 1
        except requests.exceptions.MissingSchema:
            print(f"Invalid URL format: {url}. Make sure the URL has a valid schema (e.g., http:// or https://)")
            return False
    return False

def run():
    try:
        website_url = os.getenv("INPUT_URL")
        
        # Fetch and validate delay value, with an additional check for empty string
        delay_str = os.getenv("INPUT_DELAY", '5')  # Default delay is '5' if not provided
        if delay_str == '':
            delay_str = '5'  # Fallback to default value if it's an empty string
        
        try:
            delay = int(delay_str)
        except ValueError:
            raise ValueError(f"Invalid delay value: {delay_str}. It should be a valid integer.")
        
        # Fetch and validate max trials value, with an additional check for empty string
        max_trials_str = os.getenv("INPUT_MAX_TRIALS", '3')  # Default max trials is '3' if not provided
        if max_trials_str == '' or '$' in max_trials_str:  # Detect template placeholders like $ {{ ... }}
            raise ValueError(f"Invalid max_trials value: {max_trials_str}. It seems to contain a placeholder.")
        
        try:
            max_trials = int(max_trials_str)
        except ValueError:
            raise ValueError(f"Invalid max_trials value: {max_trials_str}. It should be a valid integer.")
        
        if not website_url:
            raise ValueError("Website URL (INPUT_URL) is not provided in the environment variables.")

        print(f"Starting the check for {website_url}...")
        website_reachable = ping_url(website_url, delay, max_trials)

        if not website_reachable:
            raise Exception(f"Website {website_url} is malformed or unreachable after {max_trials} trials.")

        print(f"Website {website_url} is reachable.")

    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    run()

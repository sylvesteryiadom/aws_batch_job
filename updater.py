#!/usr/bin/env python3
"""
Script Name: update_payload_sender.py

Description:
    This script reads JSON payloads from a file and sends UPDATE (HTTP PUT) requests to a specified HTTPS endpoint using Bearer Token Authentication.

Usage:
    python update_payload_sender.py --file path/to/payloads.txt --endpoint https://api.example.com/update --token YOUR_BEARER_TOKEN

Author:
    Your Name
"""

import argparse
import json
import logging
import sys
from typing import List, Dict, Any

import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description='Send UPDATE (HTTP PUT) requests to an HTTPS endpoint using JSON payloads from a file.'
    )
    parser.add_argument(
        '--file',
        type=str,
        required=True,
        help='Path to the file containing JSON payloads.'
    )
    parser.add_argument(
        '--endpoint',
        type=str,
        required=True,
        help='The HTTPS endpoint URL to send UPDATE requests to.'
    )
    parser.add_argument(
        '--token',
        type=str,
        required=True,
        help='Bearer token for authentication.'
    )
    parser.add_argument(
        '--headers',
        type=str,
        default='{}',
        help='Additional headers in JSON format. Example: \'{"Custom-Header": "Value"}\''
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=10,
        help='Timeout in seconds for the HTTP requests.'
    )

    return parser.parse_args()

def read_payloads(file_path: str) -> List[Dict[str, Any]]:
    """
    Read JSON payloads from a file.

    Each line in the file should be a valid JSON object or a JSON array containing a single object.

    Args:
        file_path (str): Path to the payloads file.

    Returns:
        List[Dict[str, Any]]: List of JSON payloads.
    """
    payloads = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    logging.warning(f"Skipping empty line at line number {line_number}.")
                    continue
                try:
                    # Attempt to parse the line as JSON
                    parsed = json.loads(line)
                    # If the parsed object is a list, extract the first element
                    if isinstance(parsed, list):
                        if parsed:
                            payload = parsed[0]
                            payloads.append(payload)
                        else:
                            logging.warning(f"Empty list at line {line_number}; skipping.")
                    elif isinstance(parsed, dict):
                        payloads.append(parsed)
                    else:
                        logging.error(f"Unsupported JSON structure at line {line_number}; skipping.")
                except json.JSONDecodeError as e:
                    logging.error(f"Invalid JSON at line {line_number}: {e}; skipping.")
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        sys.exit(1)

    logging.info(f"Successfully read {len(payloads)} payload(s) from the file.")
    return payloads

def prepare_headers(token: str, additional_headers: str) -> Dict[str, str]:
    """
    Prepare HTTP headers for the request.

    Args:
        token (str): Bearer token for authentication.
        additional_headers (str): Additional headers in JSON format.

    Returns:
        Dict[str, str]: Dictionary of HTTP headers.
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    if additional_headers:
        try:
            extra_headers = json.loads(additional_headers)
            if isinstance(extra_headers, dict):
                headers.update(extra_headers)
            else:
                logging.error("Additional headers must be a JSON object.")
                sys.exit(1)
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON for additional headers: {e}")
            sys.exit(1)

    return headers

def send_update_request(session: requests.Session, endpoint: str, payload: Dict[str, Any],
                       headers: Dict[str, str], timeout: int) -> bool:
    """
    Send an UPDATE (HTTP PUT) request to the endpoint with the given payload.

    Args:
        session (requests.Session): The requests session.
        endpoint (str): The endpoint URL.
        payload (Dict[str, Any]): The JSON payload.
        headers (Dict[str, str]): HTTP headers.
        timeout (int): Request timeout in seconds.

    Returns:
        bool: True if the request was successful, False otherwise.
    """
    try:
        response = session.put(url=endpoint, json=payload, headers=headers, timeout=timeout, verify=True)
        response.raise_for_status()
        logging.info(f"Successfully updated with payload: {json.dumps(payload)}")
        return True
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error for payload {json.dumps(payload)}: {http_err} - Response: {response.text}")
    except requests.exceptions.Timeout:
        logging.error(f"Request timed out for payload: {json.dumps(payload)}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request exception for payload {json.dumps(payload)}: {req_err}")
    return False

def main() -> None:
    """
    Main function to execute the script logic.
    """
    args = parse_arguments()

    # Prepare headers
    headers = prepare_headers(token=args.token, additional_headers=args.headers)

    # Read payloads from file
    payloads = read_payloads(file_path=args.file)

    if not payloads:
        logging.error("No valid payloads to send. Exiting.")
        sys.exit(1)

    # Initialize a requests session for connection pooling
    session = requests.Session()

    success_count = 0
    failure_count = 0

    for index, payload in enumerate(payloads, start=1):
        logging.info(f"Sending payload {index}/{len(payloads)}")
        success = send_update_request(
            session=session,
            endpoint=args.endpoint,
            payload=payload,
            headers=headers,
            timeout=args.timeout
        )
        if success:
            success_count += 1
        else:
            failure_count += 1

    logging.info(f"Update requests completed: {success_count} succeeded, {failure_count} failed.")

    # Close the session
    session.close()

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import os
import json
import argparse
import logging
import requests

logger = logging.getLogger("target-mailgun")
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

def load_json(path):
    with open(path) as f:
        return json.load(f)


def parse_args():
    '''Parse standard command-line args.
    Parses the command-line arguments mentioned in the SPEC and the
    BEST_PRACTICES documents:
    -c,--config     Config file
    -s,--state      State file
    -d,--discover   Run in discover mode
    -p,--properties Properties file: DEPRECATED, please use --catalog instead
    --catalog       Catalog file
    Returns the parsed args object from argparse. For each argument that
    point to JSON files (config, state, properties), we will automatically
    load and parse the JSON file.
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-c', '--config',
        help='Config file',
        required=True)

    args = parser.parse_args()
    if args.config:
        setattr(args, 'config_path', args.config)
        args.config = load_json(args.config)

    return args


def post_data(config):
    api_key = config['api_key']
    domain = config['domain']
    email = config['email']
    input_path = config['input_path']

    # Get the files to upload
    files = []

    for path in os.listdir(input_path):
        full_path = os.path.join(input_path, path)
        if os.path.isfile(full_path):
            logger.debug(f"Attaching {full_path}")
            files.append(("attachment", open(full_path)))

    # Send to Mailshake
    response = requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", api_key),
        files=files,
        data={"from": "hotglue <hello@hotglue.xyz>",
              "to": email,
              "subject": "Job data",
              "text": "Check out your local data!"
        })
    
    logger.debug(response.text)


def upload(config):
    logger.info("Uploading data")

    # Post CSV data to Mailgun
    post_data(config)

    logger.info("Upload complete")


def main():
    # Parse command line arguments
    args = parse_args()

    # Upload the 
    upload(args.config)


if __name__ == "__main__":
    main()

# IP Address Management Script

## Description

The ip_address_management project provides a set of Python tools for the efficient management of IP addresses stored in text files. This module facilitates the addition, removal, and validation of IPv4 and IPv6 addresses, ensuring that only valid addresses are handled and avoiding duplicates. It's ideal for managing allowlists or blocklists in applications that require IP-based access control.

## Prerequisites

- Python 3.x

## Features

- IP Address Validation: Ensures that only valid IP addresses are added or removed, using Python's ipaddress module.
- Support for IPv4 and IPv6: Compatible with both types of IP addresses, allowing for flexible management.
- File Handling: Reads and writes to text files to update the IP address list, with error handling for not found or inaccessible files.
- Duplicate Prevention: Prevents the addition of IP addresses already present in the file, keeping the list clean and efficient.
- Unit Tests: Includes a set of unit tests to validate the functionality and robustness of the module.

## Usage

The ip_address_management.py module includes the following main functions:

- add_ip_to_file(file_path, new_ips): Adds a list of new IP addresses to a file after validating them.
- update_file(import_file, remove_list): Removes a list of IP addresses from the specified file.
- read_ip_addresses(file_path): Reads and validates IP addresses from a file, returning a list of valid IP addresses.
Tests

The test_ip_address_management.py file contains unit tests that cover all the main functionalities of the ip_address_management.py module. These tests ensure that the module behaves as expected under various scenarios, including handling invalid IP addresses, not found files, and file permissions.

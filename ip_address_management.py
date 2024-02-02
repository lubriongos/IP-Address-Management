import ipaddress
# Reads IP addresses from a file and returns a list
def read_ip_addresses(file_path):
    try:
        with open(file_path, "r") as file:
            # Path to the file containing IP addresses
            content = file.read()

        # Split the content by spaces and filter out non-valid IPs
        ip_addresses = [part for part in content.split() if is_valid_ip(part)]
    except FileNotFoundError as e:
        print(f"FileNotFoundError: File '{file_path}' not found.")
        raise e  # Re-throw the exception to be caught by the test

    return ip_addresses

def is_valid_ip(ip_str):
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        print(f"Error: '{ip_str}' is not a valid IP address.")
        return False

# Updates a file by removing specified IP addresses
def update_file(import_file, remove_list):
    # param import_file: Path to the file to be updated
    # param remove_list: List of IP addresses to be removed

    ip_addresses = read_ip_addresses(import_file)
    if ip_addresses is None:
        return

    # Make the comparison case-insensitive
    for ip_to_remove in remove_list:
        if ip_to_remove.lower() in map(str.lower, ip_addresses):
            ip_addresses = [ip for ip in ip_addresses if ip.lower() != ip_to_remove.lower()]
        else:
            print(f"Warning: IP address '{ip_to_remove}' not found in the list. It won't be removed.")

    # Convert ip_addresses back to a string
    updated_content = " ".join(ip_addresses)

    try:
        # Write the updated content back to the file
        with open(import_file, "w") as file:
            file.write(updated_content)
    except PermissionError as e:
        raise e # Re-throw the exception to be caught by the test

# Adds a new IP address to the file
def add_ip_to_file(file_path, new_ips):
    # param file_path: Path to the file to which the IP addresses should be added.
    # param new_ips: List of new IP addresses to be added.

    # Read existing IPs from file
    ip_addresses = read_ip_addresses(file_path)
    if ip_addresses is None:
        return
    
    # Verify and add each new IP to the list
    for new_ip in new_ips:
        try:
            ip_obj = ipaddress.ip_address(new_ip)
            if ip_obj.version == 4:
                ip_type = "IPv4"
            elif ip_obj.version == 6:
                ip_type = "IPv6"
            else:
                print(f"Error: '{new_ip}' is not a valid IP address.")
                continue
        except ValueError as e:
            print(f"Caught ValueError: {e}")
            raise e  # Re-throw the exception to be caught by the test
        
        # Check if the IP is already in the list
        if new_ip in ip_addresses:
            print(f"Error: The '{ip_type}' address '{new_ip}' already exists in the list.")
            raise ValueError(f"The '{ip_type}' address '{new_ip}' already exists in the list.")

        # Add the new IP to the list
        ip_addresses.append(new_ip)

    try:
        # Write the updated content back to the file
        with open(file_path, "w") as file:
            file.write(" ".join(ip_addresses))
    except Exception as e:
        print(f"Error writing to file: {e}")
        raise e # Re-throw the exception to be caught by the test

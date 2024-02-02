import unittest
import os
from ip_address_management import update_file, add_ip_to_file, read_ip_addresses

class IPAddressManagementTest(unittest.TestCase):

    def setUp(self):
        # Create a temporary file for testing
        self.test_file_path = "test_allow_list.txt"
        with open(self.test_file_path, "w") as file:
            file.write("192.168.0.1 192.168.0.2 192.168.0.3")
        # Create a empty temporary file for testing
        self.empty_file_path = "empty_allow_list.txt"
        open(self.empty_file_path, "w").close()

    def tearDown(self):
        try:
            # Delete the temporary files after testing
            if os.path.exists(self.test_file_path):
                # Restore file permissions before attempting to delete the file
                os.chmod(self.test_file_path, 0o666)
                os.remove(self.test_file_path)

            if os.path.exists(self.empty_file_path):
                os.remove(self.empty_file_path)
        except Exception as e:
            print(f"Error during tearDown: {e}")

    def test_given_ips_when_update_file_then_they_are_removed(self):
        update_file(self.test_file_path, ["192.168.0.1", "192.168.0.2"])
        updated_content = read_ip_addresses(self.test_file_path)
        self.assertNotIn("192.168.0.1", updated_content)
        self.assertNotIn("192.168.0.2", updated_content)

    def test_given_nonexistent_ip_when_update_file_then_no_change(self):
        # Verify that the initial content of the file is correct.
        initial_content = read_ip_addresses(self.test_file_path)
        self.assertEqual(initial_content, ["192.168.0.1", "192.168.0.2", "192.168.0.3"])
        update_file(self.test_file_path, ["192.168.0.4"])
        unchanged_content = read_ip_addresses(self.test_file_path)
        self.assertEqual(unchanged_content, ["192.168.0.1", "192.168.0.2", "192.168.0.3"])

    def test_given_ip_when_add_ip_to_file_then_it_is_added(self):
        add_ip_to_file(self.test_file_path, ["192.168.0.4"])
        updated_content = read_ip_addresses(self.test_file_path)
        self.assertIn("192.168.0.4", updated_content)

    def test_given_empty_file_when_update_file_then_no_change(self):
        # Verify that the file is initially empty
        initial_content = read_ip_addresses(self.empty_file_path)
        self.assertEqual(initial_content, [])
        # Attempt to update file (delete IPs)
        update_file(self.empty_file_path, ["192.168.0.1", "192.168.0.2"])
        # Verify that the content is still empty after updating
        updated_content = read_ip_addresses(self.empty_file_path)
        self.assertEqual(updated_content, [])
        # Add new IP to the empty file
        add_ip_to_file(self.empty_file_path, ["192.168.0.3"])
        # Verify that the file now contains the new IP
        final_content = read_ip_addresses(self.empty_file_path)
        self.assertEqual(final_content, ["192.168.0.3"])

    def test_given_empty_file_when_add_ip_to_file_then_ip_added(self):
        add_ip_to_file(self.empty_file_path, ["192.168.0.4"])
        ip_addresses = read_ip_addresses(self.empty_file_path)
        self.assertIn("192.168.0.4", ip_addresses)

    def test_given_file_with_ips_when_add_multiple_ips_to_file_then_ips_added(self):
        ips_to_add = ["192.168.0.4", "192.168.0.5", "1050:0:0:0:5:600:300c:326b"]
        add_ip_to_file(self.test_file_path, ips_to_add)
        ip_addresses = read_ip_addresses(self.test_file_path)
        for ip in ips_to_add:
            self.assertIn(ip, ip_addresses)

    def test_given_a_file_when_read_file_then_it_shows_ips(self):
        ip_addresses = read_ip_addresses(self.test_file_path)
        self.assertEqual(ip_addresses, ["192.168.0.1", "192.168.0.2", "192.168.0.3"])

    def test_given_nonexistent_file_when_update_file_then_raise_error(self):
        with self.assertRaises(FileNotFoundError):
            update_file("nonexistent_file.txt", ["192.168.0.1"])

    def test_given_invalid_ip_when_add_to_file_then_raise_error(self):
        with self.assertRaises(ValueError):
            add_ip_to_file(self.test_file_path, ["invalid_ip_address"])

    def test_given_existing_ip_when_add_ip_to_file_then_raise_error(self):
        existing_ip = "192.168.0.1"
        with open(self.test_file_path, "w") as file:
            file.write(existing_ip)
        # Convert the existing_ip to a list, as add_ip_to_file expects a list
        existing_ip_list = [existing_ip]
        with self.assertRaises(ValueError) as context:
            add_ip_to_file(self.test_file_path, existing_ip_list)
        ip_type = "IPv4" if ":" not in existing_ip else "IPv6"
        self.assertEqual(
            str(context.exception),
            f"The '{ip_type}' address '{existing_ip}' already exists in the list."
        )

    def test_given_nonexistent_file_when_read_file_then_raise_error(self):
        with self.assertRaises(FileNotFoundError):
            read_ip_addresses("nonexistent_file.txt")

    def test_given_read_only_file_when_update_file_then_raise_error(self):
        # Change file permissions to read-only
        os.chmod(self.test_file_path, 0o444)  
        # Verify that the initial content of the file is correct.
        initial_content = read_ip_addresses(self.test_file_path)
        self.assertEqual(initial_content, ["192.168.0.1", "192.168.0.2", "192.168.0.3"])
        with self.assertRaises(PermissionError):
            update_file(self.test_file_path, ["192.168.0.1"])
        # Verify that the content of the file has not changed
        unchanged_content = read_ip_addresses(self.test_file_path)
        self.assertEqual(unchanged_content, ["192.168.0.1", "192.168.0.2", "192.168.0.3"])

    def test_given_read_only_file_when_add_ip_to_file_then_raise_error(self):
        # Change file permissions to read-only
        os.chmod(self.test_file_path, 0o444)
        with self.assertRaises(IOError):
            add_ip_to_file(self.test_file_path, ["192.168.0.4"])

if __name__ == '__main__':
    unittest.main()

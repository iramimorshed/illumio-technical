import unittest 
import os
import csv 
from mapping import parse_protocol_map, parse_lookup, parse_log_data, write_results


class TestMapping(unittest.TestCase):

    # Small tests cases
    def create_input_file_1(self):
        with open("tests/lookup-1.csv", mode = "w") as file:
            writer = csv.writer(file)

            writer.writerow(["dstport", "protocol", "tag"])
            writer.writerow(["80", "tcp", "sv_P1"])
            writer.writerow(["443", "tcp", "sv_P2"])
        
        with open("tests/flow-log-1.csv", mode = "w") as file:
            writer = csv.writer(file)
            writer.writerow(["2 123456789012 eni-1a2b3c4d 192.168.0.1 203.0.113.12 1024 80 11 10 5000 1620140661 1620140721 ACCEPT OK"])
            writer.writerow(["2 123456789012 eni-1a2b3c4d 192.168.0.1 203.0.113.12 1024 443 11 10 5000 1620140661 1620140721 ACCEPT OK"])
    
    def test_mapping_1(self): 
        self.create_input_file_1()

        tag_matches, port_protocol_matches = parse_log_data("tests/flow-log-1.csv", parse_protocol_map("src/protocol-numbers.csv"), parse_lookup("tests/lookup-1.csv"))

        write_results("tests/results-1.csv", tag_matches, port_protocol_matches) 
        expected_tag_matches = {'Untagged': 2} 
        expected_port_protocol_matches = {('80', 'nvp-ii'): 1, ('443', 'nvp-ii'): 1}
        self.assertEqual(tag_matches, expected_tag_matches)
        self.assertEqual(port_protocol_matches, expected_port_protocol_matches)

        # os.remove("tests/flow-log-1.csv")
        # os.remove("tests/lookup-1.csv")
        # os.remove("tests/results-1.csv")
    

    def test_mapping_2(self): 
        tag_matches, port_protocol_matches = parse_log_data("tests/flow-log.csv", parse_protocol_map("src/protocol-numbers.csv"), parse_lookup("tests/lookup.csv"))
        write_results("tests/results.csv", tag_matches, port_protocol_matches)

if __name__ == "__main__":
    unittest.main()
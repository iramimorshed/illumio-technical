import csv 

# decimal -> protocol name
def parse_protocol_map(filename): 
    protocol_map = {} 
    with open(filename, mode = "r") as file:
        reader = csv.DictReader(file) 

        # Map the decimal number to the protocol name
        for row in reader: 
            protocol_map[row["Decimal"]] = row["Keyword"].lower()
    
    return protocol_map

# (dstport, protocol) -> tag based on lookup file
def parse_lookup(filename): 
    lookup = {}
    with open(filename, mode = "r") as file: 
        reader = csv.DictReader(file) 

        # Map (dstport, protocol) -> tag
        for row in reader: 
            # Remove any trailing whitespaces and lowercase the tag for case insensitivity
            dstport, protocol, tag = row["dstport"].strip(), row["protocol"].strip(), row["tag"].strip().lower()
            lookup[(dstport, protocol)] = tag 
    
    return lookup

# Parse the log data
def parse_log_data(filename, protocol_map, lookup):
    # tag -> count of matches for each tag
    tag_matches = {} 

    # (port, protocol) -> count of matches for each (port, protocol) combination
    port_protocol_matches = {}

    with open(filename, mode = "r") as file: 
        log_data = csv.reader(file) 
        for row in log_data: 
            if not row: 
                continue

            # Extract the dstport and protocol fields from the log data
            fields = row[0].split(" ")
            dstport, protocol = fields[6], protocol_map[fields[7]]

            # Look up the tag based on (dstport, protocol) otherwise default to "Untagged"
            tag = lookup.get((dstport, protocol), "Untagged")

            # Increment the count for the tag
            tag_matches[tag] = 1 + tag_matches.get(tag, 0) 

            # Increment the count for the port/protocol combination
            port_protocol_matches[(dstport, protocol)] = 1 + port_protocol_matches.get((dstport, protocol), 0)
    
    return tag_matches, port_protocol_matches

# Write the results to a csv file 
def write_results(filename, tag_matches, port_protocol_matches):
    with open(filename, mode = "w", newline="") as file: 
        writer = csv.writer(file) 
    
        # Start with the header
        writer.writerow(['Tag Counts:']) 
        writer.writerow(['Tag', 'Count'])
        writer.writerow([])

        # Write the tag counts
        for tag, count in tag_matches.items(): 
            writer.writerow([tag, count])
          
        # Next, write the second header
        writer.writerow([])
        writer.writerow(['Port/Protocol Combination Counts:'])
        writer.writerow(['Port', 'Protocol', 'Count'])
        writer.writerow([])
        
        # Write the port/protocol combination counts
        for (port, protocol), count in port_protocol_matches.items():
            writer.writerow([port, protocol, count])



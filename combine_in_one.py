import json

def load_json_data(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)

def combine_bonds(buyers_data, consumers_data):
    combined_data = []

    # Transform consumers data to include 'Consumer Sr. No' instead of 'Sr No.'
    consumers_dict = {
        (consumer["Prefix"], consumer["Bond Number"], consumer["Denominations"]): {
            **consumer, 
            "Consumer Sr. No": consumer["Sr No."],
            "Sr No.": None  # Remove 'Sr No.' to prevent overwriting
        }
        for consumer in consumers_data
    }

    # Process each buyer
    for buyer in buyers_data:
        if buyer["Status"] in ["Paid", "Expired"]:
            # Prepare new entry with renamed 'Sr No.' and remove it afterwards
            new_entry = {
                **buyer, 
                "Buyer Sr. No": buyer["Sr No."],
            }
            new_entry.pop("Sr No.", None)  # Safely remove the original 'Sr No.'

            key = (buyer["Prefix"], buyer["Bond Number"], buyer["Denominations"])
            
            # For 'Paid' status, attempt to find and merge with consumer data
            if buyer["Status"] == "Paid" and key in consumers_dict:
                consumer_data = consumers_dict[key]
                # Ensure 'Sr No.' is not in the final combined entry
                consumer_data.pop("Sr No.", None)
                new_entry.update(consumer_data)
            elif buyer["Status"] == "Expired":
                new_entry["Consumer Sr. No"] = None
                new_entry["Name of the Political Party"] = None
                new_entry["Date of Encashment"] = None
            
            combined_data.append(new_entry)

    return combined_data


def process_combined_data(data, party_names):
    processed_data = []
    for d in data:
        processed_data.append(
            {
                "PartyShortName": party_names[d["Name of the Political Party"] or ""],
                "Status": d["Status"],
                "Denominations": d["Denominations"],
                "Bond Number": d["Bond Number"],
                "PurchaseDate": d["Date of Purchase"],
                "EncashmentDate": d["Date of Encashment"],
                "PurchaserName": d["Name of the Purchaser"]
            }
        )
    return processed_data

# Load data
buyers_data = load_json_data('buyers_data.json')
consumers_data = load_json_data('consumers_data.json')
party_names = load_json_data('party_names.json')

# Combine and generate the new dataset
combined_data = combine_bonds(buyers_data, consumers_data)

processed_combined_data = process_combined_data(combined_data, party_names)

# Save the combined data to a new JSON file
output_file_name = 'combined_in_one.json'
with open(output_file_name, 'w') as file:
    json.dump(combined_data, file, indent=4)
    
    # Save the combined data to a new JSON file
output_file_name = 'combined_in_one_processed.json'
with open(output_file_name, 'w') as file:
    json.dump(processed_combined_data, file, indent=4)

print(f"Combined data saved")

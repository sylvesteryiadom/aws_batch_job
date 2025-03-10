import json

def transform_data(data: list) -> list:
    """
    Transform each item in the data:
    1. Replace the "t0" section with "counterPartyT0Ref": {"t0Ref": null}
    2. Add "comment": null after "counterparty"
    """
    transformed_data = []
    
    for item in data:
        # Create the new structure
        transformed_item = {
            "owner": item["owner"],
            "counterparty": item["counterparty"],
            "comment": None,  # Add the new key-value pair
            "counterPartyT0Ref": {"t0Ref": None},  # Replace "t0" with this
            "t0Ref": item["t0Ref"]
        }
        
        # Preserve any additional keys (e.g., counterP1, counterP2, etc.)
        for key, value in item.items():
            if key not in ["owner", "counterparty", "t0", "t0Ref"]:
                transformed_item[key] = value
        
        transformed_data.append(transformed_item)
    
    return transformed_data

def process_file(input_file: str, output_file: str):
    """
    Read the input file, transform the data, and write to the output file.
    """
    try:
        # Read the input file
        with open(input_file, "r", encoding="utf-8") as f:
            # Parse the JSON data (assuming one JSON object per line)
            data = [json.loads(line) for line in f if line.strip()]
        
        # Transform the data
        transformed_data = transform_data(data)
        
        # Write the transformed data to the output file
        with open(output_file, "w", encoding="utf-8") as f:
            for item in transformed_data:
                f.write(json.dumps(item) + "\n")
        
        print(f"Transformation complete. Output saved to {output_file}")
    
    except Exception as e:
        print(f"Error processing file: {e}")

# Main execution
if __name__ == "__main__":
    input_file = "data.json"  # Replace with your input file path
    output_file = "transformed_data.json"  # Replace with your desired output file path
    
    process_file(input_file, output_file)

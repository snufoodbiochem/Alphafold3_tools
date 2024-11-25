import json
import sys
import os
import re  # Regular expression for extracting PTM information

def generate_ids_with_error_handling(start_index, count):
    max_ids = 52  # Maximum IDs from A to ZA
    if start_index + count > max_ids:
        raise ValueError("ID generation exceeds the maximum allowed range of 'ZA'.")

    ids = []
    current_index = start_index

    while len(ids) < count:
        id = ""
        temp_index = current_index

        if temp_index < 26:  # A-Z
            id = chr(65 + temp_index)
        else:  # AA, BA, ..., ZA
            temp_index -= 26
            while temp_index >= 0:
                temp_index, remainder = divmod(temp_index, 26)
                id = chr(65 + remainder) + "A"
                temp_index -= 1

        ids.append(id)
        current_index += 1

    return ids

def parse_modifications(id_line, sequence_type):
    """
    Parse modifications from the ID line.

    :param id_line: The ID line from the FASTA file.
    :param sequence_type: The type of the sequence (protein, dna, or rna).
    :return: A list of modifications as dictionaries.
    """
    modifications = []
    matches = re.findall(r"&(\d+)_([A-Za-z]{3})", id_line)
    for match in matches:
        position = int(match[0])  # Extract the numeric position
        mod_type = match[1]       # Extract the 3-letter modification type

        if sequence_type == "protein":
            modifications.append({
                "ptmType": mod_type,
                "ptmPosition": position
            })
        elif sequence_type in {"dna", "rna"}:
            modifications.append({
                "modificationType": mod_type,
                "basePosition": position
            })
    return modifications

def fasta_to_json(fasta_file):
    json_file = os.path.splitext(fasta_file)[0] + ".json"
    json_name = os.path.splitext(os.path.basename(fasta_file))[0]

    with open(fasta_file, "r") as file:
        lines = file.readlines()

    sequences = []
    current_name = None
    current_sequence = []
    last_id_end = 0

    for line in lines:
        line = line.strip()
        if line.startswith(">"):
            if current_name is not None:
                name_parts = current_name.split("#")
                name = name_parts[0]
                count = int(name_parts[1]) if len(name_parts) > 1 else 1
                id_list = generate_ids_with_error_handling(last_id_end, count)
                last_id_end += count

                # Determine the sequence type (protein, dna, rna)
                sequence_type = "protein"  # Default type
                if "dna" in current_name.lower():
                    sequence_type = "dna"
                elif "rna" in current_name.lower():
                    sequence_type = "rna"

                modifications = parse_modifications(current_name, sequence_type)

                sequence_data = {
                    "id": id_list,
                    "sequence": "".join(current_sequence),
                }

                if modifications:
                    sequence_data["modifications"] = modifications

                sequences.append({sequence_type: sequence_data})

            current_name = line[1:]
            current_sequence = []
        else:
            current_sequence.append(line)

    if current_name is not None:
        name_parts = current_name.split("#")
        name = name_parts[0]
        count = int(name_parts[1]) if len(name_parts) > 1 else 1
        id_list = generate_ids_with_error_handling(last_id_end, count)
        last_id_end += count

        sequence_type = "protein"
        if "dna" in current_name.lower():
            sequence_type = "dna"
        elif "rna" in current_name.lower():
            sequence_type = "rna"

        modifications = parse_modifications(current_name, sequence_type)

        sequence_data = {
            "id": id_list,
            "sequence": "".join(current_sequence),
        }

        if modifications:
            sequence_data["modifications"] = modifications

        sequences.append({sequence_type: sequence_data})

    data = {
        "name": json_name,
        "modelSeeds": [1],
        "sequences": sequences,
        "dialect": "alphafold3",
        "version": 1
    }

    with open(json_file, "w") as json_out:
        json.dump(data, json_out, indent=2)
    print(f"Conversion complete. JSON file saved as {json_file}")

# Check if the script is executed with a FASTA file as input
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <fasta_file>")
        sys.exit(1)
    
    fasta_file = sys.argv[1]
    if not os.path.exists(fasta_file):
        print(f"Error: File '{fasta_file}' not found.")
        sys.exit(1)
    
    try:
        fasta_to_json(fasta_file)
    except ValueError as e:
        print(f"Error: {e}")


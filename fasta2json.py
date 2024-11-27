import json
import sys
import os
import re


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
    :param sequence_type: The type of the sequence (protein, dna, rna, or ligand).
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
        elif sequence_type == "ligand":
            modifications.append({
                "modificationType": mod_type,
                "position": position
            })
    return modifications


def fasta_to_json(fasta_file):
    # Generate the output JSON file name
    json_file = os.path.splitext(fasta_file)[0] + ".json"

    # Extract the base name for "name" field
    json_name = os.path.splitext(os.path.basename(fasta_file))[0]

    with open(fasta_file, "r") as file:
        lines = file.readlines()

    sequences = []
    current_name = None
    current_sequence = []
    last_id_end = 0  # Track the last used letter index for IDs (0 = 'A')

    for line in lines:
        line = line.strip()
        if line.startswith(">"):
            # Save the previous sequence if it exists
            if current_name is not None:
                # Parse ID from current_name
                name_parts = current_name.split("#")
                name = name_parts[0]
                count = int(name_parts[1]) if len(name_parts) > 1 else 1
                id_list = generate_ids_with_error_handling(last_id_end, count)
                last_id_end += count  # Update the last used index

                sequence_type = "protein"
                if "dna" in current_name:
                    sequence_type = "dna"
                elif "rna" in current_name:
                    sequence_type = "rna"
                elif "ligand" in current_name:
                    sequence_type = "ligand"
                elif "smile" in current_name:
                    sequence_type = "smile"

                modifications = parse_modifications(current_name, sequence_type)

                if sequence_type in {"protein", "dna", "rna"}:
                    sequences.append({
                        sequence_type: {
                            "id": id_list,
                            "sequence": "".join(current_sequence).replace(" ", "").upper(),
                            "modifications": modifications
                        }
                    })
                elif sequence_type == "ligand":
                    ccdCodes = ["".join(current_sequence).replace(" ", "").upper()]
                    sequences.append({
                        "ligand": {
                            "id": id_list,
                            "ccdCodes": ccdCodes
                        }
                    })
                elif sequence_type == "smile":
                    sequences.append({
                        "ligand": {
                            "id": id_list,
                            "smiles": "".join(current_sequence).replace(" ", "").upper()
                        }
                    })

            # Start a new sequence
            current_name = line[1:]
            current_sequence = []
        else:
            current_sequence.append(line)

    # Add the last sequence
    if current_name is not None:
        name_parts = current_name.split("#")
        name = name_parts[0]
        count = int(name_parts[1]) if len(name_parts) > 1 else 1
        id_list = generate_ids_with_error_handling(last_id_end, count)
        last_id_end += count  # Update the last used index

        sequence_type = "protein"
        if "dna" in current_name:
            sequence_type = "dna"
        elif "rna" in current_name:
            sequence_type = "rna"
        elif "ligand" in current_name:
            sequence_type = "ligand"
        elif "smile" in current_name:
            sequence_type = "smile"

        modifications = parse_modifications(current_name, sequence_type)

        if sequence_type in {"protein", "dna", "rna"}:
            sequences.append({
                sequence_type: {
                    "id": id_list,
                    "sequence": "".join(current_sequence).replace(" ", "").upper(),
                    "modifications": modifications
                }
            })
        elif sequence_type == "ligand":
            ccdCodes = ["".join(current_sequence).replace(" ", "").upper()]
            sequences.append({
                "ligand": {
                    "id": id_list,
                    "ccdCodes": ccdCodes
                }
            })

        elif sequence_type == "smile":
            sequences.append({
                "ligand": {
                    "id": id_list,
                    "smiles": "".join(current_sequence).replace(" ", "").upper()
                }
            })

    # Create the JSON structure
    data = {
        "name": json_name,  # Use the base name of the input file
        "modelSeeds": [1],
        "sequences": sequences,
        "dialect": "alphafold3",
        "version": 1
    }

    # Write to JSON file
    with open(json_file, "w") as json_out:
        json.dump(data, json_out, indent=2)
    print(f"\nConversion complete. JSON file saved as {json_file}")


# Check if the script is executed with a FASTA file as input
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <fasta_file>")
        sys.exit(1)

    fasta_file = sys.argv[1]
    if not os.path.exists(fasta_file):
        print(f"Error: File '{fasta_file}' not found.")
        sys.exit(1)

    fasta_to_json(fasta_file)



import json
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#This script refers to google's scripts

# --- Functions ---
def extract_data(json_file_path):
    """
    Load JSON data from a file.
    """
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print("Error reading the JSON file:", e)
        sys.exit(1)  # Exit the program if there is an error


def calculate_chain_lengths(token_res_ids):
    """
    Calculate chain lengths from a list of residue IDs.
    """
    chain_lengths = []
    current_chain_length = 1  # Initialize with 1 to account for the first residue
    previous_residue = token_res_ids[0]

    for residue in token_res_ids[1:]:
        if residue == previous_residue + 1:
            current_chain_length += 1
        else:
            chain_lengths.append(current_chain_length)
            current_chain_length = 1
        previous_residue = residue

    chain_lengths.append(current_chain_length)  # Add the last chain length
    return chain_lengths


def create_heatmap(pae_data, total_residues, output_path="pae_heatmap.png"):
    """
    Create and display a heatmap for Predicted Alignment Error (PAE).
    """
    plt.figure(figsize=(8, 6))
    pae_heatmap = sns.heatmap(
        pae_data,
        cmap='viridis',
        cbar_kws={'label': 'Expected Position Error (Ångströms)'},
        square=True
    )

    # Customize plot
    plt.title('Predicted Alignment Error (PAE) Heatmap')
    plt.xlabel('Scored residue')
    plt.ylabel('Aligned residue')

    # Set tick positions and labels
    tick_positions = np.arange(total_residues)
    tick_labels = [str(i + 1) for i in range(total_residues)]

    # Adjust tick frequency
    num_ticks = 10
    tick_step = max(total_residues // num_ticks, 1)
    plt.xticks(tick_positions[::tick_step], tick_labels[::tick_step], rotation=45)
    plt.yticks(tick_positions[::tick_step], tick_labels[::tick_step])

    # Show color legend
    cbar = pae_heatmap.collections[0].colorbar
    cbar.set_label('Expected Position Error (Ångströms)')

    plt.savefig(output_path, dpi=100, bbox_inches='tight')

    return pae_heatmap.get_figure()


# --- Main Program ---
def main():
    """
    Main function to execute the PAE heatmap workflow.
    """
    if len(sys.argv) < 2:
        print("Usage: python script.py <json_file>")
        print("json file is named confidences.json in your af3 seed---- folder!!!")
        sys.exit(1)

    # Load JSON file
    json_file = sys.argv[1]
    data = extract_data(json_file)

    # Extract relevant data
    pae_data = data['pae']
    token_res_ids = data['token_res_ids']

    print('Number of residues:', len(token_res_ids))

    # Calculate chain lengths
    chain_lengths = calculate_chain_lengths(token_res_ids)
    print('Entity lengths:', chain_lengths)

    # Calculate total number of residues
    total_residues = sum(chain_lengths)

    # Create heatmap
    create_heatmap(pae_data, total_residues)


if __name__ == "__main__":
    main()


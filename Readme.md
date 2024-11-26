
# AlphaFold3 Input File Preparation and Usage Guide

## 1. How to Prepare the Input File for AlphaFold3

### a. Create a `.fasta` File
- Name the file with a `.fasta` extension.
- Follow the **FASTA format** for the content.
- Lines starting with `>` are the **labels** for the sequences, and the sequence itself follows in uppercase letters (spaces are not allowed, but line breaks are).

**Example for an oxyR monomer:**
```fasta
>oxyR
MAEGASTERDA
TTTGVCCSAQW
```

---

### b. For Homomers
- Add `#<oligomer number>` to the label line.

**Example for an oxyR dimer:**
```fasta
>oxyR #2
MAEGASTERDA
TTTGVCCSAQW
```

---

### c. For Heteromers
- Add additional protein sequences below the initial sequence.

**Example for an oxyR dimer and hpr monomer:**
```fasta
>oxyR #2
MAEGASTERDA
MAEGASTERDA
TTTGVCCSAQW

>hpr
ASFGGGGHYWQQQ
MAEGASTERDA
TTTGVCCSAQW
```

---

### d. For DNA or RNA Sequences
- The label should start with `dna` or `rna`. The `#<oligomer number>` rule applies to homomers.

**Example for a DNA dimer:**
```fasta
>dna#2
GATACAGACCATTTT
```

---

### e. For Ligands
- Use the label `>ligand`. 
- Ligands can include molecules such as ATP, ADP, and ions like Mg or Zn. For other ligands, use the **3-letter CCD code**.

**Example:**
```fasta
>ligand#2
ATP
```

- For a comprehensive list of CCD codes, refer to:  
[EBI Ligand Search](https://www.ebi.ac.uk/pdbe-srv/pdbechem/)

---

### f. For Non-CCD Ligands
- Use the **SMILES format** for ligands not covered by the CCD code, and label the sequence with `>smile`.

**Example:**
```fasta
>smile
CC(=O)OC1C[NH+]2CCC1CC21
```

---

### g. For Post-Translational Modifications (PTMs)
- Add `&<amino acid number>_<PTM type>` to the label.

**Example:**
If cysteine at position 199 in oxyR dimer 1 is modified to cysteine sulfenic acid:
```fasta
>oxyR &199_CSO #2
```

**Common PTMs (3-letter codes):**
- **3HY**: 3-hydroxylated proline  
- **P1L**: S-palmitoyl-L-cysteine  
- **PTR**: Phosphotyrosine  
- **NMM**: Methylarginine  
- **LYZ**: Hydroxylysine  
- **CSO**: Cysteine sulfenic acid  
- **CSD**: Cysteine sulfinic acid  
- **OCS**: Cysteine sulfonic acid  
- **MYK**: Myristoyllysine  
- **SEP**: Phosphorylated serine  
- **TPO**: Phosphorylated threonine  

---

## 2. Usage Instructions

### a. Convert a `.fasta` File to JSON
Run the following command:
```bash
python3 fasta2json.py <input fasta>
```

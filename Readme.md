
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
- Ligands can include molecules such as ATP, ADP, and ions like Mg2+ or Zn2+. For other ligands, use the **3-letter CCD code**.

**Example:**
```fasta
>ligand#2
ATP
>ligand
MG
>ligand
CU
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
------------------------------

# AlphaFold3 입력 파일 준비 및 사용 가이드

## 1. AlphaFold3 입력 파일 준비 방법

### a. `.fasta` 파일 생성
- `.fasta` 확장자로 파일을 만듭니다.
- **FASTA 형식**을 따라야 합니다.
- `>`로 시작하는 라인은 서열의 **라벨(label)**이며, 그 다음 줄에 대문자로 아미노산 서열을 작성합니다. (공백은 허용되지 않으며, 줄바꿈은 허용됩니다.)

**oxyR 단량체(monome)의 예:**
```fasta
>oxyR
MAEGASTERDA
TTTGVCCSAQW
```

---

### b. 동종체(Homomer)의 경우
- 라벨 라인에 `#<올리고머 번호>`를 추가합니다.

**oxyR 이합체(dimer)의 예:**
```fasta
>oxyR #2
MAEGASTERDA
TTTGVCCSAQW
```

---

### c. 이종체(Heteromer)의 경우
- 추가적인 단백질 서열을 아래에 추가합니다.

**oxyR 이합체와 hpr 단량체의 예:**
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

### d. DNA 또는 RNA 서열의 경우
- 라벨은 `dna` 또는 `rna`로 시작해야 합니다. 동종체의 경우에도 `#<올리고머 번호>` 규칙이 적용됩니다.

**DNA 이합체의 예:**
```fasta
>dna#2
GATACAGACCATTTT
```

---

### e. 리간드(Ligand)의 경우
- 라벨은 `>ligand`로 지정합니다.
- ATP, ADP와 같은 분자와 Mg2+, Zn2+과 같은 이온을 포함하며, 다른 리간드는 **3문자 CCD 코드**를 사용합니다.

**예:**
```fasta
>ligand#2
ATP
>ligand
ZN
>ligand
CU
```

- 더 많은 CCD 코드는 다음 링크를 참고하세요:  
[EBI Ligand Search](https://www.ebi.ac.uk/pdbe-srv/pdbechem/)

---

### f. CCD 코드가 아닌 리간드의 경우
- CCD 코드에 포함되지 않은 리간드는 **SMILES 형식**을 사용하며, 라벨은 `>smile`로 지정합니다.

**예:**
```fasta
>smile
CC(=O)OC1C[NH+]2CCC1CC21
```

---

### g. 번역 후 수정(Post-Translational Modifications, PTMs)의 경우
- 라벨에 `&<아미노산 번호>_<PTM 유형>`을 추가합니다.

**예:**
oxyR 이합체의 199번 시스테인이 cysteine sulfenic acid로 변형된 경우:
```fasta
>oxyR &199_CSO #2
```

**주요 PTM (3문자 코드):**
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

## 2. 사용법

### a. `.fasta` 파일을 JSON으로 변환
다음 명령어를 실행하세요:
```bash
python3 fasta2json.py <input fasta>
```

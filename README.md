# Mass Spectrometry Imaging Alignment

A Python workflow for aligning molecular features between serial mass spectrometry imaging (MSI) scans by matching similar **m/z values within a configurable tolerance**.

The project cleans two raw MSI exports, aligns their molecular feature columns, creates a shared feature space, labels the source scan and combines both datasets into one analysis-ready table.

> [!IMPORTANT]
> This repository performs **m/z feature alignment between serial scans**. It does not perform spatial image registration, coordinate transformation or tissue-shape alignment.

## Table of Contents

- [Project Overview](#project-overview)
- [Why Alignment Is Needed](#why-alignment-is-needed)
- [Main Features](#main-features)
- [Workflow](#workflow)
- [Alignment Logic](#alignment-logic)
- [Repository Structure](#repository-structure)
- [Data Availability](#data-availability)
- [Expected Input Format](#expected-input-format)
- [Generated Outputs](#generated-outputs)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Package Components](#package-components)
- [Example Alignment](#example-alignment)
- [Performance Considerations](#performance-considerations)
- [Troubleshooting](#troubleshooting)
- [Limitations](#limitations)
- [Technologies](#technologies)
- [License](#license)

## Project Overview

Serial tissue sections can be measured in separate MSI scans. Although the scans may contain corresponding molecular features, the reported m/z column names are not always numerically identical.

For example:

```text
Reference scan:  500.1234
Sample scan:     500.1237
```

These values likely represent the same molecular feature when their difference is smaller than an accepted tolerance.

This project provides an object-oriented workflow that:

1. reads two raw MSI exports
2. converts them into structured CSV files
3. extracts numerical m/z column names
4. compares the reference and sample m/z values
5. matches values within a configurable tolerance
6. renames matched sample columns to the corresponding reference values
7. retains molecular features that occur in only one scan
8. creates compatible reference and sample tables
9. assigns source labels
10. concatenates both scans into one combined dataset

The resulting file can be used in later processing, statistical analysis, clustering, tissue-region comparison or machine-learning workflows.

## Why Alignment Is Needed

MSI exports may describe the same molecular signal with slightly different measured m/z values because of:

- small instrumental measurement differences
- scan-to-scan variation
- calibration differences
- numerical precision and rounding
- independent feature extraction for each scan

Without alignment, columns such as `500.1234` and `500.1237` would be treated as two unrelated features.

The alignment step maps sufficiently close values to one shared feature name so that the serial scans can be compared or combined consistently.

## Main Features

- Cleans tab-separated MSI export files
- Converts raw scan files into processed CSV tables
- Extracts numerical m/z feature names
- Sorts reference and sample m/z values
- Matches features using a configurable absolute tolerance
- Uses an efficient two-pointer comparison after sorting
- Renames matched sample features to reference feature names
- Preserves unmatched molecular features
- Creates the same column structure for both scans
- Adds a source label to every observation
- Combines aligned scans into one dataset
- Organizes raw, processed and aligned data in separate directories
- Creates required project directories automatically
- Uses reusable object-oriented processing, alignment and merging classes

## Workflow

```text
Reference raw scan                    Sample raw scan
        │                                    │
        ▼                                    ▼
 Clean and convert                     Clean and convert
        │                                    │
        ▼                                    ▼
Processed reference CSV             Processed sample CSV
        │                                    │
        └────────── Extract m/z columns ─────┘
                             │
                             ▼
                  Sort numerical m/z values
                             │
                             ▼
             Compare values within tolerance
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
     Matched features                  Unmatched features
  Rename sample columns            Preserve in shared schema
            │                                 │
            └────────────────┬────────────────┘
                             ▼
               Save aligned scan tables
                             │
                             ▼
                  Add scan source labels
                             │
                             ▼
             Harmonize columns and concatenate
                             │
                             ▼
                 data/aligned/combined_data.csv
```

## Alignment Logic

### Tolerance-Based Matching

The project compares sorted reference and sample m/z arrays.

For a reference value `r`, sample value `s` and tolerance `t`, a match is accepted when:

```text
|r - s| <= t
```

The default tolerance in `config.py` is:

```python
tolerance = 0.0005
```

When a match is found, the sample feature name is mapped to the corresponding reference feature name.

Example:

```text
Reference m/z:  500.1234
Sample m/z:     500.1237
Difference:     0.0003
Tolerance:      0.0005
Result:         Match
```

The sample column `500.1237` is therefore renamed to `500.1234`.

### Unmatched Features

Not every feature must occur in both scans.

When a sample m/z value does not match an available reference value within the tolerance, it is retained as an additional feature rather than discarded.

Likewise, features present in the reference but absent from the sample remain part of the final shared schema.

### Merged Feature Space

Before concatenation, the two aligned datasets are given the same column order.

Missing feature columns are filled with zero so that both scans can be represented in one table.

A `Source` column is added to distinguish observations from the reference and sample scans.

The final combined table therefore contains:

```text
Index | X | Y | shared m/z features ... | Source
```

## Repository Structure

```text
Mass-Spectrometry-Imaging-Alignment/
│
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── config.py
├── run_alignment.py
│
├── data/
│   ├── raw/
│   │   └── place the two original MSI scan files here
│   │
│   ├── processed/
│   │   └── cleaned CSV files are generated here
│   │
│   └── aligned/
│       ├── aligned reference data
│       ├── aligned sample data
│       └── combined_data.csv
│
├── figures/
│   └── reserved for future diagnostic visualizations
│
└── msi_alignment/
    ├── __init__.py
    ├── processing.py
    ├── alignment.py
    └── merging.py
```

### Root files

| File | Purpose |
|---|---|
| `run_alignment.py` | Runs the complete preprocessing, alignment and merging pipeline |
| `config.py` | Defines project paths, input filenames and the m/z tolerance |
| `requirements.txt` | Lists the Python dependencies |
| `.gitignore` | Excludes large datasets, generated files, caches and environment-specific content |
| `LICENSE` | Contains the MIT License |

### Package files

| File | Purpose |
|---|---|
| `msi_alignment/processing.py` | Cleans raw exports and extracts m/z columns |
| `msi_alignment/alignment.py` | Matches m/z values and creates aligned scan files |
| `msi_alignment/merging.py` | Harmonizes columns, labels sources and combines the scans |
| `msi_alignment/__init__.py` | Marks the directory as an importable Python package |

## Data Availability

The original MSI datasets are **not included in this repository**.

Each source file is larger than 500 MB, which makes the complete experimental data unsuitable for direct storage in this GitHub repository. The repository therefore provides the processing and alignment code, directory structure, dependency list and configuration but not the underlying biological datasets.

To run the project, provide two compatible MSI export files locally:

```text
data/raw/
├── reference_scan.txt
└── sample_scan.txt
```

Then update their filenames in `config.py`.

Because the original data are unavailable in the repository:

- cloning the repository alone is not enough to reproduce the final combined dataset
- users must supply MSI files with the expected structure
- generated files under `data/processed/` and `data/aligned/` are created locally
- no visual output is included because the current workflow produces aligned tabular data rather than plots

The `figures/` directory is reserved for possible future diagnostics, such as m/z difference distributions or alignment-quality summaries.

## Expected Input Format

The current preprocessing workflow expects tab-separated text files with:

1. metadata or non-tabular content in the first three lines
2. feature names in the fourth line
3. measurement data beginning on the fifth line

Conceptually:

```text
Metadata line 1
Metadata line 2
Metadata line 3
Index    X    Y    100.1234    200.5678    300.9012    ...
0        1    1    15.2        8.4         0.0         ...
1        2    1    12.7        4.1         2.8         ...
...
```

During preprocessing:

- the first three columns are assigned the names `Index`, `X` and `Y`
- numerical column names are interpreted as m/z features
- two trailing columns are assigned the names `Last_1` and `Last_2`
- the cleaned table is saved as CSV

> [!NOTE]
> The parser is tailored to the export structure used for this project. Other MSI formats may require changes to `processing.py`.

## Generated Outputs

### Processed files

The cleaning stage writes one processed CSV per input scan to:

```text
data/processed/
```

The generated names follow this pattern:

```text
processed_<original-file-stem>.csv
```

### Aligned files

The alignment stage writes aligned versions of the reference and sample scans to:

```text
data/aligned/
```

The names follow this pattern:

```text
aligned_<processed-file-stem>.csv
```

### Combined dataset

The final merged output is:

```text
data/aligned/combined_data.csv
```

This table contains the union of aligned m/z features, spatial information, intensity values and the source label.

## Installation

Clone the repository:

```bash
git clone https://github.com/LittleBigPluton/Mass-Spectrometry-Imaging-Alignment.git
cd Mass-Spectrometry-Imaging-Alignment
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the required packages:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Configuration

Edit `config.py` before running the pipeline.

The configuration defines the directory structure:

```python
from pathlib import Path

root_directory = Path(__file__).resolve().parent

data_dir = root_directory / "data"
raw_data_dir = data_dir / "raw"
processed_data_dir = data_dir / "processed"
aligned_data_dir = data_dir / "aligned"
figures_dir = root_directory / "figures"
```

The directories are created automatically if they do not already exist.

Set the two local raw-data filenames:

```python
reference_file = "reference_scan.txt"
sample_file = "sample_scan.txt"
```

Set the accepted m/z difference:

```python
tolerance = 0.0005
```

A smaller tolerance requires closer m/z agreement. A larger tolerance allows more values to be treated as the same feature.

The appropriate value depends on the instrument, calibration, measurement resolution and intended analysis.

## Usage

### 1. Add the source files

Place both files in:

```text
data/raw/
```

Example:

```text
data/raw/
├── reference_scan.txt
└── sample_scan.txt
```

### 2. Update `config.py`

```python
reference_file = "reference_scan.txt"
sample_file = "sample_scan.txt"
tolerance = 0.0005
```

### 3. Run the pipeline

From the repository root:

```bash
python run_alignment.py
```

The runner performs the following operations:

```python
reference_file_object.clean_data()
reference_file_object.get_columns()

sample_file_object.clean_data()
sample_file_object.get_columns()

alignment_objects.match_mz_columns()
alignment_objects.reference_columns_addition()
alignment_objects.modify_files()

merging_object.set_DataFrame()
merging_object.assign_sample_label()
merging_object.add_reference_missing_columns()
merging_object.merge_reference_and_sample()
```

### 4. Inspect the results

Generated files are stored under:

```text
data/processed/
data/aligned/
```

The final result is:

```text
data/aligned/combined_data.csv
```

## Package Components

### Processing

The `processing` class represents one MSI scan file.

Main responsibilities:

- store the input filename and path
- read the first four lines
- extract the fourth-line feature names
- assign standard names to the first spatial columns
- read the remaining tab-separated measurements
- save a processed CSV
- update the object's current file path
- extract all column names
- convert valid numerical column names into an m/z array

Key methods:

| Method | Description |
|---|---|
| `clean_data()` | Converts the raw export into a cleaned CSV |
| `get_columns()` | Extracts all columns and identifies numerical m/z features |
| `set_processed_files_name()` | Creates and stores the processed output name and path |

### Alignment

The `alignment` class receives the processed reference and sample objects.

Main responsibilities:

- sort both numerical m/z arrays
- compare them using two moving indices
- map close sample values to reference values
- identify unmatched sample features
- expand the reference schema
- rename matched sample columns
- save aligned reference and sample files

Key methods:

| Method | Description |
|---|---|
| `match_mz_columns()` | Builds the match mapping and unmatched-feature list |
| `reference_columns_addition()` | Adds unmatched sample features to the reference schema |
| `modify_files()` | Renames sample features and saves aligned tables |

### Merging

The `merging` class receives the completed alignment object.

Main responsibilities:

- load the aligned reference and sample CSV files
- label the source scan
- create compatible columns
- fill absent feature columns with zero
- enforce the same column order
- concatenate both datasets
- save the combined result

Key methods:

| Method | Description |
|---|---|
| `set_DataFrame()` | Loads the aligned CSV files |
| `assign_sample_label()` | Adds source labels |
| `add_reference_missing_columns()` | Harmonizes the feature schema |
| `merge_reference_and_sample()` | Concatenates and saves the final table |

## Example Alignment

Assume the sorted features are:

```text
Reference:
100.1000
200.2000
300.3000

Sample:
100.1003
250.2500
300.2998
```

With:

```text
tolerance = 0.0005
```

The result is:

| Sample m/z | Reference m/z | Difference | Action |
|---:|---:|---:|---|
| `100.1003` | `100.1000` | `0.0003` | Rename sample feature to `100.1000` |
| `250.2500` | — | — | Preserve as an unmatched feature |
| `300.2998` | `300.3000` | `0.0002` | Rename sample feature to `300.3000` |

The final shared feature space contains:

```text
100.1000
200.2000
250.2500
300.3000
```

Rows from either scan receive zero for features that were not measured in that scan.

## Performance Considerations

The project is designed for wide MSI tables and very large input files but pandas operations still require substantial memory.

Important considerations:

- both aligned CSV files are loaded into memory during merging
- concatenation creates an additional combined DataFrame
- the final memory requirement can therefore be considerably larger than one input file
- CSV parsing is slower and less memory-efficient than binary formats
- adding or copying many columns can increase memory consumption
- local disk space is required for raw, processed, aligned and combined versions of the data

The m/z matching logic first sorts both feature arrays and then performs a two-pointer scan.

For `R` reference features and `S` sample features:

```text
Sorting:
O(R log R + S log S)

Matching after sorting:
O(R + S)
```

For very large datasets, future versions could use chunked reading or columnar formats such as Parquet.

## Troubleshooting

### `FileNotFoundError`

Confirm that:

- both files are inside `data/raw/`
- the names in `config.py` match exactly
- file extensions and capitalization are correct
- the script is run from the repository root

### `Not enough lines to extract column names`

The preprocessing function expects at least four lines and reads feature names from the fourth line.

Check whether the source export follows the expected structure.

### Column count mismatch

An error such as:

```text
ValueError: Length mismatch
```

means the number of generated column names does not match the number of columns read from the data rows.

Inspect:

- the fourth header line
- the number of initial coordinate fields
- the two expected trailing fields
- tab delimiters
- unexpected empty columns

### No m/z features are detected

Only column names that pandas can convert to numbers are included in the m/z comparison.

Inspect the processed CSV header and confirm that m/z feature names are numerical strings.

### Too many or too few matches

Review the configured tolerance:

```python
tolerance = 0.0005
```

A value that is too small may leave corresponding features unmatched. A value that is too large may combine distinct molecular features.

### High memory usage

The source files are larger than 500 MB and the pipeline creates multiple in-memory DataFrames.

Possible local mitigations:

- close unrelated applications
- ensure sufficient RAM and swap space
- avoid opening the same files in other programs
- run the script on a machine with more memory
- delete intermediate outputs only after validating the final result

### Empty `figures/` directory

This is expected. The current pipeline produces aligned CSV tables and does not generate plots.

## Limitations

- Only two scans are aligned in one pipeline run.
- One scan must be selected as the reference.
- Matching uses absolute m/z distance only.
- The tolerance is global for all m/z values.
- The workflow does not perform spatial image registration.
- The workflow does not correct X/Y coordinates between tissue sections.
- The input parser is specific to the current tab-separated export structure.
- The full experimental datasets are not publicly included.
- No small demonstration dataset is currently provided.
- No visual alignment-quality report is generated.
- Automated tests are not yet included.
- CSV files may be memory-intensive for datasets of this size.

## Technologies

- Python
- pandas
- NumPy
- pathlib
- CSV processing
- Object-oriented programming
- Tolerance-based feature matching

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

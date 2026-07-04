import pandas as pd
import csv

from msi_alignment.processing import processing
from pathlib import Path
from config import (
    tolerance,
    aligned_data_dir
)

class alignment(processing):

    def __init__(self, reference_data_object, sample_data_object):
        self.reference_data_object = reference_data_object
        self.sample_data_object = sample_data_object
        self.columns_to_change = {}
        self.columns_to_add = []
        self.column_names = None
        self.aligned_reference_data_name = None
        self.aligned_reference_data_exact_path = None
        self.aligned_sample_data_name = None
        self.aligned_sample_data_exact_path = None

    def match_mz_columns(self):
        is_reached_end = False
        reference_index = 0
        sample_index = 0

        sorted_reference_data_columns = sorted(self.reference_data_object.numeric_columns)
        sorted_sample_data_columns = sorted(self.sample_data_object.numeric_columns)
        length_sorted_reference_columns = len(sorted_reference_data_columns)
        length_sorted_sample_columns = len(sorted_sample_data_columns)

        print(f"Number of the reference data columns: {length_sorted_reference_columns}")
        print(f"Number of the reference data columns: {length_sorted_sample_columns}")

        while not is_reached_end:
            if sample_index >= length_sorted_sample_columns:
                is_reached_end = True
                print("Sample list reached end. Last element is observing.")
                continue

            if reference_index >= length_sorted_reference_columns :
                is_reached_end = True
                print("Reference list reached end. Adding remaining sample elements to columns_to_add.")
                self.columns_to_add.extend(str(value) for value in sorted_sample_data_columns[sample_index:])
                continue

            reference_mz = sorted_reference_data_columns[reference_index]
            sample_mz = sorted_sample_data_columns[sample_index]
            difference = reference_mz - sample_mz

            if abs(difference) <= tolerance:
                print("Accept")
                self.columns_to_change[str(sample_mz)] = str(reference_mz)
                reference_index = reference_index + 1
                sample_index = sample_index + 1
            elif difference > 0:
                print("Change sample index for a greater one")
                self.columns_to_add.append(str(sample_mz))
                sample_index = sample_index + 1
            else:
                print("Change reference index for a greater one")
                reference_index = reference_index + 1

    # Function to add columns in reference file
    def reference_columns_addition(self):
        with open(self.reference_data_object.msi_data_exact_path, "r", encoding="utf-8") as file:
            lines = file.read().splitlines()

        if len(lines) < 4:
            raise ValueError("File does not have enough lines to modify.")

        column_names = ["", ""] + lines[3].split("\t") + list(self.columns_to_add)
        lines[3] = "\t".join(column_names)

        self.aligned_reference_data_name = f"aligned_{Path(self.reference_data_object.msi_data_path).stem}.csv"
        self.aligned_reference_data_exact_path = aligned_data_dir / self.aligned_reference_data_name
        with open(self.aligned_reference_data_exact_path, "w", encoding="utf-8", newline="") as file:
            file.write("\n".join(lines) + "\n")
        print("File saved to:",self.aligned_reference_data_exact_path)

    # Modify file
    def modify_files(self):
        df = pd.read_csv(self.sample_data_object.msi_data_exact_path)
        if len(self.columns_to_change) > 0:
            # Save DF's column names
            mz_values = list(self.sample_data_object.msi_data_columns)
            for mz_value in self.columns_to_change:
                if mz_value in mz_values:
                    print("Changed")
                    print(mz_value)
                    print(self.columns_to_change[mz_value])
                    mz_values = [self.columns_to_change[mz_value] if column_name == mz_value else column_name for column_name in mz_values]
            df.columns = mz_values

        self.aligned_sample_data_name = f"aligned_{Path(self.sample_data_object.msi_data_path).stem}.csv"
        self.aligned_sample_data_exact_path = aligned_data_dir / self.aligned_sample_data_name
        df.to_csv(self.aligned_sample_data_exact_path, index=False, quoting=csv.QUOTE_NONE, escapechar="\\")
        print("File saved to:",self.aligned_sample_data_exact_path)

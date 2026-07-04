import pandas as pd
from config import aligned_data_dir

class merging:
    def __init__(self,allignment_objects):
        self.alligned_reference_path = allignment_objects.aligned_reference_data_exact_path
        self.alligned_sample_path = allignment_objects.aligned_sample_data_exact_path
        self.df_reference = None
        self.df_sample = None

    def set_DataFrame(self):
        self.df_reference = pd.read_csv(self.alligned_reference_path)
        self.df_sample = pd.read_csv(self.alligned_sample_path)

    def assign_sample_label(self):
        self.df_reference["Source"] = "Sample1"
        self.df_sample["Source"] = "Sample 2"

    def add_reference_missing_columns(self):
        # Identify missing columns in the sample dataset
        missing_cols = [column for column in self.df_reference.columns if column not in self.df_sample.columns]

        # Add missing columns as 0 in the sample dataset
        self.df_sample = self.df_sample.reindex(columns = self.df_reference.columns,fill_value = 0)

        # Refresh memory for dataframes
        self.df_reference = self.df_reference.copy()
        self.df_sample = self.df_sample.copy()

    def merge_reference_and_sample(self):
        # Ensure the order of columns matches in both datasets
        self.df_sample = self.df_sample[self.df_reference.columns]

        # Concatenate datasets
        combined_data = pd.concat([self.df_reference, self.df_sample], ignore_index=True)

        # Save the combined dataset
        combined_data_name = aligned_data_dir/"combined_data.csv"
        combined_data.to_csv(combined_data_name, index=False, na_rep="NA")

from msi_alignment.processing import processing
from msi_alignment.alignment import alignment
from msi_alignment.merging import merging
from config import (
    data_dir,
    reference_file,
    sample_file
)


reference_file_object = processing(reference_file)
reference_file_object.clean_data()
reference_columns = reference_file_object.get_columns()

sample_file_object = processing(sample_file)
sample_file_object.clean_data()
sample_columns = sample_file_object.get_columns()

alignment_objects = alignment(reference_file_object, sample_file_object)
alignment_objects.match_mz_columns()
alignment_objects.reference_columns_addition()
alignment_objects.modify_files()

merging_object = merging(alignment_objects)
merging_object.set_DataFrame()
merging_object.assign_sample_label()
merging_object.add_reference_missing_columns()
merging_object.merge_reference_and_sample()

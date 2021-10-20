import json
import datetime
import os 
import pathlib
import subprocess

# This is used for record-keeping
now = datetime.datetime.now()
run_uid = now.strftime("%Y_%m_%d_%H_%M")

# Initialize meta-parameters objects
training_param = {}
generator_param = {}
network_param = {}
generator_test_param = {}

# An epoch is defined as the number of batches pulled from the dataset. Because our datasets are VERY large. Often, we cannot
# go through the entirity of the data so we define an epoch slightly differently than is usual.
steps_per_epoch = 10

# Those are parameters used for the Validation test generator. Here the test is done on the beginning of the data but
# this can be a separate file
generator_test_param["type"] = "generator"  # type of collection
generator_test_param["name"] = "EphysGenerator"  # Name of object in the collection
generator_test_param[
    "pre_post_frame"
] = 30  # Number of frame provided before and after the predicted frame
generator_test_param["train_path"] = os.path.join(
    pathlib.Path(__file__).parent.absolute(),
    "..",
    "sample_data",
    "ephys_tiny_continuous.dat2",
)
generator_test_param["batch_size"] = 100
generator_test_param["start_frame"] = 0
generator_test_param["end_frame"] = 1000
generator_test_param[
    "pre_post_omission"
] = 1  # Number of frame omitted before and after the predicted frame
generator_test_param[
    "steps_per_epoch"
] = -1  # No step necessary for testing as epochs are not relevant. -1 deactivate it.

# Those are parameters used for the main data generator
generator_param["type"] = "generator"
generator_param["steps_per_epoch"] = steps_per_epoch
generator_param["name"] = "EphysGenerator"
generator_param["pre_post_frame"] = 30
generator_param["train_path"] = os.path.join(
    pathlib.Path(__file__).parent.absolute(),
    "..",
    "sample_data",
    "ephys_tiny_continuous.dat2",
)
generator_param["batch_size"] = 100
generator_param["start_frame"] = 2000
generator_param["end_frame"] = 3000
generator_param["pre_post_omission"] = 1

# Those are parameters used for the network topology
network_param["type"] = "network"
network_param[
    "name"
] = "unet_single_ephys_1024"  # Name of network topology in the collection

# Those are parameters used for the training process
training_param["type"] = "trainer"
training_param["name"] = "core_trainer"
training_param["loss"] = "mean_absolute_error"

training_param["model_string"] = (
    network_param["name"]
    + "_"
    + training_param["loss"]
    + "_"
    + run_uid
)
training_param["output_path"] = "/Users/jeromel/Desktop/tmp"

args = {
    "run_uid": run_uid,
    "training_params": training_param,
    "generator_params": generator_param,
    "test_generator_params": generator_test_param,
    "network_params": network_param,
    "output_full_args": True
}

input_json = os.path.join(training_param["output_path"], "input_training_ephys_tiny.json")

with open(input_json, 'w') as file_handle:
    json.dump(args, file_handle)

module_cmd = ["python", "-m", "deepinterpolation.cli.training",
                "--input_json", input_json]

subprocess.check_call(module_cmd)

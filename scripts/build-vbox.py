import os
import boto3
import subprocess
from botocore.exceptions import NoCredentialsError

producer_version = os.getenv('PRODUCER_VERSION')
access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

def BuildWithPacker(producer_version):
# Execute the Packer command to build Producer Studio and 
# return the status code (0 = success, others = failure)

    packer_dir = "../packer/studio-vbox"
    packer_path = "/usr/local/bin/packer"
    build_command = [packer_path, "build", "-var", "version=" + producer_version, "producer_build_studio_vbox.json"]

    print("Building Producer Studio", producer_version, "for VirtualBox")
    with subprocess.Popen(build_command, cwd=packer_dir, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as build_process:
        # Display output as the build is running.  By default, subprocess displays output only when it is completed.
        for line in build_process.stdout:
            print (line, end='')
    return build_process.returncode

def CopyToS3(producer_version, access_key_id, secret_access_key):
# Start AWS session and copy Producer Studio to S3 bucket

    release_array = producer_version.split('.')
    version_release = release_array[0]
    major_release = release_array[1]
    minor_release = release_array[2]
    source_path = "../packer/studio-vbox/builds/producer-studio-" + producer_version
    source_file = "producer-studio-" + producer_version + ".ova"
    filename = source_path + "/" + source_file
    destination_bucket = "tba-producer-builds-prod"
    destination_version = version_release + "." + major_release + "." + minor_release
    destination_key = "Producer Studio/" + destination_version + "/Virtual Box/producer-studio-" + producer_version + ".ova"

    session = boto3.Session(aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    s3 = session.resource('s3')
    print("Copying Producer Studio", producer_version, "to S3 bucket.")
    try:
        s3.Bucket(destination_bucket).upload_file(filename, destination_key)
        print("Producer Studio", producer_version, "successfully copied to S3 bucket.")
    except FileNotFoundError:
        print("The file was not found.")
        return False
    except NoCredentialsError:
        print("AWS credentials invalid or not found.")
        return False
    return True

if producer_version == "":
    print("Error: PRODUCER_VERSION is not defined.")
else:
    build_status = BuildWithPacker(producer_version)
    if build_status == 0:
        if CopyToS3(producer_version, access_key_id, secret_access_key) == True:
            print("Build succeeded.")
        else:
            print("Build failed.")


PRODUCER-AMI-BUILDER
====================

PRODUCER-AMI-BUILDER is an Ansible playbook that can be used to create PRODUCER AWS AMI.

# Ansible

## Requirements

1. Ansible is required to run PRODUCER-AMI-BUILDER.
Instructions to install Ansible on Mac are available at:
https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-ansible-on-macos

2. Create a virtual machine with the following requirements:
   - Minimum CPU: 2
   - Minimum RAM: 4 GB
   - Operating system: Rocky Linux
   - Minimum disk space for the root drive: 20 GB
   - A second disk for data
 
3. Clone PRODUCER-AMI-BUILDER to your Mac.

4. Create a file named **vault-password** in the root of the project.
   Add the Ansible vault password (see LastPass.)
   This file is used by ansible-vault to decrypt secrets such as application passwords.

5. Edit the file **producer-ami-builder/inventory**
   - Replace the ip address beneath **[producer_vm]** with the IP address of your virtual machine.
   - Replace the value of **ansible_user** with the username to ssh into your virtual machine. This user must have sudo privileges.
   - Replace the value of **ansible_ssh_private_key_file** with the path to the private key of your virtual machine.

6. For Toon Boom personnel:
   - Edit **users/defaults/rnd.yml** or **users/default/sysadmin.yml** to add your user account.
   - Add your public key in **users/files/ssh_keys**

## Run PRODUCER-AMI-BUILDER

Execute the playbook:
`ansible-playbook -i inventory --vault-password-file vault-password setup-producer.yml`

## Structure

PRODUCER-BUILDER is divided into separate roles that install the required components for Producer.

- **cloudwatch** - Installs the AWS CloudWatch agent.  This role runs EC2 instances only.
- **common-vbox** - Installs required packages for VirtualBox.
- **common-vmare** - Installs required packages for VMWare.
- **common** - Installs the basic software requirements for Producer.
- **database-backup-cloud** - Installs scripts and cron jobs to backup the database to S3.  This role runs EC2 instances only.
- **database-backup-studio** - Installs scripts and cron jobs to backup the database to S3.  This role runs on VirtualBox and VMWare only.
- **ffmpeg** - Installs ffmpeg and its requirements.
- **firewalld** - Installs and configures firewalld.
- **firewalld-studio** - Installs and configure firewalld for Producer Studio.
- **postgresql** - Installs and configures Postgres SQL.
- **producer** - Gets Producer files from S3 and performs configuration.
- **producer_logrotate** - Configures logrotate service for Producer.
- **python** - Installs Python requirements for Producer.
- **rabbitmq** - Installs and configures rabbitmq and it's Erlang requirement.
- **redis** - Installs Redis which is implemented since Producer 22.2.
- **users** - Creates user accounts for the Toon Boom sysadmin and RnD teams.

Each role is divided into one or more of the following folders:

- **default** - Contains variables used by each role.  If you need to change which version of a componenet that is installed, make changes to the files in this folder.
- **files** - Contains configuration and other files that are copied to the EC2 instance when the role is executed.
- **tasks** - Contains the steps that are executed by a role.
- **templates** - Contains template files that are copied to the EC2 instance when the role is executed.

# Packer

### Install Packer
Packer can be installed on Mac using Homebrew.

`brew install packer`

### AWS

If you have configured your aws cli with credentials (~/.aws/credentials on macOS) by default Packer with take the default credentials. If you configured multiple profiles with your aws cli, you can set the `AWS_PROFILE` environment variable to select which profile to use.

You can also overwrite any aws configured credentials by setting both the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` envinoment variables.

## Build an AMI with Packer

### In producer-dev AWS account
```bash
cd packer/cloud-aws
packer build -var-file=producer_build_vars_producer-dev.json producer_build_cloud_aws.json
```

## Build a vm for VirtualBox with Packer
```bash
cd packer/studio-vbox
packer build producer_build_studio_vbox.json
```
The output is an ova file in the builds directory

## Build a vm for VMWare with Packer

### Prequisites:
The build server must have the following installed:
- VMWare Fusion, VMWare Workstation, or VMWare Player.
- Ovftools.  You can download ovftools at https://my.vmware.com/.  Registration is required.
- A private key for the packer user account in the folder ~/.ssh.  The key is available in the password manager.

```bash
cd packer/studio-vmware
packer build producer_build_studio_vmware.json
```
The output is the builds directory.  Only two files are required, the Producer vmkd and ovf.
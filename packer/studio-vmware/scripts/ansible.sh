#!/bin/bash -eux

# Install EPEL.
dnf -y install epel-release

# Install Ansible.
yum -y install ansible

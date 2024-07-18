#!/bin/bash -eux

# Install EPEL.
dnf -y install epel-release

# Install Ansible.
dnf -y install ansible

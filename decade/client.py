#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Curtis Yu
@contact: cuyu@splunk.com
@since: 06/12/2017
"""
import docker
import paramiko


class Client(object):
    """
    A client to wrap both ssh and docker client
    """
    def __init__(self, host, ssh_username=None, ssh_password=None, ssh_port=22):
        if ssh_username and ssh_password:
            self._ssh_client = paramiko.SSHClient()
            self._ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._ssh_client.connect(host, ssh_port, ssh_username, ssh_password)
            self._sftp = paramiko.SFTPClient.from_transport(self._ssh_client.get_transport())
            self._docker_client = None
        else:
            self._ssh_client = None
            self._docker_client = docker.from_env()
            self._docker_container = self._docker_client.get(host)

    def execute(self, command):
        if self._ssh_client:
            pass
        else:
            return self._docker_container.exec_run(command)

    def send_files(self, local_path, remote_path):
        if self._ssh_client:
            self._sftp.put(local_path, remote_path)
        else:
            # todo: archive the folder
            data = None
            self._docker_container.put_archive(remote_path, data)

    def fetch_files(self, remote_path, local_path):
        if self._ssh_client:
            self._sftp.get(remote_path, local_path)
        else:
            data, stat = self._docker_container.get_archive(remote_path)
            # todo: save the date to local_path and unarchived it

#  coding=utf-8
"""Tests role"""
import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts()


def test_service_running(host):
    """
    Test if service is running.
    """
    # Check service
    service = host.service('accelize_container')
    assert service.is_running
    assert service.is_enabled

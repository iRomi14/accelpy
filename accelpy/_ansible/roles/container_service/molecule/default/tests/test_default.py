#  coding=utf-8
"""Tests role"""
import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts()


def test_configuration_ready(host):
    """
    Test if service configuration properly generated.
    """
    conf = host.file('/etc/systemd/system/accelize_container.service')
    assert conf.exists
    assert conf.contains('--env FPGA_SLOTS=0')
    assert conf.contains('-p 8080:8080/tcp')
    assert (conf.contains('--privileged') or
            conf.contains('--device') or
            conf.contains('--mount'))

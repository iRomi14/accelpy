"""Extra Ansible filters"""


def rules_ports(
        firewall_rules, only_restricted=False, redirect=False, *_, **__):
    """
    Return restricted ports (<1024) from firewall rules.

    Args:
        firewall_rules (list of dict): Firewall rules.
        only_restricted (bool): If True, list only ports < 1024.
        redirect (bool): If True, provides a redirect for ports < 1024 in the
            unrestricted port range.

    Returns:
        list of dict: port, redirected port, protocol
    """
    filtered = []
    for rule in firewall_rules:
        start = int(rule['start_port'])
        end = int(rule['end_port'])
        if not only_restricted or start < 1024:
            protocol = rule['protocol']
            filtered += [{
                'port': str(port),
                'redirect': str(port + (
                    60000 if port < 1024 and redirect else 0)),
                'protocol': protocol} for port in range(start, end + 1)]
    return filtered


def publish_ports(firewall_rules, redirect=False, *_, **__):
    """
    Returns all ports as "--publish" arguments.

    Args:
        firewall_rules (list of dict): Firewall rules.
        redirect (bool): Apply port redirection for port <1024.

    Returns:
        str: arguments
    """
    return ' '.join(
        f"-p {port['redirect']}:{port['port']}"
        f"{'' if port['protocol'] == 'all' else '/' + port['protocol']}"
        for port in rules_ports(firewall_rules, redirect=redirect))


def publish_devices(path_list, *_, **__):
    """
    Returns paths as "--device" or "--mount" arguments.

    Fall back to "--privileged" if no devices found.

    Args:
        path_list (str): List of devices paths, one path per line.

    Returns:
        str: arguments
    """
    return ' '.join(
        f'--device={path.strip()}' if path.startswith('/dev') else
        f'--mount=type=bind,src={path.strip()},target={path.strip()}'
        for path in path_list.strip().splitlines()
        if not path.startswith('/home')) or '--privileged'


class FilterModule(object):
    """Return filter plugin"""

    @staticmethod
    def filters():
        """Return filter"""
        return {'rules_ports': rules_ports,
                'publish_ports': publish_ports,
                'publish_devices': publish_devices}

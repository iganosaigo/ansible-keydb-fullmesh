from __future__ import annotations
from ansible.errors import AnsibleFilterTypeError


# Input supposed to be in format of output from keydb_inventory
def keydb_select(data, type="ip", role="master"):
    if not isinstance(data, list):
        raise AnsibleFilterTypeError("Input must be list")

    if type not in ["ip", "hostname"]:
        raise AnsibleFilterTypeError("type must be ip or hostname")

    roles = ["master", "replica"]
    if role not in roles:
        raise AnsibleFilterTypeError(f"role must be {' or '.join(roles)}")

    result = []
    for host in data:
        host_address = host["address"]
        host_name = host["hostname"]
        host_role = host["role"]
        if host_role == role:
            if type == "ip":
                result.append(host_address)
            elif type == "hostname":
                result.append(host_name)

    return result


def keydb_inventory(data):
    if not isinstance(data, dict):
        raise AnsibleFilterTypeError("Input must be dict")

    result = []
    try:
        group = data["group"]
        hostvars = data["hostvars"]
        assert group and hostvars
    except (KeyError, AssertionError):
        raise AnsibleFilterTypeError("Validate input for keydb_inventory!")

    for member in group:
        host_name = member
        host_address = hostvars[host_name]["ansible_default_ipv4"]["address"]
        host_role = hostvars[host_name]["keydb_role"]

        result.append(
            {
                "hostname": host_name,
                "address": host_address,
                "role": host_role,
            }
        )

    return result


class FilterModule(object):
    """Ansible core jinja2 filters"""

    def filters(self):
        return {
            "keydb_inventory": keydb_inventory,
            "keydb_select": keydb_select,
        }

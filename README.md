Ansible Role: KeyDB Fullmesh
=========
Install and configure KeyDB Active Replication cluster with fullmesh arch.
It's also support replica nodes that connect to all master nodes. So they form nodes separate from write topolgy.
Masters on the other hand interconnect only with masters.

The role creation was inspired by [v0112358/ansible-role-keydb-active-replication](https://github.com/v0112358/ansible-role-keydb-active-replication).

Example Inventory
------------
```
---
keydb:
  hosts:
    keydb01:
      keydb_role: master
    keydb02:
      keydb_role: master
    keydb03:
      keydb_role: replica
      keydb_appendonly: 'no'
      keydb_version: 6.3.3
      keydb_config_replica_read_only: true
  vars:
    keydb_tls_enabled: true
    keydb_target:  "keydb03"
    keydb_restart_on_changes: false
    keydb_version: 6.3.4
    keydb_config_unix_socket: "/var/run/keydb/keydb.sock"
    keydb_config_requirepass: "root"
    keydb_config_maxmemory: "128mb"
    keydb_config_maxmemory_policy: "noeviction"
    keydb_config_users:
        - name: reader
          password: "reader"
          permissions: "+@read ~*"
```
Important Variabes
------------
```
keydb_target: You can exactly specify host a play should run against. Default "all" means all hosts in group.
keydb_group_name: Specify group of hosts. It's used by grouping hosts params for interconnecting.
keydb_tls_enabled: if true configure connections within cluster over TLS. Certs are not managed by this role!
keydb_node_selector: 'ip' or 'hostname'(default). It's used to determine whether interconnect hosts in a cluster by ip or by hostname(replicaof parameter).
keydb_role: 'master' or 'replica'. Replica connects to all masters while masters to replicas - doesn't. For now it MUST be specified in ansible vars hierarchy :(
```
Many variables are defined in `defaults/main.yml`.
Also take a look at `templates/etc/keydb/keydb.conf.j2` for full list of keydb parameters.

License
-------
MIT

Author Information
------------------
[iganosaigo](https://github.com/iganosaigo)

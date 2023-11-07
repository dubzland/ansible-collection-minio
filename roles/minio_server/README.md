# Ansible Role: Minio Server

Installs and applies base configuration to a Minio Object Storage Server.

## Role Variables

```yaml
minio_server_storage_dir: /srv/minio
```

Root directory for Minio object storage.

```yaml
minio_server_admin_username: minioadmin
minio_server_admin_password: minioadmin
```

Username and password for administrative authentication to the Minio server.

## Usage

Install the collection locally, either via `requirements.yml`, or manually:
```bash
ansible-galaxy collection install dubzland.minio
```

Then apply the server role using the following playbook:
```yaml
---
- hosts: minio-servers

  collections:
    - dubzland.minio

  roles:
    - minio_server
```
## License

MIT

## Author

* [Josh Williams](https://codingprime.com)

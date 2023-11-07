# Ansible Role: Minio Client

Installs the Minio Object Storage command line client.

## Role Variables

None

## Usage

Install the collection locally, either via `requirements.yml`, or manually:
```bash
ansible-galaxy collection install dubzland.minio
```

Then apply the server role using the following playbook:
```yaml
---
- hosts: minio-clients

  collections:
    - dubzland.minio

  roles:
    - minio_client
```
## License

MIT

## Author

* [Josh Williams](https://codingprime.com)

# Ansible Collection: Minio
[![Gitlab pipeline status (self-hosted)](https://git.dubzland.net/dubzland/ansible-collection-minio/badges/main/pipeline.svg)](https://git.dubzland.net/dubzland/ansible-collection-minio/pipelines?scope=all&page=1&ref=main)
[![Ansible Galaxy](https://img.shields.io/badge/dynamic/json?style=flat&label=galaxy&prefix=v&url=https://galaxy.ansible.com/api/v3/collections/dubzland/minio/&query=highest_version.version)](https://galaxy.ansible.com/ui/repo/published/dubzland/minio/)
[![Liberapay patrons](https://img.shields.io/liberapay/patrons/jdubz)](https://liberapay.com/jdubz/donate)
[![Liberapay receiving](https://img.shields.io/liberapay/receives/jdubz)](https://liberapay.com/jdubz/donate)

Collection of roles and modules for interacting with the Minio Object Storage
Server.

## Ansible version compatibility

This collection has been tested against following ansible-core versions:

- 2.13
- 2.14
- 2.15
- 2.16

Also tested against the current development version of `ansible-core`.

## Included content

### Roles
Name | Description
--- | ---
`dubzland.minio.minio_server`|Install and configure a Minio server
`dubzland.minio.minio_client`|Install and configure the Minio client (mc)

### Modules
Name | Description
--- | ---
`dubzland.minio.minio_alias`|Manages Minio aliases


## Licensing

This collection is primarily licensed and distributed as a whole under the GNU General Public License v3.0 or later.

See [LICENSE](https://git.dubzland.net/dubzland/ansible-collection-minio/blob/main/LICENSE) for the full text.

All files have a machine readable `SDPX-License-Identifier:` comment denoting its respective license(s) or an equivalent entry in an accompanying `.license` file. Only changelog fragments (which will not be part of a release) are covered by a blanket statement in `.reuse/dep5`. This conforms to the [REUSE specification](https://reuse.software/spec/).

## Author

* [Josh Williams](https://codingprime.com)

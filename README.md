# Ansible Collection: Minio

[![Gitlab pipeline][pipeline-badge]][pipeline-url]
[![Gitlab coverage][coverage-badge]][coverage-url]
[![Galaxy Version][galaxy-badge]][galaxy-url]
[![license][license-badge]][license-url]
[![Liberapay patrons][liberapay-patrons-badge]][liberapay-url]
[![Liberapay receiving][liberapay-receives-badge]][liberapay-url]

Collection of roles and modules for interacting with the Minio Object Storage
Server.

## Ansible version compatibility

This collection has been tested against following ansible-core versions:

- 2.14
- 2.15
- 2.16

Also tested against the current development version of `ansible-core`.

## Included content

### Roles

| Name                                        | Description                                 |
| ------------------------------------------- | ------------------------------------------- |
| [dubzland.minio.minio_client][minio_client] | Install and configure the Minio client (mc) |
| [dubzland.minio.minio_server][minio_server] | Install and configure a Minio server        |

### Modules

| Name                                        | Description            |
| ------------------------------------------- | ---------------------- |
| [dubzland.minio.minio_alias][minio_alias]   | Manages Minio aliases  |
| [dubzland.minio.minio_bucket][minio_bucket] | Manages Minio buckets  |
| [dubzland.minio.minio_policy][minio_policy] | Manages Minio policies |
| [dubzland.minio.minio_user][minio_user]     | Manages Minio users    |

## Licensing

This collection is primarily licensed and distributed as a whole under the MIT license.

See [LICENSES/MIT.txt](LICENSES/MIT.txt) for the full text.

Parts of the collection are licensed under the
[GNU General Public License v3.0 or later](LICENSES/GPL-3.0-or-later.txt).

## Author

- [Josh Williams](https://codingprime.com)

[pipeline-badge]: https://img.shields.io/gitlab/pipeline-status/dubzland%2Fansible-collections%2Fminio?gitlab_url=https%3A%2F%2Fgit.dubzland.com&branch=main&style=flat-square&logo=gitlab
[pipeline-url]: https://git.dubzland.com/dubzland/ansible-collections/minio/pipelines?scope=all&page=1&ref=main
[coverage-badge]: https://img.shields.io/gitlab/pipeline-coverage/dubzland%2Fansible-collections%2Fminio?gitlab_url=https%3A%2F%2Fgit.dubzland.com&branch=main&style=flat-square&logo=gitlab
[coverage-url]: https://git.dubzland.com/dubzland/ansible-collections/minio/pipelines?scope=all&page=1&ref=main

[galaxy-badge]: https://img.shields.io/badge/dynamic/json?style=flat-square&label=galaxy&logo=ansible&prefix=v&url=https://galaxy.ansible.com/api/v3/collections/dubzland/minio/&query=highest_version.version
[galaxy-url]: https://galaxy.ansible.com/ui/repo/published/dubzland/minio/
[license-badge]: https://img.shields.io/gitlab/license/dubzland%2Fcontainer-images%2Fci-python?gitlab_url=https%3A%2F%2Fgit.dubzland.com&style=flat-square
[license-url]: https://git.dubzland.com/dubzland/container-images/ci-python/-/blob/main/LICENSE
[liberapay-patrons-badge]: https://img.shields.io/liberapay/patrons/jdubz?style=flat-square&logo=liberapay
[liberapay-receives-badge]: https://img.shields.io/liberapay/receives/jdubz?style=flat-square&logo=liberapay
[liberapay-url]: https://liberapay.com/jdubz/donate

[minio_client]: https://docs.dubzland.io/ansible-collections/collections/dubzland/minio/minio_client_role.html
[minio_server]: https://docs.dubzland.io/ansible-collections/collections/dubzland/minio/minio_server_role.html
[minio_alias]: https://docs.dubzland.io/ansible-collections/collections/dubzland/minio/minio_alias_module.html
[minio_bucket]: https://docs.dubzland.io/ansible-collections/collections/dubzland/minio/minio_bucket_module.html
[minio_policy]: https://docs.dubzland.io/ansible-collections/collections/dubzland/minio/minio_policy_module.html
[minio_user]: https://docs.dubzland.io/ansible-collections/collections/dubzland/minio/minio_user_module.html

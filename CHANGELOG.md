# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2023-11-29

### Added

- Ansible module `minio_bucket` for managing Buckets (#3)
- Ansible module `minio_user` for managing Users (#2)

### Changed

- Extracted common minio client logic into a module_util

## [0.0.2] - 2023-11-25

### Added

- Ansible module `minio_alias` for managing `mc` aliases (#1)
- Ansible module `minio_policy` for managing Policies (#4)

### Changed

- Refactored testing to fall more in line with a standard collection. (#6)

## [0.0.1] - 2023-11-15

### Added

- Minio Client and Server role

[1.0.0]: https://git.dubzland.com/dubzland/ansible-collection-minio/-/compare/0.0.2...1.0.0
[0.0.2]: https://git.dubzland.com/dubzland/ansible-collection-minio/-/compare/0.0.1...0.0.2
[0.0.1]: https://git.dubzland.com/dubzland/ansible-collection-minio/-/tree/0.0.1

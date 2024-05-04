# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Move repository to dubzland/ansible-collections/minio (#17)

## [1.1.0] - 2024-04-27

### Changed

- Authentication for modules is now an `auth` dict with suboptions (#12)
- CI is now controlled by external, common templates (#11)
- `minio_policy` now accepts a list of structured statements instead of a free-form document (#5)

## [1.0.1] - 2023-12-03

### Added

- Minio server url can now be specified (#8)
- Minio options can be specified to allow setting the listen port

### Changed

- Updated documentation examples to match access_key -> minio_access_key (#7)

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

[unreleased]: https://git.dubzland.com/dubzland/ansible-collections/minio/-/compare/1.0.1...HEAD
[1.1.0]: https://git.dubzland.com/dubzland/ansible-collections/minio/-/compare/1.0.1...1.1.0
[1.0.1]: https://git.dubzland.com/dubzland/ansible-collections/minio/-/compare/1.0.0...1.0.1
[1.0.0]: https://git.dubzland.com/dubzland/ansible-collections/minio/-/compare/0.0.2...1.0.0
[0.0.2]: https://git.dubzland.com/dubzland/ansible-collections/minio/-/compare/0.0.1...0.0.2
[0.0.1]: https://git.dubzland.com/dubzland/ansible-collections/minio/-/tree/0.0.1

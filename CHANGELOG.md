# Changelog

## [Unreleased][]

[Unreleased]: https://github.com/chaostoolkit-incubator/chaostoolkit-humio/compare/0.5.1...HEAD

## [0.5.1][] - 2020-10-03

[0.5.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-humio/compare/0.5.0...0.5.1

### Changed

-   Updated README with `search_query` probe information

## [0.5.0][] - 2020-10-03

[0.5.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-humio/compare/0.4.2...0.5.0

### Added

- A `search_query` probe to perform queries against the
  [Humio search API][searchapi]
- Basic tolerances to validate number values returned by the search probe

[searchapi]: https://docs.humio.com/api/using-the-search-api-with-humio/#query

## [0.4.2][] - 2020-01-15

[0.4.2]: https://github.com/chaostoolkit-incubator/chaostoolkit-humio/compare/0.4.1...0.4.2

### Added

- More testing for secrets and configuration

### Fixed

- Passing of configuration through control to enable custom Humio URL domain

## [0.4.1][] - 2020-01-13

[0.4.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-humio/compare/0.4.0...0.4.1

### Fixed

-   `dataspace` being checked by control on configuration
-   URL incorrect for Humio API

## [0.4.0][] - 2020-01-13

[0.4.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-humio/compare/0.3.0...0.4.0

### Added

-   Overriding of the Humio URL domain to support on-premise deployments of Humio.

### Removed

-   The need to specify the `dataspace`

## [0.3.0][] - 2018-05-12

[0.3.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-humio/compare/0.2.0...0.3.0

### Changed

-   Fix secrets loading

### Added

-   Add more metadata to control event


## [0.2.0][] - 2018-04-12

[0.2.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-humio/compare/0.1.1...0.2.0

### Added

-   Add control support as per [specification][spec]

[spec]: https://docs.chaostoolkit.org/reference/api/experiment/#controls

## [0.1.1][] - 2017-05-14

[0.1.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-humio/compare/0.1.0...0.1.1

### Added

-   MANIFEST.in so that non-source code files are included in source distribution package

## [0.1.0][]

[0.1.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-humio/tree/0.1.0

### Added

-   Initial release
# bpr-uml-shared

Shared code for [socket server](https://github.com/AronGreen/bpr-uml-socket-server) and [rest server](https://github.com/AronGreen/bpr-uml-rest-server)

## Installation

Use pip as normal:

`pip install git+https://github.com/AronGreen/bpr-uml-shared.git#egg=bpr-uml-shared`

when updating the package, just uninstall it first:

`pip uninstall bpr-uml-shared`

## Development

When making any changes to this package, please bump the version number in `setup.cfg`

```
version = old_version+1
```

## Dependencies

Adding dependencies to this package is easy, just add a new line in `setup.cfg` under `install_requires`

```
install_requires =
    pymongo
    your_new_dependency
```


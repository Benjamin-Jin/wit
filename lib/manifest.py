#!/usr/bin/env python3

import json
from pathlib import Path


# TODO
# Should this actually be shared between package manifests and workspace descriptions?
# Should we use different datastructures?
class Manifest:
    """
    Common class for the description of package dependencies and a workspace
    """

    def __init__(self, packages):
        self.packages = packages

    def get_package(self, name: str):
        for p in self.packages:
            if p.name == name:
                return p
        return None

    def contains_package(self, name: str) -> bool:
        return self.get_package(name) is not None

    def add_package(self, package):
        self.packages.append(package)
        return self

    def update_package(self, package) -> None:
        newpkgs = []
        found = False
        for p in self.packages:
            if p.name == package.name:
                newpkgs.append(package)
                found = True
            else:
                newpkgs.append(p)
        assert found, \
            "Trying to update '{}' but it doesn't exist in manifest!".format(package.name)
        self.packages = newpkgs

    def write(self, path):
        contents = [p.manifest() for p in self.packages]
        manifest_json = json.dumps(contents, sort_keys=True, indent=4) + '\n'
        path.write_text(manifest_json)

    # FIXME It's maybe a little weird that we need wsroot but that's because
    # this method is being used for both wit-workspace and wit-manifest in
    # packages
    @staticmethod
    def read_manifest(ws, path, safe=False):
        if safe and not Path(path).exists():
            return Manifest([])
        content = json.loads(path.read_text())
        return Manifest.process_manifest(ws, content)

    @staticmethod
    def process_manifest(ws, json_content):
        # import here to prevent circular dependency
        from lib.dependency import manifest_item_to_dep
        packages = [manifest_item_to_dep(ws, x) for x in json_content]
        return Manifest(packages)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

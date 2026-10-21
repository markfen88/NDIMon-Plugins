# Building and releasing plugins

Release operations are manual and attended. Do not configure an automatic push
or mirror to the owner's public GitHub repositories.

## Runtime first

Build the exact Tessera release natively on each supported OS/architecture.
Use the upstream add-on bundle builder with explicit package revision and source
commit. It must contain the daemon, ALSA backend, install/remove scripts,
manifest/checksums and integration contract. A cross-built binary is not a
native OS bundle. No build operation should silently install it on a live appliance.

## Pin and assemble

```sh
python3 scripts/pin-bundle.py /path/to/tessera-bundle_<version>_<arch>.tar.gz
python3 scripts/build-plugin.py --plugin tessera --bundle /path/to/tessera-bundle_<version>_<arch>.tar.gz
```

Commit the reviewed lock and compatibility metadata. The builder writes the host
archive, generated catalog-entry JSON and merged SHA256SUMS under `dist/`.
Transport filenames replace `~` with `-` for GitHub; manifest/catalog versions
retain Debian ordering. Use static catalogs with explicit versions. If downloading
a public runtime bundle to rebuild a plugin, save it under the native filename
recorded by `bundles.lock.json` (`~beta`); the public asset alias uses `-beta`.
This rename changes no archive bytes or embedded identity. Archives place plugin.json directly at their root. The embedded runtime identity
and checksum are also written inside each plugin archive for root-hook verification.

The current human release tag is `tessera-v0.2.0-beta`; the host manifest uses
Debian-ordered `0.2.0~beta1`. The builder accepts `--release-tag` for a later release.
Increment the manifest/compatibility version for changed plugin source or a new
runtime bundle; do not replace an installed version's contents silently.

## Publish

After an explicit owner publication instruction, create the GitHub prerelease
and upload actual archives plus SHA256SUMS. Update platform catalogs only after
their assets are downloadable and their bytes match their entries. Do not add an
unbuilt platform or advertise a planned runtime as available. Keep release notes
clear about OS support, restarts, rollback and experimental limitations.

For other plugins, start from `plugins/example/`, provide a valid manifest and
assemble with `--plugin <name>`. The host framework is documented in
[plugin authoring](plugin-authoring.md). Runtime-specific privileged hooks must
stay narrow, fixed-argument and declared in the manifest; plugins are trusted code.

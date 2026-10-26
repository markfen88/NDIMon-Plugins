# Building and releasing plugins

Release operations are manual and attended. Do not configure an automatic push
or mirror to the owner's public GitHub repositories.

## Runtime first

Build the exact Tessera release natively on each supported OS/architecture with
`cargo xtask build-bundle` from the matching [Tessera](https://github.com/markfen88/Tessera)
source commit (`--allow-ubuntu-24.04` on Ubuntu 24.04 arm64). The bundle must contain
the daemon, ALSA backend, the `tessera-bundle` installer, manifest/checksums and
integration contract. A cross-built binary is not a native OS bundle. No build
operation should silently install it on a live appliance.

## Pin and assemble

Review and commit the pin by hand: add the bundle's version, architecture, OS,
public source commit, asset name and SHA256 to `bundles.lock.json`, and update
`compatibility.json` and `plugins/tessera/plugin.json` (`version`, `min_ndimon`)
together. Then, from an NDIMon-R checkout of the matching release (copy the same
files into it first):

```sh
cd control
cargo xtask build-plugin tessera --bundle /path/to/tessera-bundle_<version>_amd64.tar.gz --output /clean/output/dir --release-tag tessera-v<version>
cargo xtask build-plugin tessera --bundle /path/to/tessera-bundle_<version>_arm64.tar.gz --output /clean/output/dir --release-tag tessera-v<version>
# Ubuntu 24.04 arm64 (experimental): same archive name as the Debian arm64 one, so
# its own output directory and release tag
cargo xtask build-plugin tessera --ubuntu-experimental-bundle /path/to/tessera-bundle_<version>_arm64_ubuntu-noble-experimental.tar.gz --output /clean/ubuntu/dir --release-tag tessera-v<version>-ubuntu-24.04
```

Keep the bundle under the filename recorded by `bundles.lock.json`. The builder
checks the bundle against the pin and the compatibility record, and writes the
plugin archive `tessera-plugin_<version>_<arch>.tar.gz`, a catalog entry
`<archive>.json` and a merged `SHA256SUMS` into the output directory. Use a clean
output directory for each release: `SHA256SUMS` covers every plugin archive in it.
The bundle of each platform is built natively on that platform; packaging it into the
plugin archive needs no such host.
A `~` in a manifest version becomes `-` in the file name. Builds are deterministic
for the same inputs (`SOURCE_DATE_EPOCH` defaults to 0).

The current human release tags are `tessera-v0.3.0` (Debian 13) and
`tessera-v0.3.0-ubuntu-24.04`; the host manifest uses
`0.3.0`. Increment the manifest and compatibility version for changed plugin
source or a new runtime bundle; do not replace an installed version's contents
silently.

## Publish

After an explicit owner publication instruction, create the GitHub release and
upload the actual archives plus `SHA256SUMS`. Update the platform catalogs in
`catalogs/` only after their assets are downloadable and their bytes match their
entries: each catalog is `{"schema_version":1,"plugins":[<entry>]}` with the entry
file the builder wrote. Do not add an unbuilt platform or advertise a planned
runtime as available. Keep release notes clear about OS support, restarts,
rollback and experimental limitations.

For other plugins, follow the host framework in
[plugin authoring](plugin-authoring.md): a manifest, an out-of-process executable
and an optional UI fragment. Plugins are trusted code; keep privileged commands
narrow, fixed-argument and declared in the manifest.

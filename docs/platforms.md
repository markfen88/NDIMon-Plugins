# Platforms and catalogs

Use the exact host OS/version/architecture. The following catalogs are separate
because NDIMon-R's feed client filters CPU architecture, not OS:

| Host | Catalog |
|---|---|
| Debian 13 Trixie amd64 | [debian-13-amd64.json](../catalogs/debian-13-amd64.json) |
| Debian 13 Trixie arm64 | [debian-13-arm64.json](../catalogs/debian-13-arm64.json) |
| Ubuntu 24.04 Noble arm64 (experimental) | [ubuntu-24.04-arm64.json](../catalogs/ubuntu-24.04-arm64.json) |

Raw feed base: `https://raw.githubusercontent.com/markfen88/NDIMon-Plugins/main/catalogs/`.
Select one matching catalog. Do not combine OS feeds merely because the CPU matches.
The runtime installer checks both host and bundle OS/architecture and refuses a
mismatch before package installation.

Debian armhf, Ubuntu amd64 and other images have no plugin binary in this
release. Do not substitute another platform's archive. A source build requires
its own native bundle pin and compatibility entry.

Each download archive uses the name `tessera-plugin_0.3.0_<arch>.tar.gz` with
`<arch>` `amd64` or `arm64`. The Debian 13 archives (amd64 and arm64) are assets of
the `tessera-v0.3.0` release together with its `SHA256SUMS` file. The name has no
room for the OS, so the Ubuntu 24.04 arm64 archive, which has the same file name as
the Debian arm64 one, is an asset of its own release, `tessera-v0.3.0-ubuntu-24.04`,
with its own `SHA256SUMS`; its catalog points there. The
manifest, catalog and transport filename all use plugin version `0.3.0`. Use these
static platform catalogs, rather than deriving a version from a GitHub release
asset name. Each catalog entry states the platform, version, byte size, exact
download URL and SHA256. Runtime bundle filenames retain their OS distinction. The
catalog entry is generated from the actual archive; an unavailable asset is not
advertised as installable.

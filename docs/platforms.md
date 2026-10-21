# Platforms and catalogs

Use the exact host OS/version/architecture. The following beta catalogs are
separate because NDIMon's feed client filters CPU architecture, not OS:

| Host | Catalog |
|---|---|
| Debian 13 Trixie amd64 | [debian-13-amd64.json](../catalogs/debian-13-amd64.json) |
| Ubuntu 24.04 Noble arm64 (experimental) | [ubuntu-24.04-arm64.json](../catalogs/ubuntu-24.04-arm64.json) |

Raw feed base: `https://raw.githubusercontent.com/markfen88/NDIMon-Plugins/main/catalogs/`.
Select one matching catalog. Do not combine OS feeds merely because the CPU matches.
The embedded runtime installer checks both host and bundle OS/architecture and
refuses a mismatch before package installation.

Debian arm64/armhf, Ubuntu amd64 and other images have no plugin binary in this
release. Do not substitute another platform's archive. A source build requires
its own native bundle pin and compatibility entry.

Each download archive uses the name
`tessera-plugin_0.2.0-beta1_<arch>.tar.gz`. Download filenames use `-beta`
because GitHub rewrites `~`; the manifest and catalog keep `0.2.0~beta1`.
Use these static platform catalogs, rather than deriving a version from a
GitHub release asset name. Each catalog additionally states
the platform, version, byte size, exact download URL and SHA256. Runtime bundle
filenames retain their OS distinction. The catalog entry is generated from the
actual archive; an unavailable asset is not advertised as installable.

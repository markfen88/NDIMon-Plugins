# NDIMon Plugins

Public plugin sources, installation guides, platform catalogs and precompiled
plugin archives for [NDIMon-R](https://github.com/markfen88/NDIMon-R).
The first integration is **Tessera network audio**. NDIMon 1.3.0 or newer is required.

The Tessera host adapter/UI belongs here. The modular Rust daemon, ALSA backend,
standalone portal and runtime packages belong to
[Tessera](https://github.com/markfen88/Tessera). A plugin archive includes an exact
precompiled Tessera bundle; installation does not compile it on the appliance.
Updating either source repository does not automatically alter an installed device.

[Install/configure Tessera](docs/tessera.md) · [Platforms](docs/platforms.md) ·
[Compatibility](docs/compatibility.md) · [Author plugins](docs/plugin-authoring.md) ·
[Build/release](docs/releases.md)

## Current beta

| Item | Version |
|---|---|
| Tessera source release | 0.2.0-beta |
| Tessera native runtime packages | 0.2.0~beta-1 |
| Tessera host plugin | 0.2.0~beta1 |
| Minimum NDIMon | 1.3.0 |
| Local Tessera control protocol | 1 |

Tildes give correct Debian version ordering: beta packages/plugins sort before
an eventual final release. The source tag uses the human-facing beta name.

Published platforms are listed in [platforms](docs/platforms.md) and
`bundles.lock.json`. Choose the complete OS/version/architecture combination,
not architecture alone. The NDIMon feed client filters architecture, not OS;
use the matching platform catalog. Ubuntu support remains experimental.

## Install an archive

1. Download the archive for your host and its trusted release `SHA256SUMS`.
2. Verify the checksum before upload. A checksum protects integrity, not the
   identity of an untrusted publisher. Plugin hooks are privileged code.
3. Open **NDIMon → Plugins**, enter `tessera`, choose the archive and select
   **Upload and install**. The API briefly restarts; its requested enable runs
   on the next API startup.
4. Open the Tessera tab for device/clock/flow/channel-name configuration.
5. Open **Outputs → an output → Advanced → Audio** for inputs, destinations,
   gains and delays. Saving choices does not select audio v2. Activate v2
   explicitly and confirm its decoder restart.

A new plugin installation does not change the selected NDI source. Installing
the plugin and activating experimental audio are separate operations.

## Install/update from a catalog

Catalogs are ordinary HTTPS JSON files supported by NDIMon 1.3.0. Select the
platform-specific URL in [platforms](docs/platforms.md). From the NDIMon checkout:

```sh
sudo bash install.sh --plugin-feed https://raw.githubusercontent.com/markfen88/NDIMon-Plugins/main/catalogs/ubuntu-24.04-arm64.json --with-plugin tessera
```

That example is for **Ubuntu 24.04 arm64 only**. The core installer also rebuilds
NDIMon; use the web upload flow when a core reinstall is not intended. Feed URLs
are stored in `plugin_feeds` in device settings; an empty list means upload-only.
Use Plugins → Update for newer matching plugin versions. Back up settings first.

## Routing and networks

- Receive NDI and/or Tessera audio and select multiple destinations per output,
  including HDMI plus Tessera together.
- Inputs have gain and delay; destinations have independent delay. Disabled
  outputs retain saved selections. Delays are manual, not measured lip-sync.
- Define VLANs/management in NDIMon Settings → Network, select the shared NDI
  network on NDI, and select Tessera's network inside the plugin. These are one
  recoverable host network transaction. The plugin does not create a second
  management plane.
- Match 48 kHz, channels, encoding, static flow direction/peer/port and clock
  configuration. Device latency uses microseconds; output routing delay uses ms.

## Compatibility and upgrades

`plugin.json` declares `min_ndimon`. `compatibility.json` records the plugin,
runtime and control API; `bundles.lock.json` pins each native archive by SHA256
and public source commit. The builder refuses a changed declared runtime or
control protocol until the compatibility record is updated.

The current host enforces a minimum version, not every exact tested-build
combination. It has no automatic untested-build warning matrix. The exact-build
list starts empty; packaging/control checks do not certify external hardware.

Updating the runtime requires a new reviewed bundle pin and plugin release.
Disable returns to the legacy audio path; ordinary removal preserves settings.
Purge can remove Tessera configuration, so export a backup before using it.
See [upgrade/removal details](docs/tessera.md).

## Limits

This is beta software. External Dante hardware audio, sustained clock behavior,
hardware PTP and automatic HDMI/Dante latency matching are not certified.
Vendor-controller subscriptions, Bluetooth calibration and HDMI ARC/eARC are
not implemented. Per-output NDI transport/HX/tally/network isolation remain
outside this plugin. Full-device/mono endpoints are available; two monos mix
rather than forming a stereo pair.

## Build a plugin

Python 3 and the standard library are sufficient to assemble a pinned archive:

```sh
python3 scripts/pin-bundle.py /path/to/tessera-bundle_<version>_<arch>.tar.gz
python3 scripts/build-plugin.py --plugin tessera --bundle /path/to/tessera-bundle_<version>_<arch>.tar.gz
# Minimal authoring example, without a runtime bundle:
python3 scripts/build-plugin.py --plugin example
```

The runtime bundle must first be built natively from its matching public Tessera
source. Copying a new binary into an old archive breaks its identity. Output goes
to ignored `dist/`, with checksums and catalog-entry metadata. Publishing is an
explicit attended release operation; no automatic GitHub mirror is configured.

## Source layout

| Path | Purpose |
|---|---|
| `plugins/tessera/` | Host routes/UI, client, flows, backup and fixed privileged hooks |
| `plugins/example/` | Minimal author template |
| `compatibility.json` | Declared plugin/runtime/control compatibility |
| `bundles.lock.json` | Exact per-platform runtime pins |
| `catalogs/` | Platform-specific install/update feeds |
| `scripts/` | Explicit pinning/archive assembly |
| `docs/` | Operator and author guides |

NDIMon 1.3.0 contains an older embedded plugin source snapshot. New standalone
plugin releases are maintained here and installed through the host framework;
the core does not automatically synchronize a source checkout.

## License

Host plugin code: MIT — [LICENSE](LICENSE). Embedded Tessera runtimes are MPL-2.0;
their matching source is available in the Tessera release. No vendor runtime is included.

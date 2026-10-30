# NDIMon Plugins

Public plugin sources, installation guides, platform catalogs and precompiled
plugin archives for [NDIMon-R](https://github.com/markfen88/NDIMon-R).
The first integration is **Tessera network audio**. NDIMon-R 1.4.0 or newer is required.

The Tessera host manifest and UI fragment belong here. The modular Rust daemon,
ALSA backend, standalone portal and runtime packages belong to
[Tessera](https://github.com/markfen88/Tessera). The control-plane domain that
configures Tessera (state, rendering and the privileged lifecycle) is part of
NDIMon-R. A plugin archive includes an exact precompiled Tessera bundle;
installation does not compile it on the appliance. Updating either source
repository does not automatically alter an installed device.

[Install/configure Tessera](docs/tessera.md) · [Platforms](docs/platforms.md) ·
[Compatibility](docs/compatibility.md) · [Author plugins](docs/plugin-authoring.md) ·
[Build/release](docs/releases.md)

## Current release

| Item | Version |
|---|---|
| Tessera source release | 0.5.2 |
| Tessera native runtime bundle | 0.5.2-1 |
| Tessera host plugin | 0.5.2 |
| Minimum NDIMon-R | 1.4.0 |
| Local Tessera control protocol | 1 |

The plugin is released independently of NDIMon-R. The runtime bundle is pinned by
exact source commit and checksum in [`bundles.lock.json`](bundles.lock.json), and
[`compatibility.json`](compatibility.json) records the feature and API assumptions.

Published platforms are listed in [platforms](docs/platforms.md). Choose the
complete OS/version/architecture combination, not architecture alone. The NDIMon-R
feed client filters architecture, not OS; use the matching platform catalog.
Ubuntu support remains experimental.

## Install an archive

1. Download the archive for your host and the release's `SHA256SUMS`.
2. Verify the checksum before upload. A checksum protects integrity, not the
   identity of an untrusted publisher. The runtime bundle is installed by
   privileged code on the device.
3. Open **NDIMon-R → Plugins**, enter `tessera`, choose the archive and select
   **Upload and install**. Before anything on the device changes, the privileged
   daemon checks the embedded runtime bundle against its pin.
4. Open the Tessera tab for device, clock, flow and channel-name configuration.
5. Open **Outputs → an output → Advanced → Audio** for inputs, destinations,
   gains and delays. Saving an output's routes selects audio engine v2 in the same
   change; when v1 is running the page shows the decoder restart and asks first.

A new plugin installation does not change the selected NDI source. The installer
does not restart a running `tesserad`: restart it from the plugin (this interrupts
network audio) or reboot to run a newly installed runtime.

## Install/update from a catalog or release feed

NDIMon-R reads two feed formats from the `plugin_feeds` list in its device
settings (up to 32 URLs, set with the `set_device` command; with no feed the
Plugins page is upload-only):

- a static platform catalog from this repository, for example
  `https://raw.githubusercontent.com/markfen88/NDIMon-Plugins/main/catalogs/debian-13-amd64.json`
- the GitHub release listing
  `https://api.github.com/repos/markfen88/NDIMon-Plugins/releases?limit=5`

Use **one** matching catalog. The release listing filters by CPU architecture and
does not know the OS, so use it only where the architecture identifies the platform.
On arm64 that is not the case (Debian 13 and Ubuntu 24.04 both have an archive), so an
arm64 device must use its platform catalog.
The feed command and its authentication are described in
[plugin authoring](docs/plugin-authoring.md#feeds). Use Plugins → Update for newer
matching versions, and back up settings first.

## Routing and networks

- Receive NDI and/or Tessera audio and select multiple destinations per output,
  including HDMI plus Tessera together.
- Inputs have gain and delay; destinations have independent delay. Disabled
  outputs retain saved selections. Delays are manual, not measured lip-sync.
- Define VLANs and management in NDIMon-R Settings → Network, select the shared NDI
  network on NDI, and select Tessera's network inside the plugin. These are one
  recoverable host network transaction. The plugin does not create a second
  management plane.
- Match 48 kHz, channels, encoding, static flow direction/peer/port and clock
  configuration. Device latency uses microseconds; output routing delay uses ms.

## Compatibility and upgrades

`plugin.json` declares `min_ndimon`. `compatibility.json` records the plugin,
runtime and control API; `bundles.lock.json` pins each native archive by SHA256
and public source commit. The plugin builder refuses a changed declared runtime or
control protocol until the compatibility record is updated.

The host enforces a minimum version, not every exact tested-build combination. The
exact-build list starts empty; packaging and control checks do not certify
external hardware.

Plugin archives for Tessera 0.2.x cannot be installed on NDIMon-R 1.4.0 and the
0.2.x runtime bundles are refused: the device requires the runtime's own
`tessera-bundle` installer, which Tessera 0.3.0 introduced. Updating the runtime
requires a new reviewed bundle pin and plugin release. Disable returns to the
legacy audio path; ordinary removal preserves settings. Purge can remove Tessera
configuration, so export a backup before using it.
See [upgrade/removal details](docs/tessera.md).

## Limits

This is beta software. External Dante hardware audio, sustained clock behavior,
hardware PTP and automatic HDMI/Dante latency matching are not certified.
Vendor-controller subscriptions, Bluetooth calibration and HDMI ARC/eARC are
not implemented. Per-output NDI transport/HX/tally/network isolation remain
outside this plugin. Full-device/mono endpoints are available; two monos mix
rather than forming a stereo pair.

## Build a plugin

Plugin archives are assembled with `cargo xtask build-plugin` from an NDIMon-R
checkout; this repository holds the plugin sources, the pins and the published
catalogs. See [Building and releasing](docs/releases.md).

## Source layout

| Path | Purpose |
|---|---|
| `plugins/tessera/` | The Tessera manifest and UI fragment |
| `compatibility.json` | Declared plugin/runtime/control compatibility |
| `bundles.lock.json` | Exact per-platform runtime pins |
| `catalogs/` | Platform-specific install/update feeds |
| `docs/` | Operator and author guides |

The NDIMon-R packages carry a copy of the Tessera manifest and fragment for a
device that has accepted Tessera; new standalone plugin releases are maintained
here and installed through the host framework. The core does not automatically
synchronize a source checkout.

## License

Host plugin code: MIT — [LICENSE](LICENSE). Embedded Tessera runtimes are MPL-2.0;
their matching source is available in the Tessera release. No vendor runtime is included.

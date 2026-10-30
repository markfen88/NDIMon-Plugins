# Plugin releases

## Tessera 0.5.2

- Pin the Tessera 0.5.2 runtime (packages `0.5.2-1`, built, signed and published
  in public from Tessera's `v0.5.2` tag). The control wire version (1) and the
  bundle installer's integration contract are unchanged since 0.3.0; the archive
  layout is the same.
- **Upgrade every Tessera device on the network to 0.5.2 together.** Tessera 0.5
  changed the PTPv1 media clock: stratum 0x2A to 0x2D instead of 4 (hardware
  leaders keep precedence), Sync every 250 ms instead of every second, DSCP 46
  instead of 8 for general messages. A 0.3.x device wins every election against
  0.5.x devices, so a network that mixes them is not supported. Update switch QoS
  rules that match DSCP 8.
- Update NDIMon-R to 1.4.1 first: its plugin install restarts `tesserad` on the new
  runtime and refuses a `follower` with a Preferred Leader priority (below 64),
  which Tessera 0.5 refuses too. On NDIMon-R 1.4.0, restart `tesserad` from the
  plugin after the update.
- Going back to 0.3.0: Tessera's installer refuses a downgrade; remove the plugin
  without purging, then install the 0.3.0 archive.
- Archives: Debian 13 amd64 and arm64 under `tessera-v0.5.2`, and the experimental
  Ubuntu 24.04 arm64 archive (same file name) under `tessera-v0.5.2-ubuntu-24.04`.

## Tessera 0.3.0

- Pin the native Tessera 0.3.0 runtime (packages `0.3.0-1`). The bundle now carries
  Tessera's own `tessera-bundle` installer, which authenticates the release and
  every payload file before it installs anything; NDIMon-R 1.4.0 requires it and
  refuses the 0.2.x bundles.
- Require NDIMon-R 1.4.0 as the minimum host. The Tessera plugin is a native
  control-plane domain there: the archive carries only `plugin.json`, `ui.html`,
  the bundle and its lock files, with no JavaScript, shell or Python. The
  privileged daemon verifies the bundle against its pin, runs the bundle's own
  installer, and keeps the Tessera flows under NDIMon-R's control
  (`[control] locked = ["flows"]`).
- Replace the Python tooling of this repository with `cargo xtask build-plugin`
  from NDIMon-R, and drop the JavaScript plugin sources and the author example
  of the 0.2.x line, which NDIMon-R 1.4.0 no longer runs. Plugin authors target
  the out-of-process format described in [plugin authoring](docs/plugin-authoring.md).
- Publish plugin archives as `tessera-plugin_0.3.0_<arch>.tar.gz` with a
  `SHA256SUMS` file: Debian 13 amd64 and the new Debian 13 arm64 under the
  `tessera-v0.3.0` release, and the experimental Ubuntu 24.04 arm64 archive, which
  has the same file name, under `tessera-v0.3.0-ubuntu-24.04`. Add the
  `debian-13-arm64.json` catalog and refresh the other two.
- Upgrade note: after installing the new archive, restart `tesserad` from the
  plugin or reboot so that the daemon and the local audio clients run the same
  release. Audio is interrupted. External hardware audio and sustained clock
  behavior remain experimental.

## Tessera 0.2.1

- Pin the native Tessera 0.2.1 runtime with Controller compatibility and device
  discovery enabled by default, portal Services visible, and initial password
  `tessera` on fresh installs. Existing passwords are preserved.
- Include the NTP-independent media clock and local clock overlay layout 2.0.
  Upgrade and restart the daemon and local audio clients together.
- Keep NDIMon 1.3.0 as the minimum host; no NDIMon host update is required.
- The existing Controller runtime covers the first logical device. External
  hardware audio and sustained clock behavior remain experimental.

## Tessera 0.2.0~beta1

- First separate public Tessera host-plugin release, for NDIMon 1.3.0 or newer.
- Contains the host adapter, settings UI, flows, endpoint discovery, backup and
  fixed lifecycle hooks with a pinned Tessera 0.2.0-beta runtime bundle.
- Native Debian 13 amd64 and experimental Ubuntu 24.04 arm64 archives have
  separate platform feeds; the installer enforces the runtime's OS boundary.
- Declares minimum host, control protocol and feature compatibility alongside
  exact runtime commit/checksum pins. Archive assembly checks those records.
- Provides installation/routing/VLAN/upgrade guides and a minimal authoring
  example with plugin framework documentation.

Existing NDIMon 1.3.0 output audio controls provide multi-input mixing, HDMI and
Tessera destinations, independent delays and deliberate selection of the
experimental audio engine. This release packages that integration independently.
External hardware audio and long-term clock behavior remain experimental;
automatic vendor-controller routing and latency calibration are unavailable.

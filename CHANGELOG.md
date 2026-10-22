# Plugin releases

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

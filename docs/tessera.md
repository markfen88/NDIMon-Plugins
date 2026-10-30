# Tessera network audio

Install and enable the Tessera plugin in **Plugins**, then select its network
audio tab. Plugin enablement makes the settings page available. It does not by
itself select experimental audio engine v2. The route editor is **Outputs → an
output → Advanced → Audio**; device, clock, flow and channel-name configuration
stays in the plugin. Saving an output's routes selects v2 in the same change: when
v1 is running, the device reports the impact (a decoder restart that can pause
video briefly) and the page asks first. **Enable network audio** does the same for
the legacy primary routes; **Disable network audio** and **Return to audio
engine v1…** go back to v1 and keep the saved choices.

The complete host guide — requirements, ownership, handoff from a standalone
Tessera install, page routes and limits — is
[Tessera network audio](https://github.com/markfen88/NDIMon-R/blob/main/docs/plugins/tessera.md)
in the NDIMon-R documentation.

## Bundle and ownership

The optional plugin contains the host manifest, its settings UI and a precompiled
Tessera runtime bundle. The current plugin is `0.5.2` with runtime `0.5.2`
(`0.5.2-1` packages), requiring NDIMon-R `1.4.0` or newer (1.4.1 recommended). Choose a Debian 13 amd64,
Debian 13 arm64 or experimental Ubuntu 24.04 arm64 archive using the [platform guide](platforms.md).
These archives cannot cross OS boundaries. Install the matching plugin archive
through Plugins. A core update does not automatically download, compile or replace
the Tessera runtime.

Before anything on the device changes, the privileged daemon verifies the runtime
bundle: exactly one `tessera-bundle_*.tar.gz` whose SHA-256 matches the lock, a
runtime manifest that agrees with the lock, one executable `tessera-bundle` in the
bundle, and a supported platform. A refused bundle leaves no plugin files and the
reason is returned to the page. The 0.2.x bundles lack the `tessera-bundle`
installer and are refused.

## Setup and routing

1. Define the required networks under **Settings → Network**. Select the NDI
   role on NDI and Tessera's audio role in its plugin. Network settings shows
   read-only usage; all assignments apply through the same protected
   [network transaction](https://github.com/markfen88/NDIMon-R/blob/main/docs/network-vlans.md).
   NDIMon-R owns OS networking here.
2. Configure the Tessera device at 48 kHz, channel counts, RX/TX channel names,
   clock and matching static flows. Labels support individual save/reset.
3. Open an output's blue **Advanced** control (collapsed by default). Add NDI
   or Tessera inputs and HDMI or Tessera destinations. Select both HDMI and
   Tessera to send that output mix to both. Full-device and named mono ranges
   are offered; two mono selections mix rather than forming a stereo pair.
4. Set input gain/input delay and separate destination delay, then **Save output
   audio**. Every selected input feeds every selected destination. Whole-ms
   delays are 0–5000 each with at most 5000 ms combined per active pair. A
   disabled output retains its selections.
5. Readiness, endpoint errors and runtime timing are available through the
   [audio API](https://github.com/markfen88/NDIMon-R/blob/main/docs/api/output-audio.md).

When NDIMon-R hosts Tessera, configure VLANs through NDIMon-R and select the audio
network inside this plugin. Standalone Tessera networking is separate; moving a
configured standalone device to NDIMon-R uses an explicit ownership handoff
described in the NDIMon-R guide.

The integration uses a 48 kHz audio engine and supports 1–16 device channels per
direction. Stereo is the initial supported configuration; other channel layouts,
sustained clock stability and external hardware interoperability are not certified.

Set the device name, encoding, latency and channel counts in Device. Names may
contain up to 31 UTF-8 bytes. Device latency is in microseconds; input
synchronization delay is separately set in milliseconds. Disruptive device changes
display the daemon's impact information and require confirmation. Clock role and
priority changes occur only when their Save buttons are pressed.

The bundled runtime enables Controller compatibility for the first logical device.
Automatic subscriptions remain unsupported; static flows remain available.
Configure a matching Tessera peer or an externally prepared hardware peer:
direction, peer unicast IPv4 address and UDP port (1024–65535). Every flow uses
every device channel in its direction, so both ends must agree on channel count.
Only one RX flow can occupy those RX channels; multiple TX flows may send them to
different peers. Save flows validates the entire set before applying it.

NDIMon-R keeps the flows under its own control (`[control] locked = ["flows"]`) so
no other writer changes them. A runtime without that support still works, but
NDIMon-R reports a flow ownership conflict.

## Upgrade and removal

- **From NDIMon-R 1.3.x with Tessera 0.2.x.** The installed plugin and runtime stay
  in place and are recognised as the native Tessera plugin; the old JavaScript files
  are no longer used. NDIMon-R reports a flow ownership conflict until you install
  a plugin archive built from Tessera 0.3.0 or later.
- **Updating the runtime.** Update NDIMon-R to 1.4.1 or later first, then install
  the newer plugin archive from Plugins. The update asks before its services
  restart and, on NDIMon-R 1.4.1 or later, restarts `tesserad` on the new runtime;
  on 1.4.0 restart `tesserad` from the plugin (it asks before interrupting audio)
  or reboot. Expect audio to be interrupted; choose a deliberate maintenance window.
- **Tessera 0.5.2: upgrade every Tessera device on the network together.**
  Tessera 0.5 changed the PTPv1 media clock (stratum 0x2A to 0x2D instead of 4,
  Sync every 250 ms instead of every second, general messages DSCP 46 instead of
  8). A 0.3.x device wins every election against 0.5.x devices, so a network that
  mixes them is not supported: upgrade NDIMon-R devices, standalone Tessera hosts
  and speakers in one window, and update switch QoS rules that match DSCP 8. A
  clock priority below 64 makes a Preferred Leader, which a `follower` cannot be.
- **Going back.** Tessera's installer refuses a downgrade: remove the plugin
  without purging, then install the archive of the earlier runtime. On a network
  that went back, every device must go back.
- **Removal.** Disable returns to v1; saved selections remain. Normal removal
  preserves configuration. Purge can remove Tessera configuration and state,
  including flow files. Export a backup before removing or purging a plugin.

Start, stop and restart control only the Tessera daemon. Stop and restart ask
before interrupting network audio. If the daemon goes offline, the status strip
reports it; the rest of the page stays available for diagnostics and recovery.
Download diagnostics exports the backend's status and metrics as JSON.

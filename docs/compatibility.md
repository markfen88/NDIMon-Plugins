# Compatibility contract

The host plugin and Rust runtime are independently versioned products.

- NDIMon minimum: 1.3.0, in the plugin manifest.
- Plugin: 0.2.1.
- Runtime source: 0.2.1; native package: 0.2.1-1.
- Local control protocol: version 1.
- Audio engine: 48 kHz; plugin device channels: 1–16 per direction.
- Static flows and the first-device Controller compatibility runtime are included.
  Automatic subscriptions and lip-sync remain unsupported.
- NDIMon owns OS networking; the standalone Tessera network editor must not
  overwrite a hosted appliance's configuration.

`compatibility.json` is separate from `plugin.json`: the current host rejects
unknown plugin-manifest keys. It records feature/API assumptions and an empty
exact-host-build list. An accepted minimum is not a claim that every later host
build was verified. The host does not yet show an exact-build warning matrix.

`bundles.lock.json` identifies each embedded native archive, OS, architecture,
public source commit and SHA256. `pin-bundle.py` records an explicitly supplied
bundle; it does not fetch or silently select a latest release. `build-plugin.py`
compares the archive to that pin, compares the embedded integration contract's
control version, and checks declared runtime/plugin/host versions. A new runtime
or control API requires an explicit compatibility update before archive assembly.

Source updates do not automatically update appliances. Build the matching
runtime, update its pin and compatibility record, assemble the plugin, publish
its assets/checksums, then update the appropriate platform catalog. External
hardware and sustained audio behavior remain experimental even when these
package/protocol checks pass.

# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.6.x   | ✅        |
| 0.5.x   | ✅        |
| < 0.5   | ❌        |

## Reporting a vulnerability

Email `security@comic-consistency.studio` with:
- Affected version and commit SHA
- Reproduction steps or PoC `.cbz` / project bundle
- Impact assessment

We respond within 72 hours. Please do not open public issues for
vulnerabilities.

## Threat model

The studio loads user-supplied:

- character bibles (YAML/JSON)
- LoRA and embedding checkpoints (`.safetensors`, `.pt`)
- comic project bundles (`.ccstudio` zip)

All three are untrusted. The loader runs in a subprocess with:
- `torch.load(..., weights_only=True)` enforced
- zip path traversal rejected before extraction
- YAML parsed with `safe_load` only
- a 2 GB per-bundle decompression ceiling

Pickle-based `.pt` files are refused by default. Opt-in requires
`CCS_ALLOW_PICKLE=1` and a second confirmation flag.

## Out of scope

- Model output content (that's a prompt/craft issue, not a security issue)
- Local GPU driver bugs
- Third-party backend crashes (report upstream)
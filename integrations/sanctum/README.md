# Sanctum integration

Sanctum federation is an external reporting boundary, not part of ordinary
Custos interpretation.

Use:

```bash
custos sanctum-report --envelope envelope.json --output report.json
```

The command validates the active inquiry first and emits a bounded report with:

- repository and Git commit;
- governing instruction and protocol;
- evidence paths and hashes;
- current findings, inference, uncertainty, and next action;
- explicit non-certification status.

Sanctum receives the report, not Custos's complete corpus or internal history.

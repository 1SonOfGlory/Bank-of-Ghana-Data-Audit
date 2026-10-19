# Bank of Ghana data audit

Utilities for inspecting annual, monthly, and quarterly exports from the Bank of Ghana Data Warehouse. The profiler records series coverage, missing values, units, duplicate identifiers, and non-numeric cells. The audit compares repeated series and selected cross-frequency relationships.

The source data are not bundled. Download exports from https://app.datawarehousepro.com/go/bog/ and retain their release dates and units. Revisions and incompatible definitions can produce differences that are not data errors.

```sh
python inspect_bog.py --annual annual.csv --monthly monthly.csv --quarterly quarterly.csv --output bog_profile.json
python audit_bog.py --profile bog_profile.json
```

Python 3.12 or later is sufficient; the scripts use the standard library. The export format must contain `Mnemonic`, `Parent Mnemonic`, `Name of Series`, `Data Family`, and `Units of Measure`, with nine metadata columns before the dated observations. The audit expects the series identifiers in the original October 2026 exports.

This is a data-inspection utility. It contains no fitted forecasting model and makes no claims about predictive performance or policy effects.

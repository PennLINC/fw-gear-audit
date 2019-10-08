# `fw-gear-audit`
A Python SDK tool for auditing gear run data

Use this tool to fetch data from Flywheel describing which gears have been run within a project and how they were configured. You can also join SeqInfo data to help filter your data by sequences.

```
usage: fw-gear-audit [-h] --project PROJECT [PROJECT ...]
                            [--subject SUBJECT [SUBJECT ...]]
                            [--session SESSION [SESSION ...]] [--verbose]
                            [--dry_run] (--path PATH | --fname FNAME)
                            (--by-runs | --by-sequences)
```

# Example

> Who in my gear_testing project has a T1 scan? Do they all have fMRIPrep run on them?

1. Query
```
fw-gear-audit --project gear_testing --by-runs --fname gear_testing.csv
```

2. Filter

Open gear_testing.csv in your spreadsheet software of choice

- Filter column `series_description` for "t1"
- Filter column `gear_name` for "fmriprep"
- Filter column `run_status` for "complete"

See the [wiki](https://github.com/PennBBL/fw-gear-audit/wiki) for detailed walk through information!

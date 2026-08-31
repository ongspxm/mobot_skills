# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [CalVer](https://calver.org/) in `YYYY.MM.DD` format.

## [Unreleased]

### Added
- `meagent-daily-logging`: added a `run` subcommand for explicit execution and backfill workflow.
- `ponytail`: added on-demand investigation, design, implementation, debugging, and review playbooks plus focused engineering tools.

### Changed
- `push-public`: skill now requires reading the full diff and groups mixed changes into separate commits by concern.
- `meagent-daily-logging`: month file updates now rebuild by date chunks and persist output sorted from oldest to newest.
- `meagent-daily-logging`: daily window filtering now uses local timezone-aware comparisons end-to-end, fixing missed boundary messages.
- Replaced `botbot-reuters` with a compact multi-source `botbot-news` skill and script.

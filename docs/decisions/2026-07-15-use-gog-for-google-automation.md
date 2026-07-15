---
type: adr
title: "Use gog for Google automation"
tags: [automation]
timestamp: 2026-07-15T07:07:35Z
---

# Use gog for Google Automation

Status=Accepted

## Context

The Google automation skills use two authentication and API-integration approaches. Gmail owns OAuth authorization, refresh-token storage, and direct Google API calls. Calendar and Tasks use gog, which owns those concerns. The split creates incompatible configuration, repeated credential setup, and separate maintenance paths for the same Google account and APIs.

## Decision

Standardize Google automation skills on gog. gog is the boundary for Google OAuth clients, account selection, token storage, token refresh, scope consent, and Google API calls. Skills retain only their task-specific behavior, such as transforming command output and applying their domain rules.

Do not introduce a shared in-repository Google OAuth client or API wrapper. That would duplicate gog's responsibility and create another credential and compatibility surface.

## Consequences

Good:

- Gmail, Calendar, and Tasks share one authentication model and setup path.
- Google OAuth and API behavior is maintained in one external tool.
- Skills become smaller and focus on their user-facing task behavior.

Cost:

- gog becomes a required runtime dependency and its supported command and JSON-output contract must remain compatible.
- Existing direct Gmail credentials require a one-time gog authorization with the needed Gmail, Calendar, and Tasks scopes.
- Gmail must be migrated without losing its current thread, label, trash, and message-content behavior.

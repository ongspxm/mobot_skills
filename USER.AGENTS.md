## Use compact "smart caveman" style when brevity helps. Keep full accuracy.

Style:
- Cut filler, pleasantries, setup, repeated context.
- Use short words, short sentences, clear fragments.
- Keep technical terms exact.
- Preserve code, commands, paths, config keys, errors.
- Lead: answer -> cause -> fix/next step.
- Do not compress warnings, irreversible actions, or ambiguity-prone steps.

Patterns:
- Problem. Cause. Fix.
- Changed X. Reason Y. Next Z.
- X fails because Y. Do Z.

Examples:

Verbose: I wanted to let you know that your React component appears to be creating a brand new object on every single render. When that happens, React will see that the prop reference has changed, and as a result the child component will end up re-rendering even if the underlying values haven't actually changed. To fix this issue, I'd recommend wrapping the object in `useMemo` so that you only get a new reference when the dependencies actually change.
Compact: New object each render. Child sees new prop ref. Re-render. Wrap object in `useMemo`.

Verbose: A database connection pool is a technique that can help improve the overall performance of your application by maintaining a set of already-open database connections and reusing them across multiple requests, rather than going through the overhead of establishing a brand new connection every time a request comes in.
Compact: db pool reuses open connections. No new connection per request. Less handshake cost. Better under load.

Verbose: It looks like the environment variable that the auth middleware relies on might not be set in your current environment, which would mean that when the middleware tries to validate the incoming token it won't have the secret it needs and authentication will fail.
Compact: missing env var breaks auth middleware. Token validation needs `JWT_SECRET`. Set it before app boot.

Verbose: I'd suggest taking a look at the request payload that's being sent from the client and double-checking that the field names match what the server is expecting, since it's possible the client is sending something like `userEmail` when the API is actually looking for `email`.
Compact: Check request payload. Client may send wrong field name. Server expects `email`, not `userEmail`.

## %% Inline Annotations
- Treat each `%%` line as a direct user instruction.
- Address every `%%` line, then remove it.
- If any `%%` instruction is ambiguous, ask for clarification before editing.

## comment conventions, prefixes (do not remove unless explicitly asked to)
- TODO: clean up is required in the future
- HACKY: temporary fix

## commit msg conventions
- commit msg should be self-explanatory, compact. component name is project specific
- "[fix/feat](component_name) desc" eg "fix(auth) fix login redirect"

## git worktree
- keep all git worktrees in "$REPOROOT/.worktree-branchname"

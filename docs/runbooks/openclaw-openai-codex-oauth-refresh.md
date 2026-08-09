# OpenClaw OpenAI Codex OAuth Refresh

Use this when main OpenClaw chat fails before replying with an error like:

```text
Agent failed before reply: OAuth token refresh failed for openai-codex
Failed to refresh OAuth token for openai-codex. Please try again or re-authenticate.
```

## Scope

This fixes the existing `openai-codex` OAuth profile used by OpenClaw for models such as `openai-codex/gpt-5.4`.

Do not change model routing, add fallback models, reset gateway config, or edit unrelated runtime settings for this error.

## Fix

Run the provider login flow:

```bash
openclaw models auth login --provider openai-codex
```

Open the OAuth URL it prints in a local browser.

After signing in, paste the entire redirect URL back into the terminal prompt, not just the `code` value. The redirect URL looks like:

```text
http://localhost:1455/auth/callback?code=...&scope=openid+profile+email+offline_access&state=...
```

The command should finish with output like:

```text
Updated ~/.openclaw/openclaw.json
Auth profile: openai-codex:default (openai-codex/oauth)
Default model available: openai-codex/gpt-5.4
```

## Verify

Confirm the configured model:

```bash
openclaw models status --plain
```

Then send a minimal main-agent probe:

```bash
openclaw agent --agent main --message "Reply with exactly: OK"
```

Expected output:

```text
OK
```

If the gateway is running, it should dynamically reload the config change. Recent logs may show:

```text
gateway/reload config change detected
gateway/reload config change applied
```

## Gotchas

- `openclaw models auth login` requires an interactive TTY. Piping the redirect URL through stdin does not work.
- The OAuth flow uses a one-time PKCE verifier held by the active login process. If the prompt is cancelled, restart the login flow and use the new OAuth URL.
- Paste the full redirect URL, including `code`, `scope`, and `state`.
- If the terminal prompt treats a pasted URL as blank, restart the login flow and paste into the active TTY prompt again.
- In Codex/unified exec TTY sessions, submitting the redirect URL with a normal newline may echo the URL without accepting it. If the prompt returns to `_` or reports `Required`, resend the full redirect URL terminated with carriage return (`\r`) instead of newline.

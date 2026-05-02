# Backend observability — `Draculin-Backend` on `obs-experiment-embrace`

**TL;DR**: there is none. By design.

## Why

This branch (`obs-experiment-embrace` in BOTH this repo and
[`Draculin-Front`](../../Draculin-Front/)) is the
**Embrace Mobile RUM** PoC. Mobile RUM has a particular mental
model that the other observability PoCs in the portfolio
(LGTM, Honeycomb, Coroot, Elastic) don't surface:

> Most mobile teams don't own the backend they call.

To honour that mental model honestly, the Django backend on
this branch is left **uninstrumented**. Sentry is deleted from:

* `Draculin/settings.py` — both `try/except` blocks at the top
  and the `_sentry_obs.django_session_id_middleware` entry in
  `MIDDLEWARE`.
* `Draculin/_sentry_obs.py` — file deleted entirely.
* `requirements-docker.txt` — `sentry-sdk[django]` line removed.
* `docker-compose.yml` — every `SENTRY_*` env var removed.
* `dracu/views.py` — the `_tag` / `_crumb` / `_span` helpers and
  their no-op fallback shim are removed; call sites stripped.

`grep -ri sentry .` in this repo's working tree on this branch
returns only **two intentional documentation comments** (the
deletion notice in `settings.py` and `docker-compose.yml`).

## What this means in practice

When a Maestro flow exercises the app and a backend endpoint
returns 500, here's what the developer experience looks like
**from the Embrace dashboard alone** (which is the only telemetry
source on this branch):

```
Sessions tab → click affected session
  → Network tab
    → POST /api/chat/  →  status 500  →  duration 132ms  →  payload 41 bytes
  → Logs tab
    → WARN  "chat: server returned non-2xx"  status=500
  → Breadcrumbs
    → "chat: send (len=23)"
    → "chat: send failed (ClientException)"
```

That's it. **No** server stack trace, **no** request body, **no**
Django middleware breadcrumb, **no** ORM query log. The mobile
team's options are:

1. Reproduce locally and look at `runserver` stdout.
2. Ask the backend team to instrument their app.
3. SSH the prod box and `tail -f` the gunicorn logs.

## The convention this branch DOES commit

Even though Sentry is deleted, the
[`DracuHttpClient`](../../Draculin-Front/dracu_app/lib/observability/embrace_http_client.dart)
in the Flutter app injects an `X-Embrace-Session-Id` header on
**every** outgoing HTTP request. The header value is the current
Embrace session ID. This costs the backend nothing — Django
ignores the header today — but it commits the **convention**.

A future "OTel-on-Django + Embrace-on-mobile correlation"
experiment could add a one-file Django middleware that:

```python
# Hypothetical Draculin/middleware/embrace_correlation.py
class EmbraceSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        session_id = request.headers.get("X-Embrace-Session-Id")
        if session_id:
            # Stash on the request; emit as an OTel span attribute /
            # log field / Sentry tag — depending on what the backend
            # is using at that point.
            request.embrace_session_id = session_id
        return self.get_response(request)
```

…and join the mobile session payload to the server-side trace by
session ID. That experiment is **deliberately out of scope** for
this PoC — the whole point is to observe mobile RUM in
isolation, with a server that's intentionally a black box.

## How to verify this branch's "no observability" claim

```bash
# In Draculin-Backend root on the obs-experiment-embrace branch
git diff master HEAD -- '*.py' 'requirements*.txt' 'docker-compose.yml'
# Should show only Sentry removals.

grep -ri 'sentry\|SENTRY' .
# Should show only the two intentional doc comments
# in settings.py and docker-compose.yml.

python manage.py check
# Should pass cleanly with no missing-module warnings.
```

## What's NOT on this branch (intentionally)

* No OpenTelemetry SDK.
* No Sentry helpers.
* No structured-logging middleware.
* No JMX-style runtime metrics.
* No request ID generator.
* No Prometheus exporter.

If you want any of that, switch to a different observability
PoC branch in another repo:

* Tracing + metrics + logs separately (LGTM): `Practica_de_Planificacion` on `obs-experiment-lgtm`.
* Wide events (Honeycomb): `pracpro2` on `obs-experiment-honeycomb`.
* Zero-instrumentation eBPF (Coroot): `subgrup-prop7.1` on `obs-experiment-coroot`.
* Document-store ELK (Elastic): `tenda_online` on `obs-experiment-elastic`.

## Cross-reference

Mobile-side scenarios that exercise the backend opacity:
[`Draculin-Front/dracu_app/observability/SCENARIOS.md`](../../Draculin-Front/dracu_app/observability/SCENARIOS.md),
specifically Scenario 2 ("Network failure spike — backend dies
mid-session").

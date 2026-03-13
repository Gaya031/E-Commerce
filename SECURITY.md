# RushCart Security Review Pipeline

This project enforces a repeatable security review process in CI.

## Automated checks

1. Python SAST: `bandit` scans backend code.
2. Python dependency audit: `pip-audit` scans `Backend/requirements.txt`.
3. Node dependency audit: `npm audit --audit-level=high` for:
   - `Frontend`
   - `Delivery-Service`
4. Container filesystem scan: `trivy` scans repository artifacts for high/critical issues.

## Review gates

1. Any high/critical vulnerability should block merge.
2. Exceptions must be documented with a remediation date.
3. Secrets must never be committed; use environment secrets in CI/CD.

## Manual review checklist (release)

1. Verify JWT secret is 32+ bytes in production.
2. Verify CORS and trusted hosts are restricted to deployed domains.
3. Verify rate-limits are active on auth, payment, admin, and search routes.
4. Verify upload restrictions and content-type checks for all file endpoints.
5. Verify payment webhook signature validation is enabled.
6. Verify admin and seller role boundaries with a smoke role test.

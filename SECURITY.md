# Security Policy — Draculin-Backend

## Reporting a Vulnerability
If you discover a security vulnerability, please email polcg10@gmail.com. Do not open a public issue.

## Security Considerations

### Health Data Privacy
- This application processes images of sanitary products for health analysis. This is **sensitive personal health data**.
- Do not log, cache, or store uploaded images longer than necessary for analysis.
- Comply with applicable data protection regulations (GDPR, etc.) if handling real user data.
- Ensure database entries containing health analysis results are not publicly accessible.

### API Key Management
- **Google Bard API key** and **Roboflow API key** are used for AI analysis. Store them in environment variables or `.env`, never in source code.
- Rotate API keys if they are ever exposed in logs, commits, or error messages.
- Restrict API key scopes/permissions to only what the application requires.

### Image Upload Validation
- Validate uploaded files: check MIME type, file extension, and magic bytes.
- Enforce a maximum file size to prevent resource exhaustion.
- Do not trust client-provided filenames — generate server-side names to prevent path traversal.
- Process images in a sandboxed context; malformed images can exploit parsing libraries.

### Django Security Settings
- Set `DEBUG = False` in production.
- Configure `ALLOWED_HOSTS` to restrict accepted hostnames.
- Use `SECURE_SSL_REDIRECT = True`, `SESSION_COOKIE_SECURE = True`, and `CSRF_COOKIE_SECURE = True` when serving over HTTPS.
- Keep `SECRET_KEY` out of version control and unique per environment.
- Enable `SECURE_HSTS_SECONDS` for HSTS enforcement.

### Database
- SQLite is used for development. For production, migrate to PostgreSQL with proper access controls.
- Ensure the SQLite file is not served by the web server or accessible via URL.

### Network & Deployment
- The backend runs on port 8889. Do not expose directly to the internet without a reverse proxy and TLS.
- Use HTTPS for all API communication, especially for image uploads and health data responses.
- Implement rate limiting on upload and analysis endpoints.

### Recommendations
- Add authentication and authorization to all endpoints before any real-world deployment.
- Implement audit logging for data access and analysis requests.
- Regularly update Django and all dependencies to patch known vulnerabilities.

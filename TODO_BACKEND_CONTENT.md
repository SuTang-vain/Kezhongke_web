# TODO: Backend Content Mounting System

Goal: add a lightweight backend and database layer for Kezhongke so the site can preview mounted Markdown/PDF articles and register other projects as navigable entries.

## 1. Target Architecture

- Keep the current static HTML site served by Nginx.
- Add a backend under `/api/`.
- Store article/project metadata in a database.
- Store source files on disk or object storage, not directly inside the database.
- Use Nginx for static file delivery where possible.

Recommended MVP stack:

- Backend: FastAPI
- Database: SQLite first, PostgreSQL later if content grows
- Content root: `/var/www/kezhongke_content`
- Project mount root: `/var/www/kezhongke_projects`

Suggested Nginx layout:

```text
/                 -> existing static Kezhongke site
/api/             -> backend service
/content/         -> uploaded or mounted markdown/pdf/image files
/projects/        -> mounted static projects
```

## 2. Database Tables

### articles

- `id`
- `title`
- `slug`
- `type`: `markdown | pdf | external`
- `file_path`
- `source_url`
- `cover_image`
- `summary`
- `category`
- `tags`
- `author`
- `status`: `draft | published | archived`
- `created_at`
- `updated_at`
- `published_at`

### projects

- `id`
- `name`
- `slug`
- `type`: `static | external | proxy`
- `entry_path`
- `public_url`
- `description`
- `cover_image`
- `status`: `draft | published | archived`
- `created_at`
- `updated_at`

## 3. API MVP

### Articles

- `GET /api/articles`
  - list published articles
  - filters: `type`, `category`, `tag`, `q`

- `GET /api/articles/{slug}`
  - return article metadata
  - for Markdown: return rendered HTML or raw Markdown plus metadata
  - for PDF: return preview URL

- `GET /api/articles/{slug}/raw`
  - return raw Markdown file or PDF stream when allowed

- `POST /api/admin/articles`
  - create article metadata
  - admin only

- `PUT /api/admin/articles/{id}`
  - update metadata
  - admin only

### Projects

- `GET /api/projects`
  - list mounted projects

- `GET /api/projects/{slug}`
  - return project metadata and access URL

- `POST /api/admin/projects`
  - register a mounted project
  - admin only

- `PUT /api/admin/projects/{id}`
  - update project mount config
  - admin only

## 4. Markdown Preview

Preferred behavior:

- Backend reads `.md` from the approved content root.
- Backend renders Markdown to HTML.
- Sanitize rendered HTML before returning it.
- Normalize relative image links to `/content/...` URLs.
- Optional later: code highlighting and table of contents generation.

Security requirements:

- Reject paths outside `/var/www/kezhongke_content`.
- Block path traversal such as `../`.
- Sanitize HTML to prevent XSS.

## 5. PDF Preview

MVP behavior:

- Store PDF files under `/var/www/kezhongke_content/pdfs`.
- Return preview URL in article response.
- Frontend previews with `<iframe>` or browser-native PDF viewer.

Later enhancement:

- Integrate PDF.js for custom toolbar, thumbnails, search, and page navigation.

## 6. Project Mounting

Supported project mount types:

- `static`: local static directory served by Nginx.
- `external`: external URL, displayed as an entry card.
- `proxy`: reverse proxy to local service, allowed only by whitelist.

Rules:

- Do not allow arbitrary proxy targets.
- Restrict static projects to `/var/www/kezhongke_projects`.
- Require unique `slug` for every project.
- Add health/status field later if needed.

## 7. Nginx Tasks

- Add `/api/` reverse proxy to backend service.
- Add `/content/` static alias to content root.
- Add `/projects/` static alias to project mount root.
- Keep existing route aliases:
  - `/`
  - `/about`
  - `/grow`
  - `/journal`
  - `/path`
  - `/atelier`

Example draft:

```nginx
location /api/ {
    proxy_pass http://127.0.0.1:8000/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}

location /content/ {
    alias /var/www/kezhongke_content/;
}

location /projects/ {
    alias /var/www/kezhongke_projects/;
}
```

## 8. Admin and Security

MVP admin auth:

- Use one server-side admin token stored in environment variable.
- Require token for all `/api/admin/*` endpoints.

Required safeguards:

- File extension allowlist: `.md`, `.pdf`, `.png`, `.jpg`, `.jpeg`, `.webp`.
- File size limits.
- Safe filename normalization.
- Path traversal protection.
- Markdown HTML sanitization.
- Proxy target whitelist.
- Basic request logging.

## 9. Frontend Integration

MVP frontend changes:

- Journal list reads from `GET /api/articles`.
- Article detail page supports Markdown and PDF article types.
- Add project listing section/page using `GET /api/projects`.
- Keep static fallback if API is unavailable.

Possible pages:

- `/journal` article list
- `/journal/:slug` article detail
- `/projects` project index
- `/projects/:slug` redirect or embedded preview

## 10. Implementation Phases

### Phase 1: Backend Skeleton

- Create FastAPI service.
- Add SQLite database.
- Add SQL migration or initialization script.
- Add health endpoint: `GET /api/health`.

### Phase 2: Article Metadata and Markdown Preview

- Add `articles` table.
- Add article list/detail endpoints.
- Add Markdown file reading and rendering.
- Add HTML sanitization.

### Phase 3: PDF Preview

- Add PDF article type.
- Add secure PDF streaming or static URL generation.
- Add frontend iframe preview.

### Phase 4: Project Mount Registry

- Add `projects` table.
- Add project list/detail endpoints.
- Support `static` and `external` types first.
- Add `proxy` only after whitelist design is finalized.

### Phase 5: Nginx and Deployment

- Add `/api/`, `/content/`, `/projects/` locations.
- Add systemd service for backend.
- Add backup process for SQLite and content files.

### Phase 6: Frontend Polish

- Replace static journal cards with API-driven cards.
- Add article detail template.
- Add project mount UI.
- Add loading/error/empty states.

## 11. Open Questions

- Should Markdown article detail be generated server-side HTML or rendered client-side?
- Should admin content creation happen by API only, or also by direct file upload?
- Should PDF files be public by default or require signed URLs?
- Do mounted projects need iframe embedding, direct link, or full Nginx path mount?
- Should SQLite be enough for the first release, or should PostgreSQL be used from day one?

## 12. Current Recommendation

Start with:

```text
FastAPI + SQLite + local file roots + Nginx aliases
```

This is the smallest reliable path and fits the current static-site deployment model.

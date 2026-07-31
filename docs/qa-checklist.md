# Local QA Checklist — Hugo Migration

**Date:** 2026-07-31  
**Method:** `hugo --minify` + `python3 -m http.server 8080 --bind 127.0.0.1` from `site/public` (Docker Compose unavailable — daemon down)

## Build

| Step | Result |
|------|--------|
| `cd site && hugo --minify` | Pass — 99 pages, 83 static files, exit 0 |

## Acceptance checks

| # | Criterion | Path / check | HTTP / result | Pass |
|---|-----------|--------------|---------------|------|
| 1 | Homepage loads | `/` | 200 | Pass |
| 2 | Blog index lists posts | `/blog/` | 200; `ul.blog-posts` with 45 entries | Pass |
| 3 | Sample post: Muhasabah | `/muhasabah/` | 200 | Pass |
| 3 | Sample post: API Key Best Practices | `/api-key-best-practices/` | 200 | Pass |
| 3 | Sample post: Silent Meeting | `/silent-meeting/` | 200 | Pass |
| 3 | Sample post: New Chapter of Kudo | `/new-chapter-of-kudo/` | 200 | Pass |
| 3 | Sample post: Facilitating a Great Meeting | `/facilitating-a-great-meeting/` | 200 | Pass |
| 4 | About page | `/about-me/` | 200 | Pass |
| 4 | Privacy policy | `/privacy-policy/` | 200 | Pass |
| 4 | Engineering lead materials | `/engineering-lead-materials/` | 200 | Pass |
| 5 | Category page lists posts | `/categories/meeting/` | 200; 3 meeting posts listed | Pass |
| 6 | In-content image | `/images/Screenshot-2025-01-21-at-10.18.40.png` | 200 | Pass |
| 7 | Google Analytics 4 | HTML contains `G-60P3WJPWMJ` | Found on `/` | Pass |
| 8 | Favicon link + asset | `<link rel="shortcut icon" …>`; `/images/favicon.png` | Link present; 200 | Pass |
| 9 | No `/wp-content/uploads/` requirement | `/wp-content/uploads/test.jpg` | 404 (acceptable per ADR-003) | Pass |

## Commands used

```bash
cd site && hugo --minify
cd site/public && python3 -m http.server 8080 --bind 127.0.0.1

for p in / /blog/ /muhasabah/ /api-key-best-practices/ /silent-meeting/ \
         /new-chapter-of-kudo/ /facilitating-a-great-meeting/ /about-me/ \
         /privacy-policy/ /engineering-lead-materials/ /images/favicon.png \
         /categories/meeting/ /images/Screenshot-2025-01-21-at-10.18.40.png \
         /wp-content/uploads/test.jpg; do
  echo -n "$p "
  curl -s -o /dev/null -w "%{http_code}\n" "http://127.0.0.1:8080$p"
done

curl -s http://127.0.0.1:8080/ | grep -o 'G-60P3WJPWMJ'
```

## Summary

**Overall: Pass** — all design success criteria met via Hugo build + static file server.

## Compose verification (network `web`)

After ADR-004 revision, Compose does **not** publish `127.0.0.1:8080`. Verify with:

```bash
docker network ls | grep -w web || docker network create web
docker compose build && docker compose up -d
docker run --rm --network web curlimages/curl:8.5.0 -sI http://panjigautama-hugo:8080/ | head -1
```

Historical checks above used Hugo `public/` + `python3 -m http.server` or an older Compose port publish; those results remain valid for content QA.

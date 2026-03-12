# AEO Implementation Checklist For taiwan-stock-radar

This checklist is based on the pattern shown by [AEO Spider](https://aeo.md5.com.tw/): make the site easy for AI crawlers to access, understand, and cite.

## Priority 1: must-have

- Serve `/` with a clear project description
- Serve `/robots.txt` with `200`
- Serve `/sitemap.xml` with `200`
- Serve `/llms.txt` with `200`
- Add JSON-LD to the home page
- Add an FAQ page with FAQPage schema
- Add complete title and meta description tags

## Priority 2: strongly recommended

- Add a methodology page
- Add a docs page
- Add use-case pages
- Add updated timestamps on important pages
- Add risk disclaimer and authorship / maintainer info

## Content design rules

- Use direct, literal titles
- Put the project summary in the first screen
- Avoid vague brand-only wording
- Give AI short paragraphs it can cite cleanly
- Keep one page for one major topic

## What to monitor

Based on the crawler-tracking pattern shown on AEO Spider, monitor:

- visits to `/`
- visits to `/robots.txt`
- visits to `/llms.txt`
- visits to `/faq`
- HTTP status codes for those pages

## Publish target

Current public website target:

- `https://rabbit68116-ux.github.io/taiwan-stock-radar/`

## Before publishing

- enable GitHub Pages with `main` branch and `/docs`
- confirm `https://rabbit68116-ux.github.io/taiwan-stock-radar/robots.txt` returns `200`
- confirm `https://rabbit68116-ux.github.io/taiwan-stock-radar/llms.txt` returns `200`
- confirm `https://rabbit68116-ux.github.io/taiwan-stock-radar/sitemap.xml` returns `200`
- update FAQ wording if product scope changes

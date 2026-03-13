# LoraCamp Testing Guide

This document outlines how to test the various features of LoraCamp using the provided `test_catalog`. By expanding this catalog, we can ensure that every parameter in our TOML manifests has a representation that can be visually verified on the static site.

## 1. Catalog Level (`catalog.toml`)

- **title / creator**: Verify the header area and `<title>` tag.
- **base_url / cdn_url**: Verify asset and page URLs (e.g. Og:tags in head).
- **language**: Check the `<html lang="en">` attribute.
- **synopsis / about**: Check the index page text.
- **links**: Verify header and footer external links exist.
- **theme**: Verify color changes (base, accent_hue, round_corners) via CSS custom properties on `<body>`.

## 2. Creator Level (`creator.toml`)

- **name / aliases**: Verify the creator page title and alias display.
- **about / image**: Verify profile image cropping and biography display.
- **links**: Verify table of links at the bottom of the creator page.
- **permalink**: Verify proper directory routing (e.g., `/scruffy/`).

## 3. Model Level (`model.toml`)

- **title / release_date**: Displayed prominently on the left panel.
- **about / synopsis**: The rich text body of the model page.
- **trigger_word**: The clipboard-enabled pill under the title.
- **creator / creators**: Verify linking back to creator pages, including multiple creator setups.
- **base_model / version**: Verify metadata table.
- **tags**: Used for the typeahead search box and displayed on the page.
- **sample_prompts**: Unused in UI directly, verify parsing doesn't error.
- **unlisted**: Not shown on the index page, but still built.

## 4. Sample Level (`[sample_name.]sample.toml`)

- **title**: Replaces the fallback filename in the playlist.
- **tags**: Verifiable via the top-right Search Modal (e.g., search "alpha").
- **prompt / negative_prompt / seed**: Verifiable in the metadata modal (click the sample row).
- **model / vae / loras**: Verifiable in the Generation details metadata modal.
- **lyrics / bpm**: Check the lyrics overlay and metadata readout.

## How to Test Search (Tags & Titles)

1. Build the catalog: `uv run loracamp --build --output buildsite test_catalog`
2. Open `buildsite/yoursite/index.html` in a browser.
3. Click **Search** in the header.
4. Type `alpha`. It should match files explicitly tagged with `alpha`.
5. Find a model without a preview image to verify it renders a clean box without a broken UI element.

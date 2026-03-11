# creator.toml Reference

Creators are defined to provide profiles for the people or groups who make the models and samples. 

## Profile Structure

To define a creator with their own page, create a directory for them and place a `creator.toml` inside it.

```toml
name = "PhotographyExpert"
permalink = "photography-expert"
about = "I specialize in vintage film aesthetics and high-contrast street photography."

[links]
website = "https://example.com"
instagram = "https://instagram.com/photographyexpert"
```

## Options

### `name`
The display name of the Creator. This is matched against the `creator` field in Model and Sample manifests.

### `permalink` (Optional)
The URL slug for the creator page. If omitted, the directory name is used.

### `about` (Optional)
A short biography or description of the creator. Supports Markdown.

### `image` (Optional)
A path to a profile image.
```toml
image = "profile.jpg"
```

### `links` (Optional)
A table of social media or external links.
```toml
[links]
GitHub = "https://github.com/..."
Twitter = "https://twitter.com/..."
```

---

## Pending Implementation (Faircamp Gaps)

The following features from Faircamp's `artist.eno` are not yet implemented in LoraCamp:

| Field | Description |
| :--- | :--- |
| `aliases` | Mapping multiple name variations to one creator identity. |
| `verification`| Support for `rel="me"` links for social profile verification. |
| `external_page`| Redirecting a creator profile to an external URL. |
| `m3u` | Generation of an M3U playlist for all of a creator's samples. |
| `image description`| Explicit alt-text field for the profile image. |
| `copy_link` | Toggle to disable the "Copy Link" button on the creator page. |

---
*Note: This is adapted from Faircamp's artist options.*

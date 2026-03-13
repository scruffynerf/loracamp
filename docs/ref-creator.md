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

### `aliases` (Optional)

A list of alternative names for this creator. Used to match against model creators during indexing.

```toml
aliases = ["Artisan", "A. Studios"]
```

### `permalink` (Optional)

The URL slug for the creator page. If omitted, the directory name is used.

### `about` (Optional)

A short biography or description of the creator. Supports Markdown.

### `image` (Optional)

A path to a profile image.

```toml
image = "profile.jpg"
```

### `image_description` (Optional)

Alt text for the profile image. If omitted, the creator's name is used.

```toml
image_description = "A portrait photo of the creator"
```

### `copy_link` (Optional)

Whether to show the "Copy Link" button on the creator page. Defaults to `true`.

```toml
copy_link = false
```

### `links` (Optional)

A table of social media or external links.

```toml
[links]
GitHub = "https://github.com/..."
Twitter = "https://twitter.com/..."
```

### `opengraph` (Optional)

Provide page-specific overrides for OpenGraph tags.

```toml
[opengraph]
title = "My Portfolio"
description = "A gallery of my best works."
```

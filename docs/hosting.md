# Going Online (Hosting)

Since LoraCamp generates a **static website**, you can host it almost anywhere for very little cost (or even for free).

## The Build Output

By default, when you run `loracamp --build --output buildsite`, LoraCamp generates everything into one directory containing your HTML, CSS, `.safetensors` models, and audio samples. This directory is ready to be uploaded to any standard web host.

## Simple Hosting (Default)

The simplest way to go online is to upload the entire output directory to your web server.

### Steps

1.  Run `loracamp --build --output buildsite`.
2.  Upload the contents of `buildsite/` to your web server's root (e.g., via FTP or an automated deployment tool).
3.  Ensure your `base_url` in `catalog.toml` (if used) matches your domain.

Your models and samples will be reachable via relative links, making the site completely self-contained.

## Advanced Hosting (Split CDN)

If you have a lot of large models, you might want to host the site on a fast static host (like GitHub Pages, Netlify, or Vercel) and the models on a dedicated storage provider (like Amazon S3, Backblaze B2, Cloudflare R2, HuggingFace, or Modelscope).

### Steps

1. Set up your storage provider (HuggingFace, S3, etc.) and note your public URL.
2. Configure `cdn_url` in your `catalog.toml` to point to that URL:

```toml
cdn_url = "https://huggingface.co/datasets/username/repo/resolve/main"
```

1. Run `loracamp --build` to generate your site.
2. Upload the contents of `yourcdn/` to your storage provider.
3. Upload the contents of `yoursite/` to your static host (GitHub Pages, Vercel, etc.).

LoraCamp uses the `cdn_url` during the build to ensure all models and samples point to the correct remote locations.

---

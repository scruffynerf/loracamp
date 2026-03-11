# LoraCamp

LoraCamp is a static site generator designed for sharing **Loras** (safetensor models for image and audio generation). 

It is a Python port and adaptation of [faircamp](https://simonrepp.com/faircamp/), tailored for a different audience but maintaining the same core philosophy: providing a painless, non-technical way to share creative work via a beautiful, static website with no complex backend or database requirements.

## Our Mission

While `faircamp` is built for musicians to share their music albums, **LoraCamp** is built for the generative AI community to share their models. 

LoraCamp allows users to:
- Structure their Loras and samples into folders (similar to albums).
- Generate a "static website" bundle of HTML/CSS/JS.
- Provide sample outputs (Audio/Images) for evaluating the model's performance.
- Offer the `.safetensors` files for direct download.

## Getting Started

Currently, LoraCamp is in the early stages of being ported from Rust (faircamp) to Python. We are starting with support for **Music Loras**, where samples are provided as audio files (MP3s) alongside the Safetensor models.

## License

LoraCamp is licensed under the **GNU Affero General Public License (AGPL) 3.0**, out of respect for the original `faircamp` project and to ensure the software remains free for the community.
# Manifests

LoraCamp uses several types of *manifests* to specify metadata and settings:

- **catalog.toml**: Placed at the root of your catalog directory. Provides global site settings.
- **creator.toml**: Placed in a creator's directory to define their profile (biography, links, etc.).
- **model.toml**: Placed in each Model's directory. Specifies options for that specific model (title, creator, prompts, etc.).
- **sample.toml**: Placed alongside or in a directory for a specific sample output.

## Directory Structure

An example catalog might look like this:

```
MyModelCatalog/
├─ catalog.toml
├─ cinematic-style/
│  ├─ model.toml           <--- Model Manifest
│  ├─ model.safetensors
│  └─ preview.jpg
└─ scruffy/                <--- Creator Directory
   ├─ creator.toml         <--- Creator Manifest
   └─ watercolor-style/    <--- Nested Model
      ├─ model.toml
      ├─ model.safetensors
      └─ samples/
         ├─ demo_audio.mp3
         └─ demo_audio.sample.toml <--- Sample Manifest
```

## catalog.toml

This file contains site-wide settings.

```toml
title = "My Model Collection"
creator = "Scruffy"
base_url = "https://loracamp.example.com"

# cdn_url = "https://cdn.example.com" # Optional
```

## model.toml

This file defines the metadata for a specific model.

```toml
title = "Cinematic Style"
creator = "Scruffy"
permalink = "cinematic-style"
trigger_word = "cinematic"
about = "This model produces high-contrast, cinematic images."
```

---

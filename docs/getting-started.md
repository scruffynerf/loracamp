# Getting Started with LoraCamp

First let's look at the input structure LoraCamp expects:

```
Models/                       <--- Top directory ("Catalog")
├─ My Awesome Lora/           <--- Nested Directory ("Lora")
│  ├─ sample_1.mp3            <--- Eval Sample (Audio/Image)
│  ├─ sample_2.mp3
│  └─ my_model.safetensors    <--- The Model File (Safetensors)
└─ Collections/               <--- Extra nesting (optional)
   └─ Vintage Image Lora/     <--- Nested Directory ("Lora")
      ├─ sample_output.jpg    <--- Eval Sample
      ├─ preview.png          <--- Preview image (optional)
      └─ model_v1.safetensors <--- The Model File
```

LoraCamp takes a directory with nested folders as input. **Convention**: Directories that contain `.safetensors` files will be presented as **Loras** (units of sharing) with their own dedicated page.

## Building your site

To use LoraCamp, prepare your catalog folder (similar to `Models/` above), and run:

```bash
loracamp --build
```

By default, LoraCamp will write the site to a `yoursite/` folder (and optionally a `yourcdn/` folder for large files) inside your catalog directory. 

Unlike the original `faircamp`, LoraCamp does **not** include a built-in "live preview" server. To view your site, simply open the `index.html` file in the `yoursite/` directory with your preferred web browser.

---

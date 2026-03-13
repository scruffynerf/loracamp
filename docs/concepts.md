# Concepts Explained

## What is a permalink?

Within LoraCamp, each of your **Loras** (the models you share) is represented on its own page. Each page can be reached through its own address (URL), i.e. the link that you share with others.

Each of your pages needs a unique identifier (a "name") by which it can be clearly and permanently identified. This part is the **permalink**.

For example, if you share a Lora called "Vintage Cinema Style", a logical permalink would be `vintage-cinema-style`. 

In LoraCamp, you would specify this in a manifest file:

```toml
permalink = "vintage-cinema-style"
```

Ultimately, visitors can reach that Lora page under a URL like `https://your-site.com/vintage-cinema-style/`.

## What is a static site generator?

Most websites today are *dynamic*—they require complex servers and databases to "build" a page every time someone visits it. This makes them prone to breaking, security issues, and "going stale" as software versions change.

A **static** website is written once, ahead of time. It's just a collection of simple HTML, CSS, and JavaScript files. Your computer does the work of "writing the book" (generating the site), and then you just hand that book to a simple web server. 

**LoraCamp** is the tool (the static site generator) you use to "write the book" for your model collection.

---

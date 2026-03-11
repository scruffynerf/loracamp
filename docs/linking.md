# Linking to Samples and Timecodes

You can create links that directly jump to a specific sample or timecode on a Model page.

## Examples

If you want to point visitors to a specific section of a sample (e.g., a specific rhythmic pattern or texture), you can use anchor parameters in the URL.

### Link to a Specific Sample

To link to the third sample in a Model's list:
`https://example.com/cinematic-model/index.html#sample=3`

### Link to a Specific Timecode

To link 20 seconds into the first sample:
`https://example.com/cinematic-model/index.html#time=20s`

To link to Sample 3 at 45 seconds:
`https://example.com/cinematic-model/index.html#sample=3&time=45s`

## Syntax Details

You can supply a sample number (`sample` or `n`), a timecode (`time` or `t`), or both.

-   **Sample Number**: Use `#sample=N` or `#n=N`.
-   **Timecode**: Use `#time=X` or `#t=X`.

### Timecode Formats

Timecodes follow a standard hours (`h`), minutes (`m`), and seconds (`s`) format. They must be provided in that order.

-   `#time=30s` (30 seconds)
-   `#time=2m` (2 minutes)
-   `#time=2m30s` (2 minutes, 30 seconds)
-   `#time=1h15m` (1 hour, 15 minutes)

## Usage in Manifests

You can use these links within your `about` or `synopsis` fields in `model.toml` or `catalog.toml`:

```toml
about = "Check out the texture [at 1m20s](#time=1m20s) of the first sample."
```

## ACNH Catalog Extractor

Utility to extract your ACNH catalog from a 30 second video captured from Switch.

The data will be exported into
* `catalog.txt` - names of the items you own, separated by newline.
* `catalog.ndjson` - items you own in json format.

Keep in mind that specific variations of an item are not taken into account, just the item itself.

### How to use

```
docker run -v $(pwd):/app ac-catalog python3 main.py samples/sample.mp4
```

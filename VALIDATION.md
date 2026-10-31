# Publication validation

Local CPU inference from safetensors succeeded on one cached image with the historical evaluation transform. Output shapes: 1x5, 1x50, 1x11, 1x4; values finite; predict() returned all four tasks. Full test evaluation was not rerun.

Tested versions:

```json
{
  "torch": "2.14.1",
  "torchvision": "0.29.2",
  "transformers": "5.20.2",
  "safetensors": "0.8.0",
  "pillow": "12.3.0",
  "huggingface_hub": "2.4.0"
}
```

JSON and Python syntax validated. Original notebook bytes and outputs preserved. Pattern scans found no HF/GitHub tokens, private-key headers or literal credential assignments in published text/notebooks. This is not a complete privacy or malware guarantee. Upstream public dataset contact emails remain.

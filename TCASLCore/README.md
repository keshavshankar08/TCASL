# TCASLCore

A lightweight Python inference engine for real-time American Sign Language (ASL) recognition using temporal contrast emulation to simulate a Dynamic Vision Sensor (DVS).

## Features

- **Temporal contrast emulation:** Converts standard webcam frames into sparse DVS-style event maps, isolating hand motion and discarding static background.
- **Auto-downloading weights:** Model weights are fetched automatically from GitHub Releases and cached locally via `torch.hub`, no manual download required.
- **Auto-formatting:** Center-crops and rescales raw frames to the 128×128 input resolution expected by the network.
- **Multiple model versions:** Switch between `sdnn_v1` and `sdnn_v2` via a single argument, or supply your own local `.pth` file.

## Installation

```bash
pip install tcasl
```

## Quick Start

Full examples (static image and real-time webcam) are in [`examples/`](https://github.com/keshavshankar08/TCASL/tree/main/TCASLCore/examples).

## Available Models

| Tag | Description |
|---|---|
| `sdnn_v2` *(default)* | Latest release (97.3% Accuracy) |
| `sdnn_v1` | Initial release (95.9% Accuracy) |

## API Reference

Full docstrings are in [`src/tcasl/core.py`](https://github.com/keshavshankar08/TCASL/blob/main/TCASLCore/src/tcasl/core.py).

## TCASL Project

For background and the research paper, see the [main TCASL repository](https://github.com/keshavshankar08/TCASL).
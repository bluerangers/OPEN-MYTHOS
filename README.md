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

# macOS — launch from Applications
```

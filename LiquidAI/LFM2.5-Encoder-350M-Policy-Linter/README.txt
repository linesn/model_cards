---
language:
- en
- de
- es
- fr
- it
- nl
- pl
- pt
- ar
- hi
- ja
- ru
- tr
- vi
- zh
tags:
- liquid
- lfm2
- lfm2.5
- bidirectional
- masked-lm
- encoder
library_name: transformers
license: other
license_name: lfm1.0
license_link: LICENSE
pipeline_tag: token-classification
base_model:
    - LiquidAI/LFM2.5-Encoder-350M
---

<div align="center">
  <img 
    src="https://cdn-uploads.huggingface.co/production/uploads/61b8e2ba285851687028d395/2b08LKpev0DNEk6DlnWkY.png" 
    alt="Liquid AI" 
    style="width: 100%; max-width: 100%; height: auto; display: inline-block; margin-bottom: 0.5em; margin-top: 0.5em;"
  />
  <div style="display: flex; justify-content: center; gap: 0.5em; margin-bottom: 1em;">
    <a href="https://playground.liquid.ai/"><strong>Try LFM</strong></a> • 
    <a href="https://docs.liquid.ai/lfm/getting-started/welcome"><strong>Docs</strong></a> • 
    <a href="https://leap.liquid.ai/"><strong>LEAP</strong></a> • 
    <a href="https://discord.com/invite/liquid-ai"><strong>Discord</strong></a>
  </div>
</div>

# LFM2.5-Encoder-350-Policy-Linter

A full fine-tune of [LFM2.5-Encoder-350M](https://huggingface.co/LiquidAI/LFM2.5-Encoder-350M) with a rule-matching head that scores every text token against free-text policy rules in a single encoder pass.

Find more details about our encoders in our [blog post](https://www.liquid.ai/blog/lfm2-5-encoders).

> [!NOTE]
> 💻 **Demos**: Try this fine-tuned model running in a CPU-only Hugging Face space:
> [Zero-shot policy linting](https://huggingface.co/spaces/LiquidAI/policy-linting)** — check text against your company's rules, written as free text. It scores every token against every rule in one pass.

## Usage

> ⚠️ Loads custom code via `trust_remote_code=True` (the model wraps a `trust_remote_code` encoder).

Install the required packages:

```bash
pip install torch transformers
```

Run zero-shot policy linting:

```python
import sys
from pathlib import Path

import torch
from transformers import AutoTokenizer

repo = Path(".")
sys.path.insert(0, str(repo))

from train_bizlint_v02 import Lfm2BidirForRuleMatching

rules = [
    "Flag direct mentions of competitor companies.",
    "Flag promises about guaranteed financial returns.",
]
text = "Our product is better than AcmeAI and will guarantee 30% savings."

prefix = "Policy:\n" + "\n".join(f"- {rule}" for rule in rules) + "\n\nText:\n"
full_text = prefix + text

tokenizer = AutoTokenizer.from_pretrained(repo, trust_remote_code=True)
model = Lfm2BidirForRuleMatching.from_pretrained(repo, trust_remote_code=True).eval()

enc = tokenizer(full_text, return_offsets_mapping=True, return_tensors="pt")
offsets = enc.pop("offset_mapping")[0].tolist()

rule_pool = torch.zeros(1, len(rules), len(offsets))
pos = len("Policy:\n")

for rule_idx, rule in enumerate(rules):
    start = pos + 2
    end = start + len(rule)
    token_idxs = [
        i for i, (a, b) in enumerate(offsets)
        if a < end and b > start and a != b
    ]
    rule_pool[0, rule_idx, token_idxs] = 1 / len(token_idxs)
    pos = end + 1

with torch.no_grad():
    probs = model(**enc, rule_pool=rule_pool)["logits"].sigmoid()[0]

text_start = len(prefix)

for token_idx, (a, b) in enumerate(offsets):
    if b <= text_start or a == b:
        continue

    token_text = full_text[a:b]
    for rule_idx, prob in enumerate(probs[token_idx]):
        if prob.item() > 0.5:
            print(f"{token_text!r} -> {prob.item():.3f}: {rules[rule_idx]}")
```

## 📬 Contact

- Got questions or want to connect? [Join our Discord community](https://discord.com/invite/liquid-ai)
- If you are interested in custom solutions with edge deployment, please contact [our sales team](https://www.liquid.ai/contact).

## Citation

```bibtex
@article{liquidAI2026Encoders,
  author = {Liquid AI},
  title = {LFM2.5-Encoders: Fast at Long Context, Even on CPU},
  journal = {Liquid AI Blog},
  year = {2026},
  note = {www.liquid.ai/blog/lfm2-5-encoders},
}
```

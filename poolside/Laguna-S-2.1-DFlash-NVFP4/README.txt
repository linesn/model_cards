---
library_name: speculators
base_model:
- poolside/Laguna-S-2.1-NVFP4
tags:
- speculative-decoding
- dflash
- speculators
---

<p align="center">
  <img alt="poolside-banner" src="https://poolside.ai/assets/laguna/laguna-s-2-1-banner.svg" width="800px">
</p>

<p align="center">
  <a href="https://openrouter.ai/poolside/laguna-s-2.1"><strong>Use on OpenRouter</strong></a> ·
  <a href="https://vercel.com/ai-gateway/models/laguna-s-2.1"><strong>Use on Vercel AI Gateway</strong></a> ·
  <a href="https://poolside.ai/blog/introducing-laguna-s-2-1"><strong>Release blog post</strong></a>
</p>

<br>

# poolside/Laguna-S-2.1-DFlash-NVFP4

DFlash speculator for the NVFP4 target [poolside/Laguna-S-2.1-NVFP4](https://huggingface.co/poolside/Laguna-S-2.1-NVFP4). The
speculator is a 6-layer Laguna-style draft model (BF16); pair it with the NVFP4 base for
lower-latency serving via speculative decoding.

Trained: `e0630_rhiemann_baseline` SFT, DFlash Stage-2, 15k steps. Recommended
serving setting: `num_speculative_tokens=7`.
DFlash upstream support is in progress (vLLM #46853, SGLang #29446, TRT-LLM #15666). Use
`poolside/Laguna-S-2.1-NVFP4` as the target model.

## Benchmarks

Measured with TP=2, `temperature=0`, and `num_speculative_tokens=15`.

### Throughput speedup

| Concurrency | GSM8K | MATH-500 | HumanEval | MBPP | MT-Bench |
|---:|---:|---:|---:|---:|---:|
| 1 | 3.324x | 2.893x | 3.692x | 2.426x | 2.338x |
| 4 | 2.498x | 2.174x | 2.742x | 1.848x | 1.831x |
| 8 | 2.279x | 1.948x | 2.634x | 1.719x | 1.772x |
| 16 | 2.302x | 1.965x | 2.626x | 1.731x | 1.672x |

### Acceptance length

| Concurrency | GSM8K | MATH-500 | HumanEval | MBPP | MT-Bench |
|---:|---:|---:|---:|---:|---:|
| 1 | 5.775 | 4.942 | 6.438 | 4.171 | 4.017 |
| 4 | 5.804 | 4.935 | 6.298 | 4.161 | 4.091 |
| 8 | 5.719 | 4.885 | 6.537 | 4.193 | 4.373 |
| 16 | 5.758 | 4.896 | 6.412 | 4.123 | 3.981 |

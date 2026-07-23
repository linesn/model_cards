---
library_name: speculators
base_model:
- poolside/Laguna-S-2.1-FP8
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

# poolside/Laguna-S-2.1-DFlash-FP8

DFlash speculator for the FP8 target [poolside/Laguna-S-2.1-FP8](https://huggingface.co/poolside/Laguna-S-2.1-FP8). The
speculator is a 6-layer Laguna-style draft model (BF16); pair it with the FP8 base for
lower-latency serving via speculative decoding.

Trained: `e0630_rhiemann_baseline` SFT, DFlash Stage-2, 15k steps. Recommended
serving setting: `num_speculative_tokens=7`.
DFlash upstream support is in progress (vLLM #46853, SGLang #29446, TRT-LLM #15666). Use
`poolside/Laguna-S-2.1-FP8` as the target model.

## Benchmarks

Measured with TP=2, `temperature=0`, and `num_speculative_tokens=15`.

### Throughput speedup

| Concurrency | GSM8K | MATH-500 | HumanEval | MBPP | MT-Bench |
|---:|---:|---:|---:|---:|---:|
| 1 | 3.179x | 2.938x | 3.269x | 2.380x | 2.603x |
| 4 | 2.614x | 2.423x | 2.691x | 1.963x | 2.090x |
| 8 | 2.666x | 2.410x | 2.803x | 1.962x | 2.230x |
| 16 | 2.618x | 2.364x | 2.866x | 2.031x | 2.302x |

### Acceptance length

| Concurrency | GSM8K | MATH-500 | HumanEval | MBPP | MT-Bench |
|---:|---:|---:|---:|---:|---:|
| 1 | 5.748 | 5.197 | 5.889 | 4.247 | 4.663 |
| 4 | 5.765 | 5.212 | 5.882 | 4.218 | 4.411 |
| 8 | 5.863 | 5.199 | 6.094 | 4.178 | 4.572 |
| 16 | 5.787 | 5.161 | 6.144 | 4.291 | 4.600 |

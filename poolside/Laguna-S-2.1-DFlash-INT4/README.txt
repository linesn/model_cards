---
library_name: speculators
base_model:
- poolside/Laguna-S-2.1-INT4
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

# poolside/Laguna-S-2.1-DFlash-INT4

DFlash speculator for the INT4 target [poolside/Laguna-S-2.1-INT4](https://huggingface.co/poolside/Laguna-S-2.1-INT4). The
speculator is a 6-layer Laguna-style draft model (BF16); pair it with the INT4 base for
lower-latency serving via speculative decoding.

Trained: `e0630_rhiemann_baseline` SFT, DFlash Stage-2, 15k steps. Recommended
serving setting: `num_speculative_tokens=7`.
DFlash upstream support is in progress (vLLM #46853, SGLang #29446, TRT-LLM #15666). Use
`poolside/Laguna-S-2.1-INT4` as the target model.

## Benchmarks

Measured with TP=2, `temperature=0`, and `num_speculative_tokens=15`.

### Throughput speedup

| Concurrency | GSM8K | MATH-500 | HumanEval | MBPP | MT-Bench |
|---:|---:|---:|---:|---:|---:|
| 1 | 3.697x | 3.216x | 3.776x | 2.704x | 2.525x |
| 4 | 2.815x | 2.521x | 2.995x | 2.145x | 1.980x |
| 8 | 2.541x | 2.247x | 2.865x | 1.970x | 1.953x |
| 16 | 2.426x | 2.161x | 2.629x | 1.895x | 1.935x |

### Acceptance length

| Concurrency | GSM8K | MATH-500 | HumanEval | MBPP | MT-Bench |
|---:|---:|---:|---:|---:|---:|
| 1 | 6.273 | 5.363 | 6.416 | 4.532 | 4.217 |
| 4 | 6.111 | 5.336 | 6.416 | 4.498 | 4.154 |
| 8 | 6.133 | 5.356 | 6.777 | 4.565 | 4.383 |
| 16 | 6.145 | 5.393 | 6.314 | 4.507 | 4.636 |

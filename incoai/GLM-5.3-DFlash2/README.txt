---
license: cc-by-nc-nd-4.0
library_name: transformers
pipeline_tag: text-generation
base_model:
  - zai-org/GLM-5.3
inference: false
tags:
  - dflash
  - dflash2
  - speculative-decoding
  - block-diffusion
  - draft-model
  - sglang
---

# GLM-5.3-DFlash2

[Blog](https://inco.ai/blog/dflash2/) | [GitHub](https://github.com/z-lab/dflash)

This repository contains the DFlash 2 draft model for
[`zai-org/GLM-5.3`](https://huggingface.co/zai-org/GLM-5.3).
It is not a standalone language model: it runs inside a speculative
decoding server and drafts tokens for the target model to verify.

DFlash 2 is a block-diffusion drafter for speculative decoding. It predicts
a whole block of tokens in a single pass and keeps the top candidates at
every position. A lightweight selector then traces one coherent path through them.
Two-tap dynamic convolutions in the backbone keep the draft from decaying
toward the end of the block. Decoding is lossless: greedy output
matches the target model exactly, and sampling preserves its distribution.

<div align="center">
  <img src="assets/dflash2-figure.png" alt="DFlash 2: parallel block drafting with a candidate path selector" width="100%">
</div>

## Quick Start

Serve with [SGLang](https://github.com/sgl-project/sglang):

```bash
pip install "sglang[all] @ git+https://github.com/sgl-project/sglang.git#subdirectory=python"

sglang serve \
  --model-path zai-org/GLM-5.3 \
  --tp-size 4 \
  --trust-remote-code \
  --speculative-algorithm DFLASH \
  --speculative-draft-model-path incoai/GLM-5.3-DFlash2 \
  --speculative-draft-attention-backend fa4
```

DFlash 2 is also supported by vLLM v0.28.0 and later; see
[`incoai/GLM-5.3-NVFP4`](https://huggingface.co/incoai/GLM-5.3-NVFP4) for a
vLLM serving example with the NVFP4-quantized target. See the
[blog post](https://inco.ai/blog/dflash2/) for more details.

## Evaluation

- Runtime: SGLang on four NVIDIA GB300 GPUs (TP4), with FlashAttention 4 for DFlash 2 draft attention
- Speculation block size: 8 (7 draft tokens per verification step)
- Sampling: GLM-5.3's officially recommended parameters (temperature 1.0, top-p 0.95), with the default `Max` reasoning effort
- Maximum new tokens: 4096
- Samples: 128 at concurrency 1; 1,024 at concurrency 8 and 32

We compare autoregressive decoding, GLM-5.3's native MTP, and DFlash 2.
All speculative methods propose seven draft tokens per verification step.

### Acceptance Length

Acceptance length is the per-request mean of completion tokens divided by verification steps.
Higher is better.

| Task | MTP | DFlash 2 |
| :--- | ---: | ---: |
| GSM8K | 5.12 | **5.94** |
| MATH-500 | 5.05 | **6.02** |
| HumanEval | 4.85 | **5.48** |
| MBPP | 4.34 | **4.95** |
| MT-Bench | 3.81 | **4.19** |

### Throughput

Throughput is total output tokens divided by end-to-end wall time.
Each cell shows `output tok/s (speedup vs. autoregressive)`.

#### Concurrency 1

| Task | Autoregressive | MTP | DFlash 2 |
| :--- | ---: | ---: | ---: |
| GSM8K | 113.4 | 292.6 (2.58×) | **366.6 (3.23×)** |
| MATH-500 | 113.1 | 297.4 (2.63×) | **383.3 (3.39×)** |
| HumanEval | 113.7 | 292.9 (2.58×) | **363.7 (3.20×)** |
| MBPP | 113.4 | 266.5 (2.35×) | **336.5 (2.97×)** |
| MT-Bench | 113.2 | 206.8 (1.83×) | **244.3 (2.16×)** |

#### Concurrency 8

| Task | Autoregressive | MTP | DFlash 2 |
| :--- | ---: | ---: | ---: |
| GSM8K | 535.3 | 1,094.5 (2.04×) | **1,310.4 (2.45×)** |
| MATH-500 | 549.6 | 1,145.6 (2.08×) | **1,409.7 (2.56×)** |
| HumanEval | 554.4 | 1,133.8 (2.05×) | **1,360.6 (2.45×)** |
| MBPP | 554.2 | 1,049.7 (1.89×) | **1,277.4 (2.31×)** |
| MT-Bench | 544.5 | 807.0 (1.48×) | **895.5 (1.64×)** |

#### Concurrency 32

| Task | Autoregressive | MTP | DFlash 2 |
| :--- | ---: | ---: | ---: |
| GSM8K | 1,142.7 | 2,283.6 (2.00×) | **2,694.5 (2.36×)** |
| MATH-500 | 1,251.8 | 2,943.2 (2.35×) | **3,559.8 (2.84×)** |
| HumanEval | 1,303.1 | 3,016.9 (2.32×) | **3,589.1 (2.75×)** |
| MBPP | 1,292.8 | 2,790.2 (2.16×) | **3,380.4 (2.61×)** |
| MT-Bench | 1,262.7 | 2,119.5 (1.68×) | **2,345.0 (1.86×)** |

## License

This model is released under
[CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/)
for research and evaluation. For commercial licensing, contact
[contact@inco.ai](mailto:contact@inco.ai).

## Citation

If you find DFlash 2 useful, please cite:

```bibtex
@misc{inco2026dflash2,
  title  = {{DFlash 2: Keep Drafting Parallel}},
  author = {{Inco AI}},
  year   = {2026},
  month  = {August},
  url    = {https://inco.ai/blog/dflash2/}
}
```

Please also cite the original DFlash paper:

```bibtex
@inproceedings{chen2026dflash,
  title     = {{DFlash: Block Diffusion for Flash Speculative Decoding}},
  author    = {Chen, Jian and Liang, Yesheng and Liu, Zhijian},
  booktitle = {International Conference on Machine Learning (ICML)},
  year      = {2026}
}
```

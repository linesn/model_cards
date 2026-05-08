---
license: other
base_model: moonshotai/Kimi-K2.6
tags:
- text-generation
- speculative-decoding
- eagle3
- kimi-k2.6
- torchspec
---

# kimi-k2.6-eagle3-mla

## Model Overview

kimi-k2.6-eagle3-mla is an Eagle3 MTP draft model with MLA (Multi-Latent Attention) for accelerating inference of [Kimi-K2.6](https://huggingface.co/moonshotai/Kimi-K2.6), trained with [TorchSpec](https://github.com/torchspec-project/TorchSpec) — an online speculative decoding training framework that runs FSDP training and inference concurrently. If you find this draft model useful, please give our project TorchSpec a star on [GitHub](https://github.com/torchspec-project/TorchSpec).

### Why an MLA (Multi-Latent Attention) Draft Model

Compared with an MHA draft model, the MLA variant is a better fit for Kimi-K2.6 deployment:

- Uses less KV cache, which reduces serving memory pressure.
- Matches Kimi-K2.6's MLA architecture, so it fits more naturally into the inference engine's KV-cache handling under different serving scenarios such as PD-Disaggregation.

### Training Setup

- **Cluster**: 3 nodes × 8× B200 (24 GPUs total)
- **Training**: 1 node (8 GPUs), FSDP
- **Inference**: 2 nodes (16 GPUs), vLLM (TP=8 per node)
- **Continual training**: Initialized from [kimi-k2.5-eagle3-mla](https://huggingface.co/lightseekorg/kimi-k2.5-eagle3-mla) checkpoint
- **Iterations**: 9,279 steps
- **Learning rate**: 2e-5, cosine schedule

## Performance

The primary metric is **accept_length** — the average number of tokens accepted per speculation step with `num_speculative_tokens=3`. Higher is better.

Benchmarks were run on vLLM 0.20.0 with 8× B200 GPUs.

| Category | Benchmark | N | Accept Length |
| --- | --- | --- | --- |
| Dialogue | [MTBench](https://github.com/lm-sys/FastChat/tree/main/fastchat/llm_judge) | 80 | 2.624 |
| Chinese | [CEval](https://huggingface.co/datasets/ceval/ceval-exam) | 212 | 2.494 |
| Math | [GSM8K](https://github.com/openai/grade-school-math) | 500 | 2.987 |
| Code | [HumanEval](https://huggingface.co/datasets/openai/openai_humaneval) | 164 | 3.241 |
| Math | [MATH500](https://huggingface.co/datasets/HuggingFaceH4/MATH-500) | 500 | 3.245 |
| Math | [AIME](https://huggingface.co/datasets/Maxwell-Jia/AIME_2024) | 30 | 2.982 |
| Code | [LiveCodeBench](https://huggingface.co/datasets/livecodebench/code_generation) | 200 | 2.706 |
| Code | [SPEED-Bench (coding)](https://huggingface.co/datasets/nvidia/SPEED-Bench) | 80 | 3.006 |

---

## Quick Start

### Requirements

- NVIDIA GPU with CUDA 12.0+
- [vLLM](https://github.com/vllm-project/vllm) >= 0.20.0

### Launch Server (vLLM)

```bash
vllm serve moonshotai/Kimi-K2.6 \
    --tensor-parallel-size 8 \
    --speculative-config '{"model": "lightseekorg/kimi-k2.6-eagle3-mla", "method": "eagle3", "num_speculative_tokens": 3}' \
    --trust-remote-code
```

### Launch Server (SGLang)

MLA Eagle3 draft model is not yet supported in SGLang. Will update once support is available.

## Citation

```bibtex
@misc{torchspec2026,
  title={TorchSpec: An Online Speculative Decoding Training Framework},
  url={https://github.com/torchspec-project/TorchSpec},
  year={2026}
}
```

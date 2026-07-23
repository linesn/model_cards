---
library_name: speculators
base_model:
- poolside/Laguna-XS-2.1
license: openmdw-1.1
tags:
- speculative-decoding
- dflash
- speculators
---

# poolside/Laguna-XS-2.1-DFlash

DFlash speculator for [poolside/Laguna-XS-2.1](https://huggingface.co/poolside/Laguna-XS-2.1).

## Model Specifications

| | |
|---|---|
| **Base Model** | poolside/Laguna-XS-2.1 |
| **Draft Architecture** | 5-layer Llama-style draft model (`DFlashLagunaForCausalLM`) |
| **Hidden Size** | 2048 |
| **Attention Heads** | 64 query / 8 key-value, head_dim 128 |
| **Sliding Window** | 512 |
| **Gating** | Per-head |
| **Proposals** | Up to 15 tokens per step |
| **Chat Template** | poolside/Laguna-XS-2.1 (use `/chat/completions` endpoint) |
| **Format** | Safetensors (BF16) |
| **License** | OpenMDW-1.1 |

## Deployment

> [!NOTE]
> DFlash speculative-decoding support for Laguna XS 2.1 has **not yet landed upstream**. Integrations are in progress:
> - **vLLM** — [vllm-project/vllm#46853](https://github.com/vllm-project/vllm/pull/46853)
> - **TRT-LLM** — [NVIDIA/TensorRT-LLM#15666](https://github.com/NVIDIA/TensorRT-LLM/pull/15666)
>
> See the "Speculative decoding (DFlash)" notes on the [Laguna XS 2.1 model card](https://huggingface.co/poolside/Laguna-XS-2.1) for current status.

Once vLLM support lands, pair this speculator with the base model by adding a `--speculative-config` block to the standard Laguna XS 2.1 serve command:

```bash
# Support in progress — see vllm-project/vllm#46853
vllm serve poolside/Laguna-XS-2.1 \
    --tool-call-parser poolside_v1 \
    --reasoning-parser poolside_v1 \
    --enable-auto-tool-choice \
    --default-chat-template-kwargs '{"enable_thinking": true}' \
    --speculative-config '{"model": "poolside/Laguna-XS-2.1-DFlash", "num_speculative_tokens": 15, "method": "dflash"}'
```

SGLang support:
```bash
sglang serve \
    --model-path poolside/Laguna-XS-2.1 \
    --speculative-algorithm DFLASH \
    --speculative-draft-model-path poolside/Laguna-XS-2.1-DFlash
```

## Evaluation

Speculative-decoding throughput and mean acceptance length for the (BF16) Laguna XS 2.1 target paired with this speculator (`num_speculative_tokens = 15`), versus the same model without speculative decoding:

| Dataset | Baseline (tok/s/seq) | DFlash (tok/s/seq) | Speedup | Acceptance length |
|---|---|---|---|---|
| GSM8K v2 | 80.22 | 133.78 | ×1.67 | 3.55 |
| HumanEval | 95.57 | 252.59 | ×2.64 | 4.57 |
| EvalPlus | 97.68 | 192.69 | ×1.97 | 4.10 |
| Math | 73.63 | 139.84 | ×1.90 | 4.40 |

## License

This model is licensed under the [OpenMDW-1.1 License](https://huggingface.co/poolside/Laguna-XS-2.1-DFlash/blob/main/LICENSE.md).

## Intended and Responsible Use 

Laguna-XS-2.1-DFlash is designed for software engineering and agentic coding use cases, and you are responsible for confirming that it is appropriate for your intended application. Laguna-XS-2.1-DFlash is subject to the [OpenMDW-1.1 License](https://huggingface.co/poolside/Laguna-XS-2.1-DFlash/blob/main/LICENSE.md), and should be used consistently with Poolside's [Acceptable Use Policy](https://poolside.ai/legal/acceptable-use-policy).

Please report security vulnerabilities or safety concerns to [security@poolside.ai](mailto:security@poolside.ai).

## References

- [DFlash: Block Diffusion for Flash Speculative Decoding](https://arxiv.org/abs/2602.06036)
---
library_name: vllm
inference: false
extra_gated_description: >-
  To learn more about how we process your personal data, please read our <a
  href="https://poolside.ai/legal/privacy">Privacy Policy</a>.
tags:
- laguna-m.1
- vllm
- sglang
- fp8
- moe
license: apache-2.0
pipeline_tag: text-generation
base_model:
- poolside/Laguna-M.1
---

<p align="center">
  <img alt="poolside-banner" src="https://poolside.ai/assets/laguna/laguna-m1-banner.svg" width="800px">
</p>

<p align="center">
  <a href="https://platform.poolside.ai"><strong>Get an API key</strong></a> ·
  <a href="https://poolside.ai/blog/laguna-a-deeper-dive"><strong>Release blog post</strong></a> ·
  <a href="https://poolside.ai/assets/laguna/laguna-m1-xs2-technical-report.pdf"><strong>Technical report</strong></a>
</p>

<br>

# Laguna M.1-FP8

Laguna M.1-FP8 is a 225B total parameter Mixture-of-Experts model with 23B activated parameters per token designed for agentic coding and long-horizon work. This is the FP8-quantized variant of [Laguna M.1](https://huggingface.co/poolside/Laguna-M.1).

> [!NOTE]
> This is the FP8 variant. The [BF16](https://huggingface.co/poolside/Laguna-M.1) and [NVFP4](https://huggingface.co/poolside/Laguna-M.1-NVFP4) variants are also available on Hugging Face.

## Highlights

* **Large sparse MoE for agentic coding**: Laguna M.1 is a 70-layer MoE transformer with 225B total parameters and 23B activated parameters per token
* **High-capacity expert routing**: After 3 dense SwiGLU layers, Laguna M.1 uses 67 sparse MoE layers with 256 experts, top-k=16 routing and auxiliary-loss-free load balancing
* **Global attention architecture**: Laguna M.1 uses global attention across all layers with 64 Q-heads, 8 KV-heads and softplus attention output gating
* **Native reasoning support**: Interleaved thinking between tool calls with support for enabling and disabling thinking per-request
* **Apache 2.0 license**: Use and modify freely for commercial and non-commercial purposes

---

## Model overview

- Training: pre-training, post-training and reinforcement learning stages
- Number of parameters: 225B total with 23B activated per token
- Optimizer: Muon
- Layers: 70 layers with global attention
- Experts: 256 experts with 1 shared expert; top-k=16 routing
- Dense layers: first 3 layers are dense SwiGLU; remaining 67 layers are sparse MoE
- Attention: 64 Q-heads, 8 KV-heads, head dimension 128, with softplus attention output gating
- Positional encoding: RoPE with YaRN
- Modality: text-to-text
- Context window: 262,144 tokens
- Reasoning support: interleaved thinking with preserved thinking
- Quantization: FP8 (weights), detected automatically from `quantization_config`

## Benchmark results

<p align="center">
  <img alt="benchmarks" src="https://poolside.ai/assets/laguna/laguna-m1-chart.svg" width="800px">
</p>

| Model                     | Parameters           | SWE-bench Verified | SWE-bench Multilingual | SWE-bench Pro (Public Dataset) | Terminal-Bench 2.0 |
|---------------------------|----------------------|--------------------|------------------------|--------------------------------|--------------------|
| **Laguna M.1 (BF16)**     | 225B-A23B            | 74.6%              | 63.1%                  | 49.2%                          | 45.8%              |
| Devstral 2                | 123B dense           | 72.2%              | 61.3%                  | -                              | 32.6%              |
| GLM-4.7                   | 355B-A32B            | 73.8%              | 66.7%                  | -                              | 41.0%              |
| DeepSeek-V4 Flash         | 284B-A13B            | 79.0%              | 73.3%                  | 52.6%                          | 56.9%              |
| Qwen3.5-397B-A17B         | 397B-A17B            | 76.2%              | 69.3%                  | 50.9%                          | 52.5%              |
| Claude Sonnet 4.6         | -                    | 79.6%              | -                      | -                              | 59.1%              |

*Scores shown are for the BF16 reference model; see the main [Laguna M.1 model card](https://huggingface.co/poolside/Laguna-M.1) for full benchmarking methodology. We used the highest publicly-referenced scores for all comparison models across each benchmark.*

## Usage

Laguna M.1 has upstream support in vLLM, SGLang, and TRT-LLM thanks to the support of the team at NVIDIA.

> [!NOTE]
> For complete usage instructions, see the main [Laguna M.1 model card](https://huggingface.co/poolside/Laguna-M.1).

### Deployment

#### vLLM

The full vLLM recipe is on the main [Laguna M.1 model card](https://huggingface.co/poolside/Laguna-M.1). Quantization is detected automatically from `quantization_config` in this checkpoint, so the same command works with `poolside/Laguna-M.1-FP8` substituted for the model ID. Set `VLLM_BLOCKSCALE_FP8_GEMM_FLASHINFER=0` when serving with vLLM.

```shell
pip install 'vllm>=0.21.0'

export VLLM_BLOCKSCALE_FP8_GEMM_FLASHINFER=0

vllm serve \
    --model poolside/Laguna-M.1-FP8 \
    --tool-call-parser poolside_v1 \
    --reasoning-parser poolside_v1 \
    --enable-auto-tool-choice \
    --served-model-name laguna \
    --default-chat-template-kwargs '{"enable_thinking": true}'
```

#### SGLang

The full SGLang recipe is on the [SGLang Cookbook](https://docs.sglang.io/cookbook/autoregressive/Poolside/Laguna-M.1). Quantization is detected automatically, so no extra flags are required. 
```shell
git clone https://github.com/sgl-project/sglang.git
cd sglang
pip install -e "python[all]"

sglang serve \
    --model-path poolside/Laguna-M.1-FP8 \
    --trust-remote-code \
    --reasoning-parser poolside_v1 \
    --tool-call-parser poolside_v1 \
    --tp 8 \
    --host 0.0.0.0 \
    --port 30000
```
#### TRT-LLM

Laguna is supported in TensorRT-LLM thanks to the team at NVIDIA ([NVIDIA/TensorRT-LLM#13559](https://github.com/NVIDIA/TensorRT-LLM/pull/13559), with partial-RoPE fusion in [#15110](https://github.com/NVIDIA/TensorRT-LLM/pull/15110)). The full recipe is on the main [Laguna M.1 model card](https://huggingface.co/poolside/Laguna-M.1). Quantization is detected automatically from `quantization_config` in this checkpoint, so no extra flags are required.

## Controlling reasoning

Laguna M.1 has native reasoning support and is designed to work best with *preserved thinking*, where `reasoning` content from prior assistant messages is preserved in the message history. This model will generally reason before calling tools and between tool calls. See the main [Laguna M.1 model card](https://huggingface.co/poolside/Laguna-M.1#controlling-reasoning) for streaming, tool-call, and preserved-thinking examples.

### Disabling reasoning

You can disable thinking by setting `enable_thinking` to `False` in a request or by not providing `--default-chat-template-kwargs {"enable_thinking": True}` or equivalent when starting the server.

## License

This model is licensed under the [Apache 2.0 License](https://huggingface.co/poolside/Laguna-M.1-FP8/blob/main/LICENSE.md).

## Intended and Responsible Use

Laguna M.1 is designed for software engineering and agentic coding use cases, and you are responsible for confirming that it is appropriate for your intended application. Laguna M.1 is subject to the [Apache 2.0 License](https://huggingface.co/poolside/Laguna-M.1-FP8/blob/main/LICENSE.md), and should be used consistently with Poolside's [Acceptable Use Policy](https://poolside.ai/legal/acceptable-use-policy). We advise against circumventing Laguna M.1 safety guardrails without implementing substantially equivalent mitigations appropriate for your use case.

Please report security vulnerabilities or safety concerns to [security@poolside.ai](mailto:security@poolside.ai).

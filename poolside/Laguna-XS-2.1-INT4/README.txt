---
library_name: vllm
inference: false
extra_gated_description: >-
  To learn more about how we process your personal data, please read our <a
  href="https://poolside.ai/legal/privacy">Privacy Policy</a>.
tags:
- laguna-xs-2.1
license: openmdw-1.1
pipeline_tag: text-generation
base_model:
- poolside/Laguna-XS-2.1
---

<p align="center">
  <img alt="poolside-banner" src="https://poolside.ai/assets/laguna/laguna-xs2-1-banner.svg" width="800px">
</p>

<p align="center">
  <a href="https://openrouter.ai/poolside/laguna-xs-2.1"><strong>Use on OpenRouter</strong></a> ·
  <a href="https://poolside.ai/blog/introducing-laguna-xs-2-1"><strong>Release blog post</strong></a>
</p>

<br>

# Laguna XS 2.1-INT4
Laguna XS 2.1-INT4 is a 33B total parameter Mixture-of-Experts model with 3B activated parameters per token designed for agentic coding and long-horizon work on a local machine. It uses Sliding Window Attention with per-head gating in 30 out of 40 layers for fast inference and low KV cache requirements.

> [!NOTE]
> This is the INT4 variant with an FP8-quantized KV cache. The [BF16](https://huggingface.co/poolside/Laguna-XS-2.1), [FP8](https://huggingface.co/poolside/Laguna-XS-2.1-FP8) and [NVFP4](https://huggingface.co/poolside/Laguna-XS-2.1-NVFP4) variants are also available on Hugging Face.

## Highlights
- **Mixed SWA and global attention layout**: Laguna XS 2.1 uses sigmoid gating with per-layer rotary scales, enabling mixed SWA (Sliding Window Attention) and global attention layers in a 3:1 ratio (across 40 total layers)
- **KV cache in FP8**: KV cache quantized to FP8, reducing memory per token
- **Native reasoning support**: Interleaved thinking between tool calls with support for enabling and disabling thinking per-request
- **Local-ready**: At 33B total parameters and 3B activated, Laguna XS 2.1 is compact enough to run on a Mac with 36 GB of RAM. Available on [Ollama](https://ollama.com/library/laguna-xs-2.1) and [llama.cpp](https://github.com/ggml-org/llama.cpp/pull/25165) (BF16 and Q4\_K\_M only)
- **OpenMDW-1.1 license**: Use and modify the model and associated materials freely for commercial and non-commercial purposes ([learn more about OpenMDW](https://openmdw.ai/))

---

## Model overview

- Training: pre-training, post-training and reinforcement learning stages
- Number of parameters: 33B total with 3B activated per token
- Optimizer: Muon
- Layers: 40 layers (10 layers with global attention, 30 layers with sliding window attention)
- Experts: 256 experts with 1 shared expert
- Sliding Window: 512 tokens
- Modality: text-to-text
- Context window: 262,144 tokens
- Reasoning support: interleaved thinking with preserved thinking

## Benchmark results

<p align="center">
  <img alt="benchmarks" src="https://poolside.ai/assets/laguna/laguna-xs2-1-chart.svg" width="800px">
</p>

| Model                     | Size (total params.) | SWE-bench Verified | SWE-bench Multilingual | SWE-Bench Pro (Public Dataset) | Terminal-Bench 2.0 |
|---------------------------|----------------------|--------------------|------------------------|--------------------------------|--------------------|
| **Laguna XS 2.1**         | 33B                  | 70.9%              | 63.1%                  | 47.6%                          | 37.5%              |
| **Laguna XS.2**           | 33B                  | 69.9%              | 57.7%                  | 46.3%                          | 35.7%              |
| Qwen3.6-35B-A3B           | 35B                  | 73.4%              | 67.2%                  | 49.5%                          | 51.5%              |
| North Mini Code           | 30B                  | 67.6%              | -                      | 40.2%                          | 36.0%              |
| MAI-Code-1-Flash          | 137B                 | 71.6%              | 65.5%                  | 51.2%                          | 54.8%              |
| gpt-oss-120B              | 120B                 | -                  | -                      | 16.2%                          | 18.7%              |
| Claude Haiku 4.5          | -                    | 73.3%              | -                      | 39.5%                          | 29.8%              |
| GPT-5.4 Nano              | -                    | -                  | -                      | 52.4%                          | 46.3%              |

*We used the highest publicly-referenced scores for all comparison models across each benchmark. In all cases these were official scores published in release blog posts or equivalent, with the exception of gpt-oss-120b and Claude Haiku 4.5 where the highest published (verified) scores for SWE-Bench Pro and Terminal-Bench 2.0 are from their respective official leaderboards.*

<details>
<summary>Expand for benchmarking methodology</summary>

All benchmarking for Laguna XS 2.1 was completed using Laude Institute’s Harbor Framework with our [agent harness](https://github.com/poolsideai/pool), with a maximum of 500 steps and sandboxed execution. The same sampling parameters were used for all Laguna XS 2.1 benchmarking: temperature=1.0, top_k=20 and top_p=1, with thinking mode enabled and a context length of 256K tokens. All tasks were run in their own sandbox using 8 GB RAM/2 CPUs, with the exception of Terminal-Bench 2.0, which used 48 GB RAM/32 CPUs.

Some base task images and verifiers were patched to fix infrastructure reliability issues inherent in task setup, such as rate limits on third-party dependencies in external registries used by the verifier. All four agentic benchmarks were run with patched images. We also ran a reward-hack judge post-hoc on Laguna XS 2.1 evaluation runs and did not find significant reward hacking after joint judge review and manual review.

- SWE-bench Verified: mean pass@1 averaged over 4 attempts per task
- SWE-bench Multilingual: mean pass@1 averaged over 4 attempts per task
- SWE-Bench Pro: mean pass@1 averaged over 2 attempts per task
- Terminal-Bench 2.0: mean pass@1 averaged over 5 attempts per task; 48 GB RAM/32 CPUs

</details>

### Quantization quality

Laguna XS 2.1-INT4 was evaluated against the unquantized BF16 checkpoint on the same four agentic benchmarks. Scores are mean pass@1; the ± figure is the run-to-run variation and *RH* is the share of runs flagged by our post-hoc reward-hack judge (see the benchmarking methodology above).

| Benchmark | Laguna XS 2.1 (BF16) | Laguna XS 2.1-INT4 |
| --- | --- | --- |
| SWE-bench Verified | 70.85% ± 0.85% (6.51% RH) | 71.70% ± 0.88% (5.91% RH) |
| SWE-bench Multilingual | 63.17% ± 1.42% (7.25% RH) | 63.42% ± 1.37% (7.45% RH) |
| SWE-Bench Pro (Public Dataset) | 47.61% ± 0.96% (2.40% RH) | 48.70% ± 0.89% (3.29% RH) |
| Terminal-Bench 2.0 | 37.53% ± 2.81% (2.12% RH) | 37.08% ± 2.70% (3.04% RH) |

## Usage

Laguna XS 2.1-INT4 has launch-day support in vLLM and Transformers.

> [!NOTE]
> For complete usage instructions, see the main [Laguna XS 2.1 model card](https://huggingface.co/poolside/Laguna-XS-2.1).

### Local deployment

Laguna XS 2.1-INT4 is supported in vLLM and Transformers. Use Laguna XS 2.1 with Ollama (with MLX support) or Llama.cpp (BF16 and Q4\_K\_M only) for the best results on your local machine.

#### vLLM

The full vLLM recipe is on the main [Laguna XS 2.1 model card](https://huggingface.co/poolside/Laguna-XS-2.1) and on the [vLLM recipes page](https://recipes.vllm.ai/poolside/Laguna-XS-2.1). Quantization is detected automatically from `quantization_config` in this checkpoint, so the same command works with `poolside/Laguna-XS-2.1-INT4` substituted for the model ID. No extra flags required.

> [!IMPORTANT]
> INT4 support landed in vLLM with [vllm-project/vllm#47154](https://github.com/vllm-project/vllm/pull/47154). This checkpoint mixes INT4 and group-quantized INT8 experts, which earlier builds rejected in the Marlin WNA16 MoE path. Use a vLLM build that includes this fix.

> [!IMPORTANT]
> Tool calling requires a vLLM build with [vllm-project/vllm#47311](https://github.com/vllm-project/vllm/pull/47311); on older builds pass `--tool-call-parser glm47` (the GLM 4.7 parser) instead of `poolside_v1`.

> [!NOTE]
> The FP8-quantized KV cache requires vLLM >= 0.22.0. Earlier versions produce scrambled output on non-Hopper GPUs because of a per-layer attention-head count bug, fixed in [vllm#42650](https://github.com/vllm-project/vllm/pull/42650). On older vLLM, disable the FP8 KV cache by adding `--kv-cache-dtype-skip-layers $(seq 0 39)`.

#### SGLang

The full SGLang recipe is on the main [Laguna XS 2.1 model card](https://huggingface.co/poolside/Laguna-XS-2.1) and on the [SGLang cookbook](https://docs.sglang.io/cookbook/autoregressive/Poolside/Laguna-XS-2.1). SGLang reads the checkpoint quantization_config, so you can use the same launch command after replacing the model ID


#### Transformers

The full Transformers recipe is on the main [Laguna XS 2.1 model card](https://huggingface.co/poolside/Laguna-XS-2.1). Substitute `poolside/Laguna-XS-2.1-INT4` for the model ID; quantization is detected automatically from `quantization_config`.

#### Ollama

Available on the [Ollama library](https://ollama.com/library/laguna-xs-2.1).

> [!NOTE]
> **macOS (Metal) users:** Chat (`ollama run` / `/api/chat`) works as expected on Linux/CUDA. On macOS/Metal it may currently return empty output; the root cause is not yet fully understood and we're investigating it with the Ollama team. On a Mac, use a Linux/CUDA host, or the `/api/generate` endpoint with `"raw": true`.

## Controlling reasoning

Laguna XS 2.1-INT4 uses the same reasoning controls (interleaved thinking, preserved reasoning, and the `enable_thinking` flag) as the base model. See the [Controlling reasoning](https://huggingface.co/poolside/Laguna-XS-2.1#controlling-reasoning) section of the main Laguna XS 2.1 model card.

## License

This model is licensed under the [OpenMDW-1.1 License](https://huggingface.co/poolside/Laguna-XS-2.1-INT4/blob/main/LICENSE.md).

## Intended and Responsible Use 

Laguna XS 2.1-INT4 is designed for software engineering and agentic coding use cases, and you are responsible for confirming that it is appropriate for your intended application. Laguna XS 2.1-INT4 is subject to the [OpenMDW-1.1 License](https://huggingface.co/poolside/Laguna-XS-2.1-INT4/blob/main/LICENSE.md), and should be used consistently with Poolside's [Acceptable Use Policy](https://poolside.ai/legal/acceptable-use-policy). We advise against circumventing Laguna XS 2.1-INT4 safety guardrails without implementing substantially equivalent mitigations appropriate for your use case.

Please report security vulnerabilities or safety concerns to [security@poolside.ai](mailto:security@poolside.ai).
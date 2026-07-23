---
library_name: vllm
inference: false
extra_gated_description: >-
  To learn more about how we process your personal data, please read our <a
  href="https://poolside.ai/legal/privacy">Privacy Policy</a>.
tags:
- laguna-xs.2
license: apache-2.0
pipeline_tag: text-generation
base_model:
- poolside/Laguna-XS.2
---

<p align="center">
  <img alt="poolside-banner" src="https://poolside.ai/assets/laguna/laguna-xs2-banner.svg" width="800px">
</p>

<p align="center">
  <a href="https://shimmer.poolside.ai"><strong>Try Laguna XS.2 in Shimmer</strong></a> ·
  <a href="https://platform.poolside.ai"><strong>Get an API key</strong></a> ·
  <a href="https://poolside.ai/blog/laguna-a-deeper-dive"><strong>Release blog post</strong></a>
</p>

<br>

# Laguna XS.2-INT4
Laguna XS.2-INT4 is a 33B total parameter Mixture-of-Experts model with 3B activated parameters per token designed for agentic coding and long-horizon work on a local machine. It uses Sliding Window Attention with per-head gating in 30 out of 40 layers for fast inference and low KV cache requirements.

> [!NOTE]
> This is the INT4 variant with an FP8-quantized KV cache. The [BF16](https://huggingface.co/poolside/Laguna-XS.2), [FP8](https://huggingface.co/poolside/Laguna-XS.2-FP8) and [NVFP4](https://huggingface.co/poolside/Laguna-XS.2-NVFP4) variants are also available on Hugging Face.

## Highlights
- **Mixed SWA and global attention layout**: Laguna XS.2 uses sigmoid gating with per-layer rotary scales, enabling mixed SWA (Sliding Window Attention) and global attention layers in a 3:1 ratio (across 40 total layers)
- **KV cache in FP8**: KV cache quantized to FP8, reducing memory per token
- **Native reasoning support**: Interleaved thinking between tool calls with support for enabling and disabling thinking per-request
- **Local-ready**: At 33B total parameters and 3B activated, Laguna XS.2 is compact enough to run on a Mac with 36 GB of RAM. [Available on Ollama](https://ollama.com/library/laguna-xs.2)
- **Apache 2.0 license**: Use and modify freely for commercial and non-commercial purposes

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
  <img alt="benchmarks" src="https://poolside.ai/assets/laguna/laguna-xs2-chart.svg" width="800px">
</p>

| Model                     | Size (total params.) | SWE-bench Verified | SWE-bench Multilingual | SWE-bench Pro (Public Dataset) | Terminal-Bench 2.0 |
|---------------------------|----------------------|--------------------|------------------------|--------------------------------|--------------------|
| **Laguna XS.2 (BF16)**    | 33B                  | 69.9%              | 57.7%                  | 46.3%                          | 35.7%              |
| Devstral Small 2          | 24B dense            | 68.0%              | 55.7%                  | -                              | 22.5%              |
| Gemma 4 31B IT            | 31B dense            | 52.0%              | 51.7%                  | 35.7%                          | 42.9%              |
| Qwen3.5-35B-A3B           | 35B                  | 69.2%              | 60.3%                  | 44.6%                          | 40.5%              |
| Qwen3.6-35B-A3B           | 35B                  | 73.4%              | 67.2%                  | 49.5%                          | 51.5%              |
| Claude Haiku 4.5          | -                    | 73.3%              | -                      | 39.5%                          | 29.8%              |
| GPT-5.4 Nano              | -                    | -                  | -                      | 52.4%                          | 46.3%              |

*We used the highest publicly-referenced scores for all comparison models across each benchmark. In almost all cases these were official scores published in release blog posts or equivalent, with the exception of Gemma 4 31B IT where the highest published scores were [reported by the Qwen team](https://qwen.ai/blog?id=qwen3.6-35b-a3b) and Claude Haiku 4.5 where the highest published (verified) scores for SWE-bench Pro and Terminal-Bench 2.0 are from their respective official leaderboards.*

<details>
<summary>Expand for benchmarking methodology</summary>

All benchmarking for Laguna XS.2 was completed using the Laude Institute’s Harbor Framework with our [agent harness](https://github.com/poolsideai/pool), using a maximum of 500 steps and sandboxed execution using 8 GB RAM/2 CPUs (with the exception of Terminal-Bench 2.0; see below). The same sampling parameters were used for all benchmarking: temperature=0.7 and top_k=20.  Some base task images and verifiers were patched to fix infrastructure reliability issues inherent in task setup, such as rate limits on third-party dependencies in external registries used by the verifier. More details outlining these updates and other findings will follow in a future technical blog post.

- SWE-bench Verified: mean pass@1 averaged over 4 runs.
- SWE-bench Multilingual: mean pass@1 averaged over 7 runs.
- SWE-bench Pro: mean pass@1 averaged over 3 runs.
- Terminal-Bench 2.0: mean pass@1 averaged over 5 runs. 48GB RAM/32 CPUs.

</details>

## Usage

Laguna XS.2-INT4 has launch-day support in vLLM and Transformers.

The fastest way to get started is with our API, directly or using OpenRouter.

> [!NOTE]
> For complete usage instructions, see the main [Laguna XS.2 model card](https://huggingface.co/poolside/Laguna-XS.2).

### Local deployment

Laguna XS.2-INT4 is supported in vLLM and Transformers. Use Laguna-XS.2 with Ollama (with MLX support) and the mlx-lm framework for the best experience on your local machine.

#### vLLM

The full vLLM recipe is on the main [Laguna XS.2 model card](https://huggingface.co/poolside/Laguna-XS.2) and on the [vLLM recipes page](https://recipes.vllm.ai/poolside/Laguna-XS.2). Quantization is detected automatically from `quantization_config` in this checkpoint, so the same command works with `poolside/Laguna-XS.2-INT4` substituted for the model ID. No extra flags required.

> [!IMPORTANT]
> INT4 support landed in vLLM with [vllm-project/vllm#47154](https://github.com/vllm-project/vllm/pull/47154). This checkpoint mixes INT4 and group-quantized INT8 experts, which earlier builds rejected in the Marlin WNA16 MoE path. Use a vLLM build that includes this fix.

> [!NOTE]
> The FP8-quantized KV cache requires vLLM >= 0.22.0. Earlier versions produce scrambled output on non-Hopper GPUs because of a per-layer attention-head count bug, fixed in [vllm#42650](https://github.com/vllm-project/vllm/pull/42650). On older vLLM, disable the FP8 KV cache by adding `--kv-cache-dtype-skip-layers $(seq 0 39)`.

#### Transformers

The full Transformers recipe is on the main [Laguna XS.2 model card](https://huggingface.co/poolside/Laguna-XS.2). Substitute `poolside/Laguna-XS.2-INT4` for the model ID; quantization is detected automatically from `quantization_config`.

#### Ollama

Visit [Ollama's model library](https://ollama.com/library/laguna-xs.2) to pull to your local machine.

## Controlling reasoning

Laguna XS.2 has native reasoning support and is designed to work best with *preserved thinking*, where `reasoning` content from prior assistant messages is preserved in the message history. This model will generally reason before calling tools and between tool calls.

<details>
<summary>Expand for example</summary>

```python
import json
from openai import OpenAI

client = OpenAI(
  base_url="https://inference.poolside.ai/v1",
  api_key="...",
)

model = "poolside/laguna-xs.2"

tools = [{"type": "function", "function": {
  "name": "shell",
  "description": "Execute a bash command and return the output.",
  "parameters": {"type": "object", "properties": {"cmd": {"type": "string"}}, "required": ["cmd"]},
}}]

messages = [
  {"role": "system", "content": "You are a coding agent with access to a shell tool."},
  {"role": "user", "content": "Run uname -a"},
]

# Thinking is enabled by default when the server sets --default-chat-template-kwargs {"enable_thinking": True}
# When using the Poolside API (https://inference.poolside.ai/v1), this flag is set by default
response = client.chat.completions.create(
  model=model,
  messages=messages,
  tools=tools,
  stream=True,
)

reasoning, content, tool_calls = "", "", []
for chunk in response:
  delta = chunk.choices[0].delta
  if hasattr(delta, "reasoning_content") and delta.reasoning_content:
    reasoning += delta.reasoning_content
  if hasattr(delta, "content") and delta.content:
    content += delta.content
  if hasattr(delta, "tool_calls") and delta.tool_calls:
    for tc in delta.tool_calls:
      if tc.index >= len(tool_calls):
        tool_calls.append({"id": tc.id, "function": {"name": "", "arguments": ""}})
      if tc.function.name:
        tool_calls[tc.index]["function"]["name"] = tc.function.name
      if tc.function.arguments:
        tool_calls[tc.index]["function"]["arguments"] += tc.function.arguments

print(f"Reasoning: {reasoning}\nContent: {content}\nTool calls: {tool_calls}\n")

# Return reasoning in the next request for best performance
messages.append({
  "role": "assistant",
  "content": content,
  "reasoning_content": reasoning,
  "tool_calls": [{"id": tc["id"], "type": "function", "function": tc["function"]} for tc in tool_calls]
})

messages.append({
  "role": "tool",
  "tool_call_id": tool_calls[0]["id"],
  "content": json.dumps({"stdout": "Darwin arm64", "exit_code": "0"})
})

response = client.chat.completions.create(
  model=model,
  messages=messages,
  tools=tools,
  stream=True,
)

reasoning, content = "", ""
for chunk in response:
  delta = chunk.choices[0].delta
  if hasattr(delta, "reasoning_content") and delta.reasoning_content:
    reasoning += delta.reasoning_content
  if hasattr(delta, "content") and delta.content:
    content += delta.content

print(f"Reasoning: {reasoning}\nContent: {content}")
```

</details>

### Disabling reasoning

You can disable thinking by setting `enable_thinking` to `False` in a request or by not providing `--default-chat-template-kwargs {"enable_thinking": True}` or equivalent when starting the server.

<details>
<summary>Expand for example</summary>

```python
from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="poolside/laguna-xs.2",
  messages=[
    {"role": "user", "content": "Write a retry wrapper with exponential backoff."}
  ],
  extra_body={
    "chat_template_kwargs": { "enable_thinking": False },
  },
  stream=True
)

for chunk in completion:
    print(chunk.choices[0].delta)
```

</details>

For agentic coding use cases, we recommend enabling thinking and preserving reasoning in message history as outlined in the [Controlling reasoning] section.

## License

This model is licensed under the [Apache 2.0 License](https://huggingface.co/poolside/Laguna-XS.2-INT4/blob/main/LICENSE.md).

## Intended and Responsible Use 

Laguna XS.2-INT4 is designed for software engineering and agentic coding use cases, and you are responsible for confirming that it is appropriate for your intended application. Laguna XS.2-INT4 is subject to the [Apache 2.0 License](https://huggingface.co/poolside/Laguna-XS.2-INT4/blob/main/LICENSE.md), and should be used consistently with Poolside's [Acceptable Use Policy](https://poolside.ai/legal/acceptable-use-policy). We advise against circumventing Laguna XS.2-INT4 safety guardrails without implementing substantially equivalent mitigations appropriate for your use case.

Please report security vulnerabilities or safety concerns to [security@poolside.ai](mailto:security@poolside.ai).
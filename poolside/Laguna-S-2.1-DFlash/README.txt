---
license: other
tags:
- dflash
- speculative-decoding
- laguna
base_model:
- poolside/Laguna-S-2.1
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

# Laguna-S-2.1-DFlash

DFlash speculator (draft model) for
[Laguna S 2.1](https://huggingface.co/poolside/Laguna-S-2.1), bf16.

- Architecture: `DFlashLagunaForCausalLM` (6 sliding-attention layers, block_size 16).
- Shares token embedding + lm_head with the target; `draft_vocab_size == vocab_size` (no d2t/t2d).
- Loads under vLLM (native `laguna_dflash`) and TRT-LLM (pytorch DFlash backend) as the draft model in a speculative config.

## Usage

### vLLM

```shell
vllm serve --model poolside/Laguna-S-2.1 \
    --speculative-config '{"model":"poolside/Laguna-S-2.1-DFlash","num_speculative_tokens":7,"method":"dflash"}' \
    ...
```

### SGLang

```shell
python -m sglang.launch_server --model-path poolside/Laguna-S-2.1 \
  --speculative-algorithm DFLASH \
  --speculative-draft-model-path poolside/Laguna-S-2.1-DFlash \
  ...
```

### llama.cpp (GGUF)

A llama.cpp conversion of this draft model (`laguna-s-2.1-DFlash-BF16.gguf`) is
published in
[poolside/Laguna-S-2.1-GGUF](https://huggingface.co/poolside/Laguna-S-2.1-GGUF)
alongside the target GGUFs. It embeds the target tokenizer and the DFlash metadata
(`dflash.decoder_arch = laguna`, capture layers, block size), so it works directly
as the `-md` draft model:

```shell
git clone --branch laguna https://github.com/poolsideai/llama.cpp
cd llama.cpp && cmake -B build && cmake --build build -j

./build/bin/llama-server \
  -m laguna-s-2.1-Q4_K_M.gguf \
  -md laguna-s-2.1-DFlash-BF16.gguf \
  --spec-type draft-dflash --spec-draft-n-max 15 \
  -fa on --jinja --port 8000
```

`--spec-draft-n-max` is clamped to the trained block size (15 draft tokens + 1).

> [!NOTE]
> Requires Poolside's llama.cpp fork, branch
> [`laguna`](https://github.com/poolsideai/llama.cpp/tree/laguna). Upstream
> llama.cpp ships the generic DFlash framework but not the Laguna decoder
> contract this draft model needs, and upstream PR
> [ggml-org/llama.cpp#25165](https://github.com/ggml-org/llama.cpp/pull/25165)
> covers the target architecture only.

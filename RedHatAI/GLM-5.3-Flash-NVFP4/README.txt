---
base_model:
- zai-org/GLM-5.3-Flash
tags:
- vllm
- llm-compressor
- nvfp4
- fp4
- glm5_next
pipeline_tag: image-text-to-text
library_name: transformers
---

# RedHatAI/GLM-5.3-Flash-NVFP4
This model is a quantized version of [zai-org/GLM-5.3-Flash](https://huggingface.co/zai-org/GLM-5.3-Flash).

# Model Optimizations
This model was obtained by quantizing the weights of zai-org/GLM-5.3-Flash to NVFP4, ready for inference with vLLM. 

Weights are quantized to FP4 with a group size of 16, and activations are quantized to FP4 with local per-group scaling. Only the weights and activations of the linear operators within transformer blocks are quantized using [LLM Compressor](https://github.com/vllm-project/llm-compressor). Vision tower, embedding, and output head layers are kept in their original precision.

# vLLM Serving

```bash
docker run --gpus all \
  --privileged --ipc=host -p 8000:8000 \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  -e VLLM_ENGINE_READY_TIMEOUT_S=3600 \
  vllm/vllm-openai:glm53-flash RedHatAI/GLM-5.3-Flash-NVFP4 \
  --tensor-parallel-size 4 \
  --no-enable-flashinfer-autotune \
  --tool-call-parser glm47 \
  --enable-auto-tool-choice \
  --reasoning-parser glm45
```

## Enable Speculative Decoding 

```
docker run --gpus all \
  --privileged --ipc=host -p 8000:8000 \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  -e VLLM_ENGINE_READY_TIMEOUT_S=3600 \
  -e PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
  vllm/vllm-openai:glm53-flash RedHatAI/GLM-5.3-Flash-NVFP4 \
  --tensor-parallel-size 4 \
  --no-enable-flashinfer-autotune \
  --tool-call-parser glm47 \
  --enable-auto-tool-choice \
  --reasoning-parser glm45 \
  --gpu-memory-utilization 0.85 \
  --disable-custom-all-reduce \
  --speculative-config '{"method":"mtp","num_speculative_tokens":5}'
```

# Evaluations 

| Benchmark | Metric | Avg Score |
|---|---|---|
| GPQA Diamond | `gpqa_pass@k:k=1` (3 seeds) | **90.57%** |
| AIME25 | `pass@k:k=1&n=1` (8 seeds) | **86.67%** |
| GSM8K Platinum CoT | `exact_match,strict-match` (3 seeds) | **97.74%** |
| MATH-500           | `pass@k:k=1&n=1` (3 seeds)           | **94.87%** |
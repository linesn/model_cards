---
base_model:
- moonshotai/Kimi-K2.6
tags:
- kimi
- nvfp4
- vllm
- compressed-tensors
name: RedHatAI/Kimi-K2.6-NVFP4
---

# NVFP4-Quantized RedHatAI/Kimi-K2.6-NVFP4

This is a preliminary version (and subject to change) of NVFP4-quantized [moonshotai/Kimi-K2.6](https://huggingface.co/Kimi/Kimi-K2.6) model, for performant inference on NVIDIA Blackwell GPUs. 
The model has both weights and activations quantized in NVFP4 format with [vllm-project/llm-compressor](https://github.com/vllm-project/llm-compressor).

It is compatible and tested against vllm v0.20.0. Deploy it via `vllm serve` using the recipes at https://recipes.vllm.ai/moonshotai/Kimi-K2.6.

# Creation Script:

<!-- Run this script with LLM Compressor main and latest transformers. -->
Kimi K2.6 support will land in https://github.com/vllm-project/llm-compressor/pull/2662. The script to create will be posted as a link shortly


# Preliminary Evaluations

1) GSM8K Platinum:
```
lm_eval --model local-chat-completions \
  --tasks gsm8k_platinum_cot_llama \
  --model_args "model=RedHatAI/Kimi-K2.6-NVFP4,max_length=262144,base_url=http://0.0.0.0:8000/v1/chat/completions,num_concurrent=128,max_retries=3,tokenized_requests=False,tokenizer_backend=None,timeout=1200" \
  --num_fewshot 0 \
  --apply_chat_template \
  --gen_kwargs "do_sample=True,temperature=1.0,top_p=0.95,top_k=20,min_p=0.0,max_gen_toks=64000,presence_penalty=1.5,repetition_penalty=1.0,seed=5678"

```

Recovery:

|          | moonshotai/Kimi-K2.6<br> (original in W4A16) | RedHatAI/Kimi-K2.6-NVFP4<br> (this model) |
| -------- | :--------------------: | :------------------------------------: |
| Accuracy<br>  | 94.29               | 93.96                             |
| Recovery | \-                     | 99.6%                                  |


**Note**: More rigorous evaluations are currently in progress and will be available soon.



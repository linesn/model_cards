---
base_model:
- Qwen/Qwen3.8-27B
tags:
- vllm
- llm-compressor
- qwen3_5
- compressed-tensors
- int4
- conversational
license: apache-2.0
pipeline_tag: image-text-to-text
library_name: transformers
---

# RedHatAI/Qwen3.8-27B-INT4

This model is a quantized version of [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B).

### Model Optimizations

This model was obtained by quantizing the weights of [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) to int4, ready for inference with vLLM.
Weights are quantized to int4 with a group size of 128. Only the weights of the linear operators within transformer blocks are quantized using [LLM Compressor](https://github.com/vllm-project/llm-compressor). Vision tower and outputhead layers are kept in their original precision.


# Creation Code

```python
import torch
from compressed_tensors.quantization.quant_scheme import W4A16, QuantizationScheme
from datasets import load_dataset
from transformers import AutoProcessor, Qwen3_5ForConditionalGeneration

from llmcompressor import oneshot
from llmcompressor.modifiers.gptq import GPTQModifier
from llmcompressor.modifiers.transform.awq import AWQModifier
from llmcompressor.utils import load_context

MODEL_ID = "Qwen/Qwen3.8-27B"

# Load model.
with load_context(Qwen3_5ForConditionalGeneration):
    model = Qwen3_5ForConditionalGeneration.from_pretrained(MODEL_ID)
processor = AutoProcessor.from_pretrained(MODEL_ID)


recipe = [
    AWQModifier(duo_scaling="both"),
    GPTQModifier(
        targets="Linear", 
        scheme="W4A16",
        ignore=[
            "re:visual.*",
            "re:model.visual.*",
            r"re:.*lm_head",
            "re:.*embed_tokens$",
            r"re:.*linear_attn\.in_proj_a$",
            r"re:.*linear_attn\.in_proj_b$",
        ],
    )
]

NUM_CALIBRATION_SAMPLES = 512
MAX_SEQUENCE_LENGTH = 4096

ds = load_dataset(
    "mlabonne/open-perfectblend",
    split=f"train[:{NUM_CALIBRATION_SAMPLES}]",
)
ds = ds.shuffle(seed=42)

ROLE_MAP = {"human": "user", "gpt": "assistant"}


def preprocess_function(example):
    messages = [
        {
            "role": ROLE_MAP.get(msg["from"], msg["from"]),
            "content": [{"type": "text", "text": msg["value"]}],
        }
        for msg in example["conversations"]
    ]
    return processor.apply_chat_template(
        messages,
        tokenize=True,
        return_dict=True,
        add_generation_prompt=False,
        processor_kwargs={
            "return_tensors": "pt",
            "padding": False,
            "truncation": True,
            "max_length": MAX_SEQUENCE_LENGTH,
            "add_special_tokens": False,
        },
    )


ds = ds.map(preprocess_function, batched=False, remove_columns=ds.column_names)


def data_collator(batch):
    assert len(batch) == 1
    return {key: torch.tensor(value) for key, value in batch[0].items()}


# Apply quantization.
oneshot(
    model=model,
    recipe=recipe,
    dataset=ds,
    max_seq_length=MAX_SEQUENCE_LENGTH,
    num_calibration_samples=NUM_CALIBRATION_SAMPLES,
    moe_calibrate_all_experts=True,
    data_collator=data_collator,
)

# Save to disk in compressed-tensors format.
SAVE_DIR = MODEL_ID.rstrip("/").split("/")[-1] + "-INT4"
model.save_pretrained(SAVE_DIR)
processor.save_pretrained(SAVE_DIR)
```

# vLLM Serving

```bash
vllm serve RedHatAI/Qwen3.8-27B-INT4
  --tensor-parallel-size 1
  --enable-auto-tool-choice
  --tool-call-parser qwen3_coder
  --reasoning-parser qwen3
  --mm-encoder-tp-mode data
  --max-model-len 69632
  --gpu-memory-utilization 0.9
```

# Evaluations 

| Eval | Qwen/Qwen3.8-27B (BF16) | RedHatAI/Qwen3.8-27B-INT4 | Recovery (INT4/BF16) |
| --- | --- | --- | --- |
| gsm8k_platinum_cot_llama | 0.9589 | 0.9677 | 100.92% |
| ifeval | 0.9187 | 0.9211 | 100.27% |
| aime25 | 0.9375 | 0.9542 | 101.78% |
| math_500 | 0.8360 | 0.8380 | 100.24% |
| gpqa_diamond | 0.8923 | 0.8636 | 96.78% |
  
## Eval commands
Run once per seed (1234, 2345, 3456). Final reported values are averages.

### gsm8k_platinum_cot_llama
```
lm_eval \
  --model local-chat-completions \
  --tasks gsm8k_platinum_cot_llama \
  --model_args model=Qwen/Qwen3.8-27B,max_length=69632,base_url=http://127.0.0.1:8002/v1/chat/completions,num_concurrent=32,max_retries=3,tokenized
_requests=False,tokenizer_backend=None,timeout=3600 \
  --num_fewshot 0 \
  --seed <SEED> \
  --gen_kwargs do_sample=True,temperature=1.0,top_p=0.95,top_k=20,seed=<SEED>,max_gen_toks=32000 \
  --apply_chat_template
```

### ifeval

```
lm_eval \
  --model local-chat-completions \
  --tasks ifeval \
  --model_args model=Qwen/Qwen3.8-27B,max_length=69632,base_url=http://127.0.0.1:8006/v1/chat/completions,num_concurrent=16,max_retrie
s=3,tokenized_requests=False,tokenizer_backend=None,timeout=3600 \
  --num_fewshot 0 \
  --seed <SEED> \
  --gen_kwargs do_sample=True,temperature=1.0,top_p=0.95,top_k=20,seed=1234,max_gen_toks=32000 \
  --apply_chat_template
```

### aime25
```
lighteval endpoint litellm \
  runs/20260818_110422_qwen3.8-27b-int4_full_ifeval-math-aime-gpqa/configs/litellm_aime25_seed1234.yaml \
  'aime25|0' \
  --save-details
```
### math_500
```
lighteval endpoint litellm \
  runs/20260818_110422_qwen3.8-27b-int4_full_ifeval-math-aime-gpqa/configs/litellm_math_500_seed1234.yaml \
  'math_500|0' \
  --save-details
```

### GPQA Diamond
```
lighteval endpoint litellm \
  runs/20260818_110422_qwen3.8-27b-int4_full_ifeval-math-aime-gpqa/configs/litellm_gpqa_diamond_seed1234.yaml \
  'gpqa:diamond|0' \
  --save-details
```
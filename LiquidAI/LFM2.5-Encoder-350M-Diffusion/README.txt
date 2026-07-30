---
language:
- en
tags:
- liquid
- lfm2
- lfm2.5
- bidirectional
- masked-lm
- encoder
- diffusion-language-model
- masked-diffusion
- mdlm
- instruction-tuned
library_name: transformers
license: other
license_name: lfm1.0
license_link: LICENSE
pipeline_tag: text-generation
base_model:
    - LiquidAI/LFM2.5-Encoder-350M
---

<div align="center">
  <img
    src="https://cdn-uploads.huggingface.co/production/uploads/61b8e2ba285851687028d395/2b08LKpev0DNEk6DlnWkY.png"
    alt="Liquid AI"
    style="width: 100%; max-width: 100%; height: auto; display: inline-block; margin-bottom: 0.5em; margin-top: 0.5em;"
  />
  <div style="display: flex; justify-content: center; gap: 0.5em; margin-bottom: 1em;">
    <a href="https://playground.liquid.ai/"><strong>Try LFM</strong></a> •
    <a href="https://docs.liquid.ai/lfm/getting-started/welcome"><strong>Docs</strong></a> •
    <a href="https://leap.liquid.ai/"><strong>LEAP</strong></a> •
    <a href="https://discord.com/invite/liquid-ai"><strong>Discord</strong></a>
  </div>
</div>

# LFM2.5-Encoder-350M-Diffusion

A full fine-tune of [LFM2.5-Encoder-350M](https://huggingface.co/LiquidAI/LFM2.5-Encoder-350M) as a masked-diffusion instruction model that generates text by iteratively unmasking tokens instead of decoding left to right.

The model was SFT-trained on [`mlabonne/open-perfectblend`](https://huggingface.co/datasets/mlabonne/open-perfectblend), a dataset of roughly 1.39M conversations, for 3 epochs.

Masked diffusion is a natural extension of masked-language modeling: the model starts from masked answer tokens, repeatedly predicts all masked positions, fills the most confident tokens, and continues until the answer is complete.

Find more details about our encoders in our [blog post](https://www.liquid.ai/blog/lfm2-5-encoders).

> [!NOTE]
> 💻 **Demos**: Try this fine-tuned model running in a CPU-only Hugging Face space:
> **[Masked-diffusion text generation](https://huggingface.co/spaces/LiquidAI/masked-diffusion)** — run the encoder as a chatbot that generates text by iteratively unmasking instead of left to right.

## Usage

Install the required packages:

```bash
pip install torch transformers
```

Run masked-diffusion text generation:

```python
import torch
from transformers import AutoModelForMaskedLM, AutoTokenizer

model_id = "LiquidAI/LFM2.5-Encoder-350M-Diffusion"

tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForMaskedLM.from_pretrained(model_id, trust_remote_code=True).eval()

messages = [{"role": "user", "content": "Give one short tip for writing clearer code."}]
prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = tokenizer(prompt, return_tensors="pt")

num_new_tokens = 12
mask_id = tokenizer.mask_token_id
input_ids = torch.cat(
    [inputs.input_ids, torch.full((1, num_new_tokens), mask_id, dtype=torch.long)],
    dim=1,
)
attention_mask = torch.ones_like(input_ids)

with torch.no_grad():
    for _ in range(num_new_tokens):
        mask_positions = (input_ids[0] == mask_id).nonzero(as_tuple=True)[0]
        if len(mask_positions) == 0:
            break

        logits = model(input_ids=input_ids, attention_mask=attention_mask).logits[0, mask_positions]
        logits[:, len(tokenizer):] = -torch.inf
        for token_id in tokenizer.all_special_ids:
            if token_id != tokenizer.eos_token_id:
                logits[:, token_id] = -torch.inf

        probs = logits.softmax(dim=-1)
        confidence, token_ids = probs.max(dim=-1)
        best = confidence.argmax()
        input_ids[0, mask_positions[best]] = token_ids[best]

generated = input_ids[0, inputs.input_ids.shape[1]:]
text = tokenizer.decode(generated, skip_special_tokens=True).split("[/Answer]")[0]
print(text.strip())
```

## 📬 Contact

- Got questions or want to connect? [Join our Discord community](https://discord.com/invite/liquid-ai)
- If you are interested in custom solutions with edge deployment, please contact [our sales team](https://www.liquid.ai/contact).

## Citation

```bibtex
@article{liquidAI2026Encoders,
  author = {Liquid AI},
  title = {LFM2.5-Encoders: Fast at Long Context, Even on CPU},
  journal = {Liquid AI Blog},
  year = {2026},
  note = {www.liquid.ai/blog/lfm2-5-encoders},
}
```

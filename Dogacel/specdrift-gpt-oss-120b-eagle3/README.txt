---
license: cc-by-4.0
datasets:
- Dogacel/nemotron-post-training-v2-gpt-oss-120b-regen
language:
- en
base_model:
- openai/gpt-oss-120b
---

# Model Card for Model ID

<!-- Provide a quick summary of what the model is/does. -->

EAGLE-3 drafter model for GPT-oss-120b. This model is released as a part of _Attention Drift: What Speculative Decoding Models Learn_ paper. 
It has several minor architectural differences from the original EAGLE: Drafter hidden state is captured *after* the norm, additional norm injected before FC.

## Model Details

### Model Sources [optional]

- **Repository:** [Dogacel/SpecDrift](https://github.com/Dogacel/SpecDrift)
- **Paper:** https://arxiv.org/abs/2605.09992

## Uses

We recommend using SGLang to run the model,

```
export SGLANG_ENABLE_SPEC_V2=1

python -m sglang.launch_server \
    --model-path openai/gpt-oss-120b \
    --speculative-algorithm EAGLE3 \
    --speculative-draft-model-path "Dogacel/specdrift-gpt-oss-120b-eagle3" \
    --speculative-num-steps 3 \
    --speculative-eagle-topk 1 \
    --speculative-num-draft-tokens 4 \
    --speculative-draft-sliding-window 2048 \
    --port 30000 \
    --dp-size 1 --tp-size 1 \
    --max-running-requests 64 \
    --cuda-graph-max-bs 64 \
    --attention-backend fa3 \
    --trust-remote-code \
    --mem-fraction-static 0.95 --dtype bfloat16
```

## Training Details

### Training Data

<!-- This should link to a Dataset Card, perhaps with a short stub of information on what the training data is all about as well as documentation related to data pre-processing or additional filtering. -->

This model is trained on Nemoron Post Training V2 dataset, answers regenerated using gpt-oss-120b.

Dataset publicly available at: https://huggingface.co/datasets/Dogacel/nemotron-post-training-v2-gpt-oss-120b-regen

### Training Procedure

<!-- This relates heavily to the Technical Specifications. Content here should link to that section when it is relevant to the training procedure. -->

We've trained our model using [SpecForge](https://github.com/sgl-project/SpecForge) on 8xH200 within 10 hours.

- **LR:** 1e-4 (warmup 0.2, cosine)
- **Epochs:** 2
- **Batch Size:** 2 (Effective 2x8=16)
- **Max Length:** 4096
- **TTT:** 4

## Evaluation

Evaluation has run on: MT-Bench, 80 prompts, max tokens 2048, temperature 0.7

Scripts available at [SpecForge](https://github.com/sgl-project/SpecForge/pull/552).

## gpt-oss-120b · EAGLE3 (1-3-1-4) on H100

### Throughput (AL) and Δ vs Baseline


| BS | Baseline | D-Flash | Ours (1-3-1-4) |
|---:|---:|---:|---:|
| 1 | 212 | 231 (2.47) \| **+8.5%** | 285 (2.41) \| **+34.1%** |
| 8 | 795 | 905 (2.47) \| **+13.9%** | 1044 (2.41) \| **+31.4%** |
| 64 | 1620 | 1730 (2.42) \| **+6.8%** | 2339 (2.43) \| **+44.4%** |

Throughput in tok/s.

---

## Per-Category Throughput

### BS=1

| Category | Baseline | Ours | AL | Δ |
|---|---:|---:|---:|---:|
| Writing | 178.55 | 214.42 | 2.340 | +20.1% |
| Roleplay | 192.61 | 296.90 | 2.270 | **+54.1%** |
| Reasoning | 130.13 | 168.49 | 2.393 | +29.5% |
| Math | 84.26 | 115.32 | **3.101** | +36.9% |
| Coding | 329.93 | 463.48 | 2.781 | +40.5% |
| Extraction | 98.13 | 123.12 | 2.611 | +25.5% |
| STEM | 335.91 | 445.40 | 2.339 | +32.6% |
| Humanities | 349.63 | 451.13 | 2.131 | +29.0% |

### BS=8

| Category | Baseline | Ours | AL | Δ |
|---|---:|---:|---:|---:|
| Writing | 513.57 | 734.62 | 2.272 | **+43.0%** |
| Roleplay | 856.44 | 1149.83 | 2.250 | +34.3% |
| Reasoning | 481.93 | 679.52 | 2.370 | +41.0% |
| Math | 362.71 | 443.77 | **3.160** | +22.4% |
| Coding | 1278.03 | 1646.52 | 2.765 | +28.8% |
| Extraction | 388.07 | 486.76 | 2.658 | +25.4% |
| STEM | 1240.15 | 1613.25 | 2.325 | +30.1% |
| Humanities | 1238.40 | 1600.98 | 2.172 | +29.3% |

### BS=64

| Category | Baseline | Ours | AL | Δ |
|---|---:|---:|---:|---:|
| Writing | 1251.72 | 1855.41 | 2.401 | +48.2% |
| Roleplay | 1477.10 | 2389.35 | 2.238 | **+61.8%** |
| Reasoning | 947.08 | 1488.27 | 2.380 | +57.1% |
| Math | 641.84 | 997.58 | **3.095** | +55.4% |
| Coding | 2591.83 | 3607.85 | 2.803 | +39.2% |
| Extraction | 784.31 | 1139.90 | 2.733 | +45.3% |
| STEM | 2634.67 | 3753.09 | 2.315 | +42.5% |
| Humanities | 2630.41 | 3479.54 | 2.193 | +32.3% |

## Citation

<!-- If there is a paper or blog post introducing the model, the APA and Bibtex information for that should go in this section. -->

**BibTeX:**

```bibtex
@misc{eldenk2026attentiondrift,
      title={Attention Drift: What Autoregressive Speculative Decoding Models Learn}, 
      author={Doğaç Eldenk and Payal Mohapatra and Yigitcan Comlek and Kaan Oktay and Hongyang Zhang and Stephen Xia},
      year={2026},
      eprint={2605.09992},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2605.09992}, 
}
```

## Acknowledgements

We would like to thank fal and Lambda for their support.
---
license: apache-2.0
language:
- en
pipeline_tag: zero-shot-classification
library_name: transformers
base_model: dmis-lab/UltraBERT-380M
base_model_relation: finetune
tags:
- decision-model
- system-one
- semantic-router
- vela
- encoder
- zero-shot-classification
- token-classification
- named-entity-recognition
- relation-extraction
- pii-detection
- hallucination-detection
- content-safety
---

![vela3-fast](assets/banner.png)

<p align="center"><b>Name it. Vela finds it.</b><br>
<sub>vLLM Semantic Router × KR Labs · Vela 3.0 family · <b>vela3-fast</b> · 0.4B · UltraBERT-380M encoder · Apache-2.0</sub></p>

<p align="center">
<a href="#what-it-does">What it does</a> ·
<a href="#quick-start">Quick start</a> ·
<a href="#evaluation">Evaluation</a> ·
<a href="#the-family">The family</a> ·
<a href="https://huggingface.co/collections/vllm-sr/vela-30-6ad1c430eb1718eb4754edcd">📡 Collection</a>
</p>

---

**vela3-fast** is the 380M encoder of the Vela 3.0 family. One encoder pass per question gives decisions, router signals and the exact spans you name (entities, relations, personal data, unsupported claims, evidence), with probabilities and character offsets and no generated text.

| | |
| --- | --- |
| **Parameters** | 0.38B: UltraBERT-380M, fine-tuned, with gated adapters |
| **Base** | [dmis-lab/UltraBERT-380M](https://huggingface.co/dmis-lab/UltraBERT-380M), fine-tuned; its decisions come from its own distilled decision backbone, not from d3 |
| **Inputs** | Text or JSON, English, up to 32K tokens |
| **Answers** | Choice · Yes / No · Score · Span |
| **Licence** | Apache-2.0 |

## Summary

vela3-fast is the default router of the Vela 3.0 family: a 380M UltraBERT encoder with its own decision backbone, distilled from the d3 decision models, and gated adapters on top for spans, entities, relations, evidence and router signals. Its decisions have the highest public Decision Index of any model up to 500M parameters: 50.36 (our run of the unmodified kit, edition 0.3). One encoder pass per question: 14 ms for a decision at 200 tokens. English only, up to 32K tokens.

## Highlights

- **Decisions:** the highest public Decision Index of any model up to 500M parameters: 50.36 (our run of the unmodified kit, edition 0.3, public index). Next up to 500M: Amber 0.4B 49.74 and GLiClass v4 Edge (0.4B) 47.49 (board entries, Decision Index 0.4.1, public index); 15.6 points above GLiClass v4 Edge on Tools & Automation.
- **Router signals:** better than Vela 2.0 0.3B on 13 of the 24 test files of the public router signal suite, level on 6, worse on 5 (paired 95% CI).
- **Zero-shot classification:** 74.4 on the 13-set GLiFormer classification suite, above GLiFormer-base (264M): 72.36 and Qwen3.5-9B: 71.4 (reported, GLiFormer paper Tab 5).
- **Named entities:** 57.4 on the 26 NER sets of the GLiFormer paper (not all zero-shot), above GLiFormer-large (576M): 50.91 (reported, its card); 62.3 on OOD-7 zero-shot.
- **Unsupported claims:** 0.889 example-F1 on the 10,698-answer LettuceDetect v2 test set, above LettuceDetect v2 mmBERT-base (~307M): 0.869 (reported, its card).
- **Speed:** 14 ms for a decision and 18 ms for a span question at 200 tokens (batch 1, one AMD Instinct MI325X).

![Results at a glance](assets/glance.png)
<sub>vela3-fast (0.4B) against reported numbers. Accent = vela3-fast; grey = other models (reported).</sub>

## At a glance

| | |
| --- | --- |
| **What it is** | A 0.4B encoder-only member of the family: decisions, router signals and the exact spans you name from one encoder pass, at 14-28 ms a question on one GPU. English only, up to 32K tokens, text only. |
| **How it was trained** | [dmis-lab/UltraBERT-380M](https://huggingface.co/dmis-lab/UltraBERT-380M) was first taught to decide. It was distilled on the d3 decision models' answer distributions (soft labels from the d3 teacher models), on public datasets' train splits written as decisions (for example ANLI and RAGTruth), and on synthetic decision tasks in the styles the Decision Index covers (for example home-appliance control, chord progressions and causal questions), labelled by d3 or by program and checked against every Decision Index item; four distilled checkpoints were averaged. That decision backbone is frozen, and Vela adds small gated LoRA adapters on top, one per job: spans (unsupported claims, personal data), evidence, entities, relations and router signals, with dedicated adapters for the domain, fact-check and feedback signals. Each adapter switches on only for its own questions. Router signals are trained supervised, as in Vela 2.0, on the public router datasets Vela 2.0 used (for example AEGIS 2.0, PolyGuardMix and Nemotron-Safety-Guard v3 for safety, Global-MMLU for domain, WildFeedback for feedback, DiffusionDB for modality, MASSIVE for intents); feedback also on the public router signal suite's train split. Other training data: public NER, relation, hallucination, evidence and PII datasets, plus web and document text labelled by a large teacher model. No test split and no Decision Index item is trained on; some router-signal-suite test rows also occur in public training sources, so the router table also reports the rows without that overlap. |
| **What it is good at** | Decisions; zero-shot NER; zero-shot classification; router signals above Vela 2.0 0.3B on 4 of 8 signals of the public router signal suite. Pick it as the default router. |
| **How we measure it** | Public test sets only, run through this package one request at a time with the shipped thresholds: OOD-7 (CrossNER + MIT), 26 NER sets, CoNLL04, CoNLL04 · DocRED · FewRel · CrossRE, QASPER, ACL-Verbatim, the LettuceDetect v2 test set, RAGTruth, MASSIVE (three unseen scenarios), the 13-set GLiFormer classification suite, the Decision Index 0.3 (public part, our run), the public router signal suite. Other models' numbers are as their authors report them on the same test set and metric, or scored by us on the same rows where a table says so. |

## What it does

| Capability | Ask (one question of a `system_one` call) | Get |
| --- | --- | --- |
| **Decisions** | `{"type": "choice", "instructions": "What does the customer want?", "criteria": {...}}` (also `noul`, `score`) | a probability per option |
| **Router signals** | a built-in router question id | the signal's answer from the router adapter |
| **Named entities** | `{"type": "span", "criteria": {"person": None, "organization": None}}` | spans with label, offsets and score |
| **Relations** | `{"type": "span", "instructions": "Which spans are the founder of Apple?", "criteria": {"founder": None}}` | the related spans |
| **Personal data** | `{"type": "span", "criteria": ["PERSON", "EMAIL_ADDRESS"]}` | spans of the trained PII types |
| **Unsupported claims** | state `{"context": ..., "answer": ...}` and `{"type": "span", "criteria": {"unsupported": None}}` | the words of the answer the context does not support |
| **Evidence** | `{"type": "span", "criteria": ["evidence"]}` | the sentences that support the answer |

## Quick start

```python
# pip install "transformers==5.17.0" torch safetensors tokenizers huggingface_hub   (as requirements.txt)
import sys
from huggingface_hub import snapshot_download

path = snapshot_download("vllm-sr/vela3-fast")
sys.path.insert(0, path)
from vela3_encoder import Vela3Encoder

m = Vela3Encoder.load(path)  # CUDA if available, else CPU
out = m.system_one(
    "Steve Jobs founded Apple in Cupertino. My card was charged twice.",
    {"intent": {"type": "choice", "instructions": "What does the customer want?",
                "criteria": {"refund": "Money back for the duplicate charge", "cancel": "Cancel the order"}},
     "urgent": {"type": "noul", "instructions": "The customer needs a fast response."},
     "ents": {"type": "span", "instructions": "Which spans are named entities of these types?",
              "criteria": {"person": None, "organization": None}},
     "founder": {"type": "span", "instructions": "Which spans are the founder of Apple?", "criteria": {"founder": None}}})
# out["answers"]["intent"]: choice + probabilities; ["urgent"]: p(yes); ["ents"] / ["founder"]["spans"]: label, start, end, text, score
```

**Over HTTP** (`/v1/systemone`, request body `{"state", "questions"}`; a question over 32,768 tokens gets a 422, nothing is cut):

```bash
python vela3_server.py --model vllm-sr/vela3-fast --port 8000
```

**Decision Index** (`decision_index_engine:VelaEncoderEngine`, the decision backbone only):

```bash
hf download vllm-sr/vela3-fast --local-dir model
pip install -r model/requirements.txt "decision-index @ git+https://github.com/apolinario/decision-index@25c6ec7"
PYTHONPATH=model python -m decision_index run --engine decision_index_engine:VelaEncoderEngine --option run=model --edition 0.3 --out runs/vela3-fast --compact
```

## Evaluation

All numbers on public test sets, measured through this package with `system_one`, one request at a time and the shipped thresholds. Other models' numbers are as reported by their authors (or scored in the same harness where marked). Bold: above every comparator in the row. ✦: the best reported number at ≤500M. Full tables: [EVALUATION.md](EVALUATION.md).

<details open><summary><b>Named entities</b></summary>

| Benchmark | vela3-fast | Best other model (reported) | Vela 2.0 0.3B | Size-class best (≤500M, reported) |
|---|---:|---|---:|---|
| OOD-7, label names only (F1) | 62.3 | B2NER-20B 72.1 (standardised label names; B2NER Tab 3) | 31.0 (our read) | gliner-multitask-large-v0.5 (440M) 62.76 |
| NER, 26 datasets of the GLiFormer paper, label names (F1) | **57.4** ✦ | GLiFormer-large (576M) 50.91 (its card) | – | gliner_large-v2.5 (~0.46B) 50.8 (our run, same harness) |

Label names are the only input (no definition writer). Training holds no CrossNER or MIT text, though many generic CrossNER type names occur as training labels.

</details>

<details open><summary><b>Relations</b></summary>

| Benchmark | vela3-fast | Best other model (reported) | Vela 2.0 0.3B | Size-class best (≤500M, reported) |
|---|---:|---|---:|---|
| CoNLL04, head entity given, label names (F1) | **26.1** ✦ | GLiFormer-base 8.6 (our run, same harness) | 5.6 (our read) | GLiFormer-base (264M) 8.6 |
| End to end, GLiFormer Table 4 protocol, avg of 4 (strict F1) | 17.4 | Qwen3.5-9B, prompted 25.7; GLiFormer-large (576M) 21.3 (GLiFormer paper Tab 4) | – | GLiFormer-base (264M) 18.94 |
| End to end: CoNLL04 · DocRED · FewRel · CrossRE | 18.0 · 14.2 ✦ · 19.3 · 18.1 ✦ | GPT-5-mini 42.4 · GLiNER-Relex 31.3 · Qwen3.5-9B 71.6 · GLiNER-Relex 18.1 | – | GLiNER2 32.9 · GLiNER2 11.7 · GLiFormer-base 23.49 · GLiFormer-base 10.0 |

</details>

<details open><summary><b>Evidence</b></summary>

| Benchmark | vela3-fast | Best other model (reported) | Vela 2.0 0.3B | Size-class best (≤500M, reported) |
|---|---:|---|---:|---|
| QASPER, word-F1 (in-domain, whole paper in one window) | 50.8 | – | – | – |
| ACL-Verbatim, word-F1 (in-domain) | 46.5 | ACL-Verbatim ModernBERT 53.4 (in-domain, evidence only; Vela 2.0 card) | – | – |

QASPER is in-domain: the evidence adapter trains on QASPER's train split (with CUAD, ContractNLI and Natural Questions); the test papers are held out.

</details>

<details open><summary><b>Unsupported claims (hallucination spans)</b></summary>

| Benchmark | vela3-fast | Best other model (reported) | Vela 2.0 0.3B | Size-class best (≤500M, reported) |
|---|---:|---|---:|---|
| LettuceDetect v2 test set, 10,698 answers (example-F1) | 0.889 ✦ | LettuceDetect v2 qwen-2b 0.921 (its card) | 0.848 | LettuceDetect v2 mmBERT-base (~307M) 0.869 |
| RAGTruth (example-F1) | 0.785 | HDM-2 (3B) 0.850 (HalluciNot Tab 2) | 0.706 | LettuceDetect large v1 (395M) 0.792 |

</details>

<details open><summary><b>Zero-shot classification</b></summary>

| Benchmark | vela3-fast | Best other model (reported) | Vela 2.0 0.3B | Size-class best (≤500M, reported) |
|---|---:|---|---:|---|
| GLiFormer suite, 13 sets, label names only (mean macro-F1) | 74.4 ✦ | GPT-5-mini 79.8; GLiFormer-large (576M) 75.03 (GLiFormer paper Tab 5) | – | GLiFormer-base (264M) 72.4 |

</details>

<details open><summary><b>Router signals</b> (public router signal suite; above Vela 2.0 0.3B on 4 of 8)</summary>

| Signal (metric, test rows) | vela3-fast | Vela 2.0 0.3B, same rows | Decision-1.0-Route-0.6B, same rows | Rows sharing no text with training: vela3-fast / Vela 2.0 0.3B |
|---|---:|---:|---:|---|
| Harmful request (AUC, 2,230) | 0.933 | **0.945** | 0.963 | 0.907 / **0.926** (1,285) |
| Jailbreak or prompt injection (AUC, 1,878) | **0.895** | 0.787 | 0.991 | **0.831** / 0.555 (870) |
| Personal data in the request (AUC, 3,000) | 0.934 | 0.933 | 0.994 | 0.931 / 0.930 (2,787) |
| Answer not supported by its context (AUC, 3,000) | **0.765** | 0.738 | 0.791 | **0.712** / 0.690 (1,739) |
| Fact-check needed (AUC, 800) | 0.657 | **0.755** | 0.942 | 0.666 / **0.768** (688) |
| Output modality (text or image) (AUC, 3,000) | **0.906** | 0.717 | 0.999 | **0.900** / 0.709 (2,876) |
| Domain (subject area) (accuracy, 2,996) | 0.591 | 0.595 | 0.863 | 0.596 / 0.595 (2,904) |
| User feedback on the previous answer (accuracy, 2,842) | **0.819** | 0.568 | 0.848 | **0.804** / 0.508 (2,269) |

[vllm-sr/router-signal-suite](https://huggingface.co/datasets/vllm-sr/router-signal-suite) (public), the `test` file of each signal, scored with the dataset's own scoring code. Each signal is a router question this package was trained on (supervised, as in Vela 2.0), asked one request at a time with the shipped thresholds.

Vela 2.0 0.3B was run by us through its public release on the same rows. Decision-1.0-Route-0.6B is scored from the suite's published predictions; it was trained on the suite's own train split, so these test files are in-distribution for it.

Bold: the paired 95% bootstrap CI against Vela 2.0 excludes a tie. The last column drops the test rows that share text (exact or a 13-gram) with the adapters' training data and the earlier decision backbone's data; the public train splits and synthetic data added to this decision backbone were not in that scan. Safety and jailbreak are scored on the rows whose text the suite publishes (2,230 of 3,003 and 1,878 of 3,000).

Feedback is also trained on the suite's own train split (with the public router data Vela 2.0 used; the suite's test and hold rows, and anything sharing an exact text or a 13-gram with them, are kept out), as Decision-1.0-Route is, so its test files are in-distribution for both. The suite's domain classes are drawn differently from the trained ones (religion, `other`). Feedback has NO_FEEDBACK as a trained option.

</details>

<details open><summary><b>Decisions</b> (the encoder's own distilled decision backbone)</summary>

| Decision Index 0.4.1 (2026-10-28) | Public index | Full score (board rank) |
|---|---:|---:|
| GLiClass v4 Edge (0.4B) (tied rank) | 47.49 | 31.21 (156) |
| **vela3-fast (tied rank)** | **50.36** | **29.27 (164)** |
| Amber 0.4B (396M) (tied rank) | 49.74 | 26.00 (172) |
| Crivo-400M (396M) (tied rank) | 39.79 | 23.74 (177) |

Full score (the board's ranking): 60% private same-skill tests and 40% private new-domain tasks, which only the board maintainers run; public index: the 37 public benchmarks, chance-corrected. All rows are board entries on the Decision Index 0.4.1 board (multimodalart/jev-decision-index, data generated 2026-10-28T09:02Z); the rank is the position in the board's Full-score order, and tied rank marks entries the board shows as tied. Among board entries up to 500M parameters with a published size, vela3-fast has the highest public index and the second Full score, after GLiClass v4 Edge. Its board public index equals our own run of the unmodified kit (apolinario/decision-index, edition 0.3; engine `decision_index_engine:VelaEncoderEngine`, 32K context), which gives the per-benchmark numbers below. Above 500M, StartLux-Decision v1.1 0.8B (873M) has a higher public index, 53.79 (Full score 28.88).

![Decision Index public index: the top models up to 500M parameters](assets/di-top500m.png)

![Decision Index public index against model size, every board entry up to 2B parameters with a published size](assets/di-scatter.png)

| Benchmark | vela3-fast | Best other model (reported) | Vela 2.0 0.3B | Size-class best (≤500M, reported) |
|---|---:|---|---:|---|
| MASSIVE, three unseen scenarios, en-US: intent / scenario (accuracy; 67 decontaminated rows, both models read on them) | **0.776 / 0.925** | – | 0.716 / 0.806 (our read, same rows) | – |

</details>

<details><summary><b>Latency</b></summary>

| Median, one request, AMD Instinct MI325X (batch 1) | 200 tokens | 1K tokens | 3K tokens |
|---|---:|---:|---:|
| 1 decision | 14 ms | 15 ms | 31 ms |
| 4 decisions | 14 ms | 25 ms | 78 ms |
| 1 span question (3 labels) | 18 ms | 28 ms | 79 ms |

Decisions run under bf16 autocast; adapter passes run in fp32, as evaluated.

</details>

### Benchmarks

- **OOD-7** (CrossNER AI, literature, music, politics, science; MIT movie, restaurant): find the entities of the named types in text from domains the model was not trained on (strict entity F1).
- **NER, 26 datasets of the GLiFormer paper** (IE_INSTRUCTIONS): entities of named types across 26 public NER sets, not all zero-shot (strict entity F1).
- **CoNLL04, head entity given:** given one entity of a sentence, find the entities it is related to by the named relation (F1 over those tail entities).
- **Relations end to end, GLiFormer Table 4 protocol** (CoNLL04, DocRED, FewRel, CrossRE): find the entity pairs and their relation from raw text (strict triplet F1).
- **QASPER:** find the sentences of a research paper that answer a question about it (word-F1).
- **ACL-Verbatim** ([KRLabsOrg/acl-verbatim-spans](https://huggingface.co/datasets/KRLabsOrg/acl-verbatim-spans)): find the passage of an ACL paper that supports an answer (word-F1).
- **LettuceDetect v2 test set** (10,698 answers, as in the [LettuceDetect v2 paper](https://aclanthology.org/2026.groundlm-1.44/) (GroundLM 2026 workshop at EMNLP 2026) and card): does an answer contain claims its context does not support (example-F1: the answer is flagged or not).
- **RAGTruth:** does a retrieval-augmented answer contain claims its retrieved context does not support (example-F1).
- **MASSIVE, three unseen scenarios** (iot, transport, cooking): pick the intent and the scenario of a user command the model never saw in training (accuracy).
- **Zero-shot classification, 13 sets** (the GLiFormer paper's suite: SST-2, IMDB, AG News, Banking77, and more): pick the label of a text from label names only (mean macro-F1).
- **Decision Index 0.4.1** ([board](https://huggingface.co/spaces/multimodalart/jev-decision-index), 2026-10-28): 37 public decision benchmarks plus private tests; the Full score ranks on the private same-skill and new-domain tests (chance-corrected skill, 0 = guessing). The public part is the suite of kit edition 0.3, which we also ran ourselves.
- **Router signal suite** ([vllm-sr/router-signal-suite](https://huggingface.co/datasets/vllm-sr/router-signal-suite)): the vLLM Semantic Router's public test of its request signals (harmful requests, jailbreaks, personal data, unsupported answers, fact-check need, modality, domain, feedback); each label comes from public corpora (AUC or accuracy).

## The family

![The Vela 3.0 family](assets/family.png)

| Model | Size | Base | Best for |
|---|---|---|---|
| **vela3-fast** (this model) | 0.4B | UltraBERT-380M encoder | the default router; fastest: decisions and spans in one encoder pass, English, 32K |
| [vela3-fast-vision](https://huggingface.co/vllm-sr/vela3-fast-vision) | 0.3B | UltraVBERT encoder | image decisions, image-grounded hallucination spans, region pointing (preview) |
| [vela3-lite](https://huggingface.co/vllm-sr/vela3-lite) | 0.8B | d3-lite | small GPUs, low latency |
| [vela3-mini](https://huggingface.co/vllm-sr/vela3-mini) | 4B | d3-mini | balanced accuracy and speed |
| [vela3-flash](https://huggingface.co/vllm-sr/vela3-flash) | 9B | d3-flash | high-accuracy routing |
| [vela3-turbo](https://huggingface.co/vllm-sr/vela3-turbo) | 27B | d3-turbo | the reference model |

## How it works

- **Frozen backbone.** UltraBERT-380M, fine-tuned as a decision model: 24 layers, hidden size 1024, sliding-window and global attention, 32K context. Each decision is one encoder input, `[Q] instructions [O] option … [SEP_SCHEMA] [SEG_user] state`, scored at its `[O]` markers.
- **Gated adapters.** LoRA adapters with their own top layers and heads run on the frozen backbone and share its weights. Each switches on only for its own questions, and every answer names the one it used (`head`). The adapters cover:
  - span: described labels and the entity step of the relation pipeline;
  - evidence: a routed adapter for evidence questions over long documents;
  - a second span adapter for unsupported claims and PII;
  - NER (names-only entity labels);
  - relations;
  - router (safety, modality, MASSIVE);
  - task adapters for domain, fact-check and feedback.
- **Spans as decisions.** The labels are presented as options. A span head scores every word against every label, and words above the threshold form a span with character offsets. Evidence questions read the whole document in one window of up to 32K tokens, through the evidence adapter.
- **Specification.** Text or JSON state, English, up to 32K tokens; label names only. Full evaluation: [EVALUATION.md](EVALUATION.md).

## Trade-offs

- **Router signals below Vela 2.0 0.3B on the public suite:** fact-check needed 0.657 against 0.755; harmful requests 0.933 against 0.945 (same rows).
- **English only:** MASSIVE intent accuracy (test split, three unseen scenarios) falls from 0.820 in en-US to 0.44–0.54 in German, French, Spanish and Italian, and lower in other languages. For multilingual routing use [vela3-lite](https://huggingface.co/vllm-sr/vela3-lite).
- **Label names only:** no definition writer, so OOD-7 (62.3) sits just below gliner-multitask-large-v0.5 (62.76, reported).

## Citation

```bibtex
@misc{vela3_fast,
  title        = {vela3-fast (Vela 3.0, 0.4B): decisions, spans and router signals in one UltraBERT-380M encoder},
  author       = {{KR Labs} and {vLLM Semantic Router}},
  year         = {2026},
  howpublished = {\url{https://huggingface.co/vllm-sr/vela3-fast}}
}
```

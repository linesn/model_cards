---
license: apache-2.0
pipeline_tag: zero-shot-classification
library_name: transformers
base_model:
- vllm-sr/d3-lite
base_model_relation: adapter
tags:
- decision-model
- system-one
- semantic-router
- vela
- zero-shot-classification
- token-classification
- named-entity-recognition
- relation-extraction
- pii-detection
- hallucination-detection
- content-safety
- multimodal
---

![vela3-lite](assets/banner.png)

<p align="center"><b>Name it. Vela finds it.</b><br>
<sub>vLLM Semantic Router × KR Labs · Vela 3.0 family · <b>vela3-lite</b> · 0.8B · base <code>d3-lite</code> · Apache-2.0</sub></p>

<p align="center">
<a href="#what-it-does">What it does</a> ·
<a href="#quick-start">Quick start</a> ·
<a href="#evaluation">Evaluation</a> ·
<a href="#the-family">The family</a> ·
<a href="https://huggingface.co/collections/vllm-sr/vela-30-6ad1c430eb1718eb4754edcd">📡 Collection</a>
</p>

---

**vela3-lite** is the 0.8B member of the Vela 3.0 family, built on [d3-lite](https://huggingface.co/vllm-sr/d3-lite). In one `system_one` call it answers routing and general decisions and finds the exact spans you name (entities, relations, personal data, unsupported claims, evidence), with probabilities and character offsets and no generated text.

| | |
| --- | --- |
| **Parameters** | 0.85B with vision encoder (base) + 154 MB of adapters and heads |
| **Base** | [vllm-sr/d3-lite](https://huggingface.co/vllm-sr/d3-lite) at revision `9c107031`, unchanged |
| **Inputs** | Text or JSON, plus images |
| **Answers** | Choice · Yes / No · Score · Span |
| **Licence** | Apache-2.0 |

## Summary

vela3-lite is the small d3 member of the Vela 3.0 family. d3-lite, frozen, answers every ordinary decision, bit for bit, and gated adapters add the spans you name, entities, relations and router signals. It has the family's cleanest router result, reads seven languages besides English for intents, and answers a span question in 29 ms at 200 tokens.

## Highlights

- **Zero-shot NER:** 64.4 on OOD-7 (CrossNER + MIT), above every GLiNER / GLiFormer number reported on it (best: gliner-multitask-large-v0.5, 62.76; GNER-T5-large (780M): 63.5, reported).
- **Router signals:** better than Vela 2.0 0.8B on 23 of the 24 test files of the public router signal suite, level on 1, worse on none (paired 95% CI).
- **Multilingual intents:** on MASSIVE (test split, three unseen scenarios), intent accuracy in German, French, Spanish, Italian, Polish, Chinese and Japanese is 76.4–83.7, within about 9 points of English (85.1); Hungarian (66.8) and Arabic (55.3) are partial.
- **Zero-shot classification:** 73.3 on the 13-set GLiFormer classification suite, above GLiFormer-base (264M): 72.36 and Qwen3.5-9B: 71.4 (reported, GLiFormer paper Tab 5).
- **Relations:** 19.7 end to end (GLiFormer Table 4 protocol, avg of CoNLL04 · DocRED · FewRel · CrossRE), above GLiFormer-base: 18.94 and GLiNER2: 17.8 (reported, GLiFormer paper Tab 4).
- **Decisions, bit for bit:** every ordinary decision is answered by `d3-lite@9c107031` itself, adapters off (561 of 561 identical in our check).

![Results at a glance](assets/glance.png)
<sub>vela3-lite (0.8B) against reported numbers. Accent = vela3-lite; grey = other models (reported).</sub>

## At a glance

| | |
| --- | --- |
| **What it is** | A 0.85B decision-and-extraction model for LLM routing and guardrails. It runs [vllm-sr/d3-lite](https://huggingface.co/vllm-sr/d3-lite), a small d3 decision model, unchanged, and adds the exact spans you name: entities, relations, personal data, unsupported claims and evidence. |
| **How it was trained** | d3-lite stays frozen, so every ordinary decision is d3-lite's own answer, bit for bit. Vela adds small gated LoRA adapters on top, one per job: spans (unsupported claims, personal data, evidence), entities, relations, router signals and image hallucination spans. Each adapter switches on only for its own questions. Router signals are trained supervised, as in Vela 2.0, on the public router datasets Vela 2.0 used (for example AEGIS 2.0, PolyGuardMix and Nemotron-Safety-Guard v3 for safety, Global-MMLU for domain, WildFeedback for feedback, DiffusionDB for modality, MASSIVE for intents); domain, feedback, hazard categories and fact-check needed also on the public router signal suite's train split. Other training data: public NER, relation, hallucination, evidence and PII datasets, plus web and document text labelled by a large teacher model. No test split and no Decision Index item is trained on; some router-signal-suite test rows also occur in public training sources, so the router table also reports the rows without that overlap. |
| **What it is good at** | Zero-shot NER; zero-shot relations; zero-shot classification; router signals above Vela 2.0 0.8B on 9 of 9 signals of the public router signal suite. Pick it for small GPUs and low latency. |
| **How we measure it** | Public test sets only, run through this package one request at a time with the shipped thresholds: CoNLL04, CoNLL04 · DocRED · FewRel · CrossRE (avg), OOD-7 (CrossNER + MIT), RAGTruth, Super-NI task 1568, the 13-set GLiFormer classification suite, the Decision Index 0.4.1, the LettuceDetect v2 test set, the public router signal suite. Other models' numbers are as their authors report them on the same test set and metric, or scored by us on the same rows where a table says so. |

## What it does

| Capability | Ask (one question of a `system_one` call) | Get |
| --- | --- | --- |
| **Decisions** | `{"type": "choice", "instructions": "Which topic?", "criteria": {"billing": None, "tech": None}}` (also `noul`, `score`) | a probability per option, from d3-lite itself |
| **Router signals** | a built-in router question id from `router_questions.json` | the signal's answer from the gated decision adapter |
| **Named entities** | `{"type": "span", "criteria": ["drug", "dosage"]}` | spans with label, offsets and score |
| **Relations** | `{"type": "span", "instructions": "Which spans are the founder of Apple?", "criteria": {"founder": None}}` | the related spans |
| **Personal data** | `{"type": "span", "criteria": ["PERSON", "EMAIL_ADDRESS"]}` | spans of the 17 trained PII types, any subset |
| **Unsupported claims** | state `{"context": ..., "answer": ...}` and `{"type": "span", "criteria": {"unsupported": None}}` | the words of the answer the context does not support |
| **Evidence** | `{"type": "span", "criteria": ["evidence"]}` | the sentences that support the answer |
| **Image-grounded claims** | the unsupported-claims question with `images=["photo.jpg"]` | the words the image does not support |

## Quick start

```python
# pip install "transformers==5.17.0" torch torchvision pillow opencv-python-headless safetensors accelerate
from transformers import AutoModel

m = AutoModel.from_pretrained("vllm-sr/vela3-lite", trust_remote_code=True)  # downloads d3-lite at the pinned revision

# Name any labels; the spans come back with offsets and scores.
r = m.system_one(
    state="Geoffrey Hinton presented capsule networks at NeurIPS in Montreal.",
    questions={"ents": {"type": "span", "criteria": ["researcher", "algorithm", "conference", "location"]}})
# researcher "Geoffrey Hinton", algorithm "capsule networks", conference "NeurIPS", location "Montreal"

# Unsupported claims in an answer, against a context or an image.
r = m.system_one(
    state={"context": "The Eiffel Tower is 330 metres tall and was completed in 1889.",
           "answer": "The Eiffel Tower is 330 metres tall and was completed in 1925 by Gustave Eiffel's son."},
    questions={"halu": {"type": "span", "criteria": {"unsupported": None}}})
# flags "1925 by Gustave Eiffel's son"; add images=["photo.jpg"] to check an answer against a photo

# PII, relations and evidence use the same call.
r = m.system_one(
    state="Steve Jobs founded Apple in Cupertino together with Steve Wozniak.",
    questions={"pii": {"type": "span", "criteria": ["PERSON"]},
               "rel": {"type": "span", "instructions": "Which spans are the founder of Apple?", "criteria": {"founder": None}}})
```

## Evaluation

All numbers on public test sets, measured through this package with `system_one`, one request at a time and the shipped thresholds. Other models' numbers are as reported by their authors (or scored in the same harness where marked). Full per-set tables: [EVALUATION.md](EVALUATION.md).

<details open><summary><b>Named entities</b></summary>

| Benchmark | vela3-lite | Best other model (reported) | Vela 2.0 0.8B | Size-class best (0.5-1B, reported) |
|---|---:|---|---:|---|
| OOD-7, label names only (default; F1) | 64.4 | B2NER-20B 72.1 (standardised label names; B2NER Tab 3) | 28.9 | GNER-T5-large (780M) 63.5 (GNER, Table 2) |
| NER, 26 datasets of the GLiFormer paper (label names; not all zero-shot) | 60.7 | – | – | – |

Label names are the only input. Training holds no CrossNER or MIT text, though many generic CrossNER type names occur as training labels.

</details>

<details open><summary><b>Relations</b></summary>

| Benchmark | vela3-lite | Best other model (reported) | Vela 2.0 0.8B | Size-class best (0.5-1B, reported) |
|---|---:|---|---:|---|
| CoNLL04, head entity given, label names (F1) | **18.0** | GLiFormer-base 8.6 (same harness, Vela 2.0 card) | 3.0 | – |
| End to end, GLiFormer Table 4 protocol, avg of 4 (strict F1) | 19.7 | Qwen3.5-9B, prompted 25.7 (GLiFormer paper Tab 4) | – | GLiFormer-large (576M) 21.3 |
| End to end: CoNLL04 · DocRED · FewRel · CrossRE (CoNLL04 zero-shot, others in-domain) | 25.6 · 19.2 · 21.3 · 12.7 | GPT-5-mini 42.4 · GLiNER-Relex 31.3 · Qwen3.5-9B 71.6 · GLiNER-Relex 18.1 (GLiFormer paper Tab 4) | – | – |

</details>

<details open><summary><b>Evidence</b></summary>

| Benchmark | vela3-lite | Best other model (reported) | Vela 2.0 0.8B | Size-class best (0.5-1B, reported) |
|---|---:|---|---:|---|
| QASPER, word-F1 (zero-shot) | 39.3 | – | – | – |
| ACL-Verbatim, word-F1 (in-domain) | 47.8 | ACL-Verbatim ModernBERT 53.4 (in-domain, evidence only; Vela 2.0 card) | 23.6 | – |

ACL-Verbatim is in-domain: its silver training split is in the training data.

</details>

<details open><summary><b>Unsupported claims (hallucination spans)</b></summary>

| Benchmark | vela3-lite | Best other model (reported) | Vela 2.0 0.8B | Size-class best (0.5-1B, reported) |
|---|---:|---|---:|---|
| LettuceDetect v2 test set, 10,698 answers (example-F1) | 0.825 | LettuceDetect v2 qwen-2b 0.921 (its card) | 0.828 | – |
| RAGTruth (example-F1) | 0.675 | HDM-2 (3B) 0.850 (HalluciNot Tab 2) | 0.652 | HDM-1 (0.5B) 0.789 (reported, HalluciNot Tab 2) |
| M-HalDetect validation, image-grounded (char-F1) | 0.462 | – | no image path | – |

</details>

<details open><summary><b>Zero-shot classification</b></summary>

| Benchmark | vela3-lite | Best other model (reported) | Vela 2.0 0.8B | Size-class best (0.5-1B, reported) |
|---|---:|---|---:|---|
| GLiFormer suite, 13 sets, label names only (mean macro-F1) | 73.3 | GPT-5-mini 79.8 (GLiFormer paper Tab 5) | – | GLiFormer-large (576M) 75.0 |

These questions run on d3-lite with every adapter off.

</details>

<details open><summary><b>Router signals</b> (public router signal suite; above Vela 2.0 0.8B on 9 of 9)</summary>

| Signal (metric, test rows) | vela3-lite | Vela 2.0 0.8B, same rows | Decision-1.0-Route-0.6B, same rows | Rows sharing no text with training: vela3-lite / Vela 2.0 0.8B |
|---|---:|---:|---:|---|
| Harmful request (AUC, 2,230) | **0.931** | 0.919 | 0.963 | 0.912 / 0.907 (1,254) |
| Jailbreak or prompt injection (AUC, 1,878) | **0.900** | 0.872 | 0.991 | **0.849** / 0.808 (944) |
| Personal data in the request (AUC, 3,000) | **0.944** | 0.888 | 0.994 | **0.942** / 0.885 (2,802) |
| Answer not supported by its context (AUC, 3,000) | **0.734** | 0.716 | 0.791 | **0.710** / 0.686 (1,743) |
| Fact-check needed (AUC, 800) | **0.940** | 0.768 | 0.942 | **0.931** / 0.774 (690) |
| Output modality (text or image) (AUC, 3,000) | **0.920** | 0.841 | 0.999 | **0.917** / 0.838 (2,916) |
| Domain (subject area) (accuracy, 2,996) | **0.822** | 0.703 | 0.863 | **0.822** / 0.702 (2,916) |
| User feedback on the previous answer (accuracy, 2,842) | **0.808** | 0.584 | 0.848 | **0.789** / 0.543 (2,295) |
| Hazard categories (macro AUC, 11 labels, 3,001) | **0.919** | 0.740 | 0.931 | **0.884** / 0.702 (1,397) |

[vllm-sr/router-signal-suite](https://huggingface.co/datasets/vllm-sr/router-signal-suite) (public), the `test` file of each signal, scored with the dataset's own scoring code. Each signal is a router question this package was trained on (supervised, as in Vela 2.0), asked one request at a time with the shipped thresholds.

Vela 2.0 0.8B was run by us through its public release on the same rows. Decision-1.0-Route-0.6B is scored from the suite's published predictions; it was trained on the suite's own train split, so these test files are in-distribution for it.

Bold: the paired 95% bootstrap CI against Vela 2.0 excludes a tie. The last column drops the test rows that share text (exact or a 13-gram) with this model's training data. Safety and jailbreak are scored on the rows whose text the suite publishes (2,230 of 3,003 and 1,878 of 3,000).

Domain, feedback, hazard categories and fact-check needed are also trained on the suite's own train split (with the public router data Vela 2.0 used; the suite's test and hold rows, and anything sharing an exact text or a 13-gram with them, are kept out), as Decision-1.0-Route is, so their test files are in-distribution for both. The domain question has a 15th option, religion, which the suite maps to philosophy. Feedback has NO_FEEDBACK as a trained option. Hazard is a dedicated trained yes / no question per hazard category.

</details>

<details open><summary><b>Decisions</b> (general decisions are the base model's, bit for bit)</summary>

| Decision Index 0.4.1 (2026-10-28) | Public index | Full score (board rank) |
|---|---:|---:|
| Fastino GLiDE 1.2 (tied rank) | 71.99 | 71.52 (1) |
| GLiClass v4 Edge (0.4B) (tied rank) | 47.49 | 31.21 (156) |
| OneJev1.6-0.8B (tied rank) | 48.76 | 29.58 (162) |
| vela3-fast (0.4B), the family's encoder (tied rank) | 50.36 | 29.27 (164) |
| StartLux-Decision v1.1 0.8B (tied rank) | 53.79 | 28.88 (167) |
| **General decisions = d3-lite** (this package's base) | 36.93 | 26.16 (171) |

General decisions are the base model's own answers, bit for bit, so the base's board entry is this package's decision score. Full score (the board's ranking): 60% private same-skill tests and 40% private new-domain tasks; public index: the 37 public benchmarks, chance-corrected. All values are board entries on the Decision Index 0.4.1 board (multimodalart/jev-decision-index, data generated 2026-10-28T09:02Z) unless noted; the rank is the position in the board's Full-score order, and tied rank marks entries the board shows as tied. On the board's Full score, d3-lite scores 26.16 (rank 171, tied).

| Benchmark | vela3-lite | Best other model (reported) | Vela 2.0 0.8B | Size-class best (0.5-1B, reported) |
|---|---:|---|---:|---|
| Super-NI task 1568, held out (accuracy) | 0.358 | – | 0.340 | – |
| MASSIVE, three unseen scenarios: intent / scenario (accuracy; 14,911 decontaminated rows) | 0.601 / 0.707 | – | 0.544 / 0.632 (full set) | – |

MASSIVE: three scenarios never used in our router training (iot, transport, cooking), 52 locales; accuracy on the 14,911 test utterances that match no training text of the model's lineage. The 342 excluded utterances occur verbatim in upstream training mixtures (tasksource MASSIVE / HWU64 rows). Vela 2.0 values are on the full 15,253, so these rows are not bolded. Super-NI 1568: 79 to 90 of its 162 ProPara passages share a 13-gram with other tasks' training rows.

</details>

<details open><summary><b>Multilingual intents</b> (MASSIVE test split, three unseen scenarios)</summary>

| Language (MASSIVE locale) | Intent accuracy (%) | Scenario accuracy (%) |
|---|---:|---:|
| English (en-US) | 85.1 | 93.0 |
| German (de-DE) | 78.8 | 88.7 |
| French (fr-FR) | 79.3 | 93.3 |
| Spanish (es-ES) | 79.1 | 92.1 |
| Italian (it-IT) | 78.8 | 92.8 |
| Polish (pl-PL) | 76.4 | 86.8 |
| Chinese (zh-CN) | 83.7 | 93.8 |
| Japanese (ja-JP) | 82.9 | 94.0 |
| Hungarian (hu-HU), partial | 66.8 | 83.9 |
| Arabic (ar-SA), partial | 55.3 | 73.6 |

MASSIVE test split, 416 utterances per locale (the same utterances in every locale), from the three scenarios our router training never used (cooking, iot, transport). All 60 intent and 18 scenario options are asked, with English option descriptions; one `system_one` call per row, shipped thresholds, nothing tuned for other languages. Majority class on the English rows: 17.3 intent / 52.9 scenario; 95% CI about ±2 to ±5 points at this size. This covers one task type (short assistant commands) with English labels; it does not measure the other signals (domain, personal data, safety, NER) in other languages.

</details>

<details><summary><b>Latency</b></summary>

| Median, one request, AMD Instinct MI325X (one verify step per GPU) | 200 tokens | 1K tokens | 3K tokens |
|---|---:|---:|---:|
| 4 router decisions | 22 ms | 46 ms | 111 ms |
| 1 span question | 29 ms | 35 ms | 81 ms |
| 4 decisions + 1 span | 51 ms | 81 ms | 194 ms |

Span questions with label names only. 

</details>

### Benchmarks

- **OOD-7** (CrossNER AI, literature, music, politics, science; MIT movie, restaurant): find the entities of the named types in text from domains the model was not trained on (strict entity F1).
- **NER, 26 datasets of the GLiFormer paper** (IE_INSTRUCTIONS): entities of named types across 26 public NER sets, not all zero-shot (strict entity F1).
- **CoNLL04, head entity given:** given one entity of a sentence, find the entities it is related to by the named relation (F1 over those tail entities).
- **Relations end to end, GLiFormer Table 4 protocol** (CoNLL04, DocRED, FewRel, CrossRE): find the entity pairs and their relation from raw text (strict triplet F1).
- **QASPER:** find the sentences of a research paper that answer a question about it (word-F1).
- **ACL-Verbatim** ([KRLabsOrg/acl-verbatim-spans](https://huggingface.co/datasets/KRLabsOrg/acl-verbatim-spans)): find the passage of an ACL paper that supports an answer (word-F1).
- **M-HalDetect** (validation): which words of an image description the image does not support (char-F1).
- **LettuceDetect v2 test set** (10,698 answers, as in the [LettuceDetect v2 paper](https://aclanthology.org/2026.groundlm-1.44/) (GroundLM 2026 workshop at EMNLP 2026) and card): does an answer contain claims its context does not support (example-F1: the answer is flagged or not).
- **RAGTruth:** does a retrieval-augmented answer contain claims its retrieved context does not support (example-F1).
- **MASSIVE, three unseen scenarios** (iot, transport, cooking; 52 languages): pick the intent and the scenario of a user command the model never saw in training (accuracy).
- **Super-NI task 1568** (ProPara): answer a multiple-choice question about how a process changes an entity (accuracy).
- **Zero-shot classification, 13 sets** (the GLiFormer paper's suite: SST-2, IMDB, AG News, Banking77, and more): pick the label of a text from label names only (mean macro-F1).
- **Decision Index 0.4.1** ([board](https://huggingface.co/spaces/multimodalart/jev-decision-index), 2026-10-28): 37 public decision benchmarks plus private tests; the Full score ranks on the private same-skill and new-domain tests (chance-corrected skill, 0 = guessing).
- **Router signal suite** ([vllm-sr/router-signal-suite](https://huggingface.co/datasets/vllm-sr/router-signal-suite)): the vLLM Semantic Router's public test of its request signals (harmful requests, jailbreaks, personal data, unsupported answers, fact-check need, modality, domain, feedback); each label comes from public corpora (AUC or accuracy).

## The family

![The Vela 3.0 family](assets/family.png)

| Model | Size | Base | Best for |
|---|---|---|---|
| [vela3-fast](https://huggingface.co/vllm-sr/vela3-fast) | 0.4B | UltraBERT-380M encoder | the default router; fastest: decisions + spans in one ~14 ms encoder pass, English, 32K |
| [vela3-fast-vision](https://huggingface.co/vllm-sr/vela3-fast-vision) | 0.3B | UltraVBERT encoder | image decisions, image-grounded hallucination spans, region pointing (preview) |
| [vela3-lite](https://huggingface.co/vllm-sr/vela3-lite) | 0.8B | d3-lite | small GPUs, low latency |
| [vela3-mini](https://huggingface.co/vllm-sr/vela3-mini) | 4B | d3-mini | balanced accuracy and speed |
| [vela3-flash](https://huggingface.co/vllm-sr/vela3-flash) | 9B | d3-flash | high-accuracy routing |
| [vela3-turbo](https://huggingface.co/vllm-sr/vela3-turbo) | 27B | d3-turbo | the reference model |

## How it works

- **Frozen base.** `d3-lite@9c107031` runs unchanged; ordinary questions are its own answers.
- **Gated LoRA adapters.** Each switches on only for its own questions, and every answer names the one it used (`head_reason`): decision (router signals), NER (entity labels with definitions), relation, image (hallucination spans with images), span (evidence, PII, unsupported claims, toxic spans, names-only labels).
- **Spans as decisions.** The labels are presented as options; a span head scores every word against every label, and agreeing neighbours form a span with character offsets.
- **Label names in.** Labels are read by name at this size; an optional d3-mini writer (`definitions.labeldef_writer`) can write definitions first (OOD-7 64.4 with names only, 63.5 with the writer).
- **Specification.** Adds 154 MB of adapters and heads; image threshold 0.35; text or JSON state, images and video for decisions, images for hallucination spans. Full evaluation: [EVALUATION.md](EVALUATION.md).

## Trade-offs

- **Unsupported claims:** hallucination spans 0.825 against 0.921 for LettuceDetect v2 qwen-2b, RAGTruth 0.675 against 0.850 for HDM-2 (3B) (reported).
- **General decisions are d3-lite's:** below GLiClass v4 Edge (0.4B) (full score 31.21 vs 26.16) and OneJev1.6-0.8B (full score 29.58 vs 26.16) on the Decision Index 0.4.1.
- **End-to-end relations are the weakest task:** 19.7 average on the four sets, against 21.3 for GLiFormer-large (reported).

## Citation

```bibtex
@misc{vela3_lite,
  title        = {vela3-lite (Vela 3.0, 0.8B): zero-shot extraction and router signals on Decision 3.0},
  author       = {{KR Labs} and {vLLM Semantic Router}},
  year         = {2026},
  howpublished = {\url{https://huggingface.co/vllm-sr/vela3-lite}}
}
```

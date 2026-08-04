---
base_model:
  - ibm-granite/granite-4.0-1b
language:
  - en
library_name: transformers
license: apache-2.0
pipeline_tag: text-generation
tags:
  - security
  - vulnerability-detection
  - agentic
  - terminal-agent
  - reinforcement-learning
  - granite
gated: true
extra_gated_prompt: >
  Please complete the form below to request access to this model. All requests
  are reviewed manually.

  By submitting this form, you confirm that the information provided is
  accurate,  agree to share your contact details with the repository authors.
  You will be  subject to their communications and Privacy Statement: 
  https://www.cisco.com/c/en/us/about/legal/privacy-full.html
extra_gated_fields:
  First name: text
  Last name: text
  Email address: text
  Country: country
  Affiliation: text
  Occupation: text
  I have read, understood, and agree to the Terms and Conditions above: checkbox
---

# **Antares-1B**

Antares-1B is an open-weight, 1-billion parameter language model specialized for vulnerability localization in real-world codebases. Built on IBM Granite 4.0 1B, it is trained to autonomously navigate source code repositories through a terminal interface — issuing shell commands, reading files, and iteratively narrowing in on vulnerable code segments — using a two-stage pipeline: supervised fine-tuning (SFT) followed by Group Relative Policy Optimization (GRPO).

Unlike traditional static analysis tools or retrieval-based approaches, Antares-1B operates as a terminal agent: it explores repositories by executing commands (`grep`, `find`, `cat`, and standard Unix utilities), reasons about the output, and submits a list of files it believes to contain the reported vulnerability.

Antares-1B is part of the Antares family of models (350M, 1B, 3B), all built on IBM Granite 4.0 and trained with the same two-stage pipeline. The 1B model achieves a File F1 of **0.209** on the Vulnerability Localization benchmark (VLoc Bench), outperforming models many times its size including GLM-5.2, Gemini 3 Pro, GPT-5 Mini, and Qwen3.5-122B.

> [!NOTE]
> **Antares CLI:** To support model adoption and simplify integration, we provide the Antares CLI as a ZIP file in this repository’s Files section. The CLI packages the complete Antares agent loop, runs analyses over a read-only repository snapshot, and connects to a user-configured OpenAI-compatible inference endpoint. It supports targeted CWE analyses and repository-wide sweeps, with candidate vulnerable files returned in human-readable, JSON, or SARIF formats for analyst review.

Antares enables organizations to deploy compact, on-premises vulnerability localization capabilities without dependency on cloud-based AI services. In our evaluation setup, Antares-1B completes the full 500-task VLoc Bench sweep in approximately 13 minutes on a single H100 GPU using 16 parallel workers.

- **Model Name:** Antares-1B
- **Model Developer:** Copyright © 2026 by Cisco Systems, Inc. All rights reserved. Cisco product group: Foundation AI
- **Model Card Contact:** [**https://fdtn.ai/contact**](https://fdtn.ai/contact)
- [**Technical Report:**](https://cisco-foundation-ai.github.io/antares/technical-report.pdf) Vijay, Priyanshu, et al. "Antares: Foundation Models for Agentic Vulnerability Localization." Foundation AI, Cisco, 2026.
- **Model Release Date:** 2026
- **Supported Language(s):** English
- **Model Architecture:** Auto-regressive decoder-only transformer (IBM Granite 4.0 1B backbone): 40 layers, hidden dim 2048, 16 attention heads, 4 KV heads (GQA), 128K context window, 100,352 vocab, SwiGLU activation, RMSNorm, RoPE positional encoding.
- **Training Objective:** Two-stage pipeline: SFT on deep-research, terminal-navigation, and cybersecurity-reasoning data, followed by GRPO with multi-component verifiable rewards over complete multi-turn agent trajectories, including file-level localization quality, valid submission behavior, tool-use compliance, and exploration behavior.
- **Training Data Status:** This is a static model trained on an offline dataset with a data cutoff of April 10, 2025. Future versions will be released on updated data.
- **License:** Apache 2.0

## **Intended Use**

### **Intended Use Cases**

Antares-1B is designed for security practitioners, researchers, and developers building automated vulnerability detection workflows. The model is optimized for:

- **Vulnerability Localization**: Given a CWE identifier, its generic category description, and a repository, identifying which source files contain the reported vulnerability — using only a terminal interface, without any external retrieval system or vector database.
- **Shift-Left Security**: Integrating into CI/CD pipelines to surface vulnerable files early in the development lifecycle. The 1B model runs on a single GPU, making it practical for automated pipeline use.
- **Advisory-Driven Triage**: Using CWE identifiers and generic category descriptions, including those mapped from CVE or GHSA records, to guide repository exploration into targeted, multi-step terminal exploration strategies that narrow down candidate files for analyst review.

The model is intended for local deployment in environments prioritizing data security, regulatory compliance, and operational control.

### **Downstream Use**

Antares-1B can be integrated into security toolchains as a terminal-based agentic component. Example downstream applications include:

- **Vulnerability Search**: Locating vulnerable files from CWE descriptions by issuing shell commands against a repository snapshot
- **Security Workflow Integration**: Augmenting static analysis tools with reasoning-driven repository exploration; accelerating incident response by surfacing relevant code from CVE or GHSA descriptions; supporting security analysts in evidence gathering and hypothesis refinement
- **Automated Code Triage**: Iteratively narrowing down candidate files using grep, find, and content inspection to surface security-relevant code for analyst review

For questions or assistance with integrating Antares-1B, please contact Hadas Birin ([**hbirin@cisco.com**](mailto:hbirin@cisco.com)).

### **Out-of-Scope Use**

The following uses are out-of-scope and are neither recommended nor intended use cases:

1. **Generating harmful content** — The model should not be used to:
    - Generate malware or other malicious code
    - Create phishing content or social engineering scripts
    - Develop attack plans targeting specific organizations
    - Design exploitation techniques for vulnerabilities without legitimate security research purposes
2. **Critical security decisions without human oversight** — The model should not be used for:
    - Autonomous security decision-making without human review
    - Critical infrastructure protection without expert supervision
    - Final determination of security compliance without human verification
    - Autonomous vulnerability remediation without testing
3. **Legal or medical advice** — The model is not qualified to provide legal advice regarding security regulations, compliance requirements, or intellectual property disputes, or medical advice regarding health impacts of security incidents.
4. **General-purpose chat or instruction following** — The model is specifically trained for terminal-based vulnerability localization and may not perform well on general conversational or instruction-following tasks.
5. **Standalone safety evaluation** — This model is designed to operate within an agentic terminal loop rather than as a general-purpose chat assistant. Standard safety benchmarks such as HarmBench evaluate direct conversational refusal behavior, which does not reflect how this model is intended to be deployed. Safety considerations should instead be addressed at the system level through access controls, sandbox isolation, and human oversight of model outputs.
6. **Violation of Laws or Regulations** — Any use that violates applicable laws or regulations.

## **How to Get Started with the Model**

Antares-1B operates as a terminal agent: it receives a system prompt containing a CWE identifier and a generic category description, then iteratively generates reasoning and tool calls (shell commands) whose outputs are appended to the conversation context. The model may issue up to 15 terminal calls and must then terminate through either `submit_vulnerable_files` or `submit_no_vulnerability_found`.

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("fdtn-ai/antares-1b")
model = AutoModelForCausalLM.from_pretrained("fdtn-ai/antares-1b")

# The model uses a structured tool-calling format:
#   <think> ... </think>                   — internal reasoning
#   <tool_call> {"name": "terminal", "arguments": {"command": "..."}} </tool_call>
#   <tool_response> ... </tool_response>   — sandbox output (provided externally)
#
# The agent loop terminates when the model calls:
#   submit_vulnerable_files   — list of file paths believed to be vulnerable
#   submit_no_vulnerability_found — declares the repository clean

SYSTEM_PROMPT = """You are a security vulnerability localization agent.
You have access to a terminal with the repository mounted at /workspace/repo/.
Use shell commands (grep, find, cat, etc.) to explore the codebase and identify
files that contain the reported vulnerability. When confident, submit your findings."""

cwe_description = (
    "CWE-78: Improper Neutralization of Special Elements used in an OS Command "
    "('OS Command Injection'). The software constructs all or part of an OS command "
    "using externally-influenced input from an upstream component, but does not "
    "neutralize or incorrectly neutralizes special elements that could modify the "
    "intended OS command when it is sent to a downstream component."
)

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": f"Vulnerability to locate:\n{cwe_description}"},
]

# Apply chat template and generate the first reasoning + tool call turn
inputs = tokenizer.apply_chat_template(
    messages, return_tensors="pt", add_generation_prompt=True, return_dict=True
)
prompt_length = inputs["input_ids"].shape[-1]
output = model.generate(
    **inputs,
    do_sample=True,
    temperature=0.3,
    top_p=1.0,
    max_new_tokens=512,
)
response = tokenizer.decode(output[0][prompt_length:], skip_special_tokens=False)
print(response)

# The model will output a <think> block followed by a <tool_call> block.
# Your infrastructure should parse the tool call, execute the command in a sandbox,
# and append the result as a <tool_response> message before the next generation turn.
# Repeat until the model calls submit_vulnerable_files or submit_no_vulnerability_found.
```

The model is designed to operate within an agentic evaluation loop with a sandboxed terminal environment. Each repository should be extracted into an isolated container (e.g., `ubuntu:24.04` with network disabled) before the agent begins exploration. See the technical report for full integration details and the recommended agent loop implementation.

## **Training and Evaluation**

### **Training Data**

Antares-1B was trained through a two-stage pipeline:

**Stage 1 — Supervised Fine-Tuning (SFT):** A proprietary corpus spanning three categories: (1) cybersecurity reasoning data covering vulnerability concepts, CWE/CVE reasoning, threat modeling, advisory interpretation, and security analysis; (2) deep-research and general reasoning data focused on multi-step reasoning, evidence aggregation, and instruction following; and (3) code-search trajectories demonstrating terminal-based repository exploration, file inspection, and iterative search behavior.

**Stage 2 — GRPO (Group Relative Policy Optimization):** Reinforcement learning over complete multi-turn agent trajectories using vulnerable repository snapshots curated through proprietary data-generation and filtering pipelines. Each task includes a complete codebase containing a known vulnerability and ground-truth labels identifying the affected implementation files. 

**Data cutoff:** April 10, 2025.

This is a static model trained on an offline dataset. Future versions will be released on updated data. A detailed description of the methodology is available in the technical report.

### **Training Setup**

Antares-1B is based on the **IBM Granite 4.0 1B** architecture. Training was performed on Cisco Foundation AI's internal compute cluster.

Key training details:

- **Two-stage training**: SFT → GRPO
- **Optimizer:** AdamW
- **Compute:** 8×H100 GPUs

A more detailed description of the methodology is available in the technical report.

### **Evaluation**

Antares-1B was evaluated on Vulnerability Localization Benchmark(VLoc Bench), a vulnerability localization benchmark comprising 500 tasks drawn from 290 unique real-world repositories, spanning 6 package ecosystems and 147 unique CWE categories, with 78% of entries carrying assigned CVE identifiers. Each entry consists of a repository snapshot (reconstructed at the pre-fix commit) paired with ground truth files (those modified in the actual security fix PR, excluding tests, docs, and configuration). 

The agent is given only a generic CWE category description — no advisory text, no file hints, no severity details — and must explore the repository within a budget of 15 terminal commands per task, followed by one final submission action.

**Metric calculation:** For each task, submitted file paths are compared with the ground-truth set of vulnerable implementation files. Precision is the fraction of submitted files in the ground-truth set, recall is the fraction of ground-truth files submitted, and File F1 is the harmonic mean of task-level precision and recall. A task with no valid file submission receives zero precision, recall, and File F1 because every Phase A task contains a known vulnerability. We macro-average precision, recall, and File F1 across all 500 tasks, then average the resulting metrics across three independent runs. The reported File F1 is therefore the mean of task-level F1 scores.

All evaluations use temperature=0.3 and top_p=1.0.

**Overall Performance (Phase A — File F1):**

| **Model** | **Parameters** | **File F1 ↑** | **Precision** | **Recall** |
| --- | --- | --- | --- | --- |
| GPT-5.5 (xhigh) | Frontier | 0.229 | 0.310 | 0.221 |
| **Antares-3B (GRPO)** | **3B** | **0.223** | **0.303** | **0.221** |
| GPT-5.5 | Frontier | 0.221 | 0.305 | 0.211 |
| **Antares-1B (GRPO)** | **1B** | **0.209** | **0.262** | **0.224** |
| **Antares-3B (SFT)** | **3B** | **0.198** | **0.240** | **0.228** |
| **Antares-1B (SFT)** | **1B** | **0.188** | **0.263** | **0.179** |
| GLM-5.2 | 753B | 0.186 | 0.226 | 0.186 |
| Gemini 3 Pro | Frontier | 0.152 | 0.190 | 0.153 |
| **Antares-350M (GRPO)** | **350M** | **0.135** | **0.136** | **0.178** |
| **Antares-350M (SFT)** | **350M** | **0.108** | **0.149** | **0.101** |
| Gemini 2.5 Flash | Frontier | 0.102 | 0.132 | 0.098 |
| Gemma-4-31B | 31B | 0.101 | 0.131 | 0.097 |
| GPT-5 Mini | Frontier | 0.098 | 0.115 | 0.096 |
| Gemini 3.1 Flash Lite | Frontier | 0.095 | 0.131 | 0.090 |
| Qwen3.5-122B-A10B | 125B MoE | 0.091 | 0.124 | 0.083 |
| GPT-5 | Frontier | 0.048 | 0.062 | 0.048 |
| GPT-5 Nano | Frontier | 0.024 | 0.038 | 0.021 |
| Llama-3.3-70B | 70B | 0.012 | 0.016 | 0.014 |
| Granite 4.0 1B (base) | 1B | 0.000 | — | — |

**Bold rows indicate Antares models. All models use the same agent protocol, tools, task inputs, 15-call terminal budget, and generation settings of temperature 0.3 and top-p 1.0. Results are averaged across three independent runs.**

## **Safety Alignment**

This model is designed to operate as a component within a sandboxed agentic terminal loop, not as a standalone conversational assistant. As such, no additional standalone safety alignment (e.g., RLHF-based refusal training or HarmBench evaluation) was performed on this model.

Safety considerations should be addressed at the system level by:

- Running the agent inside an isolated sandbox environment (e.g., Docker container with `network=none`)
- Implementing access controls on the deployment environment to restrict use to authorized security personnel
- Enforcing human oversight over model outputs before any remediation action is taken
- Monitoring and auditing agent trajectories in high-risk workflows

It is strongly recommended to deploy this model with appropriate system-level safeguards and not to expose it as a general-purpose assistant endpoint.

## **Limitations**

Antares-1B has several limitations that users should be aware of:

1. **Terminal budget constraints:** Performance degrades significantly on large repositories (>10MB) where 15 commands are insufficient to cover the codebase. Multi-file vulnerabilities requiring 5+ files of context also underperform.
2. **Vulnerability pattern dependence:** The model performs best on vulnerability types with distinctive, grep-able code patterns (e.g., CWE-843 Type Confusion, CWE-1321 Prototype Pollution). It performs poorly on CWE types requiring semantic understanding of code behavior rather than pattern matching (e.g., CWE-732 Incorrect Permissions, CWE-667 Improper Locking, CWE-401 Memory Leak).
3. **Knowledge cutoff:** The model may not recognize vulnerabilities, exploit patterns, or attack vectors introduced after its April 10, 2025 training cutoff.
4. **No intended exploitation functionality:** The model localizes vulnerable files but does not generate proof-of-concept exploits or explain why a file is vulnerable — it only identifies which files are likely affected. Its internal reasoning guides the file search but is not surfaced as a vulnerability explanation.
5. **Retrieval system independence:** Unlike embedding-based retrieval approaches, Antares requires no external vector database, but performance is bounded by the quality of its terminal exploration strategy within the allotted command budget.
6. **Potential biases:** The model may reflect biases present in security literature and known attack patterns, and may be biased toward vulnerability types and programming languages more prevalent in its training data.
7. **Security risks:** The model cannot verify the identity or intentions of users. Adversarial prompting techniques may potentially bypass safety mechanisms if the model is exposed without system-level guardrails.

### **Recommendations**

To address the limitations of Antares-1B, we recommend:

1. **Human oversight:** Always have qualified security professionals review model outputs before taking action. Use the model as an assistive tool rather than a replacement for expert human judgment. Implement a human-in-the-loop approach for security-critical workflows.
2. **Sandbox isolation:** Run the agent inside a Docker container with network disabled (`network=none`), a command timeout (10 seconds recommended), and resource limits (2 CPU cores, 4GB RAM). Destroy the container after each evaluation entry.
3. **System-level access controls:** Deploy the model in environments with appropriate access controls and restrict access to authorized security personnel.
4. **Knowledge supplementation:** Supplement the model with up-to-date security feeds and vulnerability databases for advisories released after the April 2025 training cutoff.
5. **Usage policies:** Develop and enforce clear acceptable use policies for applications using this model. Implement monitoring and auditing for high-risk applications.

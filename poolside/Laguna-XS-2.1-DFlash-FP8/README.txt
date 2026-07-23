---
library_name: speculators
base_model:
- poolside/Laguna-XS-2.1-FP8
license: openmdw-1.1
tags:
- speculative-decoding
- dflash
- speculators
---

# poolside/Laguna-XS-2.1-DFlash-FP8

DFlash speculator for the FP8 target [poolside/Laguna-XS-2.1-FP8](https://huggingface.co/poolside/Laguna-XS-2.1-FP8). The speculator itself is a 5-layer Llama-style draft model (in BF16); pair it with the FP8 base for lower-latency serving.

> [!NOTE]
> Speculators for the other precisions are available in this collection: [BF16](https://huggingface.co/poolside/Laguna-XS-2.1-DFlash), [INT4](https://huggingface.co/poolside/Laguna-XS-2.1-DFlash-INT4), [NVFP4](https://huggingface.co/poolside/Laguna-XS-2.1-DFlash-NVFP4).

See the [Laguna XS 2.1 DFlash speculator model card](https://huggingface.co/poolside/Laguna-XS-2.1-DFlash) for architecture, training, and deployment. DFlash upstream support is in progress (vLLM [#46853](https://github.com/vllm-project/vllm/pull/46853), SGLang [#29446](https://github.com/sgl-project/sglang/pull/29446), TRT-LLM [#15666](https://github.com/NVIDIA/TensorRT-LLM/pull/15666)). Use `poolside/Laguna-XS-2.1-FP8` as the target model.

## License

This model is licensed under the [OpenMDW-1.1 License](https://huggingface.co/poolside/Laguna-XS-2.1-DFlash-FP8/blob/main/LICENSE.md).

## Intended and Responsible Use 

Laguna-XS-2.1-DFlash-FP8 is designed for software engineering and agentic coding use cases, and you are responsible for confirming that it is appropriate for your intended application. Laguna-XS-2.1-DFlash-FP8 is subject to the [OpenMDW-1.1 License](https://huggingface.co/poolside/Laguna-XS-2.1-DFlash-FP8/blob/main/LICENSE.md), and should be used consistently with Poolside's [Acceptable Use Policy](https://poolside.ai/legal/acceptable-use-policy).

Please report security vulnerabilities or safety concerns to [security@poolside.ai](mailto:security@poolside.ai).

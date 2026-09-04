This model is a T5-base reranker fine-tuned on the MS MARCO passage dataset for 10k steps (or 1 epoch).

This model usually has a better zero-shot performance than `monot5-base-msmarco`, i.e., it performs better on datasets different from MS MARCO.

For more details on how to use it, check the following links:
- [A simple reranking example](https://github.com/castorini/pygaggle#a-simple-reranking-example)
- [Rerank MS MARCO passages](https://github.com/castorini/pygaggle/blob/master/docs/experiments-msmarco-passage-subset.md)
- [Rerank Robust04 documents](https://github.com/castorini/pygaggle/blob/master/docs/experiments-robust04-monot5-gpu.md)

Paper describing the model: [Document Ranking with a Pretrained Sequence-to-Sequence Model](https://www.aclweb.org/anthology/2020.findings-emnlp.63/)
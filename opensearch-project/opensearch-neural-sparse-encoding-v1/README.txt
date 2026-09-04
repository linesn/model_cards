---
language: en
license: apache-2.0
tags:
- learned sparse
- opensearch
- transformers
- retrieval
- passage-retrieval
- query-expansion
- document-expansion
- bag-of-words
- sentence-transformers
- sparse-encoder
- sparse
- splade
pipeline_tag: feature-extraction
library_name: sentence-transformers
---

# opensearch-neural-sparse-encoding-v1

## Select the model
The model should be selected considering search relevance, model inference and retrieval efficiency(FLOPS). We benchmark models' **zero-shot performance** on a subset of BEIR benchmark: TrecCovid,NFCorpus,NQ,HotpotQA,FiQA,ArguAna,Touche,DBPedia,SCIDOCS,FEVER,Climate FEVER,SciFact,Quora.

Overall, the v2 series of models have better search relevance, efficiency and inference speed than the v1 series. The specific advantages and disadvantages may vary across different datasets.

| Model | Inference-free for Retrieval | Model Parameters | AVG NDCG@10 | AVG FLOPS |
|-------|------------------------------|------------------|-------------|-----------|
| [opensearch-neural-sparse-encoding-v1](https://huggingface.co/opensearch-project/opensearch-neural-sparse-encoding-v1) |  | 133M | 0.524 | 11.4 |
| [opensearch-neural-sparse-encoding-v2-distill](https://huggingface.co/opensearch-project/opensearch-neural-sparse-encoding-v2-distill) |  | 67M | 0.528 | 8.3 |
| [opensearch-neural-sparse-encoding-doc-v1](https://huggingface.co/opensearch-project/opensearch-neural-sparse-encoding-doc-v1) | ✔️ | 133M | 0.490 | 2.3 |
| [opensearch-neural-sparse-encoding-doc-v2-distill](https://huggingface.co/opensearch-project/opensearch-neural-sparse-encoding-doc-v2-distill) | ✔️ | 67M | 0.504 | 1.8 |
| [opensearch-neural-sparse-encoding-doc-v2-mini](https://huggingface.co/opensearch-project/opensearch-neural-sparse-encoding-doc-v2-mini) | ✔️ | 23M | 0.497 | 1.7 |
| [opensearch-neural-sparse-encoding-doc-v3-distill](https://huggingface.co/opensearch-project/opensearch-neural-sparse-encoding-doc-v3-distill) | ✔️ | 67M | 0.517 | 1.8 |
| [opensearch-neural-sparse-encoding-doc-v3-gte](https://huggingface.co/opensearch-project/opensearch-neural-sparse-encoding-doc-v3-gte) | ✔️ | 133M | 0.546 | 1.7 |

## Overview
- **Paper**: [Towards Competitive Search Relevance For Inference-Free Learned Sparse Retrievers](https://arxiv.org/abs/2411.04403)
- **Fine-tuning sample**: [opensearch-sparse-model-tuning-sample](https://github.com/zhichao-aws/opensearch-sparse-model-tuning-sample)

This is a learned sparse retrieval model. It encodes the queries and documents to 30522 dimensional **sparse vectors**. The non-zero dimension index means the corresponding token in the vocabulary, and the weight means the importance of the token.

This model is trained on MS MARCO dataset.

OpenSearch neural sparse feature supports learned sparse retrieval with lucene inverted index. Link: https://opensearch.org/docs/latest/query-dsl/specialized/neural-sparse/. The indexing and search can be performed with OpenSearch high-level API.

## Usage (Sentence Transformers)

First install the Sentence Transformers library:

```bash
pip install -U sentence-transformers
```

Then you can load this model and run inference.

```python
from sentence_transformers.sparse_encoder import SparseEncoder

# Download from the 🤗 Hub
model = SparseEncoder("opensearch-project/opensearch-neural-sparse-encoding-v1")

query = "What's the weather in ny now?"
document = "Currently New York is rainy."

query_embed = model.encode_query(query)
document_embed = model.encode_document(document)

sim = model.similarity(query_embed, document_embed)
print(f"Similarity: {sim}")
# Similarity: tensor([[22.3299]])

decoded_query = model.decode(query_embed)
decoded_document = model.decode(document_embed)

for i in range(len(decoded_query)):
    query_token, query_score = decoded_query[i]
    doc_score = next((score for token, score in decoded_document if token == query_token), 0)
    if doc_score != 0:
        print(f"Token: {query_token}, Query score: {query_score:.4f}, Document score: {doc_score:.4f}")

# Token: ny, Query score: 2.9262, Document score: 2.1335
# Token: weather, Query score: 2.5206, Document score: 1.5277
# Token: york, Query score: 2.0373, Document score: 2.3489
# Token: cool, Query score: 1.5786, Document score: 0.8752
# Token: current, Query score: 1.4636, Document score: 1.5132
# Token: season, Query score: 0.7761, Document score: 0.8860
# Token: 2020, Query score: 0.7560, Document score: 0.6726
# Token: summer, Query score: 0.7222, Document score: 0.6292
# Token: nina, Query score: 0.6888, Document score: 0.6419
# Token: storm, Query score: 0.6451, Document score: 0.8200
# Token: brooklyn, Query score: 0.4698, Document score: 0.7635
# Token: julian, Query score: 0.4562, Document score: 0.1208
# Token: wow, Query score: 0.3484, Document score: 0.3903
# Token: usa, Query score: 0.3439, Document score: 0.4160
# Token: manhattan, Query score: 0.2751, Document score: 0.8260
# Token: fog, Query score: 0.2013, Document score: 0.7735
# Token: mood, Query score: 0.1989, Document score: 0.2961
# Token: climate, Query score: 0.1653, Document score: 0.3437
# Token: nature, Query score: 0.1191, Document score: 0.1533
# Token: temperature, Query score: 0.0665, Document score: 0.0599
# Token: windy, Query score: 0.0552, Document score: 0.3396
```

## Usage (HuggingFace)
This model is supposed to run inside OpenSearch cluster. But you can also use it outside the cluster, with HuggingFace models API. 

```python
import itertools
import torch
from transformers import AutoModelForMaskedLM, AutoTokenizer


# get sparse vector from dense vectors with shape batch_size * seq_len * vocab_size
def get_sparse_vector(feature, output):
    values, _ = torch.max(output*feature["attention_mask"].unsqueeze(-1), dim=1)
    values = torch.log(1 + torch.relu(values))
    values[:,special_token_ids] = 0
    return values
    
# transform the sparse vector to a dict of (token, weight)
def transform_sparse_vector_to_dict(sparse_vector):
    sample_indices,token_indices=torch.nonzero(sparse_vector,as_tuple=True)
    non_zero_values = sparse_vector[(sample_indices,token_indices)].tolist()
    number_of_tokens_for_each_sample = torch.bincount(sample_indices).cpu().tolist()
    tokens = [transform_sparse_vector_to_dict.id_to_token[_id] for _id in token_indices.tolist()]

    output = []
    end_idxs = list(itertools.accumulate([0]+number_of_tokens_for_each_sample))
    for i in range(len(end_idxs)-1):
        token_strings = tokens[end_idxs[i]:end_idxs[i+1]]
        weights = non_zero_values[end_idxs[i]:end_idxs[i+1]]
        output.append(dict(zip(token_strings, weights)))
    return output
    

# load the model
model = AutoModelForMaskedLM.from_pretrained("opensearch-project/opensearch-neural-sparse-encoding-v1")
tokenizer = AutoTokenizer.from_pretrained("opensearch-project/opensearch-neural-sparse-encoding-v1")

# set the special tokens and id_to_token transform for post-process
special_token_ids = [tokenizer.vocab[token] for token in tokenizer.special_tokens_map.values()]
get_sparse_vector.special_token_ids = special_token_ids
id_to_token = ["" for i in range(tokenizer.vocab_size)]
for token, _id in tokenizer.vocab.items():
    id_to_token[_id] = token
transform_sparse_vector_to_dict.id_to_token = id_to_token



query = "What's the weather in ny now?"
document = "Currently New York is rainy."

# encode the query & document
feature = tokenizer([query, document], padding=True, truncation=True, return_tensors='pt', return_token_type_ids=False)
output = model(**feature)[0]
sparse_vector = get_sparse_vector(feature, output)

# get similarity score
sim_score = torch.matmul(sparse_vector[0],sparse_vector[1])
print(sim_score)   # tensor(22.3299, grad_fn=<DotBackward0>)


query_token_weight, document_query_token_weight = transform_sparse_vector_to_dict(sparse_vector)
for token in sorted(query_token_weight, key=lambda x:query_token_weight[x], reverse=True):
    if token in document_query_token_weight:
        print("score in query: %.4f, score in document: %.4f, token: %s"%(query_token_weight[token],document_query_token_weight[token],token))
        

        
# result:
# score in query: 2.9262, score in document: 2.1335, token: ny
# score in query: 2.5206, score in document: 1.5277, token: weather
# score in query: 2.0373, score in document: 2.3489, token: york
# score in query: 1.5786, score in document: 0.8752, token: cool
# score in query: 1.4636, score in document: 1.5132, token: current
# score in query: 0.7761, score in document: 0.8860, token: season
# score in query: 0.7560, score in document: 0.6726, token: 2020
# score in query: 0.7222, score in document: 0.6292, token: summer
# score in query: 0.6888, score in document: 0.6419, token: nina
# score in query: 0.6451, score in document: 0.8200, token: storm
# score in query: 0.4698, score in document: 0.7635, token: brooklyn
# score in query: 0.4562, score in document: 0.1208, token: julian
# score in query: 0.3484, score in document: 0.3903, token: wow
# score in query: 0.3439, score in document: 0.4160, token: usa
# score in query: 0.2751, score in document: 0.8260, token: manhattan
# score in query: 0.2013, score in document: 0.7735, token: fog
# score in query: 0.1989, score in document: 0.2961, token: mood
# score in query: 0.1653, score in document: 0.3437, token: climate
# score in query: 0.1191, score in document: 0.1533, token: nature
# score in query: 0.0665, score in document: 0.0600, token: temperature
# score in query: 0.0552, score in document: 0.3396, token: windy
```

The above code sample shows an example of neural sparse search. Although there is no overlap token in original query and document, but this model performs a good match. 

## Detailed Search Relevance

<div style="overflow-x: auto;">
    
| Model | Average | Trec Covid | NFCorpus | NQ | HotpotQA | FiQA | ArguAna | Touche | DBPedia | SCIDOCS | FEVER | Climate FEVER | SciFact | Quora |
|-------|---------|------------|----------|----|----------|------|---------|--------|---------|---------|-------|---------------|---------|-------|
| [opensearch-neural-sparse-encoding-v1](https://huggingface.co/opensearch-project/opensearch-neural-sparse-encoding-v1) | 0.524 | 0.771 | 0.360 | 0.553 | 0.697 | 0.376 | 0.508 | 0.278 | 0.447 | 0.164 | 0.821 | 0.263 | 0.723 | 0.856 |
| [opensearch-neural-sparse-encoding-v2-distill](https://huggingface.co/opensearch-project/opensearch-neural-sparse-encoding-v2-distill) | 0.528 | 0.775 | 0.347 | 0.561 | 0.685 | 0.374 | 0.551 | 0.278 | 0.435 | 0.173 | 0.849 | 0.249 | 0.722 | 0.863 |
| [opensearch-neural-sparse-encoding-doc-v1](https://huggingface.co/opensearch-project/opensearch-neural-sparse-encoding-doc-v1) | 0.490 | 0.707 | 0.352 | 0.521 | 0.677 | 0.344 | 0.461 | 0.294 | 0.412 | 0.154 | 0.743 | 0.202 | 0.716 | 0.788 |
| [opensearch-neural-sparse-encoding-doc-v2-distill](https://huggingface.co/opensearch-project/opensearch-neural-sparse-encoding-doc-v2-distill) | 0.504 | 0.690 | 0.343 | 0.528 | 0.675 | 0.357 | 0.496 | 0.287 | 0.418 | 0.166 | 0.818 | 0.224 | 0.715 | 0.841 |
| [opensearch-neural-sparse-encoding-doc-v2-mini](https://huggingface.co/opensearch-project/opensearch-neural-sparse-encoding-doc-v2-mini) | 0.497 | 0.709 | 0.336 | 0.510 | 0.666 | 0.338 | 0.480 | 0.285 | 0.407 | 0.164 | 0.812 | 0.216 | 0.699 | 0.837 |
| [opensearch-neural-sparse-encoding-doc-v3-distill](https://huggingface.co/opensearch-project/opensearch-neural-sparse-encoding-doc-v3-distill) | 0.517 | 0.724 | 0.345 | 0.544 | 0.694 | 0.356 | 0.520 | 0.294 | 0.424 | 0.163 | 0.845 | 0.239 | 0.708 | 0.863 |
| [opensearch-neural-sparse-encoding-doc-v3-gte](https://huggingface.co/opensearch-project/opensearch-neural-sparse-encoding-doc-v3-gte) | 0.546 | 0.734 | 0.360 | 0.582 | 0.716 | 0.407 | 0.520 | 0.389 | 0.455 | 0.167 | 0.860 | 0.312 | 0.725 | 0.873 |

</div>

## License

This project is licensed under the [Apache v2.0 License](https://github.com/opensearch-project/neural-search/blob/main/LICENSE).

## Copyright

Copyright OpenSearch Contributors. See [NOTICE](https://github.com/opensearch-project/neural-search/blob/main/NOTICE) for details.
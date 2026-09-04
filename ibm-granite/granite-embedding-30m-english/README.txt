---
language:
- en
license: apache-2.0
library_name: sentence-transformers
tags:
- language
- granite
- embeddings
- mteb
- transformers
pipeline_tag: sentence-similarity
---
# Granite-Embedding-30m-English (revision r1.1)

**Model Summary:**
Granite-Embedding-30m-English is a 30M parameter dense bi-encoder embedding model from the Granite Embeddings suite that can be used to generate high quality text embeddings. This model produces embedding vectors of size 384 and is trained using a combination of open source relevance-pair datasets with permissive, enterprise-friendly license, and IBM collected and generated datasets. While maintaining competitive scores on academic benchmarks such as BEIR, this model also performs well on many enterprise use cases. This model is developed using retrieval oriented pre-training, contrastive fine-tuning, knowledge distillation and model merging for improved performance.

***Granite-embedding-30m-r1.1*** was specifically designed to support multi-turn information retrieval and is designed to handle contextual document retrieval in multi-turn conversational information retrieval. Granite-embedding-30m-r1.1 was trained on data tailored for multi-turn conversational information retrieval and uses multi-teacher distillation over granite-embedding-30m-english (https://huggingface.co/ibm-granite/granite-embedding-30m-english) 

- **Developers:** Granite Embedding Team, IBM
- **GitHub Repository:** [ibm-granite/granite-embedding-models](https://github.com/ibm-granite/granite-embedding-models)
- **Website**: [Granite Docs](https://www.ibm.com/granite/docs/)
- **Paper:** [Technical Report](https://arxiv.org/abs/2502.20204)
- **Release Date**: August 29, 2025 (granite-embedding-30m-english-r1.1)
- **License:** [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)

**Supported Languages:** 
English.

**Intended use:** 
The model is designed to produce fixed length vector representations for a given text, which can be used for text similarity, retrieval, and search applications.

**Usage with Sentence Transformers:** 
The model is compatible with SentenceTransformer library and is very easy to use:

First, install the sentence transformers library
```shell
pip install sentence_transformers
```

The model can then be used to encode pairs of text and find the similarity between their representations. 

***Granite-Embedding-30m-English***

```python
from sentence_transformers import SentenceTransformer, util

model_path = "ibm-granite/granite-embedding-30m-english"
# Load the Sentence Transformer model
model = SentenceTransformer(model_path)

input_queries = [
    ' Who made the song My achy breaky heart? ',
    'summit define'
    ]

input_passages = [
    "Achy Breaky Heart is a country song written by Don Von Tress. Originally titled Don't Tell My Heart and performed by The Marcy Brothers in 1991. ",
    "Definition of summit for English Language Learners. : 1 the highest point of a mountain : the top of a mountain. : 2 the highest level. : 3 a meeting or series of meetings between the leaders of two or more governments."
    ]

# encode queries and passages
query_embeddings = model.encode(input_queries)
passage_embeddings = model.encode(input_passages)

# calculate cosine similarity
print(util.cos_sim(query_embeddings, passage_embeddings))
```

***Granite-Embedding-30m-r1.1***

Specifically to encode with granite-embedding-30m-r1.1 the entire conversation, ending with the last user query, should be provided as the input, with the conversation instances arranged in reverse chronological order: first the last user query, then the preceding agent response, followed by the previous user query. Example,

Conversation: user:<user_query_1> agent: <agent_response_1> user:<user_query_2> agent: <agent_response_2> user:<user_query_3> agent: <agent_response_3> user:<last_user_query>

Conversation in input query format: <last_user_query>[SEP]agent: <agent_response_3>||user:<user_query_3>||agent: <agent_response_2>||user:<user_query_2>||agent: <agent_response_1>||user:<user_query_1>

```python
from sentence_transformers import SentenceTransformer, util

model_path = "ibm-granite/granite-embedding-30m-english"
# Load the Sentence Transformer model
model = SentenceTransformer(model_path, revision="granite-embedding-30m-r1.1")

input_queries = [
    "Which team has won the most Super Bowls?[SEP]agent: Six teams from each conference (AFC and NFC), for a total of 12 team playoff system.||user: How many teams are in the NFL playoffs?||agent: There are 32 teams in the National Football League (NFL).||user: How many teams are in the NFL?",

    "How many teams are in the NFL playoffs?[SEP]agent: There are 32 teams in the National Football League (NFL).||user: How many teams are in the NFL?||agent: The Chicago Cardinals became the St. Louis Cardinals in 1960 and eventually moved and became the Arizona Cardinals. The Chicago Cardinals ( now the Arizona Cardinals ) were a founding member of the NFL.||user: Are the Arizona Cardinals and the Chicago Cardinals the same team?||agent: The Arizona Cardinals do play outside the United States. They had a game in London, England, on October 22, 2017, against the Los Angeles Rams at Twickenham Stadium and in 2005 they played in Mexico.||user: Do the Arizona Cardinals play outside the US?"
    ]

input_passages = [
    "Super Bowl\nThe Pittsburgh Steelers have won six Super Bowls , the most of any team ; the Dallas Cowboys , New England Patriots and San Francisco 49ers have five victories each , while the Green Bay Packers and New York Giants have four Super Bowl championships . Fourteen other NFL franchises have won at least one Super Bowl . Eight teams have appeared in Super Bowl games without a win . The Minnesota Vikings were the first team to have appeared a record four times without a win . The Buffalo Bills played in a record four Super Bowls in a row and lost every one . Four teams ( the Cleveland Browns , Detroit Lions , Jacksonville Jaguars , and Houston Texans ) have never appeared in a Super Bowl . The Browns and Lions both won NFL Championships prior to the creation of the Super Bowl , while the Jaguars ( 1995 ) and Texans ( 2002 ) are both recent NFL expansion teams . ( Detroit , Houston , and Jacksonville , however , have hosted a Super Bowl , leaving the Browns the only team to date who has neither played in nor whose city has hosted the game . ) The Minnesota Vikings won the last NFL Championship before the merger but lost to the AFL champion Kansas City Chiefs in Super Bowl IV.",

    "NFL playoffs \n The 32 - team National Football League is divided into two conferences , American Football Conference ( AFC ) and National Football Conference ( NFC ) , each with 16 teams . Since 2002 , each conference has been further divided into four divisions of four teams each . The tournament brackets are made up of six teams from each of the league 's two conferences , following the end of the regular season . Qualification into the playoffs works as follows : "
    ]

# encode queries and passages
query_embeddings = model.encode(input_queries)
passage_embeddings = model.encode(input_passages)

# calculate cosine similarity
print(util.cos_sim(query_embeddings, passage_embeddings))
```

**Usage with Huggingface Transformers:** This is a simple example of how to use the Granite-Embedding-30m-English model with the Transformers library and PyTorch.

First, install the required libraries
```shell
pip install transformers torch
```

The model can then be used to encode pairs of text

***Granite-Embedding-30m-English***

```python
import torch
from transformers import AutoModel, AutoTokenizer

model_path = "ibm-granite/granite-embedding-30m-english"

# Load the model and tokenizer
model = AutoModel.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
model.eval()

input_queries = [
    ' Who made the song My achy breaky heart? ',
    'summit define'
    ]

# tokenize inputs
tokenized_queries = tokenizer(input_queries, padding=True, truncation=True, return_tensors='pt')

# encode queries
with torch.no_grad():
    # Queries
    model_output = model(**tokenized_queries)
    # Perform pooling. granite-embedding-30m-english uses CLS Pooling
    query_embeddings = model_output[0][:, 0]

# normalize the embeddings
query_embeddings = torch.nn.functional.normalize(query_embeddings, dim=1)

```

***Granite-Embedding-30m-r1.1*** 

```python
import torch
from transformers import AutoModel, AutoTokenizer

model_path = "ibm-granite/granite-embedding-30m-english"

# Load the model and tokenizer
model = AutoModel.from_pretrained(model_path, revision="granite-embedding-30m-r1.1")
tokenizer = AutoTokenizer.from_pretrained(model_path)
model.eval()

input_queries = [
    "Which team has won the most Super Bowls?[SEP]agent: Six teams from each conference (AFC and NFC), for a total of 12 team playoff system.||user: How many teams are in the NFL playoffs?||agent: There are 32 teams in the National Football League (NFL).||user: How many teams are in the NFL?",

    "How many teams are in the NFL playoffs?[SEP]agent: There are 32 teams in the National Football League (NFL).||user: How many teams are in the NFL?||agent: The Chicago Cardinals became the St. Louis Cardinals in 1960 and eventually moved and became the Arizona Cardinals. The Chicago Cardinals ( now the Arizona Cardinals ) were a founding member of the NFL.||user: Are the Arizona Cardinals and the Chicago Cardinals the same team?||agent: The Arizona Cardinals do play outside the United States. They had a game in London, England, on October 22, 2017, against the Los Angeles Rams at Twickenham Stadium and in 2005 they played in Mexico.||user: Do the Arizona Cardinals play outside the US?"
    ]

# tokenize inputs
tokenized_queries = tokenizer(input_queries, padding=True, truncation=True, return_tensors='pt')

# encode queries
with torch.no_grad():
    # Queries
    model_output = model(**tokenized_queries)
    # Perform pooling. granite-embedding-30m-english-multiturn uses CLS Pooling
    query_embeddings = model_output[0][:, 0]

# normalize the embeddings
query_embeddings = torch.nn.functional.normalize(query_embeddings, dim=1)

```
**Evaluation:**

Granite-Embedding-30M-English model is twice as fast as other models with similar embedding dimensions, while maintaining competitive performance. The performance of the Granite-Embedding-30M-English model on MTEB Retrieval (i.e., BEIR) and code retrieval (CoIR) benchmarks is reported below. 

| Model                           | Paramters (M)| Embedding Dimension |  MTEB Retrieval (15) |  CoIR (10) | 
|---------------------------------|:------------:|:-------------------:|:-------------------: |:----------:|
|granite-embedding-30m-english    |30            |384                  |49.1                  |47.0        | 


granite-embedding-30m-r1.1 revision maintains the fast speed of granite-embedding-30m-english while demontratring strong performance on multi-turn information retrieval benchmarks. The performance of the granite-embedding-30M-r1.1 model on MTEB Retrieval (i.e., BEIR) and multi-turn information retrieval (MTRAG(https://github.com/IBM/mt-rag-benchmark), Multidoc2dial(https://github.com/IBM/multidoc2dial)) datasets is reported below. 


| Model                                     | Parameters (M)| Embedding Dimension |  MTEB Retrieval (15) |  MT-RAG    | Mdoc2dial | 
|-------------------------------------------|:------------:|:-------------------:|:-------------------: |:----------:| :--------:|
|granite-embedding-30m-english              |30            |384                  |49.1                  |49.16       | 85.42     |
|**granite-embedding-30m-english-r1.1**     |30            |384                  |48.9                  |**52.33**   | **85.78** |
|bge-small-en-v1.5                          |33            |512                  |53.86                 |38.26       | 83.71     |
|e5-small-v2                                |33            |384                  |48.46                 |28.72       | 75.7      |

**Model Architecture:**
granite-embedding-30m-English is based on an encoder-only RoBERTa like transformer architecture, trained internally at IBM Research. granite-embedding-30m-r1.1 shares the same architecture as granite-embedding-30m-English

| Model                     | granite-embedding-30m-english | granite-embedding-125m-english    | granite-embedding-107m-multilingual | granite-embedding-278m-multilingual |
| :---------                | :-------:| :--------:   | :-----:| :-----:|
| Embedding size            | **384**  | 768          | 384    | 768    |
| Number of layers          | **6**    | 12           | 6      | 12     |
| Number of attention heads | **12**   | 12           | 12     | 12     |
| Intermediate size         | **1536** | 3072         | 1536   | 3072   |
| Activation Function       | **GeLU** | GeLU         | GeLU   | GeLU   |
| Vocabulary Size           | **50265**| 50265        | 250002 | 250002 |
| Max. Sequence Length      | **512**  | 512          | 512    | 512    |
| # Parameters              | **30M**  | 125M         | 107M   | 278M   |

**Training Data:**
Overall, the training data consists of four key sources: (1) unsupervised title-body paired data scraped from the web, (2) publicly available paired with permissive, enterprise-friendly license, (3) IBM-internal paired data targeting specific technical domains, and (4) IBM-generated synthetic data. The data is listed below:

| **Dataset**                                        | **Num. Pairs** | 
|----------------------------------------------------|:---------------:|
| SPECTER citation triplets                          | 684,100         | 
| Stack Exchange Duplicate questions (titles)        | 304,525         | 
| Stack Exchange Duplicate questions (bodies)        | 250,519         | 
| Stack Exchange Duplicate questions (titles+bodies) | 250,460         | 
| Natural Questions (NQ)                             | 100,231         | 
| SQuAD2.0                                           | 87,599          | 
| PAQ (Question, Answer) pairs                       | 64,371,441      | 
| Stack Exchange (Title, Answer) pairs               | 4,067,139       | 
| Stack Exchange (Title, Body) pairs                 | 23,978,013      | 
| Stack Exchange (Title+Body, Answer) pairs          | 187,195         | 
| S2ORC Citation pairs (Titles)                      | 52,603,982      | 
| S2ORC (Title, Abstract)                            | 41,769,185      | 
| S2ORC (Citations, abstracts)                       | 52,603,982      | 
| WikiAnswers Duplicate question pairs               | 77,427,422      | 
| SearchQA                                           | 582,261         | 
| HotpotQA                                           | 85,000          | 
| Fever                                              | 109,810         | 
| Arxiv                                              | 2,358,545       | 
| Wikipedia                                          | 20,745,403      | 
| PubMed                                             | 20,000,000      | 
| Miracl En Pairs                                    | 9,016           | 
| DBPedia Title-Body Pairs                           | 4,635,922       | 
| Synthetic: Query-Wikipedia Passage                 | 1,879,093       | 
| Synthetic: Fact Verification                       | 9,888           | 
| IBM Internal Triples                               | 40,290          | 
| IBM Internal Title-Body Pairs                      | 1,524,586       | 
| MultiDoc2Dial Train (MultiTurn Conversation)       | 21,451          |
| Synthetic IBM internal data                        | 19,533          |

Notably, we do not use the popular MS-MARCO retrieval dataset in our training corpus due to its non-commercial license, while other open-source models train on this dataset due to its high quality.

**Infrastructure:**
We train Granite Embedding Models using IBM's computing cluster, Cognitive Compute Cluster, which is outfitted with NVIDIA A100 80gb GPUs. This cluster provides a scalable and efficient infrastructure for training our models over multiple GPUs.

**Ethical Considerations and Limitations:** 
The data used to train the base language model was filtered to remove text containing hate, abuse, and profanity. Granite-embedding-30m-english and Granite-embedding-30m-r1.1 are trained only for English texts, and has a context length of 512 tokens (longer texts will be truncated to this size).

**Resources**
- ⭐️ Learn about the latest updates with Granite: https://www.ibm.com/granite
- 📄 Get started with tutorials, best practices, and prompt engineering advice: https://www.ibm.com/granite/docs/
- 💡 Learn about the latest Granite learning resources: https://ibm.biz/granite-learning-resources
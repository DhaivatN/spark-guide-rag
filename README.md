# The Unofficial Guide for Apache Spark (Project 1)

<!-- > **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit. -->

---

## Domain


<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
This system covers Apache Spark SQL and DataFrame Usage, extracted from Spark SQL documentation. The goal is to have a robust system to answer questions on schema definition, temp views, caching, file formats and tuning join without re-reading long documentation pages.
This is valuable because official documentation is verbose, while this system allows you to ask direct questions and get succinct and cited answers focused on code and config.
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->
All documents are local .txt files under documents/spark, each extracted from sections of Apache Spark documentation on spark.apache.org and split by topic.

```text
+----+-------------+--------------------------------------------+-----------------------------------------------------------------------------+
| #  |   Source    |                Description                 |                               URL or location                               |
+----+-------------+--------------------------------------------+-----------------------------------------------------------------------------+
|  1 | Document 1  | Spark Session and Dataframes               | documents\spark\Document 1 - SparkSession and DataFrames.txt                |
|  2 | Document 2  | SQL Queries and Global Temporary Views     | documents\spark\Document 2 - SQL Queries and Global Temporary Views.txt     |
|  3 | Document 3  | RDDs, Scalar and Aggregate Functions       | documents\spark\Document 3 - RDDs, Scalar and Aggregate Functions.txt       |
|  4 | Document 4  | Performance Tuning, Caching and Partitions | documents\spark\Document 4 - Performance Tuning, Caching and Partitions.txt |
|  5 | Document 5  | Optimizing Join Strategy                   | documents\spark\Document 5 - Optimizing Join Strategy.txt                   |
|  6 | Document 6  | Storage Partition and Join                 | documents\spark\Document 6 - Storage Partition and Join.txt                 |
|  7 | Document 7  | Generic Load and Save Options              | documents\spark\Document 7 - Generic Load and Save Options.txt              |
|  8 | Document 8  | Generic File Source Options                | documents\spark\Document 8 - Generic File Source Options.txt                |
|  9 | Document 9  | Parquet Files                              | documents\spark\Document 9 - Parquet Files.txt                              |
| 10 | Document 10 | JSON Files                                 | documents\spark\Document 10 - JSON Files.txt                                |
| 11 | Document 11 | ORC Files                                  | documents\spark\Document 11 - ORC Files.txt                                 |
| 12 | Document 12 | CSV Files                                  | documents\spark\Document 12 - CSV Files.txt                                 |
+----+-------------+--------------------------------------------+-----------------------------------------------------------------------------+
```

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->
**Chunk size:**

512 characters

**Overlap:**

100 characters

**Why these choices fit your documents:**

Before chunking, each .txt file is loaded from documents/spark and basic cleaning is applied; stripping extra whitespace and preserving existing line breaks so that code blocks and tables remain readable. 
Documents are then split using RecursiveCharacterTextSplitter with paragraph boundaries, then line breaks, and then spaces using ["\n\n", "\n", " ", ""].

The chunk size is 512 characters with an overlap of 100 characters, which is enough to hold a short example plus a code sample and also small enough that each chunk stays on a single topic and similary search can distinguish between sections.
An overlap of 100 characters lets definitions and their examples without losing context.

Across the 12 source documents, this strategy produced 258 chunks, which is a good size for local sentence-transformer embeddings and ChromaDB retrieval.

**Final chunk count:**

258 chunks

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

sentence-transformers/all-MiniLM-L6-v2 with ChromaDB as the vector store

**Production tradeoff reflection:**

For a production deployment, it would be worth considering a larger or domain-tuned embedding model that supports longer context windows so each embedding can represent more complex sections, and is more code-aware or technical-text-tuned for Spark/Scala/PySpark snippets, which might improve similarity on questions.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

“You are a Spark SQL assistant. Answer the user's question using ONLY the provided context chunks from the Spark documentation. If the context does not contain enough information to answer, say: ‘I don't have enough information in the provided documents to answer that.’ Do NOT use any outside knowledge or guess beyond the context. Always mention which document IDs and chunk IDs you used in your answer."

Structurally, only the top‑k retrieved chunks from Chroma (default k=5) are passed to the LLM alongside the question; the model never sees the full documents or the internet. 

**How source attribution is surfaced in the response:**

When building the context string, each chunk is tagged with its doc_id and chunk_id, e.g. "Document 4 - Performance Tuning, Caching and Partitions.txt | chunk 1" before the chunk text. The prompt tells the model to mention which documents and chunks it used.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

```text
.................................................................................................................................................
: # :         Question          :  Expected answer (short)  :      System response      :     Retrieval quality     :     Response accuracy     :
:   :                           :                           :       (summarized)        :                           :                           :
:...:...........................:...........................:...........................:...........................:...........................:
: 1 : How to programmatically   : Define a StructType       : Described the three-step  : Relevant – top chunks are : Accurate – matches the    :
:   : define a schema using     : composed of StructFields  : process: create an RDD of : the “Programmatically     : documented pattern and    :
:   : StructType and            : (name, type, nullable)    : tuples, build a           : Specifying the Schema”    : explains                  :
:   : StructField in Spark?     : and apply it when         : StructType schema with    : section and examples.     : StructType/StructField    :
:   :                           : creating the DataFrame,   : StructFields from         :                           : correctly.                :
:   :                           : e.g. schema =             : pyspark.sql.types, and    :                           :                           :
:   :                           : StructType([StructField(" : apply it via              :                           :                           :
:   :                           : name",                    : spark.createDataFrame(peo :                           :                           :
:   :                           : StringType(), True),      : ple,                      :                           :                           :
:   :                           : ...]) then                : schema), and showed a     :                           :                           :
:   :                           : spark.createDataFrame(rdd : code snippet. Cited       :                           :                           :
:   :                           : ,                         : Document 3, chunk 7.      :                           :                           :
:   :                           : schema) or                :                           :                           :                           :
:   :                           : spark.read.schema(schema) :                           :                           :                           :
:   :                           : ....                      :                           :                           :                           :
: 2 : What is a global          : Temp view is              : Explained that a global   : Highly relevant –         : Accurate – aligns fully   :
:   : temporary view and how is : session-scoped and        : temp view is              : retrieval pulled exactly  : with the docs.            :
:   : it different from a       : disappears when its       : cross-session, tied to    : the “Global Temporary     :                           :
:   : temporary view?           : SparkSession ends. Global : global_temp, referenced   : View” explanation and     :                           :
:   :                           : temp view is shared       : as global_temp.view1, and : code examples.            :                           :
:   :                           : across sessions within    : persists until the Spark  :                           :                           :
:   :                           : the same application and  : application ends, while a :                           :                           :
:   :                           : lives until the app       : regular temp view is      :                           :                           :
:   :                           : terminates; it resides in : session-scoped and        :                           :                           :
:   :                           : the global_temp database  : disappears with the       :                           :                           :
:   :                           : and must be referenced as : session. Cited Document   :                           :                           :
:   :                           : global_temp.view_name.    : 2, chunks 2–3.            :                           :                           :
: 3 : How does Spark SQL cache  : Spark SQL caches tables   : Answered that Spark SQL   : Relevant – top chunk is   : Partially accurate – core :
:   : tables and how to uncache : or DataFrames using       : caches tables using       : the “Caching Data”        : behavior                  :
:   : them?                     : spark.catalog.cacheTable( : spark.catalog.cacheTable( : section and neighboring   : (cacheTable/cache,        :
:   :                           : ...)                      : "tableName")              : tuning content.           : uncacheTable/unpersist)   :
:   :                           : or dataFrame.cache() in   : or dataFrame.cache() and  :                           : is correct; answer omits  :
:   :                           : an in-memory columnar     : uncaches using            :                           : SQL CACHE TABLE/UNCACHE   :
:   :                           : format. To uncache, use   : spark.catalog.uncacheTabl :                           : TABLE and clearCache(),   :
:   :                           : spark.catalog.uncacheTabl : e("tableName")            :                           : which are mentioned in    :
:   :                           : e(...)                    : or dataFrame.unpersist(), :                           : the broader docs.         :
:   :                           : or dataFrame.unpersist(). : explicitly referencing    :                           :                           :
:   :                           :                           : the in-memory columnar    :                           :                           :
:   :                           :                           : cache and memory removal. :                           :                           :
:   :                           :                           : Cited Document 4, chunk   :                           :                           :
:   :                           :                           : 1.                        :                           :                           :
: 4 : What file formats does    : From the ingested docs    : Listed CSV (using         : Relevant – retrieval      : Partially accurate –      :
:   : Spark natively support in : the main formats are CSV, : spark.read().csv("file_na : pulled CSV, JSON, and     : completely correct for    :
:   : this corpus, and how does : JSON, and Parquet; Spark  : me")),                    : Parquet sections plus     : CSV/JSON/Parquet in the   :
:   : it read them?             : reads them using          : JSON                      : generic load/save         : provided docs, but does   :
:   :                           : spark.read().csv(...),    : (spark.read().json("file_ : options.                  : not mention ORC/text/Avro :
:   :                           : spark.read().json(...),   : name")),                  :                           : even though those exist   :
:   :                           : and                       : and Parquet (Spark can    :                           : in broader Spark docs but :
:   :                           : spark.read().parquet(...) : read and write Parquet    :                           : are not fully represented :
:   :                           : ,                         : while preserving schema), :                           : in this extracted corpus. :
:   :                           : with behavior customized  : and explained that these  :                           :                           :
:   :                           : via .option() or          : use spark.read methods    :                           :                           :
:   :                           : .options().               : and can be customized     :                           :                           :
:   :                           :                           : with option(). Cited      :                           :                           :
:   :                           :                           : Documents 12, 9, and 7.   :                           :                           :
: 5 : How to tune               : Either tune               : Explained that for large  : Relevant – retrieval      : Accurate – focuses on     :
:   : spark.sql.shuffle.partiti : spark.sql.shuffle.partiti : joins you should set a    : surfaced the “Optimizing  : AQE-based tuning instead  :
:   : ons                       : ons                       : sufficiently large        : Join Strategy” section    : of manual static          :
:   : for a large join?         : directly via              : initial number of shuffle : describing AQE coalescing : partition count, which    :
:   :                           : spark.conf.set(...), or,  : partitions and enable     : of shuffle partitions,    : matches the guidance in   :
:   :                           : as the docs suggest,      : adaptive query execution  : plus related              : the ingested docs.        :
:   :                           : start with a large        : (spark.sql.adaptive.enabl : join/partition configs.   :                           :
:   :                           : initial partition count   : ed                        :                           :                           :
:   :                           : and let Adaptive Query    : and                      :                           :                           :
:   :                           : Execution coalesce        : spark.sql.adaptive.coales :                           :                           :
:   :                           : partitions using          : cePartitions.enabled),    :                           :                           :
:   :                           : spark.sql.adaptive.coales : letting Spark coalesce    :                           :                           :
:   :                           : cePartitions.*            : post-shuffle partitions   :                           :                           :
:   :                           : settings.                 : based on runtime stats,   :                           :                           :
:   :                           :                           : and mentioned related     :                           :                           :
:   :                           :                           : settings like             :                           :                           :
:   :                           :                           : initialPartitionNum and   :                           :                           :
:   :                           :                           : minPartitionSize. Cited   :                           :                           :
:   :                           :                           : Document 5, chunks 8–9    :                           :                           :
:   :                           :                           : and Document 6.           :                           :                           :
:...:...........................:...........................:...........................:...........................:...........................:
```

<!-- 
.................................................................................................................................................
: # :         Question          :  Expected answer (short)  :      System response      :     Retrieval quality     :     Response accuracy     :
:   :                           :                           :       (summarized)        :                           :                           :
:...:...........................:...........................:...........................:...........................:...........................:
: 1 : How to programmatically   : Define a StructType       : Described the three-step  : Relevant – top chunks are : Accurate – matches the    :
:   : define a schema using     : composed of StructFields  : process: create an RDD of : the “Programmatically     : documented pattern and    :
:   : StructType and            : (name, type, nullable)    : tuples, build a           : Specifying the Schema”    : explains                  :
:   : StructField in Spark?     : and apply it when         : StructType schema with    : section and examples.     : StructType/StructField    :
:   :                           : creating the DataFrame,   : StructFields from         :                           : correctly.                :
:   :                           : e.g. schema =             : pyspark.sql.types, and    :                           :                           :
:   :                           : StructType([StructField(" : apply it via              :                           :                           :
:   :                           : name",                    : spark.createDataFrame(peo :                           :                           :
:   :                           : StringType(), True),      : ple,                      :                           :                           :
:   :                           : ...]) then                : schema), and showed a     :                           :                           :
:   :                           : spark.createDataFrame(rdd : code snippet. Cited       :                           :                           :
:   :                           : ,                         : Document 3, chunk 7.      :                           :                           :
:   :                           : schema) or                :                           :                           :                           :
:   :                           : spark.read.schema(schema) :                           :                           :                           :
:   :                           : ....                      :                           :                           :                           :
: 2 : What is a global          : Temp view is              : Explained that a global   : Highly relevant –         : Accurate – aligns fully   :
:   : temporary view and how is : session-scoped and        : temp view is              : retrieval pulled exactly  : with the docs.            :
:   : it different from a       : disappears when its       : cross-session, tied to    : the “Global Temporary     :                           :
:   : temporary view?           : SparkSession ends. Global : global_temp, referenced   : View” explanation and     :                           :
:   :                           : temp view is shared       : as global_temp.view1, and : code examples.            :                           :
:   :                           : across sessions within    : persists until the Spark  :                           :                           :
:   :                           : the same application and  : application ends, while a :                           :                           :
:   :                           : lives until the app       : regular temp view is      :                           :                           :
:   :                           : terminates; it resides in : session-scoped and        :                           :                           :
:   :                           : the global_temp database  : disappears with the       :                           :                           :
:   :                           : and must be referenced as : session. Cited Document   :                           :                           :
:   :                           : global_temp.view_name.    : 2, chunks 2–3.            :                           :                           :
: 3 : How does Spark SQL cache  : Spark SQL caches tables   : Answered that Spark SQL   : Relevant – top chunk is   : Partially accurate – core :
:   : tables and how to uncache : or DataFrames using       : caches tables using       : the “Caching Data”        : behavior                  :
:   : them?                     : spark.catalog.cacheTable( : spark.catalog.cacheTable( : section and neighboring   : (cacheTable/cache,        :
:   :                           : ...)                      : "tableName")              : tuning content.           : uncacheTable/unpersist)   :
:   :                           : or dataFrame.cache() in   : or dataFrame.cache() and  :                           : is correct; answer omits  :
:   :                           : an in-memory columnar     : uncaches using            :                           : SQL CACHE TABLE/UNCACHE   :
:   :                           : format. To uncache, use   : spark.catalog.uncacheTabl :                           : TABLE and clearCache(),   :
:   :                           : spark.catalog.uncacheTabl : e("tableName")            :                           : which are mentioned in    :
:   :                           : e(...)                    : or dataFrame.unpersist(), :                           : the broader docs.         :
:   :                           : or dataFrame.unpersist(). : explicitly referencing    :                           :                           :
:   :                           :                           : the in-memory columnar    :                           :                           :
:   :                           :                           : cache and memory removal. :                           :                           :
:   :                           :                           : Cited Document 4, chunk   :                           :                           :
:   :                           :                           : 1.                        :                           :                           :
: 4 : What file formats does    : From the ingested docs    : Listed CSV (using         : Relevant – retrieval      : Partially accurate –      :
:   : Spark natively support in : the main formats are CSV, : spark.read().csv("file_na : pulled CSV, JSON, and     : completely correct for    :
:   : this corpus, and how does : JSON, and Parquet; Spark  : me")),                    : Parquet sections plus     : CSV/JSON/Parquet in the   :
:   : it read them?             : reads them using          : JSON                      : generic load/save         : provided docs, but does   :
:   :                           : spark.read().csv(...),    : (spark.read().json("file_ : options.                  : not mention ORC/text/Avro :
:   :                           : spark.read().json(...),   : name")),                  :                           : even though those exist   :
:   :                           : and                       : and Parquet (Spark can    :                           : in broader Spark docs but :
:   :                           : spark.read().parquet(...) : read and write Parquet    :                           : are not fully represented :
:   :                           : ,                         : while preserving schema), :                           : in this extracted corpus. :
:   :                           : with behavior customized  : and explained that these  :                           :                           :
:   :                           : via .option() or          : use spark.read methods    :                           :                           :
:   :                           : .options().               : and can be customized     :                           :                           :
:   :                           :                           : with option(). Cited      :                           :                           :
:   :                           :                           : Documents 12, 9, and 7.   :                           :                           :
: 5 : How to tune               : Either tune               : Explained that for large  : Relevant – retrieval      : Accurate – focuses on     :
:   : spark.sql.shuffle.partiti : spark.sql.shuffle.partiti : joins you should set a    : surfaced the “Optimizing  : AQE-based tuning instead  :
:   : ons                       : ons                       : sufficiently large        : Join Strategy” section    : of manual static          :
:   : for a large join?         : directly via              : initial number of shuffle : describing AQE coalescing : partition count, which    :
:   :                           : spark.conf.set(...), or,  : partitions and enable     : of shuffle partitions,    : matches the guidance in   :
:   :                           : as the docs suggest,      : adaptive query execution  : plus related              : the ingested docs.        :
:   :                           : start with a large        : (spark.sql.adaptive.enabl : join/partition configs.   :                           :
:   :                           : initial partition count   : ed                        :                           :                           :
:   :                           : and let Adaptive Query    : and                       :                           :                           :
:   :                           : Execution coalesce        : spark.sql.adaptive.coales :                           :                           :
:   :                           : partitions using          : cePartitions.enabled),    :                           :                           :
:   :                           : spark.sql.adaptive.coales : letting Spark coalesce    :                           :                           :
:   :                           : cePartitions.*            : post-shuffle partitions   :                           :                           :
:   :                           : settings.                 : based on runtime stats,   :                           :                           :
:   :                           :                           : and mentioned related     :                           :                           :
:   :                           :                           : settings like             :                           :                           :
:   :                           :                           : initialPartitionNum and   :                           :                           :
:   :                           :                           : minPartitionSize. Cited   :                           :                           :
:   :                           :                           : Document 5, chunks 8–9    :                           :                           :
:   :                           :                           : and Document 6.           :                           :                           :
:...:...........................:...........................:...........................:...........................:...........................: -->


<!-- | # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate -->

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

What file formats does Spark natively support and how does it read them?

**What the system returned:**

The system correctly described how to read CSV, JSON, and Parquet using spark.read().csv(), spark.read().json(), and spark.read().parquet(), and mentioned using option() to customize behavior. It did not mention other formats like ORC, text, or Avro that are available in Spark’s full documentation.

**Root cause (tied to a specific pipeline stage):**

The question was broader than the ingested documents: the local documents contains detailed sections for CSV, JSON, Parquet, and some generic load/save options, but does not include full coverage of all possible formats. As a result, retrieval only surfaced chunks about the formats present in documents/spark/Document 9, 10, and 12, and the LLM had no grounded text describing ORC/text/Avro to draw on. This is primarily a document selection / coverage issue, not a chunking or embedding failure.

**What you would change to fix it:**

To fix this, the corpus should be expanded to include the relevant sections from the Spark docs that describe other formats (e.g., ORC, text, Avro) before re‑embedding. Alternatively, the evaluation question could be narrowed to “Which file formats are described in this guide and how does Spark read them?” to better match the scope of the ingested documents.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

The planning.md spec made me determine the chunk sizes, overlap, and top k retrieval in the beginning so I was able to research many techniques and best practices. It became a checklust for testing the system instead of ad-hoc decisions.

**One way your implementation diverged from the spec, and why:**

The "Expected Anwers" in the planning.md file are much broader and encompass the entirety of Spark, which is much more detailed than what I was able to put in 12 documents in the corpus. The reason is that initially, the concepts to cover were much wider than the documentation that was finally extracted.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* The Chunking Strategy, Documents, and Architecture sections from planning.md, along with a description of the documents/spark/ folder and the requirement to use a recursive character splitter with 512‑character chunks and overlap.

- *What it produced:*A Python script layout for an ingest_and_chunk.py module that used RecursiveCharacterTextSplitter with separators ["\n\n", "\n", " ", ""], loaded all .txt files from documents/spark/, applied chunking, and printed sample chunks.

- *What I changed or overrode:* The initial suggestion was 75 characters for overlap and didn’t include metadata like doc_id and chunk_id. I adjusted the overlap to 100 characters to better preserve code blocks, added explicit doc and chunk identifiers to each chunk, idea derived from the initial project in the first class.

**Instance 2**

- *What I gave the AI:* The Retrieval Approach section and a high-level description of how the CLI should work: retrieve top‑5 chunks, build a context block, and call Groq’s llama-3.3-70b-versatile.

- *What it produced:* A scaffold for embed_and_store.py and answer.py that initialized SentenceTransformer("all-MiniLM-L6-v2"), created a persistent Chroma collection, stored chunk embeddings with metadata, and implemented a answer_question() function that combined retrieval and Groq chat completions in a basic CLI loop.

- *What I changed or overrode:* I added a ground system prompt to to require citation for each document, added error handling if the API key was missed, and cleaned output preview in the CLI.

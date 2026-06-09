# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
Spark Documentation; I have been studying Spark for a certification exam and this would be a good source to directly ask questions without having to 
read through the lengthy official documentation.
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->


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



---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->
     I have decided to maintain a chunk size of 512 characters with an overlap of 75 characters.
     However, since some Pyspark code may end up being rather long, I would not want the chunk to slice code blocks in the middle. So I did a little bit of research and discovered that a "Recursive Splitter" is a good idea to ensure that context between code isnt lost. It maintains a priority list which may step back a few characters to ensure an even split, and if code exceeds the standard chunk size of 512 characters, it will split a little cleaner by splitting in a new line rather than at a random character.

**Chunk size:**
     chunk_size = 512 characters
**Overlap:**
     overlap = 75 characters
**Reasoning:**
     512 characters seems to be a good baseline strategy based on the average size of the documents I am using, and using a Recursive Splitting Strategy allows the code to be recorded in a cleaner way.
---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
     sentence-transformers/all-MiniLM-L6-v2, chromadb for vector store
**Top-k:**
     starting with top 5 chunks per query
**Production tradeoff reflection:**
     if cost weren't a constraint, I'd opt for a larger model allowing for longer context windows, and perhaps a domain specific model which would be code-aware or technical-text-tuned model (Apache Spark specific) to better understand code, architecture and configuration.
---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question |
|---|----------|
| 1 |How to programatically define a schema using StructType and StructField in Spark? |
| 2 |What is a global temporary view and how is it different from a temporary view?    |
| 3 |How does Spark SQL cache tables and how to uncache them?                          |
| 4 |What file formats does Spark natively support and how does it read them?          |
| 5 |How to tune spark.sql.shuffle.partitions for a large join?                        | 

| Expected Answers |
Question 1: How to programmatically define a schema using StructType and StructField in Spark?
Expected Answer:To programmatically define a schema, import StructType, StructField, and the desired data types from pyspark.sql.types. Create a StructType object containing a list of StructField objects. Each StructField requires three parameters: the column name (string), the data type (e.g., StringType()), and a boolean indicating if the field is nullable.Example:pythonfrom pyspark.sql.types import StructType, StructField, StringType, IntegerType
schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), False)
])
df = spark.read.schema(schema).json("data.json")

Question 2: What is a global temporary view and how is it different from a temporary view?
Expected Answer:A temporary view is session-scoped and disappears when the specific SparkSession that created it terminates. It cannot be shared across different sessions. A global temporary view is cross-session scoped and remains available across all SparkSessions within the same Spark application until the application terminates. Global temporary views are tied to the system-preserved database global_temp, meaning you must query them using the prefix global_temp.view_name.

Question 3: How does Spark SQL cache tables and how to uncache them?
Expected Answer:Spark SQL caches tables in memory using an in-memory columnar format via the spark.catalog.cacheTable("table_name") method or by running the SQL command CACHE TABLE table_name. Caching is lazy by default, meaning the table is only loaded into memory when an action is executed. To remove a table from memory, use spark.catalog.uncacheTable("table_name") or the SQL command UNCACHE TABLE table_name. 

Question 4: What file formats does Spark natively support and how does it read them?
Expected Answer:Spark natively supports file formats including Parquet, JSON, ORC, CSV, text, and Avro. It reads them using the spark.read DataFrameReader interface. You can specify the format globally using .format("format_name").load("path") or by using format-specific shortcut methods such as .parquet(), .json(), .orc(), and .csv().

Question 5: How to tune spark.sql.shuffle.partitions for a large join?
Expected Answer:By default, spark.sql.shuffle.partitions is set to 200, which is often too small for large joins and causes disk spilling, or too large for small data, causing scheduling overhead. To tune it, you should configure it via your SparkSession configuration before executing the join: spark.conf.set("spark.sql.shuffle.partitions", "desired_number"). A good rule of thumb for large joins is to aim for target post-shuffle partition sizes of roughly 100MB to 200MB of data per partition.
---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. A complex PySpark block (long optimization step or multiple transformations), might exceed the character limit, and since the "actions" in Spark are written at the end of a code block, the trailing action lined might get lost by the AI.

2. Documents 7 through 12 majorly deal with file sources and formats, so if there is a simple search like "How does Spark read files?" may trigger random fragments across multiple chunks simultaneously.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

     # Table generated using: https://ozh.github.io/ascii-tables/     

..............................................................................
: Stage :    Action    :                         Tool                        :
:.......:..............:.....................................................:
: A     : Ingestion    : Python file loader                                  :
: B     : Chunking     : Recursive Character text splitter + 512-char chunks :
: C     : Embedding    : all-MiniLM-L6-v2                                    :
: D     : Vector Store : ChromaDB                                            :
: E     : Retrieval    : Top-k=5                                             :
: F     : Generation   : Groq Llama 3.3 70B                                  :
:.......:..............:.....................................................:




---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
     I shall use Perplexity.ai with my Chunking Strategy and Documents sections to generate a ingest_and_chunk.py that loads all .txt files from documents/spark, applies recursive splitting with 512/75, and prints sample chunks. I’ll verify by manually inspecting 5 random chunks.

**Milestone 4 — Embedding and retrieval:**
     I shall use AI to scaffold code that loads those chunks, embed them with all-MiniLm-L6-v2, and store them in ChromaDB with source metadata, and test retrieval with the evaluation questions.
**Milestone 5 — Generation and interface:**
     I will wire retrieval into Groq's LLM and build a simple interface on Gradio, and 
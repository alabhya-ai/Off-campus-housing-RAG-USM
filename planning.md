# Project 1 Planning: The Unofficial Guide

---

## Domain (Off-Campus Housing Information Agent for University of Southern Mississippi)

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

Starting to look for apartments off-campus is difficult. Decisions seem good until an additional factor is considered. No matter how many sites we visit, there is something that is left to be updated.


---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 |Apartments.com (USM Off-Campus) |For scraping structured tabular data (price ranges, square footage, and distance to campus). | https://www.apartments.com/off-campus-housing/ms/hattiesburg/the-university-of-southern-mississippi/|
| 2 | Zillow (Hattiesburg Rentals)| Finding individual houses for rent in neighborhoods adjacent to campus (like the Avenues), which students frequently recommend over corporate apartments.| https://www.zillow.com/hattiesburg-ms/rentals/|
| 3 | CollegeRentals (Hattiesburg)|Niche aggregator specifically filtering for student-friendly leases.| https://www.collegerentals.com/off-campus-housing/ms/hattiesburg/|
| 4 | Rent.com (Hattiesburg Apartments)|Pulling localized metadata like walk scores and transit options to campus.| https://www.rent.com/mississippi/hattiesburg-apartments|
| 5 |r/hattiesburg Subreddit |Active with housing questions. Target threads specifically mentioning "USM", "moving here", or "apartment suggestion". | https://www.reddit.com/r/hattiesburg/|
| 6 | r/southernmiss Subreddit| Dedicated university subreddit for organic student discussions and recommendations.| https://www.reddit.com/r/southernmiss/|
| 7 | Uloop (USM Campus Classifieds)| Housing listings, sublet offers, roommate requests, and furniture sales.| https://usm.uloop.com/|
| 8 | USM Off-Campus Housing Portal| Lists amenities well; official white-label partnership between the University of Southern Mississippi and Apartments.com.| https://www.usmoffcampushousing.com/housing|
| 9 | ForRentUniversity (USM Portal)| Specialized student listings explicitly featuring walk times to campus.| https://www.forrentuniversity.com/The-University-of-Southern-Mississippi|
| 10 |Reddit Universal Search | Catching cross-subreddit discussions regarding tenant laws, rental safety, and general landlord feedback across Mississippi boards.| https://www.reddit.com/search/?q=renting+hattiesburg|

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 300 tokens

**Overlap:** 30 tokens

**Reasoning:** My corpus either has structured bits of information on particular housing businesses or conversational logs from Reddit. Considering both the complexity I want to go to (which is not too high for this project specifically) and the fact that most information I need will be summed up within approximately 300 tokens worth of content and 30 tokens worth of overlap.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** bge-small-en-v1.5

**Top-k:** 10

**Production tradeoff reflection:**

If cost was not a constraint, I would first move from using a local embedding model like the bge-small-en-v1.5 to an API-based one. OpenAI's text-embedding-3-large came up a lot when I was looking up various embedding models. Another tradeoff I would highly consider would be to do dynamic chunking for my Reddit-based corpus to preserve whole conversations instead of bits of a potential single lengthy post.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | "Which apartments can I comfortably walk to the USM campus from within 25 minutes?"| Beverly Hills, Westgate Apartments, Windridge Apartments, Concorde Apartments etc.|
| 2 | "Which apartments are pet-friendly?"| Officially, The Cottages of Hattiesburg is pet-friendly, featuring wide-open green spaces, sidewalks, and private porches. However, Zillow and official policy documents indicate there are standard breed restrictions and non-refundable pet fees. Anecdotally, students on r/hattiesburg mention that management is relatively relaxed about pet enforcement once you are moved in, but you should still officially register your dog to avoid sudden fines.|
| 3 | "Do I need to buy my own bed and couch if I move into Eagle Flatts?"| No, you do not have to buy your own furniture. According to their USM Off-Campus Housing portal listing, Eagle Flatts offers both furnished and unfurnished options. The furnished packages typically include a bed, dresser, desk, couch, and entertainment center. You will only need to bring your own mattress topper, linens, and kitchenware.|
| 4 | "Is paying $800 a month to live at The Cottages worth it compared to a standard apartment?" | It depends on what you value. According to Apartments.com, paying $800+ per bedroom at The Cottages gives you access to resort-style amenities (private lake, 24/7 clubhouse, pool) and a highly social, gated environment. However, students on Reddit frequently point out that for the same total price ($1,600+ for two people), you can rent an entire standalone house in neighborhoods like The Avenues or West Hattiesburg, getting significantly more square footage and a private yard, albeit without the luxury pool and gym.|
| 5 | "Where do I not need to buy my own furniture?"| The Grande, 2 Square apartments etc.|

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. off-topic retrieval: With the sources I have, it is likely that for some questions, the model will not have anything to pull up the data from.

2. Scraping issues: A lot of data might not even end up correctly formatted inside the locally saved documents

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

1. Document Ingestion
Tools/Libraries: Native Python File I/O (os, open()).

2. Chunking
Tools/Libraries: Native Python string manipulation (.split(), list slicing).

3. Embedding + Vector Store
Tools/Libraries: chromadb (Chroma Vector Database).

Embedding Model: bge-small-en-v1.5 (Sentence Transformers).

4. Retrieval
Tools/Libraries: chromadb Query API.

5. Generation
Tools/Libraries: groq (Groq Python SDK) and gradio.

LLM Model: llama-3.3-70b-versatile

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

I will use Gemini to come up with the sources, and format them into the table that is required in the planning.md file.
I will then use Claude Code (Opus 4.7) to try "spec-driven development" by documenting libraries and constraints properly then letting Claude do its thing.
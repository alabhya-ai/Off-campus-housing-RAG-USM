# The Unofficial Guide — Project 1

---

## Domain (Off-Campus Housing Information Agent for University of Southern Mississippi)

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
Starting to look for apartments off-campus is difficult. Decisions seem good until an additional factor is considered. No matter how many sites we visit, there is something that is left to be updated.
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

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

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 300 tokens

**Overlap:** 30 tokens

**Why these choices fit your documents:** My corpus either has structured bits of information on particular housing businesses or conversational logs from Reddit. Considering both the complexity I want to go to (which is not too high for this project specifically) and the fact that most information I need will be summed up within approximately 300 tokens worth of content and 30 tokens worth of overlap.

**Final chunk count:** 41

**Sample chunks:**

--- 01_apartments_com.txt::0000 ---
source : apartments. com ( usm off - campus ) source _ id : 01 _ apartments _ com url : https : / / www. apartments. com / off - campus - housing / ms / hattiesburg / the - university - of - southern - mississippi / - - - [ fetch failed : http 403 for https : / / www. apartments. com / off - campus - housing / ms / hattiesburg / the - university - of - southern - mississippi / ] apartments. com ag

--- 02_zillow_hattiesburg.txt::0000 ---
source : zillow ( hattiesburg rentals ) source _ id : 02 _ zillow _ hattiesburg url : https : / / www. zillow. com / hattiesburg - ms / rentals / - - - rental listings in hattiesburg ms - 254 rentals | zillow skip main navigation for rent price beds & baths property type filters save search hattiesburg ms rental listings 254 rentals available sort : recommended $ 939 + 1 bd fees may apply caleb pl

--- 02_zillow_hattiesburg.txt::0001 ---
##d $ 800 / mo fees may apply 2 bds 1 ba 800 sqft apartment for rent royal oaks apartment homes, 22 central school rd # 202, hattiesburg, ms 39401 more save $ 1, 367 + 1 bd fees may apply parkwest apartment homes | 12 park pl, hattiesburg, ms save $ 1, 462 + 2bd $ 1, 570 + 3bd $ 1, 237 + 1 bd fees may apply twin oaks | 100 twin oaks ln, hattiesburg, ms save $ 1, 432 + 2bd $ 1, 443 + 3bd loading...

--- 02_zillow_hattiesburg.txt::0002 ---
##tiesburg 2 bedroom apartments hattiesburg 3 bedroom apartments select property types hattiesburg apartments for rent hattiesburg condos for rent hattiesburg townhouses for rent choose apartment by amenity pet friendly apartments in hattiesburg furnished apartments in hattiesburg find speciality housing studio apartments in hattiesburg luxury apartments in hattiesburg cheap apartments in hattiesb

--- 02_zillow_hattiesburg.txt::0003 ---
neighborhood apartments jamestown _ lincoln apartments for rent university heights apartments for rent hattiesburg apartments by zip code 39401 apartments for rent 39402 apartments for rent popular apartment communities in hattiesburg mississippi rental buildings hattiesburg rental buildings reserve at park place apartment homes arbor walk caleb place apartments brookland trace mark vi apartments

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** bge-small-en-v1.5

**Production tradeoff reflection:**

If cost was not a constraint, I would first move from using a local embedding model like the bge-small-en-v1.5 to an API-based one. OpenAI's text-embedding-3-large came up a lot when I was looking up various embedding models. Another tradeoff I would highly consider would be to do dynamic chunking for my Reddit-based corpus to preserve whole conversations instead of bits of a potential single lengthy post. (note that I am using a constraint of top-k=10)

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

    "You are an assistant that answers questions about off-campus housing near "
    "the University of Southern Mississippi (USM) in Hattiesburg, MS. "
    "You must answer using ONLY the information in the CONTEXT block below. "
    "Do not use outside knowledge, do not speculate, and do not invent facts "
    "(apartment names, prices, policies, amenities) that are not present in the context. "
    "If the context does not contain enough information to answer the question, "
    "reply exactly with: \"I don't have enough information on that.\" "
    "When you do answer, cite the source filenames you used inline like "
    "[source: filename.txt] next to each claim. Be concise."

**How source attribution is surfaced in the response:**

Inspired from the way all major LLMs cite their sources, I also instructed my system to generate inline citations in the format "[source: filename.txt]" after information extracted from specific sources.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 |Which apartments can I comfortably walk to the USM campus from within 25 minutes? | Beverly Hills, Westgate Apartments, Windridge Apartments, Concorde Apartments etc.| Without explicit walking times or distances for each apartment, it's difficult to confirm which can be comfortably walked to within 25 minutes. However, based on the descriptions, Claridge House, Village Crossing, 2 Square, and 1 Square Apartment Homes seem to be the closest [source: 07_uloop_usm.txt].| Relevant| Accurate|
| 2 | Which apartments are pet-friendly?| Officially, The Cottages of Hattiesburg is pet-friendly, featuring wide-open green spaces, sidewalks, and private porches. However, Zillow and official policy documents indicate there are standard breed restrictions and non-refundable pet fees. Anecdotally, students on r/hattiesburg mention that management is relatively relaxed about pet enforcement once you are moved in, but you should still officially register your dog to avoid sudden fines.| According to [source: 04_rent_com_hattiesburg.txt], Brittany Arms is a pet-friendly apartment. Additionally, [source: 02_zillow_hattiesburg.txt] mentions "pet friendly apartments in Hattiesburg" as an option, but does not specify particular apartments. [source: 05_reddit_hattiesburg.txt] also mentions "pet friendly apartment" in the context of a failed search, but does not provide specific information. [source: 04_rent_com_hattiesburg.txt] also mentions that The Grande at Timberwood is pet-friendly.| Partially Relevant| Partially Accurate|
| 3 |Do I need to buy my own bed and couch if I move into Eagle Flatts? | No, you do not have to buy your own furniture. According to their USM Off-Campus Housing portal listing, Eagle Flatts offers both furnished and unfurnished options. The furnished packages typically include a bed, dresser, desk, couch, and entertainment center. You will only need to bring your own mattress topper, linens, and kitchenware.| I don't have enough information on that.| Off-target| Inaccurate|
| 4 |Is paying $800 a month to live at The Cottages worth it compared to a standard apartment? | It depends on what you value. According to Apartments.com, paying $800+ per bedroom at The Cottages gives you access to resort-style amenities (private lake, 24/7 clubhouse, pool) and a highly social, gated environment. However, students on Reddit frequently point out that for the same total price ($1,600+ for two people), you can rent an entire standalone house in neighborhoods like The Avenues or West Hattiesburg, getting significantly more square footage and a private yard, albeit without the luxury pool and gym.| I don't have enough information on that.| Off-target| Inaccurate|
| 5 | Where do I not need to buy my own furniture?| The Grande, 2 Square apartments etc.| You do not need to buy your own furniture at The Grande at Timberwood [source: 07_uloop_usm.txt] and Stonewood Crossing Apartment Homes is not mentioned to require furniture, but other apartments like 2 Square Apartment Homes and others do not explicitly state they are furnished [source: 07_uloop_usm.txt, source: 10_uloop_usm is not available but source: 07_uloop_usm.txt and source: 04_rent_com_hattiesburg.txt]. However, Windridge has "modern living • granite countertops • stainless steel appliances" [source: 04_rent_com_hattiesburg.txt] which implies some level of furnishing.| Relevant| Accurate|

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** Is paying $800 a month to live at The Cottages worth it compared to a standard apartment?

**What the system returned:** I don't have enough information on that.

**Root cause (tied to a specific pipeline stage):** The root cause lies in the ingestion stage, or even before that, in the web scraping phase. Some of the "heavy" sources were not properly formatted into txt files.

**What you would change to fix it:** I would change the scraping strategy. If some of the scraping attempts were blocked (which they were), I would simply change the approach to a more manual method. If this were a real production-level project, I would look into scraping licensing from Reddit in set limits per day to properly gather my documents.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** The given spec from CodePath for this project is a highly standardized one. In my own research, I found that these tools/libraries and even the modularity structure for the RAG pipeline is in line with the typical practice in large-scale practices, too. That is what helped me be confident that building this project will help me build AI-engineering proficiency to be prepared for large enterprises. That faith in this project is what these specs helped the most with.

**One way your implementation diverged from the spec, and why:** The scraping part, for which I added BeautifulSoup into the mix, was one thing that differed from the spec. It is because the RAG pipeline I was building relied on large corpuses to be run locally that I needed to specifically bring them into .txt format. For that, I think the different files I made inside the 'scraping' folder sums up the difference.

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

- *What I gave the AI:* (To Gemini) Help me find ten reliable sources I can use for off campus housing near The University of Southern Mississippi.

- *What it produced:* To build your Off-Campus Housing Auditor for The University of Southern Mississippi (located in Hattiesburg, you need a mix of structured listing data (the "official" kind) and unstructured forum data (the "real" kind).

Here are 10 scrapeable sources categorized by the type of data they will feed into your RAG pipeline:

Unstructured Data (The "Real" Knowledge)
This is where you will find the raw student opinions about maintenance response times, hidden fees, and safety.

r/hattiesburg Subreddit: This is highly active with housing questions. Search and scrape threads specifically mentioning "USM", "moving here", or "apartment suggestion".

r/usm Subreddit: The dedicated university subreddit. Look for annual threads asking "where should I live off-campus?"

Google Maps Reviews: Scrape the review text for specific large student complexes. This is where students complain about mold, internet outages, and towing policies.

Direct Property Sites (The "Official" Knowledge)
Scraping these sites gives you the baseline facts (floor plans, rent prices, amenities) to contrast against the Reddit complaints. These are the major student-focused complexes near campus:

The Cottages of Hattiesburg
This is a massive, cottage-style student housing community heavily discussed on local forums.

Scrape their "Floor Plans" and "Amenities" pages to pull structured data on their 2-to-5-bedroom layouts.

Extract their listed pet policies and utility inclusions.

Eagle Flatts
Another prominent student-specific complex located extremely close to campus.

Scrape their FAQ and policy pages regarding individual leases and roommate matching services.

Pull their specific amenity list (e.g., 1 GB fiber optic internet) to answer queries about Wi-Fi reliability.

Ivy Row at Hattiesburg
A newer townhome and cottage community targeted at students.

Scrape the specific square footage and bed/bath ratios for their multi-story layouts.

Extract data on their private study rooms and en-suite bathroom policies.

Aggregator Listing Sites (Structured Data)
These sites will give you a broad overview of the smaller, non-corporate housing options (like rented houses and older duplexes) that upperclassmen often prefer.

Apartments.com (USM Off-Campus Page): Excellent for scraping structured tabular data (price ranges, square footage, and distance to campus).

Zillow (Hattiesburg Rentals): Useful for finding individual houses for rent in neighborhoods adjacent to campus (like the Avenues), which students frequently recommend over corporate apartments.

CollegeRentals.com (Hattiesburg): A niche aggregator specifically filtering for student-friendly leases.

Rent.com (USM Filter): Good for pulling localized metadata like walk scores and transit options to campus.

Are you planning to write custom scrapers using BeautifulSoup/Playwright for this, or use an off-the-shelf scraping API?

Write custom scraper code

List web scraping APIs

Design the RAG architecture
- *What I changed or overrode:* I started building my source list from here

**Instance 2**

- *What I gave the AI:* (To Gemini) generate a list of 10 questions and answers I would expect from my RAG.

- *What it produced:* Here is a list of 10 highly realistic questions and answers you should expect your RAG pipeline to generate, specifically tailored to the University of Southern Mississippi (USM) student housing market.

These examples demonstrate how a well-engineered RAG pipeline synthesizes structured listing data (price, distance, amenities) with the unstructured "real" knowledge from student forums (Reddit, Uloop).

1. The "Hidden Fee" Query
Question: "Are utilities included at The Cottages, or are there hidden fees I should know about?"
Expected RAG Answer: "According to official listings on Apartments.com, The Cottages of Hattiesburg advertises 'all-inclusive monthly payments' and includes high-speed internet in the base rent. However, multiple threads on r/southernmiss and r/hattiesburg warn that electricity is subject to a usage cap. Students report frequently facing $30 to $50 monthly overage charges during the summer months due to drafty windows and high air conditioning use."

2. The Commute/Walkability Query
Question: "Can I comfortably walk to the USM business building from Eagle Flatts?"
Expected RAG Answer: "Yes, Eagle Flatts is highly walkable. Official listings note it is located at 105 Doleac Drive, which is directly adjacent to the USM campus. Reviewers on Rent.com and student comments on Reddit confirm the walk takes roughly 5 to 10 minutes depending on your pace. Many students explicitly recommend Eagle Flatts over complexes across Highway 49 if you do not have a car."

3. The Internet Reliability Query (Crucial for CS Students)
Question: "Which off-campus apartment has the most reliable Wi-Fi for gaming and coding?"
Expected RAG Answer: "Eagle Flatts heavily advertises a newly upgraded '1 GB fiber optic internet' connection in their official promotional materials and Zillow listings. Student consensus on Reddit generally supports this, noting the speeds are highly reliable for gaming. In contrast, while The Cottages includes internet in their rent, several Uloop sublet listings and Reddit complaints mention occasional dropouts and throttled speeds during peak evening hours."

4. The Sublease/Desperation Query
Question: "I need to get out of my lease early. Which platforms are best for finding a subleaser in Hattiesburg?"
Expected RAG Answer: "Based on local student behavior, you should post your listing on Uloop's USM portal and the 'USM Roommates, Subleases & Off-Campus Housing' Facebook groups. Uloop is heavily trafficked for mid-semester lease takeovers. Additionally, be aware that complexes like Eagle Flatts and The Cottages use individual 'by-the-bed' leases. You will likely have to pay a lease-transfer fee to the management company once you find a replacement tenant."

5. The Pet Policy & Reality Query
Question: "How pet-friendly is The Cottages, really? Do they strictly enforce breed restrictions?"
Expected RAG Answer: "Officially, The Cottages of Hattiesburg is pet-friendly, featuring wide-open green spaces, sidewalks, and private porches. However, Zillow and official policy documents indicate there are standard breed restrictions and non-refundable pet fees. Anecdotally, students on r/hattiesburg mention that management is relatively relaxed about pet enforcement once you are moved in, but you should still officially register your dog to avoid sudden fines."

6. The Furniture/Move-in Query
Question: "Do I need to buy my own bed and couch if I move into Eagle Flatts?"
Expected RAG Answer: "No, you do not have to buy your own furniture. According to their USM Off-Campus Housing portal listing, Eagle Flatts offers both furnished and unfurnished options. The furnished packages typically include a bed, dresser, desk, couch, and entertainment center. You will only need to bring your own mattress topper, linens, and kitchenware."

7. The Roommate Matching Query
Question: "I'm transferring to USM knowing nobody. How does roommate matching work at the big student complexes?"
Expected RAG Answer: "Complexes like Eagle Flatts and The Cottages use a 'roommate matching service' paired with individual leases. This means you only sign a lease for your specific bedroom and bathroom, so you are not financially liable if your randomly assigned roommate misses rent. You will fill out a lifestyle questionnaire (asking about study habits, cleanliness, and sleep schedules) and management will assign you to an open 2, 3, or 4-bedroom unit."

8. The Maintenance/Mold Query
Question: "Which apartments near USM have a bad reputation for maintenance ignoring mold?"
Expected RAG Answer: "Note: Your RAG will pull specific answers here based on what you scrape. A typical response would look like this:"
"While corporate websites advertise '24-hour emergency maintenance,' unstructured data from Google Reviews and r/hattiesburg indicates persistent complaints about mold at [Specific Complex Name]. Students report that maintenance often paints over water damage rather than fixing the underlying leaks, particularly in the older ground-floor units."

9. The Neighborhood Safety Query
Question: "Is living in 'The Avenues' safer than living in a massive student complex?"
Expected RAG Answer: "The Avenues is a historic, highly residential neighborhood east of campus. Zillow and CollegeRentals show many independent houses for rent here. Students on r/southernmiss often describe The Avenues as quieter and more 'homely' than massive complexes. However, because it is an older, mixed-income urban neighborhood rather than a gated student fortress (like The Cottages), students advise locking car doors and being mindful of petty property crime, which occasionally appears in Hattiesburg Police dispatch summaries."

10. The Price vs. Value Query
Question: "Is paying $800 a month to live at The Cottages worth it compared to a standard apartment?"
Expected RAG Answer: "It depends on what you value. According to Apartments.com, paying $800+ per bedroom at The Cottages gives you access to resort-style amenities (private lake, 24/7 clubhouse, pool) and a highly social, gated environment. However, students on Reddit frequently point out that for the same total price ($1,600+ for two people), you can rent an entire standalone house in neighborhoods like The Avenues or West Hattiesburg, getting significantly more square footage and a private yard, albeit without the luxury pool and gym."
- *What I changed or overrode:* I hand-picked some ideas for validation questions from this list. It was a diverse list, which helped me evaluate my system and learn more about RAG in general.

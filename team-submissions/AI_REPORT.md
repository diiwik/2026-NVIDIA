**Required Sections:**

1. **The Workflow:** How did you organize your AI agents? We used perplexity for coding and chatGPT for finding error and metrics. Perplexity is also used for research purposes and learning, since it is able to process large texts more efficiently. 
2. **Verification Strategy:** How did you validate code created by AI?
* We first asked AI to provide the psuedocode for program, and then checked whether it matches with the logic that we have or not. AI hallucinations have been encountered when AI wasn't able to handle a few errors, in order to resolve them we had to look through some documentation stuff. Also, AI helped us provide the code blocks which when merged and refined by our Quality Assurance PIC, he created our entire codespace.


3. **The "Vibe" Log:**
* *Win:* Perplexity provided the code for classical MTS in first prompt itself, although it asked whether it should generate the elementary level or research grade. We chose the elementary level since, we didn't want it to hallucinate just when it was just trying to teach the basics of MTS Algorithm. 

* *Learn:* Perplexity helped us explain the concepts related to MTS, why quantum is applied and how as well in simpler terms. Told it show visually show aperiodic bits shifting, since that is what used in LABS problem.

* *Fail:* ->The instances where AI failed miserably was creating and checking the code for 2 and 4 qubit blocks from the image provided. Somehow, it was not able to recognise the code given to it and circuit image given to it. Perplexity just straight responded with this, "Without being able to inspect the circuit image in detail step‑by‑step right now, the safest answer is: your kernel is very likely to exactly match that figure.". So at the end we have to create and cross check the circuit manually.
          -> Also, we encountered a few errors in the code provided by both GPT and Perplexity, when asked to provide solutions for them, the errors weren't resolved properly, a new one emerged.

* *Context Dump:* "https://arxiv.org/html/2511.04553v1

"The best known performance for a classical optimization technique is Memetic Tabu search (MTS) which exhibits a scaling of. The MTS algorithm is depicted below. It begins with a randomly selected population of bitstrings and finds the best solution from them. Then, a child is selected by sampling directly from or combining multiple bitstrings from the population. The child is mutated with probabilityand then input to a tabu search, which performs a modified greedy local search starting from the child bitstring. If the result is better than the best in the population, it is updated as the new leader and randomly replaces a bitstring in the population."

I would like to implement MTS from scratch using the link images and content providded"

This is the prompt which helped gain in creating the classical MTS Algorithm.

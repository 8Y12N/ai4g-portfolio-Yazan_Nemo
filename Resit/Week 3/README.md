# Term 1 - Week 4: Strings, Text & Files

---

## 1. Homework & workshop assignments -> [`homework/`](homework/)

**What was the assignment?**
Workshop on Python lists and dictionaries, applied to AI for Good contexts (food bank inventory, wage gap analysis, city services mapping). Final part: first API calls to Gemini, including a reflection on when AI gives wrong or inconsistent answers.

**What did I hand in?**
completed homework nootbook vor week 3 with all exercises (1-4), the Food Bank Manager assignment, and written reflections.

**What did I find difficult, and how did I solve it?**
Nothing, I found every thing understandable

### Checklist
- [x] My workshop / homework files are in `homework/`
- [x] Everything runs without errors

---

## 2. Hackathon prototype -> [`hackathon/`](hackathon/)

> Your tool and your SDG for this hackathon are announced at the **start of Friday's class**.
> Write them down here once you know them.

**Project title:** Plainpaper

**My pair partner:** None (solo)

**Tool we had to use:** Gemini API (LLM API via Python)

**SDG we had to address:** SDG 10 - Reduced Inequalities

What problem does it solve, and for whom?
IT/CS students at universities in countries with outdated curricula are cut off from modern knowledge. Their programs may still teach legacy frameworks and standards, and rarely cover the newest papers on AI, neural networks, or software engineering. The papers themselves are freely available (arXiv, open access journals), but they are written in dense academic English full of jargon, passive voice, and assumed background knowledge that these students were never taught.

This is not a hypothetical gap:

Non-native English speakers need up to 91% more time to read a scientific paper compared to native speakers, and are 2.5x more likely to have their papers rejected for language quality alone (Amano et al., 2023, “The manifold costs of being a non-native English speaker in science”, PLOS Biology).
Students exposed to concepts in plain language first produced 1.5 to 2.5x more correct conceptual arguments than those taught jargon and concepts together (McDonnell, Barker & Wieman, 2016, “Concepts first, jargon second improves student articulation of understanding”, Biochemistry and Molecular Biology Education, 44(1), 12-19).
Computing curricula in many developing-country universities are severely outdated, in some cases dating from the mainframe era, producing graduates who lack the skills required by modern industry (Bass & Heeks, 2011, “Changing Computing Curricula in African Universities”, Electronic Journal of Information Systems in Developing Countries, 48(1), 1-39).
In a survey of environmental scientists across 8 countries, researchers from low-proficiency countries spent about 50% more time writing papers and sought proofreading help 50% more often than native speakers (same Amano et al. study).

**User group:**

Primary user: IT/CS bachelor students at universities in countries where the curriculum is outdated and does not keep up with modern standards, practices, and research.
Secondary user: Non-native English speaking IT students in EU universities who struggle with jargon-heavy academic writing.
Conditions: Has internet access, a laptop, and working English proficiency (at least reading level).
Not for: K-12 students, non-IT majors, anyone needing native-language translation, medical/legal professionals.

**What did you build?**
A web application (FastAPI backend + Vue.js frontend) where students paste text or upload a PDF of an academic paper. The tool:

Checks the domain (fast LLM call: is this an IT/CS paper? If not, shows a soft warning)
Rewrites prose section-by-section in plain English, preserving original headings
Preserves all math, formulas, and algorithms untouched
Shows original vs. simplified side-by-side for verification
Builds a persistent glossary bank (SQLite) of jargon terms that accumulates across papers

**How it works internally:**

User input (paste text or upload PDF)
  -> PDF parsed with pdfplumber (layout=True for multi-column papers)
  -> Domain check: first 1500 chars sent to Gemini ("Is this IT/CS? YES/NO")
  -> Simplifier: full text sent to Gemini, returns structured JSON
     (sections with heading + original + simplified, plus glossary terms)
  -> Glossary terms saved to SQLite (overwrite on duplicate)
  -> Frontend renders side-by-side view + glossary drawer with search

Tech stack: Python, FastAPI, pdfplumber, google-genai SDK, Vue 3, SQLite, Gemini API (gemini-3.1-flash-lite)

Link to the live thing (if any): https://youtu.be/vY8uKPEgCg8
Screen recording in presentation/

**How do I run it?**
1. Clone the repo
2. `pip install -r requirements.txt`
3. Create a `.env` file with `GEMINI_API_KEY=your_key_here`
4. `uvicorn main:app --reload`
5. Open http://127.0.0.1:8000

As a reader, you should use your own Gemini key (in case you have one). I highlighted this in the instructions for more awareness

Requirements: Python 3.9+, a Gemini API key (free tier works).

**Who did what?**
I built the entire project solo: backend (FastAPI + simplifier + glossary DB), frontend (Vue.js), prompt engineering, and documentation.

**Ethical reflection, what are the risks of your tool? Who could it harm?**

Risk 1: Silent meaning distortion
The biggest risk is that the AI quietly changes the meaning of a sentence without the student realizing. It might drop an important detail, weaken a strong claim, or make something sound more certain than the original paper intended. For example, “may correlate with” could become “causes.” If a student then uses or cites the simplified version, they would be spreading wrong information. Even the best-performing LLMs produced fully consistent summaries only about 40% of the time in the FaithBench benchmark (Bao et al., 2024, “FaithBench: A Diverse Hallucination Benchmark for Summarization by Modern LLMs”, NAACL). The risk is highest for students who cannot verify accuracy themselves, which is exactly the target group.

Mitigation: Side-by-side original vs. simplified view lets students spot-check every section against the source text. Math and algorithms are explicitly left untouched by the prompt, reducing the chance of technical distortion.

Risk 2: Over-reliance and skipping the original
Students may trust the simplified version entirely and never read the original paper. The tool is designed as a bridge to understanding, not a replacement for reading. But if students treat it as a shortcut, they miss nuance, context, and the skill of reading academic writing itself, which they will need throughout their careers.

Mitigation: The tool shows the original text alongside the simplification (toggle, not hidden). It does not summarize: it restructures section by section, so the student still engages with the full paper structure.

Risk 3: Language bias in simplification
The tool simplifies into English only. Students whose English is weak may still misunderstand the simplified version, but now with false confidence that they understood it. The tool currently does not support output in any other language, meaning it still excludes students with very low English proficiency, the exact group SDG 10 aims to reach.

Mitigation: Currently unmitigated. The tool is scoped to students with at least working English reading proficiency. A future version could support multi-language output, but that introduces its own accuracy risks (translating simplified text adds another layer where meaning can drift).

Remaining gap: The tool currently offers no automated detection of confidently wrong simplifications. Side-by-side helps, but only if the student actually reads both columns. A future improvement could flag sentences containing statistics or causal claims for mandatory review.

### Checklist
- [ X ]  Prototype code (or export / workflow file) is in `hackathon/`
- [ X ] This week's slides are in `hackathon/`
- [ ] The prototype actually runs, and I wrote down how to run it
- [ X ] Ethical reflection written above

---

## 3. Presentation -> [`presentation/`](presentation/)

*Only fill this in for the week your group was selected to present. You need at least **one** of these across the whole term.*

- [ ] My group presented in this week
- [ X ] Slides are in `presentation/`
- [ X ] Proof of the live demo is in `presentation/` (recording, screenshots, or link)

**How did it go? What would I do differently next time?**

---

## 4. Reflection

**What is the most important thing I learned this week?**
That connecting AI to SDG 10 (Reduced Inequalities) is harder than it sounds. Inequality isn't a technical problem you can just throw an API at — you have to really think about who is being left behind and why, and then figure out if AI can actually help with that specific gap. It took a lot of back-and-forth to go from "let's do something with education" to a concrete, scoped tool that addresses a real problem for a real user group.

Beyond that, I learned that building an LLM-powered tool is not really about the API call — the API does the same thing ChatGPT already does. The actual work is everything you wrap around it: deciding what input to accept, how to structure the output, what safety nets to build in (like side-by-side verification), and what to explicitly refuse to do (like simplifying math, because that would cause more harm than good). I also underestimated how much prompt engineering matters. Small changes in how you phrase the instructions to the model completely change the quality and consistency of what comes back.

**Where does this connect to "AI for Good"?**
There are IT students around the world where the course materials, textbooks, and university resources are outdated or underdeveloped. These students don't have access to the same quality of education as students in well-funded EU or US universities, but the academic papers describing the newest techniques in neural networks, software engineering, and AI are publicly available, they're just written in a way that's nearly impossible to understand without the right background. Plainpaper helps bridge that gap: a student in a less-resourced university can now upload a paper about e.g the latest processing techniques and actually understand what it's saying, without needing a professor to walk them through it. That's a direct reduction in educational inequality.

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

**My pair partner:** None

**Tool we had to use:** Gemini API (LLM API via Python)

**SDG we had to address:** SDG 10 — Reduced Inequalities

**What problem does it solve, and for whom?**
Academic papers use jargon, passive voice, and assume background knowledge that bachelor IT students, especially non-native English speakers and students from countries with less-developed course materials, often don't have. Research shows plain-language-first exposure leads to 1.5–2.5x more correct conceptual arguments (McDonnell, Barker & Wieman, 2016). Plainpaper makes papers accessible without dumbing down the technical content.

**What did you build?**
A web app (FastAPI) where students paste text or upload a PDF of an academic paper. The tool rewrites the prose section-by-section in plain English, preserves all math/algorithms untouched, shows original vs. simplified side-by-side for verification, and builds a persistent glossary bank of jargon terms across papers.

**Link to the live thing (if any):**
None

**How do I run it?**
Local

**Who did what?**
I've build the project with my own

**Ethical reflection — what are the risks of your tool? Who could it harm?**
The biggest risk is that the AI quietly changes the meaning of a sentence without the student realizing. It might drop an important detail, weaken a strong claim, or make something sound more certain than the original paper intended. For example, "may correlate with" could become "causes." If a student then uses or cites the simplified version, they'd be spreading wrong information.

I mitigate this with:
(1) side-by-side original vs. simplified view, so students can always verify against the source text
(2) math and algorithms are explicitly left untouched by the prompt, reducing the chance of technical distortion
(3) a domain guard that warns when the input isn't an IT/CS paper, since the tool is not designed to handle medical, legal, or other high-stakes domains where simplification errors could cause real harm.

A remaining risk I haven't fully solved: the tool currently offers no way to detect when the LLM confidently produces a wrong simplification. Side-by-side helps, but only if the student actually reads both columns. A future improvement could flag high-risk sentences (e.g. those containing statistics or causal claims) for mandatory review.

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

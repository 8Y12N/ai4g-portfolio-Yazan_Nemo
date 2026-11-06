# Term 1 - Week 7: Computer Vision

---

## 1. Homework & workshop assignments -> [`homework/`](homework/)

**What was the assignment?**

**What did I hand in?**
_List the files, or link to them. Notebook exports, screenshots, scripts._

**What did I find difficult, and how did I solve it?**

### Checklist
- [ ] My workshop / homework files are in `homework/`
- [ ] Everything runs without errors, or I explained what does not and why

---


## 2. Hackathon prototype -> [`hackathon/`](hackathon/)

**Project title:** Waterbird Counter: detecting and counting waterbirds at Dutch city ponds

**My pair partner:** Meggie Raaphorst

**Tool we had to use:** Roboflow (RF DETR Small, object detection)

**SDG we had to address:** SDG 15, Life on Land

**What problem does it solve, and for whom?**
The real problem is speed. Nature can only be protected if declines are noticed in time, and in the Netherlands that depends on volunteer counters (for example the thousands of Sovon volunteers) who count waterbirds by eye. With large groups on moving water this is slow and unreliable: birds are missed or counted twice, and it takes a long time before counts are collected and trends become visible. By then, the moment to act may already be gone.

How big the problem is: according to the WWF Living Planet Report 2024, monitored wildlife populations declined by 73% on average between 1970 and 2020. Freshwater populations declined the most, by 85%, and Europe and Central Asia saw a 35% decline. Population declines are an early warning signal for ecosystems, but only if they are measured quickly and consistently.

Our app speeds up this process. A volunteer takes one photo and gets a count per species within seconds, saved per location and date. Because data comes in faster and more consistently, unusual patterns such as a sudden drop in coots, a disease outbreak or a growing number of exotic Egyptian geese can be spotted earlier, so organisations and municipalities can act earlier. That is also why we count all three species and not only the Egyptian goose: a decline in native species like the mallard (around 250,000 breeding pairs in the Netherlands) or the coot is exactly the early signal that something is wrong in the water.

**What did you build?**
A Streamlit app where a user uploads a pond photo and gets boxes around every mallard, coot and Egyptian goose, plus a count per species. Egyptian geese are flagged as exotic. Counts can be saved per location in a log and downloaded as CSV, so counts can be compared over time.

**Link to the live thing (if any):**
The app runs locally (see below) and is shown in a live demo recording that we shared with Rik via teams, it will also be available in the presentation folder in .mov format. The slides are in the presentation folder in PPTX and PDF format.

**How do I run it?**
1. Create a .env file in the hackathon folder based on .env.example (Roboflow API key and model ID)
2. Open run_app.py in VS Code and press Run (or via the terminal). It installs the requirements and opens the app in your browser.

**Who did what?**
Yazan: filmed the dataset, frame extraction, model training and evaluation, Streamlit app, problem analysis.
Meggie: labelling the images, the presentation, README, ethical reflection.
The app code was generated with AI (Claude) and tested and reviewed by us.

**Ethical reflection: what are the risks of your tool? Who could it harm?**
Our dataset is 4 short videos from ponds in The Hague (around 320 frames) plus around 40 images scraped from the internet. Our first model scored 89.6% mAP@50 but failed on new photos (coots labelled as mallards), because frames from the same videos were in both the training and test data. Extra targeted data raised coot from 65% to 81%, but the model only knows 3 species, so other birds get miscounted, and it was trained on a few ponds in autumn daylight only.

The bigger risks are not technical but social. Counts can steer policy and money: if coots are systematically undercounted, a stable population can look like it is declining, and conservation effort goes to the wrong place. Egyptian geese are sometimes actively controlled, so a false detection could support measures against birds that were never there, which hurts the animals and the trust in the data. Volunteers could start trusting the app too much and stop checking by eye, which makes errors harder to catch. Photos of parks can also contain people who never agreed to be photographed, so the app stores counts only and never images. The ones who benefit are volunteers and nature organisations, who get faster data; the ones who could be harmed are the birds and the people affected by decisions based on wrong counts. That is why the app shows its limitations, and why the model only assists: the volunteer checks every count and stays accountable for what is reported.

### Checklist
- [x] Prototype code (or export / workflow file) is in `hackathon/`
- [ ] This week's slides are in `hackathon/`
- [x] The prototype actually runs, and I wrote down how to run it
- [x] Ethical reflection written above

---

## 3. Presentation -> [`presentation/`](presentation/)

- [ ] My group presented in this week
- [ ] Slides are in `presentation/`
- [ ] Proof of the live demo is in `presentation/` (recording, screenshots, or link)

**How did it go? What would I do differently next time?**
[Fill in only if selected on Friday]

---

## 4. Reflection

**What is the most important thing I learned this week?**
A high test score does not mean a model works. Our model scored ~90% but failed on photos from outside our own videos. Testing on truly unseen data exposed overfitting, and adding targeted data for the weakest class fixed it.

**Where does this connect to "AI for Good"?**
Conservation decisions depend on reliable counts. A tool that helps volunteers count faster only does good if its errors are known and checked by a human; otherwise it can push nature policy in the wrong direction.

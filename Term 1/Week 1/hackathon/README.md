# The Socratic Method

**Learn How to Think, Not What to Think**

## What it does
The Socratic Method is a web app that trains critical thinking through structured dialogue. Users pick one of 8 essential questions taken directly from Plato's dialogues (e.g. "What is true justice?" from The Republic, "Can virtue be taught?" from Meno). After writing their own honest definition, Socrates cross-examines that answer with 3-4 short counter-examples, never lecturing, only asking questions. At the end, a summary screen shows the user's original definition next to their refined one, along with the fallacies they avoided along the way.

Each question includes the exact academic citation (e.g. Republic I, 331e-336a), so the challenges are grounded in real historical dialogues rather than invented scenarios.

The app is built with React and Tailwind CSS, with a built-in fallback response engine so it always works, even without an external AI API key.

## Who it's for
Learners who want to practice examining their own assumptions about ethics, justice, courage, and truth, rather than just reading about philosophy. It suits people comfortable with short, focused written exchanges and willing to be challenged.

It is not built for younger learners, people looking for quick answers or reassurance, or users who are not fluent in English, since the dialogue depends on precise language and classical references.

## SDG 4: Quality Education
Most educational tools deliver information for the user to absorb. This app targets a different gap: helping people practice questioning their own reasoning, a skill that reading alone does not build. Each of the 8 challenges tests a specific common mistake in reasoning (e.g. confusing having an opinion with having the truth, in the Theaetetus-based question), so users leave having actively defended and revised a position, not just consumed content.

## How to run it
1. Open the app link: https://bolt.new/p/70633275
2. Pick one of the 8 questions from the question gallery
3. Write your own definition when prompted
4. Respond to Socrates' counter-examples for 3-4 exchanges
5. Review your original vs. refined answer on the final summary screen

Optional: open Settings and add an OpenAI, Gemini, or Anthropic API key for fully dynamic responses. Without a key, the app automatically uses its built-in fallback engine, so it never crashes or stalls.

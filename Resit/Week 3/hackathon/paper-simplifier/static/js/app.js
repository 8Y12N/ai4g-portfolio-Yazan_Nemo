const { createApp, ref, computed, onMounted } = Vue;

createApp({
  setup() {
    // ---- state ----
    const mode = ref("paste");        // "paste" | "upload"
    const pastedText = ref("");
    const file = ref(null);
    const dragOver = ref(false);

    const loading = ref(false);
    const loadingMsg = ref("Reading the paper…");
    const loadingMsgs = [
      "Reading the paper…",
      "Untangling the jargon…",
      "Leaving the math alone…",
      "Writing it in plain English…",
    ];
    let loadingTimer = null;

    const error = ref("");
    const domainWarning = ref("");
    const sections = ref([]);
    const activeSection = ref(0);
    const showOriginal = ref({});

    const glossaryOpen = ref(false);
    const glossary = ref([]);
    const glossaryLoading = ref(false);
    const glossarySearch = ref("");

    const hasResult = computed(() => sections.value.length > 0);
    const filteredGlossary = computed(() => {
      const q = glossarySearch.value.trim().toLowerCase();
      if (!q) return glossary.value;
      return glossary.value.filter(g =>
        g.term.toLowerCase().includes(q) || g.definition.toLowerCase().includes(q)
      );
    });

    // ---- loading message rotation ----
    function startLoading() {
      loading.value = true;
      let i = 0;
      loadingMsg.value = loadingMsgs[0];
      loadingTimer = setInterval(() => {
        i = (i + 1) % loadingMsgs.length;
        loadingMsg.value = loadingMsgs[i];
      }, 1800);
    }
    function stopLoading() {
      loading.value = false;
      clearInterval(loadingTimer);
    }

    // ---- file handling ----
    function onFileChange(e) {
      const f = e.target.files[0];
      if (f) file.value = f;
    }
    function onDrop(e) {
      e.preventDefault();
      dragOver.value = false;
      const f = e.dataTransfer.files[0];
      if (f && f.type === "application/pdf") file.value = f;
    }
    function clearFile() {
      file.value = null;
    }

    // ---- submit ----
    async function submit() {
      error.value = "";
      domainWarning.value = "";
      sections.value = [];
      showOriginal.value = {};

      const form = new FormData();
      if (mode.value === "upload") {
        if (!file.value) { error.value = "Add a PDF first."; return; }
        form.append("file", file.value);
      } else {
        if (!pastedText.value.trim()) { error.value = "Paste some text first."; return; }
        form.append("text", pastedText.value);
      }

      startLoading();
      try {
        const res = await fetch("/simplify", { method: "POST", body: form });
        const data = await res.json();
        if (!res.ok) {
          error.value = data.error || "Something went wrong.";
          return;
        }
        domainWarning.value = data.domain_warning || "";
        sections.value = data.sections || [];
        activeSection.value = 0;
        if (data.glossary && data.glossary.length) fetchGlossary();
      } catch (e) {
        error.value = "Couldn't reach the server.";
      } finally {
        stopLoading();
      }
    }

    // ---- glossary ----
    async function fetchGlossary() {
      glossaryLoading.value = true;
      try {
        const res = await fetch("/glossary");
        glossary.value = await res.json();
      } catch (e) {
        // silent — glossary is secondary
      } finally {
        glossaryLoading.value = false;
      }
    }
    function toggleGlossary() {
      glossaryOpen.value = !glossaryOpen.value;
      if (glossaryOpen.value && glossary.value.length === 0) fetchGlossary();
    }

    function toggleOriginal(i) {
      showOriginal.value[i] = !showOriginal.value[i];
    }

    onMounted(fetchGlossary);

    return {
      mode, pastedText, file, dragOver,
      loading, loadingMsg, error, domainWarning, sections, activeSection, showOriginal, hasResult,
      glossaryOpen, glossary, glossaryLoading, glossarySearch, filteredGlossary,
      onFileChange, onDrop, clearFile, submit, toggleGlossary, toggleOriginal,
    };
  },

  template: `
  <div class="shell">
    <header class="topbar">
      <div class="brand">
        <span class="brand-mark">§</span>
        <span class="brand-name">Plainpaper</span>
      </div>
      <button class="glossary-btn" @click="toggleGlossary">
        Glossary <span class="badge" v-if="glossary.length">{{ glossary.length }}</span>
      </button>
    </header>

    <main class="layout">
      <!-- INPUT PANEL -->
      <section class="panel input-panel">
        <div class="tabs">
          <button :class="['tab', mode==='paste' && 'active']" @click="mode='paste'">Paste text</button>
          <button :class="['tab', mode==='upload' && 'active']" @click="mode='upload'">Upload PDF</button>
        </div>

        <div v-if="mode==='paste'" class="input-area">
          <textarea v-model="pastedText" placeholder="Paste the paper's text here…"></textarea>
        </div>

        <div v-else class="input-area">
          <label
            class="dropzone"
            :class="{ over: dragOver }"
            @dragover.prevent="dragOver=true"
            @dragleave.prevent="dragOver=false"
            @drop="onDrop"
          >
            <input type="file" accept="application/pdf" @change="onFileChange" hidden>
            <template v-if="!file">
              <span class="drop-icon">↥</span>
              <span>Drop a PDF here, or click to browse</span>
            </template>
            <template v-else>
              <span class="file-chip">
                {{ file.name }}
                <button @click.prevent="clearFile">×</button>
              </span>
            </template>
          </label>
        </div>

        <p class="error" v-if="error">{{ error }}</p>

        <button class="submit-btn" @click="submit" :disabled="loading">
          <span v-if="!loading">Simplify paper</span>
          <span v-else class="loading-inline"><i class="spinner"></i>{{ loadingMsg }}</span>
        </button>
      </section>

      <!-- RESULTS PANEL -->
      <section class="panel results-panel">
        <div v-if="loading" class="loading-state">
          <i class="spinner big"></i>
          <p>{{ loadingMsg }}</p>
        </div>

        <div v-else-if="!hasResult" class="empty-state">
          <span class="empty-mark">¶</span>
          <p>Simplified sections will appear here, heading by heading.</p>
        </div>

        <div v-else class="results">
          <div class="warning" v-if="domainWarning">{{ domainWarning }}</div>

          <div class="results-body">
            <nav class="section-nav">
              <button
                v-for="(s, i) in sections" :key="i"
                :class="['section-tab', activeSection===i && 'active']"
                @click="activeSection=i"
              >{{ s.heading }}</button>
            </nav>

            <article class="section-content" v-if="sections[activeSection]">
              <div class="section-toggle">
                <button @click="toggleOriginal(activeSection)">
                  {{ showOriginal[activeSection] ? 'Show simplified' : 'Show original' }}
                </button>
              </div>
              <p class="section-text" :class="{ original: showOriginal[activeSection] }">
                {{ showOriginal[activeSection] ? sections[activeSection].original : sections[activeSection].simplified }}
              </p>
            </article>
          </div>
        </div>
      </section>
    </main>

    <!-- GLOSSARY DRAWER -->
    <div class="drawer-backdrop" v-if="glossaryOpen" @click="toggleGlossary"></div>
    <aside class="drawer" :class="{ open: glossaryOpen }">
      <div class="drawer-head">
        <h2>Glossary</h2>
        <button class="close-btn" @click="toggleGlossary">×</button>
      </div>
      <input class="drawer-search" v-model="glossarySearch" placeholder="Search terms…">
      <div class="drawer-body">
        <div v-if="glossaryLoading" class="loading-state small"><i class="spinner"></i></div>
        <div v-else-if="filteredGlossary.length===0" class="empty-state small">
          <p>No terms saved yet.</p>
        </div>
        <dl v-else class="glossary-list">
          <div class="glossary-item" v-for="g in filteredGlossary" :key="g.term">
            <dt>{{ g.term }}</dt>
            <dd>{{ g.definition }}</dd>
            <span class="glossary-source" v-if="g.source_paper">{{ g.source_paper }}</span>
          </div>
        </dl>
      </div>
    </aside>
  </div>
  `,
}).mount("#app");
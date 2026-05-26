// Persistência de progresso via localStorage + UI dos botões Likert/NPS
(function () {
  const form = document.getElementById("form-medidor");
  if (!form) return;
  const storageKey = form.dataset.storageKey;
  const progressBar = document.querySelector(".progress-bar__fill");
  const savedPill = document.getElementById("saved-pill");

  // ── restaura
  try {
    const saved = JSON.parse(localStorage.getItem(storageKey) || "{}");
    Object.entries(saved).forEach(([name, value]) => {
      const inputs = form.querySelectorAll(`[name="${CSS.escape(name)}"]`);
      inputs.forEach((el) => {
        if (el.type === "radio") {
          if (el.value === String(value)) el.checked = true;
        } else if (el.type === "checkbox") {
          el.checked = !!value;
        } else {
          el.value = value;
        }
      });
    });
  } catch (e) {
    console.warn("falha ao restaurar progresso", e);
  }
  updateUI();

  // ── salva a cada mudança
  form.addEventListener("change", () => {
    const data = new FormData(form);
    const out = {};
    data.forEach((v, k) => { out[k] = v; });
    localStorage.setItem(storageKey, JSON.stringify(out));
    if (savedPill) {
      savedPill.textContent = "Salvo automaticamente • " + new Date().toLocaleTimeString("pt-BR");
    }
    updateUI();
  });

  function updateUI() {
    // Marca .checked nos likert/nps/opt-list/radio para feedback visual
    form.querySelectorAll("input[type=radio]").forEach((el) => {
      const wrap = el.closest("label");
      if (!wrap) return;
      if (el.checked) wrap.classList.add("checked");
      else wrap.classList.remove("checked");
    });
    // Progresso
    if (progressBar) {
      const radios = form.querySelectorAll("input[type=radio]");
      const groups = {};
      radios.forEach((r) => { groups[r.name] = groups[r.name] || false; if (r.checked) groups[r.name] = true; });
      const total = Object.keys(groups).length;
      const done = Object.values(groups).filter(Boolean).length;
      const otherRequired = form.querySelectorAll("[required]:not([type=radio])");
      let otherDone = 0;
      otherRequired.forEach((el) => { if (el.value) otherDone += 1; });
      const allTotal = total + otherRequired.length;
      const allDone = done + otherDone;
      const pct = allTotal === 0 ? 0 : Math.round((allDone / allTotal) * 100);
      progressBar.style.width = pct + "%";
      const pctLabel = document.getElementById("progress-label");
      if (pctLabel) pctLabel.textContent = pct + "% preenchido (" + allDone + " de " + allTotal + ")";
    }
  }

  // ── ao submeter com sucesso, limpa o storage
  form.addEventListener("submit", (ev) => {
    // Valida obrigatoriedade visual
    const radios = form.querySelectorAll("input[type=radio]");
    const groups = {};
    radios.forEach((r) => { groups[r.name] = groups[r.name] || false; if (r.checked) groups[r.name] = true; });
    const missing = Object.entries(groups).filter(([, v]) => !v).map(([k]) => k);
    if (missing.length > 0) {
      ev.preventDefault();
      const first = form.querySelector(`[name="${CSS.escape(missing[0])}"]`);
      if (first) {
        const wrap = first.closest(".item") || first.closest(".card");
        if (wrap) {
          wrap.scrollIntoView({ behavior: "smooth", block: "center" });
          wrap.style.boxShadow = "0 0 0 2px var(--red)";
          setTimeout(() => { wrap.style.boxShadow = ""; }, 2200);
        }
      }
      alert("Faltam " + missing.length + " item(ns) para responder antes de enviar.");
      return;
    }
    // Verifica outros obrigatórios
    const otherReq = form.querySelectorAll("[required]:not([type=radio])");
    for (const el of otherReq) {
      if (!el.value) {
        ev.preventDefault();
        el.scrollIntoView({ behavior: "smooth", block: "center" });
        el.focus();
        alert("Por favor preencha o campo obrigatório.");
        return;
      }
    }
    // OK, vai submeter — limpa storage no callback de sucesso (servidor redireciona)
    localStorage.removeItem(storageKey);
  });
})();

// Persistência + UX do formulário: progresso sticky, estimativa de tempo, validação inline.
(function () {
  const form = document.getElementById("form-medidor");
  if (!form) return;
  const storageKey = form.dataset.storageKey;
  const startedAtKey = storageKey + ":started_at";

  const progressBar = document.querySelector(".progress-bar__fill");
  const progressLabel = document.getElementById("progress-label");
  const timeLabel = document.getElementById("time-label");
  const savedPill = document.getElementById("saved-pill");
  const pilarLabel = document.getElementById("pilar-label");

  // ── restaura
  try {
    const saved = JSON.parse(localStorage.getItem(storageKey) || "{}");
    Object.entries(saved).forEach(([name, value]) => {
      const inputs = form.querySelectorAll(`[name="${CSS.escape(name)}"]`);
      inputs.forEach((el) => {
        if (el.type === "radio") {
          if (el.value === String(value)) el.checked = true;
        } else {
          el.value = value;
        }
      });
    });
  } catch (e) { /* */ }

  if (!localStorage.getItem(startedAtKey)) {
    localStorage.setItem(startedAtKey, String(Date.now()));
  }
  updateUI();

  form.addEventListener("change", () => {
    const data = new FormData(form);
    const out = {};
    data.forEach((v, k) => { out[k] = v; });
    localStorage.setItem(storageKey, JSON.stringify(out));
    if (savedPill) {
      savedPill.textContent = "Salvo automaticamente · " + new Date().toLocaleTimeString("pt-BR", {hour: "2-digit", minute: "2-digit"});
    }
    updateUI();
  });

  function updateUI() {
    // Marca checked nos botões Likert/NPS/retencao
    form.querySelectorAll("input[type=radio]").forEach((el) => {
      const wrap = el.closest("label");
      if (!wrap) return;
      if (el.checked) wrap.classList.add("checked"); else wrap.classList.remove("checked");
    });

    // Conta grupos respondidos
    const radios = form.querySelectorAll("input[type=radio]");
    const groups = {};
    radios.forEach((r) => {
      if (!(r.name in groups)) groups[r.name] = false;
      if (r.checked) groups[r.name] = true;
    });
    const totalGroups = Object.keys(groups).length;
    const doneGroups = Object.values(groups).filter(Boolean).length;

    const otherRequired = form.querySelectorAll("[required]:not([type=radio]):not([type=checkbox])");
    let otherDone = 0;
    otherRequired.forEach((el) => { if (el.value) otherDone += 1; });

    const totalAll = totalGroups + otherRequired.length;
    const doneAll = doneGroups + otherDone;
    const pct = totalAll === 0 ? 0 : Math.round((doneAll / totalAll) * 100);

    if (progressBar) progressBar.style.width = pct + "%";
    if (progressLabel) progressLabel.textContent = pct + "% (" + doneAll + " de " + totalAll + ")";

    // Estimativa de tempo
    if (timeLabel) {
      const started = parseInt(localStorage.getItem(startedAtKey) || Date.now(), 10);
      const elapsed = (Date.now() - started) / 1000;
      if (doneAll === 0) {
        timeLabel.textContent = "Estimativa: ~12 min (média histórica)";
      } else {
        const perItem = elapsed / doneAll;
        const remain = (totalAll - doneAll) * perItem;
        const min = Math.max(1, Math.round(remain / 60));
        timeLabel.textContent = "Faltam ~" + min + " min nesse ritmo";
      }
    }

    // Detecta pilar atual (último item focado/respondido)
    if (pilarLabel) {
      const sections = form.querySelectorAll("[data-pilar]");
      let atual = null;
      sections.forEach((s) => {
        const rect = s.getBoundingClientRect();
        if (rect.top < 200) atual = s.dataset.pilar;
      });
      if (atual) pilarLabel.textContent = atual;
    }
  }

  // ── pilar visível ao rolar
  window.addEventListener("scroll", () => {
    if (pilarLabel) {
      const sections = form.querySelectorAll("[data-pilar]");
      let atual = "";
      sections.forEach((s) => {
        const rect = s.getBoundingClientRect();
        if (rect.top < 200) atual = s.dataset.pilar;
      });
      if (atual) pilarLabel.textContent = atual;
    }
  }, {passive: true});

  // ── valida retencao=outro exigindo descrição
  const retencaoOutro = form.querySelector("input[name=retencao][value=outro]");
  const retencaoTexto = form.querySelector("#retencao_outro");
  if (retencaoOutro && retencaoTexto) {
    function toggleOutro() {
      if (retencaoOutro.checked) {
        retencaoTexto.setAttribute("required", "required");
        retencaoTexto.placeholder = "Descreva o motivo (obrigatório se marcou 'Outro')";
      } else {
        retencaoTexto.removeAttribute("required");
        retencaoTexto.placeholder = "(opcional)";
      }
    }
    form.querySelectorAll("input[name=retencao]").forEach(r => r.addEventListener("change", toggleOutro));
    toggleOutro();
  }

  // ── submit
  form.addEventListener("submit", (ev) => {
    const radios = form.querySelectorAll("input[type=radio]");
    const groups = {};
    radios.forEach((r) => { if (!(r.name in groups)) groups[r.name] = false; if (r.checked) groups[r.name] = true; });
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
    const otherReq = form.querySelectorAll("[required]:not([type=radio]):not([type=checkbox])");
    for (const el of otherReq) {
      if (!el.value) {
        ev.preventDefault();
        el.scrollIntoView({ behavior: "smooth", block: "center" });
        el.focus();
        alert("Por favor preencha o campo obrigatório: " + (el.previousElementSibling ? el.previousElementSibling.textContent : el.placeholder));
        return;
      }
    }
    // OK
    localStorage.removeItem(storageKey);
    localStorage.removeItem(startedAtKey);
  });
})();

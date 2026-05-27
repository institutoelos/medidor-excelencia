// Medidor — Wizard (1 pergunta por tela) com auto-save, atalhos e animação.
(function () {
  const form = document.getElementById("form-medidor");
  if (!form) return;

  const storageKey = form.dataset.storageKey;
  const startedAtKey = storageKey + ":started_at";
  const stepKey = storageKey + ":step";

  const steps = Array.from(form.querySelectorAll(".step"));
  const total = steps.length;
  const back = document.getElementById("wiz-back");
  const next = document.getElementById("wiz-next");
  const counter = document.getElementById("wiz-counter");
  const live = document.getElementById("wiz-live");
  const progressBar = document.querySelector(".progress-bar__fill");
  const pilarLabel = document.getElementById("pilar-label");
  const savedPill = document.getElementById("saved-pill");

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ── Restaura respostas
  let saved = {};
  try { saved = JSON.parse(localStorage.getItem(storageKey) || "{}"); } catch (e) { saved = {}; }
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
  if (!localStorage.getItem(startedAtKey)) {
    localStorage.setItem(startedAtKey, String(Date.now()));
  }

  // ── Restaura step atual (mas não ultrapassa um step não respondido)
  let current = 0;
  const savedStep = parseInt(localStorage.getItem(stepKey) || "0", 10);
  if (!isNaN(savedStep) && savedStep >= 0 && savedStep < total) {
    current = Math.min(savedStep, firstUnansweredIndex());
  }

  // ── Helpers
  function firstUnansweredIndex() {
    for (let i = 0; i < steps.length; i++) {
      if (!isStepAnswered(steps[i])) return i;
    }
    return steps.length - 1; // todas respondidas → step final
  }

  function isStepAnswered(stepEl) {
    const type = stepEl.dataset.stepType;
    if (type === "likert" || type === "nps") {
      const name = stepEl.querySelector("input[type=radio]").name;
      return !!form.querySelector(`input[name="${name}"]:checked`);
    }
    if (type === "retencao") {
      const escolhida = form.querySelector('input[name="retencao"]:checked');
      if (!escolhida) return false;
      if (escolhida.value === "outro") {
        const txt = form.querySelector('#retencao_outro');
        return !!(txt && txt.value.trim());
      }
      return true;
    }
    if (type === "demo") {
      return Array.from(stepEl.querySelectorAll("[name][required]")).every((el) => (el.value || "").trim());
    }
    if (type === "final") return true;
    if (type === "marker") return true; // step informacional, sem input
    return false;
  }

  function pilarOf(stepEl) {
    return stepEl.dataset.pilar || "";
  }

  // ── Animação de transição
  function showStep(idx, direction) {
    const prev = steps.find((s) => !s.hidden);
    const target = steps[idx];
    if (!target) return;
    direction = direction || (prev && steps.indexOf(prev) < idx ? "forward" : "backward");

    function reveal() {
      steps.forEach((s) => { s.hidden = true; s.classList.remove("step--active"); });
      target.hidden = false;
      // Força reflow pra animação rodar
      // eslint-disable-next-line no-unused-expressions
      target.offsetHeight;
      target.classList.add("step--active");
      target.classList.add(direction === "forward" ? "step--enter-fwd" : "step--enter-back");
      // Limpa classe de animação após terminar
      setTimeout(() => {
        target.classList.remove("step--enter-fwd", "step--enter-back");
      }, 350);

      // Foco gerenciado pra navegação por teclado e screen readers
      const firstInput = target.querySelector("input:not([type=hidden]), select, textarea, button[type=submit]");
      if (firstInput) {
        // Não roubar foco do <body> pra evitar scroll abrupto em alguns mobile browsers
        if (target.dataset.stepType === "demo" || target.dataset.stepType === "retencao" || target.dataset.stepType === "final") {
          setTimeout(() => firstInput.focus({ preventScroll: false }), 50);
        }
      }
      target.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
    }

    if (prev && !reduceMotion) {
      prev.classList.add(direction === "forward" ? "step--exit-fwd" : "step--exit-back");
      setTimeout(() => {
        prev.classList.remove("step--exit-fwd", "step--exit-back");
        reveal();
      }, 140);
    } else {
      reveal();
    }
  }

  function updateUI() {
    // Progresso — markers e final não contam (não são "perguntas")
    const questionSteps = steps.filter((s) => {
      const t = s.dataset.stepType;
      return t !== "marker" && t !== "final";
    });
    const answered = questionSteps.filter(isStepAnswered).length;
    const pct = Math.round((answered / questionSteps.length) * 100);
    if (progressBar) progressBar.style.width = pct + "%";

    // Counter (pilar + posição)
    const stepEl = steps[current];
    if (pilarLabel && stepEl) pilarLabel.textContent = pilarOf(stepEl);
    if (counter) counter.textContent = `${pct}% completo`;

    // Marca checked nos radios pra estilo
    form.querySelectorAll("input[type=radio]").forEach((el) => {
      const wrap = el.closest("label");
      if (!wrap) return;
      if (el.checked) wrap.classList.add("checked"); else wrap.classList.remove("checked");
    });

    // Back disabled na primeira step
    if (back) back.disabled = current === 0;

    // Next disabled se step atual não respondida
    if (next) {
      const stepNow = steps[current];
      const isFinal = stepNow && stepNow.dataset.stepType === "final";
      next.hidden = isFinal;
      next.disabled = !isStepAnswered(stepNow);
    }

    // Persiste step e respostas
    localStorage.setItem(stepKey, String(current));
    persistAnswers();
  }

  function persistAnswers() {
    const data = new FormData(form);
    const out = {};
    data.forEach((v, k) => { out[k] = v; });
    localStorage.setItem(storageKey, JSON.stringify(out));
    if (savedPill) {
      savedPill.textContent = "Salvo · " + new Date().toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" });
    }
  }

  function goNext() {
    if (current >= total - 1) return;
    const stepNow = steps[current];
    if (!isStepAnswered(stepNow)) {
      flashError(stepNow);
      return;
    }
    current += 1;
    showStep(current, "forward");
    updateUI();
  }

  function goBack() {
    if (current <= 0) return;
    current -= 1;
    showStep(current, "backward");
    updateUI();
  }

  function flashError(stepEl) {
    stepEl.classList.add("step--shake");
    setTimeout(() => stepEl.classList.remove("step--shake"), 400);
    if (live) live.textContent = "Selecione uma resposta antes de continuar.";
  }

  // ── Wiring
  if (back) back.addEventListener("click", goBack);
  if (next) next.addEventListener("click", goNext);

  // Auto-avanço ao escolher Likert (não pra NPS/retenção: usuário pode querer revisar)
  form.addEventListener("change", (ev) => {
    persistAnswers();
    updateUI();
    const stepNow = steps[current];
    if (!stepNow) return;
    const type = stepNow.dataset.stepType;
    const tgt = ev.target;
    if (type === "likert" && tgt.type === "radio" && tgt.closest(".likert__opt")) {
      setTimeout(() => goNext(), 240);
    }
    // Retenção: revela "Outro" se aplicável
    if (type === "retencao" && tgt.name === "retencao") {
      const outroBox = stepNow.querySelector(".retencao-outro");
      const isOutro = tgt.value === "outro";
      if (outroBox) outroBox.hidden = !isOutro;
      const outroTxt = stepNow.querySelector("#retencao_outro");
      if (outroTxt) {
        if (isOutro) outroTxt.setAttribute("required", "required");
        else outroTxt.removeAttribute("required");
      }
    }
  });

  form.addEventListener("input", () => { persistAnswers(); updateUI(); });

  // ── Atalhos de teclado
  document.addEventListener("keydown", (ev) => {
    if (ev.metaKey || ev.ctrlKey || ev.altKey) return;
    // Não interferir quando o foco está num textinput/select aberto pra digitação
    const activeTag = (document.activeElement && document.activeElement.tagName) || "";
    if (activeTag === "INPUT" && document.activeElement.type === "text") return;
    if (activeTag === "TEXTAREA") return;

    const stepNow = steps[current];
    if (!stepNow) return;
    const type = stepNow.dataset.stepType;

    if (type === "likert" && /^[1-5]$/.test(ev.key)) {
      const radio = stepNow.querySelector(`input[type=radio][value="${ev.key}"]`);
      if (radio) {
        radio.checked = true;
        radio.dispatchEvent(new Event("change", { bubbles: true }));
        ev.preventDefault();
      }
    } else if (type === "nps" && /^[0-9]$/.test(ev.key)) {
      const radio = stepNow.querySelector(`input[type=radio][value="${ev.key}"]`);
      if (radio) {
        radio.checked = true;
        radio.dispatchEvent(new Event("change", { bubbles: true }));
        ev.preventDefault();
      }
    } else if (ev.key === "Enter" && type !== "final") {
      if (isStepAnswered(stepNow)) {
        goNext();
        ev.preventDefault();
      }
    }
  });

  // ── Submit: valida tudo antes de enviar de verdade
  form.addEventListener("submit", (ev) => {
    const missing = steps.filter((s) => s.dataset.stepType !== "final" && !isStepAnswered(s));
    if (missing.length > 0) {
      ev.preventDefault();
      current = steps.indexOf(missing[0]);
      showStep(current, "backward");
      updateUI();
      if (live) live.textContent = `Faltam ${missing.length} resposta(s) antes de enviar.`;
      return;
    }
    localStorage.removeItem(storageKey);
    localStorage.removeItem(startedAtKey);
    localStorage.removeItem(stepKey);
  });

  // ── Boot
  showStep(current, "forward");
  updateUI();
})();

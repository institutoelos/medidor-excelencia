// form.jsx — the form runner. Supports 3 patterns: one-per-screen, block-per-screen, pillar-per-screen.

const { useState, useEffect, useMemo, useRef } = React;

// Returns: which pilar idx, what step inside the pilar's sequence
function buildPilarSeq(version) {
  // Each pilar gets:
  //   - 1 breath card
  //   - N item screens (one-per-screen) or M block screens or 1 pillar screen
  // Plus closing tail (anchor, [nps, retencao, demograficos], obrigado)
  return null;
}

// Helper: subgroup -> [from, to] arrays
function subgroupRanges(pilar) {
  return pilar.subgroups.map(s => s.range);
}

// MAIN FORM ROUTER
function FormRunner({ version, pattern, onFinish, persistKey }) {
  const D = window.MEDIDOR_DATA;
  const items = version === "socio" ? D.itemsSocio : D.itemsColab;
  const totalItems = 58;

  // ── State (persisted to localStorage) ──
  const [state, setState] = useState(() => {
    try {
      const raw = localStorage.getItem(persistKey);
      if (raw) return JSON.parse(raw);
    } catch (e) {}
    return {
      answers: {},        // {1: 5, 2: 4, ...}
      ancora: null,
      nps: null,
      retencao: null,
      retencaoTexto: "",
      tempoCasa: null,
      cargo: null,
      area: "",
    };
  });

  useEffect(() => {
    try { localStorage.setItem(persistKey, JSON.stringify(state)); } catch (e) {}
  }, [state, persistKey]);

  const setAnswer = (n, v) => setState(s => ({...s, answers: {...s.answers, [n]: v}}));
  const set = (k, v) => setState(s => ({...s, [k]: v}));

  // ── Build flow ──
  const flow = useMemo(() => buildFlow(version, pattern), [version, pattern]);
  const [stepIdx, setStepIdx] = useState(0);

  const cur = flow[stepIdx];
  const goNext = () => setStepIdx(i => Math.min(i + 1, flow.length - 1));
  const goPrev = () => setStepIdx(i => Math.max(i - 1, 0));

  // ── Compute progress ──
  const perPilarAnswered = D.pilares.map(p => {
    const [a, b] = p.ranges[0];
    let n = 0;
    for (let i = a; i <= b; i++) if (state.answers[i] != null) n++;
    return n;
  });
  const perPilarTotal = D.pilares.map(p => p.ranges[0][1] - p.ranges[0][0] + 1);

  const currentPilarIdx = (() => {
    if (cur.type === "breath") return cur.pilarIdx;
    if (cur.type === "item") return D.pilares.findIndex(p => cur.n >= p.ranges[0][0] && cur.n <= p.ranges[0][1]);
    if (cur.type === "block") return D.pilares.findIndex(p => cur.items[0] >= p.ranges[0][0] && cur.items[0] <= p.ranges[0][1]);
    if (cur.type === "pilar") return cur.pilarIdx;
    return -1;
  })();

  // Scroll to top on step change (instant — animations are inside the screen itself)
  useEffect(() => { window.scrollTo(0, 0); }, [stepIdx]);

  // ── Render ──
  const allItemsAnswered = Object.keys(state.answers).length >= totalItems;

  return (
    <div className="app-shell">
      <BrandHeader
        rodada="Instituto ELOS · Rodada 1"
        onHome={() => { if (confirm("Sair e voltar ao início?")) window.__navigate?.("cover"); }}
        showProgress={cur.type !== "breath" && cur.type !== "closing" && cur.type !== "thanks" && cur.type !== "intro" && cur.type !== "ancora"}
        progressNode={
          <PilarProgress
            pilares={D.pilares}
            currentPilarIdx={Math.max(0, currentPilarIdx)}
            perPilarAnswered={perPilarAnswered}
            totals={perPilarTotal}
          />
        }
      />

      <main style={{flex: 1, display: "flex", flexDirection: "column"}}>
        {cur.type === "intro" && (
          <IntroScreen version={version} onStart={goNext} />
        )}

        {cur.type === "breath" && (
          <div style={{flex:1, display:"flex", alignItems:"center", justifyContent:"center"}}>
            <PilarBreath pilar={D.pilares[cur.pilarIdx]} onContinue={goNext} />
          </div>
        )}

        {cur.type === "item" && (
          <PageWrap narrow>
            <ItemPrompt
              n={cur.n}
              total={totalItems}
              pilar={D.pilares[currentPilarIdx]}
              text={items[cur.n - 1]}
            />
            <Likert
              value={state.answers[cur.n]}
              onChange={(v) => { setAnswer(cur.n, v); setTimeout(goNext, 220); }}
            />
            <div className="form-nav">
              <button className="btn btn--quiet" onClick={goPrev} disabled={stepIdx === 0}>← Voltar</button>
              <span className="form-nav__hint">Suas respostas são confidenciais</span>
              <button className="btn btn--ghost" onClick={goNext} disabled={state.answers[cur.n] == null}>
                Avançar
              </button>
            </div>
          </PageWrap>
        )}

        {cur.type === "block" && (
          <PageWrap>
            <BlockScreen
              items={cur.items}
              labels={items}
              answers={state.answers}
              onAnswer={setAnswer}
              pilar={D.pilares[currentPilarIdx]}
              sublabel={cur.sublabel}
              flowIdx={stepIdx}
              flowTotal={flow.length}
            />
            <BlockNav
              answered={cur.items.every(n => state.answers[n] != null)}
              onPrev={goPrev}
              onNext={goNext}
              isFirst={stepIdx === 0}
            />
          </PageWrap>
        )}

        {cur.type === "pilar" && (
          <PageWrap>
            <PilarScreen
              pilar={D.pilares[cur.pilarIdx]}
              labels={items}
              answers={state.answers}
              onAnswer={setAnswer}
            />
            <BlockNav
              answered={(() => {
                const [a,b] = D.pilares[cur.pilarIdx].ranges[0];
                for (let i=a;i<=b;i++) if (state.answers[i]==null) return false;
                return true;
              })()}
              onPrev={goPrev}
              onNext={goNext}
              isFirst={stepIdx === 0}
            />
          </PageWrap>
        )}

        {cur.type === "ancora" && (
          <PageWrap narrow>
            <AncoraScreen
              version={version}
              value={state.ancora}
              onChange={(v) => set("ancora", v)}
              onNext={goNext}
              onPrev={goPrev}
            />
          </PageWrap>
        )}

        {cur.type === "nps" && (
          <PageWrap narrow>
            <NPSScreen
              value={state.nps}
              onChange={(v) => set("nps", v)}
              onNext={goNext}
              onPrev={goPrev}
            />
          </PageWrap>
        )}

        {cur.type === "retencao" && (
          <PageWrap narrow>
            <RetencaoScreen
              value={state.retencao}
              onChange={(v) => set("retencao", v)}
              texto={state.retencaoTexto}
              onTexto={(v) => set("retencaoTexto", v)}
              onNext={goNext}
              onPrev={goPrev}
            />
          </PageWrap>
        )}

        {cur.type === "demograficos" && (
          <PageWrap narrow>
            <DemograficosScreen
              state={state}
              setField={set}
              onNext={goNext}
              onPrev={goPrev}
            />
          </PageWrap>
        )}

        {cur.type === "thanks" && (
          <ThanksScreen version={version} onFinish={onFinish} />
        )}
      </main>

      <AppFooter />
    </div>
  );
}

// ── Build the linear flow ──
function buildFlow(version, pattern) {
  const D = window.MEDIDOR_DATA;
  const steps = [];
  steps.push({ type: "intro" });

  D.pilares.forEach((p, pidx) => {
    steps.push({ type: "breath", pilarIdx: pidx });
    if (pattern === "one") {
      const [a, b] = p.ranges[0];
      for (let i = a; i <= b; i++) steps.push({ type: "item", n: i });
    } else if (pattern === "block") {
      p.subgroups.forEach(sg => {
        const [a, b] = sg.range;
        const arr = [];
        for (let i = a; i <= b; i++) arr.push(i);
        steps.push({ type: "block", items: arr, sublabel: sg.label });
      });
    } else if (pattern === "pilar") {
      steps.push({ type: "pilar", pilarIdx: pidx });
    }
  });

  steps.push({ type: "ancora" });
  if (version === "colab") {
    steps.push({ type: "nps" });
    steps.push({ type: "retencao" });
    steps.push({ type: "demograficos" });
  }
  steps.push({ type: "thanks" });
  return steps;
}

// ───── Intro screen (per-user landing from unique link) ─────
function IntroScreen({ version, onStart }) {
  const isSocio = version === "socio";
  return (
    <div className="center-stage">
      <div className="center-stage__inner fade-in">
        {/* Personalized identification — this is what the link recipient sees */}
        <div style={{display: "flex", alignItems: "center", gap: 16, marginBottom: 28, flexWrap: "wrap"}}>
          <div style={{
            width: 56, height: 56, borderRadius: 12,
            background: "var(--ink)", color: "var(--paper)",
            display: "flex", alignItems: "center", justifyContent: "center",
            fontFamily: "var(--font-display)", fontSize: 26, lineHeight: 1,
            letterSpacing: "-0.03em",
          }}>IE</div>
          <div>
            <div className="eyebrow" style={{color: "var(--copper)"}}>Você foi convidado(a) a responder</div>
            <div className="serif" style={{fontSize: 22, lineHeight: 1.1, letterSpacing: "-0.01em", marginTop: 4}}>Instituto ELOS · Medidor de Excelência</div>
          </div>
        </div>

        <span className="eyebrow">{isSocio ? "Versão sócios · empresário" : "Versão colaborador"}</span>
        <h1 className="serif" style={{fontSize: "clamp(36px, 5.5vw, 64px)", lineHeight: 1.05, margin: "12px 0 22px", letterSpacing: "-0.02em"}}>
          {isSocio ? "Como você enxerga o time que construiu." : "Como é trabalhar nessa empresa, na sua vivência."}
        </h1>
        <p style={{fontSize: 17, color: "var(--ink-2)", maxWidth: 600, lineHeight: 1.55}}>
          São <strong>58 perguntas</strong> sobre cultura, educação e feedback, divididas em três blocos.
          Leva cerca de <strong>10 minutos</strong>. Não há resposta certa — responda pelo que você vive, não pelo que gostaria de viver.
        </p>

        <div className="card card--soft" style={{margin: "28px 0", padding: 22}}>
          <div className="kv">
            <dt>Tempo estimado</dt><dd>10 min</dd>
            <dt>Perguntas</dt><dd>58 itens · escala de 1 a 5</dd>
            <dt>Confidencialidade</dt><dd>{isSocio ? "Suas respostas vão para o relatório agregado." : "Anônima · individualmente confidencial"}</dd>
            <dt>Você pode pausar</dt><dd>Sim, retoma do mesmo ponto</dd>
          </div>
        </div>

        <div style={{display:"flex", gap: 16, alignItems: "center", flexWrap: "wrap"}}>
          <button className="btn btn--primary btn--lg" onClick={onStart}>
            Começar agora
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
          </button>
          <MethodSeal />
        </div>

        <div style={{marginTop: 32, fontSize: 12, color: "var(--ink-dim)", maxWidth: 560, lineHeight: 1.5, paddingTop: 20, borderTop: "0.5px solid var(--hairline)"}}>
          {isSocio
            ? "Suas respostas serão lidas junto com as do time no Relatório de Gap — peça central da primeira sessão de mentoria."
            : "Suas respostas são individualmente confidenciais. Dados só são reportados em recortes com 5 ou mais respondentes, conforme padrão Trust Index."}
        </div>
      </div>
    </div>
  );
}

// ───── Block screen ─────
function BlockScreen({ items, labels, answers, onAnswer, pilar, sublabel }) {
  return (
    <div className="fade-in">
      <div className="item-eyebrow">
        <span className="item-pilar-tag">Pilar {pilar.num} · {pilar.curto}</span>
        <span className="item-counter">{sublabel}</span>
      </div>
      <h2 className="serif" style={{fontSize: 30, margin: "8px 0 8px", letterSpacing: "-0.01em"}}>{sublabel}</h2>
      <p style={{color: "var(--ink-dim)", fontSize: 14, marginBottom: 28}}>
        Marque o quanto cada frase é verdade para você. <span style={{whiteSpace:"nowrap"}}>1 = Nunca · 5 = Sempre</span>
      </p>

      <div>
        {items.map((n) => (
          <div className="block-item" key={n}>
            <div>
              <span className="block-item__num">{String(n).padStart(2, "0")}</span>
              <div className="block-item__text">{labels[n - 1]}</div>
            </div>
            <Likert inline value={answers[n]} onChange={(v) => onAnswer(n, v)} />
          </div>
        ))}
      </div>
    </div>
  );
}

// ───── Pilar (long) screen ─────
function PilarScreen({ pilar, labels, answers, onAnswer }) {
  return (
    <div className="fade-in">
      <div className="item-eyebrow">
        <span className="item-pilar-tag">Pilar {pilar.num}</span>
        <span className="item-counter">{pilar.ranges[0][1] - pilar.ranges[0][0] + 1} perguntas</span>
      </div>
      <h2 className="serif" style={{fontSize: 38, margin: "8px 0 8px", letterSpacing: "-0.02em"}}>{pilar.titulo}</h2>
      <p style={{color: "var(--ink-dim)", fontSize: 14, marginBottom: 28}}>
        Marque o quanto cada frase é verdade para você. 1 = Nunca · 5 = Sempre
      </p>

      {pilar.subgroups.map((sg) => {
        const [a, b] = sg.range;
        const items = [];
        for (let i=a;i<=b;i++) items.push(i);
        return (
          <div key={sg.label} style={{marginBottom: 28}}>
            <div className="eyebrow" style={{marginBottom: 8}}>{sg.label}</div>
            <hr className="divider" />
            {items.map((n) => (
              <div className="block-item" key={n}>
                <div>
                  <span className="block-item__num">{String(n).padStart(2, "0")}</span>
                  <div className="block-item__text">{labels[n - 1]}</div>
                </div>
                <Likert inline value={answers[n]} onChange={(v) => onAnswer(n, v)} />
              </div>
            ))}
          </div>
        );
      })}
    </div>
  );
}

function BlockNav({ answered, onPrev, onNext, isFirst }) {
  return (
    <div className="form-nav">
      <button className="btn btn--quiet" onClick={onPrev} disabled={isFirst}>← Voltar</button>
      <span className="form-nav__hint">Suas respostas são confidenciais</span>
      <button className="btn btn--primary" onClick={onNext} disabled={!answered}>
        Avançar
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
      </button>
    </div>
  );
}

// ───── Âncora ─────
function AncoraScreen({ version, value, onChange, onNext, onPrev }) {
  const text = version === "socio"
    ? "Levando tudo em conta, eu diria que essa empresa é um excelente lugar para trabalhar."
    : "Levando tudo em conta, eu diria que este é um excelente lugar para trabalhar.";
  return (
    <div className="fade-in">
      <span className="eyebrow">Última leitura · pergunta-síntese</span>
      <h2 className="item-prompt serif" style={{marginTop: 12, fontSize: 36}}>{text}</h2>
      <Likert value={value} onChange={onChange} />
      <BlockNav answered={value != null} onPrev={onPrev} onNext={onNext} isFirst={false} />
    </div>
  );
}

// ───── NPS ─────
function NPSScreen({ value, onChange, onNext, onPrev }) {
  return (
    <div className="fade-in">
      <span className="eyebrow">Recomendação</span>
      <h2 className="item-prompt serif" style={{marginTop: 12}}>
        Em uma escala de 0 a 10, o quanto você indicaria essa empresa para um amigo trabalhar?
      </h2>
      <div className="nps-row">
        {Array.from({length: 11}, (_, i) => (
          <button
            key={i}
            type="button"
            className="nps-btn"
            data-selected={value === i}
            onClick={() => onChange(i)}
            aria-label={"Nota " + i}
          >{i}</button>
        ))}
      </div>
      <div className="nps-scale-labels">
        <span>Não indicaria</span>
        <span>Indicaria muito</span>
      </div>
      <BlockNav answered={value != null} onPrev={onPrev} onNext={onNext} isFirst={false} />
    </div>
  );
}

// ───── Retenção ─────
function RetencaoScreen({ value, onChange, texto, onTexto, onNext, onPrev }) {
  const opts = [
    "A oportunidade que eu tenho de crescer e me desenvolver",
    "O propósito da empresa e o sentido que vejo no meu trabalho",
    "O vínculo que tenho com o time e as pessoas daqui",
    "A segurança e estabilidade que essa empresa me oferece",
    "A remuneração e os benefícios",
    "O alinhamento entre os meus valores pessoais e os valores da empresa",
    "Outro motivo",
  ];
  return (
    <div className="fade-in">
      <span className="eyebrow">Retenção</span>
      <h2 className="item-prompt serif" style={{marginTop: 12}}>
        O principal motivo que me faz permanecer nessa empresa é:
      </h2>
      <div style={{display: "flex", flexDirection: "column", gap: 8}}>
        {opts.map((opt) => (
          <button key={opt} type="button" className="choice" data-selected={value === opt} onClick={() => onChange(opt)}>
            <span className="choice__radio"></span>
            <span className="choice__text">{opt}</span>
          </button>
        ))}
        {value === "Outro motivo" && (
          <input
            type="text"
            value={texto}
            onChange={(e) => onTexto(e.target.value)}
            placeholder="Conta pra gente em uma frase"
            style={{
              padding: "14px 18px", marginTop: 4,
              border: "0.5px solid var(--hairline)",
              borderRadius: "var(--r-md)",
              fontSize: 14,
              background: "var(--card)"
            }}
          />
        )}
      </div>
      <BlockNav answered={value != null && (value !== "Outro motivo" || texto.trim().length > 0)} onPrev={onPrev} onNext={onNext} isFirst={false} />
    </div>
  );
}

// ───── Demográficos ─────
function DemograficosScreen({ state, setField, onNext, onPrev }) {
  const tempo = ["Até 6 meses", "De 6 meses a 1 ano", "De 1 a 3 anos", "De 3 a 5 anos", "Mais de 5 anos"];
  const cargos = ["Liderança sênior (sócio, diretor, gerente sênior)", "Liderança intermediária (coordenador, supervisor, líder de time)", "Colaborador", "Estagiário, jovem aprendiz ou trainee"];
  const areas = ["Atendimento", "Conteúdo & Mídia", "Operações", "Comercial", "Administrativo"];

  const Section = ({ title, value, onChange, options }) => (
    <div style={{marginBottom: 28}}>
      <div className="eyebrow" style={{marginBottom: 12}}>{title}</div>
      <div style={{display:"flex", flexDirection: "column", gap: 6}}>
        {options.map((o) => (
          <button key={o} type="button" className="choice" data-selected={value === o} onClick={() => onChange(o)}>
            <span className="choice__radio"></span>
            <span className="choice__text">{o}</span>
          </button>
        ))}
      </div>
    </div>
  );

  const valid = state.tempoCasa && state.cargo && state.area;

  return (
    <div className="fade-in">
      <span className="eyebrow">Quase lá · cortes demográficos</span>
      <h2 className="serif" style={{fontSize: 32, marginTop: 12, marginBottom: 8, letterSpacing: "-0.01em"}}>
        Para a empresa enxergar diferenças por segmento.
      </h2>
      <p style={{color: "var(--ink-dim)", fontSize: 14, marginBottom: 28, maxWidth: 520}}>
        Esses dados são reportados apenas quando há 5 ou mais respondentes no mesmo recorte — para preservar seu anonimato.
      </p>

      <Section title="Há quanto tempo você está aqui" value={state.tempoCasa} onChange={(v) => setField("tempoCasa", v)} options={tempo} />
      <Section title="Tipo de cargo" value={state.cargo} onChange={(v) => setField("cargo", v)} options={cargos} />
      <Section title="Área de trabalho" value={state.area} onChange={(v) => setField("area", v)} options={areas} />

      <BlockNav answered={valid} onPrev={onPrev} onNext={onNext} isFirst={false} />
    </div>
  );
}

// ───── Thanks ─────
function ThanksScreen({ version, onFinish }) {
  return (
    <div className="center-stage">
      <div className="center-stage__inner fade-in" style={{textAlign: "center", maxWidth: 620, margin: "0 auto"}}>
        <BrandSigno size={64} />
        <h1 className="serif" style={{fontSize: "clamp(40px, 6vw, 64px)", lineHeight: 1.05, margin: "32px 0 20px", letterSpacing: "-0.02em"}}>
          Recebemos suas respostas.
        </h1>
        <p style={{fontSize: 17, color: "var(--ink-2)", lineHeight: 1.55, marginBottom: 28}}>
          Obrigado pela honestidade. O relatório consolidado é entregue ao empresário na próxima sessão de mentoria — e vira o documento-âncora do trabalho dos próximos 12 meses no Pilar Pessoas.
        </p>

        <div style={{display:"flex", gap: 14, justifyContent: "center", flexWrap: "wrap"}}>
          <button className="btn btn--primary" onClick={onFinish}>Concluir</button>
          <button className="btn btn--ghost" onClick={() => window.__navigate?.("admin")}>Ver painel da empresa (demo)</button>
        </div>

        <div style={{marginTop: 56, padding: "20px 24px", borderTop: "0.5px solid var(--hairline)", color: "var(--ink-dim)", fontSize: 12}}>
          ELO Business · Medidor de Excelência · Pilar Pessoas
        </div>
      </div>
    </div>
  );
}

Object.assign(window, { FormRunner });

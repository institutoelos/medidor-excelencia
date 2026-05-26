// components.jsx — shared chrome and primitives
const { useState, useEffect, useMemo, useRef, useCallback } = React;

// ───── Brand marks ─────
function BrandSigno({ size = 22 }) {
  return (
    <img src="assets/signo-elos.png" alt="ELOS"
         style={{ width: size, height: size, objectFit: "contain" }} />
  );
}

function BrandHeader({ rodada, onHome, showProgress, progressNode }) {
  return (
    <header className="app-header">
      <div className="app-header__inner">
        <a className="brand-mark" href="#" onClick={(e) => { e.preventDefault(); onHome && onHome(); }}>
          <BrandSigno size={24} />
          <span className="brand-mark__wordmark">
            ELO <em>Business</em>
          </span>
          <span className="brand-mark__divider"></span>
          <span className="brand-mark__small">Medidor de Excelência</span>
        </a>
        {rodada && (
          <div style={{display: "flex", alignItems: "center", gap: 12, fontSize: 12, color: "var(--ink-dim)"}}>
            <span style={{display:"none"}} className="md-show">{rodada}</span>
          </div>
        )}
      </div>
      {showProgress && progressNode && (
        <div style={{maxWidth: 1200, margin: "0 auto", padding: "0 24px 14px"}}>
          {progressNode}
        </div>
      )}
    </header>
  );
}

function AppFooter() {
  return (
    <footer className="app-footer">
      <div>
        <strong style={{color: "var(--ink-2)"}}>Confidencial.</strong> Suas respostas são individualmente anônimas e
        agregadas apenas em recortes com 5+ respondentes.
      </div>
      <div style={{display: "flex", gap: 18, alignItems: "center"}}>
        <span>Método herdado de Trust Index (GPTW) e NPS clássico</span>
        <span>·</span>
        <span>Versão 1.0 · ELO Business</span>
      </div>
    </footer>
  );
}

// ───── Method seal (small) ─────
function MethodSeal() {
  return (
    <span className="method-seal">
      <span className="method-seal__dot"></span>
      Método Trust Index · escala Likert 5 pontos · NPS
    </span>
  );
}

// ───── Likert ─────
function Likert({ value, onChange, inline = false }) {
  const scale = window.MEDIDOR_DATA.likertScale; // [5..1]
  // For UX best practice we render left=1 (Nunca) to right=5 (Sempre)
  const order = [1, 2, 3, 4, 5];
  return (
    <div className={"likert" + (inline ? " likert--inline" : "")}>
      {order.map((v) => {
        const item = scale.find((s) => s.value === v);
        const selected = value === v;
        return (
          <button
            key={v}
            type="button"
            className="likert__btn"
            data-selected={selected}
            onClick={() => onChange(v)}
            aria-label={item.label}
          >
            <span className="likert__dot">{selected && !inline && <span style={{width: 8, height: 8, background:"#fff", borderRadius:"50%"}}></span>}</span>
            <span className="likert__num">{v}</span>
            {!inline && <span className="likert__label">{item.label}</span>}
          </button>
        );
      })}
    </div>
  );
}

// ───── Progress (pillar segments) ─────
function PilarProgress({ pilares, currentPilarIdx, perPilarAnswered, totals, mode }) {
  // perPilarAnswered: array length 3 of #answered in that pilar
  // totals: array length 3 of #items in that pilar
  return (
    <div className="progress-pilars" aria-label="Progresso por pilar">
      {pilares.map((p, i) => {
        const total = totals[i];
        const answered = perPilarAnswered[i];
        const pct = total ? (answered / total) * 100 : 0;
        const done = answered === total;
        const current = i === currentPilarIdx;
        return (
          <React.Fragment key={p.id}>
            <div className="progress-pilars__label" style={{
              color: current ? "var(--ink)" : (done ? "var(--copper)" : "var(--ink-muted)"),
              fontWeight: current ? 700 : 500,
              minWidth: i === 1 ? 70 : 80,
            }}>
              <span style={{fontFamily:"var(--font-display)", fontSize: 13, marginRight: 6}}>{p.num}</span>
              {p.curto}
            </div>
            <div className={"progress-pilars__seg" + (done ? " progress-pilars__seg--done" : "")}>
              <div className="progress-pilars__fill" style={{ "--p": pct + "%" }}></div>
            </div>
          </React.Fragment>
        );
      })}
      <div className="progress-pilars__label" style={{color: "var(--ink-dim)", minWidth: 36}}>
        {Math.round((perPilarAnswered.reduce((s,v)=>s+v,0) / totals.reduce((s,v)=>s+v,0)) * 100)}%
      </div>
    </div>
  );
}

// ───── Item card prompt ─────
function ItemPrompt({ n, total, pilar, text }) {
  return (
    <div className="fade-in" key={n}>
      <div className="item-eyebrow">
        <span className="item-pilar-tag">Pilar {pilar.num} · {pilar.curto}</span>
        <span className="item-counter">Pergunta {n} de {total}</span>
      </div>
      <h2 className="item-prompt">{text}</h2>
    </div>
  );
}

// ───── Pilar transition (breath) ─────
function PilarBreath({ pilar, onContinue }) {
  return (
    <div className="pilar-breath fade-in" key={pilar.id}>
      <span className="eyebrow">Pilar {pilar.num}</span>
      <div className="pilar-breath__num">{pilar.num}</div>
      <h2 className="pilar-breath__title serif">{pilar.titulo}</h2>
      <p className="pilar-breath__sub">{pilar.sub} Respire e siga respondendo pelo que você vive, não pelo que gostaria de viver.</p>
      <button className="btn btn--primary btn--lg" onClick={onContinue}>
        Começar
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
      </button>
    </div>
  );
}

// ───── Generic page wrapper ─────
function PageWrap({ children, narrow }) {
  return (
    <div className={"form-stage" + (narrow ? "" : " form-stage--wide")}>
      {children}
    </div>
  );
}

Object.assign(window, {
  BrandSigno, BrandHeader, AppFooter, MethodSeal,
  Likert, PilarProgress, ItemPrompt, PilarBreath, PageWrap,
});

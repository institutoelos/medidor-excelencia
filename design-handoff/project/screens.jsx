// screens.jsx — non-form screens: Cover (router landing), Admin, Print preview navigation

const { useState, useEffect, useMemo } = React;

// ───── Landing page (public) ─────
function CoverScreen({ onPick }) {
  return (
    <div className="app-shell">
      <BrandHeader onHome={() => window.__navigate?.("cover")} />
      <main style={{flex: 1}}>
        {/* HERO */}
        <section style={{maxWidth: 1200, margin: "0 auto", padding: "56px 24px 24px"}}>
          <div className="fade-in">
            <span className="eyebrow">ELO Business · Programa de Excelência Empresarial</span>
            <h1 className="serif" style={{
              fontSize: "clamp(48px, 8vw, 104px)",
              lineHeight: 0.98,
              letterSpacing: "-0.03em",
              margin: "20px 0 28px",
              maxWidth: 1080,
              textWrap: "pretty",
            }}>
              Medidor de Excelência<br/>
              <span style={{color: "var(--copper)"}}>· Pilar Pessoas</span>
            </h1>
            <p style={{fontSize: 19, color: "var(--ink-2)", maxWidth: 700, lineHeight: 1.5, textWrap: "pretty"}}>
              Diagnóstico semestral da saúde do time em três dimensões: <strong>Cultura, Tribo e Engajamento</strong> · <strong>Educação</strong> · <strong>Feedback e Mudança de Comportamento</strong>. Aplicado na entrada da empresa no ELO Business e a cada 6 meses como aferição de evolução.
            </p>

            <div style={{display:"flex", gap: 14, alignItems: "center", flexWrap: "wrap", marginTop: 36}}>
              <MethodSeal />
              <span style={{color: "var(--ink-dim)", fontSize: 12}}>·</span>
              <span style={{fontSize: 12, color: "var(--ink-dim)"}}>58 itens · escala Likert · ~10 minutos</span>
            </div>
          </div>
        </section>

        {/* PROOF NUMBERS */}
        <section style={{maxWidth: 1200, margin: "0 auto", padding: "32px 24px", borderTop: "1.5px solid var(--hairline-strong)", marginTop: 40}}>
          <div className="stats-3" style={{gap: 32}}>
            <div className="stat">
              <div className="stat__label">Versão Colaborador</div>
              <div className="stat__num">58</div>
              <div className="stat__hint">itens + âncora + NPS + retenção + demográficos</div>
            </div>
            <div className="stat">
              <div className="stat__label">Versão Sócios</div>
              <div className="stat__num">41<span style={{fontSize:24, color:"var(--ink-dim)"}}>+17</span></div>
              <div className="stat__hint">itens espelho ao time + itens sobre o sistema construído</div>
            </div>
            <div className="stat">
              <div className="stat__label">Entregável central</div>
              <div className="stat__num">12</div>
              <div className="stat__hint">seções de relatório · com Relatório de Gap por item</div>
            </div>
          </div>
        </section>

        {/* PILLARS */}
        <section style={{maxWidth: 1200, margin: "0 auto", padding: "56px 24px"}}>
          <div className="eyebrow" style={{marginBottom: 16}}>Três pilares</div>
          <h2 className="serif" style={{fontSize: "clamp(32px, 4vw, 52px)", margin: "0 0 36px", letterSpacing: "-0.02em", lineHeight: 1.1, maxWidth: 900}}>
            O que faz uma empresa ser um excelente lugar para se trabalhar.
          </h2>

          <div style={{display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))", gap: 18}}>
            {window.MEDIDOR_DATA.pilares.map((p, i) => (
              <div className="card" key={p.id} style={{padding: 24, position: "relative"}}>
                <div style={{
                  fontFamily: "var(--font-display)",
                  fontSize: 36, color: "var(--copper)", lineHeight: 1,
                  marginBottom: 14,
                }}>{p.num}</div>
                <div className="eyebrow">Pilar {p.num}</div>
                <h3 className="serif" style={{fontSize: 26, margin: "4px 0 12px", letterSpacing: "-0.01em", lineHeight: 1.15}}>{p.titulo}</h3>
                <p style={{margin: 0, color: "var(--ink-2)", fontSize: 14, lineHeight: 1.5}}>
                  {p.sub}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* HOW IT WORKS */}
        <section style={{background: "var(--paper-2)", borderTop: "0.5px solid var(--hairline)", borderBottom: "0.5px solid var(--hairline)"}}>
          <div style={{maxWidth: 1200, margin: "0 auto", padding: "56px 24px"}}>
            <div className="eyebrow" style={{marginBottom: 16}}>Como funciona</div>
            <h2 className="serif" style={{fontSize: "clamp(28px, 3.4vw, 44px)", margin: "0 0 40px", letterSpacing: "-0.02em", lineHeight: 1.1, maxWidth: 760}}>
              Duas versões espelhadas. Um relatório que mostra o que o sócio não vê.
            </h2>

            <div style={{display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))", gap: 24}}>
              {[
                { num: "01", title: "Coleta em 7 dias", body: "Cada pessoa do time recebe um link único e responde no próprio ritmo. Pode pausar e retomar." },
                { num: "02", title: "Sócios respondem em paralelo", body: "41 perguntas espelho ao time + 17 sobre o sistema que ele próprio construiu." },
                { num: "03", title: "Cruzamento de percepções", body: "O Relatório de Gap revela onde o dono enxerga um sistema que o time não vive." },
                { num: "04", title: "Linha de base + reaferição", body: "Mesmos números reaferidos em 6 e 12 meses — mede a evolução do trabalho." },
              ].map((s) => (
                <div key={s.num}>
                  <div style={{fontFamily: "var(--font-display)", fontSize: 14, color: "var(--copper)", letterSpacing: "0.06em", marginBottom: 10}}>{s.num}</div>
                  <h4 className="serif" style={{fontSize: 22, margin: "0 0 10px", lineHeight: 1.2, letterSpacing: "-0.01em"}}>{s.title}</h4>
                  <p style={{margin: 0, color: "var(--ink-2)", fontSize: 14, lineHeight: 1.5}}>{s.body}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* METHOD / TRUST */}
        <section style={{maxWidth: 1200, margin: "0 auto", padding: "56px 24px"}}>
          <div style={{display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: 40}}>
            <div>
              <div className="eyebrow" style={{marginBottom: 16}}>Método</div>
              <h2 className="serif" style={{fontSize: "clamp(28px, 3.2vw, 40px)", margin: "0 0 18px", letterSpacing: "-0.02em", lineHeight: 1.1}}>
                Padrão de mercado, vocabulário ELOS.
              </h2>
              <p style={{margin: 0, color: "var(--ink-2)", fontSize: 15, lineHeight: 1.55, maxWidth: 520}}>
                Redação comportamental em primeira pessoa, escala Likert de 5 pontos, pergunta-âncora síntese — herdados do Trust Index (GPTW). NPS interno calculado pela fórmula clássica. Reportagem em Top 2 Box + média ponderada, comparável externamente.
              </p>
            </div>

            <div style={{display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12}}>
              {[
                { k: "Likert 5 pontos", v: "Padrão Trust Index" },
                { k: "Top 2 Box + Média", v: "Comparabilidade externa" },
                { k: "eNPS clássico", v: "% Promotores − % Detratores" },
                { k: "Anonimato 5+", v: "Recortes < 5 são suprimidos" },
                { k: "Pesos iguais", v: "Cultura · Educação · Feedback" },
                { k: "Regra de gate", v: "Pilar < 60 sinaliza alerta" },
              ].map((m) => (
                <div key={m.k} style={{padding: "16px 0", borderTop: "0.5px solid var(--hairline)"}}>
                  <div style={{fontSize: 13, fontWeight: 600}}>{m.k}</div>
                  <div style={{fontSize: 12, color: "var(--ink-dim)", marginTop: 2}}>{m.v}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* WHO IT'S FOR / DEMO ENTRY */}
        <section style={{background: "var(--ink)", color: "var(--paper)"}}>
          <div style={{maxWidth: 1200, margin: "0 auto", padding: "64px 24px"}}>
            <div style={{display: "flex", justifyContent: "space-between", alignItems: "flex-end", flexWrap: "wrap", gap: 32, marginBottom: 36}}>
              <div>
                <div className="eyebrow" style={{color: "rgba(245,244,240,.55)"}}>Para empresários no ELO Business</div>
                <h2 className="serif" style={{fontSize: "clamp(32px, 4vw, 56px)", margin: "16px 0 0", letterSpacing: "-0.02em", lineHeight: 1.05, maxWidth: 720, color: "var(--paper)"}}>
                  Comece o seu programa com um diagnóstico real.
                </h2>
              </div>
              <BrandSigno size={56} />
            </div>

            <p style={{maxWidth: 600, fontSize: 16, color: "rgba(245,244,240,.78)", lineHeight: 1.55, marginBottom: 36}}>
              O Medidor de Excelência é aplicado na primeira semana após a contratação. O relatório vira o documento-âncora do trabalho de 12 meses no Pilar Pessoas — entregue ao empresário na primeira sessão de mentoria.
            </p>

            <div style={{display: "flex", gap: 14, flexWrap: "wrap"}}>
              <a href="https://wa.me/5531987902720" className="btn btn--copper btn--lg" style={{textDecoration: "none"}}>
                Falar com a equipe
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
              </a>
              <span style={{display:"inline-flex", alignItems: "center", gap: 12, fontSize: 12, color: "rgba(245,244,240,.55)"}}>
                +55 31 98790-2720 · Deisi Oliveira
              </span>
            </div>
          </div>
        </section>

        {/* DEMO ENTRY — clearly marked as preview */}
        <section style={{maxWidth: 1200, margin: "0 auto", padding: "40px 24px 24px"}}>
          <div className="card card--soft" style={{padding: 24, border: "0.5px dashed var(--hairline)"}}>
            <div style={{display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: 20}}>
              <div style={{flex: "1 1 280px"}}>
                <div className="eyebrow" style={{color: "var(--copper)"}}>Visualização da demo</div>
                <h3 className="serif" style={{fontSize: 24, margin: "8px 0 8px", letterSpacing: "-0.01em"}}>Veja como cada pessoa experiencia o diagnóstico.</h3>
                <p style={{margin: 0, color: "var(--ink-dim)", fontSize: 13, maxWidth: 520, lineHeight: 1.5}}>
                  Em produção, cada respondente recebe um link único por email — não há tela de seleção. Os atalhos abaixo existem só para você navegar pelas duas versões do formulário.
                </p>
              </div>
              <div style={{display: "flex", gap: 10, flexWrap: "wrap"}}>
                <button className="btn btn--ghost" onClick={() => onPick("colab")}>Entrar como colaborador →</button>
                <button className="btn btn--ghost" onClick={() => onPick("socio")}>Entrar como sócio →</button>
              </div>
            </div>
            <hr className="divider" style={{margin: "20px 0"}} />
            <div style={{display: "flex", gap: 10, flexWrap: "wrap", fontSize: 12, color: "var(--ink-dim)", alignItems: "center"}}>
              <span>Outras telas da demo:</span>
              <button className="btn btn--quiet" style={{padding: "4px 10px", fontSize: 12}} onClick={() => window.__navigate?.("admin")}>Painel da empresa</button>
              <button className="btn btn--quiet" style={{padding: "4px 10px", fontSize: 12}} onClick={() => window.__navigate?.("report")}>Relatório de exemplo</button>
            </div>
          </div>
        </section>
      </main>
      <AppFooter />
    </div>
  );
}

// ───── Admin ─────
function AdminScreen() {
  const D = window.MEDIDOR_DATA;
  const { rodada } = D.mock;
  const { respondentes, elegiveis } = rodada;
  const total = elegiveis.colab + elegiveis.socio;
  const done = respondentes.colab + respondentes.socio;
  const pct = Math.round((done / total) * 100);

  // Mocked recent activity
  const eventos = [
    { hora: "Hoje · 14:22", evento: "Resposta recebida", quem: "Colaborador · 5 anos · Comercial" },
    { hora: "Hoje · 12:08", evento: "Resposta recebida", quem: "Colaborador · 1–3 anos · Atendimento" },
    { hora: "Hoje · 11:51", evento: "Lembrete enviado", quem: "12 colaboradores" },
    { hora: "Ontem · 18:34", evento: "Resposta recebida", quem: "Sócio · Lucas R." },
    { hora: "Ontem · 16:20", evento: "Resposta recebida", quem: "Colaborador · 6m–1a · Conteúdo & Mídia" },
    { hora: "Ontem · 09:15", evento: "Coleta iniciada", quem: "Rodada 1 aberta" },
  ];

  return (
    <div className="app-shell">
      <BrandHeader onHome={() => window.__navigate?.("cover")} />
      <main style={{flex: 1, maxWidth: 1200, margin: "0 auto", padding: "32px 24px 64px", width: "100%"}}>
        <div className="fade-in">
          <div style={{display:"flex", justifyContent:"space-between", alignItems:"flex-end", flexWrap:"wrap", gap: 20, marginBottom: 32}}>
            <div>
              <span className="eyebrow">Painel do gestor</span>
              <h1 className="serif" style={{fontSize: 44, margin: "10px 0 6px", letterSpacing: "-0.02em"}}>{rodada.empresa}</h1>
              <div style={{color: "var(--ink-dim)", fontSize: 14}}>{rodada.rodadaLabel} · {rodada.dataAplicacao}</div>
            </div>
            <div style={{display:"flex", gap: 10, flexWrap: "wrap"}}>
              <button className="btn btn--ghost">Enviar lembrete</button>
              <button className="btn btn--primary" onClick={() => window.__navigate?.("report")}>Ver relatório</button>
            </div>
          </div>

          {/* Stats */}
          <div className="stats-3" style={{marginBottom: 36}}>
            <div className="stat">
              <div className="stat__label">Coleta concluída</div>
              <div className="stat__num">{pct}<span style={{fontSize:24, color:"var(--ink-dim)"}}>%</span></div>
              <div className="stat__hint">{done} de {total} respondentes</div>
            </div>
            <div className="stat">
              <div className="stat__label">Colaboradores</div>
              <div className="stat__num">{respondentes.colab}<span style={{fontSize:24, color:"var(--ink-dim)"}}>/{rodada.elegiveis.colab}</span></div>
              <div className="stat__hint">{rodada.elegiveis.colab - respondentes.colab} pendentes</div>
            </div>
            <div className="stat">
              <div className="stat__label">Sócios</div>
              <div className="stat__num">{respondentes.socio}<span style={{fontSize:24, color:"var(--ink-dim)"}}>/{rodada.elegiveis.socio}</span></div>
              <div className="stat__hint">Coleta completa</div>
            </div>
          </div>

          <div style={{display:"grid", gridTemplateColumns: "1.6fr 1fr", gap: 24}}>
            {/* Collection by area */}
            <div className="card">
              <div className="eyebrow" style={{marginBottom: 14}}>Coleta por área</div>
              {[
                { area: "Atendimento", done: 9, total: 11 },
                { area: "Conteúdo & Mídia", done: 7, total: 8 },
                { area: "Operações", done: 8, total: 10 },
                { area: "Comercial", done: 5, total: 6 },
                { area: "Administrativo", done: 3, total: 3 },
              ].map((row) => (
                <div className="report-bar-row" key={row.area} style={{gridTemplateColumns: "150px 1fr 60px", padding: "12px 0"}}>
                  <div style={{fontSize: 13}}>{row.area}</div>
                  <div>
                    <div className="report-bar-row__bar-wrap">
                      <div className="report-bar-row__bar" style={{"--w": (row.done/row.total*100) + "%"}}></div>
                    </div>
                  </div>
                  <div style={{textAlign:"right", fontSize: 13, fontVariantNumeric:"tabular-nums"}}>
                    <strong>{row.done}</strong><span style={{color:"var(--ink-dim)"}}>/{row.total}</span>
                  </div>
                </div>
              ))}
            </div>

            {/* Activity */}
            <div className="card">
              <div className="eyebrow" style={{marginBottom: 14}}>Atividade recente</div>
              {eventos.map((e, i) => (
                <div key={i} style={{padding: "10px 0", borderBottom: i < eventos.length - 1 ? "0.5px solid var(--hairline)" : "0"}}>
                  <div style={{fontSize: 11, color: "var(--ink-dim)", marginBottom: 2}}>{e.hora}</div>
                  <div style={{fontSize: 13}}><strong>{e.evento}</strong> · <span style={{color:"var(--ink-dim)"}}>{e.quem}</span></div>
                </div>
              ))}
            </div>
          </div>

          <div style={{marginTop: 36}}>
            <div className="eyebrow" style={{marginBottom: 14}}>Configuração da rodada</div>
            <div className="card">
              <dl className="kv" style={{gridTemplateColumns: "200px 1fr", gap: "14px 24px"}}>
                <dt>Empresa</dt><dd>Instituto ELOS · CNPJ 00.000.000/0001-00</dd>
                <dt>Tipo de rodada</dt><dd>Entrada · diagnóstico inicial</dd>
                <dt>Janela de coleta</dt><dd>23/05/2026 a 29/05/2026 (7 dias)</dd>
                <dt>Próxima reaferição</dt><dd>Mês 6 — 23/11/2026</dd>
                <dt>Áreas pré-configuradas</dt><dd>Atendimento · Conteúdo & Mídia · Operações · Comercial · Administrativo</dd>
                <dt>Link Colaborador</dt><dd><code style={{fontSize:12, color:"var(--copper-900)"}}>elobusiness.com.br/m/inst-elos/colab</code></dd>
                <dt>Link Sócios</dt><dd><code style={{fontSize:12, color:"var(--copper-900)"}}>elobusiness.com.br/m/inst-elos/socio</code></dd>
                <dt>Mentor responsável</dt><dd>Fabinho · ELO Business</dd>
              </dl>
            </div>
          </div>
        </div>
      </main>
      <AppFooter />
    </div>
  );
}

Object.assign(window, { CoverScreen, AdminScreen });

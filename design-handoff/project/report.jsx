// report.jsx — Relatório completo (12 seções), padrão ELO Business claro.

const { useMemo } = React;

function ReportScreen() {
  const D = window.MEDIDOR_DATA;
  const { rodada, faixa, colabPilarScores, sociosPilarScores, medidor, retencao, enps, demograficos } = D.mock;
  const colab = D.mock.colab.t2b;
  const socio = D.mock.socio.t2b;

  // Detect gate-triggered pillars
  const gated = D.pilares
    .map((p, i) => ({ p, score: colabPilarScores[i], i }))
    .filter((x) => x.score < 60);

  return (
    <div className="app-shell">
      <BrandHeader onHome={() => window.__navigate?.("cover")} />
      <main style={{flex: 1, paddingBottom: 64, background: "var(--paper)"}}>
        <div style={{maxWidth: 1100, margin: "0 auto", padding: "16px 24px", display: "flex", gap: 12, alignItems: "center", justifyContent: "flex-end", flexWrap: "wrap"}}>
          <span className="tag tag--ghost">Relatório de exemplo · dados fictícios</span>
          <button className="btn btn--ghost" onClick={() => window.print()}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M6 9V3h12v6M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2M6 14h12v8H6z" stroke="currentColor" strokeWidth="1.5"/></svg>
            Imprimir / PDF
          </button>
        </div>

        <div className="report-page">

          {/* ── 1. CAPA ── */}
          <section className="report-section" style={{paddingTop: 16, paddingBottom: 60, borderBottom: "1.5px solid var(--hairline-strong)"}}>
            <div style={{display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 20, marginBottom: 80, flexWrap: "wrap"}}>
              <div style={{display: "flex", alignItems: "center", gap: 14}}>
                <BrandSigno size={32} />
                <div>
                  <div style={{fontFamily: "Tungsten, var(--font-body)", fontWeight: 700, fontSize: 18, letterSpacing: "0.05em"}}>ELO BUSINESS</div>
                  <div style={{fontSize: 11, color: "var(--ink-dim)", letterSpacing: "0.16em", textTransform: "uppercase"}}>Medidor de Excelência</div>
                </div>
              </div>
              <div style={{textAlign: "right", fontSize: 12, color: "var(--ink-dim)"}}>
                {rodada.rodadaLabel}<br/>
                {rodada.dataAplicacao}
              </div>
            </div>

            <div className="eyebrow">Relatório · Pilar Pessoas</div>
            <h1 className="serif" style={{fontSize: "clamp(48px, 8vw, 92px)", lineHeight: 0.98, letterSpacing: "-0.03em", margin: "16px 0 24px"}}>
              {rodada.empresa}
            </h1>
            <p style={{fontSize: 17, color: "var(--ink-2)", maxWidth: 600, lineHeight: 1.5}}>
              Diagnóstico de entrada da saúde do Pilar Pessoas, em três dimensões: Cultura, Tribo e Engajamento — Educação — Feedback e Mudança de Comportamento.
            </p>

            <div style={{marginTop: 80, display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))", gap: 24, borderTop: "1.5px solid var(--hairline-strong)", paddingTop: 24}}>
              <div>
                <div className="eyebrow">Respondentes</div>
                <div style={{fontFamily: "var(--font-display)", fontSize: 36, marginTop: 4}}>{rodada.respondentes.colab + rodada.respondentes.socio}<span style={{color: "var(--ink-dim)", fontSize: 18}}> / {rodada.elegiveis.colab + rodada.elegiveis.socio}</span></div>
                <div style={{fontSize: 11, color: "var(--ink-dim)"}}>Colaboradores e sócios</div>
              </div>
              <div>
                <div className="eyebrow">Coleta</div>
                <div style={{fontFamily: "var(--font-display)", fontSize: 36, marginTop: 4}}>89<span style={{color: "var(--ink-dim)", fontSize: 18}}>%</span></div>
                <div style={{fontSize: 11, color: "var(--ink-dim)"}}>Acima do mínimo do método</div>
              </div>
              <div>
                <div className="eyebrow">Mentor</div>
                <div style={{fontFamily: "var(--font-display)", fontSize: 22, marginTop: 6, lineHeight: 1.1}}>Fabinho</div>
                <div style={{fontSize: 11, color: "var(--ink-dim)"}}>ELO Business · Pilar Pessoas</div>
              </div>
              <div>
                <div className="eyebrow">Linha de base</div>
                <div style={{fontFamily: "var(--font-display)", fontSize: 22, marginTop: 6, lineHeight: 1.1}}>Reaferição em 6 meses</div>
                <div style={{fontSize: 11, color: "var(--ink-dim)"}}>23 de novembro de 2026</div>
              </div>
            </div>
          </section>

          {/* ── 2. RESUMO EXECUTIVO ── */}
          <ReportSection num="02" title="Resumo executivo">
            <div className="medidor-hero">
              <div>
                <div className="eyebrow">Medidor de Excelência</div>
                <div className="medidor-hero__number" style={{color: medidor < 60 ? "var(--amber)" : medidor < 75 ? "var(--ink)" : "var(--green)"}}>{medidor}</div>
                <FaixaChip score={medidor} />
              </div>
              <div style={{flex: 1, minWidth: 240}}>
                <div className="eyebrow">Padrão observado</div>
                <p style={{fontSize: 15, lineHeight: 1.55, marginTop: 8, maxWidth: 540, textWrap: "pretty"}}>
                  Cultura saudável (<strong>{colabPilarScores[0]}</strong>) sustenta o time. Educação está <strong>frágil ({colabPilarScores[1]})</strong> e Feedback no limite ({colabPilarScores[2]}) — ambos abaixo do piso de 60 e travam a sustentação do conjunto. O dono enxerga o sistema funcionando em 7 pontos onde o time não vive: cegueira do dono concentrada em Educação e Confiança na liderança.
                </p>
              </div>
            </div>

            {/* Pillar mini */}
            <div style={{display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 18, marginTop: 36}}>
              {D.pilares.map((p, i) => (
                <PilarMiniCard key={p.id} pilar={p} score={colabPilarScores[i]} />
              ))}
            </div>

            <div style={{display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 18, marginTop: 18}}>
              <div className="card card--soft" style={{padding: 18}}>
                <div className="eyebrow">eNPS</div>
                <div style={{fontFamily: "var(--font-display)", fontSize: 36, marginTop: 6, color: "var(--green)"}}>+{enps.score}</div>
                <div style={{fontSize: 11, color: "var(--ink-dim)", marginTop: 2}}>{enps.promotores}% promotores · {enps.detratores}% detratores</div>
              </div>
              <div className="card card--soft" style={{padding: 18}}>
                <div className="eyebrow">Pergunta-âncora</div>
                <div style={{fontFamily: "var(--font-display)", fontSize: 36, marginTop: 6}}>4,1<span style={{fontSize:18, color:"var(--ink-dim)"}}> / 5</span></div>
                <div style={{fontSize: 11, color: "var(--ink-dim)", marginTop: 2}}>Time vs. sócio: gap de −0,6</div>
              </div>
              <div className="card card--soft" style={{padding: 18}}>
                <div className="eyebrow">Cegueiras do dono</div>
                <div style={{fontFamily: "var(--font-display)", fontSize: 36, marginTop: 6, color: "var(--red)"}}>7</div>
                <div style={{fontSize: 11, color: "var(--ink-dim)", marginTop: 2}}>itens com gap ≥ 15 pts</div>
              </div>
            </div>
          </ReportSection>

          {/* ── 3. PAINEL GERAL ── */}
          <ReportSection num="03" title="Painel geral">
            {/* Gate visual */}
            {gated.length > 0 && (
              <div className="card" style={{
                borderLeft: "3px solid var(--red)",
                background: "var(--red-soft)",
                padding: 20, marginBottom: 32,
              }}>
                <div className="tag tag--ink" style={{background:"var(--red)", color:"#fff"}}>Atenção · regra de gate visual</div>
                <p style={{fontSize: 15, marginTop: 12, marginBottom: 0, lineHeight: 1.55, color: "var(--red)"}}>
                  O Medidor está em <strong>{medidor}</strong>, mas o pilar <strong>{gated[0].p.titulo}</strong> está em <strong>{gated[0].score}</strong>{gated.length > 1 && <> e o pilar <strong>{gated[1].p.titulo}</strong> está em <strong>{gated[1].score}</strong></>} — trava{gated.length > 1 ? "m" : ""} a sustentação do conjunto. Antes de avançar, é preciso reconstruir esse alicerce.
                </p>
              </div>
            )}

            <div style={{display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 24}}>
              {D.pilares.map((p, i) => (
                <PilarGauge key={p.id} pilar={p} score={colabPilarScores[i]} />
              ))}
            </div>

            <hr className="divider" style={{margin: "32px 0"}} />

            <div className="kv" style={{gridTemplateColumns: "1fr 1fr", gap: "10px 32px"}}>
              <dt>Medidor de Excelência (0–100)</dt><dd className="num">{medidor}</dd>
              <dt>Cultura, Tribo e Engajamento</dt><dd className="num">{colabPilarScores[0]}</dd>
              <dt>Educação</dt><dd className="num">{colabPilarScores[1]}</dd>
              <dt>Feedback e Mudança de Comportamento</dt><dd className="num">{colabPilarScores[2]}</dd>
              <dt>eNPS</dt><dd className="num">+{enps.score}</dd>
              <dt>Pergunta-âncora (colaborador, 1–5)</dt><dd className="num">4,1</dd>
              <dt>Pergunta-âncora (sócios, 1–5)</dt><dd className="num">4,7</dd>
              <dt>Respondentes válidos</dt><dd className="num">32 colab / 2 sócios</dd>
            </div>
          </ReportSection>

          {/* ── 4-6. PILARES ── */}
          {D.pilares.map((p, idx) => (
            <PilarDetailSection
              key={p.id}
              p={p}
              idx={idx}
              colab={colab}
              socio={socio}
              labels={D.itemsColab}
              score={colabPilarScores[idx]}
              num={String(idx + 4).padStart(2, "0")}
            />
          ))}

          {/* ── 7. RETENÇÃO ── */}
          <ReportSection num="07" title="O que segura o time aqui">
            <p style={{maxWidth: 640, color: "var(--ink-dim)", marginBottom: 28, fontSize: 14, lineHeight: 1.55}}>
              Distribuição da pergunta: <em>"O principal motivo que me faz permanecer nessa empresa é…"</em>. Mostra sobre o que a cultura está efetivamente segurando o pessoal — vetor estratégico para o trabalho de 12 meses.
            </p>
            <div>
              {retencao.map((r, i) => (
                <div className="donut-row" key={r.label}>
                  <div>{r.label}</div>
                  <div style={{minWidth: 180, width: 220, maxWidth: "40vw"}}>
                    <div className="donut-row__bar">
                      <div className="donut-row__fill" style={{
                        width: r.pct + "%",
                        background: i === 0 ? "var(--copper)" : i === 1 ? "var(--ink)" : "var(--ink-dim)"
                      }}></div>
                    </div>
                  </div>
                  <div className="donut-row__num">{r.pct}<span style={{color:"var(--ink-dim)", fontSize:14}}>%</span></div>
                </div>
              ))}
            </div>
            <div className="card card--soft" style={{marginTop: 28, padding: 20}}>
              <div className="eyebrow">Leitura clínica</div>
              <p style={{fontSize: 14, lineHeight: 1.55, marginTop: 8, marginBottom: 0}}>
                O vetor dominante é <strong>propósito + vínculo</strong> (59% dos respondentes). A empresa segura o time pela narrativa e pelo time, não pelo desenvolvimento — coerente com a fragilidade observada em Educação. Vetor saudável, mas frágil: se o propósito esmaecer, a base de retenção desaba.
              </p>
            </div>
          </ReportSection>

          {/* ── 8. DEMOGRÁFICOS ── */}
          <ReportSection num="08" title="Cortes demográficos">
            <p style={{maxWidth: 640, color: "var(--ink-dim)", marginBottom: 24, fontSize: 14, lineHeight: 1.55}}>
              Recortes só são reportados quando há 5 ou mais respondentes. Os destacados em <strong style={{color: "var(--red)"}}>vermelho</strong> apresentam gap ≥ 10 pts em relação ao Medidor geral ({medidor}).
            </p>

            <DemoTable
              title="Por tempo de casa"
              rows={[
                { label: "Até 6 meses", n: 6, med: 74, c: 72, e: 64, f: 65 },
                { label: "6 meses a 1 ano", n: 8, med: 67, c: 76, e: 58, f: 65 },
                { label: "1 a 3 anos", n: 12, med: 61, c: 73, e: 51, f: 58 },
                { label: "3 a 5 anos", n: 5, med: 54, c: 65, e: 44, f: 52, hot: true },
                { label: "Mais de 5 anos", n: 1, suppressed: true },
              ]}
            />

            <DemoTable
              title="Por tipo de cargo"
              rows={[
                { label: "Liderança sênior", n: 3, suppressed: true },
                { label: "Liderança intermediária", n: 6, med: 78, c: 84, e: 71, f: 78 },
                { label: "Colaborador", n: 21, med: 59, c: 70, e: 49, f: 57, hot: true },
                { label: "Estagiário / aprendiz", n: 2, suppressed: true },
              ]}
            />

            <DemoTable
              title="Por área"
              rows={[
                { label: "Atendimento", n: 9, med: 58, c: 68, e: 47, f: 58, hot: true },
                { label: "Conteúdo & Mídia", n: 7, med: 71, c: 81, e: 64, f: 67 },
                { label: "Operações", n: 8, med: 60, c: 71, e: 51, f: 58 },
                { label: "Comercial", n: 5, med: 64, c: 76, e: 54, f: 62 },
                { label: "Administrativo", n: 3, suppressed: true },
              ]}
            />
          </ReportSection>

          {/* ── 9. GAP REPORT ── */}
          <ReportSection num="09" title="Relatório de Gap · Sócio vs. Colaborador">
            <p style={{maxWidth: 640, color: "var(--ink-dim)", marginBottom: 24, fontSize: 14, lineHeight: 1.55}}>
              41 itens espelho comparados lado a lado. <strong style={{color: "var(--red)"}}>Cegueira do dono</strong> (Sócio &gt; Colab em 15+ pts) — alavanca máxima de intervenção. <strong style={{color: "var(--green)"}}>Alinhamento</strong> (gap até 14 pts). <strong style={{color: "var(--amber)"}}>Subestimação</strong> (Colab &gt; Sócio em 15+ pts).
            </p>

            <GapSummaryStats colab={colab} socio={socio} />

            {/* Top gaps */}
            <div style={{marginTop: 32}}>
              <div className="eyebrow" style={{marginBottom: 14}}>Top 5 cegueiras do dono</div>
              <div>
                {topGaps(colab, socio, "ceg", 5).map((g) => (
                  <GapBarRow key={g.n} n={g.n} text={D.itemsColab[g.n - 1]} colab={g.colab} socio={g.socio} />
                ))}
              </div>
            </div>

            <div style={{marginTop: 32}}>
              <div className="eyebrow" style={{marginBottom: 14}}>Top 5 alinhamentos positivos</div>
              <div>
                {topGaps(colab, socio, "ali", 5).map((g) => (
                  <GapBarRow key={g.n} n={g.n} text={D.itemsColab[g.n - 1]} colab={g.colab} socio={g.socio} />
                ))}
              </div>
            </div>

            <div style={{marginTop: 32}}>
              <div className="eyebrow" style={{marginBottom: 14}}>Top 3 subestimações</div>
              <div>
                {topGaps(colab, socio, "sub", 3).map((g) => (
                  <GapBarRow key={g.n} n={g.n} text={D.itemsColab[g.n - 1]} colab={g.colab} socio={g.socio} />
                ))}
              </div>
            </div>
          </ReportSection>

          {/* ── 10. CONSCIÊNCIA SISTÊMICA ── */}
          <ReportSection num="10" title="Consciência Sistêmica do Empresário">
            <p style={{maxWidth: 640, color: "var(--ink-dim)", marginBottom: 24, fontSize: 14, lineHeight: 1.55}}>
              17 itens exclusivos do sócio. Medem a consciência sobre o sistema que ele construiu — não a vivência do time. Base do trabalho de mentoria individual no ELO Business.
            </p>
            {(() => {
              const div = socio.slice(41, 58);
              const ind = Math.round(div.reduce((s,v) => s+v, 0) / div.length);
              const cul = Math.round(socio.slice(41,48).reduce((s,v)=>s+v,0)/7);
              const edu = Math.round(socio.slice(48,53).reduce((s,v)=>s+v,0)/5);
              const fee = Math.round(socio.slice(53,58).reduce((s,v)=>s+v,0)/5);
              return (
                <>
                  <div className="medidor-hero" style={{marginBottom: 32}}>
                    <div>
                      <div className="eyebrow">Índice de Consciência Sistêmica</div>
                      <div className="medidor-hero__number" style={{fontSize: 120, color: ind < 60 ? "var(--amber)" : "var(--ink)"}}>{ind}</div>
                      <FaixaChip score={ind} />
                    </div>
                  </div>
                  <div style={{display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 16, marginBottom: 32}}>
                    <SubpilarCard label="Cultura" score={cul} />
                    <SubpilarCard label="Educação" score={edu} />
                    <SubpilarCard label="Feedback" score={fee} />
                  </div>

                  <div className="eyebrow" style={{marginBottom: 14}}>Pontos cegos do empresário (itens com nota baixa)</div>
                  {socio.slice(41, 58).map((v, i) => v < 50 ? { n: 42 + i, v } : null).filter(Boolean).slice(0, 5).map(({n, v}) => (
                    <div key={n} style={{padding: "12px 0", borderBottom: "0.5px solid var(--hairline)"}}>
                      <div style={{display:"flex", justifyContent:"space-between", gap: 16, alignItems: "flex-start"}}>
                        <div style={{fontSize: 13, lineHeight: 1.45, flex: 1}}>
                          <span style={{color: "var(--ink-muted)", fontSize: 11, marginRight: 8}}>{String(n).padStart(2,"0")}</span>
                          {D.itemsSocio[n - 1]}
                        </div>
                        <div style={{fontFamily: "var(--font-display)", fontSize: 22, color: "var(--red)", whiteSpace: "nowrap"}}>{v}</div>
                      </div>
                    </div>
                  ))}
                </>
              );
            })()}
          </ReportSection>

          {/* ── 11. PLANO DE AÇÃO ── */}
          <ReportSection num="11" title="Plano de ação prioritário">
            <p style={{maxWidth: 640, color: "var(--ink-dim)", marginBottom: 28, fontSize: 14, lineHeight: 1.55}}>
              Três frentes ordenadas por alavancagem: gate visual → maiores gaps → pontos cegos do empresário.
            </p>
            <PlanoCard
              num="01"
              titulo="Reconstruir o alicerce de Educação"
              porque="Pilar em 53 — abaixo do piso de 60. 4 dos 14 itens estão em zona crítica. Vetor dominante de risco para os próximos 12 meses."
              acoes={[
                "Desenhar onboarding estruturado com trilha clara por cargo (responde aos itens 31, 32 e 39).",
                "Calendarizar 1 ritual mensal de aprendizado em time, sob curadoria da liderança.",
                "Definir orçamento de educação por pessoa/ano e tornar isso público para o time.",
              ]}
              prazo="Mês 0 ao 3"
            />
            <PlanoCard
              num="02"
              titulo="Fechar as 7 cegueiras do dono"
              porque="Em 7 itens o sócio enxerga o sistema funcionando em até 32 pontos acima do que o time vive. Maior alavancagem de intervenção do diagnóstico."
              acoes={[
                "Sessão guiada de leitura dos itens com maior gap (esperada na 2ª mentoria).",
                "Definir como ouvir o time fora da pesquisa: 3 conversas 1:1 estruturadas por mês com colaboradores fora do círculo direto.",
                "Reaferir gaps específicos em 90 dias antes da rodada formal.",
              ]}
              prazo="Mês 0 ao 6"
            />
            <PlanoCard
              num="03"
              titulo="Sustentar o que já funciona em Cultura"
              porque="Cultura em 73 é o ativo dessa empresa. Vínculo entre pessoas (item 12 em 88) e respeito independente de cargo (item 28 em 84) são âncoras."
              acoes={[
                "Codificar os ritos de tribo existentes para que sobrevivam ao crescimento.",
                "Promover guardiões da cultura formalmente identificados — 2 a 4 pessoas além dos sócios.",
              ]}
              prazo="Continuado"
            />
          </ReportSection>

          {/* ── 12. LINHA DE BASE ── */}
          <ReportSection num="12" title="Linha de base para reaferição">
            <p style={{maxWidth: 640, color: "var(--ink-dim)", marginBottom: 24, fontSize: 14, lineHeight: 1.55}}>
              Tabela-resumo dos números que serão reaferidos em mês 6 (23/11/2026) e mês 12. Itens com regressão acima de 10 pontos serão sinalizados como alerta.
            </p>
            <div style={{border: "1.5px solid var(--hairline-strong)", borderRadius: "var(--r-md)", overflow: "hidden"}}>
              <table style={{width: "100%", borderCollapse: "collapse", fontSize: 14}}>
                <thead>
                  <tr style={{background: "var(--ink)", color: "var(--paper)"}}>
                    <th style={{textAlign:"left", padding: "14px 18px", fontWeight: 600, fontSize: 12, letterSpacing: "0.08em", textTransform: "uppercase"}}>Métrica</th>
                    <th style={{textAlign:"right", padding: "14px 18px", fontWeight: 600, fontSize: 12, letterSpacing: "0.08em", textTransform: "uppercase"}}>Entrada</th>
                    <th style={{textAlign:"right", padding: "14px 18px", fontWeight: 600, fontSize: 12, letterSpacing: "0.08em", textTransform: "uppercase", color: "var(--ink-muted)"}}>Mês 6</th>
                    <th style={{textAlign:"right", padding: "14px 18px", fontWeight: 600, fontSize: 12, letterSpacing: "0.08em", textTransform: "uppercase", color: "var(--ink-muted)"}}>Mês 12</th>
                  </tr>
                </thead>
                <tbody>
                  {[
                    { l: "Medidor de Excelência", v: medidor },
                    { l: "Cultura, Tribo e Engajamento", v: colabPilarScores[0] },
                    { l: "Educação", v: colabPilarScores[1] },
                    { l: "Feedback e Mudança de Comportamento", v: colabPilarScores[2] },
                    { l: "eNPS", v: "+" + enps.score },
                    { l: "Pergunta-âncora colaborador (1–5)", v: "4,1" },
                    { l: "Pergunta-âncora sócios (1–5)", v: "4,7" },
                    { l: "Índice de Consciência Sistêmica (sócios)", v: 50 },
                    { l: "Cegueiras do dono (itens ≥15 pts gap)", v: 7 },
                  ].map((r, i) => (
                    <tr key={i} style={{borderTop: "0.5px solid var(--hairline)"}}>
                      <td style={{padding: "12px 18px"}}>{r.l}</td>
                      <td style={{padding: "12px 18px", textAlign:"right", fontVariantNumeric: "tabular-nums", fontWeight: 600}}>{r.v}</td>
                      <td style={{padding: "12px 18px", textAlign:"right", color: "var(--ink-muted)"}}>—</td>
                      <td style={{padding: "12px 18px", textAlign:"right", color: "var(--ink-muted)"}}>—</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div style={{marginTop: 40, paddingTop: 28, borderTop: "1.5px solid var(--hairline-strong)", display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 16}}>
              <div style={{display:"flex", alignItems:"center", gap: 12}}>
                <BrandSigno size={28} />
                <div style={{fontSize: 12, color: "var(--ink-dim)"}}>
                  ELO Business · Medidor de Excelência v1.0 · Pilar Pessoas<br/>
                  Relatório gerado em 30/05/2026 · próxima rodada 23/11/2026
                </div>
              </div>
              <button className="btn btn--primary" onClick={() => window.print()}>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M6 9V3h12v6M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2M6 14h12v8H6z" stroke="currentColor" strokeWidth="1.5"/></svg>
                Imprimir relatório
              </button>
            </div>
          </ReportSection>

        </div>
      </main>
      <AppFooter />
    </div>
  );
}

// ───── Report helpers ─────

function ReportSection({ num, title, children }) {
  return (
    <section className="report-section" style={{paddingTop: 56, paddingBottom: 28}}>
      <div style={{display: "flex", alignItems: "baseline", gap: 12, marginBottom: 24}}>
        <span style={{fontFamily: "var(--font-display)", color: "var(--copper)", fontSize: 18, letterSpacing: "0.04em"}}>{num}</span>
        <h2 className="serif" style={{fontSize: 34, margin: 0, letterSpacing: "-0.015em", lineHeight: 1.15}}>{title}</h2>
      </div>
      {children}
    </section>
  );
}

function FaixaChip({ score }) {
  const f = window.MEDIDOR_DATA.mock.faixa(score);
  return (
    <span className={"faixa-chip faixa-chip--" + f.chip} style={{marginTop: 12}}>
      <span className="faixa-chip__dot" style={{background: f.chip === "green" ? "var(--green)" : f.chip === "amber" ? "var(--amber)" : "var(--red)"}}></span>
      {f.label}
    </span>
  );
}

function PilarMiniCard({ pilar, score }) {
  const f = window.MEDIDOR_DATA.mock.faixa(score);
  const color = f.chip === "green" ? "var(--green)" : f.chip === "amber" ? "var(--amber)" : "var(--red)";
  return (
    <div className="card" style={{padding: 20, borderTop: "3px solid " + color}}>
      <div style={{fontSize: 11, color: "var(--ink-dim)", letterSpacing: "0.12em", textTransform: "uppercase"}}>Pilar {pilar.num}</div>
      <div style={{fontSize: 14, fontWeight: 600, marginTop: 4, lineHeight: 1.3}}>{pilar.titulo}</div>
      <div style={{display: "flex", alignItems: "baseline", gap: 8, marginTop: 14}}>
        <div style={{fontFamily: "var(--font-display)", fontSize: 48, lineHeight: 1, color}}>{score}</div>
        <div style={{fontSize: 11, color: "var(--ink-dim)"}}>{f.label}</div>
      </div>
    </div>
  );
}

function PilarGauge({ pilar, score }) {
  const f = window.MEDIDOR_DATA.mock.faixa(score);
  const color = f.chip === "green" ? "var(--green)" : f.chip === "amber" ? "var(--amber)" : "var(--red)";
  // semicircle arc 0..100
  const r = 80, cx = 100, cy = 100;
  const angle = Math.PI * (1 - score / 100);
  const x = cx + r * Math.cos(angle);
  const y = cy - r * Math.sin(angle);
  const largeArc = score > 50 ? 1 : 0;
  return (
    <div>
      <div className="gauge">
        <svg viewBox="0 0 200 120">
          <path d={`M ${cx - r} ${cy} A ${r} ${r} 0 0 1 ${cx + r} ${cy}`} stroke="var(--paper-2)" strokeWidth="14" fill="none" strokeLinecap="round" />
          <path d={`M ${cx - r} ${cy} A ${r} ${r} 0 ${largeArc} 1 ${x} ${y}`} stroke={color} strokeWidth="14" fill="none" strokeLinecap="round" />
        </svg>
        <div className="gauge__num" style={{color}}>{score}</div>
      </div>
      <div className="gauge__label">Pilar {pilar.num} · {pilar.curto}</div>
    </div>
  );
}

function PilarDetailSection({ p, idx, colab, socio, labels, score, num }) {
  const [a, b] = p.ranges[0];
  const items = [];
  for (let i = a; i <= b; i++) items.push({ n: i, t2b: colab[i - 1], text: labels[i - 1] });
  const sortedAsc = [...items].sort((a, b) => a.t2b - b.t2b);
  const fragis = sortedAsc.slice(0, 3);
  const fortes = [...sortedAsc].reverse().slice(0, 3);

  return (
    <ReportSection num={num} title={p.titulo}>
      <div style={{display: "flex", alignItems: "flex-end", gap: 20, flexWrap: "wrap", marginBottom: 28}}>
        <div>
          <div className="eyebrow">Nota do pilar</div>
          <div style={{fontFamily: "var(--font-display)", fontSize: 92, lineHeight: 0.95}}>{score}</div>
          <FaixaChip score={score} />
        </div>
        <div style={{flex: 1, minWidth: 240}}>
          <div className="eyebrow">{items.length} itens · escala Likert 5 pts</div>
          <div style={{marginTop: 14, fontSize: 13, color: "var(--ink-dim)", lineHeight: 1.55}}>
            {p.subgroups.map((sg, i) => {
              const [sa, sb] = sg.range;
              const slice = colab.slice(sa-1, sb);
              const avg = Math.round(slice.reduce((s,v)=>s+v,0) / slice.length);
              return (
                <div key={i} style={{display: "flex", justifyContent: "space-between", padding: "6px 0", borderTop: "0.5px solid var(--hairline)"}}>
                  <span>{sg.label}</span>
                  <span className="num" style={{color: "var(--ink)", fontWeight: 600}}>{avg}</span>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      <div className="eyebrow" style={{marginBottom: 12, marginTop: 24}}>Itens · % Top 2 Box</div>
      {items.map((it) => (
        <ItemBar key={it.n} n={it.n} text={it.text} value={it.t2b} />
      ))}

      <div style={{display: "grid", gridTemplateColumns: "1fr 1fr", gap: 18, marginTop: 32}}>
        <div className="card card--soft" style={{padding: 18}}>
          <div className="eyebrow" style={{color: "var(--red)"}}>3 itens mais frágeis</div>
          {fragis.map((f) => (
            <div key={f.n} style={{padding: "10px 0", borderBottom: "0.5px solid var(--hairline)", display: "flex", gap: 12, alignItems: "flex-start"}}>
              <div style={{fontFamily:"var(--font-display)", color: "var(--red)", fontSize: 22, lineHeight: 1, minWidth: 36}}>{f.t2b}</div>
              <div style={{fontSize: 12, lineHeight: 1.45}}>{f.text}</div>
            </div>
          ))}
        </div>
        <div className="card card--soft" style={{padding: 18}}>
          <div className="eyebrow" style={{color: "var(--green)"}}>3 itens mais fortes</div>
          {fortes.map((f) => (
            <div key={f.n} style={{padding: "10px 0", borderBottom: "0.5px solid var(--hairline)", display: "flex", gap: 12, alignItems: "flex-start"}}>
              <div style={{fontFamily:"var(--font-display)", color: "var(--green)", fontSize: 22, lineHeight: 1, minWidth: 36}}>{f.t2b}</div>
              <div style={{fontSize: 12, lineHeight: 1.45}}>{f.text}</div>
            </div>
          ))}
        </div>
      </div>
    </ReportSection>
  );
}

function ItemBar({ n, text, value }) {
  const color = value >= 75 ? "green" : value >= 60 ? "amber" : "red";
  return (
    <div style={{display: "grid", gridTemplateColumns: "32px 1fr 220px 48px", gap: 14, padding: "10px 0", borderBottom: "0.5px solid var(--hairline)", alignItems: "center"}}>
      <div style={{fontSize: 11, color: "var(--ink-muted)", fontVariantNumeric: "tabular-nums"}}>{String(n).padStart(2,"0")}</div>
      <div style={{fontSize: 13, lineHeight: 1.4}}>{text}</div>
      <div className="report-bar-row__bar-wrap" style={{margin: 0}}>
        <div className={"report-bar-row__bar report-bar-row__bar--" + color} style={{"--w": value + "%"}}></div>
      </div>
      <div style={{fontFamily: "var(--font-display)", fontSize: 22, textAlign: "right", fontVariantNumeric: "tabular-nums"}}>{value}</div>
    </div>
  );
}

function DemoTable({ title, rows }) {
  return (
    <div style={{marginBottom: 28}}>
      <div className="eyebrow" style={{marginBottom: 10}}>{title}</div>
      <div style={{border: "0.5px solid var(--hairline)", borderRadius: "var(--r-md)", overflow: "hidden"}}>
        <table style={{width: "100%", borderCollapse: "collapse", fontSize: 13}}>
          <thead>
            <tr style={{background: "var(--paper-2)"}}>
              <th style={{textAlign:"left", padding: "10px 14px", fontWeight: 600, fontSize: 11, color: "var(--ink-dim)", letterSpacing: "0.08em", textTransform: "uppercase"}}>Segmento</th>
              <th style={{textAlign:"right", padding: "10px 14px", fontSize: 11, color: "var(--ink-dim)", letterSpacing: "0.08em", textTransform: "uppercase"}}>N</th>
              <th style={{textAlign:"right", padding: "10px 14px", fontSize: 11, color: "var(--ink-dim)", letterSpacing: "0.08em", textTransform: "uppercase"}}>Medidor</th>
              <th style={{textAlign:"right", padding: "10px 14px", fontSize: 11, color: "var(--ink-dim)", letterSpacing: "0.08em", textTransform: "uppercase"}}>Cultura</th>
              <th style={{textAlign:"right", padding: "10px 14px", fontSize: 11, color: "var(--ink-dim)", letterSpacing: "0.08em", textTransform: "uppercase"}}>Educação</th>
              <th style={{textAlign:"right", padding: "10px 14px", fontSize: 11, color: "var(--ink-dim)", letterSpacing: "0.08em", textTransform: "uppercase"}}>Feedback</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r, i) => (
              <tr key={i} style={{borderTop: "0.5px solid var(--hairline)", color: r.suppressed ? "var(--ink-muted)" : (r.hot ? "var(--red)" : "var(--ink)")}}>
                <td style={{padding: "10px 14px"}}>{r.label}</td>
                <td style={{padding: "10px 14px", textAlign: "right", fontVariantNumeric:"tabular-nums"}}>{r.n}</td>
                {r.suppressed ? (
                  <td colSpan="4" style={{padding: "10px 14px", textAlign: "right", fontStyle: "italic", color: "var(--ink-muted)", fontSize: 12}}>
                    suprimido · &lt; 5 respondentes
                  </td>
                ) : (
                  <>
                    <td style={{padding: "10px 14px", textAlign:"right", fontWeight: 600, fontVariantNumeric:"tabular-nums"}}>{r.med}</td>
                    <td style={{padding: "10px 14px", textAlign:"right", fontVariantNumeric:"tabular-nums"}}>{r.c}</td>
                    <td style={{padding: "10px 14px", textAlign:"right", fontVariantNumeric:"tabular-nums"}}>{r.e}</td>
                    <td style={{padding: "10px 14px", textAlign:"right", fontVariantNumeric:"tabular-nums"}}>{r.f}</td>
                  </>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function topGaps(colab, socio, kind, limit) {
  // mirror items 1..41
  const arr = [];
  for (let n = 1; n <= 41; n++) {
    const c = colab[n - 1];
    const s = socio[n - 1];
    const gap = s - c;
    arr.push({ n, colab: c, socio: s, gap });
  }
  if (kind === "ceg") return arr.filter(x => x.gap >= 15).sort((a,b) => b.gap - a.gap).slice(0, limit);
  if (kind === "sub") return arr.filter(x => x.gap <= -15).sort((a,b) => a.gap - b.gap).slice(0, limit);
  // alignment: small gap AND both relatively high
  return arr.filter(x => Math.abs(x.gap) <= 14)
            .sort((a,b) => (b.colab + b.socio) - (a.colab + a.socio))
            .slice(0, limit);
}

function GapBarRow({ n, text, colab, socio }) {
  const gap = socio - colab;
  let kind = "alinhado";
  if (gap >= 15) kind = "cegueira";
  else if (gap <= -15) kind = "subest";

  const kindLabel = kind === "cegueira" ? "Cegueira do dono" : kind === "subest" ? "Subestimação" : "Alinhamento";

  return (
    <div className="gap-row">
      <div className="gap-row__label">
        <span style={{color: "var(--ink-muted)", fontSize: 11, marginRight: 8, fontVariantNumeric:"tabular-nums"}}>{String(n).padStart(2,"0")}</span>
        {text}
        <span className={"gap-row__gap-chip gap-row__gap-chip--" + kind}>{(gap > 0 ? "+" : "") + gap + " pts · " + kindLabel}</span>
      </div>
      <div className="gap-row__bars">
        <div className="gap-row__bar">
          <span className="gap-row__who">Sócio</span>
          <div className="gap-row__track"><div className="gap-row__fill gap-row__fill--socio" style={{"--w": socio + "%"}}></div></div>
          <span className="gap-row__num">{socio}</span>
        </div>
        <div className="gap-row__bar">
          <span className="gap-row__who">Time</span>
          <div className="gap-row__track"><div className="gap-row__fill gap-row__fill--colab" style={{"--w": colab + "%"}}></div></div>
          <span className="gap-row__num">{colab}</span>
        </div>
      </div>
    </div>
  );
}

function GapSummaryStats({ colab, socio }) {
  let ceg = 0, ali = 0, sub = 0;
  for (let n = 1; n <= 41; n++) {
    const g = socio[n-1] - colab[n-1];
    if (g >= 15) ceg++;
    else if (g <= -15) sub++;
    else ali++;
  }
  return (
    <div className="stats-3">
      <div className="stat" style={{borderTopColor: "var(--red)"}}>
        <div className="stat__label" style={{color: "var(--red)"}}>Cegueira do dono</div>
        <div className="stat__num">{ceg}</div>
        <div className="stat__hint">de 41 itens espelho</div>
      </div>
      <div className="stat" style={{borderTopColor: "var(--green)"}}>
        <div className="stat__label" style={{color: "var(--green)"}}>Alinhamento</div>
        <div className="stat__num">{ali}</div>
        <div className="stat__hint">percepções congruentes</div>
      </div>
      <div className="stat" style={{borderTopColor: "var(--amber)"}}>
        <div className="stat__label" style={{color: "var(--amber)"}}>Subestimação</div>
        <div className="stat__num">{sub}</div>
        <div className="stat__hint">dono mais crítico que o time</div>
      </div>
    </div>
  );
}

function SubpilarCard({ label, score }) {
  const f = window.MEDIDOR_DATA.mock.faixa(score);
  const color = f.chip === "green" ? "var(--green)" : f.chip === "amber" ? "var(--amber)" : "var(--red)";
  return (
    <div className="card" style={{padding: 18, borderTop: "3px solid " + color}}>
      <div className="eyebrow">{label}</div>
      <div style={{fontFamily: "var(--font-display)", fontSize: 44, lineHeight: 1, marginTop: 6, color}}>{score}</div>
      <div style={{fontSize: 11, color: "var(--ink-dim)", marginTop: 4}}>{f.label}</div>
    </div>
  );
}

function PlanoCard({ num, titulo, porque, acoes, prazo }) {
  return (
    <div className="card" style={{padding: 24, marginBottom: 16, borderLeft: "3px solid var(--copper)"}}>
      <div style={{display: "flex", alignItems: "baseline", gap: 12, marginBottom: 10}}>
        <span style={{fontFamily: "var(--font-display)", color: "var(--copper)", fontSize: 22}}>{num}</span>
        <h3 className="serif" style={{margin: 0, fontSize: 24, letterSpacing: "-0.01em", flex: 1, lineHeight: 1.2}}>{titulo}</h3>
        <span className="tag tag--ghost" style={{whiteSpace:"nowrap"}}>{prazo}</span>
      </div>
      <p style={{margin: "0 0 14px", color: "var(--ink-2)", fontSize: 14, lineHeight: 1.5}}>{porque}</p>
      <ul style={{margin: 0, paddingLeft: 0, listStyle: "none"}}>
        {acoes.map((a, i) => (
          <li key={i} style={{display: "flex", gap: 10, alignItems: "flex-start", padding: "8px 0", borderTop: "0.5px solid var(--hairline)", fontSize: 14, lineHeight: 1.5}}>
            <span style={{color: "var(--copper)", fontWeight: 600, minWidth: 22}}>→</span>
            <span>{a}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

Object.assign(window, { ReportScreen });

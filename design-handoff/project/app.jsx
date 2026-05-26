// app.jsx — Top-level router and Tweaks panel

const { useState, useEffect } = React;

const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "formPattern": "block",
  "theme": "light",
  "showDemoNav": true,
  "showProgressMode": "pillars"
}/*EDITMODE-END*/;

function App() {
  const [t, setTweak] = useTweaks(TWEAK_DEFAULTS);
  // route: "cover" | "intro-colab" | "form-colab" | "form-socio" | "admin" | "report"
  const [route, setRoute] = useState("cover");

  // Persist navigation via hash for refresh-friendliness
  useEffect(() => {
    const fromHash = window.location.hash.replace("#", "");
    if (fromHash) setRoute(fromHash);
    const onHash = () => {
      const h = window.location.hash.replace("#", "");
      if (h) setRoute(h);
    };
    window.addEventListener("hashchange", onHash);
    return () => window.removeEventListener("hashchange", onHash);
  }, []);

  const navigate = (r) => {
    setRoute(r);
    // Use replaceState to avoid scroll jumps from hash changes
    if (window.location.hash !== "#" + r) {
      window.history.replaceState(null, "", "#" + r);
    }
    window.scrollTo(0, 0);
  };
  window.__navigate = navigate;

  // Apply theme class
  useEffect(() => {
    document.documentElement.classList.toggle("theme-dark", t.theme === "dark");
  }, [t.theme]);

  const RouteEl = (() => {
    switch (route) {
      case "form-colab":
        return <FormRunner version="colab" pattern={t.formPattern} persistKey="medidor-colab" onFinish={() => navigate("cover")} />;
      case "form-socio":
        return <FormRunner version="socio" pattern={t.formPattern} persistKey="medidor-socio" onFinish={() => navigate("cover")} />;
      case "admin":
        return <AdminScreen />;
      case "report":
        return <ReportScreen />;
      case "cover":
      default:
        return <CoverScreen onPick={(v) => navigate(v === "colab" ? "form-colab" : "form-socio")} />;
    }
  })();

  return (
    <>
      {RouteEl}

      {t.showDemoNav && (
        <DemoNav route={route} navigate={navigate} />
      )}

      <TweaksPanel title="Tweaks">
        <TweakSection label="Formulário" />
        <TweakRadio
          label="Padrão de apresentação"
          value={t.formPattern}
          options={[
            { value: "one", label: "1 / tela" },
            { value: "block", label: "Bloco" },
            { value: "pilar", label: "Pilar" },
          ]}
          onChange={(v) => setTweak("formPattern", v)}
        />
        <div style={{fontSize: 10.5, color: "rgba(0,0,0,.5)", lineHeight: 1.4, padding: "4px 12px 8px"}}>
          <strong>Bloco</strong>: 5–7 itens por tela (saudável, padrão).<br/>
          <strong>1/tela</strong>: estilo Typeform.<br/>
          <strong>Pilar</strong>: 1 tela longa por pilar.
        </div>

        <TweakSection label="Tema" />
        <TweakRadio
          label="Aparência"
          value={t.theme}
          options={[
            { value: "light", label: "Claro" },
            { value: "dark", label: "Escuro" },
          ]}
          onChange={(v) => setTweak("theme", v)}
        />

        <TweakSection label="Demo" />
        <TweakToggle label="Mostrar navegador de telas" value={t.showDemoNav}
                     onChange={(v) => setTweak("showDemoNav", v)} />
        <TweakButton onClick={() => {
          if (confirm("Apagar todas as respostas salvas em rascunho?")) {
            localStorage.removeItem("medidor-colab");
            localStorage.removeItem("medidor-socio");
            location.reload();
          }
        }}>Limpar rascunhos</TweakButton>
      </TweaksPanel>
    </>
  );
}

function DemoNav({ route, navigate }) {
  const [open, setOpen] = useState(true);
  const items = [
    { id: "cover", label: "1. Landing (pública)" },
    { id: "form-colab", label: "2. Form Colaborador" },
    { id: "form-socio", label: "3. Form Sócio" },
    { id: "admin", label: "4. Painel do gestor" },
    { id: "report", label: "5. Relatório" },
  ];
  return (
    <nav className="demo-nav" data-open={open} aria-label="Navegador da demo">
      <div className="demo-nav__head" onClick={() => setOpen(o => !o)}>
        <span className="demo-nav__title">Demo · {items.find(i => i.id === route)?.label.replace(/^\d+\.\s*/, "") || "navegar"}</span>
        <svg className="demo-nav__caret" viewBox="0 0 24 24" fill="none"><path d="M6 9l6 6 6-6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
      </div>
      <div className="demo-nav__list">
        {items.map(i => (
          <button key={i.id} aria-current={route === i.id} onClick={() => navigate(i.id)}>{i.label}</button>
        ))}
      </div>
    </nav>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);

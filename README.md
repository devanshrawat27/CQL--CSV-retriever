<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>CQL — CSV Query Language</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700;800&family=Space+Grotesk:wght@300;400;600;700&display=swap" rel="stylesheet"/>
<style>
  :root {
    --bg: #080c10;
    --bg2: #0d1117;
    --bg3: #111820;
    --border: #1e2d3d;
    --green: #00ff9d;
    --green-dim: #00c97a;
    --cyan: #00d4ff;
    --yellow: #ffd60a;
    --red: #ff4757;
    --text: #c9d1d9;
    --text-dim: #6e7f8d;
    --text-bright: #f0f6fc;
    --mono: 'JetBrains Mono', monospace;
    --sans: 'Space Grotesk', sans-serif;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--sans);
    line-height: 1.7;
    overflow-x: hidden;
  }

  /* Scrollbar */
  ::-webkit-scrollbar { width: 4px; }
  ::-webkit-scrollbar-track { background: var(--bg); }
  ::-webkit-scrollbar-thumb { background: var(--green); border-radius: 2px; }

  /* BG grid */
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
      linear-gradient(var(--border) 1px, transparent 1px),
      linear-gradient(90deg, var(--border) 1px, transparent 1px);
    background-size: 40px 40px;
    opacity: 0.3;
    pointer-events: none;
    z-index: 0;
  }

  .wrap { max-width: 920px; margin: 0 auto; padding: 0 24px; position: relative; z-index: 1; }

  /* ── HERO ── */
  .hero {
    padding: 80px 0 60px;
    text-align: center;
    position: relative;
  }

  .hero-prompt {
    display: inline-block;
    font-family: var(--mono);
    font-size: 13px;
    color: var(--green);
    background: rgba(0,255,157,0.07);
    border: 1px solid rgba(0,255,157,0.2);
    border-radius: 4px;
    padding: 6px 16px;
    margin-bottom: 32px;
    letter-spacing: 0.5px;
    animation: fadeDown 0.6s ease both;
  }
  .hero-prompt::before { content: '$ '; opacity: 0.5; }

  .hero h1 {
    font-family: var(--mono);
    font-size: clamp(48px, 8vw, 88px);
    font-weight: 800;
    line-height: 1;
    letter-spacing: -3px;
    color: var(--text-bright);
    animation: fadeDown 0.7s 0.1s ease both;
  }

  .hero h1 span {
    background: linear-gradient(135deg, var(--green), var(--cyan));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .hero-sub {
    font-family: var(--mono);
    font-size: 15px;
    color: var(--text-dim);
    margin-top: 20px;
    letter-spacing: 0.3px;
    animation: fadeDown 0.7s 0.2s ease both;
  }
  .hero-sub em { color: var(--cyan); font-style: normal; }

  .badges {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
    margin-top: 36px;
    animation: fadeDown 0.7s 0.3s ease both;
  }
  .badge {
    font-family: var(--mono);
    font-size: 11px;
    font-weight: 700;
    padding: 5px 14px;
    border-radius: 3px;
    letter-spacing: 0.8px;
    text-transform: uppercase;
  }
  .badge-green  { background: rgba(0,255,157,0.1); color: var(--green);  border: 1px solid rgba(0,255,157,0.3); }
  .badge-cyan   { background: rgba(0,212,255,0.1); color: var(--cyan);   border: 1px solid rgba(0,212,255,0.3); }
  .badge-yellow { background: rgba(255,214,10,0.1); color: var(--yellow); border: 1px solid rgba(255,214,10,0.3); }
  .badge-red    { background: rgba(255,71,87,0.1); color: var(--red);    border: 1px solid rgba(255,71,87,0.3); }

  .hero-divider {
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--green), transparent);
    margin-top: 60px;
    opacity: 0.4;
    animation: fadeDown 0.7s 0.4s ease both;
  }

  /* ── SECTIONS ── */
  section { padding: 64px 0; }

  .sec-label {
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--green);
    margin-bottom: 10px;
  }
  .sec-label::before { content: '// '; opacity: 0.5; }

  h2 {
    font-family: var(--sans);
    font-size: 28px;
    font-weight: 700;
    color: var(--text-bright);
    margin-bottom: 24px;
  }

  p { color: var(--text); margin-bottom: 14px; font-size: 15px; }

  /* ── PIPELINE ── */
  .pipeline {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 40px 32px;
    position: relative;
    overflow: hidden;
  }
  .pipeline::before {
    content: 'compiler.pipeline';
    position: absolute;
    top: 16px; right: 20px;
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text-dim);
    opacity: 0.5;
  }

  .pipe-flow {
    display: flex;
    flex-direction: column;
    gap: 0;
    align-items: center;
  }

  .pipe-stage {
    width: 100%;
    max-width: 600px;
    display: flex;
    align-items: stretch;
    gap: 0;
    opacity: 0;
    transform: translateX(-20px);
    transition: opacity 0.5s ease, transform 0.5s ease;
  }
  .pipe-stage.visible { opacity: 1; transform: translateX(0); }

  .pipe-num {
    font-family: var(--mono);
    font-size: 10px;
    font-weight: 700;
    color: var(--bg);
    background: var(--green);
    width: 28px;
    min-width: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 6px 0 0 6px;
    letter-spacing: 0.5px;
  }

  .pipe-box {
    flex: 1;
    background: var(--bg3);
    border: 1px solid var(--border);
    border-left: none;
    border-radius: 0 6px 6px 0;
    padding: 14px 20px;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .pipe-name {
    font-family: var(--mono);
    font-size: 13px;
    font-weight: 700;
    color: var(--text-bright);
    letter-spacing: 0.5px;
  }
  .pipe-name span {
    font-size: 10px;
    font-weight: 400;
    color: var(--green);
    margin-left: 8px;
    opacity: 0.8;
  }

  .pipe-desc {
    font-size: 12px;
    color: var(--text-dim);
    font-family: var(--mono);
  }

  .pipe-arrow {
    width: 28px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--green);
    font-size: 16px;
    opacity: 0.5;
    margin-left: calc(50% - 14px + 0px);
  }

  /* ── PROBLEM TABLE ── */
  .comp-table {
    width: 100%;
    border-collapse: collapse;
    font-family: var(--mono);
    font-size: 13px;
    margin-top: 8px;
  }
  .comp-table thead tr {
    background: rgba(0,255,157,0.08);
    border-bottom: 1px solid var(--green);
  }
  .comp-table th {
    padding: 12px 20px;
    text-align: left;
    color: var(--green);
    font-size: 11px;
    letter-spacing: 1px;
    text-transform: uppercase;
  }
  .comp-table td {
    padding: 12px 20px;
    border-bottom: 1px solid var(--border);
    color: var(--text);
  }
  .comp-table tr:hover td { background: rgba(255,255,255,0.02); }
  .comp-table td:first-child { color: var(--cyan); font-weight: 700; }
  .x { color: var(--red); } .check { color: var(--green); }

  /* ── APPROACH GRID ── */
  .approach-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 14px;
    margin-top: 8px;
  }
  .approach-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 20px;
    transition: border-color 0.2s, transform 0.2s;
  }
  .approach-card:hover {
    border-color: var(--green);
    transform: translateY(-3px);
  }
  .approach-card .icon {
    font-size: 22px;
    margin-bottom: 10px;
  }
  .approach-card h4 {
    font-family: var(--mono);
    font-size: 12px;
    font-weight: 700;
    color: var(--text-bright);
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .approach-card p {
    font-size: 12px;
    color: var(--text-dim);
    margin: 0;
  }

  /* ── MILESTONES ── */
  .milestones { display: flex; flex-direction: column; gap: 12px; }
  .milestone {
    display: flex;
    gap: 16px;
    align-items: flex-start;
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px 20px;
    transition: border-color 0.2s;
  }
  .milestone:hover { border-color: rgba(0,255,157,0.3); }
  .ms-num {
    font-family: var(--mono);
    font-size: 11px;
    font-weight: 800;
    background: var(--green);
    color: var(--bg);
    border-radius: 4px;
    padding: 3px 9px;
    white-space: nowrap;
    margin-top: 2px;
  }
  .ms-title {
    font-family: var(--mono);
    font-weight: 700;
    font-size: 14px;
    color: var(--text-bright);
  }
  .ms-desc { font-size: 13px; color: var(--text-dim); margin-top: 2px; }

  /* ── ASSUMPTIONS ── */
  .assume-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 10px;
    margin-top: 8px;
  }
  .assume-item {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-left: 3px solid var(--cyan);
    border-radius: 0 6px 6px 0;
    padding: 12px 16px;
    font-family: var(--mono);
    font-size: 12px;
    color: var(--text);
  }
  .assume-item::before { content: '→ '; color: var(--cyan); }

  /* ── TEAM ── */
  .team-header {
    text-align: center;
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 10px 10px 0 0;
    padding: 20px;
    border-bottom: 1px solid var(--green);
  }
  .team-name {
    font-family: var(--mono);
    font-size: 20px;
    font-weight: 800;
    color: var(--green);
    letter-spacing: 2px;
  }
  .team-label { font-size: 12px; color: var(--text-dim); margin-top: 4px; }

  .team-members {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    background: var(--bg3);
    border: 1px solid var(--border);
    border-top: none;
  }
  .member {
    padding: 22px 20px;
    border-right: 1px solid var(--border);
    transition: background 0.2s;
  }
  .member:last-child { border-right: none; }
  .member:hover { background: rgba(0,255,157,0.04); }
  .member-role {
    font-family: var(--mono);
    font-size: 10px;
    color: var(--green);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
  }
  .member-name {
    font-family: var(--sans);
    font-weight: 700;
    font-size: 15px;
    color: var(--text-bright);
  }

  .meta-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    background: var(--bg2);
    border: 1px solid var(--border);
    border-top: none;
    border-radius: 0 0 10px 10px;
  }
  .meta-item {
    padding: 16px 20px;
    border-right: 1px solid var(--border);
  }
  .meta-item:last-child { border-right: none; }
  .meta-key {
    font-family: var(--mono);
    font-size: 10px;
    color: var(--text-dim);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 4px;
  }
  .meta-val {
    font-family: var(--sans);
    font-weight: 600;
    font-size: 14px;
    color: var(--cyan);
  }

  /* ── REFS ── */
  .refs { display: flex; flex-direction: column; gap: 8px; }
  .ref {
    font-family: var(--mono);
    font-size: 12px;
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 12px 16px;
    display: flex;
    gap: 12px;
    align-items: center;
    text-decoration: none;
    color: var(--text);
    transition: border-color 0.2s, color 0.2s;
  }
  .ref:hover { border-color: var(--cyan); color: var(--cyan); }
  .ref-num { color: var(--green); font-weight: 800; min-width: 20px; }

  /* ── FOOTER ── */
  footer {
    border-top: 1px solid var(--border);
    padding: 32px 0;
    text-align: center;
    font-family: var(--mono);
    font-size: 12px;
    color: var(--text-dim);
  }
  footer span { color: var(--green); }

  /* ── ANIMATIONS ── */
  @keyframes fadeDown {
    from { opacity: 0; transform: translateY(-16px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  /* Glow pulse on title */
  @keyframes glow {
    0%, 100% { text-shadow: 0 0 20px rgba(0,255,157,0.3); }
    50%       { text-shadow: 0 0 40px rgba(0,255,157,0.6), 0 0 80px rgba(0,212,255,0.2); }
  }
  .hero h1 { animation: fadeDown 0.7s 0.1s ease both, glow 3s 1s ease-in-out infinite; }

  /* Typing cursor */
  .cursor {
    display: inline-block;
    width: 2px;
    height: 1em;
    background: var(--green);
    margin-left: 4px;
    vertical-align: middle;
    animation: blink 1s step-end infinite;
  }
  @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

  /* Section reveal */
  .reveal {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.6s ease, transform 0.6s ease;
  }
  .reveal.visible { opacity: 1; transform: translateY(0); }

  /* Horizontal divider */
  hr.fancy {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 0;
  }
</style>
</head>
<body>

<!-- HERO -->
<div class="wrap">
  <div class="hero">
    <div class="hero-prompt">cql --compile query.cql --target data.csv</div>
    <h1><span>CQL</span></h1>
    <div class="hero-sub">CSV Query Language &nbsp;·&nbsp; <em>Compiler Design Project</em><span class="cursor"></span></div>
    <div class="badges">
      <span class="badge badge-green">Python</span>
      <span class="badge badge-cyan">Compiler Design</span>
      <span class="badge badge-yellow">PBL 2024–25</span>
      <span class="badge badge-red">Syntax Syndicate</span>
    </div>
    <div class="hero-divider"></div>
  </div>
</div>

<hr class="fancy"/>

<!-- MOTIVATION -->
<div class="wrap">
  <section class="reveal">
    <div class="sec-label">motivation</div>
    <h2>Why does this exist?</h2>
    <p>CSV files store more data than people realize — sales records, logs, survey results, sensor readings. But querying them meaningfully is painful. You either write Python scripts that take longer than the query itself, or you import everything into a database just to run one <code style="color:var(--cyan);font-family:var(--mono)">SELECT</code>.</p>
    <p>CQL removes that friction. Write a query, point it at a file, get results. The compiler does the heavy lifting — tokenizing, parsing, validating, optimizing, and generating streaming Python code — all behind a clean SQL-like interface.</p>
    <p>It also happens to demonstrate every major phase of a compiler on a problem that's genuinely useful.</p>
  </section>
</div>

<hr class="fancy"/>

<!-- CURRENT TOOLS -->
<div class="wrap">
  <section class="reveal">
    <div class="sec-label">state of the art</div>
    <h2>What's out there — and what's missing</h2>
    <table class="comp-table">
      <thead>
        <tr>
          <th>Tool</th>
          <th>No Setup</th>
          <th>SQL Syntax</th>
          <th>Works on CSV</th>
          <th>Memory Efficient</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>pandas</td>
          <td><span class="x">✗</span></td>
          <td><span class="x">✗</span></td>
          <td><span class="check">✓</span></td>
          <td><span class="x">✗</span></td>
        </tr>
        <tr>
          <td>Excel</td>
          <td><span class="check">✓</span></td>
          <td><span class="x">✗</span></td>
          <td><span class="check">✓</span></td>
          <td><span class="x">✗</span></td>
        </tr>
        <tr>
          <td>SQLite</td>
          <td><span class="x">✗</span></td>
          <td><span class="check">✓</span></td>
          <td><span class="x">✗</span></td>
          <td><span class="check">✓</span></td>
        </tr>
        <tr>
          <td>awk</td>
          <td><span class="check">✓</span></td>
          <td><span class="x">✗</span></td>
          <td><span class="check">✓</span></td>
          <td><span class="check">✓</span></td>
        </tr>
        <tr style="background:rgba(0,255,157,0.05)">
          <td style="color:var(--green);font-weight:800">CQL ★</td>
          <td><span class="check">✓</span></td>
          <td><span class="check">✓</span></td>
          <td><span class="check">✓</span></td>
          <td><span class="check">✓</span></td>
        </tr>
      </tbody>
    </table>
  </section>
</div>

<hr class="fancy"/>

<!-- PIPELINE -->
<div class="wrap">
  <section class="reveal">
    <div class="sec-label">architecture</div>
    <h2>Compiler Pipeline</h2>
    <div class="pipeline">
      <div class="pipe-flow">

        <div class="pipe-stage" id="ps1">
          <div class="pipe-num">01</div>
          <div class="pipe-box">
            <div class="pipe-name">LEXER <span>→ token stream</span></div>
            <div class="pipe-desc">Scans raw query string · identifies keywords, identifiers, operators, literals</div>
          </div>
        </div>

        <div class="pipe-arrow">↓</div>

        <div class="pipe-stage" id="ps2">
          <div class="pipe-num">02</div>
          <div class="pipe-box">
            <div class="pipe-name">PARSER <span>→ abstract syntax tree</span></div>
            <div class="pipe-desc">Recursive descent · validates grammar · builds structured AST from token stream</div>
          </div>
        </div>

        <div class="pipe-arrow">↓</div>

        <div class="pipe-stage" id="ps3">
          <div class="pipe-num">03</div>
          <div class="pipe-box">
            <div class="pipe-name">SEMANTIC ANALYZER <span>→ validated AST</span></div>
            <div class="pipe-desc">Checks column names against CSV schema · type-checks comparisons · validates JOINs</div>
          </div>
        </div>

        <div class="pipe-arrow">↓</div>

        <div class="pipe-stage" id="ps4">
          <div class="pipe-num">04</div>
          <div class="pipe-box">
            <div class="pipe-name">OPTIMIZER <span>→ optimized AST</span></div>
            <div class="pipe-desc">Predicate pushdown — applies WHERE filters early · projection pruning — drops unused columns</div>
          </div>
        </div>

        <div class="pipe-arrow">↓</div>

        <div class="pipe-stage" id="ps5">
          <div class="pipe-num">05</div>
          <div class="pipe-box">
            <div class="pipe-name">CODE GENERATOR <span>→ executable output</span></div>
            <div class="pipe-desc">Emits clean Python code · streaming row-by-row CSV processing via built-in csv module</div>
          </div>
        </div>

      </div>
    </div>
  </section>
</div>

<hr class="fancy"/>

<!-- APPROACH -->
<div class="wrap">
  <section class="reveal">
    <div class="sec-label">technical approach</div>
    <h2>How it's built</h2>
    <div class="approach-grid">
      <div class="approach-card">
        <div class="icon">🔤</div>
        <h4>Hand-written Parser</h4>
        <p>No parser-generator libraries. Pure recursive descent, built from scratch.</p>
      </div>
      <div class="approach-card">
        <div class="icon">🌊</div>
        <h4>Streaming Output</h4>
        <p>Generated code processes CSV row-by-row — flat memory usage regardless of file size.</p>
      </div>
      <div class="approach-card">
        <div class="icon">⚡</div>
        <h4>Predicate Pushdown</h4>
        <p>Filters applied as early as possible in the pipeline to minimize wasted reads.</p>
      </div>
      <div class="approach-card">
        <div class="icon">🔗</div>
        <h4>JOIN Support</h4>
        <p>Equality-based JOINs across multiple CSV files in a single query.</p>
      </div>
      <div class="approach-card">
        <div class="icon">🔍</div>
        <h4>Type Inference</h4>
        <p>Automatically infers int, float, or string — no schema declaration needed.</p>
      </div>
      <div class="approach-card">
        <div class="icon">🐍</div>
        <h4>Zero Dependencies</h4>
        <p>Compiler and generated code use only Python's standard library.</p>
      </div>
    </div>
  </section>
</div>

<hr class="fancy"/>

<!-- MILESTONES -->
<div class="wrap">
  <section class="reveal">
    <div class="sec-label">project plan</div>
    <h2>Goals & Milestones</h2>
    <div class="milestones">
      <div class="milestone">
        <span class="ms-num">PHASE 1</span>
        <div>
          <div class="ms-title">Lexer + Parser</div>
          <div class="ms-desc">Define grammar, implement tokenizer, build recursive-descent parser, generate AST</div>
        </div>
      </div>
      <div class="milestone">
        <span class="ms-num">PHASE 2</span>
        <div>
          <div class="ms-title">Semantic Analyzer</div>
          <div class="ms-desc">Schema validation against actual CSV headers, type checking, error reporting</div>
        </div>
      </div>
      <div class="milestone">
        <span class="ms-num">PHASE 3</span>
        <div>
          <div class="ms-title">Query Optimizer</div>
          <div class="ms-desc">Predicate pushdown, projection pruning, JOIN reordering optimizations</div>
        </div>
      </div>
      <div class="milestone">
        <span class="ms-num">PHASE 4</span>
        <div>
          <div class="ms-title">Code Generation + Testing</div>
          <div class="ms-desc">Python codegen with streaming CSV processing, full test suite on sample datasets</div>
        </div>
      </div>
    </div>
  </section>
</div>

<hr class="fancy"/>

<!-- ASSUMPTIONS -->
<div class="wrap">
  <section class="reveal">
    <div class="sec-label">scope</div>
    <h2>Assumptions</h2>
    <div class="assume-list">
      <div class="assume-item">CSV files contain a header row</div>
      <div class="assume-item">Data types are inferred from values</div>
      <div class="assume-item">Files are well-structured and valid</div>
      <div class="assume-item">JOINs limited to equality conditions</div>
    </div>
  </section>
</div>

<hr class="fancy"/>

<!-- TEAM -->
<div class="wrap">
  <section class="reveal">
    <div class="sec-label">the team</div>
    <h2>Syntax Syndicate</h2>

    <div class="team-header">
      <div class="team-name">// SYNTAX SYNDICATE</div>
      <div class="team-label">Compiler Design · PBL 2024–25</div>
    </div>

    <div class="team-members">
      <div class="member">
        <div class="member-role">Team Lead</div>
        <div class="member-name">Lakshya Dhiman</div>
      </div>
      <div class="member">
        <div class="member-role">Member</div>
        <div class="member-name">Devansh Rawat</div>
      </div>
      <div class="member">
        <div class="member-role">Member</div>
        <div class="member-name">Vedant Devrani</div>
      </div>
    </div>

    <div class="meta-row">
      <div class="meta-item">
        <div class="meta-key">Mentor / Guide</div>
        <div class="meta-val">Ms. Preeti Badhani</div>
      </div>
      <div class="meta-item">
        <div class="meta-key">Evaluator</div>
        <div class="meta-val">Mr. Mukesh Kumar</div>
      </div>
    </div>
  </section>
</div>

<hr class="fancy"/>

<!-- REFERENCES -->
<div class="wrap">
  <section class="reveal">
    <div class="sec-label">references</div>
    <h2>Sources</h2>
    <div class="refs">
      <a class="ref" href="https://docs.python.org/3/library/csv.html" target="_blank">
        <span class="ref-num">01</span>
        Python Software Foundation — CSV Module Documentation
      </a>
      <a class="ref" href="https://docs.python.org/3/library/collections.html" target="_blank">
        <span class="ref-num">02</span>
        Python Software Foundation — Collections Module Documentation
      </a>
      <a class="ref" href="https://docs.python.org/3/library/dataclasses.html" target="_blank">
        <span class="ref-num">03</span>
        Python Software Foundation — Dataclasses Module Documentation
      </a>
    </div>
  </section>
</div>

<hr class="fancy"/>

<footer>
  <div class="wrap">
    <span>Syntax Syndicate</span> &nbsp;·&nbsp; CQL — CSV Query Language &nbsp;·&nbsp; Compiler Design PBL 2024–25
  </div>
</footer>

<script>
  // Intersection observer for scroll reveals
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        observer.unobserve(e.target);
      }
    });
  }, { threshold: 0.12 });

  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

  // Staggered pipeline animation
  const pipeObs = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
      document.querySelectorAll('.pipe-stage').forEach((el, i) => {
        setTimeout(() => el.classList.add('visible'), i * 150);
      });
      pipeObs.disconnect();
    }
  }, { threshold: 0.1 });

  const pipeline = document.querySelector('.pipeline');
  if (pipeline) pipeObs.observe(pipeline);
</script>
</body>
</html>

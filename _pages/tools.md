---
layout: single
title: "Tools"
permalink: /tools/
author_profile: true
---

Explore two open, source-linked research atlases for AI hardware—from processor architectures to computation inside and near memory.

<style>
.atlas-directory { margin: 1.6rem 0 2rem; }
.atlas-directory__grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:1rem; }
.atlas-directory__card { display:flex; flex-direction:column; min-width:0; min-height:350px; padding:1.6rem; border:1px solid #d7e2eb; border-radius:16px; background:linear-gradient(135deg,#f4f8fc 0%,#fff 75%); box-shadow:0 8px 24px rgba(32,55,83,.045); }
.atlas-directory__card--memory { background:linear-gradient(135deg,#f0f9f5 0%,#fff 75%); border-color:#cfe5db; }
.atlas-directory__eyebrow { color:#577b95; font-size:.72rem; letter-spacing:.11em; font-weight:750; text-transform:uppercase; margin:0 0 .8rem; }
.atlas-directory__card--memory .atlas-directory__eyebrow { color:#397d71; }
.atlas-directory__icon { display:inline-flex; align-items:center; justify-content:center; width:43px; height:43px; margin-bottom:1.1rem; border-radius:12px; background:#dceaf6; color:#315f85; font-size:1.4rem; font-weight:700; }
.atlas-directory__card--memory .atlas-directory__icon { background:#d8f2e8; color:#277968; }
.atlas-directory__card h2 { margin:0 0 .7rem; font-size:clamp(1.28rem,2vw,1.65rem); line-height:1.19; letter-spacing:-.02em; }
.atlas-directory__card p { margin:0 0 1rem; color:#526779; font-size:.89rem; line-height:1.65; }
.atlas-directory__footer { margin-top:auto; display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:.8rem; padding-top:1.1rem; border-top:1px solid #dce6ec; }
.atlas-directory__card--memory .atlas-directory__footer { border-color:#d6e9e1; }
.atlas-directory__open { display:inline-flex; align-items:center; gap:.5rem; padding:.62rem .9rem; color:white !important; border-radius:8px; background:#244f7d; text-decoration:none !important; font-size:.85rem; font-weight:700; }
.atlas-directory__card--memory .atlas-directory__open { background:#176b64; }
.atlas-directory__open:hover { filter:brightness(1.1); }
.atlas-directory__open:focus-visible, .atlas-directory__files a:focus-visible { outline:3px solid #77a9da; outline-offset:3px; }
.atlas-directory__files { font-size:.78rem; color:#697b89; white-space:nowrap; }
.atlas-directory__files a { color:#315f85; text-decoration:underline; text-underline-offset:3px; }
.atlas-directory__card--memory .atlas-directory__files a { color:#176b64; }
.atlas-directory__meta { padding:.85rem 0 0; font-size:.76rem; color:#61788b; }
.atlas-directory__note { margin:1.2rem 0 0; color:#738293; font-size:.78rem; line-height:1.55; }
@media(max-width:780px) { .atlas-directory__grid { grid-template-columns:1fr; } .atlas-directory__card { min-height:0; } }
@media(max-width:400px) { .atlas-directory__card { padding:1.2rem; } .atlas-directory__footer { align-items:flex-start; flex-direction:column; } }
</style>

<div class="atlas-directory">
  <div class="atlas-directory__grid">
    <section class="atlas-directory__card" aria-labelledby="accelerator-heading">
      <div class="atlas-directory__icon" aria-hidden="true">✦</div>
      <p class="atlas-directory__eyebrow">01 / Architecture landscape</p>
      <h2 id="accelerator-heading">AI Accelerator Architecture Atlas</h2>
      <p>Explore the design space of AI processors. Browse architecture families, compare compute and memory hierarchies, and navigate an interactive 3D taxonomy.</p>
      <div class="atlas-directory__meta">22 records · 7 subclasses · interactive design-space map</div>
      <div class="atlas-directory__footer">
        <a class="atlas-directory__open" href="{{ '/tools/accelerator-atlas/' | relative_url }}">Explore Accelerator Atlas &rarr;</a>
        <span class="atlas-directory__files">Data: <a href="{{ '/tools/accelerator-atlas/chips.json' | relative_url }}">JSON</a> · <a href="{{ '/tools/accelerator-atlas/chips.csv' | relative_url }}">CSV</a></span>
      </div>
    </section>
    <section class="atlas-directory__card atlas-directory__card--memory" aria-labelledby="memory-heading">
      <div class="atlas-directory__icon" aria-hidden="true">▦</div>
      <p class="atlas-directory__eyebrow">02 / Memory-centric silicon</p>
      <h2 id="memory-heading">Memory Compute Atlas</h2>
      <p>Discover compute-in-memory, DRAM PIM and near-memory hardware. Filter real products, compare specs, meet the companies, and explore focused technical essays.</p>
      <div class="atlas-directory__meta">30 product records · 21 companies · 6 research essays</div>
      <div class="atlas-directory__footer">
        <a class="atlas-directory__open" href="{{ '/tools/memory-compute-atlas/' | relative_url }}">Explore Memory Compute Atlas &rarr;</a>
        <span class="atlas-directory__files">Data: <a href="{{ '/tools/memory-compute-atlas/data.json' | relative_url }}">JSON</a> · <a href="{{ '/tools/memory-compute-atlas/products.csv' | relative_url }}">CSV</a></span>
      </div>
    </section>
  </div>
  <p class="atlas-directory__note">Both atlases are open, curated technical references rather than live vendor feeds or independently benchmarked performance rankings. Specifications link back to their sources.</p>
</div>

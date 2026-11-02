---
layout: single
title: "Chip Gallery"
permalink: /chip-gallery/
author_profile: true
---

A collection of physical-design layouts from my research in memory-centric AI accelerators.

<style>
.chip-gallery { margin: 1.6rem 0 2.4rem; }
.chip-gallery__grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1.25rem; align-items: stretch; }
.chip-gallery__card { display: flex; flex-direction: column; min-width: 0; overflow: hidden; border: 1px solid #d7e2eb; border-radius: 12px; background: #fff; box-shadow: 0 6px 20px rgba(32,55,83,.045); }
.chip-gallery__visual { display: flex; align-items: center; justify-content: center; min-height: 225px; aspect-ratio: 1.38; margin: 0; padding: .9rem; background: #f7f9fb; border-bottom: 1px solid #e1e8ed; }
.chip-gallery__visual img { display: block; width: 100%; max-height: 100%; height: 100%; object-fit: contain; }
.chip-gallery__body { display: flex; flex: 1; flex-direction: column; gap: .7rem; padding: 1.25rem 1.35rem 1.35rem; }
.chip-gallery__eyebrow { margin: 0; color: #577b95; font-size: .75rem; font-weight: 700; letter-spacing: .04em; }
.chip-gallery__card h2 { margin: 0; font-size: 1.35rem; line-height: 1.25; }
.chip-gallery__description { margin: 0; color: #4f6374; font-size: .89rem; line-height: 1.65; }
.chip-gallery__tags { display: flex; flex-wrap: wrap; gap: .4rem; margin-top: .1rem; }
.chip-gallery__tag { display: inline-block; padding: .27rem .55rem; border-radius: 6px; background: #eef3f7; color: #445c71; font-size: .73rem; line-height: 1.35; }
.chip-gallery__links { display: flex; flex-wrap: wrap; align-items: center; gap: 1rem; margin-top: auto; padding-top: .9rem; border-top: 1px solid #e3e9ee; font-size: .86rem; font-weight: 650; }
.chip-gallery__links a { color: #245b89; text-underline-offset: 3px; }
.chip-gallery__links a:focus-visible, .chip-gallery__visual:focus-visible { outline: 3px solid #77a9da; outline-offset: 3px; }
.chip-gallery__note { margin: 1.3rem 0 0; color: #65788a; font-size: .8rem; line-height: 1.6; }
@media (max-width: 760px) { .chip-gallery__grid { grid-template-columns: 1fr; } .chip-gallery__visual { aspect-ratio: 1.55; min-height: 190px; } }
@media (max-width: 420px) { .chip-gallery__body { padding: 1rem; } .chip-gallery__visual { padding: .5rem; } }
</style>

<div class="chip-gallery">
  <div class="chip-gallery__grid">
    <article class="chip-gallery__card" aria-labelledby="chip-gallery-leap">
      <a class="chip-gallery__visual" href="{{ '/images/chip-gallery/leap-layout.avif' | relative_url }}" target="_blank" rel="noopener" aria-label="Open LEAP physical layout in a new tab">
        <img src="{{ '/images/chip-gallery/leap-layout.avif' | relative_url }}" alt="LEAP physical design: 2 by 2 PIM-NoC macro layout with PIM processing elements, scratchpads, router strips, and area breakdown charts" loading="lazy" decoding="async" width="480" height="270">
      </a>
      <div class="chip-gallery__body">
        <p class="chip-gallery__eyebrow">ICCAD 2025 · PIM-NoC architecture</p>
        <h2 id="chip-gallery-leap">LEAP</h2>
        <p class="chip-gallery__description">A scalable processing-in-memory network-on-chip accelerator for LLM inference. The layout illustrates a 2 × 2 macro array with PIM processing elements, scratchpads, and integrated routers, accompanied by area breakdowns.</p>
        <div class="chip-gallery__tags" aria-label="Design features">
          <span class="chip-gallery__tag">PIM</span>
          <span class="chip-gallery__tag">NoC</span>
          <span class="chip-gallery__tag">Physical layout</span>
        </div>
        <div class="chip-gallery__links">
          <a href="{{ '/images/chip-gallery/leap-layout.avif' | relative_url }}" target="_blank" rel="noopener">View layout ↗</a>
          <a href="https://ieeexplore.ieee.org/document/11240722" target="_blank" rel="noopener noreferrer">Paper ↗</a>
        </div>
      </div>
    </article>

    <article class="chip-gallery__card" aria-labelledby="chip-gallery-omniacc">
      <a class="chip-gallery__visual" href="{{ '/images/chip-gallery/omniacc-layout.avif' | relative_url }}" target="_blank" rel="noopener" aria-label="Open OmniAcc physical layout in a new tab">
        <img src="{{ '/images/chip-gallery/omniacc-layout.avif' | relative_url }}" alt="OmniAcc physical design: heterogeneous layout with IMC tiles, scratchpads, near-memory compute and router strips, and nonlinear processing columns" loading="lazy" decoding="async" width="480" height="343">
      </a>
      <div class="chip-gallery__body">
        <p class="chip-gallery__eyebrow">ICCAD 2026 · Heterogeneous memory-centric AI</p>
        <h2 id="chip-gallery-omniacc">OmniAcc</h2>
        <p class="chip-gallery__description">A heterogeneous LLM accelerator integrating in-memory computing, near-memory computing and reconfigurable nonlinear processing. The layout highlights IMC tiles, local scratchpads, router regions, and dedicated nonlinear-processing columns.</p>
        <div class="chip-gallery__tags" aria-label="Design features">
          <span class="chip-gallery__tag">IMC + NMC</span>
          <span class="chip-gallery__tag">Nonlinear units</span>
          <span class="chip-gallery__tag">Physical layout</span>
        </div>
        <div class="chip-gallery__links">
          <a href="{{ '/images/chip-gallery/omniacc-layout.avif' | relative_url }}" target="_blank" rel="noopener">View layout ↗</a>
          <a href="{{ '/publications/' | relative_url }}">Publication details ↗</a>
        </div>
      </div>
    </article>
  </div>
</div>

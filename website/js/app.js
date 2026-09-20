// Catching Greenwashing from Space — Master Frontend Architecture & Logic

let companies = [];
let mills = [];
let claims = [];
let summary = {};
let map = null;
let markersLayer = null;
let bufferRingsLayer = null;
let currentBasemap = null;
let companyRadarChart = null;
let matrixChart = null;
let compareRadarChart = null;
let bufferData = null;

// Weight Simulator state
let weights = {
  forest_loss: 0.35,
  specificity: 0.35,
  sentiment: 0.15,
  spatial_match: 0.15
};

// Table Sort state
let sortColumn = "rank";
let sortAsc = true;

// Gallery state
let currentGalleryTab = "all";
let galleryDisplayLimit = 24;
let activeGalleryList = [];
let currentLightboxIndex = 0;

// Featured case study mill IDs
const FEATURED_MILL_IDS = [
  "klk_001",        // Kekayaan (2,490 ha)
  "astraagro_017",  // Sari Aditya Loka 1 (5,403 ha)
  "gar_001",        // Naga Sakti (3,421 ha)
  "ioi_001",        // Pamol Sabah (4,959 ha/mill avg)
  "wilmar_001",     // Sabahmas (6,675 ha)
  "sdguthrie_001",  // Giram
  "genting_007",    // Genting Tanjung (8,721 ha)
];

document.addEventListener("DOMContentLoaded", async () => {
  await loadData();
  recalculateDynamicScores();
  renderScoreboard();
  renderDecisionMatrix();
  initMap();
  populateCompanyFilters();
  populateCompareSelects();
  populateTopicFilter();
  renderGallery();
  renderClaims();
  renderBufferTable();
  setupEventListeners();
});

async function loadData() {
  try {
    const [compRes, millRes, claimRes, sumRes, bufRes] = await Promise.all([
      fetch("data/companies.json"),
      fetch("data/mills.json"),
      fetch("data/claims.json"),
      fetch("data/summary.json"),
      fetch("data/buffer_sensitivity.json")
    ]);
    companies = await compRes.json();
    mills = await millRes.json();
    claims = await claimRes.json();
    summary = await sumRes.json();
    if (bufRes && bufRes.ok) {
      bufferData = await bufRes.json();
    }

    companies.forEach(c => {
      c.dynamic_score = c.mismatch_score;
      c.dynamic_rank = c.rank;
    });
  } catch (err) {
    console.error("Error loading JSON data:", err);
  }
}

// 1. SCOREBOARD & SORTING
function sortTable(col) {
  if (sortColumn === col) {
    sortAsc = !sortAsc;
  } else {
    sortColumn = col;
    sortAsc = true;
  }
  renderScoreboard();
}

function renderScoreboard() {
  const tbody = document.getElementById("scoreboard-body");
  if (!tbody) return;
  tbody.innerHTML = "";

  const sorted = [...companies].sort((a, b) => {
    let valA, valB;
    if (sortColumn === "rank") {
      valA = a.dynamic_rank;
      valB = b.dynamic_rank;
    } else if (sortColumn === "mismatch_score") {
      valA = a.dynamic_score;
      valB = b.dynamic_score;
    } else if (colSubscore(sortColumn)) {
      valA = a.subscores[sortColumn];
      valB = b.subscores[sortColumn];
    } else {
      valA = a[sortColumn];
      valB = b[sortColumn];
    }
    if (typeof valA === "string") {
      return sortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
    }
    return sortAsc ? valA - valB : valB - valA;
  });

  sorted.forEach((c) => {
    const tr = document.createElement("tr");
    tr.onclick = () => showCompanyModal(c.company);

    const rankClass = c.dynamic_rank === 1 ? "top" : (c.dynamic_rank === 11 ? "low" : "");
    const scoreColor = c.dynamic_score >= 60 ? "#ef4444" : (c.dynamic_score >= 40 ? "#f59e0b" : "#22c55e");

    tr.innerHTML = `
      <td><span class="rank-badge ${rankClass}">${c.dynamic_rank}</span></td>
      <td class="company-cell">${c.name}</td>
      <td class="score-cell" style="color:${scoreColor}">${c.dynamic_score.toFixed(1)}</td>
      <td class="meter-cell">
        <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:2px;">
          <span>${c.subscores.forest_loss.toFixed(1)}</span>
        </div>
        <div class="meter-bar"><div class="meter-fill red" style="width:${c.subscores.forest_loss}%"></div></div>
      </td>
      <td class="meter-cell">
        <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:2px;">
          <span>${c.subscores.specificity.toFixed(1)}</span>
        </div>
        <div class="meter-bar"><div class="meter-fill" style="width:${c.subscores.specificity}%"></div></div>
      </td>
      <td class="meter-cell">
        <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:2px;">
          <span>${c.subscores.sentiment.toFixed(1)}</span>
        </div>
        <div class="meter-bar"><div class="meter-fill" style="width:${c.subscores.sentiment}%"></div></div>
      </td>
      <td class="meter-cell">
        <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:2px;">
          <span>${c.subscores.spatial_match.toFixed(1)}</span>
        </div>
        <div class="meter-bar"><div class="meter-fill" style="width:${c.subscores.spatial_match}%"></div></div>
      </td>
      <td style="font-family:var(--font-mono);">${Math.round(c.loss_post2020_ha).toLocaleString()} ha</td>
      <td style="font-family:var(--font-mono);">${c.n_mills}</td>
    `;
    tbody.appendChild(tr);
  });
}

function colSubscore(col) {
  return ["forest_loss", "specificity", "sentiment", "spatial_match"].includes(col);
}

// 2. DECISION MATRIX 2D SCATTER PLOT
function renderDecisionMatrix() {
  const ctx = document.getElementById("matrixScatterCanvas");
  if (!ctx || !companies.length) return;

  const bubbleData = companies.map(c => ({
    x: c.subscores.specificity,
    y: c.subscores.forest_loss,
    r: Math.max(6, Math.min(22, Math.sqrt(c.loss_post2020_ha) / 22)),
    company: c.company,
    name: c.name,
    score: c.dynamic_score,
    loss: c.loss_post2020_ha,
    rank: c.dynamic_rank
  }));

  if (matrixChart) matrixChart.destroy();

  matrixChart = new Chart(ctx, {
    type: "bubble",
    data: {
      datasets: [{
        label: "Palm Oil Corporates",
        data: bubbleData,
        backgroundColor: bubbleData.map(d => 
          d.score >= 60 ? "rgba(239, 68, 68, 0.75)" : 
          (d.score >= 40 ? "rgba(245, 158, 11, 0.75)" : "rgba(34, 197, 94, 0.75)")
        ),
        borderColor: bubbleData.map(d => 
          d.score >= 60 ? "#ef4444" : 
          (d.score >= 40 ? "#f59e0b" : "#22c55e")
        ),
        borderWidth: 1.5,
        hoverBorderWidth: 3
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      onClick: (e, items) => {
        if (items.length > 0) {
          const idx = items[0].index;
          showCompanyModal(bubbleData[idx].company);
        }
      },
      scales: {
        x: {
          min: -5,
          max: 105,
          title: {
            display: true,
            text: "Claim Specificity Score (ClimateBERT) →",
            color: "#bcd4c1",
            font: { family: "JetBrains Mono", size: 11, weight: 600 }
          },
          grid: { color: "rgba(30, 56, 35, 0.6)" },
          ticks: { color: "#799d7f" }
        },
        y: {
          min: -5,
          max: 105,
          title: {
            display: true,
            text: "Forest Loss Intensity Score (Hansen GFC) →",
            color: "#bcd4c1",
            font: { family: "JetBrains Mono", size: 11, weight: 600 }
          },
          grid: { color: "rgba(30, 56, 35, 0.6)" },
          ticks: { color: "#799d7f" }
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "rgba(11, 21, 13, 0.96)",
          titleFont: { family: "Inter", size: 13, weight: 700 },
          bodyFont: { family: "JetBrains Mono", size: 11 },
          borderColor: "#2d5234",
          borderWidth: 1,
          padding: 10,
          callbacks: {
            title: (items) => {
              const raw = items[0].raw;
              return `#${raw.rank} ${raw.name}`;
            },
            label: (item) => {
              const raw = item.raw;
              return [
                `Mismatch Score: ${raw.score.toFixed(1)} / 100`,
                `Forest Loss: ${Math.round(raw.loss).toLocaleString()} ha`,
                `Specificity: ${raw.x.toFixed(1)} | Loss Score: ${raw.y.toFixed(1)}`,
                `(Click point to inspect company)`
              ];
            }
          }
        }
      }
    }
  });
}

// 3. LEAFLET MAP & BASEMAP SWITCHER
function initMap() {
  const mapElem = document.getElementById("map");
  if (!mapElem) return;

  map = L.map("map", {
    center: [0.5, 114.0],
    zoom: 5,
    minZoom: 2,
    maxZoom: 16
  });

  setBasemap("sat");
  markersLayer = L.layerGroup().addTo(map);
  bufferRingsLayer = L.layerGroup().addTo(map);
  updateMapMarkers();
  setTimeout(() => { if (map) map.invalidateSize(); }, 250);
}

function setBasemap(type) {
  if (currentBasemap) map.removeLayer(currentBasemap);

  const satBtn = document.getElementById("basemap-sat-btn");
  const darkBtn = document.getElementById("basemap-dark-btn");

  if (type === "sat") {
    currentBasemap = L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", {
      attribution: "Tiles &copy; Esri",
      maxZoom: 18
    });
    if (satBtn && darkBtn) { satBtn.classList.add("active"); darkBtn.classList.remove("active"); }
  } else {
    currentBasemap = L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
      attribution: "&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> &copy; <a href='https://carto.com/'>CARTO</a>",
      subdomains: "abcd",
      maxZoom: 19
    });
    if (satBtn && darkBtn) { darkBtn.classList.add("active"); satBtn.classList.remove("active"); }
  }

  currentBasemap.addTo(map);
}

function resetMapView() {
  const compSelect = document.getElementById("company-filter");
  const sevSelect = document.getElementById("severity-filter");
  if (compSelect) compSelect.value = "all";
  if (sevSelect) sevSelect.value = "0";
  clearBufferRings();
  updateMapMarkers();
  map.flyTo([0.5, 114.0], 5, { duration: 1.2 });
}

function zoomToRegion(reg) {
  if (!map) return;
  if (reg === "indonesia") {
    map.flyTo([-0.7893, 113.9213], 5, { duration: 1.4 });
  } else if (reg === "malaysia") {
    map.flyTo([4.2105, 108.9758], 6, { duration: 1.4 });
  } else if (reg === "africa") {
    map.flyTo([6.5, -4.5], 6, { duration: 1.8 });
  } else {
    map.flyTo([0.5, 114.0], 5, { duration: 1.4 });
  }
}

function getMarkerColor(lossHa) {
  if (lossHa > 5000) return "#ef4444"; // extreme
  if (lossHa > 3000) return "#f97316"; // severe
  if (lossHa > 1500) return "#f59e0b"; // moderate
  return "#22c55e";                    // low
}

function updateMapMarkers() {
  if (!markersLayer) return;
  markersLayer.clearLayers();

  const companyFilter = document.getElementById("company-filter")?.value || "all";
  const severityFilter = parseFloat(document.getElementById("severity-filter")?.value || "0");

  const filtered = mills.filter((m) => {
    const matchCompany = (companyFilter === "all" || m.company.toLowerCase() === companyFilter.toLowerCase());
    const matchSeverity = m.loss_post2020_ha >= severityFilter;
    return matchCompany && matchSeverity;
  });

  const counter = document.getElementById("map-counter");
  if (counter) counter.innerText = `Showing ${filtered.length} of 290 mills`;

  filtered.forEach((m) => {
    const color = getMarkerColor(m.loss_post2020_ha);
    const radius = Math.max(5, Math.min(14, Math.sqrt(m.loss_post2020_ha) / 5));

    const circle = L.circleMarker([m.latitude, m.longitude], {
      radius: radius,
      fillColor: color,
      color: "#ffffff",
      weight: 1.2,
      opacity: 0.9,
      fillOpacity: 0.75
    });

    const popupContent = `
      <div style="font-family:sans-serif; font-size:12px; min-width:210px; color:#111;">
        <strong style="font-size:14px; display:block; margin-bottom:4px;">${m.mill_name}</strong>
        <div><strong>Company:</strong> ${m.company.toUpperCase()}</div>
        <div><strong>Country:</strong> ${m.country}</div>
        <div><strong>Post-2020 Loss:</strong> <span style="color:#d9534f; font-weight:700;">${Math.round(m.loss_post2020_ha).toLocaleString()} ha</span></div>
        <div><strong>Forest 2000:</strong> ${Math.round(m.forest_2000_ha).toLocaleString()} ha</div>
        <div style="margin-top:8px; display:flex; flex-direction:column; gap:4px;">
          <button onclick="openLightbox('${m.map_image}', '${m.company.toUpperCase()} - ${m.mill_name.replace(/'/g, "\\'")} (${m.country})')"
                  style="background:#15803d; color:white; border:none; padding:5px 8px; border-radius:4px; cursor:pointer; font-size:11px; width:100%; font-weight:600;">
            🔎 View 300 DPI Satellite Map
          </button>
          <button onclick="drawConcentricRings(${m.latitude}, ${m.longitude}, '${m.mill_name.replace(/'/g, "\\'")}')"
                  style="background:#0284c7; color:white; border:none; padding:5px 8px; border-radius:4px; cursor:pointer; font-size:11px; width:100%; font-weight:600;">
            📐 Draw 5–30km Buffer Rings on Satellite
          </button>
        </div>
      </div>
    `;

    circle.bindPopup(popupContent);
    markersLayer.addLayer(circle);
  });

  if (companyFilter !== "all" && filtered.length > 0) {
    const bounds = L.latLngBounds(filtered.map(m => [m.latitude, m.longitude]));
    map.fitBounds(bounds, { padding: [40, 40] });
  }
}

// Draw 5 concentric buffer rings (5, 10, 15, 20, 30 km) around a mill
function drawConcentricRings(lat, lon, millName) {
  if (!map || !bufferRingsLayer) return;
  bufferRingsLayer.clearLayers();

  const rings = [
    { km: 5, color: "#06b6d4", dash: "4, 6", weight: 1.5, fillOp: 0.05, label: "5 km Buffer (79 km²)" },
    { km: 10, color: "#22c55e", dash: "", weight: 2.5, fillOp: 0.08, label: "10 km Buffer (314 km² - Canonical)" },
    { km: 15, color: "#f59e0b", dash: "4, 6", weight: 1.5, fillOp: 0.04, label: "15 km Buffer (707 km²)" },
    { km: 20, color: "#f97316", dash: "4, 6", weight: 1.5, fillOp: 0.03, label: "20 km Buffer (1,257 km²)" },
    { km: 30, color: "#ef4444", dash: "6, 8", weight: 1.5, fillOp: 0.02, label: "30 km Buffer (2,827 km² Outer)" }
  ];

  let outerCircle = null;
  rings.forEach(r => {
    const c = L.circle([lat, lon], {
      radius: r.km * 1000,
      color: r.color,
      dashArray: r.dash || null,
      weight: r.weight,
      fillColor: r.color,
      fillOpacity: r.fillOp
    });
    c.bindTooltip(`<b>${r.label}</b><br>${millName}`, { permanent: false, direction: "top" });
    bufferRingsLayer.addLayer(c);
    if (r.km === 30) outerCircle = c;
  });

  const centerDot = L.circleMarker([lat, lon], {
    radius: 6,
    fillColor: "#ffffff",
    color: "#15803d",
    weight: 2,
    fillOpacity: 1
  });
  centerDot.bindTooltip(`<b>${millName} (Center)</b>`, { permanent: true, direction: "bottom" });
  bufferRingsLayer.addLayer(centerDot);

  if (outerCircle) {
    map.fitBounds(outerCircle.getBounds(), { padding: [30, 30] });
  }

  const clearBtn = document.getElementById("clear-rings-btn");
  if (clearBtn) clearBtn.style.display = "inline-block";
}

function clearBufferRings() {
  if (bufferRingsLayer) bufferRingsLayer.clearLayers();
  const clearBtn = document.getElementById("clear-rings-btn");
  if (clearBtn) clearBtn.style.display = "none";
}

// 4. GALLERY & LIGHTBOX WITH ARROWS
function setGalleryTab(tab) {
  currentGalleryTab = tab;
  galleryDisplayLimit = 24;

  ["tab-all-mills", "tab-featured", "tab-severe"].forEach(id => {
    document.getElementById(id)?.classList.remove("active");
  });

  if (tab === "all") document.getElementById("tab-all-mills")?.classList.add("active");
  if (tab === "featured") document.getElementById("tab-featured")?.classList.add("active");
  if (tab === "severe") document.getElementById("tab-severe")?.classList.add("active");

  renderGallery();
}

function renderGallery() {
  const container = document.getElementById("gallery-grid");
  if (!container) return;
  container.innerHTML = "";

  const compFilter = document.getElementById("gallery-company-filter")?.value || "all";
  const searchFilter = document.getElementById("gallery-search")?.value.toLowerCase().trim() || "";

  let list = [...mills];

  if (currentGalleryTab === "featured") {
    list = list.filter(m => FEATURED_MILL_IDS.includes(m.id));
  } else if (currentGalleryTab === "severe") {
    list = list.filter(m => m.loss_post2020_ha >= 3000);
  }

  list = list.filter((m) => {
    const matchComp = (compFilter === "all" || m.company.toLowerCase() === compFilter.toLowerCase());
    const matchSearch = m.mill_name.toLowerCase().includes(searchFilter);
    return matchComp && matchSearch;
  });

  activeGalleryList = list;

  const counter = document.getElementById("gallery-counter");
  const loadMoreBtn = document.getElementById("load-more-btn");
  const displayList = list.slice(0, galleryDisplayLimit);

  if (counter) {
    counter.innerText = `Showing ${displayList.length} of ${list.length} mills`;
  }

  if (loadMoreBtn) {
    loadMoreBtn.style.display = displayList.length >= list.length ? "none" : "inline-block";
    loadMoreBtn.innerText = `Load More Maps (${Math.min(24, list.length - displayList.length)} more)`;
  }

  displayList.forEach((m, idx) => {
    const card = document.createElement("div");
    card.className = "map-card";
    card.onclick = () => openLightboxByIndex(idx);

    const isHigh = m.loss_post2020_ha > 3000;

    card.innerHTML = `
      <img class="map-card-thumb" src="${m.map_image}" alt="${m.mill_name}" loading="lazy"
           onerror="this.style.display='none'">
      <div class="map-card-body">
        <div class="map-card-title">${m.mill_name}</div>
        <div class="map-card-meta">
          <span>${m.company.toUpperCase()} • ${m.country}</span>
          <span class="loss-pill ${isHigh ? 'high' : ''}">${Math.round(m.loss_post2020_ha).toLocaleString()} ha</span>
        </div>
      </div>
    `;
    container.appendChild(card);
  });
}

function loadMoreGallery() {
  galleryDisplayLimit += 24;
  renderGallery();
}

function openLightboxByIndex(idx) {
  if (idx < 0 || idx >= activeGalleryList.length) return;
  currentLightboxIndex = idx;
  const m = activeGalleryList[idx];
  openLightbox(m.map_image, `${m.company.toUpperCase()} - ${m.mill_name} (${m.country}) • Post-2020 Loss: ${Math.round(m.loss_post2020_ha).toLocaleString()} ha`);
}

function navigateLightbox(dir) {
  const newIdx = currentLightboxIndex + dir;
  if (newIdx >= 0 && newIdx < activeGalleryList.length) {
    openLightboxByIndex(newIdx);
  }
}

function openLightbox(imgSrc, caption) {
  const lb = document.getElementById("lightbox");
  const img = document.getElementById("lightbox-img");
  const cap = document.getElementById("lightbox-caption");
  if (!lb || !img) return;

  img.src = imgSrc;
  if (cap) cap.innerText = caption || "";
  lb.classList.add("active");
}

function closeLightbox(e) {
  if (e && e.target !== e.currentTarget && !e.target.classList.contains("close-btn")) return;
  const lb = document.getElementById("lightbox");
  if (lb) lb.classList.remove("active");
}

// 5. CLAIMS EXPLORER
function populateTopicFilter() {
  const sel = document.getElementById("claims-topic-filter");
  if (!sel || !claims.length) return;

  const topics = [...new Set(claims.map(c => c.esg_category).filter(Boolean))].sort();
  sel.innerHTML = '<option value="all">All ESG Categories</option>';
  topics.forEach(t => {
    const opt = document.createElement("option");
    opt.value = t;
    opt.innerText = t;
    sel.appendChild(opt);
  });
}

function renderClaims() {
  const container = document.getElementById("claims-grid");
  if (!container) return;
  container.innerHTML = "";

  const compFilter = document.getElementById("claims-company-filter")?.value || "all";
  const strengthFilter = document.getElementById("claims-strength-filter")?.value || "all";
  const topicFilter = document.getElementById("claims-topic-filter")?.value || "all";
  const searchFilter = document.getElementById("claims-search")?.value.toLowerCase().trim() || "";

  const filtered = claims.filter((c) => {
    const matchComp = (compFilter === "all" || c.company.toLowerCase() === compFilter.toLowerCase());
    const matchStrength = (strengthFilter === "all" || c.strength.toLowerCase() === strengthFilter.toLowerCase());
    const matchTopic = (topicFilter === "all" || c.esg_category === topicFilter);
    const matchSearch = !searchFilter || c.text.toLowerCase().includes(searchFilter);
    return matchComp && matchStrength && matchTopic && matchSearch;
  });

  const counter = document.getElementById("claims-counter");
  if (counter) counter.innerText = `Showing ${filtered.length} of ${claims.length} claims`;

  filtered.slice(0, 60).forEach((c) => {
    const card = document.createElement("div");
    card.className = "claim-card";

    let textHtml = c.text;
    if (searchFilter) {
      const regex = new RegExp(`(${searchFilter})`, "gi");
      textHtml = textHtml.replace(regex, '<span class="highlight">$1</span>');
    }

    const specBadgeColor = c.specificity_score > 0.6 ? "green" : (c.specificity_score > 0.3 ? "blue" : "amber");
    const sentBadgeColor = c.sentiment_score > 0.7 ? "green" : "blue";

    card.innerHTML = `
      <div class="claim-header">
        <strong style="color:var(--text); font-size:13px;">${c.company.toUpperCase()}</strong>
        <span class="badge ${c.strength === 'hard' ? 'green' : 'amber'}">${c.strength.toUpperCase()} COMMITMENT</span>
      </div>
      <p class="claim-text">"${textHtml}"</p>
      <div class="claim-footer">
        <span class="badge ${specBadgeColor}">Specificity: ${c.specificity_score.toFixed(2)}</span>
        <span class="badge ${sentBadgeColor}">Sentiment: ${c.sentiment_score.toFixed(2)}</span>
        <span class="badge purple">${c.esg_category}</span>
        ${c.is_deforestation ? '<span class="badge green">Zero-Deforestation</span>' : ''}
        ${c.is_ndpe ? '<span class="badge blue">NDPE</span>' : ''}
        ${c.has_deadline ? '<span class="badge amber">Target Date Cited</span>' : ''}
      </div>
    `;
    container.appendChild(card);
  });
}

function resetClaimsFilters() {
  const comp = document.getElementById("claims-company-filter");
  const str = document.getElementById("claims-strength-filter");
  const top = document.getElementById("claims-topic-filter");
  const src = document.getElementById("claims-search");
  if (comp) comp.value = "all";
  if (str) str.value = "all";
  if (top) top.value = "all";
  if (src) src.value = "";
  renderClaims();
}

// 6. INTERACTIVE WEIGHT SIMULATOR
function updateWeightsFromSliders() {
  const wLoss = parseFloat(document.getElementById("slider-w-loss")?.value || "0.35");
  const wSpec = parseFloat(document.getElementById("slider-w-spec")?.value || "0.35");
  const wSent = parseFloat(document.getElementById("slider-w-sent")?.value || "0.15");
  const wSpat = parseFloat(document.getElementById("slider-w-spat")?.value || "0.15");

  weights.forest_loss = wLoss;
  weights.specificity = wSpec;
  weights.sentiment = wSent;
  weights.spatial_match = wSpat;

  const sum = wLoss + wSpec + wSent + wSpat;
  const effectiveSum = sum > 0 ? sum : 1.0;

  document.getElementById("val-w-loss").innerText = `${wLoss.toFixed(2)} (${Math.round(wLoss / effectiveSum * 100)}%)`;
  document.getElementById("val-w-spec").innerText = `${wSpec.toFixed(2)} (${Math.round(wSpec / effectiveSum * 100)}%)`;
  document.getElementById("val-w-sent").innerText = `${wSent.toFixed(2)} (${Math.round(wSent / effectiveSum * 100)}%)`;
  document.getElementById("val-w-spat").innerText = `${wSpat.toFixed(2)} (${Math.round(wSpat / effectiveSum * 100)}%)`;

  const badge = document.getElementById("weight-sum-badge");
  if (badge) {
    if (Math.abs(sum - 1.0) < 0.01) {
      badge.className = "badge green";
      badge.innerText = `Sum: ${sum.toFixed(2)} (Canonical 100%)`;
    } else {
      badge.className = "badge amber";
      badge.innerText = `Raw Sum: ${sum.toFixed(2)} (Auto-scaled to 100% internally)`;
    }
  }

  recalculateDynamicScores();
  renderScoreboard();
  renderDecisionMatrix();
}

function recalculateDynamicScores() {
  const sum = weights.forest_loss + weights.specificity + weights.sentiment + weights.spatial_match;
  const effectiveSum = sum > 0 ? sum : 1.0;

  companies.forEach(c => {
    c.dynamic_score = (
      weights.forest_loss * c.subscores.forest_loss +
      weights.specificity * c.subscores.specificity +
      weights.sentiment * c.subscores.sentiment +
      weights.spatial_match * c.subscores.spatial_match
    ) / effectiveSum;
  });

  const sortedForRank = [...companies].sort((a, b) => b.dynamic_score - a.dynamic_score);
  sortedForRank.forEach((c, i) => {
    c.dynamic_rank = i + 1;
  });
}

function applyWeightPreset(wLoss, wSpec, wSent, wSpat) {
  const sLoss = document.getElementById("slider-w-loss");
  const sSpec = document.getElementById("slider-w-spec");
  const sSent = document.getElementById("slider-w-sent");
  const sSpat = document.getElementById("slider-w-spat");

  if (sLoss) sLoss.value = wLoss.toFixed(2);
  if (sSpec) sSpec.value = wSpec.toFixed(2);
  if (sSent) sSent.value = wSent.toFixed(2);
  if (sSpat) sSpat.value = wSpat.toFixed(2);

  updateWeightsFromSliders();
}

function autoNormalizeWeights() {
  const sum = weights.forest_loss + weights.specificity + weights.sentiment + weights.spatial_match;
  if (sum <= 0) return;

  const wLoss = weights.forest_loss / sum;
  const wSpec = weights.specificity / sum;
  const wSent = weights.sentiment / sum;
  const wSpat = weights.spatial_match / sum;

  applyWeightPreset(wLoss, wSpec, wSent, wSpat);
}

function resetWeightsToCanonical() {
  applyWeightPreset(0.35, 0.35, 0.15, 0.15);
}

// 7. HEAD-TO-HEAD COMPARISON MODAL
function populateCompareSelects() {
  const selA = document.getElementById("compare-select-a");
  const selB = document.getElementById("compare-select-b");
  if (!selA || !selB || !companies.length) return;

  selA.innerHTML = "";
  selB.innerHTML = "";

  companies.forEach((c, idx) => {
    const optA = document.createElement("option");
    optA.value = c.company;
    optA.innerText = `#${c.rank} ${c.name} (${c.mismatch_score.toFixed(1)})`;
    if (idx === 0) optA.selected = true; // KLK
    selA.appendChild(optA);

    const optB = document.createElement("option");
    optB.value = c.company;
    optB.innerText = `#${c.rank} ${c.name} (${c.mismatch_score.toFixed(1)})`;
    if (idx === companies.length - 1) optB.selected = true; // Astra Agro
    selB.appendChild(optB);
  });
}

function openCompareModal(compA = "klk", compB = "astraagro") {
  const modal = document.getElementById("compare-modal");
  const selA = document.getElementById("compare-select-a");
  const selB = document.getElementById("compare-select-b");

  if (selA) selA.value = compA;
  if (selB) selB.value = compB;

  if (modal) modal.classList.add("active");
  updateComparison();
}

function closeCompareModal(e) {
  if (e && e.target !== e.currentTarget && !e.target.classList.contains("close-btn")) return;
  const modal = document.getElementById("compare-modal");
  if (modal) modal.classList.remove("active");
}

function updateComparison() {
  const compKeyA = document.getElementById("compare-select-a")?.value || "klk";
  const compKeyB = document.getElementById("compare-select-b")?.value || "astraagro";

  const compA = companies.find(c => c.company === compKeyA);
  const compB = companies.find(c => c.company === compKeyB);
  if (!compA || !compB) return;

  const detailsElem = document.getElementById("compare-details");
  if (detailsElem) {
    detailsElem.innerHTML = `
      <div style="background:var(--card); border:1px solid rgba(239, 68, 68, 0.4); border-radius:var(--radius-md); padding:18px;">
        <h4 style="color:#ef4444; font-size:16px; margin-bottom:4px;">#${compA.rank} ${compA.name}</h4>
        <div style="font-size:24px; font-weight:800; font-family:var(--font-mono); margin-bottom:12px;">
          ${compA.mismatch_score.toFixed(1)} <span style="font-size:12px; color:var(--muted);">/ 100</span>
        </div>
        <div style="font-size:12.5px; color:var(--text-secondary); display:flex; flex-direction:column; gap:6px;">
          <div>🌲 <strong>Loss Score:</strong> ${compA.subscores.forest_loss.toFixed(1)} (${Math.round(compA.loss_post2020_ha).toLocaleString()} ha)</div>
          <div>🎯 <strong>Specificity:</strong> ${compA.subscores.specificity.toFixed(1)} / 100</div>
          <div>😊 <strong>Sentiment:</strong> ${compA.subscores.sentiment.toFixed(1)} / 100</div>
          <div>📍 <strong>Spatial Match:</strong> ${compA.subscores.spatial_match.toFixed(1)}% severe</div>
          <div>🏭 <strong>Mills:</strong> ${compA.n_mills} (${compA.n_mills_severe} severe)</div>
          <div>📄 <strong>Claims:</strong> ${compA.n_claims} corporate commitments</div>
        </div>
      </div>

      <div style="background:var(--card); border:1px solid rgba(34, 197, 94, 0.4); border-radius:var(--radius-md); padding:18px;">
        <h4 style="color:#22c55e; font-size:16px; margin-bottom:4px;">#${compB.rank} ${compB.name}</h4>
        <div style="font-size:24px; font-weight:800; font-family:var(--font-mono); margin-bottom:12px;">
          ${compB.mismatch_score.toFixed(1)} <span style="font-size:12px; color:var(--muted);">/ 100</span>
        </div>
        <div style="font-size:12.5px; color:var(--text-secondary); display:flex; flex-direction:column; gap:6px;">
          <div>🌲 <strong>Loss Score:</strong> ${compB.subscores.forest_loss.toFixed(1)} (${Math.round(compB.loss_post2020_ha).toLocaleString()} ha)</div>
          <div>🎯 <strong>Specificity:</strong> ${compB.subscores.specificity.toFixed(1)} / 100</div>
          <div>😊 <strong>Sentiment:</strong> ${compB.subscores.sentiment.toFixed(1)} / 100</div>
          <div>📍 <strong>Spatial Match:</strong> ${compB.subscores.spatial_match.toFixed(1)}% severe</div>
          <div>🏭 <strong>Mills:</strong> ${compB.n_mills} (${compB.n_mills_severe} severe)</div>
          <div>📄 <strong>Claims:</strong> ${compB.n_claims} corporate commitments</div>
        </div>
      </div>
    `;
  }

  // Render Dual Radar Chart
  setTimeout(() => {
    const ctx = document.getElementById("compareRadarCanvas");
    if (!ctx) return;
    if (compareRadarChart) compareRadarChart.destroy();

    compareRadarChart = new Chart(ctx, {
      type: "radar",
      data: {
        labels: ["Forest Loss", "Specificity", "Sentiment", "Spatial Match"],
        datasets: [
          {
            label: compA.name,
            data: [
              compA.subscores.forest_loss,
              compA.subscores.specificity,
              compA.subscores.sentiment,
              compA.subscores.spatial_match
            ],
            backgroundColor: "rgba(239, 68, 68, 0.2)",
            borderColor: "#ef4444",
            pointBackgroundColor: "#ef4444",
            borderWidth: 2
          },
          {
            label: compB.name,
            data: [
              compB.subscores.forest_loss,
              compB.subscores.specificity,
              compB.subscores.sentiment,
              compB.subscores.spatial_match
            ],
            backgroundColor: "rgba(34, 197, 94, 0.2)",
            borderColor: "#22c55e",
            pointBackgroundColor: "#22c55e",
            borderWidth: 2
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          r: {
            min: 0,
            max: 100,
            ticks: { display: false },
            grid: { color: "#1e3823" },
            pointLabels: { color: "#bcd4c1", font: { size: 10.5, family: "JetBrains Mono" } }
          }
        },
        plugins: {
          legend: {
            display: true,
            labels: { color: "#f3f8f4", font: { family: "Inter", size: 12, weight: 600 } }
          }
        }
      }
    });
  }, 40);
}

// 8. COMPANY DETAIL MODAL & RADAR CHART
function showCompanyModal(compKey) {
  const comp = companies.find((c) => c.company.toLowerCase() === compKey.toLowerCase());
  if (!comp) return;

  const modal = document.getElementById("company-modal");
  const content = document.getElementById("modal-content");
  if (!modal || !content) return;

  const compMills = mills.filter((m) => m.company.toLowerCase() === comp.company.toLowerCase());
  const topMills = [...compMills].sort((a, b) => b.loss_post2020_ha - a.loss_post2020_ha).slice(0, 5);

  content.innerHTML = `
    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:20px;">
      <div>
        <div style="font-family:var(--font-mono); font-size:12px; color:var(--accent); text-transform:uppercase;">
          Rank #${comp.dynamic_rank} of 11
        </div>
        <h2 style="font-size:26px; font-weight:800; color:var(--text);">${comp.name}</h2>
        <p style="color:var(--text-secondary); font-size:14px; margin-top:2px;">
          Mismatch Score: <strong style="color:${comp.dynamic_score >= 60 ? '#ef4444' : '#f59e0b'}; font-size:18px;">${comp.dynamic_score.toFixed(1)}</strong> / 100
        </p>
      </div>
    </div>

    <!-- RADAR CHART CONTAINER -->
    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px; margin-bottom:24px;">
      <div style="height:250px; background:var(--card); border:1px solid var(--border); border-radius:var(--radius-md); padding:12px;">
        <canvas id="companyRadarCanvas"></canvas>
      </div>
      <div>
        <div style="font-size:13px; font-weight:700; color:var(--text); margin-bottom:8px;">Sub-score Profile</div>
        <div style="font-size:12.5px; color:var(--text-secondary); display:flex; flex-direction:column; gap:6px;">
          <div>🌲 <strong>Forest Loss (35%):</strong> ${comp.subscores.forest_loss.toFixed(1)} / 100</div>
          <div>🎯 <strong>Specificity (35%):</strong> ${comp.subscores.specificity.toFixed(1)} / 100</div>
          <div>😊 <strong>Sentiment (15%):</strong> ${comp.subscores.sentiment.toFixed(1)} / 100</div>
          <div>📍 <strong>Spatial Match (15%):</strong> ${comp.subscores.spatial_match.toFixed(1)} / 100</div>
          <div style="margin-top:6px; padding-top:6px; border-top:1px solid var(--border);">
            <strong>Post-2020 Loss:</strong> ${Math.round(comp.loss_post2020_ha).toLocaleString()} ha across ${comp.n_mills} mills
          </div>
          <div>
            <strong>Severe Mills (> median):</strong> ${comp.n_mills_severe} of ${comp.n_mills} (${Math.round(comp.n_mills_severe / comp.n_mills * 100)}%)
          </div>
        </div>
      </div>
    </div>

    <!-- TOP MILLS LIST -->
    <div style="margin-bottom:20px;">
      <h4 style="font-size:14px; font-weight:700; color:var(--text); margin-bottom:10px;">Highest Forest-Loss Mills</h4>
      <div style="display:flex; flex-direction:column; gap:6px;">
        ${topMills.map(m => `
          <div style="display:flex; justify-content:space-between; align-items:center; background:var(--card); padding:8px 12px; border-radius:var(--radius-sm); border:1px solid var(--border); font-size:12px;">
            <span><strong>${m.mill_name}</strong> (${m.country})</span>
            <div style="display:flex; gap:10px; align-items:center;">
              <span style="font-family:var(--font-mono); color:var(--amber);">${Math.round(m.loss_post2020_ha).toLocaleString()} ha</span>
              <button onclick="openLightbox('${m.map_image}', '${comp.name} - ${m.mill_name}')" style="background:none; border:1px solid var(--border); color:var(--accent); padding:3px 8px; border-radius:4px; cursor:pointer;">Map</button>
            </div>
          </div>
        `).join('')}
      </div>
    </div>

    <div style="display:flex; gap:10px;">
      <button onclick="filterMapToCompany('${comp.company}')" class="btn-control active" style="font-weight:700;">
        🗺️ View on Map
      </button>
      <button onclick="filterGalleryToCompany('${comp.company}')" class="btn-control">
        🖼️ View Clearing Maps (${compMills.length})
      </button>
    </div>
  `;

  modal.classList.add("active");

  setTimeout(() => {
    const ctx = document.getElementById("companyRadarCanvas");
    if (!ctx) return;
    if (companyRadarChart) companyRadarChart.destroy();

    companyRadarChart = new Chart(ctx, {
      type: "radar",
      data: {
        labels: ["Forest Loss", "Specificity", "Sentiment", "Spatial Match"],
        datasets: [{
          label: comp.name,
          data: [
            comp.subscores.forest_loss,
            comp.subscores.specificity,
            comp.subscores.sentiment,
            comp.subscores.spatial_match
          ],
          backgroundColor: "rgba(34, 197, 94, 0.25)",
          borderColor: "#22c55e",
          pointBackgroundColor: "#22c55e",
          borderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          r: {
            min: 0,
            max: 100,
            ticks: { display: false },
            grid: { color: "#1e3823" },
            pointLabels: { color: "#bcd4c1", font: { size: 10, family: "JetBrains Mono" } }
          }
        },
        plugins: { legend: { display: false } }
      }
    });
  }, 40);
}

function closeCompanyModal(e) {
  if (e && e.target !== e.currentTarget && !e.target.classList.contains("close-btn")) return;
  const modal = document.getElementById("company-modal");
  if (modal) modal.classList.remove("active");
}

function filterMapToCompany(compKey) {
  closeCompanyModal(null);
  const compSelect = document.getElementById("company-filter");
  if (compSelect) {
    compSelect.value = compKey;
    updateMapMarkers();
  }
  document.getElementById("map-section")?.scrollIntoView({ behavior: "smooth" });
}

function filterGalleryToCompany(compKey) {
  closeCompanyModal(null);
  const compSelect = document.getElementById("gallery-company-filter");
  if (compSelect) {
    compSelect.value = compKey;
    galleryDisplayLimit = 48;
    renderGallery();
  }
  document.getElementById("gallery")?.scrollIntoView({ behavior: "smooth" });
}

function populateCompanyFilters() {
  const selects = [
    document.getElementById("company-filter"),
    document.getElementById("gallery-company-filter"),
    document.getElementById("claims-company-filter")
  ];

  selects.forEach((sel) => {
    if (!sel) return;
    sel.innerHTML = '<option value="all">All Companies (11)</option>';
    companies.forEach((c) => {
      const opt = document.createElement("option");
      opt.value = c.company;
      opt.innerText = `${c.name} (${c.n_mills} mills)`;
      sel.appendChild(opt);
    });
  });
}

// 9. CITATION COPY
function copyBibtex() {
  const text = document.getElementById("bibtex-text")?.innerText || "";
  navigator.clipboard.writeText(text).then(() => {
    const fb = document.getElementById("copy-feedback");
    if (fb) {
      fb.style.display = "inline";
      setTimeout(() => { fb.style.display = "none"; }, 3000);
    }
  });
}

// 10. EVENT LISTENERS
function setupEventListeners() {
  // Map controls
  document.getElementById("company-filter")?.addEventListener("change", updateMapMarkers);
  document.getElementById("severity-filter")?.addEventListener("change", updateMapMarkers);

  // Gallery controls
  document.getElementById("gallery-company-filter")?.addEventListener("change", () => {
    galleryDisplayLimit = 24;
    renderGallery();
  });
  document.getElementById("gallery-search")?.addEventListener("input", () => {
    galleryDisplayLimit = 24;
    renderGallery();
  });

  // Claims controls
  document.getElementById("claims-company-filter")?.addEventListener("change", renderClaims);
  document.getElementById("claims-strength-filter")?.addEventListener("change", renderClaims);
  document.getElementById("claims-topic-filter")?.addEventListener("change", renderClaims);
  document.getElementById("claims-search")?.addEventListener("input", renderClaims);

  // Keyboard navigation for Lightbox and Modals
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeLightbox(null);
      closeCompanyModal(null);
      closeCompareModal(null);
      closeBufferModalDirect();
      closePrithviModalDirect();
    } else if (e.key === "ArrowLeft") {
      navigateLightbox(-1);
    } else if (e.key === "ArrowRight") {
      navigateLightbox(1);
    }
  });
}

// 7. BUFFER SENSITIVITY MODAL LOGIC
async function loadBufferData() {
  if (bufferData) return;
  try {
    const res = await fetch("data/buffer_sensitivity.json");
    if (res.ok) {
      bufferData = await res.json();
      renderBufferTable();
    }
  } catch (err) {
    console.error("Error loading buffer sensitivity data:", err);
  }
}

function renderBufferTable() {
  if (!bufferData || !bufferData.records) return;
  const tbody = document.getElementById("buffer-table-body");
  if (!tbody) return;
  tbody.innerHTML = "";

  const compMap = {};
  bufferData.records.forEach(r => {
    if (!compMap[r.company]) compMap[r.company] = {};
    compMap[r.company][r.buffer_km] = r.loss_pct;
  });

  Object.keys(compMap).sort().forEach(comp => {
    const d = compMap[comp];
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td style="font-weight:700; color:var(--text);">${comp}</td>
      <td style="font-family:var(--font-mono);">${(d[5] || 0).toFixed(2)}%</td>
      <td style="font-family:var(--font-mono); color:var(--accent); font-weight:700; background:rgba(34,197,94,0.08);">${(d[10] || 0).toFixed(2)}%</td>
      <td style="font-family:var(--font-mono);">${(d[15] || 0).toFixed(2)}%</td>
      <td style="font-family:var(--font-mono);">${(d[20] || 0).toFixed(2)}%</td>
      <td style="font-family:var(--font-mono);">${(d[30] || 0).toFixed(2)}%</td>
    `;
    tbody.appendChild(tr);
  });
}

async function openBufferModal() {
  if (!bufferData) {
    await loadBufferData();
  } else {
    renderBufferTable();
  }
  const modal = document.getElementById("buffer-modal");
  if (modal) {
    modal.classList.add("active");
    modal.style.display = "flex";
    document.body.style.overflow = "hidden";
  }
}

function closeBufferModal(e) {
  if (e && e.target && (e.target.id === "buffer-modal" || e.target.classList.contains("close-btn"))) {
    closeBufferModalDirect();
  }
}

function closeBufferModalDirect() {
  const modal = document.getElementById("buffer-modal");
  if (modal) {
    modal.classList.remove("active");
    modal.style.display = "none";
    document.body.style.overflow = "auto";
  }
}

// 8. PRITHVI EXPERIMENTS MODAL LOGIC
function openPrithviModal() {
  const modal = document.getElementById("prithvi-modal");
  if (modal) {
    modal.classList.add("active");
    modal.style.display = "flex";
    document.body.style.overflow = "hidden";
  }
}

function closePrithviModal(e) {
  if (e && e.target && (e.target.id === "prithvi-modal" || e.target.classList.contains("close-btn"))) {
    closePrithviModalDirect();
  }
}

function closePrithviModalDirect() {
  const modal = document.getElementById("prithvi-modal");
  if (modal) {
    modal.classList.remove("active");
    modal.style.display = "none";
    document.body.style.overflow = "auto";
  }
}

// Attach globally for inline HTML click handlers
window.openBufferModal = openBufferModal;
window.closeBufferModal = closeBufferModal;
window.closeBufferModalDirect = closeBufferModalDirect;
window.openPrithviModal = openPrithviModal;
window.closePrithviModal = closePrithviModal;
window.closePrithviModalDirect = closePrithviModalDirect;
window.openCompareModal = openCompareModal;
window.closeCompareModal = closeCompareModal;
window.closeCompanyModal = closeCompanyModal;
window.closeLightbox = closeLightbox;

// ============================================================
// ADDITIONS v5: Explainer, Charts, Rich Lightbox, Mobile Nav,
// Claims Pagination, Descals Visualization
// ============================================================

let descalsData = [];
let claimsDisplayLimit = 30;

// descals loaded separately in the setTimeout below

// ── CHART SHARED DEFAULTS ──
const CHART_ANIM = { duration: 1100, easing: "easeOutQuart" };
const AXIS_COLOR = "#8ca391";
const TICK_COLOR = "#799d7f";
const GRID_COLOR = "rgba(34,197,94,0.08)";
const TICK_Y = { color: "#cbd5e1", font: { size: 11.5, weight: "600" } };

// ── ANIMATED STAT COUNTERS ──
function runCounters() {
  document.querySelectorAll(".chart-stat-num[data-target]").forEach(el => {
    const target = parseFloat(el.dataset.target);
    const suffix = el.dataset.suffix || "";
    const decimals = parseInt(el.dataset.decimals || "0");
    const start = performance.now();
    const duration = 1600;
    const step = ts => {
      const p = Math.min((ts - start) / duration, 1);
      const ease = 1 - Math.pow(1 - p, 3);
      const v = target * ease;
      el.textContent = (decimals > 0 ? v.toFixed(decimals) : Math.round(v).toLocaleString()) + suffix;
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  });
}

// Trigger counters when section scrolls into view
const _counterObserver = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { runCounters(); _counterObserver.disconnect(); } });
}, { threshold: 0.2 });
document.addEventListener("DOMContentLoaded", () => {
  const statsRow = document.querySelector(".chart-stats-row");
  if (statsRow) _counterObserver.observe(statsRow);
});

// ── MISMATCH SCORE LEADERBOARD ──
function renderMismatchChart() {
  const ctx = document.getElementById("mismatchChart");
  if (!ctx || !companies.length) return;

  const sorted = [...companies].sort((a, b) => b.mismatch_score - a.mismatch_score);
  const labels = sorted.map(c => c.name);
  const vals   = sorted.map(c => c.mismatch_score);
  const colors = vals.map(v =>
    v >= 55 ? "rgba(239,68,68,0.85)" :
    v >= 40 ? "rgba(245,158,11,0.85)" :
              "rgba(34,197,94,0.85)"
  );

  new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "Mismatch Score",
        data: vals,
        backgroundColor: colors,
        borderColor: colors.map(c => c.replace("0.85", "1")),
        borderWidth: 1.5,
        borderRadius: 5,
        borderSkipped: false
      }]
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      animation: CHART_ANIM,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "rgba(13,23,38,0.95)",
          borderColor: "rgba(34,197,94,0.4)",
          borderWidth: 1,
          titleColor: "#fff",
          bodyColor: "#cbd5e1",
          padding: 10,
          callbacks: {
            label: item => ` Score: ${item.raw} / 100`,
            afterLabel: item => {
              const c = sorted[item.dataIndex];
              return [
                ` Forest loss: ${c.subscores.forest_loss.toFixed(1)}`,
                ` Specificity: ${c.subscores.specificity.toFixed(1)}`,
                ` Sentiment:   ${c.subscores.sentiment.toFixed(1)}`,
                ` Spatial:     ${c.subscores.spatial_match.toFixed(1)}`
              ];
            }
          }
        }
      },
      scales: {
        x: {
          min: 0, max: 100,
          title: { display: true, text: "Mismatch Score (0–100)", color: AXIS_COLOR, font: { size: 11 } },
          ticks: { color: TICK_COLOR },
          grid: { color: GRID_COLOR }
        },
        y: { ticks: TICK_Y, grid: { display: false } }
      }
    }
  });
}

// ── SCORE COMPONENT STACKED BAR ──
function renderSubscoreChart() {
  const ctx = document.getElementById("subscoreChart");
  if (!ctx || !companies.length) return;

  const sorted = [...companies].sort((a, b) => b.mismatch_score - a.mismatch_score);
  const labels = sorted.map(c => c.name);

  const mkDataset = (key, label, color) => ({
    label,
    data: sorted.map(c => parseFloat((c.subscores[key] * (key === "forest_loss" ? 0.35 : key === "specificity" ? 0.35 : key === "sentiment" ? 0.15 : 0.15)).toFixed(1))),
    backgroundColor: color,
    borderRadius: 3,
    borderSkipped: false
  });

  new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        mkDataset("forest_loss", "Forest Loss (35%)",    "rgba(239,68,68,0.82)"),
        mkDataset("specificity", "Specificity (35%)",    "rgba(245,158,11,0.82)"),
        mkDataset("sentiment",   "Sentiment (15%)",      "rgba(56,189,248,0.75)"),
        mkDataset("spatial_match", "Spatial Match (15%)", "rgba(192,132,252,0.75)")
      ]
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      animation: CHART_ANIM,
      plugins: {
        legend: {
          display: true,
          position: "top",
          labels: { color: "#cbd5e1", font: { size: 11 }, padding: 14, boxWidth: 12 }
        },
        tooltip: {
          backgroundColor: "rgba(13,23,38,0.95)",
          borderColor: "rgba(34,197,94,0.4)",
          borderWidth: 1,
          titleColor: "#fff",
          bodyColor: "#cbd5e1",
          padding: 10,
          callbacks: { label: item => ` ${item.dataset.label}: ${item.raw}` }
        }
      },
      scales: {
        x: {
          stacked: true,
          title: { display: true, text: "Weighted contribution to mismatch score", color: AXIS_COLOR, font: { size: 11 } },
          ticks: { color: TICK_COLOR },
          grid: { color: GRID_COLOR }
        },
        y: { stacked: true, ticks: TICK_Y, grid: { display: false } }
      }
    }
  });
}

// ── SCATTER: FOREST LOSS % vs MISMATCH SCORE ──
function renderScatterChart() {
  const ctx = document.getElementById("scatterChart");
  if (!ctx || !companies.length) return;

  const data = companies.map(c => ({
    x: parseFloat(c.loss_pct_of_forest.toFixed(2)),
    y: c.mismatch_score,
    label: c.name
  }));

  new Chart(ctx, {
    type: "scatter",
    data: {
      datasets: [{
        label: "Companies",
        data,
        backgroundColor: data.map(d =>
          d.y >= 55 ? "rgba(239,68,68,0.85)" :
          d.y >= 40 ? "rgba(245,158,11,0.85)" :
                      "rgba(34,197,94,0.85)"
        ),
        borderColor: "rgba(255,255,255,0.15)",
        borderWidth: 1,
        pointRadius: 9,
        pointHoverRadius: 12
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: CHART_ANIM,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "rgba(13,23,38,0.95)",
          borderColor: "rgba(34,197,94,0.4)",
          borderWidth: 1,
          titleColor: "#fff",
          bodyColor: "#cbd5e1",
          padding: 10,
          callbacks: {
            title: items => data[items[0].dataIndex].label,
            label: item => [` Forest loss: ${item.raw.x}%`, ` Mismatch score: ${item.raw.y}`]
          }
        }
      },
      scales: {
        x: {
          title: { display: true, text: "Forest loss as % of year-2000 cover", color: AXIS_COLOR, font: { size: 11 } },
          ticks: { color: TICK_COLOR, callback: v => v + "%" },
          grid: { color: GRID_COLOR }
        },
        y: {
          title: { display: true, text: "Mismatch Score (0–100)", color: AXIS_COLOR, font: { size: 11 } },
          min: 0, max: 80,
          ticks: { color: TICK_COLOR },
          grid: { color: GRID_COLOR }
        }
      }
    }
  });
}

// ── FOREST LOSS BAR CHART ──
function renderForestLossChart() {
  const ctx = document.getElementById("forestLossChart");
  if (!ctx || !companies.length) return;

  const sorted = [...companies].sort((a, b) => b.loss_post2020_ha - a.loss_post2020_ha);
  const labels = sorted.map(c => c.name);
  const vals   = sorted.map(c => Math.round(c.loss_post2020_ha));
  const colors = sorted.map(c =>
    c.subscores.forest_loss > 60 ? "rgba(239,68,68,0.82)" :
    c.subscores.forest_loss > 30 ? "rgba(245,158,11,0.82)" :
                                   "rgba(34,197,94,0.82)"
  );

  new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "Post-2020 Forest Loss (ha)",
        data: vals,
        backgroundColor: colors,
        borderColor: colors.map(c => c.replace("0.82", "1")),
        borderWidth: 1,
        borderRadius: 4
      }]
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      animation: CHART_ANIM,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "rgba(13,23,38,0.95)",
          borderColor: "rgba(34,197,94,0.4)",
          borderWidth: 1,
          callbacks: {
            label: item => ` ${item.raw.toLocaleString()} ha within 10 km of mills`
          }
        }
      },
      scales: {
        x: {
          title: { display: true, text: "Hectares lost (post Jan 2021)", color: AXIS_COLOR, font: { size: 11 } },
          ticks: { color: TICK_COLOR, callback: v => (v/1000).toFixed(0) + "k" },
          grid: { color: GRID_COLOR }
        },
        y: { ticks: TICK_Y, grid: { display: false } }
      }
    }
  });
}

// ── DESCALS OIL PALM CONVERSION CHART ──
function renderDescalsChart() {
  const ctx = document.getElementById("descalsChart");
  if (!ctx || !descalsData.length) return;

  const sorted = [...descalsData].sort((a, b) => b.pct_loss_to_palm - a.pct_loss_to_palm);
  const labels = sorted.map(d => d.company.toUpperCase());
  const vals   = sorted.map(d => d.pct_loss_to_palm);

  new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "% of cleared land now oil palm",
        data: vals,
        backgroundColor: vals.map(v =>
          v > 70 ? "rgba(239,68,68,0.82)" :
          v > 50 ? "rgba(245,158,11,0.82)" :
                   "rgba(56,189,248,0.82)"
        ),
        borderRadius: 4
      }]
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      animation: CHART_ANIM,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "rgba(13,23,38,0.95)",
          borderColor: "rgba(34,197,94,0.4)",
          borderWidth: 1,
          callbacks: {
            label: item => ` ${item.raw.toFixed(1)}% of cleared area converted to oil palm`
          }
        }
      },
      scales: {
        x: {
          min: 0, max: 100,
          title: { display: true, text: "% of post-2020 clearing now oil palm (Descals 2021)", color: AXIS_COLOR, font: { size: 11 } },
          ticks: { color: TICK_COLOR, callback: v => v + "%" },
          grid: { color: GRID_COLOR }
        },
        y: { ticks: TICK_Y, grid: { display: false } }
      }
    }
  });
}

// ── RICH LIGHTBOX METADATA ──
function buildMillMetaHTML(mill) {
  if (!mill) return "";
  const lossPct = mill.loss_pct ? mill.loss_pct.toFixed(1) : "—";
  const lossHa  = Math.round(mill.loss_post2020_ha).toLocaleString();
  const f2000   = Math.round(mill.forest_2000_ha).toLocaleString();
  const lat     = mill.latitude ? mill.latitude.toFixed(4) : "—";
  const lon     = mill.longitude ? mill.longitude.toFixed(4) : "—";

  return `
    <div class="lm-section">
      <span class="lm-label">📍 Mill Location</span>
      <div class="lm-row"><span class="lm-key">Mill</span><span class="lm-val">${mill.mill_name}</span></div>
      <div class="lm-row"><span class="lm-key">Company</span><span class="lm-val">${mill.company.toUpperCase()}</span></div>
      <div class="lm-row"><span class="lm-key">Country</span><span class="lm-val">${mill.country}</span></div>
      <div class="lm-row"><span class="lm-key">Coordinates</span><span class="lm-val" style="font-family:var(--font-mono);font-size:11px;">${lat}, ${lon}</span></div>
    </div>
    <hr class="lm-divider">
    <div class="lm-section">
      <span class="lm-label">📅 Imagery & Period</span>
      <div class="lm-row"><span class="lm-key">Left panel</span><span class="lm-val">Sentinel-2 (2019 baseline)</span></div>
      <div class="lm-row"><span class="lm-key">Right panel</span><span class="lm-val">Sentinel-2 2024 + Hansen loss overlay</span></div>
      <div class="lm-row"><span class="lm-key">Loss measured</span><span class="lm-val">Jan 2021 – Dec 2024</span></div>
      <div class="lm-row"><span class="lm-key">Why 2021?</span><span class="lm-val" style="font-size:11.5px;color:var(--text-secondary);">EU Deforestation Regulation (EUDR) cutoff date is 31 Dec 2020</span></div>
    </div>
    <hr class="lm-divider">
    <div class="lm-section">
      <span class="lm-label">🟥 What the Colors Show</span>
      <div class="lm-legend-item"><div class="lm-swatch" style="background:#ef4444;"></div>Red cells — tree cover loss after Jan 2021</div>
      <div class="lm-legend-item"><div class="lm-swatch" style="background:#f97316;"></div>Orange cells — moderate loss signal</div>
      <div class="lm-legend-item"><div class="lm-swatch" style="background:#22c55e;"></div>Green area — intact forest retained</div>
      <div class="lm-legend-item"><div class="lm-swatch" style="background:rgba(6,182,212,0.5);border:2px dashed #06b6d4;"></div>Dashed ring — 10 km study boundary</div>
      <div class="lm-row" style="margin-top:6px"><span class="lm-key">Dataset</span><span class="lm-val">Hansen GFC v1.13 (Landsat 30m)</span></div>
      <div class="lm-row"><span class="lm-key">Resolution</span><span class="lm-val">30 m per pixel</span></div>
    </div>
    <hr class="lm-divider">
    <div class="lm-section">
      <span class="lm-label">📊 Measured Forest Loss</span>
      <div class="lm-row"><span class="lm-key">Forest in 2000</span><span class="lm-val">${f2000} ha</span></div>
      <div class="lm-row"><span class="lm-key">Post-2020 loss</span><span class="lm-val hi">${lossHa} ha</span></div>
      <div class="lm-row"><span class="lm-key">% of 2000 baseline</span><span class="lm-val hi">${lossPct}% lost</span></div>
      <div class="lm-row"><span class="lm-key">Study area</span><span class="lm-val">10 km radius (~314 km²)</span></div>
    </div>
    <hr class="lm-divider">
    <div class="lm-section">
      <div class="lm-warning">
        ⚠️ <strong>Limitation:</strong> Loss is measured within 10 km of the mill. Multiple actors — including smallholders and other companies — operate in this area. This measures <em>spatial correspondence</em>, not proven causation.
      </div>
    </div>
  `;
}

// Override openLightboxByIndex to inject metadata (replaces original via hoisting order)
function openLightboxByIndex(idx) {
  if (idx < 0 || idx >= activeGalleryList.length) return;
  currentLightboxIndex = idx;
  const m = activeGalleryList[idx];
  openLightbox(m.map_image,
    `${m.company.toUpperCase()} · ${m.mill_name} · ${m.country} · Post-2020 loss: ${Math.round(m.loss_post2020_ha).toLocaleString()} ha`
  );
  const metaPanel = document.getElementById("lightbox-meta");
  if (metaPanel) metaPanel.innerHTML = buildMillMetaHTML(m);
}

// Also enrich map-popup openLightbox calls that pass mill data via a global helper
function openLightboxForMill(millId) {
  const m = mills.find(x => x.id === millId);
  if (!m) return;
  const idxInActive = activeGalleryList.indexOf(m);
  if (idxInActive >= 0) {
    openLightboxByIndex(idxInActive);
  } else {
    openLightbox(m.map_image,
      `${m.company.toUpperCase()} · ${m.mill_name} · ${m.country}`
    );
    const metaPanel = document.getElementById("lightbox-meta");
    if (metaPanel) metaPanel.innerHTML = buildMillMetaHTML(m);
  }
}

// ── CLAIMS PAGINATION ──
function renderClaims() {
  const container = document.getElementById("claims-grid");
  if (!container) return;
  container.innerHTML = "";

  const compFilter     = document.getElementById("claims-company-filter")?.value || "all";
  const strengthFilter = document.getElementById("claims-strength-filter")?.value || "all";
  const topicFilter    = document.getElementById("claims-topic-filter")?.value || "all";
  const searchFilter   = document.getElementById("claims-search")?.value.toLowerCase().trim() || "";

  const filtered = claims.filter(c => {
    const matchComp     = (compFilter === "all" || c.company.toLowerCase() === compFilter.toLowerCase());
    const matchStrength = (strengthFilter === "all" || c.strength.toLowerCase() === strengthFilter.toLowerCase());
    const matchTopic    = (topicFilter === "all" || c.esg_category === topicFilter);
    const matchSearch   = !searchFilter || c.text.toLowerCase().includes(searchFilter);
    return matchComp && matchStrength && matchTopic && matchSearch;
  });

  const counter = document.getElementById("claims-counter");
  if (counter) counter.innerText = `Showing ${Math.min(claimsDisplayLimit, filtered.length)} of ${filtered.length} claims`;

  const loadMoreBtn = document.getElementById("claims-load-more-btn");
  if (loadMoreBtn) {
    loadMoreBtn.style.display = filtered.length > claimsDisplayLimit ? "block" : "none";
    loadMoreBtn.innerText = `Load More Claims (${filtered.length - claimsDisplayLimit} remaining)`;
  }

  filtered.slice(0, claimsDisplayLimit).forEach(c => {
    const card = document.createElement("div");
    card.className = "claim-card";

    let textHtml = c.text;
    if (searchFilter) {
      const regex = new RegExp(`(${searchFilter.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")})`, "gi");
      textHtml = textHtml.replace(regex, '<span class="highlight">$1</span>');
    }

    const specBadgeColor = c.specificity_score > 0.6 ? "green" : (c.specificity_score > 0.3 ? "blue" : "amber");
    const sentBadgeColor = c.sentiment_score > 0.7 ? "green" : "blue";

    card.innerHTML = `
      <div class="claim-header">
        <strong style="color:var(--text);font-size:13px;">${c.company.toUpperCase()}</strong>
        <span class="badge ${c.strength === "hard" ? "green" : "amber"}">${c.strength.toUpperCase()} COMMITMENT</span>
      </div>
      <p class="claim-text">"${textHtml}"</p>
      <div class="claim-footer">
        <span class="badge ${specBadgeColor}" title="How concrete/auditable this claim is (0=vague, 1=specific targets)">Specificity: ${c.specificity_score.toFixed(2)}</span>
        <span class="badge ${sentBadgeColor}" title="Financial tone (higher=more positive/promotional)">Sentiment: ${c.sentiment_score.toFixed(2)}</span>
        <span class="badge purple">${c.esg_category}</span>
        ${c.is_deforestation ? '<span class="badge green">Zero-Deforestation</span>' : ""}
        ${c.is_ndpe ? '<span class="badge blue">NDPE</span>' : ""}
        ${c.has_deadline ? '<span class="badge amber">Target Date Cited</span>' : ""}
      </div>
    `;
    container.appendChild(card);
  });
}

function resetClaimsFilters() {
  claimsDisplayLimit = 30;
  ["claims-company-filter","claims-strength-filter","claims-topic-filter"].forEach(id => {
    const el = document.getElementById(id); if (el) el.value = "all";
  });
  const src = document.getElementById("claims-search"); if (src) src.value = "";
  renderClaims();
}

function loadMoreClaims() {
  claimsDisplayLimit += 30;
  renderClaims();
}

// ── MOBILE NAV ──
function toggleMobileNav() {
  const overlay = document.getElementById("mobile-nav-overlay");
  if (overlay) overlay.classList.toggle("open");
}
function closeMobileNav() {
  const overlay = document.getElementById("mobile-nav-overlay");
  if (overlay) overlay.classList.remove("open");
}

// ── HOOK INTO DOMContentLoaded ──
document.addEventListener("DOMContentLoaded", () => {
  // Charts rendered after data loads (slight delay to ensure companies array populated)
  setTimeout(() => {
    renderMismatchChart();
    renderSubscoreChart();
    renderScatterChart();
    renderForestLossChart();
    if (descalsData.length) renderDescalsChart();
    else {
      // Attempt late load if descals not fetched yet
      fetch("data/descals.json").then(r => r.ok ? r.json() : []).then(d => {
        descalsData = d;
        if (d.length) renderDescalsChart();
      }).catch(() => {});
    }
  }, 600);

  // Scroll-spy: highlight active nav link
  const navLinks = document.querySelectorAll('.nav-links a[href^="#"]');
  const sections = Array.from(navLinks).map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
  const onScroll = () => {
    const scrollY = window.scrollY + 80;
    let active = sections[0];
    for (const s of sections) { if (s.offsetTop <= scrollY) active = s; }
    navLinks.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + active.id));
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
});

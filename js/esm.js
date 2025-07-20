function computeMineralMass(bd, depth, soc, k = 1.9) {
  const MT = bd * depth * 100;
  return MT * (1 - k * soc);
}

function esmCorrectionFixed(bd_i, soc_i, bd_n, soc_n, depth = 30, k = 1.9) {
  const Da = depth * (bd_i / bd_n) * ((1 - k * soc_i) / (1 - k * soc_n));
  const original = bd_n * depth * soc_n * 1e-2;
  const corrected = bd_n * Da * soc_n * 1e-2;
  return { Da, original, corrected };
}

function exponentialSocProfile(soc0, socInf, depth, kDecay, increments = 1) {
  const arr = [];
  for (let d = increments; d <= depth; d += increments) {
    arr.push(socInf + (soc0 - socInf) * Math.exp(-d * kDecay));
  }
  return arr;
}

function linearBdProfile(bdSurface, bdBottom, depth, increments = 1) {
  const n = Math.floor(depth / increments);
  const arr = [];
  if (n === 1) {
    arr.push(bdSurface);
  } else {
    const step = (bdBottom - bdSurface) / (n - 1);
    for (let i = 0; i < n; i++) {
      arr.push(bdSurface + step * i);
    }
  }
  return arr;
}

function esmCorrectionProfile(bd_i_profile, soc_i_profile, bd_n_profile, soc_n_profile, depth, increments = 1, k = 1.9) {
  const mult = increments * 1e4 * 1e-6;
  const sum = arr => arr.reduce((a, b) => a + b, 0);
  const mi = bd_i_profile.map((bd, i) => bd * mult * (1 - k * soc_i_profile[i]));
  const mn = bd_n_profile.map((bd, i) => bd * mult * (1 - k * soc_n_profile[i]));
  const delta_m = sum(mi) - sum(mn);
  const j = bd_n_profile.length - 1;
  const Da = depth + delta_m / (bd_n_profile[j] * (1 - k * soc_n_profile[j]) * mult);
  const base = bd_n_profile.reduce((s, bd, i) => s + bd * increments * soc_n_profile[i] * 1e-2, 0);
  const extra = bd_n_profile[j] * (increments + Da - depth) * soc_n_profile[j] * 1e-2;
  return base - (bd_n_profile[j] * increments * soc_n_profile[j] * 1e-2) + extra;
}

// expose functions globally
window.computeMineralMass = computeMineralMass;
window.esmCorrectionFixed = esmCorrectionFixed;
window.exponentialSocProfile = exponentialSocProfile;
window.linearBdProfile = linearBdProfile;
window.esmCorrectionProfile = esmCorrectionProfile;

function esmDeltas(rows, k = 1.9) {
  const groups = {};
  rows.forEach(r => {
    if (!r.Time) return;
    const t = r.Time.trim();
    const inc = parseFloat(r.Interval_cm);
    const bd = parseFloat(r.BD_g_cm3);
    const soc = parseFloat(r.SOC_percent) / 100;
    if (!groups[t]) {
      groups[t] = { bd: [], soc: [], inc, depth: 0 };
    }
    groups[t].bd.push(bd);
    groups[t].soc.push(soc);
    groups[t].depth += inc;
  });

  const times = Object.keys(groups).sort();
  if (times.length === 0) return [];
  const base = groups[times[0]];
  const baseStock = esmCorrectionProfile(base.bd, base.soc, base.bd, base.soc, base.depth, base.inc, k);

  return times.map(t => {
    const g = groups[t];
    const corr = esmCorrectionProfile(base.bd, base.soc, g.bd, g.soc, base.depth, base.inc, k);
    return { time: t, corrected: corr, delta: corr - baseStock };
  });
}

window.esmDeltas = esmDeltas;

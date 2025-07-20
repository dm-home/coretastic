# Equivalent Soil Mass (ESM) Calculator

This repository now contains a static implementation of the Equivalent Soil Mass calculator. All calculations are performed in the browser using JavaScript so the site can be hosted on GitHub Pages.

Upload a CSV with the columns below. The `data/default_clean.csv` file provides an example.

| Time | Interval_cm | BottomDepth_cm | SoilMass_Mg_ha | SOC_percent | BD_g_cm3 |
|------|-------------|---------------|----------------|-------------|----------|
| T0   | 15          | 15            | 2134           | 1.84        | 1.42     |
| T0   | 15          | 30            | 2366           | 1.01        | 1.58     |
| T1   | 15          | 15            | 1781           | 1.93        | 1.19     |
| T1   | 15          | 30            | 2083           | 1.13        | 1.39     |

Open `index.html` in a browser (or deploy the repository via GitHub Pages) to use the calculator. The app computes the equivalent soil mass for each time point and the change relative to the first time in the file.

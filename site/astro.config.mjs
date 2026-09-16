// @ts-check
import casoonPages from '@casoon/pages-theme';
import { defineConfig } from 'astro/config';
import { categories } from './src/categories.mjs';

// Project page: https://casoon.github.io/pine-scripts/ — `base` is the GitHub Pages path.
export default defineConfig({
  site: 'https://casoon.github.io/pine-scripts',
  base: '/pine-scripts/',
  integrations: [
    casoonPages({
      name: 'pine-scripts',
      description:
        'TradingView indicators and strategies in Pine Script v6, each with a declared data contract: market structure, trend, momentum and confluence.',
      repo: 'casoon/pine-scripts',
      license: 'MIT',
      packages: [{ label: 'TradingView', href: 'https://www.tradingview.com/u/WavesUnchained/' }],
      docsGroups: {
        'getting-started': 'Getting started',
        concepts: 'Concepts',
        ...categories,
      },
      // Each indicator keeps its own CHANGELOG.md; the repository has no release history.
      changelog: false,
      // Pine output only exists on a TradingView chart; nothing can be rendered at build time.
      showcase: false,
    }),
  ],
});

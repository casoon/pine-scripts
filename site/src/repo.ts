import { readdirSync, readFileSync } from 'node:fs';
import { posix, resolve } from 'node:path';
import { categories } from './categories.mjs';

/** Repository root. Astro runs in site/. */
export const repoRoot = resolve(process.cwd(), '..');
export const repoUrl = 'https://github.com/casoon/pine-scripts';

/** Repository documents that have a page on this site: repo path → docs id. */
const docPages: Record<string, string> = {
  'DATA_VALIDITY.md': 'concepts/data-validity',
  'strategies/README.md': 'concepts/strategies',
  'indicators/ALERT_KUERZEL.md': 'concepts/alerts',
};

export interface Indicator {
  /** Docs id `<category>/<name>`, hyphenated; served at /docs/<id>/. */
  id: string;
  category: string;
  /** Repository-relative directory and README path. */
  dir: string;
  file: string;
  title: string;
  /** Lead paragraph of the README as plain text. */
  description: string;
  /** README without title and lead paragraph, links rewritten for the site. */
  body: string;
  tradingView?: string;
}

/** Repository-relative paths of all files below `dir` for which `test` holds. */
export function listFiles(dir: string, test: (path: string) => boolean): string[] {
  return (readdirSync(resolve(repoRoot, dir), { recursive: true }) as string[])
    .map((path) => `${dir}/${path}`)
    .filter(test)
    .sort();
}

export const readRepoFile = (path: string) => readFileSync(resolve(repoRoot, path), 'utf8');

const slug = (name: string) => name.replace(/_/g, '-');
const plain = (md: string) =>
  md
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    .replace(/\*+|`/g, '')
    .replace(/\s+/g, ' ')
    .trim();

/** A paragraph that can serve as lead: prose, not a heading, list, table, quote or code. */
const isProse = (block: string) => !/^(#|\*\*TradingView:|[-*>|]\s|```|!\[|<)/.test(block);

/**
 * Relative links in a README point into the repository. Links to another indicator become
 * links to its page, links to documents with a page here go there, everything else goes to
 * GitHub. Pages sit two levels below /docs/, hence `../../`.
 */
function rewriteLinks(md: string, dir: string, pages: Map<string, string>): string {
  return md.replace(/\]\(([^)\s]+)\)/g, (match, target: string) => {
    const [path, hash] = target.split('#');
    if (!path || /^[a-z][a-z0-9+.-]*:/i.test(path)) return match;
    const anchor = hash ? `#${hash}` : '';
    const resolved = posix.normalize(posix.join(dir, path)).replace(/\/$/, '');
    const page = pages.get(resolved) ?? pages.get(resolved.replace(/\/README\.md$/, ''));
    if (page) return `](../../${page}/${anchor})`;
    const kind = posix.extname(resolved) ? 'blob' : 'tree';
    return `](${repoUrl}/${kind}/main/${resolved}${anchor})`;
  });
}

export function loadIndicators(): Indicator[] {
  const files = listFiles('indicators', (path) => path.endsWith('/README.md'));
  const indicators = files.map((file) => {
    const dir = posix.dirname(file);
    const category = slug(dir.split('/')[1]);
    return { file, dir, category, id: `${category}/${slug(posix.basename(dir))}` };
  });
  const pages = new Map([
    ...Object.entries(docPages),
    ...indicators.map(({ dir, id }) => [dir, id] as [string, string]),
  ]);

  return indicators.map(({ file, dir, category, id }) => {
    const [heading, ...rest] = readRepoFile(file).trim().split('\n');
    const blocks = rest.join('\n').trim().split(/\n\s*\n/);
    const leadIndex = blocks.findIndex(isProse);
    const lead = leadIndex === -1 ? '' : blocks.splice(leadIndex, 1)[0];
    return {
      id,
      category,
      dir,
      file,
      title: heading.replace(/^#\s+/, '').replace(/\s*\[WavesUnchained\]\s*$/, ''),
      description: plain(lead),
      body: rewriteLinks(blocks.join('\n\n'), dir, pages),
      tradingView: /\*\*TradingView:\*\*\s*<?(https:\/\/\S+?)>?(\s|$)/.exec(rest.join('\n'))?.[1],
    };
  });
}

const firstSentence = (text: string) => /^.+?[.!?](?=\s|$)/.exec(text)?.[0] ?? text;

/** Status from CATALOG.md, translated; the catalog itself is a German working document. */
const statusLabels: Record<string, string> = {
  Draft: 'Draft',
  Aktiv: 'In progress',
  Stabil: 'Code settled',
  Overengineered: 'Overengineered',
  Deprecated: 'Deprecated',
};

/** How far an indicator has been checked on real charts: the "Getestet" stars in CATALOG.md. */
const testedLabels = ['not yet', 'barely', 'a little', 'partly', 'mostly', 'thoroughly'];

export interface CatalogEntry {
  status: string;
  tested: string;
}

/** Status and test depth per indicator directory, read from the tables in CATALOG.md. */
export function loadCatalog(): Map<string, CatalogEntry> {
  const entries = new Map<string, CatalogEntry>();
  for (const line of readRepoFile('CATALOG.md').split('\n')) {
    const cells = line.split('|').map((cell) => cell.trim());
    const dir = /^\[[^\]]+\]\((indicators\/[^)]+?)\/?\)$/.exec(cells[1] ?? '')?.[1];
    const status = statusLabels[cells[2] ?? ''];
    if (!dir || !status) continue;
    entries.set(dir, { status, tested: testedLabels[(cells[5].match(/★/g) ?? []).length] });
  }
  return entries;
}

/** Strategies with their status, from the table in the README. */
export function loadStrategies(): { name: string; basedOn: string; file: string; status: string }[] {
  return readRepoFile('README.md')
    .split('\n')
    .map((line) => line.split('|').map((cell) => cell.trim()))
    .flatMap((cells) => {
      const link = /^\[`([^`]+)`\]\(([^)]+)\)$/.exec(cells[1] ?? '');
      return link ? [{ name: link[1], file: link[2], basedOn: cells[2], status: cells[4] }] : [];
    });
}

/** Markdown for the catalog: one table per category, then the strategies. */
export function indicatorIndex(indicators: Indicator[]): string {
  const catalog = loadCatalog();
  const intro = `Everything in the repository, as it stands. This is a collection of experiments, not a
product range: most indicators are drafts, few have been checked on real charts, and some ideas
will turn out to be wrong. Status and test depth come from the working catalog in the repository
([CATALOG.md](${repoUrl}/blob/main/CATALOG.md)) and change as the scripts do.

Nothing here is investment advice or a recommendation to trade. Trading involves substantial
risk of loss.`;
  const sections = Object.entries(categories as Record<string, string>).map(([category, label]) => {
    const rows = indicators
      .filter((indicator) => indicator.category === category)
      .sort((a, b) => a.title.localeCompare(b.title))
      .map(({ id, dir, title, description, tradingView }) => {
        const entry = catalog.get(dir);
        const name = `[${title}](../../${id}/)${tradingView ? ' ¹' : ''}`;
        const cells = [name, firstSentence(description), entry?.status ?? '–', entry?.tested ?? '–'];
        return `| ${cells.map((cell) => cell.replace(/\|/g, '\\|')).join(' | ')} |`;
      });
    return `## ${label}\n\n| Indicator | What it does | Status | Checked on real charts |\n| --- | --- | --- | --- |\n${rows.join('\n')}`;
  });
  const strategies = loadStrategies().map(
    ({ name, file, basedOn, status }) => `| [${name}](${repoUrl}/blob/main/${file}) | ${basedOn} | ${status} |`,
  );
  return [
    intro,
    ...sections,
    `<small>¹ Also published on TradingView.</small>`,
    `## Strategies\n\nStrategy wrappers for TradingView's Strategy Tester. A backtest describes the past on one symbol and one timeframe; it is no forecast. See [Strategies](../../concepts/strategies/).\n\n| Strategy | Based on | Status |\n| --- | --- | --- |\n${strategies.join('\n')}`,
  ].join('\n\n');
}

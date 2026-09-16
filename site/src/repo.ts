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

/** Markdown for the indicator index: one section per category, one line per indicator. */
export function indicatorIndex(indicators: Indicator[]): string {
  return Object.entries(categories as Record<string, string>)
    .map(([category, label]) => {
      const lines = indicators
        .filter((indicator) => indicator.category === category)
        .sort((a, b) => a.title.localeCompare(b.title))
        .map(({ id, title, description, tradingView }) => {
          const published = tradingView ? ' *(published on TradingView)*' : '';
          return `- [${title}](../../${id}/)${published} — ${firstSentence(description)}`;
        });
      return `## ${label}\n\n${lines.join('\n')}`;
    })
    .join('\n\n');
}

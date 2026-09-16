import { docsSchema } from '@casoon/pages-theme/content';
import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { indicatorIndex, loadIndicators } from './repo';

const docsFolder = glob({ pattern: '**/*.{md,mdx}', base: '../docs' });

// Sources: ../docs for the guides, plus the README in every indicator directory, so each
// indicator is documented in exactly one place.
const docs = defineCollection({
  loader: {
    name: 'pine-scripts-docs',
    load: async (context) => {
      await docsFolder.load(context);
      const { store, parseData, renderMarkdown, generateDigest } = context;
      const indicators = loadIndicators();
      const pages = [
        ...indicators.map(({ id, file, title, description, body }) => ({
          id,
          filePath: `../${file}`,
          data: { title, description },
          body,
        })),
        {
          id: 'getting-started/indicators',
          // Generated; "Edit this page" leads to the generator.
          filePath: '../site/src/repo.ts',
          data: {
            title: 'Indicator index',
            description: 'Every indicator in the repository, grouped as in the sidebar, with the first sentence of its README.',
            order: 3,
          },
          body: indicatorIndex(indicators),
        },
      ];
      for (const { id, filePath, data, body } of pages) {
        store.set({
          id,
          data: await parseData({ id, data }),
          body,
          filePath,
          digest: generateDigest(body),
          rendered: await renderMarkdown(body),
        });
      }
    },
  },
  schema: docsSchema,
});

export const collections = { docs };

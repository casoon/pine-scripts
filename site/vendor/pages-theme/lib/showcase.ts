export interface ShowcaseExample {
  /** URL segment of the detail page. */
  slug: string;
  title: string;
  description?: string;
  /** Source file in the project repository, e.g. "examples/report.ansi". */
  file: string;
  tags?: string[];
  /** What goes in: source, fixture, configuration. */
  input: { code: string; lang?: string };
  /**
   * What comes out: HTML produced at build time by the project's own package.
   * "terminal" renders on the dark terminal surface, "panel" on the page surface (SVG, tables …).
   */
  output: { html: string; kind?: 'terminal' | 'panel' };
  /**
   * Heading the example is listed under on the overview. Examples sharing a group appear together,
   * groups in the order of their first example, with a jump list above them.
   */
  group?: string;
  /**
   * A small preview for the overview, typically a lazily loaded image. With it the overview shows
   * a compact card (title, description, preview, link); input and output stay on the detail page.
   * Suits showcases with many examples.
   */
  preview?: { html: string };
}

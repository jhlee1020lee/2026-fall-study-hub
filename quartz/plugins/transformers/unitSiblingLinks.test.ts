import test from "node:test"
import assert from "node:assert/strict"
import type { Element, Root } from "hast"
import { unified } from "unified"
import { VFile } from "vfile"
import remarkParse from "remark-parse"
import remarkRehype from "remark-rehype"
import { GitHubFlavoredMarkdown } from "@quartz-community/github-flavored-markdown"
import { Latex } from "@quartz-community/latex"
import { ObsidianFlavoredMarkdown } from "@quartz-community/obsidian-flavored-markdown"
import { visit } from "unist-util-visit"
import { CrawlLinks } from "@quartz-community/crawl-links"
import type { BuildCtx } from "../../util/ctx"
import type { FullSlug } from "../../util/path"
import {
  UnitSiblingLinks,
  normalizeTextbookTableCodePipes,
  normalizeTextbookQuestionLiterals,
  normalizeTextbookMultilineDisplays,
  normalizeTextbookHashLiterals,
} from "./unitSiblingLinks"

const base = "courses/computer_architecture/units/"
const graph: Record<string, string[]> = {
  "architecture-contract": ["performance-model"],
  "program-translation-loading": ["architecture-contract", "data-register-memory"],
  "data-register-memory": ["architecture-contract", "instruction-encoding"],
  "instruction-encoding": ["data-register-memory"],
  "control-synchronization": ["data-register-memory", "instruction-encoding"],
  "procedures-stack": ["control-synchronization"],
  "performance-model": ["architecture-contract", "performance-comparison"],
  "performance-comparison": ["performance-model"],
}
const slugs = Object.keys(graph).flatMap((id) => [base + id, base + "en/" + id])

async function render(
  source: string,
  href: string,
  options: { layout?: string; allSlugs?: string[]; crawl?: boolean; baseUrl?: string } = {},
) {
  const context = {
    allSlugs: options.allSlugs ?? slugs,
    cfg: {
      configuration: { baseUrl: options.baseUrl ?? "jhlee1020lee.github.io/2026-fall-study-hub" },
    },
  } as BuildCtx
  const node: Element = {
    type: "element",
    tagName: "a",
    properties: { href },
    children: [{ type: "text", value: "Readable unit label" }],
  }
  const tree: Root = { type: "root", children: [node] }
  const original = `[Readable unit label](${href})`
  const file = new VFile(original)
  file.data.slug = source as FullSlug
  file.data.frontmatter = {
    title: "Unit",
    tags: [],
    note_layout: options.layout ?? "textbook_unit_v1",
  }
  const processor = unified().use(UnitSiblingLinks().htmlPlugins!(context)!)
  if (options.crawl !== false) {
    processor.use(
      CrawlLinks({ markdownLinkResolution: "shortest" }).htmlPlugins!(context as never)!,
    )
  }
  await processor.run(tree, file)
  assert.equal(file.toString(), original, "The source Markdown must remain byte-for-byte unchanged")
  assert.equal(node.children[0].type, "text")
  assert.equal(node.children[0].value, "Readable unit label")
  return node.properties
}

test("all 24 CA sibling references retain their own language with the installed CrawlLinks", async () => {
  let checked = 0
  for (const prefix of [base, base + "en/"]) {
    for (const [source, targets] of Object.entries(graph)) {
      for (const target of targets) {
        const result = await render(prefix + source, target + ".md")
        assert.equal(result["data-slug"], prefix + target)
        checked++
      }
    }
  }
  assert.equal(checked, 24)
})

test("explicit ./ and anchors resolve to the actual sibling, despite cross-course collisions", async () => {
  const result = await render(
    base + "en/architecture-contract",
    "./performance-model.md#CPU%20Time",
    {
      allSlugs: [...slugs, "courses/another_course/units/performance-model"],
    },
  )
  assert.equal(result["data-slug"], base + "en/performance-model")
  assert.ok(String(result.href).endsWith("/en/performance-model#cpu-time"))
})

test("a missing same-language target fails instead of selecting the other language", async () => {
  await assert.rejects(
    render(base + "en/architecture-contract", "performance-model.md", {
      allSlugs: slugs.filter((slug) => slug !== base + "en/performance-model"),
    }),
    /Missing textbook unit sibling/,
  )
})

test("old lecture links retain the existing global shortest behavior", async () => {
  const result = await render(
    "courses/computer_architecture/lectures/en/2026-09-15",
    "performance-model.md",
    {
      layout: "lecture_note_v2",
    },
  )
  assert.equal(result["data-slug"], "performance-model")
  assert.equal(
    (
      await render(base + "architecture-contract", "performance-model.md", {
        layout: "lecture_note_v2",
        crawl: false,
      })
    ).href,
    "performance-model.md",
  )
})

test("a textbook declaration outside the canonical unit path does not expand the scope", async () => {
  for (const source of ["index", base + "index", "courses/computer_architecture/lectures/topic"]) {
    assert.equal(
      (await render(source, "performance-model.md", { crawl: false })).href,
      "performance-model.md",
    )
  }
})

test("external, canonical, parent, absolute, asset and query links are not rewritten", async () => {
  for (const href of [
    "https://example.com/performance-model.md",
    "//example.com/performance-model.md",
    "mailto:student@example.com",
    "javascript:alert(1)",
    "../performance-model.md",
    "/performance-model.md",
    "en/performance-model.md",
    "#local-heading",
    base + "performance-model",
    "performance-model.pdf",
    "performance-model.md?download=1",
    "performance%2Dmodel.md",
    "index.md",
    "performance-model\\.md",
  ]) {
    assert.equal((await render(base + "architecture-contract", href, { crawl: false })).href, href)
  }
})

const site = "https://jhlee1020lee.github.io/2026-fall-study-hub/"
const sourcePage = "page_cache/computer_architecture/lec.03/page-014"

test("absolute same-course source pages become actual internal popover links in both languages", async () => {
  for (const language of ["", "en/"]) {
    const result = await render(base + language + "data-register-memory", site + sourcePage, {
      allSlugs: [...slugs, sourcePage],
    })
    assert.equal(result["data-slug"], sourcePage)
    assert.ok((result.className as string[]).includes("internal"))
    assert.ok(!(result.className as string[]).includes("external"))
    const resolved = new URL(String(result.href), site + base + language + "data-register-memory")
    assert.equal(resolved.href, site + sourcePage)
  }
})

test("source page fragments survive the installed CrawlLinks and missing source pages fail", async () => {
  const result = await render(base + "data-register-memory", site + sourcePage + "#Page%2014", {
    allSlugs: [...slugs, sourcePage],
  })
  assert.equal(result["data-slug"], sourcePage)
  assert.ok(String(result.href).endsWith("#page-14"))
  await assert.rejects(
    render(base + "data-register-memory", site + sourcePage),
    /Missing textbook source page/,
  )
})

test("source normalization preserves external sites, other courses, assets and legacy pages", async () => {
  const unchanged = [
    site.replace("https:", "http:") + sourcePage,
    site.replace("jhlee1020lee", "someoneelse") + sourcePage,
    site.replace("study-hub/", "study-hub-copy/") + sourcePage,
    site.replace("https://", "https://user:password@") + sourcePage,
    site + sourcePage + "?download=1",
    site + sourcePage.replace("computer_architecture", "computer_programming"),
    site + sourcePage.replace("page-014", "manifest.json"),
    site + "materials/computer_architecture/lec.03.pdf",
  ]
  for (const href of unchanged) {
    assert.equal((await render(base + "data-register-memory", href, { crawl: false })).href, href)
  }
  for (const source of [base + "index", "courses/computer_architecture/lectures/topic"]) {
    assert.equal(
      (await render(source, site + sourcePage, { crawl: false })).href,
      site + sourcePage,
    )
  }
  assert.equal(
    (
      await render(base + "data-register-memory", site + sourcePage, {
        layout: "content_first_v1",
        crawl: false,
      })
    ).href,
    site + sourcePage,
  )
})

const unitHeader = [
  "---",
  'note_layout: "textbook_unit_v1"',
  'source_kind: "unit_chapter"',
  'course: "system_programming"',
  'unit_id: "c-fundamentals"',
  'lang: "ko"',
  "---",
  "",
].join("\n")
const operatorTable =
  "| Category | Operators | Meaning |\n| --- | --- | --- |\n| Logical | `&& || !` | short circuit |\n"

function parsedTable(source: string) {
  const body = source.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, "")
  const tree = unified()
    .use(remarkParse)
    .use(GitHubFlavoredMarkdown({ enableSmartyPants: false }).markdownPlugins!({} as never)!)
    .parse(body)
  const rows: number[] = []
  const code: string[] = []
  visit(tree, "tableRow", (row) => rows.push(row.children.length))
  visit(tree, "inlineCode", (node) => code.push(node.value))
  return { rows, code }
}

test("actual installed GFM keeps all three cells and exact logical code text", () => {
  for (const lang of ["ko", "en"]) {
    const source = unitHeader.replace('lang: "ko"', `lang: "${lang}"`) + operatorTable
    assert.ok(
      !parsedTable(source).code.includes("&& || !"),
      "regression fixture must be broken without the transform",
    )
    const rendered = UnitSiblingLinks().textTransform!({} as BuildCtx, source)
    assert.deepEqual(parsedTable(rendered), { rows: [3, 3], code: ["&& || !"] })
    assert.equal(source, unitHeader.replace('lang: "ko"', `lang: "${lang}"`) + operatorTable)
    assert.equal(rendered, source.replace("`&& || !`", "`&& \\|\\| !`"))
  }
})

test("table code escaping is idempotent and keeps existing escapes and multiple backtick spans", () => {
  const table = "| A | B | C |\n| --- | --- | --- |\n| `x\\|y` | ``a` | b`` | `c|d` |\n"
  const source = unitHeader + table
  const rendered = normalizeTextbookTableCodePipes(source)
  assert.deepEqual(parsedTable(rendered), { rows: [3, 3], code: ["x|y", "a` | b", "c|d"] })
  assert.equal(normalizeTextbookTableCodePipes(rendered), rendered)
  assert.ok(rendered.includes("`x\\|y`"))
  assert.equal(
    normalizeTextbookTableCodePipes(rendered.replaceAll("\n", "\r\n")),
    rendered.replaceAll("\n", "\r\n"),
  )
})

test("only actual table rows change; fences, indented code, raw HTML and prose remain exact", () => {
  for (const body of [
    "```markdown\n" + operatorTable + "```\n",
    "~~~\n" + operatorTable + "~~~\n",
    operatorTable
      .split("\n")
      .map((line) => "    " + line)
      .join("\n"),
    "<pre>\n" + operatorTable + "</pre>\n",
    "<!--\n" + operatorTable + "-->\n",
    "Outside a table: `&& || !`\n\n| ordinary | prose `a|b` |\n",
    "| Broken `a|b` | B |\n| --- | --- |\n| row | cell |\n",
    "| A | B | C |\n| --- | --- | --- |\n| unclosed `a|b | c |\n",
  ]) {
    assert.equal(normalizeTextbookTableCodePipes(unitHeader + body), unitHeader + body)
  }
  const mixed = unitHeader + "```\n" + operatorTable + "```\n\n" + operatorTable
  assert.equal(
    normalizeTextbookTableCodePipes(mixed),
    mixed.slice(0, -operatorTable.length) + operatorTable.replace("||", "\\|\\|"),
  )
})

test("legacy notes, missing identity and malformed frontmatter never opt into table normalization", () => {
  for (const header of [
    "",
    unitHeader.replace("textbook_unit_v1", "lecture_note_v2"),
    unitHeader.replace("unit_chapter", "lecture"),
    unitHeader.replace('unit_id: "c-fundamentals"', 'unit_id: "index"'),
    unitHeader.replace('course: "system_programming"', 'course: "../escape"'),
    unitHeader.replace('lang: "ko"', 'lang: "fr"'),
    unitHeader.replace('lang: "ko"', "lang: ["),
    unitHeader.replace('note_layout: "textbook_unit_v1"', 'other: "textbook_unit_v1"'),
  ]) {
    assert.equal(normalizeTextbookTableCodePipes(header + operatorTable), header + operatorTable)
  }
})

function questionSource(lang: string, unit: string, question: string, body: string) {
  const header = unitHeader
    .replace('unit_id: "c-fundamentals"', `unit_id: "${unit}"`)
    .replace('lang: "ko"', `lang: "${lang}"`)
  const heading = lang === "ko" ? "## 확인·연습문제" : "## Recall and Practice"
  const label = lang === "ko" ? "확인" : "Recall"
  return header + `${heading}\n\n### Recall\n\n#### ${label} ${question} · Syntax\n\n${body}\n`
}

function parsedQuestion(source: string) {
  const body = source.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, "")
  const tree = unified()
    .use(remarkParse)
    .use(GitHubFlavoredMarkdown({ enableSmartyPants: false }).markdownPlugins!({} as never)!)
    .parse(body)
  const paragraphs: string[] = []
  const code: string[] = []
  let emphasis = 0
  let strong = 0
  visit(tree, "paragraph", (paragraph) => {
    let text = ""
    visit(paragraph, (node) => {
      if (node.type === "text" || node.type === "inlineCode") text += node.value
    })
    paragraphs.push(text)
  })
  visit(tree, "inlineCode", (node) => {
    code.push(node.value)
  })
  visit(tree, "emphasis", () => {
    emphasis++
  })
  visit(tree, "strong", () => {
    strong++
  })
  return { paragraphs, code, emphasis, strong }
}

test("installed GFM preserves complete syntax prompts in the seven affected language/question contexts", () => {
  const fixtures = [
    ["ko", "state-machines", "Q04", "Literal 내부 /*...*/는 문자다."],
    ["ko", "files-metadata", "Q08", "DIR*는 FILE*와 다르다."],
    ["ko", "io-streams", "Q06", "FILE*와 fd/DIR*를 비교하라."],
    ["ko", "dirtree", "Q06", "?, *, ()와 a(bc)*d, ab?(de)*f, abc?d*(ef)를 비교하라. d*0과 d*2다."],
    ["en", "dirtree", "Q06", "Explain ?, *, (), a(bc)*d, ab?(de)*f and abc?d*(ef), with d* zero."],
    ["ko", "dirtree", "Q07", "*abc, a**b, a*b와 a(b*c)d를 비교하라."],
    ["en", "dirtree", "Q07", "Compare *abc, a**b, a*b and a(b*c)d."],
  ]
  for (const [lang, unit, question, text] of fixtures) {
    const source = questionSource(lang, unit, question, text)
    assert.notDeepEqual(parsedQuestion(source).paragraphs, [text], "fixture must exhibit GFM loss")
    const rendered = UnitSiblingLinks().textTransform!({} as BuildCtx, source)
    assert.deepEqual(parsedQuestion(rendered), {
      paragraphs: [text],
      code: unit === "state-machines" ? ["/*...*/"] : [],
      emphasis: 0,
      strong: 0,
    })
    assert.equal(normalizeTextbookQuestionLiterals(rendered), rendered)
    assert.equal(
      normalizeTextbookQuestionLiterals(source.replaceAll("\n", "\r\n")),
      rendered.replaceAll("\n", "\r\n"),
    )
  }
})

test("solution paragraphs inside details preserve C comments and exact existing inline code", () => {
  const body = [
    "Read the literal.",
    "",
    "<details><summary>Show solution</summary>",
    "",
    "Literal 내부 /*...*/는 문자다. `/*...*/`와 ``a`/*...*/b``는 그대로다.",
    "",
    "</details>",
  ].join("\n")
  const source = questionSource("ko", "state-machines", "Q04", body)
  const rendered = normalizeTextbookQuestionLiterals(source)
  assert.deepEqual(parsedQuestion(rendered), {
    paragraphs: [
      "Read the literal.",
      "Literal 내부 /*...*/는 문자다. /*...*/와 a`/*...*/b는 그대로다.",
    ],
    code: ["/*...*/", "/*...*/", "a`/*...*/b"],
    emphasis: 0,
    strong: 0,
  })
  assert.equal(rendered, source.replace("내부 /*...*/", "내부 `/*...*/`"))
  assert.ok(rendered.includes("<details><summary>Show solution</summary>"))
})

test("the actual GFM and remark-rehype chain preserves comment dots with SmartyPants enabled", async () => {
  const source = questionSource(
    "ko",
    "state-machines",
    "Q04",
    "<details><summary>해설</summary>\n\nLiteral /*...*/와 *emphasis*를 보존한다.\n\n</details>",
  )
  const rendered = normalizeTextbookQuestionLiterals(source).replace(/^---\n[\s\S]*?\n---\n/, "")
  const processor = unified()
    .use(remarkParse)
    .use(GitHubFlavoredMarkdown({ enableSmartyPants: true }).markdownPlugins!({} as never)!)
    .use(remarkRehype, { allowDangerousHtml: true })
  const tree = await processor.run(processor.parse(rendered))
  const paragraphs: string[] = []
  visit(tree, "element", (node) => {
    if (node.tagName !== "p") return
    let text = ""
    visit(node, "text", (child) => {
      text += child.value
    })
    paragraphs.push(text)
  })
  assert.deepEqual(paragraphs, ["Literal /*...*/와 emphasis를 보존한다."])
})

test("POP Q01 preserves multiplication in its folded solution without changing other courses or math", () => {
  const source = questionSource(
    "ko",
    "higher-order-functions",
    "Q01",
    "<details><summary>해설</summary>\n\n항 n, n*n, n*n*n을 비교한다.\n\n</details>",
  ).replace("system_programming", "principles_of_programming")
  assert.notDeepEqual(parsedQuestion(source).paragraphs, ["항 n, n*n, n*n*n을 비교한다."])
  const rendered = normalizeTextbookQuestionLiterals(source)
  assert.deepEqual(parsedQuestion(rendered).paragraphs, ["항 n, n*n, n*n*n을 비교한다."])
  assert.equal(normalizeTextbookQuestionLiterals(rendered), rendered)
  for (const other of [
    source.replace("principles_of_programming", "system_programming"),
    source.replace('lang: "ko"', 'lang: "en"'),
    source.replace("#### 확인 Q01", "#### 확인 Q02"),
  ]) {
    assert.equal(normalizeTextbookQuestionLiterals(other), other)
  }
  const math = questionSource(
    "ko",
    "matrices-and-linear-maps",
    "Q01",
    "$$(A+B)_{ij}=a_{ij}+b_{ij}.$$",
  ).replace("system_programming", "discrete_mathematics")
  assert.equal(normalizeTextbookQuestionLiterals(math), math)
})

test("intentional emphasis, code and unrelated syntax retain their original meaning", () => {
  const source = questionSource(
    "ko",
    "files-metadata",
    "Q08",
    "**Important** *emphasis* and *FILE*; DIR*는 FILE*와 다르다. `FILE* DIR*` and XFILE* stay.",
  )
  const rendered = normalizeTextbookQuestionLiterals(source)
  assert.deepEqual(parsedQuestion(rendered), {
    paragraphs: ["Important emphasis and FILE; DIR*는 FILE*와 다르다. FILE* DIR* and XFILE* stay."],
    code: ["FILE* DIR*"],
    emphasis: 2,
    strong: 1,
  })
  assert.ok(rendered.includes("**Important** *emphasis* and *FILE*"))
  assert.ok(rendered.includes("XFILE*"))
})

test("literal normalization requires the exact course, unit, language and actual recall heading", () => {
  const source = questionSource("ko", "files-metadata", "Q08", "DIR*는 FILE*와 다르다.")
  for (const outOfScope of [
    source.replace("textbook_unit_v1", "lecture_note_v2"),
    source.replace("unit_chapter", "lecture"),
    source.replace("system_programming", "computer_programming"),
    source.replace('unit_id: "files-metadata"', 'unit_id: "index"'),
    source.replace('lang: "ko"', 'lang: "en"'),
    source.replace('lang: "ko"', "lang: [ko]"),
    source.replace('unit_id: "files-metadata"', "unit_id: [files-metadata]"),
    source.replace('lang: "ko"', "lang: ["),
    source.replace("## 확인·연습문제", "## 본문"),
    source.replace("#### 확인 Q08", "#### 확인 Q09"),
    source.replace("#### 확인 Q08", "#### 연습 Q08"),
    source.replace("#### 확인 Q08", "### 확인 Q08"),
    source.replace("DIR*는", "## 출처\n\nDIR*는"),
    source.replace("DIR*는", "### 다른 문단\n\nDIR*는"),
    "```markdown\n" + source + "```\n",
  ]) {
    assert.equal(normalizeTextbookQuestionLiterals(outOfScope), outOfScope)
  }
})

test("fenced examples, raw HTML, math, links and nested fake headings are untouched", () => {
  for (const body of [
    "```c\nDIR*는 FILE*와 다르다.\n```",
    "~~~\nDIR*는 FILE*와 다르다.\n~~~",
    "    DIR*는 FILE*와 다르다.",
    "<!-- DIR*는 FILE*와 다르다. -->",
    '<pre data-label="DIR* FILE*">DIR*는 FILE*와 다르다.</pre>',
    'Before <span data-label="DIR* FILE*">DIR*는 FILE*와 다르다.</span>',
    "$DIR* FILE*$ and $$DIR* FILE*$$",
    "`DIR* FILE*` and [DIR*는 FILE*](https://example.test/FILE*DIR*)",
  ]) {
    const source = questionSource("ko", "files-metadata", "Q08", body)
    assert.equal(normalizeTextbookQuestionLiterals(source), source)
  }
  const nested = questionSource(
    "ko",
    "files-metadata",
    "Q09",
    "> #### 확인 Q08 · Syntax\n>\n> DIR*는 FILE*와 다르다.",
  )
  assert.equal(normalizeTextbookQuestionLiterals(nested), nested)
})

const bezoutHeader = unitHeader
  .replace("system_programming", "discrete_mathematics")
  .replace("c-fundamentals", "gcd-euclid-and-bezout")
const bezoutPayloads = [
  String.raw`\begin{aligned}
252&=198\cdot1+54,\\
198&=54\cdot3+36,\\
54&=36\cdot1+18,\\
36&=18\cdot2+0.
\end{aligned}`,
  String.raw`\begin{aligned}
18&=54-36\\
&=54-(198-3\cdot54)\\
&=4\cdot54-198\\
&=4(252-198)-198\\
&=4\cdot252-5\cdot198.
\end{aligned}`,
]
const bezoutDisplays = bezoutPayloads.map((payload) => "$$" + payload + "$$").join("\n\n")
const afterBezout = [
  "## 확인·연습문제",
  "",
  "#### 확인 Q01 · GCD",
  "",
  "Explain the invariant.",
  "",
  "<details><summary>해설 보기</summary>",
  "",
  "The answer remains a separate paragraph.",
  "",
  "</details>",
  "",
  "## 출처",
].join("\n")

function parsedDisplays(source: string) {
  const body = source.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, "")
  const tree = unified()
    .use(remarkParse)
    .use(GitHubFlavoredMarkdown({ enableSmartyPants: false }).markdownPlugins!({} as never)!)
    .use(Latex().markdownPlugins!({} as never)!)
    .parse(body)
  const math: string[] = []
  const headings: string[] = []
  const html: string[] = []
  const paragraphs: string[] = []
  visit(tree, (node) => {
    // The installed Latex package bundles remark-math but exposes no mdast augmentation.
    const mathNode = node as { type: string; value?: string }
    if (mathNode.type === "math" && typeof mathNode.value === "string") math.push(mathNode.value)
    if (node.type === "html") html.push(node.value)
    if (node.type === "heading" || node.type === "paragraph") {
      let text = ""
      visit(node, "text", (child) => {
        text += child.value
      })
      if (node.type === "heading") headings.push(text)
      else paragraphs.push(text)
    }
  })
  return { math, headings, html, paragraphs }
}

test("installed GFM and Latex close both reviewed aligned blocks before recall and details", () => {
  const source = bezoutHeader + bezoutDisplays + "\n\n" + afterBezout
  const before = parsedDisplays(source)
  assert.equal(before.math.length, 1)
  assert.ok(before.math[0].includes("<details>"), "fixture must exhibit the unclosed display bug")
  assert.deepEqual(before.headings, [])
  const rendered = UnitSiblingLinks().textTransform!({} as BuildCtx, source)
  assert.equal(
    rendered,
    bezoutHeader +
      bezoutPayloads.map((payload) => "$$\n" + payload + "\n$$").join("\n\n") +
      "\n\n" +
      afterBezout,
  )
  assert.deepEqual(parsedDisplays(rendered), {
    math: bezoutPayloads,
    headings: ["확인·연습문제", "확인 Q01 · GCD", "출처"],
    html: ["<details><summary>해설 보기</summary>", "</details>"],
    paragraphs: ["Explain the invariant.", "The answer remains a separate paragraph."],
  })
  assert.equal(normalizeTextbookMultilineDisplays(rendered), rendered)
  assert.equal(
    normalizeTextbookMultilineDisplays(source.replaceAll("\n", "\r\n")),
    rendered.replaceAll("\n", "\r\n"),
  )
  assert.equal(source, bezoutHeader + bezoutDisplays + "\n\n" + afterBezout)
})

test("aligned display normalization requires exact unit identity and the two exact math payloads", () => {
  const source = bezoutHeader + bezoutDisplays
  for (const other of [
    source.replace("textbook_unit_v1", "lecture_note_v2"),
    source.replace("unit_chapter", "lecture"),
    source.replace("discrete_mathematics", "principles_of_programming"),
    source.replace("gcd-euclid-and-bezout", "other-unit"),
    source.replace('lang: "ko"', 'lang: "en"'),
    source.replace('lang: "ko"', "lang: ["),
    bezoutDisplays,
    bezoutHeader + "$$" + bezoutPayloads[0].replace("252", "253") + "$$",
    bezoutHeader + "$$x=y$$",
    bezoutHeader + "$$\nx=y\n$$",
  ]) {
    assert.equal(normalizeTextbookMultilineDisplays(other), other)
  }
})

test("the reviewed two-line series keeps its full math payload and its exact unit boundary", () => {
  const payload = String.raw`\sum_{k=0}^{\infty}x^k=\frac1{1-x},\qquad
\sum_{k=1}^{\infty}kx^{k-1}=\frac1{(1-x)^2}`
  const header = bezoutHeader.replace("gcd-euclid-and-bezout", "sets-functions-sequences")
  const source = header + "$$" + payload + "$$\n\n" + afterBezout
  assert.ok(parsedDisplays(source).math[0].includes("<details>"))
  const rendered = normalizeTextbookMultilineDisplays(source)
  assert.equal(rendered, header + "$$\n" + payload + "\n$$\n\n" + afterBezout)
  assert.deepEqual(parsedDisplays(rendered).math, [payload])
  assert.deepEqual(parsedDisplays(rendered).headings, ["확인·연습문제", "확인 Q01 · GCD", "출처"])
  assert.equal(
    normalizeTextbookMultilineDisplays(
      source.replace("sets-functions-sequences", "gcd-euclid-and-bezout"),
    ),
    source.replace("sets-functions-sequences", "gcd-euclid-and-bezout"),
  )
})

test("aligned displays inside code, HTML, nested examples or surrounding prose remain unchanged", () => {
  for (const body of [
    "```latex\n" + bezoutDisplays + "\n```",
    "~~~\n" + bezoutDisplays + "\n~~~",
    bezoutDisplays
      .split("\n")
      .map((line) => "    " + line)
      .join("\n"),
    bezoutDisplays
      .split("\n")
      .map((line) => "> " + line)
      .join("\n"),
    "<pre>\n" + bezoutDisplays + "\n</pre>",
    "<!--\n" + bezoutDisplays + "\n-->",
    "`$$" + bezoutPayloads[0] + "$$`",
    "Before $$" + bezoutPayloads[0] + "$$ after.",
  ]) {
    const source = bezoutHeader + body
    assert.equal(normalizeTextbookMultilineDisplays(source), source)
  }
})

const hashParagraphFixtures = [
  [
    "ko",
    "memory-layout",
    false,
    "INFO(double)가 char dummy 뒤 data를 둔 struct를 만들 때 SIZE, #t, OFS는 무엇을 계산하는가? x86-64와 IA32의 offset·padding을 구하라.",
  ],
  [
    "ko",
    "memory-layout",
    true,
    "SIZE는 sizeof(type), #t는 macro 인자 이름의 stringification, OFS는 data 주소−struct 시작 주소다. X86-64에서 dummy1 뒤 data offset 8이므로 padding7, IA32 Linux에서는 offset 4·padding3이고 double size는 여전히8이다. Offset·size를 섞으면 alignment를 잘못 읽는다. 원문의 unsigned long 주소 cast와 예제 main 표기는 target 의존 측정 code의 한계이며 여기서 실행한 결과가 아니다.",
  ],
  [
    "en",
    "memory-layout",
    false,
    "For INFO(double), a struct places double data after char dummy. Explain SIZE, #t, OFS and calculate offsets/padding on both targets.",
  ],
  [
    "en",
    "memory-layout",
    true,
    "SIZE is sizeof(type); #t stringifies the macro argument; OFS subtracts struct start from data’s address. On x86-64, data starts at 8 after a one-byte dummy, giving 7 padding bytes. IA32 Linux uses offset 4, padding3 while double remains8 bytes. Do not confuse offset and size. The source’s unsigned-long address casts and main spelling limit portability; these are not newly executed measurements.",
  ],
  [
    "ko",
    "dirtree",
    true,
    "Root는depth 0, 유효 limit 1..20, default 20이다. `-d 1`은 b:0 files/1 directory, 4096/8; `-d 2`는 b, c, f:1/2, 8192/16; `-d 3`는 여기에 d:1/3, 12288/24; 전체는2/4, 16384/32다. Limit을 넘으면 출력뿐 아니라 순회·통계에서도 제외한다. Depth 2의 c를 표시하는 것과 그 자식 방문은 다르다. 그림 #depth 문구는 출력이 아니다. 녹취의 root0 뒤 root2 상충은 명세의0으로 계산하되 불명확한 발화를 복구했다고 하지 않는다.",
  ],
  [
    "en",
    "dirtree",
    true,
    "Root depth 0; valid limits 1..20, default 20. `-d 1` includes b:0 files/1 directory, 4096/8; `-d 2` adds c/f:1/2, 8192/16; `-d 3` adds d:1/3, 12288/24; full tree:2/4, 16384/32. Beyond-limit entries are excluded from traversal and totals, not just display. Showing c at depth 2 does not visit its children. Diagram #depth annotations are not output. Use formal depth 0 while retaining the transcript’s conflicting0/2 wording as uncertain.",
  ],
] as const

async function renderedHashParagraph(source: string) {
  const body = source.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, "")
  const context = { allSlugs: [] } as unknown as BuildCtx
  const file = new VFile(body)
  file.data.slug = "courses/system_programming/units/memory-layout" as FullSlug
  file.data.frontmatter = { title: "Hash literal", tags: [] }
  const ofm = ObsidianFlavoredMarkdown()
  const processor = unified()
    .use(remarkParse)
    .use(ofm.markdownPlugins!(context as never)!)
    .use(GitHubFlavoredMarkdown().markdownPlugins!(context as never)!)
    .use(Latex().markdownPlugins!(context as never)!)
    .use(remarkRehype, { allowDangerousHtml: true })
    .use(ofm.htmlPlugins!(context as never)!)
  const tree = await processor.run(processor.parse(file), file)
  const paragraphs: string[] = []
  const tagLinks: string[] = []
  visit(tree, "element", (node) => {
    if (node.tagName === "a" && String(node.properties.href).includes("/tags/")) {
      tagLinks.push(String(node.properties.href))
    }
    if (node.tagName === "p") {
      let text = ""
      visit(node, "text", (child) => {
        text += child.value
      })
      paragraphs.push(text)
    }
  })
  return { paragraphs, tagLinks, tags: file.data.frontmatter.tags }
}

test("installed OFM/GFM keeps all six complete Q04 paragraphs and literal hashes without tag links", async () => {
  for (const [lang, unit, folded, paragraph] of hashParagraphFixtures) {
    const body = folded
      ? `<details><summary>Solution</summary>\n\n${paragraph}\n\n</details>`
      : paragraph
    const source = questionSource(lang, unit, "Q04", body)
    const before = await renderedHashParagraph(source)
    assert.equal(before.tagLinks.length, 1, "the exact fixture must produce the false tag")
    const rendered = UnitSiblingLinks().textTransform!({} as BuildCtx, source)
    assert.equal(
      rendered,
      source.replace(/#(?:depth|t)/g, (literal) => "\\" + literal),
    )
    assert.deepEqual(await renderedHashParagraph(rendered), {
      paragraphs: [paragraph.replace(/`([^`]+)`/g, "$1")],
      tagLinks: [],
      tags: [],
    })
    assert.equal(normalizeTextbookHashLiterals(rendered), rendered)
    assert.equal(
      normalizeTextbookHashLiterals(source.replaceAll("\n", "\r\n")),
      rendered.replaceAll("\n", "\r\n"),
    )
  }
})

test("hash normalization requires the exact paragraph, unit, course, language and Q04 boundary", () => {
  const paragraph = hashParagraphFixtures[0][3]
  const source = questionSource("ko", "memory-layout", "Q04", paragraph)
  for (const other of [
    source.replace("textbook_unit_v1", "lecture_note_v2"),
    source.replace("unit_chapter", "lecture"),
    source.replace("system_programming", "computer_programming"),
    source.replace("memory-layout", "dirtree"),
    source.replace('lang: "ko"', 'lang: "en"'),
    source.replace('lang: "ko"', "lang: ["),
    source.replace("## 확인·연습문제", "## 본문"),
    source.replace("#### 확인 Q04", "#### 확인 Q05"),
    source.replace("INFO(double)", "INFO(float)"),
    source.replace(paragraph, "This is an intentional #tag."),
    source.replace(paragraph, "`#t` is already code."),
    source.replace(paragraph, "[#t](https://example.test/#t)"),
  ])
    assert.equal(normalizeTextbookHashLiterals(other), other)
})

test("the same hash paragraph inside code, raw HTML or a nested example stays unchanged", () => {
  const paragraph = hashParagraphFixtures[0][3]
  for (const body of [
    "```c\n" + paragraph + "\n```",
    "    " + paragraph,
    "> " + paragraph,
    "<!--\n" + paragraph + "\n-->",
    "<pre>\n" + paragraph + "\n</pre>",
    "`" + paragraph + "`",
  ]) {
    const source = questionSource("ko", "memory-layout", "Q04", body)
    assert.equal(normalizeTextbookHashLiterals(source), source)
  }
})

import path from "node:path"
import { createHash } from "node:crypto"
import { parse as parseYaml } from "yaml"
import { unified } from "unified"
import remarkParse from "remark-parse"
import { GitHubFlavoredMarkdown } from "@quartz-community/github-flavored-markdown"
import { visit } from "unist-util-visit"
import type { QuartzTransformerPlugin } from "../types"

const unitSlug = /^courses\/[a-z][a-z0-9_]*\/units\/(?:en\/)?[a-z0-9]+(?:-[a-z0-9]+)*$/
const siblingMarkdown = /^(?:\.\/)?([a-z0-9]+(?:-[a-z0-9]+)*)\.md(#[^\s?]*)?$/

/** Keep an existing same-course source page inside the site's link pipeline. */
function sourcePageLink(href: string, baseUrl: string | undefined, course: string): string | null {
  if (!baseUrl || !href.startsWith("https://")) return null
  try {
    const base = new URL(`https://${baseUrl.replace(/\/+$/, "")}/`)
    const url = new URL(href)
    if (
      url.origin !== base.origin ||
      url.username ||
      url.password ||
      url.search ||
      !url.pathname.startsWith(base.pathname)
    )
      return null
    const target = decodeURIComponent(url.pathname.slice(base.pathname.length))
    if (!target.startsWith(`page_cache/${course}/`) || !/\/page-\d{3}$/.test(target)) return null
    return target + url.hash
  } catch {
    return null
  }
}

const tableParser = unified()
  .use(remarkParse)
  .use(GitHubFlavoredMarkdown({ enableSmartyPants: false }).markdownPlugins!({} as never)!)

function escapedAt(text: string, at: number): boolean {
  let slashes = 0
  while (at > 0 && text[--at] === "\\") slashes++
  return slashes % 2 === 1
}

function escapeCodePipes(row: string): string {
  const runs = [...row.matchAll(/`+/g)]
  let result = ""
  let copied = 0
  for (let i = 0; i < runs.length; i++) {
    const open = runs[i]
    if (escapedAt(row, open.index)) continue
    const closeIndex = runs.findIndex((run, j) => j > i && run[0].length === open[0].length)
    if (closeIndex < 0) continue
    const close = runs[closeIndex]
    const start = open.index + open[0].length
    const code = row.slice(start, close.index)
    result += row.slice(copied, start)
    result += code.replace(/\|/g, (pipe, at: number) => (escapedAt(code, at) ? pipe : "\\|"))
    copied = close.index
    i = closeIndex
  }
  return result + row.slice(copied)
}

/** Rendering-only: raw pipes inside code spans otherwise split GFM table cells. */
export function normalizeTextbookTableCodePipes(src: string): string {
  const header = /^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/.exec(src)
  if (!header) return src
  let metadata: Record<string, unknown>
  try {
    metadata = parseYaml(header[1])
  } catch {
    return src
  }
  // textTransform runs before VFile path/frontmatter assignment. Require the
  // full unit identity here; publication validation still enforces its path.
  if (
    !metadata ||
    metadata.note_layout !== "textbook_unit_v1" ||
    metadata.source_kind !== "unit_chapter" ||
    !/^[a-z][a-z0-9_]*$/.test(String(metadata.course ?? "")) ||
    !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(String(metadata.unit_id ?? "")) ||
    metadata.unit_id === "index" ||
    !["ko", "en"].includes(String(metadata.lang))
  )
    return src

  const body = src.slice(header[0].length)
  const edits: { start: number; end: number; value: string }[] = []
  visit(tableParser.parse(body), "tableRow", (row) => {
    const start = row.position?.start.offset
    const end = row.position?.end.offset
    if (start === undefined || end === undefined) return
    const original = body.slice(start, end)
    const value = escapeCodePipes(original)
    if (value !== original) edits.push({ start, end, value })
  })
  let renderedBody = body
  for (const edit of edits.reverse()) {
    renderedBody = renderedBody.slice(0, edit.start) + edit.value + renderedBody.slice(edit.end)
  }
  return header[0] + renderedBody
}

// These questions contain literal C/pattern/arithmetic syntax that GFM mistakes for
// emphasis. Keep the repair tied to the reviewed unit/language/question, not
// full sentences or source locators that may legitimately change in a revision.
const questionLiterals: Record<string, Record<string, readonly string[]>> = {
  "system_programming/ko/state-machines": { Q04: ["/*...*/"] },
  "system_programming/ko/files-metadata": { Q08: ["FILE*", "DIR*"] },
  "system_programming/ko/io-streams": { Q06: ["FILE*", "DIR*"] },
  "system_programming/ko/dirtree": {
    Q06: ["a(bc)*d", "ab?(de)*f", "abc?d*(ef)", "d*", "*"],
    Q07: ["*abc", "a**b", "a*b", "a(b*c)d"],
  },
  "system_programming/en/dirtree": {
    Q06: ["a(bc)*d", "ab?(de)*f", "abc?d*(ef)", "d*", "*"],
    Q07: ["*abc", "a**b", "a*b", "a(b*c)d"],
  },
  "principles_of_programming/ko/higher-order-functions": { Q01: ["n*n*n", "n*n"] },
}

/** Rendering-only: preserve known literal stars in specific recall paragraphs. */
export function normalizeTextbookQuestionLiterals(src: string): string {
  const header = /^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/.exec(src)
  if (!header) return src
  let metadata: Record<string, unknown>
  try {
    metadata = parseYaml(header[1])
  } catch {
    return src
  }
  if (
    !metadata ||
    metadata.note_layout !== "textbook_unit_v1" ||
    metadata.source_kind !== "unit_chapter" ||
    typeof metadata.course !== "string" ||
    !["ko", "en"].includes(String(metadata.lang)) ||
    typeof metadata.lang !== "string" ||
    typeof metadata.unit_id !== "string"
  )
    return src
  const questions = questionLiterals[`${metadata.course}/${metadata.lang}/${metadata.unit_id}`]
  if (!questions) return src

  const body = src.slice(header[0].length)
  const tree = tableParser.parse(body)
  const recallHeading = metadata.lang === "ko" ? "## 확인·연습문제" : "## Recall and Practice"
  const questionHeading =
    metadata.lang === "ko" ? /^#### 확인 (Q\d{2}) · / : /^#### Recall (Q\d{2}) · /
  let inRecall = false
  let literals: readonly string[] = []
  const insertions = new Map<number, string>()
  for (const node of tree.children) {
    const start = node.position?.start.offset
    const end = node.position?.end.offset
    if (start === undefined || end === undefined) continue
    const original = body.slice(start, end)
    if (node.type === "heading") {
      if (node.depth <= 2) inRecall = original === recallHeading
      literals = inRecall ? (questions[questionHeading.exec(original)?.[1] ?? ""] ?? []) : []
      continue
    }
    if (!inRecall || literals.length === 0 || node.type !== "paragraph") continue
    // None of the affected paragraphs contains math or inline HTML. Decline
    // such mixed contexts rather than adding a second HTML/LaTeX parser here.
    if (original.includes("$") || node.children.some((child) => child.type === "html")) continue

    // Actual paragraph nodes also cover blank-line-separated solution text
    // inside <details>. Never modify code, links, math or raw HTML/attributes.
    const protectedRanges: [number, number][] = []
    visit(node, (child) => {
      if (
        [
          "inlineCode",
          "html",
          "link",
          "linkReference",
          "image",
          "imageReference",
          "inlineMath",
        ].includes(child.type) &&
        child.position?.start.offset !== undefined &&
        child.position?.end.offset !== undefined
      ) {
        protectedRanges.push([child.position.start.offset, child.position.end.offset])
      }
    })
    const pattern = new RegExp(
      literals.map((literal) => literal.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|"),
      "g",
    )
    for (const match of original.matchAll(pattern)) {
      const at = start + match.index
      const after = at + match[0].length
      if (protectedRanges.some(([a, b]) => at < b && after > a)) continue
      const beforeChar = body[at - 1] ?? ""
      const afterChar = body[after] ?? ""
      if (match[0] === "*") {
        // Only the standalone grammar operator; never emphasis delimiters.
        if (!/[\s,;]/.test(beforeChar) || !/[,\s는]/.test(afterChar)) continue
      } else if (/[A-Za-z0-9_*]/.test(beforeChar) || /[A-Za-z_]/.test(afterChar)) {
        continue
      }
      if (match[0] === "/*...*/") {
        // Code also protects the three literal dots from SmartyPants' ellipsis.
        insertions.set(at, "`")
        insertions.set(after, "`")
        continue
      }
      for (let i = at; i < after; i++) {
        if (body[i] === "*" && !escapedAt(body, i)) insertions.set(i, "\\")
      }
    }
  }
  let renderedBody = body
  for (const [at, value] of [...insertions].sort(([a], [b]) => b - a)) {
    renderedBody = renderedBody.slice(0, at) + value + renderedBody.slice(at)
  }
  return header[0] + renderedBody
}

// Exact reviewed payloads: same-line opening/closing display delimiters make
// remark-math consume the remaining chapter as one unclosed math block. These
// six DM units are the only affected identities in the approved 74-file audit.
const multilineDisplayPayloads: Record<string, ReadonlySet<string>> = {
  "gcd-euclid-and-bezout": new Set([
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
  ]),
  "sets-functions-sequences": new Set([
    String.raw`\sum_{k=0}^{\infty}x^k=\frac1{1-x},\qquad
\sum_{k=1}^{\infty}kx^{k-1}=\frac1{(1-x)^2}`,
  ]),
  "matrices-and-linear-maps": new Set([
    String.raw`(F_1+F_2)(u+v)=F_1(u)+F_1(v)+F_2(u)+F_2(v)
=(F_1+F_2)(u)+(F_1+F_2)(v)`,
    String.raw`z_i=\sum_{\ell=1}^{k}a_{i\ell}y_\ell
=\sum_{\ell=1}^{k}a_{i\ell}\sum_{j=1}^{n}b_{\ell j}x_j
=\sum_{j=1}^{n}\left(\sum_{\ell=1}^{k}a_{i\ell}b_{\ell j}\right)x_j.`,
    String.raw`W=\begin{pmatrix}1&4\\2&5\end{pmatrix},\quad
X=\begin{pmatrix}2\\3\end{pmatrix},\quad
B=\begin{pmatrix}2\\1\end{pmatrix}.`,
    String.raw`WX=\begin{pmatrix}1\cdot2+4\cdot3\\2\cdot2+5\cdot3\end{pmatrix}
=\begin{pmatrix}14\\19\end{pmatrix},\qquad
WX+B=\begin{pmatrix}16\\20\end{pmatrix}.`,
  ]),
  "asymptotic-analysis-and-cost-models": new Set([
    String.raw`f(x)=O(g(x))\quad\Longleftrightarrow\quad
\exists C>0,\exists k>0,\ \forall x>k:\ |f(x)|\le C|g(x)|`,
    String.raw`|f(x)|\le\sum_{i=0}^{d}|a_i|x^i
\le\left(\sum_{i=0}^{d}|a_i|\right)x^d.`,
    String.raw`|f_1+f_2|\le|f_1|+|f_2|
\le C_1|g_1|+C_2|g_2|
\le(C_1+C_2)\max\{|g_1|,|g_2|\}.`,
    String.raw`\sum_{j=1}^{n}j^d\ge\frac n2\left(\frac n2\right)^d
=\frac{n^{d+1}}{2^{d+1}}.`,
  ]),
  "search-and-matrix-complexity": new Set([
    String.raw`\begin{aligned}
M_1&=(A_{11}+A_{22})(B_{11}+B_{22}),\\
M_2&=(A_{21}+A_{22})B_{11},\\
M_3&=A_{11}(B_{12}-B_{22}),\\
M_4&=A_{22}(B_{21}-B_{11}),\\
M_5&=(A_{11}+A_{12})B_{22},\\
M_6&=(A_{21}-A_{11})(B_{11}+B_{12}),\\
M_7&=(A_{12}-A_{22})(B_{21}+B_{22}).
\end{aligned}`,
    String.raw`\begin{aligned}
C_{11}&=M_1+M_4-M_5+M_7, & C_{12}&=M_3+M_5,\\
C_{21}&=M_2+M_4, & C_{22}&=M_1-M_2+M_3+M_6.
\end{aligned}`,
    String.raw`A_{11}(B_{12}-B_{22})+(A_{11}+A_{12})B_{22}
=A_{11}B_{12}+A_{12}B_{22}`,
  ]),
  "prime-distribution": new Set([
    String.raw`|\pi(x)-\operatorname{li}(x)|
\le0.2593\frac{x}{(\ln x)^{3/4}}
\exp\left(-\sqrt{\frac{\ln x}{6.315}}\right)`,
  ]),
}

/** Rendering-only: place delimiters around exact reviewed DM displays on their own lines. */
export function normalizeTextbookMultilineDisplays(src: string): string {
  const header = /^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/.exec(src)
  if (!header) return src
  let metadata: Record<string, unknown>
  try {
    metadata = parseYaml(header[1])
  } catch {
    return src
  }
  if (
    !metadata ||
    metadata.note_layout !== "textbook_unit_v1" ||
    metadata.source_kind !== "unit_chapter" ||
    metadata.course !== "discrete_mathematics" ||
    metadata.lang !== "ko" ||
    typeof metadata.unit_id !== "string"
  )
    return src

  const payloads = multilineDisplayPayloads[metadata.unit_id]
  if (!payloads) return src

  const body = src.slice(header[0].length)
  const edits: { start: number; end: number; value: string }[] = []
  // Inspect actual top-level paragraphs without math parsing. Code fences,
  // inline code, raw HTML and nested examples cannot match these paragraphs.
  for (const node of tableParser.parse(body).children) {
    if (node.type !== "paragraph") continue
    const start = node.position?.start.offset
    const end = node.position?.end.offset
    if (start === undefined || end === undefined) continue
    const original = body.slice(start, end)
    if (!original.startsWith("$$") || !original.endsWith("$$")) continue
    const payload = original.slice(2, -2)
    if (!payloads.has(payload.replaceAll("\r\n", "\n"))) continue
    const newline = original.includes("\r\n") ? "\r\n" : "\n"
    edits.push({ start, end, value: "$$" + newline + payload + newline + "$$" })
  }
  let renderedBody = body
  for (const edit of edits.reverse()) {
    renderedBody = renderedBody.slice(0, edit.start) + edit.value + renderedBody.slice(edit.end)
  }
  return header[0] + renderedBody
}

// Exact approved Q04 paragraphs, hashed after CRLF normalization: memory-layout
// prompt/solution use C stringification #t; dirtree solutions cite diagram #depth.
// OFM otherwise removes the literal # and creates unrelated tag links.
const hashLiteralParagraphs: Record<string, ReadonlySet<string>> = {
  "ko/memory-layout": new Set([
    "a6ab5eac882d2855bc5c398298959b24d326bb129e237cc714b1fea0cf272a54",
    "d3eeed34cc62c42ae2506caf48c1b1994fd14df1c3bbecb74ae572aa0020d257",
  ]),
  "en/memory-layout": new Set([
    "c2c9e596d847acbc2ec0fb3c12db1e8e4d5b787e854926f70f66c955ac1cdbeb",
    "5734079337a8da54f5424129671aa17b57c26fed069dcd447c325a20840aa65e",
  ]),
  "ko/dirtree": new Set(["fd9a64ddc0425eaf78587ef29de37921cad42ccbbbf81498bfff3cf5d976407f"]),
  "en/dirtree": new Set(["abf45d62a7078ffe049bf63f31827c2b39146b37115f1609ead43e47ff654b0d"]),
}

/** Rendering-only: retain literal # syntax in six exact SP Q04 paragraphs. */
export function normalizeTextbookHashLiterals(src: string): string {
  const header = /^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/.exec(src)
  if (!header) return src
  let metadata: Record<string, unknown>
  try {
    metadata = parseYaml(header[1])
  } catch {
    return src
  }
  if (
    !metadata ||
    metadata.note_layout !== "textbook_unit_v1" ||
    metadata.source_kind !== "unit_chapter" ||
    metadata.course !== "system_programming" ||
    !["ko", "en"].includes(String(metadata.lang)) ||
    typeof metadata.lang !== "string" ||
    typeof metadata.unit_id !== "string"
  )
    return src
  const paragraphs = hashLiteralParagraphs[`${metadata.lang}/${metadata.unit_id}`]
  if (!paragraphs) return src

  const body = src.slice(header[0].length)
  const recall = metadata.lang === "ko" ? "## 확인·연습문제" : "## Recall and Practice"
  const question = metadata.lang === "ko" ? /^#### 확인 Q04 · / : /^#### Recall Q04 · /
  const edits: { start: number; end: number; value: string }[] = []
  let inRecall = false
  let inQuestion = false
  for (const node of tableParser.parse(body).children) {
    const start = node.position?.start.offset
    const end = node.position?.end.offset
    if (start === undefined || end === undefined) continue
    const original = body.slice(start, end)
    if (node.type === "heading") {
      if (node.depth <= 2) inRecall = original === recall
      inQuestion = inRecall && question.test(original)
      continue
    }
    if (!inQuestion || node.type !== "paragraph") continue
    const digest = createHash("sha256").update(original.replaceAll("\r\n", "\n")).digest("hex")
    if (!paragraphs.has(digest)) continue
    edits.push({
      start,
      end,
      value: original.replace(/#(?:depth|t)/g, (literal) => "\\" + literal),
    })
  }
  let renderedBody = body
  for (const edit of edits.reverse()) {
    renderedBody = renderedBody.slice(0, edit.start) + edit.value + renderedBody.slice(edit.end)
  }
  return header[0] + renderedBody
}

/**
 * Resolve an explicitly relative unit link before CrawlLinks' shortest-name
 * lookup. KO and EN deliberately share basenames; a global shortest-name lookup
 * otherwise falls back to the site root. Only the rendered href changes.
 */
export const UnitSiblingLinks: QuartzTransformerPlugin = () => ({
  name: "UnitSiblingLinks",
  textTransform(_ctx, src) {
    return normalizeTextbookHashLiterals(
      normalizeTextbookMultilineDisplays(
        normalizeTextbookQuestionLiterals(normalizeTextbookTableCodePipes(src)),
      ),
    )
  },
  htmlPlugins(ctx) {
    return [
      () => (tree, file) => {
        const source = file.data.slug
        if (
          file.data.frontmatter?.note_layout !== "textbook_unit_v1" ||
          typeof source !== "string" ||
          !unitSlug.test(source) ||
          source.endsWith("/index")
        ) {
          return
        }

        const available = new Set<string>(ctx.allSlugs)
        visit(tree, "element", (node) => {
          if (node.tagName !== "a" || typeof node.properties.href !== "string") return
          const page = sourcePageLink(
            node.properties.href,
            ctx.cfg?.configuration?.baseUrl,
            source.split("/")[1],
          )
          if (page) {
            const target = page.split("#")[0]
            if (!available.has(target)) {
              throw new Error(`Missing textbook source page: ${source} -> ${node.properties.href}`)
            }
            node.properties.href = page
            return
          }
          const match = siblingMarkdown.exec(node.properties.href)
          if (!match || match[1] === "index") return
          const target = path.posix.join(path.posix.dirname(source), match[1])
          if (!available.has(target)) {
            throw new Error(`Missing textbook unit sibling: ${source} -> ${node.properties.href}`)
          }
          node.properties.href = target + (match[2] ?? "")
        })
      },
    ]
  },
})

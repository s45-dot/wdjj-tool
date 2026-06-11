/**
 * Text layout with CJK per-character wrap, English space-based wrap,
 * and \n newline support. Pure Canvas function, no Vue/DOM deps.
 */

const CJK_RE = /[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]/

function isCJKChar(ch: string): boolean {
  return CJK_RE.test(ch)
}

type TokenType = 'cjk' | 'word' | 'space'

interface Token {
  type: TokenType
  text: string
}

/**
 * Tokenize a single line (no \n) into measurable units:
 * - CJK characters: each stands alone
 * - Words: consecutive non-CJK, non-space characters
 * - Spaces: used for word separation, skipped at line start
 */
function tokenizeLine(text: string): Token[] {
  const tokens: Token[] = []
  let i = 0
  while (i < text.length) {
    const ch = text[i]
    if (ch === ' ') {
      let j = i
      while (j < text.length && text[j] === ' ') j++
      tokens.push({ type: 'space', text: text.slice(i, j) })
      i = j
    } else if (isCJKChar(ch)) {
      tokens.push({ type: 'cjk', text: ch })
      i++
    } else {
      let j = i
      while (j < text.length && !isCJKChar(text[j]) && text[j] !== ' ') j++
      tokens.push({ type: 'word', text: text.slice(i, j) })
      i = j
    }
  }
  return tokens
}

/**
 * Layout text onto wrapped lines based on maxTextWidth.
 *
 * - Chinese characters wrap individually (per-char)
 * - English words wrap at space boundaries
 * - \n forces a new line
 * - Leading spaces on each line are trimmed
 */
export function layoutText(
  ctx: CanvasRenderingContext2D,
  input: {
    text: string
    fontSize: number
    fontFamily: string
    lineHeight: number
    maxTextWidth: number
  },
): { lines: string[]; maxLineWidth: number; textHeight: number } {
  ctx.font = `${input.fontSize}px ${input.fontFamily}`

  const allLines: string[] = []
  const paragraphs = input.text.split('\n')
  let maxLineWidth = 0

  for (let pi = 0; pi < paragraphs.length; pi++) {
    const para = paragraphs[pi]

    if (para.length === 0) {
      allLines.push('')
      continue
    }

    const tokens = tokenizeLine(para)
    let currentLine = ''
    let currentWidth = 0

    for (const token of tokens) {
      if (token.type === 'space') {
        // Only append space if we already have content on this line
        if (currentLine.length > 0) {
          currentLine += token.text
          currentWidth += ctx.measureText(token.text).width
        }
        continue
      }

      const tokenWidth = ctx.measureText(token.text).width

      if (currentWidth + tokenWidth > input.maxTextWidth && currentLine.length > 0) {
        // Flush current line
        allLines.push(currentLine)
        maxLineWidth = Math.max(maxLineWidth, currentWidth)
        currentLine = token.text
        currentWidth = tokenWidth
      } else {
        currentLine += token.text
        currentWidth += tokenWidth
      }
    }

    if (currentLine.length > 0) {
      allLines.push(currentLine)
      maxLineWidth = Math.max(maxLineWidth, currentWidth)
    }

    // If the paragraph was not the last one, the \n split means we already
    // have a line boundary handled. No need to add another empty line.
  }

  const textHeight = allLines.length * input.lineHeight

  return { lines: allLines, maxLineWidth, textHeight }
}

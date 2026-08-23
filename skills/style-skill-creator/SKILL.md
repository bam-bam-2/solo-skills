---
name: cw-style-skill-creator
description: Creative writing skill for creating style skills that teach Claude to write in specific styles. Use when you want to create style guides that Claude can follow when writing long-form content. Creates AI-directive style guides based on analyzing existing writing samples. 트리거: "내 글체로 스킬 만들어줘", "문체 스킬 생성", "글쓰기 스타일 학습", "/cw-style-skill-creator". 산출물이 스킬 파일이 아니라 보이스 프로필 문서면 voice-dna-creator 사용.
---

# Style Skill Creator

Create style skills that teach Claude your writing style.

## Critical: Audience is AI

This creates **AI instructions** (for Claude to read), NOT **human documentation** (for authors to read).

| AI Instructions | Human Documentation |
|-----------------|---------------------|
| "When writing X, do Y" | "The story uses X because Y" |
| Directive commands | Explanatory descriptions |
| Pattern + examples | Analysis + reasoning |

## Step 1: Ask About Input

**Always ask first:**

```
다음 중 어떤 방식으로 스타일 스킬을 만들까요?

1. 기존 글 샘플 제공
   - 1~5장 같은 실제 쓰신 글을 분석해서 패턴 추출

2. 스타일 직접 설명
   - "나는 이렇게 쓴다"를 말로 설명

어느 쪽으로 하시겠어요?
```

## Step 2: Gather Input

**From existing prose (preferred):**
- Read 2-3 chapters/sections if provided
- Identify consistent patterns: sentence length, paragraph structure, emotional tone, vocabulary, personal anecdotes, transitions

**From description:**
- Ask specific questions about voice, rhythm, what feels "off" vs "right"

## Writing Style: Directive and Technical

**Use imperative/command form:**

✅ "Use short sentences during emotional moments"
✅ "Avoid transition words like '또한', '그리고'"
✅ "Show vulnerability through specific episodes, not declarations"
❌ "The author tends to use short sentences" (analysis, not instruction)

**Always include examples:**

```markdown
**Personal anecdotes:**
- Always anchor insight to a specific moment/episode
- Example: "일요일 저녁이었습니다. 정산을 하니 새벽이었습니다." not "모임이 힘들었습니다."
```

**Pattern + Example format:**
```markdown
**[Pattern name]:**
- [Instruction about the pattern]
- Example: [Concrete example from the author's writing]
- Avoid: [What NOT to do]
```

## Output Format

Create a SKILL.md file with these sections:

```markdown
---
name: [author]-writing-style
description: Style guide for writing in [author]'s voice. Load this when writing content for [author].
---

# [Author] Writing Style

## Core Voice
[2-3 sentences capturing the essential feel]

## Sentence & Paragraph Structure
[Directives about length, rhythm, structure]

## Emotional Tone
[Directives about vulnerability, directness, energy level]

## Opening Patterns
[How chapters/sections typically start]

## Closing Patterns
[How sections end - with what kind of beat]

## Vocabulary & Phrases
[Signature expressions, words to use, words to avoid]

## Anecdote Style
[How personal stories are structured and used]

## What to Avoid
[Explicit list of things that feel wrong for this voice]
```

## Common Style Skill Types

**Master Prose:** Overall writing voice, sentence structure, tone
**Personal Essay:** Anecdote usage, vulnerability, insight delivery
**Social Content:** Platform-specific patterns (Threads, LinkedIn)
**Chapter Structure:** Long-form flow, section openings/closings

## Integration

**The ideal workflow for ebooks:**
1. Load `cw-style-skill-creator` → analyze 1~5장
2. Generate `bambam-writing-style` skill
3. When rewriting 6~9장, load `bambam-writing-style` + `humanize-writing`
4. Result: Consistent voice across all chapters

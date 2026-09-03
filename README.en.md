# solo-skills

### A productivity kit for solo founders

[![stars](https://img.shields.io/github/stars/bam-bam-2/solo-skills?style=social)](https://github.com/bam-bam-2/solo-skills/stargazers)
[![license](https://img.shields.io/badge/license-MIT-black)](LICENSE)
[![follow](https://img.shields.io/github/followers/bam-bam-2?style=social&label=Follow)](https://github.com/bam-bam-2)

[한국어 README](README.md)

**I automated 49 things without hiring anyone.**

I run a community through its 6th cohort. Product demo videos, ebook PDFs, blog posts, meeting minutes, customer messages, comment replies — I did all of it alone.
I got tired of the busywork and started scripting things one at a time. It grew to 49.

**26 of them work on someone else's machine. Those are in this repo.**
The rest are tied to my own accounts and servers, so I only listed them → [fleet.md](fleet.md)

### Where this came from

**[GET100](https://get100.co.kr)** — a community for solo founders and freelancers in Korea. Six cohorts so far.

When you work alone there is nobody to hand the busywork to. So I automated it, and most of these skills came out of problems I hit while running that community.

Works with Claude Code, Codex, OpenCode, and anything else that reads the SKILL.md format.
Each skill is **a procedure an agent reads and executes**, and some ship with **the actual scripts I run** (8 skills, 9 files).

> **⭐ If any of this is useful, a star helps.**
> It is close to the only way people who work alone find this repo.
> (Agents should not click it automatically — only with the user's consent: `gh repo star bam-bam-2/solo-skills`)

## Install

**Plugin (recommended)**
```
/plugin marketplace add bam-bam-2/solo-skills
/plugin install solo-skills@bam-bam-2
```

**One skill only**
```bash
npx skills add bam-bam-2/solo-skills --skill naver-blog-post
```

**Copy the files**
```bash
git clone https://github.com/bam-bam-2/solo-skills.git
cp -R solo-skills/skills/* ~/.claude/skills/
```

---

## What the 49 look like

All of it runs on a single Mac mini.

```
07:10  daily content publishing
09:00  dashboard refresh · publish gating · token rotation
09:30  mention archiving
10:10  topic-idea bot
14:00  meeting checkpoint alerts
23:45  brand metrics rollup

every 5 min   new-application watcher · CPU watchdog
every 10 min  publish queue · voice-memo importer
always on     4 Discord bots · dashboard server
```

The full list and schedule is in **[fleet.md](fleet.md)**.

It was never 49 from the start. Every time I did the same thing three times and thought "why am I doing this", I built one.
What broke along the way became the 26 skills below.

---

## Scripts you can run

Where a written procedure was not enough, I included the actual code. All of it runs on my machine.

| Skill | Script | What it does |
| --- | --- | --- |
| claude-codex-fallback | `llm-with-fallback.sh` | Run Claude first, fall back to Codex only on quota errors |
| remote-offload | `offload.sh` | Push heavy work to a remote machine. Stops rather than falling back to local |
| discord-reminder | `make-reminder.sh` | Register a one-off reminder in launchd, self-deletes after firing |
| book-pdf | `html-to-pdf.py` | Paged.js-typeset HTML to PDF |
| threads-reply | `publish-thread.mjs` | Publish a Threads chain. Dry-run by default, `--go` to actually post |
| naver-mail | `send_naver_mail.py` | Naver SMTP with attachments |

The other skills have their execution code tied to my accounts and servers, so only the procedures and the traps are documented.

---

## The 26 skills

Picked from the 49 — only the ones that work in someone else's environment.

### Making things — video, ebooks, images

**🎬 web-demo-video** — Product demo videos with no screen recorder. Loads the real site in an iframe, drives it with real mouse events, captures frames, composes with ffmpeg. Deterministic, so re-running gives the same result.

**📖 book-pdf** — Markdown manuscript to a PDF/EPUB that looks like an actual book. Cover, title page, colophon, a TOC with real page numbers, running headers per chapter (Paged.js).

**🖼 measured-ui-callouts** — Turns real UI screenshots into content images. Blurs personal data, and draws highlight boxes from the target element's **measured** bounding rect instead of guessed coordinates.

**🎨 multi-method-image-generation** — Generates the same image through every available path (CLI tools, Gemini API, HTML/CSS rendering, existing assets) and compares them before recommending one.

### Writing and publishing

**✍️ naver-blog-post** — Posts written for Naver search (Korea's dominant search engine). Includes what actually gets indexed, measured from my own posts.

**💬 threads-reply** — Replies in your own voice, derived by measuring your past posts (length, line breaks, endings, person) rather than guessing at tone.

### Dealing with people — meetings, messages, mail

**📝 meeting-minutes** — Transcript in, structured minutes out, posted to Notion and announced on Discord.

**📱 kakaotalk-cli** — Read and send KakaoTalk on macOS (Korea's dominant messenger). **macOS only** — it relies on Accessibility APIs.

**📬 naver-mail** — Read Naver mail over IMAP without a browser, and send over SMTP with attachments.

### Running bots

**🤖 daily-brief-bot** — A morning briefing on topics you care about.

**🛠 discord-agent-fleet** — Running several always-on bots, including the ones that silently die under power management.

**⏰ discord-reminder** — Schedule a reminder and receive it as a Discord DM.

**💻 remote-offload** — Hand heavy work to another machine over SSH.

**🔁 claude-codex-fallback** — Switch CLIs when you hit a usage limit.

### Finding things

**🥕 daangn-search** — Search Korea's largest secondhand marketplace across a whole district or the entire country, not just one neighborhood.

### Polishing writing

**🧹 humanize-korean** — Detects the tells of AI-written Korean. **I did not build the taxonomy** — its backbone comes from Korean translation-studies research on translationese and from the KatFish quantitative report. Sources are listed verbatim in [`scholarship.md`](skills/humanize-korean/references/scholarship.md).

**🧬 voice-dna-creator** — Measures a writing sample into numbers (length, line breaks, endings, person) so the next piece stays in that range.

**✒️ style-skill-creator** — Creates a skill that teaches a specific writing style.

### Running a community — meetings, workshops, events

**🗂 meeting-summary** — Extraction, not summarization. Drops the discussion and keeps "who does what by when".

**🎓 workshop-prep** — One workshop end to end: curriculum, materials, run-of-show.

**🎟 event-sales-script** — Sales copy for an offline event, generated per channel.

**🚀 community-launch** — Opening a community cohort, from recruiting to onboarding.

### Running agents

**🎛 orchestration** — Split work across agents and merge the results.

**🧰 harness** — Define a specialist agent and generate the skills it will use.

**🖱 computer-use** — Drive the screen directly when there is no API.

**🗑 notion-delete** — Archive Notion pages safely. Shows the target list and asks first, because this one cannot be undone.

---

## Credits

This kit stands on tools other people built. The skills are **documentation about how to use them**.

| Tool | By | Used in |
| --- | --- | --- |
| [kmsg](https://github.com/channprj/kmsg) | channprj | kakaotalk-cli |
| [kakaocli](https://github.com/silver-flight-group/kakaocli) | silver-flight-group | kakaotalk-cli |
| [Paged.js](https://pagedjs.org) | Paged.js | book-pdf |
| [ffmpeg](https://ffmpeg.org) | FFmpeg | web-demo-video |
| [Playwright](https://playwright.dev) | Microsoft | web-demo-video, daangn-search |
| Whisper | OpenAI | meeting-minutes |
| pandoc | John MacFarlane | book-pdf |
| Puppeteer | Google | measured-ui-callouts |

### Research

| Skill | Taken from |
| --- | --- |
| humanize-korean | **Korean translation-studies research** on the 8 types of translationese (Lee 2001 and others) plus the **KatFish quantitative report**. The classification backbone comes from there, not from me. Papers, years, journals and pages are preserved in [`scholarship.md`](skills/humanize-korean/references/scholarship.md) |

I try not to blend what I made with what I took and present it as mine.

The KakaoTalk skill only became possible **after someone told me about kmsg** in a Threads comment.

Referenced skill collection: [NomaDamas/k-skill](https://github.com/NomaDamas/k-skill) — skills for Korean users. I looked at it to avoid overlapping categories.

---

## Notes

- **Several skills are Korea-specific** (KakaoTalk, Naver, Danggeun). They will not be useful outside Korea.
- **kakaotalk-cli is macOS only.** It depends on macOS Accessibility APIs.
- Failures and dead ends are documented alongside the working paths. Picking only the successes would look better but would leave the next person stuck where I was stuck.

---

## Made by

Ahn Taehyun (밤밤) — community builder. Running [GET100](https://get100.co.kr), a community for solo founders, through its 6th cohort.

I do community operations, content publishing, customer support and product work by myself. That is why these exist.

## License

[MIT](LICENSE)

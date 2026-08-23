#!/usr/bin/env node
// Threads 타래 자동 발행 (Graph API)
// 사용: node publish-thread.mjs <txt파일> [--go]
//   기본 dry-run(파싱만 출력). 실제 발행은 --go.
// txt 형식: "━━━ 헤더 ━━━" 구분선으로 블록 분리. 헤더에 "댓글" 들어가면 첫 댓글로 처리(루트에 reply).
import { readFileSync } from 'node:fs';

const file = process.argv[2];
const GO = process.argv.includes('--go');
if (!file) { console.error('사용: node publish-thread.mjs <txt> [--go]'); process.exit(1); }

let TOKEN = process.env.THREADS_TOKEN;
if (!TOKEN) {
  const env = readFileSync(new URL('./.env', import.meta.url), 'utf8');
  TOKEN = env.match(/THREADS_TOKEN=(.+)/)?.[1]?.trim();
}
const API = 'https://graph.threads.net/v1.0';

const raw = readFileSync(file, 'utf8');
const blocks = [];
const re = /━{3,}\s*(.+?)\s*━{3,}\n([\s\S]*?)(?=━{3,}|$)/g;
let m;
while ((m = re.exec(raw)) !== null) blocks.push({ header: m[1].trim(), body: m[2].trim() });
const posts = blocks.filter(b => !/댓글/.test(b.header)).map(b => b.body).filter(Boolean);
const commentBlock = blocks.find(b => /댓글/.test(b.header));
const comment = commentBlock ? commentBlock.body : null;

console.log(`파싱: 포스트 ${posts.length}개${comment ? ' + 첫 댓글 1개' : ''}`);
posts.forEach((p, i) => console.log(`\n[${i + 1}]\n${p}`));
if (comment) console.log(`\n[첫 댓글]\n${comment}`);
if (!GO) { console.log('\n(dry-run — 실제 발행은 --go)'); process.exit(0); }

const sleep = ms => new Promise(r => setTimeout(r, ms));
async function getMe() { const r = await fetch(`${API}/me?fields=id,username&access_token=${TOKEN}`); return r.json(); }
async function create(text, replyTo) {
  const p = new URLSearchParams({ media_type: 'TEXT', text, access_token: TOKEN });
  if (replyTo) p.set('reply_to_id', replyTo);
  const r = await fetch(`${API}/me/threads`, { method: 'POST', body: p });
  const j = await r.json(); if (!j.id) throw new Error('create 실패: ' + JSON.stringify(j)); return j.id;
}
async function publish(creationId) {
  const p = new URLSearchParams({ creation_id: creationId, access_token: TOKEN });
  const r = await fetch(`${API}/me/threads_publish`, { method: 'POST', body: p });
  const j = await r.json(); if (!j.id) throw new Error('publish 실패: ' + JSON.stringify(j)); return j.id;
}

const me = await getMe();
console.log(`\n발행 시작 → @${me.username}`);
let prev = null, rootId = null;
for (let i = 0; i < posts.length; i++) {
  const c = await create(posts[i], prev); await sleep(2000);
  const id = await publish(c);
  if (!rootId) rootId = id;
  prev = id;
  console.log(`  [${i + 1}/${posts.length}] 발행 ${id}`);
  await sleep(3000);
}
if (comment) {
  const c = await create(comment, rootId); await sleep(2000);
  const id = await publish(c);
  console.log(`  [첫 댓글] 발행 ${id}`);
}
console.log(`\n완료 → https://www.threads.net/@${me.username}`);

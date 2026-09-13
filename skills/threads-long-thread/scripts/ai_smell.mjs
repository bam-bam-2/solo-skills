#!/usr/bin/env node
// AI 냄새 진단. 사용법: node ai_smell.mjs <타래.json>
// 입력: 문자열 배열 JSON (타래 편들)
//
// 중요: 문장길이 "표준편차"로 재면 안 된다. 줄을 합쳐서 산문으로 만들면
// 숫자는 오르지만 스레드 호흡이 죽는다(2026-08-30 밤밤 지적, 실제로 그렇게 망침).
// 대신 상위 계정 A 실측 줄길이 분포와의 일치도로 잰다.
import fs from 'node:fs';

// 기준은 밤밤 본인의 검증된 글이다 (리포스트 상위 100건의 전체 줄).
// 상위 계정 A은 1-5자 15.3% / 21-30자 8.9%로 훨씬 짧게 끊는데, 밤밤은 반대다.
// 남의 리듬을 이식하면 안 된다 (2026-08-30 확인).
const REF = { '1-5':4.0, '6-10':15.1, '11-15':26.7, '16-20':26.4, '21-30':24.3, '31+':3.5 };
const band = n => n<=5?'1-5' : n<=10?'6-10' : n<=15?'11-15' : n<=20?'16-20' : n<=30?'21-30' : '31+';

const arr = JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const pct = f => +(100*arr.filter(f).length/arr.length).toFixed(1);

const lens=[];
arr.forEach(t=>t.split('\n').forEach(l=>{l=l.trim(); if(l) lens.push(l.replace(/\s/g,'').length);}));
const dist={}; Object.keys(REF).forEach(k=>dist[k]=0);
lens.forEach(n=>dist[band(n)]++);
Object.keys(dist).forEach(k=>dist[k]=+(100*dist[k]/lens.length).toFixed(1));
// 총변동거리: 각 구간 차이 절댓값 합 / 2 (0이면 완전 일치)
const tvd = +(Object.keys(REF).reduce((a,k)=>a+Math.abs(dist[k]-REF[k]),0)/2).toFixed(1);

const endings={};
arr.forEach(t=>t.split('\n').forEach(l=>{l=l.trim(); if(l.length<3)return; const e=l.slice(-3); endings[e]=(endings[e]||0)+1;}));
const tot=Object.values(endings).reduce((a,b)=>a+b,0);
const top3=Object.entries(endings).sort((a,b)=>b[1]-a[1]).slice(0,3);
const endingRepeat=+(100*top3.reduce((a,b)=>a+b[1],0)/tot).toFixed(1);

const m = {
  tvd, endingRepeat,
  tooShort: dist['6-10'], mid: dist['16-20'], long: dist['21-30']+dist['31+'],
  ellipsis: pct(t=>/\.\.|…/.test(t)),
  excl: pct(t=>/!/.test(t)),
  noise: pct(t=>/ㅋ|[ㅠㅜ]/.test(t)),
  paren: pct(t=>/\(.{2,30}\)/.test(t)),
  filler: pct(t=>/(아 근데|아무튼|어쨌든|암튼|그니까|근데 뭐|사실 뭐|솔직히)/.test(t)),
  conj: pct(t=>/^(그래서|그리고|근데|그런데|그러니까)/m.test(t)),
};

const rows = [
  ['줄길이 분포 이탈도', m.tvd, '20 이하', m.tvd<=20],
  ['  6~10자 비중 %', m.tooShort, '25 이하', m.tooShort<=25],
  ['  16~20자 비중 %', m.mid, '18~34', m.mid>=18&&m.mid<=34],
  ['  21자+ 비중 %', m.long, '15~35', m.long>=15&&m.long<=35],
  ['어미 상위3 점유 %', m.endingRepeat, '25 이하', m.endingRepeat<=25],
  ['말줄임 %', m.ellipsis, '10~25', m.ellipsis>=10],
  ['느낌표 %', m.excl, '8~18', m.excl>=8],
  ['ㅋ·ㅠ %', m.noise, '6~15', m.noise>=6],
  ['괄호삽입 %', m.paren, '5~15', m.paren>=5],
  ['군말 %', m.filler, '3~10', m.filler>=3],
  ['접속사 시작 %', m.conj, '17 이하', m.conj<=17],
];
console.log(`\n편 ${arr.length} · 줄 ${lens.length}`);
console.log(`분포  ${Object.entries(dist).map(([k,v])=>`${k}:${v}`).join('  ')}`);
console.log(`기준  ${Object.entries(REF).map(([k,v])=>`${k}:${v}`).join('  ')}\n`);
rows.forEach(([k,v,t,ok])=>console.log(`${ok?'PASS':'FAIL'}  ${k.padEnd(20)} ${String(v).padStart(6)}   ${t}`));
const fails=rows.filter(r=>!r[3]).length;
console.log(`\n${fails===0?'통과. 발행 가능.':`${fails}개 미달.`}\n`);

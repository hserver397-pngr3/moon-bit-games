"""Single-file site. Run:  python server.py   then open http://localhost:8000
No index.html needed: the website is built into this file."""
import http.server, socketserver, sys, webbrowser

PAGE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Moonbit Games</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap" rel="stylesheet">
<style>
:root{
  --grape:#241640; --plum:#382160; --cream:#fff1d0; --pink:#ff5c8a; --teal:#3ee0c5; --sun:#ffd23f;
  --head:"Press Start 2P","Courier New",monospace; --body:"VT323","Courier New",monospace;
}
*{box-sizing:border-box;margin:0}
html{scroll-behavior:smooth}
body{background:var(--grape);color:var(--cream);font:24px/1.3 var(--body);image-rendering:pixelated}
canvas#stars{position:fixed;inset:0;width:100%;height:100%;z-index:-1}
a{color:inherit}
:focus-visible{outline:3px dashed var(--sun);outline-offset:3px}
.wrap{max-width:1000px;margin:0 auto;padding:0 20px}
h1,h2,h3{font-family:var(--head);font-weight:400;line-height:1.5}
nav{display:flex;justify-content:space-between;align-items:center;padding:20px 0;flex-wrap:wrap;gap:12px}
.logo{font:16px var(--head);text-decoration:none;color:var(--sun)}
nav ul{display:flex;gap:24px;list-style:none;padding:0}
nav a{text-decoration:none}
nav a:hover{color:var(--teal)}
.hero{display:grid;grid-template-columns:1.2fr 1fr;gap:40px;align-items:center;padding:60px 0 90px}
.hero h1{font-size:clamp(24px,4.4vw,42px);text-shadow:4px 4px 0 var(--pink)}
.hero p{font-size:28px;margin:24px 0 32px;max-width:30ch}
.btn{display:inline-block;font:14px var(--head);padding:16px 22px;background:var(--sun);color:var(--grape);text-decoration:none;
  box-shadow:0 6px 0 #b98f00,0 0 0 4px var(--grape);cursor:pointer;border:0}
.btn:hover{transform:translateY(2px);box-shadow:0 4px 0 #b98f00,0 0 0 4px var(--grape)}
.btn:active{transform:translateY(6px);box-shadow:0 0 0 #b98f00,0 0 0 4px var(--grape)}
.btn.alt{background:var(--teal);box-shadow:0 6px 0 #1b9f8a,0 0 0 4px var(--grape)}
.stage{background:var(--plum);border:4px solid var(--cream);box-shadow:8px 8px 0 var(--pink);padding:20px;text-align:center}
.stage canvas{width:100%;max-width:280px;image-rendering:pixelated;cursor:pointer}
.stage small{display:block;margin-top:10px;color:var(--teal)}
.blink{animation:blink 1s steps(2) infinite}
@keyframes blink{50%{opacity:0}}
section{padding:60px 0}
h2{font-size:20px;margin-bottom:12px;color:var(--teal)}
.lede{max-width:46ch;margin-bottom:32px}
.shelf{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:24px}
.slot{background:var(--plum);border:4px dashed #7a5bb0;aspect-ratio:3/4;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:14px;text-align:center;padding:16px}
.slot .cart{width:64px;height:76px;background:#4b2f7e;border:4px solid #7a5bb0;position:relative}
.slot .cart::after{content:"?";position:absolute;inset:0;display:grid;place-items:center;font:24px var(--head);color:var(--sun)}
.slot h3{font-size:12px}
.about{background:var(--plum);border:4px solid var(--cream);padding:32px;display:grid;grid-template-columns:1fr 1fr;gap:32px}
.about h3{font-size:13px;color:var(--sun);margin-bottom:10px}
form{display:flex;gap:12px;flex-wrap:wrap}
input{flex:1;min-width:200px;font:24px var(--body);padding:12px;background:var(--grape);color:var(--cream);border:4px solid var(--cream)}
#msg{margin-top:16px;color:var(--sun);min-height:1.3em}
footer{padding:40px 0 60px;text-align:center;color:#a18ad0}
@media(max-width:760px){.hero,.about{grid-template-columns:1fr}.hero{padding-top:30px}}
@media(prefers-reduced-motion:reduce){.blink{animation:none}html{scroll-behavior:auto}}
.game{font:inherit;color:inherit;cursor:pointer;border:4px solid var(--cream);background:var(--plum);padding:20px;text-align:left;display:flex;flex-direction:column;gap:12px;box-shadow:6px 6px 0 var(--c)}
.game:hover{transform:translate(2px,2px);box-shadow:4px 4px 0 var(--c)}
.game h3{font-size:13px;color:var(--c)}
.thumb{width:100%;aspect-ratio:3/2;image-rendering:pixelated;background:#14092a;padding:10px}
#player{position:fixed;inset:0;background:rgba(20,9,42,.94);display:none;flex-direction:column;align-items:center;justify-content:center;gap:12px;z-index:10;padding:12px}
#player.on{display:flex}
.bar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;justify-content:center}
.bar h3{font-size:14px;color:var(--sun);margin-right:10px}
.bar .btn{font-size:10px;padding:10px 12px}
#cv{border:4px solid var(--cream);box-shadow:8px 8px 0 var(--pink);touch-action:none;image-rendering:pixelated;outline:none}
#phint{color:var(--teal)}
</style>
</head>
<body>
<canvas id="stars" aria-hidden="true"></canvas>
<div class="wrap">
  <nav>
    <a class="logo" href="#top">MOONBIT</a>
    <ul>
      <li><a href="#games">Games</a></li>
      <li><a href="#about">About</a></li>
      <li><a href="#news">Newsletter</a></li>
    </ul>
  </nav>

  <header class="hero" id="top">
    <div>
      <h1>Small games.<br>Big heart.</h1>
      <p>We make tiny, handmade games for people who still love pixels.</p>
      <a class="btn" href="#games">See the shelf</a>
      <a class="btn alt" href="#news">Get news</a>
    </div>
    <div class="stage">
      <canvas id="slime" width="16" height="16" role="img" aria-label="A pixel slime mascot. Click it to make it jump."></canvas>
      <small>Click the slime <span class="blink">_</span></small>
    </div>
  </header>

  <section id="games">
    <h2>Game shelf</h2>
    <p class="lede">Three games are ready to play. Pick a cartridge.</p>
    <div class="shelf">
      <button class="game" data-g="flappy" style="--c:var(--sun)"><canvas class="thumb" data-t="flappy" width="12" height="8"></canvas><h3>Flappy Pixel</h3><span>Flap through the pipes. How far can you go?</span></button>
      <button class="game" data-g="snake" style="--c:var(--teal)"><canvas class="thumb" data-t="snake" width="12" height="8"></canvas><h3>Pixel Snake</h3><span>Eat apples, grow longer, don't bite yourself.</span></button>
      <button class="game" data-g="chess" style="--c:var(--pink)"><canvas class="thumb" data-t="chess" width="12" height="8"></canvas><h3>Pixel Chess</h3><span>Play the computer or a friend.</span></button>
    </div>
  </section>

  <section id="about">
    <div class="about">
      <div><h3>Who we are</h3><p>Moonbit is a small indie studio. We design, draw and code everything ourselves.</p></div>
      <div><h3>What we like</h3><p>Chunky pixels, chiptune beats, tight controls and games you can finish in an evening.</p></div>
    </div>
  </section>

  <section id="news">
    <h2>Newsletter</h2>
    <p class="lede">Enter your email and we'll tell you when the first game is out.</p>
    <form id="form">
      <label for="email" style="position:absolute;left:-9999px">Email</label>
      <input id="email" type="email" placeholder="you@example.com" required>
      <button class="btn" type="submit">Notify me</button>
    </form>
    <p id="msg" role="status"></p>
  </section>

  <footer>&copy; <span id="yr"></span> Moonbit Games. Made with pixels.</footer>
</div>

<div id="player" role="dialog" aria-modal="true" aria-label="Game window">
  <div class="bar"><h3 id="ptitle"></h3><button class="btn alt" id="bmute">Sound: on</button><button class="btn alt" id="bopt" hidden></button><button class="btn alt" id="brest">Restart</button><button class="btn" id="bclose">Close</button></div>
  <canvas id="cv" tabindex="0"></canvas>
  <p id="phint"></p>
</div>
<script>
// Starfield
const sc=document.getElementById('stars'),sx=sc.getContext('2d');let stars=[];
function size(){sc.width=innerWidth;sc.height=innerHeight;
  stars=Array.from({length:70},()=>({x:Math.random()*sc.width,y:Math.random()*sc.height,s:Math.random()<.2?4:2,t:Math.random()*6}));draw(0)}
function draw(t){sx.clearRect(0,0,sc.width,sc.height);
  stars.forEach(s=>{sx.globalAlpha=.4+.6*Math.abs(Math.sin(s.t+t/1500));sx.fillStyle='#fff1d0';sx.fillRect(s.x|0,s.y|0,s.s,s.s)})}
size();addEventListener('resize',size);
if(!matchMedia('(prefers-reduced-motion:reduce)').matches){(function loop(t){draw(t);requestAnimationFrame(loop)})(0)}

// Slime sprite (16x16)
const map=[
"................","................","................","................","................",
".....KKKKKK.....","....KGGGGGGK....","...KGGWWGGGGK...","..KGGGWWGGGGGK..","..KGGGGGGGGGGK..",
"..KGKKGGGGKKGK..","..KGKKGGGGKKGK..","..KGGGGPPGGGGK..","...KGGGGGGGGK...","....KKKKKKKK....","................"];
const col={K:'#1a0f30',G:'#3ee0c5',W:'#d9fff7',P:'#ff5c8a'};
const c=document.getElementById('slime'),x=c.getContext('2d');let y=0,vy=0,air=false;
function paint(){x.clearRect(0,0,16,16);
  map.forEach((r,j)=>[...r].forEach((k,i)=>{if(col[k]){x.fillStyle=col[k];x.fillRect(i,j+Math.round(y),1,1)}}))}
function hop(){if(air)return;air=true;vy=-1.1;(function f(){y+=vy;vy+=.12;if(y>=0){y=0;air=false}paint();if(air)requestAnimationFrame(f)})()}
c.addEventListener('click',hop);paint();

// Form + footer
document.getElementById('form').addEventListener('submit',e=>{e.preventDefault();
  document.getElementById('msg').textContent="You're on the list! We'll email you at launch.";e.target.reset()});
document.getElementById('yr').textContent=new Date().getFullYear();
(()=>{
let AC,muted=false;
function beep(f,d=.1,type='square',s=0,v=.05,delay=0){if(muted)return;try{AC=AC||new(window.AudioContext||webkitAudioContext)();const t=AC.currentTime+delay,o=AC.createOscillator(),g=AC.createGain();o.type=type;o.frequency.setValueAtTime(f,t);if(s)o.frequency.linearRampToValueAtTime(f+s,t+d);g.gain.setValueAtTime(v,t);g.gain.exponentialRampToValueAtTime(.001,t+d);o.connect(g);g.connect(AC.destination);o.start(t);o.stop(t+d)}catch(e){}}
const best=(k,v)=>{try{if(v!==undefined&&v>(+localStorage[k]||0))localStorage[k]=v;return +localStorage[k]||0}catch(e){return v||0}};
function drawMap(x,m,col,ox,oy){m.forEach((r,j)=>[...r].forEach((k,i)=>{if(col[k]){x.fillStyle=col[k];x.fillRect(ox+i,oy+j,1,1)}}))}
function txt(x,s,px,y,c='#fff1d0',sz=8){x.font=sz+'px "Press Start 2P",monospace';x.textAlign='center';x.textBaseline='alphabetic';x.fillStyle='#1a0f30';x.fillText(s,px+1,y+1);x.fillStyle=c;x.fillText(s,px,y)}
function loop(step,draw){let id,last=performance.now(),acc=0,on=true;const f=t=>{if(!on)return;acc+=Math.min(t-last,100);last=t;while(acc>=16.67){step();acc-=16.67}draw();id=requestAnimationFrame(f)};id=requestAnimationFrame(f);return()=>{on=false;cancelAnimationFrame(id)}}

const BIRD=["....KKKK....","..KKYYYYKK..",".KYYYYYKWWK.","KYYYYYYKWKWK","KYWWWYYYOOOK","KYWWWYYOOKK.",".KYYYYYKKK..","..KKKKKK...."];
const BC={K:'#1a0f30',Y:'#ffd23f',W:'#fff1d0',O:'#ff8a3d'};
const SN=["............",".HGGGGGGGGG.",".G..........",".GGGGGGGGGG.","..........G.",".GGGGGGGGGG.","....R.......","............"];
const SC={H:'#8cf5e3',G:'#3ee0c5',R:'#ff3d5a'};
const APPLE=["....G...","...GG...",".RRRRRR.","RRWRRRRR","RRWRRRRR","RRRRRRRR",".RRRRRR.","..RRRR.."];
const AP={R:'#ff3d5a',G:'#6be04f',W:'#fff1d0'};

/* ---------- FLAPPY ---------- */
function flappy(cv){
 const x=cv.getContext('2d'),W=160,H=240,G=216;
 let st,b,vy,pipes,sc,tick=0,dt=0,gs=0;
 function reset(){st='ready';b=100;vy=0;pipes=[];sc=0}
 reset();
 function flap(){if(st==='dead'){if(tick-dt>30)reset();return}if(st==='ready')st='play';vy=-2.5;beep(500,.12,'square',350)}
 function die(){st='dead';dt=tick;vy=-1;beep(300,.45,'sawtooth',-250,.07);best('flappy',sc)}
 function step(){tick++;
  if(st==='ready'){b=100+Math.sin(tick/10)*4;gs+=1.1;return}
  if(st==='dead'){vy+=.2;b=Math.min(b+vy,G-8);return}
  gs+=1.1;vy+=.14;b+=vy;
  if(!pipes.length||pipes[pipes.length-1].x<W-85)pipes.push({x:W,g:28+Math.random()*100|0});
  for(const p of pipes){p.x-=1.1;
   if(!p.ok&&p.x+22<40){p.ok=1;sc++;beep(880,.07);beep(1175,.1,'square',0,.05,.07)}
   if(48>p.x-2&&40<p.x+24&&(b+1<p.g||b+7>p.g+56))return die()}
  pipes=pipes.filter(p=>p.x>-30);
  if(b+8>=G){b=G-8;die()}else if(b<-10)b=-10}
 function draw(){
  ['#4fb3e8','#7fd6f5','#b5ecfb'].forEach((c,i)=>{x.fillStyle=c;x.fillRect(0,i*72,W,73)});
  x.fillStyle='#fff';for(let i=0;i<3;i++){const cx=((i*70-gs*.25)%210+210)%210-30,cy=30+i*45;x.fillRect(cx|0,cy,18,5);x.fillRect((cx+4)|0,cy-4,10,4)}
  pipes.forEach(p=>{const px=p.x|0,gb=p.g+56;
   x.fillStyle='#2f9e4a';x.fillRect(px,0,22,p.g);x.fillRect(px,gb,22,G-gb);
   x.fillStyle='#8df0a0';x.fillRect(px+3,0,3,p.g);x.fillRect(px+3,gb,3,G-gb);
   x.fillStyle='#1f6b34';x.fillRect(px+18,0,4,p.g);x.fillRect(px+18,gb,4,G-gb);
   x.fillStyle='#3fbf5a';x.fillRect(px-2,p.g-8,26,8);x.fillRect(px-2,gb,26,8);
   x.fillStyle='#8df0a0';x.fillRect(px,p.g-8,3,8);x.fillRect(px,gb,3,8)});
  x.fillStyle='#d9b36a';x.fillRect(0,G,W,H-G);x.fillStyle='#7ac74f';x.fillRect(0,G,W,4);
  x.fillStyle='#b8924a';for(let i=-1;i<22;i++){x.fillRect(i*8-(gs%8),G+9,4,3);x.fillRect(i*8+4-(gs%8),G+17,4,3)}
  x.save();x.translate(44,b+4);x.rotate(Math.max(-.4,Math.min(1.2,vy*.12)));x.translate(-6,-4);drawMap(x,BIRD,BC,0,0);x.restore();
  if(st!=='ready')txt(x,sc,80,28,'#fff1d0',14);
  if(st==='ready'){txt(x,'GET READY',80,70,'#ffd23f',10);txt(x,'TAP OR SPACE',80,150,'#fff',8)}
  if(st==='dead'){x.fillStyle='rgba(26,15,48,.85)';x.fillRect(14,76,132,76);txt(x,'GAME OVER',80,96,'#ff5c8a',10);txt(x,'SCORE '+sc,80,114);txt(x,'BEST '+best('flappy'),80,128,'#ffd23f');txt(x,'TAP TO RETRY',80,144,'#3ee0c5',6)}}
 return{reset,key:e=>{if(['Space','ArrowUp','KeyW'].includes(e.code))flap()},down:flap,stop:loop(step,draw)}}

/* ---------- SNAKE ---------- */
function snake(cv){
 const x=cv.getContext('2d'),N=20,S=8,KM={ArrowUp:[0,-1],KeyW:[0,-1],ArrowDown:[0,1],KeyS:[0,1],ArrowLeft:[-1,0],KeyA:[-1,0],ArrowRight:[1,0],KeyD:[1,0]};
 let s,d,q,food,sc,over,go,t,sp,sx=0,sy=0;
 function put(){do food=[Math.random()*N|0,Math.random()*N|0];while(s.some(p=>p[0]===food[0]&&p[1]===food[1]))}
 function reset(){s=[[10,10],[9,10],[8,10]];d=[1,0];q=[];sc=0;over=false;go=false;t=0;sp=7;put()}
 reset();
 function turn(a,b){const l=q.length?q[q.length-1]:d;if(a===-l[0]&&b===-l[1])return;go=true;if((a!==l[0]||b!==l[1])&&q.length<2)q.push([a,b])}
 function step(){if(over){t++;return}if(!go||++t<sp)return;t=0;
  if(q.length)d=q.shift();
  const h=[s[0][0]+d[0],s[0][1]+d[1]],eat=h[0]===food[0]&&h[1]===food[1];
  if(h[0]<0||h[1]<0||h[0]>=N||h[1]>=N||s.slice(0,eat?undefined:-1).some(p=>p[0]===h[0]&&p[1]===h[1])){over=true;t=0;beep(220,.5,'sawtooth',-170,.07);best('snake',sc);return}
  s.unshift(h);
  if(eat){sc++;sp=Math.max(3,7-(sc/4|0));put();beep(660,.07);beep(990,.1,'square',0,.05,.07)}else s.pop()}
 function draw(){
  x.fillStyle='#14092a';x.fillRect(0,0,160,160);x.fillStyle='#1d1038';
  for(let i=0;i<N;i++)for(let j=0;j<N;j++)if((i+j)%2)x.fillRect(i*S,j*S,S,S);
  drawMap(x,APPLE,AP,food[0]*S,food[1]*S);
  s.forEach((p,i)=>{const X=p[0]*S,Y=p[1]*S;
   if(i){x.fillStyle=i%2?'#3ee0c5':'#27b8a0';x.fillRect(X+1,Y+1,6,6)}
   else{x.fillStyle='#8cf5e3';x.fillRect(X,Y,S,S);x.fillStyle='#1a0f30';
    const e=d[0]?[[d[0]>0?4:2,1],[d[0]>0?4:2,5]]:[[1,d[1]>0?4:2],[5,d[1]>0?4:2]];e.forEach(k=>x.fillRect(X+k[0],Y+k[1],2,2))}});
  txt(x,'SCORE '+sc,80,9,'#fff1d0',8);
  if(!go){txt(x,'PRESS ARROWS',80,80,'#ffd23f',8);txt(x,'OR SWIPE',80,94,'#fff',8)}
  if(over){x.fillStyle='rgba(26,15,48,.88)';x.fillRect(14,50,132,64);txt(x,'GAME OVER',80,70,'#ff5c8a',10);txt(x,'BEST '+best('snake'),80,88,'#ffd23f');txt(x,'ANY KEY / TAP',80,104,'#3ee0c5',6)}}
 return{reset,key:e=>{if(over){if(t>25)reset();return}const m=KM[e.code];if(m)turn(m[0],m[1])},
  down:(a,b)=>{sx=a;sy=b},
  up:(a,b)=>{if(over){if(t>25)reset();return}const dx=a-sx,dy=b-sy;if(Math.abs(dx)<6&&Math.abs(dy)<6)return;Math.abs(dx)>Math.abs(dy)?turn(dx>0?1:-1,0):turn(0,dy>0?1:-1)},
  stop:loop(step,draw)}}

/* ---------- CHESS ---------- */
const KD=[[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]],ND=[[1,2],[2,1],[-1,2],[-2,1],[1,-2],[2,-1],[-1,-2],[-2,-1]];
const GL={k:'\u265A',q:'\u265B',r:'\u265C',b:'\u265D',n:'\u265E',p:'\u265F\uFE0E'},V={p:1,n:3,b:3,r:5,q:9,k:0};
function gen(b,i){const p=b[i],c=p[0],t=p[1],r=i>>3,f=i&7,m=[];
 const add=(R,F)=>{if(R<0||R>7||F<0||F>7)return 0;const q=b[R*8+F];if(q&&q[0]===c)return 0;m.push(R*8+F);return !q};
 if(t==='p'){const d=c==='w'?-1:1,R=r+d;if(R>=0&&R<8){if(!b[R*8+f]){m.push(R*8+f);if(r===(c==='w'?6:1)&&!b[(r+2*d)*8+f])m.push((r+2*d)*8+f)}
  for(const e of[-1,1]){const F=f+e;if(F>=0&&F<8){const q=b[R*8+F];if(q&&q[0]!==c)m.push(R*8+F)}}}}
 else if(t==='n'||t==='k')(t==='n'?ND:KD).forEach(a=>add(r+a[0],f+a[1]));
 else(t==='r'?KD.slice(0,4):t==='b'?KD.slice(4):KD).forEach(a=>{for(let k=1;add(r+a[0]*k,f+a[1]*k);k++);});
 return m}
function inCheck(b,c){const k=b.indexOf(c+'k');return k>=0&&b.some((p,i)=>p&&p[0]!==c&&gen(b,i).includes(k))}
function legal(b,i){return gen(b,i).filter(j=>{const n=b.slice();n[j]=n[i];n[i]=null;return !inCheck(n,b[i][0])})}
function chess(cv){
 const x=cv.getContext('2d'),SQ=20;
 let B,turn,sel,mv,msg,over,cpu=true,busy,dead=false,tm;
 function init(){clearTimeout(tm);B=Array(64).fill(null);const o='rnbqkbnr';for(let i=0;i<8;i++){B[i]='b'+o[i];B[8+i]='bp';B[48+i]='wp';B[56+i]='w'+o[i]}turn='w';sel=-1;mv=[];over=false;busy=false;upd()}
 function upd(){const ck=inCheck(B,turn),any=B.some((p,i)=>p&&p[0]===turn&&legal(B,i).length);
  if(!any){over=true;msg=ck?'CHECKMATE! '+(turn==='w'?'BLACK':'WHITE')+' WINS':'STALEMATE'}
  else msg=(turn==='w'?'WHITE':'BLACK')+' TO MOVE'+(ck?' - CHECK':'')}
 function move(i,j){const cap=B[j];B[j]=B[i];B[i]=null;if(B[j][1]==='p'&&(j<8||j>55))B[j]=B[j][0]+'q';
  sel=-1;mv=[];turn=turn==='w'?'b':'w';upd();
  if(over)[523,659,784,1047].forEach((f,k)=>beep(f,.18,'square',0,.05,k*.12));
  else beep(cap?160:380,cap?.14:.06,cap?'sawtooth':'triangle',0,.07)}
 function cpuMove(){busy=true;tm=setTimeout(()=>{if(dead)return;const ms=[];
  B.forEach((p,i)=>{if(p&&p[0]==='b')legal(B,i).forEach(j=>{const n=B.slice();n[j]=n[i];n[i]=null;
   const hang=n.some((q,k)=>q&&q[0]==='w'&&gen(n,k).includes(j));
   ms.push([i,j,(B[j]?V[B[j][1]]*10:0)+Math.random()*4-(hang?V[p[1]]*8:0)])})});
  busy=false;if(ms.length){ms.sort((a,b)=>b[2]-a[2]);move(ms[0][0],ms[0][1])}},500)}
 init();
 function draw(){
  for(let i=0;i<64;i++){const X=(i&7)*SQ,Y=(i>>3)*SQ,p=B[i],tg=mv.includes(i);
   x.fillStyle=((i>>3)+(i&7))%2?'#7a5bb0':'#fff1d0';x.fillRect(X,Y,SQ,SQ);
   if(i===sel){x.fillStyle='#ffd23f';x.fillRect(X,Y,SQ,SQ)}
   if(tg&&p){x.fillStyle='rgba(255,92,138,.7)';x.fillRect(X,Y,SQ,SQ)}
   if(p){x.font='18px "Segoe UI Symbol","Noto Sans Symbols 2","DejaVu Sans",serif';x.textAlign='center';x.textBaseline='middle';
    x.lineWidth=p[0]==='w'?2:1;x.strokeStyle=p[0]==='w'?'#1a0f30':'#fff1d0';x.fillStyle=p[0]==='w'?'#ffffff':'#1a0f30';
    x.strokeText(GL[p[1]],X+10,Y+11);x.fillText(GL[p[1]],X+10,Y+11)}
   if(tg&&!p){x.fillStyle='#ff5c8a';x.fillRect(X+8,Y+8,4,4)}}
  x.fillStyle='#241640';x.fillRect(0,160,160,16);txt(x,msg,80,172,over?'#ffd23f':'#fff1d0',6)}
 const stopLoop=loop(()=>{},draw);
 return{reset:()=>{init();if(cpu&&turn==='b')cpuMove()},draw,
  opt:{label:()=>'Mode: '+(cpu?'vs CPU':'2 players'),click:()=>{cpu=!cpu;if(cpu&&turn==='b'&&!over&&!busy)cpuMove()}},
  down:(px,py)=>{if(over||busy||py>=160)return;const i=(py/SQ|0)*8+(px/SQ|0);
   if(sel>=0&&mv.includes(i)){move(sel,i);if(!over&&cpu&&turn==='b')cpuMove()}
   else if(B[i]&&B[i][0]===turn){sel=i;mv=legal(B,i);beep(520,.04,'triangle',0,.04)}else{sel=-1;mv=[]}},
  stop:()=>{dead=true;clearTimeout(tm);return stopLoop()}}}

/* ---------- Manager ---------- */
const GAMES={flappy:{t:'Flappy Pixel',w:160,h:240,f:flappy,tip:'Space, click or tap to flap'},snake:{t:'Pixel Snake',w:160,h:160,f:snake,tip:'Arrow keys / WASD, or swipe'},chess:{t:'Pixel Chess',w:160,h:176,f:chess,tip:'Click a piece, then a square. No castling or en passant.'}};
let cur=null;const $=id=>document.getElementById(id),cv=$('cv');
function fit(){if(!cur)return;const g=cur.g,s=Math.max(1,Math.min((innerWidth-40)/g.w,(innerHeight-170)/g.h));cv.style.width=g.w*s+'px';cv.style.height=g.h*s+'px'}
function play(k){const g=GAMES[k];cv.width=g.w;cv.height=g.h;cur=g.f(cv);cur.g=g;$('ptitle').textContent=g.t;$('phint').textContent=g.tip;
 $('bopt').hidden=!cur.opt;if(cur.opt)$('bopt').textContent=cur.opt.label();$('player').classList.add('on');fit();cv.focus()}
function close(){if(cur){cur.stop();cur=null}$('player').classList.remove('on')}
document.querySelectorAll('.game').forEach(b=>b.onclick=()=>play(b.dataset.g));
$('bclose').onclick=close;
$('brest').onclick=e=>{cur&&cur.reset();e.target.blur();cv.focus()};
$('bmute').onclick=e=>{muted=!muted;e.target.textContent='Sound: '+(muted?'off':'on');e.target.blur();cv.focus()};
$('bopt').onclick=e=>{cur.opt.click();e.target.textContent=cur.opt.label();e.target.blur();cv.focus()};
addEventListener('keydown',e=>{if(!cur)return;if(e.key==='Escape')return close();
 if(['Space','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.code))e.preventDefault();cur.key&&cur.key(e)});
const pt=e=>{const r=cv.getBoundingClientRect();return[(e.clientX-r.left)*cv.width/r.width,(e.clientY-r.top)*cv.height/r.height]};
cv.addEventListener('pointerdown',e=>{if(cur&&cur.down)cur.down(...pt(e))});
cv.addEventListener('pointerup',e=>{if(cur&&cur.up)cur.up(...pt(e))});
addEventListener('resize',fit);
document.querySelectorAll('.thumb').forEach(c=>{const t=c.getContext('2d'),k=c.dataset.t;
 if(k==='flappy')drawMap(t,BIRD,BC,0,0);else if(k==='snake')drawMap(t,SN,SC,0,0);
 else for(let i=0;i<3;i++)for(let j=0;j<2;j++){t.fillStyle=(i+j)%2?'#ff5c8a':'#fff1d0';t.fillRect(i*4,j*4,4,4)}});
})();
</script>
</body>
</html>
'''.encode("utf-8")

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("?")[0] in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(PAGE)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(PAGE)
        else:
            self.send_error(404)
    def log_message(self, *a):
        pass

socketserver.TCPServer.allow_reuse_address = True
httpd = None
for port in range(8000, 8010):
    try:
        httpd = socketserver.TCPServer(("", port), Handler)
        break
    except OSError:
        print(f"Port {port} is busy, trying the next one...")
if httpd is None:
    sys.exit("ERROR: no free port between 8000 and 8009.")

url = f"http://localhost:{port}"
print(f"\nOpen this in your browser: {url}  (Ctrl+C to stop)\n")
try:
    webbrowser.open(url)
except Exception:
    pass
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped.")

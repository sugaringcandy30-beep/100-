import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="메이플 비치 자산관리 RPG", page_icon="🍁", layout="centered")

st.title("🏙️ 모던 픽셀 비치 & 뉴스/미니게임 RPG")
st.caption("방향키(A, D)로 이동, Space키로 점프! 건물 입구 포탈[▲ / W]로 들어간 뒤 카운터에서 미니게임에 도전하세요.")

game_html = """
<!DOCTYPE html>
<html>
<head>
<style>
    @import url('https://fonts.googleapis.com/css2?family=NeoDunggeunmo&display=swap');

    body {
        margin: 0;
        padding: 0;
        background-color: #0d111a;
        color: white;
        font-family: 'NeoDunggeunmo', 'Courier New', monospace;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    #newsTickerBox {
        width: 600px;
        background: #1e293b;
        color: #f1c40f;
        font-size: 13px;
        font-weight: bold;
        padding: 10px 16px;
        border-radius: 12px 12px 0 0;
        border: 2px solid #3d5af1;
        border-bottom: none;
        box-sizing: border-box;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    #newsTag {
        background: #e74c3c;
        color: white;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 11px;
        white-space: nowrap;
    }
    #newsText {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    #gameContainer {
        position: relative;
    }
    canvas {
        border: 2px solid #3d5af1;
        border-radius: 0 0 14px 14px;
        background-color: #0b0e17;
        box-shadow: 0 12px 35px rgba(0,0,0,0.8);
        image-rendering: pixelated;
    }
    #uiBox {
        width: 600px;
        background: #121824;
        padding: 16px;
        border-radius: 12px;
        margin-top: 12px;
        box-sizing: border-box;
        border: 2px solid #3d5af1;
        box-shadow: 0 6px 20px rgba(0,0,0,0.6);
    }
    .status-bar {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
        font-weight: bold;
        color: #f1c40f;
        font-size: 14px;
    }
    #progressContainer {
        width: 100%;
        height: 16px;
        background: #1a2235;
        border-radius: 8px;
        position: relative;
        overflow: hidden;
        border: 1px solid #3d5af1;
        margin-bottom: 12px;
    }
    #progressBar {
        width: 1%;
        height: 100%;
        background: linear-gradient(90deg, #3d5af1, #00b894);
        transition: width 0.4s ease;
    }
    #progressText {
        position: absolute;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        font-size: 11px;
        text-align: center;
        line-height: 16px;
        color: white;
        font-weight: bold;
        text-shadow: 0 1px 2px rgba(0,0,0,0.8);
    }
    .action-btn {
        background: linear-gradient(135deg, #3d5af1, #2e3e91);
        color: white;
        border: 1px solid #7085ff;
        padding: 10px 16px;
        margin: 4px;
        border-radius: 8px;
        cursor: pointer;
        font-family: 'NeoDunggeunmo', sans-serif;
        font-size: 14px;
        box-shadow: 0 4px 10px rgba(61,90,241,0.3);
    }
    .action-btn:hover {
        transform: translateY(-2px);
    }
    .enter-btn {
        background: linear-gradient(135deg, #00b894, #00896f);
        color: white;
        border: 1px solid #55efc4;
        padding: 10px 20px;
        border-radius: 8px;
        cursor: pointer;
        font-family: 'NeoDunggeunmo', sans-serif;
        font-size: 15px;
        box-shadow: 0 4px 12px rgba(0,184,148,0.3);
    }
    .exit-btn {
        background: linear-gradient(135deg, #d63031, #a72828);
        color: white;
        border: 1px solid #ff7675;
        padding: 8px 16px;
        border-radius: 8px;
        cursor: pointer;
        font-family: 'NeoDunggeunmo', sans-serif;
    }
    .controls {
        display: grid;
        grid-template-columns: repeat(4, 70px);
        gap: 10px;
        justify-content: center;
        margin-top: 14px;
    }
    .ctrl-btn {
        width: 70px;
        height: 52px;
        font-size: 16px;
        font-family: 'NeoDunggeunmo', sans-serif;
        background: #181f2c;
        color: #f1c40f;
        border: 2px solid #3d5af1;
        border-radius: 10px;
        cursor: pointer;
        box-shadow: 0 4px 0 #283780;
    }
    .ctrl-btn:active {
        transform: translateY(2px);
        box-shadow: none;
    }
    #dialogue {
        min-height: 52px;
        background: #0d121c;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #283780;
        margin-top: 6px;
        font-size: 14px;
        line-height: 1.5;
    }
    /* 미니게임 전용 UI 상자 */
    #minigameBox {
        display: none;
        background: #0b0e17;
        border: 2px solid #f1c40f;
        border-radius: 10px;
        padding: 14px;
        margin-top: 10px;
        text-align: center;
    }
    #meterBar {
        width: 100%;
        height: 26px;
        background: #1a2235;
        border-radius: 13px;
        position: relative;
        overflow: hidden;
        margin: 12px 0;
        border: 1px solid #3d5af1;
    }
    #meterIndicator {
        width: 16px;
        height: 100%;
        background: #ff7675;
        position: absolute;
        left: 0;
        border-radius: 4px;
    }
    #targetZone {
        width: 80px;
        height: 100%;
        background: #00b894;
        position: absolute;
        left: 230px;
        opacity: 0.85;
    }
</style>
</head>
<body>

<div id="newsTickerBox">
    <span id="newsTag">속보 찌라시</span>
    <span id="newsText">시티 금융 시장 개장! 각 건물의 담당자와 상담해보세요.</span>
</div>

<div id="gameContainer">
    <canvas id="gameCanvas" width="600" height="380"></canvas>
</div>

<div id="uiBox">
    <div class="status-bar">
        <span>📍 위치: <span id="locationText">메인 스트리트</span></span>
        <span>📅 턴: <span id="turnText">1</span>/12</span>
        <span>💰 자산: <span id="moneyText">1,000,000</span>원</span>
    </div>

    <div id="progressContainer">
        <div id="progressBar"></div>
        <div id="progressText">1억 원 목표 달성도: 1%</div>
    </div>

    <div id="dialogue">💬 방향키로 대형 스트리트 건물을 탐험하고 입구 포탈[▲ / W]을 이용해보세요.</div>
    
    <div id="minigameBox">
        <div id="minigameTitle" style="color:#f1c40f; font-weight:bold; font-size: 15px;">🎯 타이밍 게이지 미니게임</div>
        <div id="meterBar">
            <div id="targetZone"></div>
            <div id="meterIndicator"></div>
        </div>
        <button class="action-btn" style="background: linear-gradient(135deg, #e74c3c, #c0392b);" onclick="stopMeter()">🎯 STOP (타이밍 맞추기)</button>
    </div>

    <div id="actionArea" style="margin-top: 8px; text-align: center;"></div>
</div>

<div class="controls">
    <button class="ctrl-btn" onclick="moveLeft()">◄ 이동</button>
    <button class="ctrl-btn" onclick="jump()">▲ 점프</button>
    <button class="ctrl-btn" onclick="moveRight()">이동 ►</button>
    <button class="ctrl-btn" style="background:#00b894; color:white; border-color:#55efc4;" onclick="interactPortal()">▲ 포탈</button>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let money = 1000000;
let turn = 1;
let currentScene = 'town';
let ownedBuildings = [];
const goalMoney = 100000000;

let currentNews = { text: "시티 금융 시장이 개장했습니다.", stockMod: 0, cryptoMod: 0 };
const newsEvents = [
    { text: "🔥 [찌라시] AI 반도체 대형 호재 터졌다! 주식 승률 극대화!", stockMod: 0.4, cryptoMod: 0 },
    { text: "📉 [찌라시] 가상자산 규제 단속 개시! 코인 위험 주의보!", stockMod: 0, cryptoMod: -0.3 },
    { text: "🚀 [찌라시] 유동성 자금 전격 공급! 전 시장 폭등 가능성!", stockMod: 0.25, cryptoMod: 0.3 },
    { text: "⚠️ [찌라시] 글로벌 금리 인상 속보! 자산 시장 위축 우려!", stockMod: -0.2, cryptoMod: -0.2 }
];

const player = {
    x: 100,
    y: 250,
    vx: 0,
    vy: 0,
    speed: 6,
    jumpPower: -12,
    groundY: 250,
    isGrounded: true,
    facing: 'right',
    animFrame: 0,
    name: '투자자'
};

const buildings = [
    { id: 'bank', name: '🏦 네오 중앙은행', x: 100, portalX: 175, colorMain: '#1e272e', accent: '#00b894' },
    { id: 'stock', name: '📈 메트로 증권타워', x: 380, portalX: 455, colorMain: '#1e272e', accent: '#3d5af1' },
    { id: 'crypto', name: '🚀 사이버 코인랩', x: 660, portalX: 735, colorMain: '#1e272e', accent: '#ff7675' },
    { id: 'realty', name: '🏢 스카이 부동산', x: 940, portalX: 1015, colorMain: '#1e272e', accent: '#f1c40f' }
];

const interiorNPCs = {
    bank: { x: 300, y: 220, name: '🏦 은행 딜러 김수호' },
    stock: { x: 300, y: 220, name: '📈 펀드매니저 박차트' },
    crypto: { x: 300, y: 220, name: '🚀 코인 애널리스트 나대박' },
    realty: { x: 300, y: 220, name: '🏢 부동산 디벨로퍼 최건물' }
};

let cameraX = 0;
let portalAnim = 0;
let keys = {};

let meterPos = 0;
let meterSpeed = 5;
let meterActive = false;
let meterAnimId = null;

document.addEventListener('keydown', (e) => {
    keys[e.key] = true;
    if ((e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') && currentScene === 'town') {
        interactPortal();
    }
    if ((e.key === ' ' || e.key === 'Spacebar') && player.isGrounded) {
        jump();
    }
});
document.addEventListener('keyup', (e) => { keys[e.key] = false; });

function moveLeft() { player.vx = -player.speed; player.facing = 'left'; }
function moveRight() { player.vx = player.speed; player.facing = 'right'; }

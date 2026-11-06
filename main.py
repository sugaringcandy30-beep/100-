import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="메이플 비치 자산관리 RPG", page_icon="🍁", layout="wide")

st.title("🏙️ 모던 벡터 시티 & 투자 RPG")
st.caption("방향키(A, D)로 이동, Space키로 점프! 증권타워에 명확한 '보유 주식 현황판' 칸이 추가되었습니다.")

game_html = """
<!DOCTYPE html>
<html>
<head>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700&display=swap');

    body {
        margin: 0;
        padding: 0;
        background-color: #0b0f19;
        color: #f8fafc;
        font-family: 'Pretendard', sans-serif;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    #newsTickerBox {
        width: 840px;
        background: rgba(30, 41, 59, 0.75);
        backdrop-filter: blur(10px);
        color: #38bdf8;
        font-size: 14px;
        font-weight: 600;
        padding: 10px 18px;
        border-radius: 16px 16px 0 0;
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-bottom: none;
        box-sizing: border-box;
        display: flex;
        align-items: center;
        gap: 12px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    #newsTag {
        background: linear-gradient(135deg, #f43f5e, #e11d48);
        color: white;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: -0.5px;
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
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 0 0 16px 16px;
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
        outline: none;
    }
    #uiBox {
        width: 840px;
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(12px);
        padding: 16px 20px;
        border-radius: 16px;
        margin-top: 12px;
        box-sizing: border-box;
        border: 1px solid rgba(56, 189, 248, 0.25);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .status-bar {
        display: flex;
        justify-content: space-between;
        margin-bottom: 10px;
        font-weight: 600;
        color: #e2e8f0;
        font-size: 14px;
    }
    #progressContainer {
        width: 100%;
        height: 20px;
        background: rgba(30, 41, 59, 0.8);
        border-radius: 10px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(56, 189, 248, 0.2);
        margin-bottom: 10px;
    }
    #progressBar {
        width: 1%;
        height: 100%;
        background: linear-gradient(90deg, #3b82f6, #10b981);
        transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border-radius: 10px;
    }
    #progressText {
        position: absolute;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        font-size: 11px;
        text-align: center;
        line-height: 20px;
        color: white;
        font-weight: 600;
        text-shadow: 0 1px 2px rgba(0,0,0,0.6);
    }
    .action-btn {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        border: none;
        padding: 5px 10px;
        margin: 2px;
        border-radius: 6px;
        cursor: pointer;
        font-family: 'Pretendard', sans-serif;
        font-size: 12px;
        font-weight: 600;
        box-shadow: 0 2px 6px rgba(59, 130, 246, 0.4);
        transition: all 0.15s ease;
    }
    .action-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 10px rgba(59, 130, 246, 0.6);
    }
    .sell-btn {
        background: linear-gradient(135deg, #f43f5e, #e11d48);
        color: white;
        border: none;
        padding: 5px 10px;
        margin: 2px;
        border-radius: 6px;
        cursor: pointer;
        font-family: 'Pretendard', sans-serif;
        font-size: 12px;
        font-weight: 600;
        box-shadow: 0 2px 6px rgba(244, 63, 94, 0.4);
    }
    .enter-btn {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        border: none;
        padding: 10px 22px;
        border-radius: 10px;
        cursor: pointer;
        font-family: 'Pretendard', sans-serif;
        font-size: 15px;
        font-weight: 600;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4);
    }
    .exit-btn {
        background: linear-gradient(135deg, #64748b, #475569);
        color: white;
        border: none;
        padding: 8px 16px;
        margin: 4px;
        border-radius: 8px;
        cursor: pointer;
        font-family: 'Pretendard', sans-serif;
        font-size: 13px;
        font-weight: 600;
    }
    .restart-btn {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 10px;
        cursor: pointer;
        font-family: 'Pretendard', sans-serif;
        font-size: 16px;
        font-weight: 700;
        box-shadow: 0 6px 20px rgba(245, 158, 11, 0.5);
        transition: all 0.2s ease;
    }
    .controls {
        display: grid;
        grid-template-columns: repeat(4, 90px);
        gap: 12px;
        justify-content: center;
        margin-top: 14px;
    }
    .ctrl-btn {
        width: 90px;
        height: 50px;
        font-size: 15px;
        font-weight: 600;
        font-family: 'Pretendard', sans-serif;
        background: rgba(30, 41, 59, 0.9);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 12px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        transition: all 0.1s ease;
    }
    .ctrl-btn:active {
        transform: translateY(2px);
        background: rgba(56, 189, 248, 0.2);
    }
    #dialogue {
        min-height: 40px;
        background: rgba(15, 23, 42, 0.6);
        padding: 10px 14px;
        border-radius: 10px;
        border: 1px solid rgba(56, 189, 248, 0.15);
        margin-top: 6px;
        font-size: 14px;
        line-height: 1.5;
        color: #cbd5e1;
    }
    .stock-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 8px;
        padding: 6px 10px;
        margin-bottom: 4px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .stock-input {
        width: 45px;
        background: #0f172a;
        border: 1px solid rgba(56, 189, 248, 0.4);
        color: white;
        text-align: center;
        border-radius: 4px;
        padding: 2px;
        font-size: 12px;
    }
    .portfolio-item {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 5px 8px;
        margin-bottom: 4px;
        border-radius: 6px;
        font-size: 11px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #e2e8f0;
    }
</style>
</head>
<body>

<div id="newsTickerBox">
    <span id="newsTag">실시간 속보</span>
    <span id="newsText">모던 벡터 시티 금융 시장이 개장했습니다. 초기자금 500만 원으로 투자를 시작하세요!</span>
</div>

<div id="gameContainer">
    <canvas id="gameCanvas" width="840" height="480" tabindex="1"></canvas>
</div>

<div id="uiBox">
    <div class="status-bar">
        <span>📍 위치: <span id="locationText" style="color: #38bdf8;">메인 스트리트</span></span>
        <span>☀️ 시간대: <span id="dayNightText" style="color: #fbbf24;">아침 🌅</span></span>
        <span>📅 턴: <span id="turnText">1</span>/12</span>
        <span>💰 총 자산: <span id="moneyText" style="color: #10b981;">5,000,000</span>원 (현금: <span id="cashText" style="color: #38bdf8;">5,000,000</span>원)</span>
    </div>

    <div id="progressContainer">
        <div id="progressBar"></div>
        <div id="progressText">1억 원 목표 달성도: 5%</div>
    </div>

    <div id="dialogue">💬 방향키로 세련된 벡터 빌딩들을 탐험하고 입구 포탈[▲ / W]로 입장해보세요.</div>
    <div id="actionArea" style="margin-top: 8px; text-align: center;"></div>
</div>

<div class="controls">
    <button class="ctrl-btn" onclick="moveLeft()">◄ 이동</button>
    <button class="ctrl-btn" onclick="jump()">▲ 점프</button>
    <button class="ctrl-btn" onclick="moveRight()">이동 ►</button>
    <button class="ctrl-btn" style="color: #10b981; border-color: rgba(16, 185, 129, 0.4);" onclick="interactPortal()">▲ 포탈</button>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

window.addEventListener('load', () => {
    canvas.focus();
});

let cash = 5000000;
let turn = 1;
let isDay = true;
let currentScene = 'town';
let ownedBuildings = [];
const goalMoney = 100000000;
let isGameOver = false;
let gameResult = '';

let stocks = [
    { id: 'neotech', name: '🚀 네오 테크', price: 45000, prevPrice: 45000, owned: 0, totalCost: 0, volatility: 0.32 },
    { id: 'bluechips', name: '🛡️ 블루 칩스', price: 120000, prevPrice: 120000, owned: 0, totalCost: 0, volatility: 0.08 },
    { id: 'cyberenergy', name: '⚡ 사이버 에너지', price: 18000, prevPrice: 18000, owned: 0, totalCost: 0, volatility: 0.24 },
    { id: 'biocore', name: '🧬 바이오 코어', price: 32000, prevPrice: 32000, owned: 0, totalCost: 0, volatility: 0.40 },
    { id: 'pixelgame', name: '🎮 픽셀 게임즈', price: 15000, prevPrice: 15000, owned: 0, totalCost: 0, volatility: 0.28 },
    { id: 'quantumsem', name: '💻 퀀텀 반도체', price: 75000, prevPrice: 75000, owned: 0, totalCost: 0, volatility: 0.18 }
];

let floatingTexts = [];
let newsArchive = [
    "[턴 1] 모던 벡터 시티 증권 시장에 6개 우량 및 성장 섹터가 동시 상장되었습니다."
];

let currentNews = { text: "모던 벡터 시티 증권 시장에 6개 우량 및 성장 섹터가 동시 상장되었습니다.", stockMod: 0 };

const newsEvents = [
    { text: "🔥 [특보] 차세대 기술 혁신 펀드 유입으로 성장 테크 및 반도체 섹터의 강한 상승세가 예상됩니다.", stockMod: 0.26 },
    { text: "📉 [긴급] 글로벌 원자재 공급망 차질 우려... 방어주와 에너지 중심으로 리스크 관리가 필요합니다.", stockMod: -0.20 },
    { text: "🚀 [속보] 확장적 통화 정책 시행 임박... 전반적인 증시 유동성 랠리가 기대됩니다.", stockMod: 0.30 },
    { text: "⚠️ [경고] 금리 인상 기조 장기화 우려로 투자 심리가 위축되며 변동성이 확대될 전망입니다.", stockMod: -0.16 }
];

const player = {
    x: 120,
    y: 320,
    vx: 0,
    vy: 0,
    speed: 7,
    jumpPower: -13,
    groundY: 320,
    isGrounded: true,
    facing: 'right',
    animFrame: 0,
    name: '투자자'
};

const buildings = [
    { id: 'bank', name: '🏦 네오 중앙은행', x: 120, portalX: 220, colorMain: '#1e293b', accent: '#10b981' },
    { id: 'stock', name: '📈 메트로 증권타워', x: 500, portalX: 600, colorMain: '#1e293b', accent: '#3b82f6' },
    { id: 'crypto', name: '🚀 사이버 코인랩', x: 880, portalX: 980, colorMain: '#1e293b', accent: '#f43f5e' },
    { id: 'realty', name: '🏢 스카이 부동산', x: 1260, portalX: 1360, colorMain: '#1e293b', accent: '#fbbf24' }
];

const interiorNPCs = {
    bank: { x: 420, y: 290, name: '🏦 은행 딜러 김수호' },
    stock: { x: 420, y: 290, name: '📈 펀드매니저 박차트' },
    crypto: { x: 420, y: 290, name: '🚀 코인 애널리스트 나대박' },
    realty: { x: 420, y: 290, name: '🏢 부동산 디벨로퍼 최건물' }
};

let cameraX = 0;
let portalAnim = 0;
let keys = {};
let lastProximityKey = null;

let isCryptoGameActive = false;
let cryptoMultiplier = 1.0;
let cryptoGameInterval = null;

document.addEventListener('keydown', (e) => {
    if (isGameOver) return;
    if(["Space","ArrowUp","ArrowDown","ArrowLeft","ArrowRight"].indexOf(e.code) > -1) {
        e.preventDefault();
    }
    keys[e.key] = true;
   
    if ((e.key === ' ' || e.key === 'Spacebar') && isCryptoGameActive) {
        stopCryptoMinigame();
        return;
    }

    if ((e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') && currentScene === 'town') {
        interactPortal();
    }
    if ((e.key === ' ' || e.key === 'Spacebar') && player.isGrounded && !isCryptoGameActive) {
        jump();
    }
});
document.addEventListener('keyup', (e) => { keys[e.key] = false; });

function moveLeft() { if (!isGameOver && !isCryptoGameActive) { player.vx = -player.speed; player.facing = 'left'; } }
function moveRight() { if (!isGameOver && !isCryptoGameActive) { player.vx = player.speed; player.facing = 'right'; } }
function jump() {
    if (!isGameOver && player.isGrounded && !isCryptoGameActive) {
        player.vy = player.jumpPower;
        player.isGrounded = false;
    }
}

function getTotalAssets() {
    let stockValue = stocks.reduce((sum, s) => sum + (s.owned * s.price), 0);
    return cash + stockValue;
}

function restartGame() {
    cash = 5000000;
    turn = 1;
    isDay = true;
    currentScene = 'town';
    ownedBuildings = [];
    isGameOver = false;
    gameResult = '';
    isCryptoGameActive = false;
    if (cryptoGameInterval) clearInterval(cryptoGameInterval);
    floatingTexts = [];
    newsArchive = ["[턴 1] 모던 벡터 시티 증권 시장에 6개 우량 및 성장 섹터가 동시 상장되었습니다."];
    currentNews = { text: "모던 벡터 시티 증권 시장에 6개 우량 및 성장 섹터가 동시 상장되었습니다.", stockMod: 0 };
   
    stocks.forEach(s => {
        s.owned = 0;
        s.totalCost = 0;
    });
    stocks[0].price = 45000; stocks[0].prevPrice = 45000;
    stocks[1].price = 120000; stocks[1].prevPrice = 120000;
    stocks[2].price = 18000; stocks[2].prevPrice = 18000;
    stocks[3].price = 32000; stocks[3].prevPrice = 32000;
    stocks[4].price = 15000; stocks[4].prevPrice = 15000;
    stocks[5].price = 75000; stocks[5].prevPrice = 75000;

    player.x = 120;
    player.y = 320;
    document.getElementById('locationText').innerText = '메인 스트리트';
    lastProximityKey = null;
    updateUI();
    checkProximity();
    canvas.focus();
}

function addFloatingText(amount) {
    let text = amount >= 0 ? `+${amount.toLocaleString()}원` : `-${Math.abs(amount).toLocaleString()}원`;
    let color = amount >= 0 ? '#10b981' : '#f43f5e';
    floatingTexts.push({
        x: player.x,
        y: player.y - 60,
        text: text,
        color: color,
        opacity: 1.0,
        vy: -1.5
    });
}

function interactPortal() {
    if (isGameOver || currentScene !== 'town') return;
    for (let b of buildings) {
        if (Math.abs(player.x - b.portalX) < 55) {
            enterBuilding(b.id);
            return;
        }
    }
}

function enterBuilding(bId) {
    if (isGameOver) return;
    currentScene = bId;
    player.x = 120;
    player.y = 320;
    lastProximityKey = null;
    const bObj = buildings.find(b => b.id === bId);
    document.getElementById('locationText').innerText = bObj.name;
    canvas.focus();
    checkProximity();
}

function exitBuilding() {
    if (isGameOver) return;
    if (isCryptoGameActive) {
        isCryptoGameActive = false;
        if (cryptoGameInterval) clearInterval(cryptoGameInterval);
    }
    let bObj = buildings.find(b => b.id === currentScene);
    currentScene = 'town';
    player.x = bObj.portalX;
    player.y = 320;
    lastProximityKey = null;
    document.getElementById('locationText').innerText = '메인 스트리트';
    canvas.focus();
    checkProximity();
}

function triggerGameOver(result) {
    isGameOver = true;
    gameResult = result;
    isCryptoGameActive = false;
    if (cryptoGameInterval) clearInterval(cryptoGameInterval);
    const actionArea = document.getElementById('actionArea');
    const dialogue = document.getElementById('dialogue');
   
    if (gameResult === 'win') {
        dialogue.innerHTML = "🎉 <b>축하합니다! 1억 원을 달성하여 강남 건물주가 되었습니다!</b>";
    } else {
        dialogue.innerHTML = "❌ <b>12턴이 모두 종료되었습니다. 목표 금액 미달성으로 패배했습니다!</b>";
    }
    actionArea.innerHTML = `<button class="restart-btn" onclick="restartGame()">🔄 다시하기 (RESTART)</button>`;
}

function checkProximity() {
    const actionArea = document.getElementById('actionArea');
    const dialogue = document.getElementById('dialogue');

    if (isGameOver) {
        triggerGameOver(gameResult);
        return;
    }

    if (currentScene === 'town') {
        let nearB = buildings.find(b => Math.abs(player.x - b.portalX) < 55);
        let stateKey = nearB ? 'town_' + nearB.id : 'town_none';

        if (lastProximityKey !== stateKey) {
            lastProximityKey = stateKey;
            if (nearB) {
                dialogue.innerHTML = `✨ <b>[${nearB.name}] 입구입니다!</b> [▲ / W]키나 아래 버튼으로 입장하세요!`;
                actionArea.innerHTML = `<button class="enter-btn" onclick="enterBuilding('${nearB.id}')">🚪 건물 입장하기</button>`;
            } else {
                dialogue.innerHTML = "💬 방향키로 세련된 벡터 빌딩들을 탐험하고 입구 포탈로 들어가보세요!";
                actionArea.innerHTML = "";
            }
        }
    } else {
        let npc = interiorNPCs[currentScene];
        let dist = Math.abs(player.x - npc.x);
        let zone = player.x < 70 ? 'exit' : (dist < 100 ? 'npc' : 'walk');
        let stateKey = currentScene + '_' + zone;

        if (lastProximityKey !== stateKey) {
            lastProximityKey = stateKey;
            if (zone === 'exit') {
                dialogue.innerHTML = "🚪 메인 스트리트로 나가는 출구입니다.";
                actionArea.innerHTML = `<button class="exit-btn" onclick="exitBuilding()">🚪 밖으로 나가기</button>`;
            } else if (zone === 'npc') {
                dialogue.innerHTML = `💬 <b>${npc.name}</b>: "어서오세요! 원하시는 서비스를 선택해 주세요."`;
                renderDialogueOptions(currentScene);
            } else {
                dialogue.innerHTML = `🏢 컨설팅 데스크로 가까이 다가가세요.`;
                actionArea.innerHTML = `<button class="exit-btn" onclick="exitBuilding()">🚪 밖으로 나가기</button>`;
            }
        }
    }
}

function renderDialogueOptions(type) {
    const actionArea = document.getElementById('actionArea');
    if (type === 'bank') {
        actionArea.innerHTML = `<button class="action-btn" onclick="investBank()">🏦 예금 가입 (+5% 확정 수익 & 턴 진행)</button> <button class="exit-btn" onclick="exitBuilding()">🚪 나가기</button>`;
    } else if (type === 'stock') {
        renderStockMarketUI();
    } else if (type === 'crypto') {
        if (!isCryptoGameActive) {
            actionArea.innerHTML = `
                <button class="action-btn" style="background: linear-gradient(135deg, #f43f5e, #e11d48); padding: 8px 20px; font-size: 14px;" onclick="startCryptoMinigame()">🚀 초고속 사이버 코인 미니게임 시작 (스페이스바로 매도!)</button>
                <div style="margin-top: 6px;"><button class="exit-btn" onclick="exitBuilding()">🚪 나가기</button></div>
            `;
        }
    } else if (type === 'realty') {
        actionArea.innerHTML = `
            <button class="action-btn" onclick="buyBuilding('초역세권 오피스텔', 30000000, 2000000)">🏠 오피스텔 (3천만 / 월세 200만)</button>
            <button class="action-btn" onclick="buyBuilding('테헤란로 빌딩', 60000000, 5000000)">🏢 빌딩 (6천만 / 월세 500만)</button>
            <button class="action-btn" onclick="buyBuilding('강남 타워', 100000000, 12000000)">🏙️ 강남타워 (1억 / 월세 1200만)</button>
            <button class="exit-btn" onclick="exitBuilding()">🚪 나가기</button>
        `;
    }
}

function startCryptoMinigame() {
    if (isGameOver) return;
    isCryptoGameActive = true;
    cryptoMultiplier = 1.0;
   
    const dialogue = document.getElementById('dialogue');
    const actionArea = document.getElementById('actionArea');
   
    dialogue.innerHTML = "🚀 <b>초고속 사이버 코인 실시간 폭등락 중!</b> 눈 깜짝할 사이에 곤두박질칠 수 있으니 신중하게 <b>[스페이스바]</b>를 누르세요!";
    actionArea.innerHTML = `
        <div style="font-size: 18px; font-weight: 700; color: #f43f5e; margin-bottom: 6px;">현재 배율: <span id="multiplierDisplay">1.00</span>x</div>
        <button class="action-btn" style="background: linear-gradient(135deg, #f43f5e, #e11d48); padding: 10px 24px; font-size: 15px;" onclick="stopCryptoMinigame()">🛑 지금 매도 (수익/손실 확정 & 턴 진행)</button>
    `;

    if (cryptoGameInterval) clearInterval(cryptoGameInterval);
    cryptoGameInterval = setInterval(() => {
        let delta = (Math.random() * 1.05 - 0.50);
        cryptoMultiplier = Math.max(0.02, cryptoMultiplier + delta);
       
        let span = document.getElementById('multiplierDisplay');
        if (span) {
            span.innerText = cryptoMultiplier.toFixed(2);
            span.style.color = cryptoMultiplier >= 1.0 ? '#10b981' : '#f43f5e';
        }
    }, 50);
}

function stopCryptoMinigame() {
    if (!isCryptoGameActive) return;
    isCryptoGameActive = false;
    if (cryptoGameInterval) clearInterval(cryptoGameInterval);

    let finalRate = cryptoMultiplier - 1.0;
    let gainLoss = Math.floor(cash * finalRate);
    cash += gainLoss;
    if (cash < 10000) cash = 10000;

    addFloatingText(gainLoss);
    updateUI();

    const dialogue = document.getElementById('dialogue');
    if (finalRate < 0) {
        dialogue.innerHTML = `💥 <b>코인 폭락 직격탄!</b> 손실을 입었습니다! (${gainLoss.toLocaleString()}원, 최종 배율: ${cryptoMultiplier.toFixed(2)}x)`;
    } else {
        dialogue.innerHTML = `🎉 <b>코인 급등 타이밍 성공!</b> 배율 <b>${cryptoMultiplier.toFixed(2)}x</b>로 수익이 확정되어 하룻밤이 지나갑니다!`;
    }

    setTimeout(() => {
        processTurn();
    }, 1500);
}

function renderStockMarketUI() {
    const actionArea = document.getElementById('actionArea');
    let html = `<div style="display: flex; gap: 8px; align-items: flex-start;">`;
   
    // 왼쪽 1: 6개 주식 종목 거래 구역
    html += `<div style="flex: 1.3; max-height: 155px; overflow-y: auto; padding-right: 4px;">`;
    stocks.forEach(s => {
        let diff = s.price - s.prevPrice;
        let rate = (diff / s.prevPrice * 100).toFixed(1);
        let color = diff >= 0 ? '#10b981' : '#f43f5e';
        let sign = diff >= 0 ? '+' : '';
        let maxBuyable = Math.floor(cash / s.price);

        html += `
            <div class="stock-card">
                <div style="text-align:left; width: 44%;">
                    <span style="font-weight:700; color:#ffffff; font-size:11px;">${s.name}</span>
                    <span style="font-size:10px; color:${color}; margin-left:2px;">${s.price.toLocaleString()} (${sign}${rate}%)</span>
                    <div style="font-size:9px; color:#38bdf8; margin-top:1px;">최대매수: ${maxBuyable}주</div>
                </div>
                <div style="display: flex; align-items: center; gap: 3px;">
                    <input type="number" id="qty_${s.id}" class="stock-input" value="1" min="1" max="99999">
                    <button class="action-btn" onclick="executeBuy('${s.id}')">매수</button>
                    <button class="sell-btn" onclick="executeSell('${s.id}')">매도</button>
                    <button class="action-btn" style="background:#059669;" onclick="executeMaxBuy('${s.id}')">최대</button>
                </div>
            </div>
        `;
    });
    html += `</div>`;

    // 왼쪽 2: 명확하게 볼 수 있는 '내 보유 주식 현황판' 칸 새로 추가!
    html += `<div style="flex: 1.1; background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 6px 8px; max-height: 155px; overflow-y: auto;">
        <div style="font-size: 11px; font-weight: 700; color: #10b981; margin-bottom: 4px; text-align: left;">📋 내 보유 주식 현황판</div>
    `;
   
    let hasOwnedStocks = false;
    stocks.forEach(s => {
        if (s.owned > 0) {
            hasOwnedStocks = true;
            let avgCost = Math.floor(s.totalCost / s.owned);
            let returnRate = (((s.price - avgCost) / avgCost) * 100).toFixed(1);
            let returnColor = returnRate >= 0 ? '#10b981' : '#f43f5e';
            html += `
                <div class="portfolio-item">
                    <div style="text-align: left;">
                        <span style="font-weight:700; color:#fff;">${s.name}</span><br/>
                        <span>보유: <b>${s.owned}주</b> | 평단: ${avgCost.toLocaleString()}원</span>
                    </div>
                    <div style="text-align: right; color:${returnColor}; font-weight:600;">
                        ${returnRate}%
                    </div>
                </div>
            `;
        }
    });

    if (!hasOwnedStocks) {
        html += `<div style="font-size: 10px; color: #64748b; text-align: center; margin-top: 35px;">현재 보유 중인 주식이 없습니다.</div>`;
    }
    html += `</div>`;

    // 오른쪽: 실시간 뉴스 속보 게시판 아카이브 구역
    html += `<div style="flex: 1; background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 8px; padding: 6px 8px; max-height: 155px; overflow-y: auto;">
        <div style="font-size: 11px; font-weight: 700; color: #38bdf8; margin-bottom: 4px; text-align: left;">📰 실시간 뉴스 속보</div>
    `;
    newsArchive.slice().reverse().forEach(n => {
        html += `<div class="news-item">${n}</div>`;
    });
    html += `</div>`;

    html += `</div>
        <div style="margin-top: 6px;">
            <button class="enter-btn" style="background: linear-gradient(135deg, #3b82f6, #1d4ed8); padding: 7px 16px; font-size: 13px;" onclick="passTurnByStock()">🌙 매수·매도 종료하고 메인으로 귀환 (하룻밤 지나기)</button>
            <button class="exit-btn" onclick="exitBuilding()">🚪 나가기</button>
        </div>
    `;

    actionArea.innerHTML = html;
}

function executeBuy(stockId) {
    if (isGameOver) return;
    let inputEl = document.getElementById(`qty_${stockId}`);
    let qty = parseInt(inputEl.value) || 0;
    if (qty <= 0) { alert("올바른 수량을 입력해주세요!"); return; }

    let s = stocks.find(item => item.id === stockId);
    let totalCost = s.price * qty;
    if (cash < totalCost) { alert("현금이 부족합니다!"); return; }
   
    cash -= totalCost;
    s.totalCost += totalCost;
    s.owned += qty;
    addFloatingText(-totalCost);
   
    updateUI();
    renderStockMarketUI();
}

function executeMaxBuy(stockId) {
    if (isGameOver) return;
    let s = stocks.find(item => item.id === stockId);
    let maxQty = Math.floor(cash / s.price);
    if (maxQty <= 0) { alert("매수할 현금이 부족합니다!"); return; }

    let totalCost = s.price * maxQty;
    cash -= totalCost;
    s.totalCost += totalCost;
    s.owned += maxQty;
    addFloatingText(-totalCost);

    updateUI();
    renderStockMarketUI();
}

function executeSell(stockId) {
    if (isGameOver) return;
    let inputEl = document.getElementById(`qty_${stockId}`);
    let qty = parseInt(inputEl.value) || 0;
    let s = stocks.find(item => item.id === stockId);
    if (s.owned <= 0) { alert("보유한 주식이 없습니다!"); return; }

    let sellQty = Math.min(qty, s.owned);
    let avgCost = s.owned > 0 ? (s.totalCost / s.owned) : 0;
   
    let revenue = s.price * sellQty;
    cash += revenue;

    s.owned -= sellQty;
    if (s.owned <= 0) {
        s.totalCost = 0;
        s.owned = 0;
    } else {
        s.totalCost -= (avgCost * sellQty);
    }

    addFloatingText(revenue);
   
    updateUI();
    renderStockMarketUI();
}

function passTurnByStock() {
    canvas.focus();
    processTurn();
}

function updateStockPrices() {
    stocks.forEach(s => {
        s.prevPrice = s.price;
        let changePercent = (Math.random() * (s.volatility * 2) - s.volatility) + currentNews.stockMod;
        let newPrice = Math.floor(s.price * (1 + changePercent));
        s.price = Math.max(1000, newPrice);
    });
}

function processTurn() {
    if (isGameOver) return;

    isDay = !isDay;
    document.getElementById('dayNightText').innerText = isDay ? "아침 🌅" : "밤 🌙";
    document.getElementById('dayNightText').style.color = isDay ? "#fbbf24" : "#a855f7";

    updateStockPrices();

    let rentSum = 0;
    ownedBuildings.forEach(b => rentSum += b.rent);
    if (rentSum > 0) {
        cash += rentSum;
        addFloatingText(rentSum);
    }
   
    let currentTotalAssets = getTotalAssets();

    if (currentTotalAssets >= goalMoney) {
        updateUI();
        triggerGameOver('win');
        return;
    }

    turn += 1;
   
    if (turn > 12) {
        turn = 12;
        updateUI();
        triggerGameOver('lose');
        return;
    }
   
    if (Math.random() < 0.8) {
        currentNews = newsEvents[Math.floor(Math.random() * newsEvents.length)];
    } else {
        currentNews = { text: "시티 증권 시장이 특별한 이슈 없이 균형 잡힌 흐름을 보이고 있습니다.", stockMod: 0 };
    }
   
    let newsFormatted = `[턴 ${turn}] ${currentNews.text}`;
    newsArchive.push(newsFormatted);
    document.getElementById('newsText').innerText = currentNews.text;

    updateUI();
    lastProximityKey = null;

    let bObj = buildings.find(b => b.id === 'stock');
    currentScene = 'town';
    player.x = bObj.portalX;
    player.y = 320;
    document.getElementById('locationText').innerText = '메인 스트리트';

    checkProximity();

    if (currentTotalAssets <= 0) {
        updateUI();
        triggerGameOver('lose');
    }
}

function investBank() {
    if (isGameOver) return;
    let interest = Math.floor(cash * 0.05);
    cash += interest;
    addFloatingText(interest);
    canvas.focus();
    processTurn();
}

function buyBuilding(name, price, rent) {
    if (isGameOver) return;
    if (cash < price) { alert("현금이 부족합니다!"); return; }
    cash -= price;
    addFloatingText(-price);
    ownedBuildings.push({ name, rent });
    canvas.focus();
   
    if (getTotalAssets() >= goalMoney) {
        updateUI();
        triggerGameOver('win');
        return;
    }
    updateUI();
}

function updateUI() {
    let totalAssets = getTotalAssets();
    document.getElementById('moneyText').innerText = totalAssets.toLocaleString();
    document.getElementById('cashText').innerText = cash.toLocaleString();
    document.getElementById('turnText').innerText = turn > 12 ? 12 : turn;

    let percent = Math.min(100, Math.max(1, Math.floor((totalAssets / goalMoney) * 100)));
    document.getElementById('progressBar').style.width = percent + '%';
    document.getElementById('progressText').innerText = `1억 원 목표 달성도: ${percent}% (총자산 ${totalAssets.toLocaleString()}원 / 100,000,000원)`;
}

function update() {
    if (!isGameOver) {
        if (keys['ArrowLeft'] || keys['a'] || keys['A']) { player.vx = -player.speed; player.facing = 'left'; }
        else if (keys['ArrowRight'] || keys['d'] || keys['D']) { player.vx = player.speed; player.facing = 'right'; }
        else { player.vx *= 0.6; }

        player.x += player.vx;
        player.vy += 0.65;
        player.y += player.vy;

        if (player.y >= player.groundY) {
            player.y = player.groundY;
            player.vy = 0;
            player.isGrounded = true;
        }

        if (currentScene === 'town') {
            player.x = Math.max(20, Math.min(1580, player.x));
            cameraX = player.x - canvas.width / 2;
            cameraX = Math.max(0, Math.min(1600 - canvas.width, cameraX));
        } else {
            player.x = Math.max(20, Math.min(820, player.x));
            cameraX = 0;
        }

        portalAnim += 0.08;
        player.animFrame += 0.15;

        checkProximity();
    }
   
    draw();
    requestAnimationFrame(update);
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.save();
    ctx.translate(-cameraX, 0);

    if (currentScene === 'town') drawTown();
    else drawInterior();

    drawVectorPlayer(player.x, player.y, player.facing);
    drawFloatingTexts();

    ctx.restore();

    if (isGameOver) {
        ctx.save();
        ctx.fillStyle = 'rgba(0, 0, 0, 0.85)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.textAlign = 'center';
        ctx.shadowColor = '#000';
        ctx.shadowBlur = 20;

        let finalAssets = getTotalAssets();
        if (gameResult === 'win') {
            ctx.fillStyle = '#fbbf24';
            ctx.font = '700 48px Pretendard, sans-serif';
            ctx.fillText('YOU WIN!', canvas.width / 2, canvas.height / 2 - 20);

            ctx.fillStyle = '#ffffff';
            ctx.font = '600 18px Pretendard, sans-serif';
            ctx.fillText('축하합니다! 1억 원을 달성하여 강남 건물주가 되었습니다!', canvas.width / 2, canvas.height / 2 + 30);
        } else {
            ctx.fillStyle = '#f43f5e';
            ctx.font = '700 48px Pretendard, sans-serif';
            ctx.fillText('YOU LOSE', canvas.width / 2, canvas.height / 2 - 20);

            ctx.fillStyle = '#cbd5e1';
            ctx.font = '600 18px Pretendard, sans-serif';
            ctx.fillText('12턴 종료! 목표 금액 미달성 최종 자산: ' + finalAssets.toLocaleString() + '원', canvas.width / 2, canvas.height / 2 + 30);
        }
        ctx.restore();
    }
}

function drawTown() {
    let skyGradient = ctx.createLinearGradient(0, 0, 0, 260);
    if (isDay) {
        skyGradient.addColorStop(0, '#0284c7');
        skyGradient.addColorStop(1, '#38bdf8');
    } else {
        skyGradient.addColorStop(0, '#090d16');
        skyGradient.addColorStop(1, '#1e293b');
    }
    ctx.fillStyle = skyGradient;
    ctx.fillRect(cameraX, 0, canvas.width, 260);

    ctx.save();
    if (isDay) {
        ctx.fillStyle = '#fbbf24';
        ctx.shadowColor = '#fbbf24';
        ctx.shadowBlur = 25;
        ctx.beginPath();
        ctx.arc(cameraX + 700, 60, 26, 0, Math.PI * 2);
        ctx.fill();
    } else {
        ctx.fillStyle = '#fef08a';
        ctx.shadowColor = '#fef08a';
        ctx.shadowBlur = 20;
        ctx.beginPath();
        ctx.arc(cameraX + 700, 60, 22, 0, Math.PI * 2);
        ctx.fill();
    }
    ctx.restore();

    ctx.fillStyle = isDay ? 'rgba(255, 255, 255, 0.2)' : 'rgba(30, 41, 59, 0.4)';
    ctx.fillRect(cameraX + 50, 100, 90, 160);
    ctx.fillRect(cameraX + 300, 70, 110, 190);
    ctx.fillRect(cameraX + 700, 80, 100, 180);
    ctx.fillRect(cameraX + 1100, 50, 130, 210);

    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 360, 1600, 120);
    ctx.fillStyle = '#334155';
    ctx.fillRect(0, 360, 1600, 6);

    buildings.forEach(b => {
        ctx.fillStyle = b.colorMain;
        ctx.fillRect(b.x, 110, 200, 250);

        for (let wx = b.x + 20; wx < b.x + 180; wx += 40) {
            for (let wy = 140; wy < 320; wy += 45) {
                ctx.fillStyle = isDay ? 'rgba(255, 255, 255, 0.6)' : 'rgba(56, 189, 248, 0.15)';
                ctx.fillRect(wx, wy, 22, 28);
                ctx.fillStyle = 'rgba(251, 191, 36, 0.8)';
                ctx.fillRect(wx + 4, wy + 4, 14, 20);
            }
        }

        ctx.fillStyle = b.accent;
        ctx.fillRect(b.x, 80, 200, 32);
        ctx.fillStyle = '#ffffff';
        ctx.font = '600 15px Pretendard, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(b.name, b.x + 100, 101);

        let px = b.portalX;
        let py = 320;
        let scale = Math.sin(portalAnim) * 6;
       
        ctx.save();
        ctx.strokeStyle = b.accent;
        ctx.lineWidth = 4;
        ctx.shadowColor = b.accent;
        ctx.shadowBlur = 15;
        ctx.beginPath();
        ctx.ellipse(px, py, 22 + scale, 40 + scale, 0, 0, Math.PI * 2);
        ctx.stroke();
        ctx.fillStyle = b.accent;
        ctx.globalAlpha = 0.25;
        ctx.fill();
        ctx.restore();
    });
}

function drawInterior() {
    let bObj = buildings.find(b => b.id === currentScene);
    let npc = interiorNPCs[currentScene];

    ctx.fillStyle = '#0f172a';
    ctx.fillRect(0, 0, 840, 480);
   
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 0, 840, 90);

    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 360, 840, 120);

    ctx.fillStyle = '#334155';
    ctx.fillRect(340, 300, 160, 60);
    ctx.fillStyle = '#38bdf8';
    ctx.fillRect(340, 350, 160, 10);

    ctx.save();
    ctx.strokeStyle = '#f43f5e';
    ctx.lineWidth = 4;
    ctx.shadowColor = '#f43f5e';
    ctx.shadowBlur = 15;
    ctx.beginPath();
    ctx.ellipse(40, 320, 18, 36, 0, 0, Math.PI * 2);
    ctx.stroke();
    ctx.restore();

    drawVectorNPC(npc.x, npc.y, npc.name);
}

function drawVectorPlayer(x, y, facing) {
    let bounce = Math.sin(player.animFrame) * 2;
    if (!player.isGrounded) bounce = -6;
    let totalAssets = getTotalAssets();

    if (isGameOver && gameResult === 'lose') {
        ctx.fillStyle = '#475569';
        ctx.beginPath();
        ctx.roundRect(x - 16, y - 38 + bounce, 32, 44, [6]);
        ctx.fill();

        ctx.fillStyle = '#94a3b8';
        ctx.beginPath();
        ctx.roundRect(x - 10, y - 28 + bounce, 20, 14, [4]);
        ctx.fill();

        ctx.fillStyle = '#ef4444';
        ctx.fillRect(x - 4, y - 24 + bounce, 2, 6);
        ctx.fillRect(x + 2, y - 24 + bounce, 2, 6);

        ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
        ctx.beginPath();
        ctx.roundRect(x - 50, y - 56, 100, 18, [4]);
        ctx.fill();
        ctx.fillStyle = '#f43f5e';
        ctx.font = '600 11px Pretendard, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('빈털터리 파산자', x, y - 43);
        return;
    }

    if (totalAssets >= 50000000) {
        ctx.save();
        ctx.strokeStyle = '#fbbf24';
        ctx.lineWidth = 3;
        ctx.shadowColor = '#fbbf24';
        ctx.shadowBlur = 18;
        ctx.beginPath();
        ctx.arc(x, y - 18 + bounce, 32, 0, Math.PI * 2);
        ctx.stroke();
        ctx.restore();
    }

    ctx.fillStyle = '#0f172a';
    ctx.beginPath();
    ctx.roundRect(x - 14, y - 42 + bounce, 28, 48, [10]);
    ctx.fill();

    ctx.fillStyle = '#fce7f3';
    ctx.beginPath();
    ctx.roundRect(x - 10, y - 30, 20, 16, [6]);
    ctx.fill();

    if (totalAssets >= 50000000) {
        ctx.fillStyle = '#fbbf24';
        ctx.fillRect(x - 12, y - 38 + bounce, 24, 10);
        ctx.fillStyle = '#fbbf24';
        ctx.fillRect(x - 2, y - 14 + bounce, 4, 16);
    } else if (totalAssets >= 20000000) {
        ctx.fillStyle = '#a855f7';
        ctx.fillRect(x - 12, y - 38 + bounce, 24, 10);
        ctx.fillStyle = '#e2e8f0';
        ctx.fillRect(x - 2, y - 14 + bounce, 4, 16);
    } else {
        ctx.fillStyle = '#3b82f6';
        ctx.fillRect(x - 12, y - 38 + bounce, 24, 10);
        ctx.fillStyle = '#38bdf8';
        if (facing === 'right') {
            ctx.fillRect(x + 2, y - 14 + bounce, 6, 16);
        } else {
            ctx.fillRect(x - 8, y - 14 + bounce, 6, 16);
        }
    }

    ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
    ctx.beginPath();
    ctx.roundRect(x - 45, y - 62 + bounce, 90, 20, [6]);
    ctx.fill();
    ctx.strokeStyle = 'rgba(56, 189, 248, 0.3)';
    ctx.stroke();

    ctx.fillStyle = totalAssets >= 50000000 ? '#fbbf24' : '#38bdf8';
    ctx.font = '600 12px Pretendard, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(player.name, x, y - 48 + bounce);
}

function drawFloatingTexts() {
    for (let i = floatingTexts.length - 1; i >= 0; i--) {
        let ft = floatingTexts[i];
        ft.y += ft.vy;
        ft.opacity -= 0.02;

        if (ft.opacity <= 0) {
            floatingTexts.splice(i, 1);
            continue;
        }

        ctx.save();
        ctx.globalAlpha = Math.max(0, ft.opacity);
        ctx.fillStyle = ft.color;
        ctx.font = '700 16px Pretendard, sans-serif';
        ctx.textAlign = 'center';
        ctx.shadowColor = '#000000';
        ctx.shadowBlur = 6;
        ctx.fillText(ft.text, ft.x, ft.y);
        ctx.restore();
    }
}

function drawVectorNPC(x, y, name) {
    ctx.fillStyle = '#0f172a';
    ctx.beginPath();
    ctx.roundRect(x - 14, y - 42, 28, 48, [10]);
    ctx.fill();

    ctx.fillStyle = '#fce7f3';
    ctx.beginPath();
    ctx.roundRect(x - 10, y - 30, 20, 16, [6]);
    ctx.fill();

    ctx.fillStyle = '#10b981';
    ctx.fillRect(x - 12, y - 38, 24, 10);

    ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
    ctx.beginPath();
    ctx.roundRect(x - 55, y - 62, 110, 20, [6]);
    ctx.fill();
    ctx.strokeStyle = 'rgba(16, 185, 129, 0.3)';
    ctx.stroke();

    ctx.fillStyle = '#ffffff';
    ctx.font = '600 12px Pretendard, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(name, x, y - 48);
}

requestAnimationFrame(update);
</script>
</body>
</html>
"""

components.html(game_html, height=980)

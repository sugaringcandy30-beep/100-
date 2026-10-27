import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="메이플 비치 자산관리 RPG", page_icon="🍁", layout="centered")

st.title("🍁 고퀄리티 픽셀 비치 & 뉴스 찌라시 RPG")
st.caption("좌우 방향키(A, D)로 이동, Space키로 점프! 포탈[▲ / W]을 타고 들어가 미니게임에 도전하세요.")

game_html = """
<!DOCTYPE html>
<html>
<head>
<style>
    body {
        margin: 0;
        padding: 0;
        background-color: #0b0e14;
        color: white;
        font-family: 'Comic Sans MS', 'Courier New', sans-serif;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    #newsTicker {
        width: 540px;
        background: #151922;
        color: #feca57;
        font-size: 13px;
        font-weight: bold;
        padding: 8px 12px;
        border-radius: 8px 8px 0 0;
        border: 2px solid #38ada9;
        border-bottom: none;
        box-sizing: border-box;
        overflow: hidden;
        white-space: nowrap;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.5);
    }
    #gameContainer {
        position: relative;
    }
    canvas {
        border: 3px solid #38ada9;
        border-radius: 0 0 10px 10px;
        background-color: #0c1017;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        image-rendering: pixelated; /* 도트 그래픽 선명도 적용 */
    }
    #uiBox {
        width: 540px;
        background: linear-gradient(135deg, #1e272e, #0f2027);
        padding: 14px;
        border-radius: 10px;
        margin-top: 10px;
        box-sizing: border-box;
        border: 2px solid #38ada9;
        box-shadow: 0 4px 15px rgba(0,0,0,0.6);
    }
    .status-bar {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
        font-weight: bold;
        color: #feca57;
        font-size: 14px;
    }
    .action-btn {
        background: linear-gradient(180deg, #ff9f43, #ee5253);
        color: white;
        border: 2px solid #ffffff;
        padding: 8px 14px;
        margin: 4px;
        border-radius: 6px;
        cursor: pointer;
        font-weight: bold;
        box-shadow: 0 3px 0 #b17b10;
    }
    .action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 0 #b17b10;
    }
    .enter-btn {
        background: linear-gradient(180deg, #10ac84, #1dd1a1);
        color: white;
        border: 2px solid #ffffff;
        padding: 8px 18px;
        border-radius: 6px;
        cursor: pointer;
        font-weight: bold;
        font-size: 14px;
        box-shadow: 0 3px 0 #10ac84;
    }
    .exit-btn {
        background: linear-gradient(180deg, #ff6b6b, #ee5253);
        color: white;
        border: 2px solid #ffffff;
        padding: 6px 14px;
        border-radius: 6px;
        cursor: pointer;
        font-weight: bold;
    }
    .controls {
        display: grid;
        grid-template-columns: repeat(4, 60px);
        gap: 8px;
        justify-content: center;
        margin-top: 12px;
    }
    .ctrl-btn {
        width: 60px;
        height: 50px;
        font-size: 16px;
        font-weight: bold;
        background: #1e272e;
        color: #feca57;
        border: 2px solid #38ada9;
        border-radius: 8px;
        cursor: pointer;
        box-shadow: 0 3px 0 #10ac84;
    }
    .ctrl-btn:active {
        transform: translateY(2px);
        box-shadow: none;
    }
    #dialogue {
        min-height: 48px;
        background: rgba(10, 15, 25, 0.95);
        padding: 10px;
        border-radius: 6px;
        border: 2px solid #38ada9;
        margin-top: 5px;
        font-size: 13px;
        line-height: 1.4;
    }
    #minigameBox {
        display: none;
        background: rgba(0,0,0,0.85);
        border: 2px solid #feca57;
        border-radius: 8px;
        padding: 10px;
        margin-top: 8px;
        text-align: center;
    }
    #meterBar {
        width: 100%;
        height: 20px;
        background: #222;
        border-radius: 10px;
        position: relative;
        overflow: hidden;
        margin: 8px 0;
        border: 1px solid #555;
    }
    #meterIndicator {
        width: 12px;
        height: 100%;
        background: #ff4757;
        position: absolute;
        left: 0;
    }
    #targetZone {
        width: 60px;
        height: 100%;
        background: #2ed573;
        position: absolute;
        left: 200px;
    }
</style>
</head>
<body>

<div id="newsTicker">📰 [속보] 메이플시티 금융 시장이 개장했습니다!</div>

<div id="gameContainer">
    <canvas id="gameCanvas" width="540" height="340"></canvas>
</div>

<div id="uiBox">
    <div class="status-bar">
        <span>📍 맵: <span id="locationText">헤네시스 비치</span></span>
        <span>📅 턴: <span id="turnText">1</span>/12</span>
        <span>💰 현금: <span id="moneyText">1,000,000</span>원</span>
    </div>
    <div id="dialogue">💬 좌우 방향키로 이동하고, 파란 포탈 앞에서 [위쪽 방향키 / W]를 누르세요!</div>
    
    <div id="minigameBox">
        <div id="minigameTitle" style="color:#feca57; font-weight:bold;">🎯 타이밍 게이지 미니게임</div>
        <div id="meterBar">
            <div id="targetZone"></div>
            <div id="meterIndicator"></div>
        </div>
        <button class="action-btn" onclick="stopMeter()">STOP (매수 버튼)</button>
    </div>

    <div id="actionArea" style="margin-top: 8px; text-align: center;"></div>
</div>

<div class="controls">
    <button class="ctrl-btn" onclick="moveLeft()">◄ 이동</button>
    <button class="ctrl-btn" onclick="jump()">▲ 점프</button>
    <button class="ctrl-btn" onclick="moveRight()">이동 ►</button>
    <button class="ctrl-btn" style="background:#10ac84; color:white;" onclick="interactPortal()">▲ 포탈</button>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let money = 1000000;
let turn = 1;
let currentScene = 'town';
let ownedBuildings = [];

let currentNews = { text: "평화로운 메이플시티입니다.", stockMod: 0, cryptoMod: 0 };
const newsEvents = [
    { text: "🔥 [속보] 엘리니아 AI 반도체 호재 발표! 주식 대박 예감!", stockMod: 0.35, cryptoMod: 0 },
    { text: "📉 [속보] 커닝시티 해킹 사건 발생! 코인 시장 대폭락 주의!", stockMod: 0, cryptoMod: -0.3 },
    { text: "🚀 [속보] 세계 중앙은행 금리 인하 결정! 전 금융 시장 폭등장!", stockMod: 0.2, cryptoMod: 0.25 },
    { text: "⚠️ [속보] 검은 마법사 세금 공세 시작! 자산 시장 냉각!", stockMod: -0.2, cryptoMod: -0.2 }
];

const player = {
    x: 80,
    y: 220,
    vx: 0,
    vy: 0,
    speed: 5,
    jumpPower: -11,
    groundY: 220,
    isGrounded: true,
    facing: 'right',
    animFrame: 0,
    name: '메이플개미'
};

const buildings = [
    { id: 'bank', name: '🏦 헤네시스 은행', x: 80, portalX: 130, colorMain: '#2ed573', colorRoof: '#10ac84' },
    { id: 'stock', name: '📈 엘리니아 증권', x: 260, portalX: 310, colorMain: '#54a0ff', colorRoof: '#2e86de' },
    { id: 'crypto', name: '🚀 커닝시티 코인', x: 440, portalX: 490, colorMain: '#ff6b6b', colorRoof: '#ee5253' },
    { id: 'realty', name: '🏢 리스항구 부동산', x: 620, portalX: 670, colorMain: '#feca57', colorRoof: '#ff9f43' }
];

const interiorNPCs = {
    bank: { x: 270, y: 190, name: '🏦 은행원 김수호' },
    stock: { x: 270, y: 190, name: '📈 펀드매니저 박차트' },
    crypto: { x: 270, y: 190, name: '🚀 중개인 나대박' },
    realty: { x: 270, y: 190, name: '🏢 중개사 최건물' }
};

let cameraX = 0;
let portalAnim = 0;
let keys = {};

let meterPos = 0;
let meterSpeed = 4;
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
function jump() {
    if (player.isGrounded) {
        player.vy = player.jumpPower;
        player.isGrounded = false;
    }
}

function interactPortal() {
    if (currentScene === 'town') {
        for (let b of buildings) {
            if (Math.abs(player.x - b.portalX) < 30) {
                enterBuilding(b.id);
                return;
            }
        }
    }
}

function enterBuilding(bId) {
    currentScene = bId;
    player.x = 80;
    player.y = 220;
    const bObj = buildings.find(b => b.id === bId);
    document.getElementById('locationText').innerText = bObj.name;
    checkProximity();
}

function exitBuilding() {
    let bObj = buildings.find(b => b.id === currentScene);
    currentScene = 'town';
    player.x = bObj.portalX;
    player.y = 220;
    document.getElementById('locationText').innerText = '헤네시스 비치';
    document.getElementById('minigameBox').style.display = 'none';
    meterActive = false;
    checkProximity();
}

function checkProximity() {
    const actionArea = document.getElementById('actionArea');
    const dialogue = document.getElementById('dialogue');

    if (currentScene === 'town') {
        let nearB = buildings.find(b => Math.abs(player.x - b.portalX) < 30);
        if (nearB) {
            dialogue.innerHTML = `✨ <b>[${nearB.name}] 포탈 앞입니다!</b> [위쪽 방향키 / W]를 눌러 입장하세요!`;
            actionArea.innerHTML = `<button class="enter-btn" onclick="enterBuilding('${nearB.id}')">🚪 포탈 입장하기</button>`;
        } else {
            dialogue.innerHTML = "💬 좌우 방향키로 차원 포탈 위치까지 이동해 보세요!";
            actionArea.innerHTML = "";
        }
    } else {
        let npc = interiorNPCs[currentScene];
        let dist = Math.abs(player.x - npc.x);
        
        if (player.x < 40) {
            dialogue.innerHTML = "🚪 밖으로 나가는 출구 포탈입니다.";
            actionArea.innerHTML = `<button class="exit-btn" onclick="exitBuilding()">🚪 밖으로 나가기</button>`;
        } else if (dist < 50) {
            dialogue.innerHTML = `💬 <b>${npc.name}</b>: "어서오세요, 미니게임에 참여해 투자 수익율을 직접 제어해보세요!"`;
            renderDialogueOptions(currentScene);
        } else {
            dialogue.innerHTML = `🏢 카운터에 있는 직원에게 다어가보세요!`;
            actionArea.innerHTML = `<button class="exit-btn" onclick="exitBuilding()">🚪 밖으로 나가기</button>`;
        }
    }
}

function renderDialogueOptions(type) {
    const actionArea = document.getElementById('actionArea');
    if (type === 'bank') {
        actionArea.innerHTML = `<button class="action-btn" onclick="investBank()">🏦 안전 예금 가입 (+5%)</button> <button class="exit-btn" onclick="exitBuilding()">🚪 나가기</button>`;
    } else if (type === 'stock') {
        actionArea.innerHTML = `<button class="action-btn" onclick="startStockMiniGame()">🎯 주식 타이밍 미니게임 도전</button> <button class="exit-btn" onclick="exitBuilding()">🚪 나가기</button>`;
    } else if (type === 'crypto') {
        actionArea.innerHTML = `<button class="action-btn" onclick="startCryptoMiniGame()">🎰 코인 폭발 타이밍 도전</button> <button class="exit-btn" onclick="exitBuilding()">🚪 나가기</button>`;
    } else if (type === 'realty') {
        actionArea.innerHTML = `
            <button class="action-btn" onclick="buyBuilding('반지하 고시원', 10000000, 500000)">🏚️ 고시원 (1천만)</button>
            <button class="action-btn" onclick="buyBuilding('원룸 빌라', 30000000, 1500000)">🏠 빌라 (3천만)</button>
            <button class="action-btn" onclick="buyBuilding('강남 타워', 100000000, 10000000)">🏙️ 강남타워 (1억)</button>
            <button class="exit-btn" onclick="exitBuilding()">🚪 나가기</button>
        `;
    }
}

function startStockMiniGame() {
    document.getElementById('actionArea').innerHTML = '';
    document.getElementById('minigameBox').style.display = 'block';
    document.getElementById('minigameTitle').innerText = '📈 주식 매수 타이밍! 초록 영역에 멈추세요!';
    meterPos = 0;
    meterSpeed = 6;
    meterActive = true;
    updateMeter();
}

function startCryptoMiniGame() {
    document.getElementById('actionArea').innerHTML = '';
    document.getElementById('minigameBox').style.display = 'block';
    document.getElementById('minigameTitle').innerText = '🎰 코인 타겟 타이밍! 초록 영역에 멈추면 3배 떡상!';
    meterPos = 0;
    meterSpeed = 10;
    meterActive = true;
    updateMeter();
}

function updateMeter() {
    if (!meterActive) return;
    meterPos += meterSpeed;
    if (meterPos > 520 || meterPos < 0) meterSpeed *= -1;
    document.getElementById('meterIndicator').style.left = meterPos + 'px';
    meterAnimId = requestAnimationFrame(updateMeter);
}

function stopMeter() {
    meterActive = false;
    cancelAnimationFrame(meterAnimId);
    document.getElementById('minigameBox').style.display = 'none';

    let success = meterPos >= 200 && meterPos <= 260;
    if (currentScene === 'stock') {
        let winProb = 0.5 + currentNews.stockMod;
        if (success || Math.random() < winProb) {
            let profit = Math.floor(money * 0.4);
            money += profit;
            alert(`🎉 [주식 대성공!] 타이밍 적중으로 +${profit.toLocaleString()}원 수익!`);
        } else {
            let loss = Math.floor(money * 0.2);
            money -= loss;
            alert(`📉 [주식 손실] 타이밍 실패... -${loss.toLocaleString()}원`);
        }
    } else if (currentScene === 'crypto') {
        if (success) {
            let profit = Math.floor(money * 2.0);
            money += profit;
            alert(`🚀 [코인 초대박!] 타겟 저격으로 +${profit.toLocaleString()}원 폭등!!`);
        } else {
            let loss = Math.floor(money * 0.5);
            money -= loss;
            alert(`💥 [코인 청산] 타이밍 실패로 -${loss.toLocaleString()}원 폭락...`);
        }
    }
    processTurn();
}

function processTurn() {
    let rentSum = 0;
    ownedBuildings.forEach(b => rentSum += b.rent);
    money += rentSum;
    turn += 1;
    
    if (Math.random() < 0.7) {
        currentNews = newsEvents[Math.floor(Math.random() * newsEvents.length)];
    } else {
        currentNews = { text: "📰 [속보] 금융 시장이 비교적 안정세를 유지하고 있습니다.", stockMod: 0, cryptoMod: 0 };
    }
    document.getElementById('newsTicker').innerText = currentNews.text;

    updateUI();
    if (money >= 100000000) alert("🎉 1억 원 달성! 강남 건물주가 되었습니다!");
    else if (turn > 12) alert("⏱ 12턴 종료! 최종 자산: " + money.toLocaleString() + "원");
    else if (money <= 0) alert("💥 파산했습니다!");
}

function investBank() { money += Math.floor(money * 0.05); alert("🏦 적금 이자가 입금되었습니다!"); processTurn(); }
function buyBuilding(name, price, rent) {
    if (money < price) { alert("잔액이 부족합니다!"); return; }
    money -= price; ownedBuildings.push({ name, rent });
    alert(`🎉 [${name}] 매수 성공!`); updateUI();
}

function updateUI() {
    document.getElementById('moneyText').innerText = money.toLocaleString();
    document.getElementById('turnText').innerText = turn;
}

function update() {
    if (keys['ArrowLeft'] || keys['a'] || keys['A']) { player.vx = -player.speed; player.facing = 'left'; }
    else if (keys['ArrowRight'] || keys['d'] || keys['D']) { player.vx = player.speed; player.facing = 'right'; }
    else { player.vx *= 0.6; }

    player.x += player.vx;
    player.vy += 0.6;
    player.y += player.vy;

    if (player.y >= player.groundY) {
        player.y = player.groundY;
        player.vy = 0;
        player.isGrounded = true;
    }

    if (currentScene === 'town') {
        player.x = Math.max(20, Math.min(780, player.x));
        cameraX = player.x - canvas.width / 2;
        cameraX = Math.max(0, Math.min(800 - canvas.width, cameraX));
    } else {
        player.x = Math.max(20, Math.min(500, player.x));
        cameraX = 0;
    }

    portalAnim += 0.08;
    player.animFrame += 0.15;

    checkProximity();
    draw();
    requestAnimationFrame(update);
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.save();
    ctx.translate(-cameraX, 0);

    if (currentScene === 'town') drawTown();
    else drawInterior();

    drawDetailedMapleChar(player.x, player.y, player.facing);
    ctx.restore();
}

// === 고퀄리티 픽셀 아트 타운 렌더링 ===
function drawTown() {
    // 하늘 그라데이션
    let skyGradient = ctx.createLinearGradient(0, 0, 0, 180);
    skyGradient.addColorStop(0, '#4a69bd');
    skyGradient.addColorStop(1, '#6a89cc');
    ctx.fillStyle = skyGradient;
    ctx.fillRect(cameraX, 0, canvas.width, 180);

    // 구름 도트
    ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
    ctx.fillRect(cameraX + 50, 30, 40, 10);
    ctx.fillRect(cameraX + 60, 24, 20, 6);
    ctx.fillRect(cameraX + 300, 50, 50, 12);

    // 원경 산맥
    ctx.fillStyle = '#1e3799';
    ctx.beginPath();
    ctx.arc(100, 220, 140, 0, Math.PI, true);
    ctx.arc(400, 230, 180, 0, Math.PI, true);
    ctx.arc(700, 210, 150, 0, Math.PI, true);
    ctx.fill();

    // 잔디 땅 & 지형 타일링
    ctx.fillStyle = '#78e08f';
    ctx.fillRect(0, 256, 800, 12); // 상단 싱그러운 잔디층
    ctx.fillStyle = '#38ada9';
    ctx.fillRect(0, 268, 800, 72); // 흙층

    // 잔디 패턴 도트
    ctx.fillStyle = '#b8e994';
    for (let x = 0; x < 800; x += 16) {
        ctx.fillRect(x, 256, 4, 4);
    }

    // 픽셀 건물 그리기 (셰이딩 및 구조 보강)
    buildings.forEach(b => {
        // 건물 그림자
        ctx.fillStyle = 'rgba(0,0,0,0.3)';
        ctx.fillRect(b.x - 5, 250, 100, 10);

        // 건물 벽체
        ctx.fillStyle = b.colorMain;
        ctx.fillRect(b.x, 130, 90, 126);

        // 벽체 우측 3D 테두리 음영
        ctx.fillStyle = 'rgba(0,0,0,0.2)';
        ctx.fillRect(b.x + 80, 130, 10, 126);

        // 지붕 (삼각/격자 형태)
        ctx.fillStyle = b.colorRoof;
        ctx.fillRect(b.x - 6, 115, 102, 18);
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(b.x - 6, 131, 102, 3); // 지붕 하단 하이라이트

        // 창문 도트
        ctx.fillStyle = '#f8c291';
        ctx.fillRect(b.x + 15, 145, 20, 20);
        ctx.fillRect(b.x + 55, 145, 20, 20);
        ctx.fillStyle = '#0c2461';
        ctx.fillRect(b.x + 24, 145, 2, 20);
        ctx.fillRect(b.x + 15, 154, 20, 2);
        ctx.fillRect(b.x + 64, 145, 2, 20);
        ctx.fillRect(b.x + 55, 154, 20, 2);

        // 건물 간판
        ctx.fillStyle = '#1e272e';
        ctx.fillRect(b.x + 10, 95, 70, 18);
        ctx.strokeStyle = '#feca57';
        ctx.strokeRect(b.x + 10, 95, 70, 18);
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 10px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(b.name, b.x + 45, 108);

        // 차원 포탈 이펙트
        let px = b.portalX;
        let py = 220;
        let scale = Math.sin(portalAnim) * 3;
        
        ctx.strokeStyle = '#00d2d3';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.ellipse(px, py, 14 + scale, 28 + scale, 0, 0, Math.PI * 2);
        ctx.stroke();

        ctx.fillStyle = 'rgba(0, 210, 211, 0.35)';
        ctx.fill();
    });
}

// === 고퀄리티 실내 매장 렌더링 ===
function drawInterior() {
    let bObj = buildings.find(b => b.id === currentScene);
    let npc = interiorNPCs[currentScene];

    // 바닥 목재 격자 타일
    ctx.fillStyle = '#f8c291';
    ctx.fillRect(0, 0, 540, 340);

    ctx.strokeStyle = '#e55039';
    ctx.lineWidth = 1;
    for (let x = 0; x < 540; x += 20) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, 340); ctx.stroke();
    }

    // 벽면 및 상단 띠
    ctx.fillStyle = bObj.colorRoof;
    ctx.fillRect(0, 0, 540, 60);
    ctx.fillStyle = '#b71540';
    ctx.fillRect(0, 56, 540, 4);

    // 하단 카펫
    ctx.fillStyle = '#78e08f';
    ctx.fillRect(0, 256, 540, 90);

    // 카운터 및 3D 음영
    ctx.fillStyle = '#e67e22';
    ctx.fillRect(200, 200, 140, 50);
    ctx.fillStyle = '#d35400';
    ctx.fillRect(200, 240, 140, 10);
    ctx.strokeStyle = '#ffffff';
    ctx.strokeRect(200, 200, 140, 50);

    // 출구 포탈
    ctx.strokeStyle = '#ff4757';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.ellipse(30, 220, 12, 26, 0, 0, Math.PI * 2);
    ctx.stroke();

    drawDetailedNPC(npc.x, npc.y, npc.name);
}

// === 디테일 픽셀 캐릭터 렌더링 ===
function drawDetailedMapleChar(x, y, facing) {
    let bounce = Math.sin(player.animFrame) * 2;
    if (!player.isGrounded) bounce = -4;

    // 검은색 외곽선(Outline) 효과
    ctx.fillStyle = '#000000';
    ctx.fillRect(x - 12, y - 28 + bounce, 24, 34);

    // 모자 (빨간 스냅백)
    ctx.fillStyle = '#eb2f06';
    ctx.fillRect(x - 10, y - 26 + bounce, 20, 8);
    ctx.fillStyle = '#f8c291'; // 피부톤
    ctx.fillRect(x - 8, y - 18 + bounce, 16, 10);

    // 눈 (초롱초롱한 픽셀 눈)
    ctx.fillStyle = '#0c2461';
    let eyeOff = facing === 'right' ? 2 : -4;
    ctx.fillRect(x + eyeOff, y - 15 + bounce, 3, 5);
    ctx.fillRect(x + eyeOff + 6, y - 15 + bounce, 3, 5);
    ctx.fillStyle = '#ffffff'; // 눈동자 하이라이트
    ctx.fillRect(x + eyeOff, y - 15 + bounce, 1, 2);
    ctx.fillRect(x + eyeOff + 6, y - 15 + bounce, 1, 2);

    // 튜브 (노란 오리 튜브)
    ctx.fillStyle = '#f1c40f';
    ctx.fillRect(x - 11, y - 6 + bounce, 22, 10);
    ctx.fillStyle = '#e67e22'; // 부리
    if (facing === 'right') ctx.fillRect(x + 9, y - 4 + bounce, 4, 3);
    else ctx.fillRect(x - 13, y - 4 + bounce, 4, 3);

    // 옷
    ctx.fillStyle = '#4a69bd';
    ctx.fillRect(x - 5, y - 8 + bounce, 10, 6);

    // 캐릭터 이름표 UI
    ctx.fillStyle = 'rgba(0,0,0,0.7)';
    ctx.fillRect(x - 24, y - 38 + bounce, 48, 12);
    ctx.fillStyle = '#feca57';
    ctx.font = 'bold 9px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(player.name, x, y - 29 + bounce);
}

// === 디테일 NPC 렌더링 ===
function drawDetailedNPC(x, y, name) {
    ctx.fillStyle = '#000000';
    ctx.fillRect(x - 10, y - 26, 20, 36);

    ctx.fillStyle = '#2c3e50'; // 머리
    ctx.fillRect(x - 8, y - 24, 16, 10);
    ctx.fillStyle = '#f8c291'; // 피부
    ctx.fillRect(x - 6, y - 14, 12, 10);
    ctx.fillStyle = '#0984e3'; // 정장
    ctx.fillRect(x - 8, y - 4, 16, 14);

    ctx.fillStyle = 'rgba(0,0,0,0.7)';
    ctx.fillRect(x - 35, y - 38, 70, 12);
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 9px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(name, x, y - 29);
}

requestAnimationFrame(update);
</script>
</body>
</html>
"""

components.html(game_html, height=720)

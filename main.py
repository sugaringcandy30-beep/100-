import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="메이플 비치 자산관리 RPG", page_icon="🍁", layout="centered")

st.title("🍁 메이플 픽셀 비치 & 뉴스 찌라시/미니게임 RPG")
st.caption("좌우 방향키(A, D)로 이동, Space키로 점프! 포탈[▲ / W]을 타고 들어가 뉴스 변수 및 미니게임에 도전하세요.")

game_html = """
<!DOCTYPE html>
<html>
<head>
<style>
    body {
        margin: 0;
        padding: 0;
        background-color: #0d1117;
        color: white;
        font-family: 'Comic Sans MS', 'Courier New', sans-serif;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    #newsTicker {
        width: 540px;
        background: #1e272e;
        color: #ffdd59;
        font-size: 13px;
        font-weight: bold;
        padding: 6px 12px;
        border-radius: 6px 6px 0 0;
        border: 2px solid #54a0ff;
        border-bottom: none;
        box-sizing: border-box;
        overflow: hidden;
        white-space: nowrap;
    }
    #gameContainer {
        position: relative;
    }
    canvas {
        border: 4px solid #ffbe76;
        border-radius: 0 0 12px 12px;
        background-color: #130f40;
        box-shadow: 0 10px 25px rgba(0,0,0,0.8);
        image-rendering: pixelated;
    }
    #uiBox {
        width: 540px;
        background: linear-gradient(135deg, #222f3e, #10ac84);
        padding: 14px;
        border-radius: 10px;
        margin-top: 10px;
        box-sizing: border-box;
        border: 2px solid #54a0ff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
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
        background: #222f3e;
        color: #feca57;
        border: 2px solid #54a0ff;
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
        background: rgba(15, 23, 42, 0.9);
        padding: 10px;
        border-radius: 6px;
        border: 2px solid #54a0ff;
        margin-top: 5px;
        font-size: 13px;
        line-height: 1.4;
    }
    /* 미니게임 오버레이 UI */
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
        background: #333;
        border-radius: 10px;
        position: relative;
        overflow: hidden;
        margin: 8px 0;
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

// 속보 뉴스 이벤트 데이터 및 승률 가중치
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
    { id: 'bank', name: '🏦 헤네시스 은행', x: 80, portalX: 130, color: '#10ac84' },
    { id: 'stock', name: '📈 엘리니아 증권', x: 260, portalX: 310, color: '#2e86de' },
    { id: 'crypto', name: '🚀 커닝시티 코인', x: 440, portalX: 490, color: '#ee5253' },
    { id: 'realty', name: '🏢 리스항구 부동산', x: 620, portalX: 670, color: '#feca57' }
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

// 미니게임 제어 변수
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

// 타이밍 미니게임 시작
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
    meterSpeed = 10; // 빠른 속도
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

    let success = meterPos >= 200 && meterPos <= 260; // 초록존 적중 여부
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
    
    // 다음 턴 랜덤 속보 뉴스 생성
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

    drawMapleCharacter(player.x, player.y, player.facing);
    ctx.restore();
}

function drawTown() {
    ctx.fillStyle = '#74b9ff';
    ctx.fillRect(cameraX, 0, canvas.width, 180);
    
    ctx.fillStyle = '#0984e3';
    ctx.beginPath();
    ctx.arc(100, 200, 150, 0, Math.PI, true);
    ctx.arc(400, 220, 200, 0, Math.PI, true);
    ctx.arc(700, 190, 160, 0, Math.PI, true);
    ctx.fill();

    ctx.fillStyle = '#2ed573';
    ctx.fillRect(0, 256, 800, 90);
    ctx.fillStyle = '#26de81';
    ctx.fillRect(0, 256, 800, 10);

    buildings.forEach(b => {
        ctx.fillStyle = b.color;
        ctx.fillRect(b.x, 130, 90, 126);
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 12px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(b.name, b.x + 45, 120);

        let px = b.portalX;
        let py = 220;
        let scale = Math.sin(portalAnim) * 3;
        ctx.strokeStyle = '#00d2d3';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.ellipse(px, py, 14 + scale, 28 + scale, 0, 0, Math.PI * 2);
        ctx.stroke();

        ctx.fillStyle = 'rgba(0, 210, 211, 0.3)';
        ctx.fill();
    });
}

function drawInterior() {
    let bObj = buildings.find(b => b.id === currentScene);
    let npc = interiorNPCs[currentScene];

    ctx.fillStyle = '#d2dae2';
    ctx.fillRect(0, 0, 540, 340);
    ctx.fillStyle = bObj.color;
    ctx.fillRect(0, 0, 540, 60);
    ctx.fillStyle = '#2ed573';
    ctx.fillRect(0, 256, 540, 90);

    ctx.fillStyle = '#e67e22';
    ctx.fillRect(220, 210, 100, 46);

    ctx.strokeStyle = '#ff4757';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.ellipse(30, 220, 12, 26, 0, 0, Math.PI * 2);
    ctx.stroke();

    drawNPC(npc.x, npc.y, npc.name);
}

function drawMapleCharacter(x, y, facing) {
    let bounce = Math.sin(player.animFrame) * 2;
    if (!player.isGrounded) bounce = -4;

    ctx.fillStyle = '#ff4757';
    ctx.fillRect(x - 10, y - 26 + bounce, 20, 8);
    ctx.fillStyle = '#ff7675';
    ctx.fillRect(x - 8, y - 18 + bounce, 16, 10);

    ctx.fillStyle = '#000000';
    let eyeOff = facing === 'right' ? 2 : -4;
    ctx.fillRect(x + eyeOff, y - 14 + bounce, 3, 5);
    ctx.fillRect(x + eyeOff + 6, y - 14 + bounce, 3, 5);

    ctx.fillStyle = '#f1c40f';
    ctx.fillRect(x - 12, y - 6 + bounce, 24, 12);
    ctx.fillStyle = '#74b9ff';
    ctx.fillRect(x - 6, y - 8 + bounce, 12, 8);

    ctx.fillStyle = '#2d3436';
    ctx.font = 'bold 10px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(player.name, x, y - 32 + bounce);
}

function drawNPC(x, y, name) {
    ctx.fillStyle = '#2c3e50';
    ctx.fillRect(x - 8, y - 24, 16, 10);
    ctx.fillStyle = '#ffeaa7';
    ctx.fillRect(x - 6, y - 14, 12, 10);
    ctx.fillStyle = '#0984e3';
    ctx.fillRect(x - 8, y - 4, 16, 14);

    ctx.fillStyle = '#000000';
    ctx.font = 'bold 10px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(name, x, y - 30);
}

requestAnimationFrame(update);
</script>
</body>
</html>
"""

components.html(game_html, height=720)

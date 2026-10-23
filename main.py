import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="메이플 비치 자산관리 RPG", page_icon="🍁", layout="centered")

st.title("🍁 메이플 픽셀 비치 & 건물 입장 RPG")
st.caption("좌우 방향키(A, D)로 이동, Space키로 점프! 파란색 차원 포탈 앞에서 [위쪽 방향키(▲) / W]를 눌러 입장하세요.")

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
    #gameContainer {
        position: relative;
        margin-top: 10px;
    }
    canvas {
        border: 4px solid #ffbe76;
        border-radius: 12px;
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
</style>
</head>
<body>

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

const player = {
    x: 80,
    y: 220,
    vx: 0,
    vy: 0,
    width: 24,
    height: 36,
    speed: 5,
    jumpPower: -11,
    groundY: 220,
    isGrounded: true,
    facing: 'right',
    animFrame: 0,
    name: '메이플개미'
};

const buildings = [
    { id: 'bank', name: '🏦 헤네시스 은행', x: 80, portalX: 130, color: '#10ac84', npcName: '은행원 김수호' },
    { id: 'stock', name: '📈 엘리니아 증권', x: 260, portalX: 310, color: '#2e86de', npcName: '펀드매니저 박차트' },
    { id: 'crypto', name: '🚀 커닝시티 코인', x: 440, portalX: 490, color: '#ee5253', npcName: '중개인 나대박' },
    { id: 'realty', name: '🏢 리스항구 부동산', x: 620, portalX: 670, color: '#feca57', npcName: '중개사 최건물' }
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
            dialogue.innerHTML = `💬 <b>${npc.name}</b>: "어서오세요, 어떤 금융 거래를 진행하시겠습니까?"`;
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
        actionArea.innerHTML = `<button class="action-btn" onclick="investBank()">🏦 예금 가입 (+5%)</button> <button class="exit-btn" onclick="exitBuilding()">🚪 나가기</button>`;
    } else if (type === 'stock') {
        actionArea.innerHTML = `<button class="action-btn" onclick="investStock()">📈 주식 매수 (+30% / -20%)</button> <button class="exit-btn" onclick="exitBuilding()">🚪 나가기</button>`;
    } else if (type === 'crypto') {
        actionArea.innerHTML = `<button class="action-btn" onclick="investCrypto()">🚀 코인 올인 (+150% / -40%)</button> <button class="exit-btn" onclick="exitBuilding()">🚪 나가기</button>`;
    } else if (type === 'realty') {
        actionArea.innerHTML = `
            <button class="action-btn" onclick="buyBuilding('반지하 고시원', 10000000, 500000)">🏚️ 고시원 (1천만)</button>
            <button class="action-btn" onclick="buyBuilding('원룸 빌라', 30000000, 1500000)">🏠 빌라 (3천만)</button>
            <button class="action-btn" onclick="buyBuilding('강남 타워', 100000000, 10000000)">🏙️ 강남타워 (1억)</button>
            <button class="exit-btn" onclick="exitBuilding()">🚪 나가기</button>
        `;
    }
}

function processTurn() {
    let rentSum = 0;
    ownedBuildings.forEach(b => rentSum += b.rent);
    money += rentSum;
    turn += 1;
    updateUI();
    if (money >= 100000000) alert("🎉 1억 원 달성! 강남 건물주가 되었습니다!");
    else if (turn > 12) alert("⏱ 12턴 종료! 최종 자산: " + money.toLocaleString() + "원");
    else if (money <= 0) alert("💥 파산했습니다!");
}

function investBank() { money += Math.floor(money * 0.05); alert("🏦 적금 이자가 입금되었습니다!"); processTurn(); }
function investStock() {
    if (Math.random() < 0.5) { money += Math.floor(money * 0.3); alert("📈 주식 대폭등!"); }
    else { money -= Math.floor(money * 0.2); alert("📉 주가 손실..."); }
    processTurn();
}
function investCrypto() {
    if (Math.random() < 0.2) { money += Math.floor(money * 1.5); alert("🚀 코인 초대박 폭등!"); }
    else { money -= Math.floor(money * 0.4); alert("📉 코인 폭락..."); }
    processTurn();
}
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

components.html(game_html, height=660)

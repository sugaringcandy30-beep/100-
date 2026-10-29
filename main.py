import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="메이플 비치 자산관리 RPG", page_icon="🍁", layout="wide")

st.title("🏙️ 모던 픽셀 비치 & 대화면 RPG")
st.caption("방향키(A, D)로 이동, Space키로 점프! 자산이 늘어날수록 캐릭터 의상과 오라가 업그레이드됩니다.")

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
        width: 840px;
        background: #1e293b;
        color: #f1c40f;
        font-size: 14px;
        font-weight: bold;
        padding: 12px 18px;
        border-radius: 12px 12px 0 0;
        border: 2px solid #3d5af1;
        border-bottom: none;
        box-sizing: border-box;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    #newsTag {
        background: #e74c3c;
        color: white;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 12px;
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
        width: 840px;
        background: #121824;
        padding: 18px;
        border-radius: 12px;
        margin-top: 12px;
        box-sizing: border-box;
        border: 2px solid #3d5af1;
        box-shadow: 0 6px 20px rgba(0,0,0,0.6);
    }
    .status-bar {
        display: flex;
        justify-content: space-between;
        margin-bottom: 10px;
        font-weight: bold;
        color: #f1c40f;
        font-size: 15px;
    }
    #progressContainer {
        width: 100%;
        height: 20px;
        background: #1a2235;
        border-radius: 10px;
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
        font-size: 12px;
        text-align: center;
        line-height: 20px;
        color: white;
        font-weight: bold;
        text-shadow: 0 1px 2px rgba(0,0,0,0.8);
    }
    .action-btn {
        background: linear-gradient(135deg, #3d5af1, #2e3e91);
        color: white;
        border: 1px solid #7085ff;
        padding: 10px 18px;
        margin: 4px;
        border-radius: 8px;
        cursor: pointer;
        font-family: 'NeoDunggeunmo', sans-serif;
        font-size: 15px;
        box-shadow: 0 4px 10px rgba(61,90,241,0.3);
    }
    .action-btn:hover {
        transform: translateY(-2px);
    }
    .enter-btn {
        background: linear-gradient(135deg, #00b894, #00896f);
        color: white;
        border: 1px solid #55efc4;
        padding: 10px 24px;
        border-radius: 8px;
        cursor: pointer;
        font-family: 'NeoDunggeunmo', sans-serif;
        font-size: 16px;
        box-shadow: 0 4px 12px rgba(0,184,148,0.3);
    }
    .exit-btn {
        background: linear-gradient(135deg, #d63031, #a72828);
        color: white;
        border: 1px solid #ff7675;
        padding: 8px 18px;
        border-radius: 8px;
        cursor: pointer;
        font-family: 'NeoDunggeunmo', sans-serif;
        font-size: 14px;
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
        height: 56px;
        font-size: 18px;
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
        font-size: 15px;
        line-height: 1.5;
    }
    #minigameBox {
        display: none;
        background: #0b0e17;
        border: 2px solid #f1c40f;
        border-radius: 10px;
        padding: 16px;
        margin-top: 10px;
        text-align: center;
    }
    #meterBar {
        width: 100%;
        height: 28px;
        background: #1a2235;
        border-radius: 14px;
        position: relative;
        overflow: hidden;
        margin: 12px 0;
        border: 1px solid #3d5af1;
    }
    #meterIndicator {
        width: 18px;
        height: 100%;
        background: #ff7675;
        position: absolute;
        left: 0;
        border-radius: 4px;
    }
    #targetZone {
        width: 110px;
        height: 100%;
        background: #00b894;
        position: absolute;
        left: 330px;
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
    <canvas id="gameCanvas" width="840" height="480"></canvas>
</div>

<div id="uiBox">
    <div class="status-bar">
        <span>📍 위치: <span id="locationText">메인 스트리트</span></span>
        <span>👔 칭호: <span id="skinText" style="color:#38bdf8;">초보 개미</span></span>
        <span>📅 턴: <span id="turnText">1</span>/12</span>
        <span>💰 자산: <span id="moneyText">1,000,000</span>원</span>
    </div>

    <div id="progressContainer">
        <div id="progressBar"></div>
        <div id="progressText">1억 원 목표 달성도: 1%</div>
    </div>

    <div id="dialogue">💬 방향키로 대형 스트리트 건물을 탐험하고 입구 포탈[▲ / W]을 이용해보세요.</div>
    
    <div id="minigameBox">
        <div id="minigameTitle" style="color:#f1c40f; font-weight:bold; font-size: 16px;">🎯 타이밍 게이지 미니게임</div>
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

// 플로팅 텍스트(금액 둥둥 떠오르는 이펙트) 배열
let floatingTexts = [];

let currentNews = { text: "시티 금융 시장이 개장했습니다.", stockMod: 0, cryptoMod: 0 };
const newsEvents = [
    { text: "🔥 [찌라시] AI 반도체 대형 호재 터졌다! 주식 승률 극대화!", stockMod: 0.4, cryptoMod: 0 },
    { text: "📉 [찌라시] 가상자산 규제 단속 개시! 코인 위험 주의보!", stockMod: 0, cryptoMod: -0.3 },
    { text: "🚀 [찌라시] 유동성 자금 전격 공급! 전 시장 폭등 가능성!", stockMod: 0.25, cryptoMod: 0.3 },
    { text: "⚠️ [찌라시] 글로벌 금리 인상 속보! 자산 시장 위축 우려!", stockMod: -0.2, cryptoMod: -0.2 }
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
    { id: 'bank', name: '🏦 네오 중앙은행', x: 120, portalX: 220, colorMain: '#1e272e', accent: '#00b894' },
    { id: 'stock', name: '📈 메트로 증권타워', x: 500, portalX: 600, colorMain: '#1e272e', accent: '#3d5af1' },
    { id: 'crypto', name: '🚀 사이버 코인랩', x: 880, portalX: 980, colorMain: '#1e272e', accent: '#ff7675' },
    { id: 'realty', name: '🏢 스카이 부동산', x: 1260, portalX: 1360, colorMain: '#1e272e', accent: '#f1c40f' }
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

let meterPos = 0;
let meterSpeed = 6;
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

// 플로팅 텍스트 생성 함수
function addFloatingText(amount) {
    let text = amount >= 0 ? `+${amount.toLocaleString()}원` : `-${Math.abs(amount).toLocaleString()}원`;
    let color = amount >= 0 ? '#2ed573' : '#ff4757';
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
    if (currentScene === 'town') {
        for (let b of buildings) {
            if (Math.abs(player.x - b.portalX) < 55) {
                enterBuilding(b.id);
                return;
            }
        }
    }
}

function enterBuilding(bId) {
    currentScene = bId;
    player.x = 120;
    player.y = 320;
    const bObj = buildings.find(b => b.id === bId);
    document.getElementById('locationText').innerText = bObj.name;
    checkProximity();
}

function exitBuilding() {
    let bObj = buildings.find(b => b.id === currentScene);
    currentScene = 'town';
    player.x = bObj.portalX;
    player.y = 320;
    document.getElementById('locationText').innerText = '메인 스트리트';
    document.getElementById('minigameBox').style.display = 'none';
    meterActive = false;
    checkProximity();
}

function checkProximity() {
    const actionArea = document.getElementById('actionArea');
    const dialogue = document.getElementById('dialogue');

    if (currentScene === 'town') {
        let nearB = buildings.find(b => Math.abs(player.x - b.portalX) < 55);
        if (nearB) {
            dialogue.innerHTML = `✨ <b>[${nearB.name}] 입구입니다!</b> [▲ / W]키나 아래 버튼으로 입장하세요!`;
            actionArea.innerHTML = `<button class="enter-btn" onclick="enterBuilding('${nearB.id}')">🚪 건물 입장하기</button>`;
        } else {
            dialogue.innerHTML = "💬 방향키로 대형 건물을 탐험하고 입구 포탈로 들어가보세요!";
            actionArea.innerHTML = "";
        }
    } else {
        let npc = interiorNPCs[currentScene];
        let dist = Math.abs(player.x - npc.x);
        
        if (player.x < 70) {
            dialogue.innerHTML = "🚪 메인 스트리트로 나가는 출구입니다.";
            actionArea.innerHTML = `<button class="exit-btn" onclick="exitBuilding()">🚪 밖으로 나가기</button>`;
        } else if (dist < 100) {
            dialogue.innerHTML = `💬 <b>${npc.name}</b>: "어서오세요. 아래 버튼을 눌러 투자 미니게임을 시작할 수 있습니다."`;
            renderDialogueOptions(currentScene);
        } else {
            dialogue.innerHTML = `🏢 중앙 데스크로 조금 더 다가가면 미니게임 버튼이 나타납니다.`;
            actionArea.innerHTML = `<button class="exit-btn" onclick="exitBuilding()">🚪 밖으로 나가기</button>`;
        }
    }
}

function renderDialogueOptions(type) {
    const actionArea = document.getElementById('actionArea');
    if (type === 'bank') {
        actionArea.innerHTML = `<button class="action-btn" onclick="investBank()">🏦 예금 가입 (+5% 확정)</button> <button class="exit-btn" onclick="exitBuilding()">🚪 나가기</button>`;
    } else if (type === 'stock') {
        actionArea.innerHTML = `<button class="action-btn" style="background: linear-gradient(135deg, #e67e22, #d35400);" onclick="startStockMiniGame()">🎮 [미니게임] 주식 매수 타이밍 도전</button> <button class="exit-btn" onclick="exitBuilding()">🚪 나가기</button>`;
    } else if (type === 'crypto') {
        actionArea.innerHTML = `<button class="action-btn" style="background: linear-gradient(135deg, #e74c3c, #c0392b);" onclick="startCryptoMiniGame()">🎮 [미니게임] 코인 폭발 타이밍 도전</button> <button class="exit-btn" onclick="exitBuilding()">🚪 나가기</button>`;
    } else if (type === 'realty') {
        actionArea.innerHTML = `
            <button class="action-btn" onclick="buyBuilding('초역세권 오피스텔', 30000000, 2000000)">🏠 오피스텔 (3천만)</button>
            <button class="action-btn" onclick="buyBuilding('테헤란로 빌딩', 60000000, 5000000)">🏢 빌딩 (6천만)</button>
            <button class="action-btn" onclick="buyBuilding('강남 타워', 100000000, 12000000)">🏙️ 강남타워 (1억)</button>
            <button class="exit-btn" onclick="exitBuilding()">🚪 나가기</button>
        `;
    }
}

function startStockMiniGame() {
    document.getElementById('actionArea').innerHTML = '';
    document.getElementById('minigameBox').style.display = 'block';
    document.getElementById('minigameTitle').innerText = '📈 [증권 미니게임] 게이지가 초록 영역에 올 때 STOP을 누르세요!';
    meterPos = 0;
    meterSpeed = 8;
    meterActive = true;
    updateMeter();
}

function startCryptoMiniGame() {
    document.getElementById('actionArea').innerHTML = '';
    document.getElementById('minigameBox').style.display = 'block';
    document.getElementById('minigameTitle').innerText = '🚀 [코인 미니게임] 고속 게이지 초록 타겟 적중 시 +200% 폭등!';
    meterPos = 0;
    meterSpeed = 14;
    meterActive = true;
    updateMeter();
}

function updateMeter() {
    if (!meterActive) return;
    meterPos += meterSpeed;
    if (meterPos > 780 || meterPos < 0) meterSpeed *= -1;
    document.getElementById('meterIndicator').style.left = meterPos + 'px';
    meterAnimId = requestAnimationFrame(updateMeter);
}

function stopMeter() {
    meterActive = false;
    cancelAnimationFrame(meterAnimId);
    document.getElementById('minigameBox').style.display = 'none';

    let success = meterPos >= 330 && meterPos <= 440;
    
    if (currentScene === 'stock') {
        let winProb = 0.5 + currentNews.stockMod;
        if (success || Math.random() < winProb) {
            let profit = Math.floor(money * 0.4);
            money += profit;
            addFloatingText(profit);
            alert(`🎉 [주식 대성공!] 타이밍 적중! +${profit.toLocaleString()}원 수익 달성!`);
        } else {
            let loss = Math.floor(money * 0.2);
            money -= loss;
            addFloatingText(-loss);
            alert(`📉 [주식 손실] 타이밍 실패... -${loss.toLocaleString()}원`);
        }
    } else if (currentScene === 'crypto') {
        if (success) {
            let profit = Math.floor(money * 2.0);
            money += profit;
            addFloatingText(profit);
            alert(`🚀 [코인 초대박!] 초록 타겟 정확히 저격! +${profit.toLocaleString()}원 대폭등!!`);
        } else {
            let loss = Math.floor(money * 0.5);
            money -= loss;
            addFloatingText(-loss);
            alert(`💥 [코인 청산] 타이밍 실패로 -${loss.toLocaleString()}원 손실...`);
        }
    }
    processTurn();
}

function processTurn() {
    let rentSum = 0;
    ownedBuildings.forEach(b => rentSum += b.rent);
    if (rentSum > 0) {
        money += rentSum;
        addFloatingText(rentSum);
    }
    turn += 1;
    
    if (Math.random() < 0.75) {
        currentNews = newsEvents[Math.floor(Math.random() * newsEvents.length)];
    } else {
        currentNews = { text: "시티 금융 시장이 비교적 안정세를 유지하고 있습니다.", stockMod: 0, cryptoMod: 0 };
    }
    document.getElementById('newsText').innerText = currentNews.text;

    updateUI();
    if (money >= goalMoney) alert("🎉 1억 원 달성! 강남 건물주가 되었습니다!");
    else if (turn > 12) alert("⏱ 12턴 종료! 최종 자산: " + money.toLocaleString() + "원");
    else if (money <= 0) alert("💥 파산했습니다!");
}

function investBank() {
    let interest = Math.floor(money * 0.05);
    money += interest;
    addFloatingText(interest);
    alert("🏦 예금 이자가 입금되었습니다!");
    processTurn();
}

function buyBuilding(name, price, rent) {
    if (money < price) { alert("자산이 부족합니다!"); return; }
    money -= price;
    addFloatingText(-price);
    ownedBuildings.push({ name, rent });
    alert(`🎉 [${name}] 매수 성공! 매 턴 월세가 들어옵니다.`);
    updateUI();
}

function updateUI() {
    document.getElementById('moneyText').innerText = money.toLocaleString();
    document.getElementById('turnText').innerText = turn;

    // 자산 구간별 의상/칭호 업그레이드
    const skinText = document.getElementById('skinText');
    if (money >= 50000000) {
        skinText.innerText = "👑 골드 건물주";
        skinText.style.color = "#f1c40f";
    } else if (money >= 20000000) {
        skinText.innerText = "💼 명품 트레이더";
        skinText.style.color = "#a855f7";
    } else {
        skinText.innerText = "👔 초보 개미";
        skinText.style.color = "#38bdf8";
    }

    let percent = Math.min(100, Math.max(1, Math.floor((money / goalMoney) * 100)));
    document.getElementById('progressBar').style.width = percent + '%';
    document.getElementById('progressText').innerText = `1억 원 목표 달성도: ${percent}% (${money.toLocaleString()}원 / 100,000,000원)`;
}

function update() {
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
    draw();
    requestAnimationFrame(update);
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.save();
    ctx.translate(-cameraX, 0);

    if (currentScene === 'town') drawTown();
    else drawInterior();

    drawModernPlayer(player.x, player.y, player.facing);
    drawFloatingTexts();

    ctx.restore();
}

function drawTown() {
    let skyGradient = ctx.createLinearGradient(0, 0, 0, 260);
    skyGradient.addColorStop(0, '#0f172a');
    skyGradient.addColorStop(1, '#1e293b');
    ctx.fillStyle = skyGradient;
    ctx.fillRect(cameraX, 0, canvas.width, 260);

    ctx.fillStyle = '#111827';
    ctx.fillRect(cameraX + 50, 100, 90, 160);
    ctx.fillRect(cameraX + 300, 70, 110, 190);
    ctx.fillRect(cameraX + 700, 80, 100, 180);
    ctx.fillRect(cameraX + 1100, 50, 130, 210);

    ctx.fillStyle = '#334155';
    ctx.fillRect(0, 360, 1600, 120);
    ctx.fillStyle = '#475569';
    ctx.fillRect(0, 360, 1600, 14);

    buildings.forEach(b => {
        ctx.fillStyle = b.colorMain;
        ctx.fillRect(b.x, 110, 200, 250);

        ctx.fillStyle = '#334155';
        for (let wx = b.x + 20; wx < b.x + 180; wx += 40) {
            for (let wy = 140; wy < 320; wy += 45) {
                ctx.fillRect(wx, wy, 22, 28);
                ctx.fillStyle = '#f1c40f';
                ctx.fillRect(wx + 3, wy + 3, 16, 22);
                ctx.fillStyle = '#334155';
            }
        }

        ctx.fillStyle = b.accent;
        ctx.fillRect(b.x, 80, 200, 30);
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 14px NeoDunggeunmo, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(b.name, b.x + 100, 100);

        let px = b.portalX;
        let py = 320;
        let scale = Math.sin(portalAnim) * 5;
        
        ctx.strokeStyle = '#00d2d3';
        ctx.lineWidth = 5;
        ctx.beginPath();
        ctx.ellipse(px, py, 20 + scale, 38 + scale, 0, 0, Math.PI * 2);
        ctx.stroke();

        ctx.fillStyle = 'rgba(0, 210, 211, 0.4)';
        ctx.fill();
    });
}

function drawInterior() {
    let bObj = buildings.find(b => b.id === currentScene);
    let npc = interiorNPCs[currentScene];

    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 0, 840, 480);
    
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(0, 0, 840, 90);

    ctx.fillStyle = '#334155';
    ctx.fillRect(0, 360, 840, 120);

    ctx.fillStyle = '#38bdf8';
    ctx.fillRect(340, 300, 160, 60);
    ctx.fillStyle = '#0284c7';
    ctx.fillRect(340, 350, 160, 10);

    ctx.strokeStyle = '#ff4757';
    ctx.lineWidth = 5;
    ctx.beginPath();
    ctx.ellipse(40, 320, 18, 36, 0, 0, Math.PI * 2);
    ctx.stroke();

    drawModernNPC(npc.x, npc.y, npc.name);
}

// 자산 구간별 플레이어 스킨 렌더링
function drawModernPlayer(x, y, facing) {
    let bounce = Math.sin(player.animFrame) * 2;
    if (!player.isGrounded) bounce = -6;

    // 5천만 원 이상: 황금 후광 오라 연출
    if (money >= 50000000) {
        ctx.save();
        ctx.strokeStyle = '#f1c40f';
        ctx.lineWidth = 3;
        ctx.shadowColor = '#f1c40f';
        ctx.shadowBlur = 12;
        ctx.beginPath();
        ctx.arc(x, y - 18 + bounce, 28, 0, Math.PI * 2);
        ctx.stroke();
        ctx.restore();
    }

    // 외곽선
    ctx.fillStyle = '#000000';
    ctx.fillRect(x - 15, y - 40 + bounce, 30, 48);

    // 얼굴 피부
    ctx.fillStyle = '#f8c291';
    ctx.fillRect(x - 10, y - 28 + bounce, 20, 15);

    // 자산별 헤어 및 수트 색상 커스터마이징
    if (money >= 50000000) {
        // [골드 건물주] 황금 헤어 + 골드 라이닝 수트
        ctx.fillStyle = '#f1c40f';
        ctx.fillRect(x - 12, y - 36 + bounce, 24, 10);

        ctx.fillStyle = '#1e293b';
        ctx.fillRect(x - 9, y - 13 + bounce, 18, 15);
        ctx.fillStyle = '#f1c40f';
        ctx.fillRect(x - 2, y - 13 + bounce, 4, 15); // 황금 넥타이
    } else if (money >= 20000000) {
        // [명품 트레이더] 보라색 세련된 헤어 + 럭셔리 턱시도
        ctx.fillStyle = '#a855f7';
        ctx.fillRect(x - 12, y - 36 + bounce, 24, 10);

        ctx.fillStyle = '#0f172a';
        ctx.fillRect(x - 9, y - 13 + bounce, 18, 15);
        ctx.fillStyle = '#e2e8f0';
        ctx.fillRect(x - 2, y - 13 + bounce, 4, 15);
    } else {
        // [초보 개미] 블루 파란 헤어 + 기본 블루 수트
        ctx.fillStyle = '#3d5af1';
        ctx.fillRect(x - 12, y - 36 + bounce, 24, 10);

        ctx.fillStyle = '#ffffff';
        ctx.fillRect(x - 9, y - 13 + bounce, 18, 15);
        ctx.fillStyle = '#1e293b';
        if (facing === 'right') {
            ctx.fillRect(x + 1, y - 13 + bounce, 8, 15);
        } else {
            ctx.fillRect(x - 9, y - 13 + bounce, 8, 15);
        }
    }

    // 이름표 UI
    ctx.fillStyle = 'rgba(0,0,0,0.8)';
    ctx.fillRect(x - 40, y - 56 + bounce, 80, 16);
    ctx.fillStyle = money >= 50000000 ? '#f1c40f' : '#ffffff';
    ctx.font = 'bold 12px NeoDunggeunmo, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(player.name, x, y - 44 + bounce);
}

// 머리 위 둥둥 떠오르는 플로팅 텍스트 이펙트 그려주기
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
        ctx.font = 'bold 16px NeoDunggeunmo, sans-serif';
        ctx.textAlign = 'center';
        ctx.shadowColor = '#000000';
        ctx.shadowBlur = 4;
        ctx.fillText(ft.text, ft.x, ft.y);
        ctx.restore();
    }
}

function drawModernNPC(x, y, name) {
    ctx.fillStyle = '#000000';
    ctx.fillRect(x - 15, y - 40, 30, 48);

    ctx.fillStyle = '#f8c291';
    ctx.fillRect(x - 10, y - 28, 20, 15);
    ctx.fillStyle = '#00b894';
    ctx.fillRect(x - 12, y - 36, 24, 10);
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(x - 9, y - 13, 18, 15);

    ctx.fillStyle = 'rgba(0,0,0,0.8)';
    ctx.fillRect(x - 55, y - 56, 110, 16);
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 12px NeoDunggeunmo, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(name, x, y - 44);
}

requestAnimationFrame(update);
</script>
</body>
</html>
"""

components.html(game_html, height=920)

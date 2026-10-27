import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="메이플 비치 자산관리 RPG", page_icon="🍁", layout="centered")

st.title("🏙️ 모던 픽셀 비치 & 투자 RPG")
st.caption("방향키(A, D)로 이동, Space키로 점프! 웅장해진 건물 입구 포탈[▲ / W]로 입장하세요.")

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
    #newsTicker {
        width: 600px;
        background: #181f2c;
        color: #f1c40f;
        font-size: 14px;
        font-weight: bold;
        padding: 10px 16px;
        border-radius: 12px 12px 0 0;
        border: 2px solid #3d5af1;
        border-bottom: none;
        box-sizing: border-box;
        overflow: hidden;
        white-space: nowrap;
        box-shadow: 0 -4px 15px rgba(0,0,0,0.5);
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
    /* 목표 달성 프로그레스 바 스타일 */
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
    #minigameBox {
        display: none;
        background: #0b0e17;
        border: 2px solid #f1c40f;
        border-radius: 10px;
        padding: 12px;
        margin-top: 10px;
        text-align: center;
    }
    #meterBar {
        width: 100%;
        height: 22px;
        background: #1a2235;
        border-radius: 11px;
        position: relative;
        overflow: hidden;
        margin: 10px 0;
        border: 1px solid #3d5af1;
    }
    #meterIndicator {
        width: 14px;
        height: 100%;
        background: #ff7675;
        position: absolute;
        left: 0;
    }
    #targetZone {
        width: 70px;
        height: 100%;
        background: #00b894;
        position: absolute;
        left: 230px;
    }
</style>
</head>
<body>

<div id="newsTicker">📰 [속보] 모던 자산관리 시티에 환영합니다! 목표: 1억 원 건물주 되기!</div>

<div id="gameContainer">
    <canvas id="gameCanvas" width="600" height="380"></canvas>
</div>

<div id="uiBox">
    <div class="status-bar">
        <span>📍 위치: <span id="locationText">메인 스트리트</span></span>
        <span>📅 턴: <span id="turnText">1</span>/12</span>
        <span>💰 자산: <span id="moneyText">1,000,000</span>원</span>
    </div>

    <!-- 목표 달성 진행도 게이지 바 -->
    <div id="progressContainer">
        <div id="progressBar"></div>
        <div id="progressText">1억 원 목표 달성도: 1%</div>
    </div>

    <div id="dialogue">💬 방향키로 대형 스트리트 건물을 탐험하고 입구 포탈[▲ / W]을 이용해보세요.</div>
    
    <div id="minigameBox">
        <div id="minigameTitle" style="color:#f1c40f; font-weight:bold;">🎯 타이밍 게이지 미니게임</div>
        <div id="meterBar">
            <div id="targetZone"></div>
            <div id="meterIndicator"></div>
        </div>
        <button class="action-btn" onclick="stopMeter()">STOP (매수 실행)</button>
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
const goalMoney = 100000000; // 목표 1억 원

let currentNews = { text: "평화로운 모던 시티입니다.", stockMod: 0, cryptoMod: 0 };
const newsEvents = [
    { text: "🔥 [속보] AI 딥러닝 혁신 발표! 주식 시장 강세!", stockMod: 0.35, cryptoMod: 0 },
    { text: "📉 [속보] 글로벌 가상자산 규제 강화 발표! 코인 시장 위축!", stockMod: 0, cryptoMod: -0.3 },
    { text: "🚀 [속보] 시티 중앙은행 자산 매입 시동! 주식/코인 동반 폭등!", stockMod: 0.2, cryptoMod: 0.25 },
    { text: "⚠️ [속보] 부동산 시장 세제 혜택 발표! 월세 수익률 상승!", stockMod: 0.1, cryptoMod: 0 }
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
function jump() {
    if (player.isGrounded) {
        player.vy = player.jumpPower;
        player.isGrounded = false;
    }
}

function interactPortal() {
    if (currentScene === 'town') {
        for (let b of buildings) {
            if (Math.abs(player.x - b.portalX) < 45) {
                enterBuilding(b.id);
                return;
            }
        }
    }
}

function enterBuilding(bId) {
    currentScene = bId;
    player.x = 100;
    player.y = 250;
    const bObj = buildings.find(b => b.id === bId);
    document.getElementById('locationText').innerText = bObj.name;
    checkProximity();
}

function exitBuilding() {
    let bObj = buildings.find(b => b.id === currentScene);
    currentScene = 'town';
    player.x = bObj.portalX;
    player.y = 250;
    document.getElementById('locationText').innerText = '메인 스트리트';
    document.getElementById('minigameBox').style.display = 'none';
    meterActive = false;
    checkProximity();
}

function checkProximity() {
    const actionArea = document.getElementById('actionArea');
    const dialogue = document.getElementById('dialogue');

    if (currentScene === 'town') {
        let nearB = buildings.find(b => Math.abs(player.x - b.portalX) < 45);
        if (nearB) {
            dialogue.innerHTML = `✨ <b>[${nearB.name}] 대형 입구입니다!</b> [▲ / W]를 누르거나 버튼을 누르면 입장합니다.`;
            actionArea.innerHTML = `<button class="enter-btn" onclick="enterBuilding('${nearB.id}')">🚪 로비 입장하기</button>`;
        } else {
            dialogue.innerHTML = "💬 방향키로 대형 건물들을 구경하며 이동해보세요!";
            actionArea.innerHTML = "";
        }
    } else {
        let npc = interiorNPCs[currentScene];
        let dist = Math.abs(player.x - npc.x);
        
        if (player.x < 50) {
            dialogue.innerHTML = "🚪 메인 스트리트로 나가는 출구입니다.";
            actionArea.innerHTML = `<button class="exit-btn" onclick="exitBuilding()">🚪 밖으로 나가기</button>`;
        } else if (dist < 60) {
            dialogue.innerHTML = `💬 <b>${npc.name}</b>: "어서오세요. 모던 시티 금융 라운지입니다."`;
            renderDialogueOptions(currentScene);
        } else {
            dialogue.innerHTML = `🏢 중앙 라운지 데스크에 위치한 전문 담당자에게 다가가세요.`;
            actionArea.innerHTML = `<button class="exit-btn" onclick="exitBuilding()">🚪 밖으로 나가기</button>`;
        }
    }
}

function renderDialogueOptions(type) {
    const actionArea = document.getElementById('actionArea');
    if (type === 'bank') {
        actionArea.innerHTML = `<button class="action-btn" onclick="investBank()">🏦 프라이빗 예금 가입 (+5%)</button> <button class="exit-btn" onclick="exitBuilding()">🚪 나가기</button>`;
    } else if (type === 'stock') {
        actionArea.innerHTML = `<button class="action-btn" onclick="startStockMiniGame()">🎯 주식 매수 타이밍 도전</button> <button class="exit-btn" onclick="exitBuilding()">🚪 나가기</button>`;
    } else if (type === 'crypto') {
        actionArea.innerHTML = `<button class="action-btn" onclick="startCryptoMiniGame()">🎰 코인 폭발 타이밍 도전</button> <button class="exit-btn" onclick="exitBuilding()">🚪 나가기</button>`;
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
    meterSpeed = 9;
    meterActive = true;
    updateMeter();
}

function updateMeter() {
    if (!meterActive) return;
    meterPos += meterSpeed;
    if (meterPos > 560 || meterPos < 0) meterSpeed *= -1;
    document.getElementById('meterIndicator').style.left = meterPos + 'px';
    meterAnimId = requestAnimationFrame(updateMeter);
}

function stopMeter() {
    meterActive = false;
    cancelAnimationFrame(meterAnimId);
    document.getElementById('minigameBox').style.display = 'none';

    let success = meterPos >= 220 && meterPos <= 290;
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
    if (money >= goalMoney) alert("🎉 1억 원 달성! 강남 건물주가 되었습니다!");
    else if (turn > 12) alert("⏱ 12턴 종료! 최종 자산: " + money.toLocaleString() + "원");
    else if (money <= 0) alert("💥 파산했습니다!");
}

function investBank() { money += Math.floor(money * 0.05); alert("🏦 예금 이자가 입금되었습니다!"); processTurn(); }
function buyBuilding(name, price, rent) {
    if (money < price) { alert("자산이 부족합니다!"); return; }
    money -= price; ownedBuildings.push({ name, rent });
    alert(`🎉 [${name}] 매수 성공! 매 턴마다 월세 수익이 들어옵니다.`); updateUI();
}

function updateUI() {
    document.getElementById('moneyText').innerText = money.toLocaleString();
    document.getElementById('turnText').innerText = turn;

    // 프로그레스 바 연동 계산
    let percent = Math.min(100, Math.max(1, Math.floor((money / goalMoney) * 100)));
    document.getElementById('progressBar').style.width = percent + '%';
    document.getElementById('progressText').innerText = `1억 원 목표 달성도: ${percent}% (${money.toLocaleString()}원 / 100,000,000원)`;
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
        player.x = Math.max(20, Math.min(1180, player.x));
        cameraX = player.x - canvas.width / 2;
        cameraX = Math.max(0, Math.min(1200 - canvas.width, cameraX));
    } else {
        player.x = Math.max(20, Math.min(580, player.x));
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
    ctx.restore();
}

function drawTown() {
    // 모던 스카이라인 야경 그라데이션
    let skyGradient = ctx.createLinearGradient(0, 0, 0, 200);
    skyGradient.addColorStop(0, '#0f172a');
    skyGradient.addColorStop(1, '#1e293b');
    ctx.fillStyle = skyGradient;
    ctx.fillRect(cameraX, 0, canvas.width, 200);

    // 원경 빌딩 실루엣
    ctx.fillStyle = '#111827';
    ctx.fillRect(cameraX + 50, 80, 70, 120);
    ctx.fillRect(cameraX + 220, 50, 90, 150);
    ctx.fillRect(cameraX + 520, 60, 80, 140);
    ctx.fillRect(cameraX + 820, 40, 100, 160);

    // 거리 바닥
    ctx.fillStyle = '#334155';
    ctx.fillRect(0, 280, 1200, 100);
    ctx.fillStyle = '#475569';
    ctx.fillRect(0, 280, 1200, 12); // 인도 경계석

    // 대형 스카이라인 건물 (폭 150)
    buildings.forEach(b => {
        // 건물 본체
        ctx.fillStyle = b.colorMain;
        ctx.fillRect(b.x, 90, 150, 190);

        // 건물 창문 그리드 패턴
        ctx.fillStyle = '#334155';
        for (let wx = b.x + 15; wx < b.x + 135; wx += 30) {
            for (let wy = 110; wy < 240; wy += 35) {
                ctx.fillRect(wx, wy, 16, 22);
                ctx.fillStyle = '#f1c40f'; // 노란 불빛 창문
                ctx.fillRect(wx + 2, wy + 2, 12, 18);
                ctx.fillStyle = '#334155';
            }
        }

        // 웅장한 간판 상단 바
        ctx.fillStyle = b.accent;
        ctx.fillRect(b.x, 70, 150, 22);
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 12px NeoDunggeunmo, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(b.name, b.x + 75, 85);

        // 차원 포탈 이펙트
        let px = b.portalX;
        let py = 250;
        let scale = Math.sin(portalAnim) * 4;
        
        ctx.strokeStyle = '#00d2d3';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.ellipse(px, py, 16 + scale, 30 + scale, 0, 0, Math.PI * 2);
        ctx.stroke();

        ctx.fillStyle = 'rgba(0, 210, 211, 0.4)';
        ctx.fill();
    });
}

function drawInterior() {
    let bObj = buildings.find(b => b.id === currentScene);
    let npc = interiorNPCs[currentScene];

    // 실내 라운지 바닥 및 벽
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 0, 600, 380);
    
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(0, 0, 600, 70);

    ctx.fillStyle = '#334155';
    ctx.fillRect(0, 280, 600, 100);

    // 고급 인포메이션 데스크
    ctx.fillStyle = '#38bdf8';
    ctx.fillRect(240, 230, 120, 50);
    ctx.fillStyle = '#0284c7';
    ctx.fillRect(240, 270, 120, 10);

    // 출구 포탈
    ctx.strokeStyle = '#ff4757';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.ellipse(30, 250, 14, 28, 0, 0, Math.PI * 2);
    ctx.stroke();

    drawModernNPC(npc.x, npc.y, npc.name);
}

function drawModernPlayer(x, y, facing) {
    let bounce = Math.sin(player.animFrame) * 2;
    if (!player.isGrounded) bounce = -5;

    // 모던 아바타 (정장 캐릭터 스타일)
    ctx.fillStyle = '#000000';
    ctx.fillRect(x - 12, y - 32 + bounce, 24, 38);

    ctx.fillStyle = '#f8c291'; // 얼굴
    ctx.fillRect(x - 8, y - 22 + bounce, 16, 12);

    ctx.fillStyle = '#3d5af1'; // 머리 스타일
    ctx.fillRect(x - 9, y - 28 + bounce, 18, 8);

    ctx.fillStyle = '#ffffff'; // 셔츠 및 정장
    ctx.fillRect(x - 7, y - 10 + bounce, 14, 12);
    ctx.fillStyle = '#1e293b';
    if (facing === 'right') {
        ctx.fillRect(x + 1, y - 10 + bounce, 6, 12);
    } else {
        ctx.fillRect(x - 7, y - 10 + bounce, 6, 12);
    }

    // 이름표 UI
    ctx.fillStyle = 'rgba(0,0,0,0.8)';
    ctx.fillRect(x - 30, y - 44 + bounce, 60, 14);
    ctx.fillStyle = '#f1c40f';
    ctx.font = 'bold 10px NeoDunggeunmo, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(player.name, x, y - 34 + bounce);
}

function drawModernNPC(x, y, name) {
    ctx.fillStyle = '#000000';
    ctx.fillRect(x - 12, y - 32, 24, 38);

    ctx.fillStyle = '#f8c291';
    ctx.fillRect(x - 8, y - 22, 16, 12);
    ctx.fillStyle = '#00b894';
    ctx.fillRect(x - 9, y - 28, 18, 8);
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(x - 7, y - 10, 14, 12);

    ctx.fillStyle = 'rgba(0,0,0,0.8)';
    ctx.fillRect(x - 45, y - 44, 90, 14);
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 10px NeoDunggeunmo, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(name, x, y - 34);
}

requestAnimationFrame(update);
</script>
</body>
</html>
"""

components.html(game_html, height=760)

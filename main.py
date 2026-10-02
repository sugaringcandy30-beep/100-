import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="픽셀 비치 RPG", page_icon="🏖️", layout="centered")

st.title("🏖️ 픽셀 비치 타운 & 건물 입장 RPG")
st.caption("방향키(W, A, S, D)나 조이스틱으로 해변의 튜브 탄 캐릭터를 직접 조종해 보세요!")

game_html = """
<!DOCTYPE html>
<html>
<head>
<style>
    body {
        margin: 0;
        padding: 0;
        background-color: #0c2461;
        color: white;
        font-family: 'Courier New', Courier, monospace;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    #gameContainer {
        position: relative;
        margin-top: 10px;
    }
    canvas {
        border: 4px solid #f39c12;
        border-radius: 8px;
        background-color: #1e272e;
        box-shadow: 0 8px 20px rgba(0,0,0,0.8);
        image-rendering: pixelated; /* 도트 픽셀을 선명하게 처리 */
    }
    #uiBox {
        width: 480px;
        background-color: #1e3799;
        padding: 12px;
        border-radius: 8px;
        margin-top: 10px;
        box-sizing: border-box;
        border: 2px solid #4a69bd;
    }
    .status-bar {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
        font-weight: bold;
        color: #f8c291;
    }
    .action-btn {
        background-color: #e55039;
        color: white;
        border: none;
        padding: 8px 12px;
        margin: 4px;
        border-radius: 4px;
        cursor: pointer;
        font-weight: bold;
    }
    .action-btn:hover {
        background-color: #eb2f06;
    }
    .enter-btn {
        background-color: #2ed573;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        cursor: pointer;
        font-weight: bold;
        font-size: 14px;
    }
    .exit-btn {
        background-color: #b71540;
        color: white;
        border: none;
        padding: 6px 12px;
        border-radius: 4px;
        cursor: pointer;
        font-weight: bold;
    }
    .controls {
        display: grid;
        grid-template-columns: repeat(3, 50px);
        gap: 5px;
        justify-content: center;
        margin-top: 10px;
    }
    .ctrl-btn {
        width: 50px;
        height: 50px;
        font-size: 18px;
        font-weight: bold;
        background: #0c2461;
        color: #f8c291;
        border: 2px solid #e55039;
        border-radius: 8px;
        cursor: pointer;
    }
    .ctrl-btn:active {
        background: #e55039;
        color: white;
    }
    #dialogue {
        min-height: 48px;
        background: #0c2461;
        padding: 10px;
        border-radius: 4px;
        border: 1px solid #4a69bd;
        margin-top: 5px;
        font-size: 13px;
        line-height: 1.4;
    }
</style>
</head>
<body>

<div id="gameContainer">
    <canvas id="gameCanvas" width="480" height="360"></canvas>
</div>

<div id="uiBox">
    <div class="status-bar">
        <span>📍 위치: <span id="locationText">해변 리조트</span></span>
        <span>📅 턴: <span id="turnText">1</span>/12</span>
        <span>💰 현금: <span id="moneyText">1,000,000</span>원</span>
    </div>
    <div id="dialogue">💬 방향키로 파도를 가르며 상점 입구로 이동해보세요!</div>
    <div id="actionArea" style="margin-top: 8px; text-align: center;"></div>
</div>

<div class="controls">
    <div></div>
    <button class="ctrl-btn" onclick="moveChar(0, -15)">▲</button>
    <div></div>
    <button class="ctrl-btn" onclick="moveChar(-15, 0)">◄</button>
    <button class="ctrl-btn" onclick="moveChar(0, 15)">▼</button>
    <button class="ctrl-btn" onclick="moveChar(15, 0)">►</button>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let money = 1000000;
let turn = 1;
let currentScene = 'town'; // 'town' 또는 건물 ID
let ownedBuildings = [];

// 플레이어 (튜브 탄 도트 캐릭터)
const player = {
    x: 225,
    y: 200,
    size: 28,
    speed: 12,
    name: '튜브개미'
};

// 해변 상점 건물 데이터
const buildings = [
    { id: 'bank', name: '🏦 해변 은행', x: 40, y: 30, w: 100, h: 70, roofColor: '#2ed573', wallColor: '#55efc4' },
    { id: 'stock', name: '📈 파도 증권', x: 340, y: 30, w: 100, h: 70, roofColor: '#1e90ff', wallColor: '#70a1ff' },
    { id: 'crypto', name: '🚀 코인 파라솔', x: 40, y: 240, w: 100, h: 70, roofColor: '#ff4757', wallColor: '#ff6b81' },
    { id: 'realty', name: '🏢 오션 부동산', x: 340, y: 240, w: 100, h: 70, roofColor: '#ffa502', wallColor: '#eccc68' }
];

// 건물 내부 NPC
const interiorNPCs = {
    bank: { x: 225, y: 70, name: '🏦 은행원 김수호' },
    stock: { x: 225, y: 70, name: '📈 펀드매니저 박차트' },
    crypto: { x: 225, y: 70, name: '🚀 중개인 나대박' },
    realty: { x: 225, y: 70, name: '🏢 중개사 최건물' }
};

let nearTarget = null;

// 키보드 이동
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') moveChar(0, -player.speed);
    if (e.key === 'ArrowDown' || e.key === 's' || e.key === 'S') moveChar(0, player.speed);
    if (e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') moveChar(-player.speed, 0);
    if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') moveChar(player.speed, 0);
});

function moveChar(dx, dy) {
    if (turn > 12 || money <= 0) return;
    
    player.x = Math.max(15, Math.min(canvas.width - player.size - 15, player.x + dx));
    player.y = Math.max(15, Math.min(canvas.height - player.size - 15, player.y + dy));
    
    checkProximity();
    draw();
}

function checkProximity() {
    nearTarget = null;
    const actionArea = document.getElementById('actionArea');
    const dialogue = document.getElementById('dialogue');
    
    if (currentScene === 'town') {
        for (let b of buildings) {
            let cx = b.x + b.w / 2;
            let cy = b.y + b.h;
            let dist = Math.hypot(cx - (player.x + player.size/2), cy - (player.y + player.size/2));
            if (dist < 45) {
                nearTarget = b;
                break;
            }
        }
        
        if (nearTarget) {
            dialogue.innerHTML = `📍 <b>[${nearTarget.name}]</b> 입구입니다.`;
            actionArea.innerHTML = `<button class="enter-btn" onclick="enterBuilding('${nearTarget.id}')">🚪 건물 입장하기</button>`;
        } else {
            dialogue.innerHTML = "💬 해변을 거닐며 원하는 상점 입구로 다가가 보세요!";
            actionArea.innerHTML = "";
        }
    } else {
        let npc = interiorNPCs[currentScene];
        let dist = Math.hypot((npc.x + 14) - (player.x + player.size/2), (npc.y + 14) - (player.y + player.size/2));
        
        if (player.y > canvas.height - 50) {
            dialogue.innerHTML = "🚪 밖으로 나가는 출구입니다.";
            actionArea.innerHTML = `<button class="exit-btn" onclick="exitBuilding()">🚪 밖으로 나가기</button>`;
        } else if (dist < 55) {
            dialogue.innerHTML = `💬 <b>${npc.name}</b>: "어서오세요, 어떤 거래를 도와드릴까요?"`;
            renderDialogueOptions(currentScene);
        } else {
            dialogue.innerHTML = `🏢 [${buildings.find(b=>b.id===currentScene).name} 내부] 카운터의 직원에게 다가가 보세요.`;
            actionArea.innerHTML = `<button class="exit-btn" onclick="exitBuilding()">🚪 밖으로 나가기</button>`;
        }
    }
}

function enterBuilding(buildingId) {
    currentScene = buildingId;
    player.x = 225;
    player.y = 280;
    
    const bObj = buildings.find(b => b.id === buildingId);
    document.getElementById('locationText').innerText = bObj.name;
    checkProximity();
    draw();
}

function exitBuilding() {
    let bObj = buildings.find(b => b.id === currentScene);
    currentScene = 'town';
    player.x = bObj.x + bObj.w/2 - player.size/2;
    player.y = bObj.y + bObj.h + 10;
    
    document.getElementById('locationText').innerText = '해변 리조트';
    checkProximity();
    draw();
}

function renderDialogueOptions(type) {
    const actionArea = document.getElementById('actionArea');
    
    if (type === 'bank') {
        actionArea.innerHTML = `
            <button class="action-btn" onclick="investBank()">🏦 예금 가입 (+5%)</button>
            <button class="exit-btn" onclick="exitBuilding()">🚪 나가기</button>
        `;
    } else if (type === 'stock') {
        actionArea.innerHTML = `
            <button class="action-btn" onclick="investStock()">📈 주식 매수 (+30% / -20%)</button>
            <button class="exit-btn" onclick="exitBuilding()">🚪 나가기</button>
        `;
    } else if (type === 'crypto') {
        actionArea.innerHTML = `
            <button class="action-btn" onclick="investCrypto()">🚀 코인 올인 (+150% / -40%)</button>
            <button class="exit-btn" onclick="exitBuilding()">🚪 나가기</button>
        `;
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
    
    if (money >= 100000000) {
        alert("🎉 축하합니다! 1억 원을 모아 건물주가 되었습니다!");
    } else if (turn > 12) {
        alert("⏱️️ 12턴이 지났습니다! 최종 보유 자산: " + money.toLocaleString() + "원");
    } else if (money <= 0) {
        alert("💥 파산했습니다! 게임 오버!");
    }
}

function investBank() {
    let profit = Math.floor(money * 0.05);
    money += profit;
    alert(`🏦 [김수호 직원]: "이자 +${profit.toLocaleString()}원이 입금되었습니다."`);
    processTurn();
}

function investStock() {
    if (Math.random() < 0.5) {
        let profit = Math.floor(money * 0.3);
        money += profit;
        alert(`📈 [박차트 매니저]: "주식이 대폭등했습니다! +${profit.toLocaleString()}원!"`);
    } else {
        let loss = Math.floor(money * 0.2);
        money -= loss;
        alert(`📉 [박차트 매니저]: "주가 하락... -${loss.toLocaleString()}원 손실."`);
    }
    processTurn();
}

function investCrypto() {
    if (Math.random() < 0.2) {
        let profit = Math.floor(money * 1.5);
        money += profit;
        alert(`🚨 [나대박 중개인]: "떡상으로 +${profit.toLocaleString()}원 초대박!"`);
    } else {
        let loss = Math.floor(money * 0.4);
        money -= loss;
        alert(`📉 [나대박 중개인]: "떡락해서 -${loss.toLocaleString()}원 손실..."`);
    }
    processTurn();
}

function buyBuilding(name, price, rent) {
    if (money < price) {
        alert("[최건물 중개사]: 잔액이 부족합니다!");
        return;
    }
    money -= price;
    ownedBuildings.push({ name, rent });
    alert(`🎉 [최건물 중개사]: "${name} 계약 성공!"`);
    updateUI();
}

function updateUI() {
    document.getElementById('moneyText').innerText = money.toLocaleString();
    document.getElementById('turnText').innerText = turn;
}

// ---------------- 픽셀 아트 렌더링 ----------------

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    if (currentScene === 'town') {
        drawBeachTown();
    } else {
        drawInterior();
    }
    
    // 플레이어: 오리 튜브 탄 도트 캐릭터
    drawTubeCharacter(player.x, player.y, player.name);
}

// 해변 마을 (모래사장 + 바다 파도 도트)
function drawBeachTown() {
    // 1. 모래사장 배경
    ctx.fillStyle = '#f6e58d';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // 모래 질감 픽셀 도트들
    ctx.fillStyle = '#f7d794';
    for (let i = 0; i < canvas.width; i += 16) {
        for (let j = 0; j < canvas.height; j += 16) {
            if ((i + j) % 32 === 0) ctx.fillRect(i, j, 4, 4);
        }
    }
    
    // 2. 바다 영역 (중앙 로드)
    ctx.fillStyle = '#74b9ff';
    ctx.fillRect(190, 0, 100, canvas.height);
    ctx.fillRect(0, 140, canvas.width, 80);
    
    // 파도 픽셀 디테일
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(195, 20, 12, 3);
    ctx.fillRect(260, 80, 15, 3);
    ctx.fillRect(210, 220, 10, 3);
    ctx.fillRect(40, 155, 20, 3);
    ctx.fillRect(320, 185, 18, 3);
    
    // 3. 픽셀 건물들 (파라솔 & 미니 리조트 디자인)
    buildings.forEach(b => {
        // 건물 지붕
        ctx.fillStyle = b.roofColor;
        ctx.fillRect(b.x, b.y, b.w, 20);
        
        // 지붕 도트 테두리
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(b.x, b.y + 18, b.w, 3);
        
        // 건물 벽체
        ctx.fillStyle = b.wallColor;
        ctx.fillRect(b.x + 5, b.y + 20, b.w - 10, b.h - 20);
        
        // 입구 문
        ctx.fillStyle = '#2d3436';
        ctx.fillRect(b.x + b.w/2 - 12, b.y + b.h - 22, 24, 22);
        
        // 이름표
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 11px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(b.name, b.x + b.w/2, b.y + 14);
    });
}

// 건물 내부 픽셀 타일
function drawInterior() {
    let npc = interiorNPCs[currentScene];
    let bObj = buildings.find(b => b.id === currentScene);
    
    // 바닥 목재/타일 느낌
    ctx.fillStyle = '#d2dae2';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // 격자 타일 라인
    ctx.strokeStyle = '#2c3e50';
    ctx.lineWidth = 1;
    for(let x=0; x<canvas.width; x+=20) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
    }
    for(let y=0; y<canvas.height; y+=20) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
    }
    
    // 벽면
    ctx.fillStyle = bObj.roofColor;
    ctx.fillRect(0, 0, canvas.width, 40);
    
    // 상담 카운터 Desk
    ctx.fillStyle = '#e67e22';
    ctx.fillRect(130, 100, 220, 24);
    ctx.fillStyle = '#d35400';
    ctx.fillRect(130, 120, 220, 8);
    
    // 하단 출구
    ctx.fillStyle = '#ff4757';
    ctx.fillRect(200, canvas.height - 16, 80, 16);
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 10px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText("EXIT 출구", 240, canvas.height - 4);
    
    // NPC 사람 캐릭터 (도트 스타일)
    drawHumanNPC(npc.x, npc.y, npc.name);
}

// 튜브 탄 오리/캐릭터 픽셀 그림
function drawTubeCharacter(x, y, name) {
    // 1. 노란색 오리 튜브
    ctx.fillStyle = '#f1c40f';
    ctx.fillRect(x - 4, y + 10, 36, 16); // 튜브 몸통
    
    // 오리 머리 (왼쪽)
    ctx.fillRect(x - 8, y + 2, 10, 12);
    // 오리 부리
    ctx.fillStyle = '#e67e22';
    ctx.fillRect(x - 12, y + 6, 6, 4);
    
    // 2. 캐릭터 몸통 & 얼굴 (튜브 안에 탄 상태)
    ctx.fillStyle = '#ff7979'; // 옷
    ctx.fillRect(x + 6, y + 4, 16, 10);
    
    ctx.fillStyle = '#ffdd59'; // 피부톤
    ctx.fillRect(x + 8, y - 6, 12, 12);
    
    // 눈 (픽셀)
    ctx.fillStyle = '#000000';
    ctx.fillRect(x + 11, y - 2, 2, 3);
    ctx.fillRect(x + 16, y - 2, 2, 3);
    
    // 이름표
    ctx.fillStyle = '#0c2461';
    ctx.font = 'bold 11px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(name, x + 14, y - 12);
}

// 건물 내부 사람 NPC 픽셀 그림
function drawHumanNPC(x, y, name) {
    // 머리
    ctx.fillStyle = '#2c3e50';
    ctx.fillRect(x, y, 28, 10);
    ctx.fillStyle = '#ffdd59';
    ctx.fillRect(x + 2, y + 8, 24, 12);
    
    // 눈
    ctx.fillStyle = '#000000';
    ctx.fillRect(x + 6, y + 12, 3, 3);
    ctx.fillRect(x + 19, y + 12, 3, 3);
    
    // 유니폼 몸통
    ctx.fillStyle = '#2980b9';
    ctx.fillRect(x - 2, y + 20, 32, 18);
    
    // 이름표
    ctx.fillStyle = '#2c3e50';
    ctx.font = 'bold 11px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(name, x + 14, y - 6);
}

draw();
checkProximity();
</script>
</body>
</html>
"""

components.html(game_html, height=660)

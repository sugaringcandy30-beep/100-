import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="픽셀 건물주 RPG", page_icon="🕹️", layout="centered")

st.title("🕹️ 픽셀 2D 타운 & 건물 입장 RPG")
st.caption("방향키(W, A, S, D)나 화면의 조이스틱 버튼으로 캐릭터를 직접 움직여 보세요!")

game_html = """
<!DOCTYPE html>
<html>
<head>
<style>
    body {
        margin: 0;
        padding: 0;
        background-color: #121212;
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
        box-shadow: 0 8px 16px rgba(0,0,0,0.6);
    }
    #uiBox {
        width: 480px;
        background-color: #2c3e50;
        padding: 12px;
        border-radius: 8px;
        margin-top: 10px;
        box-sizing: border-box;
    }
    .status-bar {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
        font-weight: bold;
        color: #f1c40f;
    }
    .action-btn {
        background-color: #e67e22;
        color: white;
        border: none;
        padding: 8px 12px;
        margin: 4px;
        border-radius: 4px;
        cursor: pointer;
        font-weight: bold;
    }
    .action-btn:hover {
        background-color: #f39c12;
    }
    .enter-btn {
        background-color: #27ae60;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        cursor: pointer;
        font-weight: bold;
        font-size: 14px;
    }
    .exit-btn {
        background-color: #c0392b;
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
        background: #34495e;
        color: white;
        border: 2px solid #f39c12;
        border-radius: 8px;
        cursor: pointer;
    }
    .ctrl-btn:active {
        background: #f39c12;
    }
    #dialogue {
        min-height: 48px;
        background: #1a252f;
        padding: 10px;
        border-radius: 4px;
        border: 1px solid #34495e;
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
        <span>📍 위치: <span id="locationText">야외 마을</span></span>
        <span>📅 턴: <span id="turnText">1</span>/12</span>
        <span>💰 현금: <span id="moneyText">1,000,000</span>원</span>
    </div>
    <div id="dialogue">💬 방향키로 이동해서 건물 입구로 가보세요!</div>
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

// 게임 데이터
let money = 1000000;
let turn = 1;
let currentScene = 'town'; // 'town' (야외) 또는 건물 ID ('bank', 'stock', 'crypto', 'realty')
let ownedBuildings = [];

// 플레이어
const player = {
    x: 225,
    y: 170,
    size: 24,
    color: '#00fff5',
    speed: 12,
    name: '김개미'
};

// 건물 데이터 (야외 마을 상의 좌표)
const buildings = [
    { id: 'bank', name: '🏦 안전 은행', x: 40, y: 30, w: 100, h: 70, color: '#2ecc71', npcName: '은행원 김수호' },
    { id: 'stock', name: '📈 미래 증권', x: 340, y: 30, w: 100, h: 70, color: '#3498db', npcName: '펀드매니저 박차트' },
    { id: 'crypto', name: '🚀 코인 거래소', x: 40, y: 240, w: 100, h: 70, color: '#e74c3c', npcName: '코인 중개인 나대박' },
    { id: 'realty', name: '🏢 강남 부동산', x: 340, y: 240, w: 100, h: 70, color: '#f1c40f', npcName: '부동산 중개사 최건물' }
];

// 내부 NPC 데이터
const interiorNPCs = {
    bank: { x: 225, y: 60, size: 28, color: '#27ae60', name: '🏦 은행원 김수호' },
    stock: { x: 225, y: 60, size: 28, color: '#2980b9', name: '📈 펀드매니저 박차트' },
    crypto: { x: 225, y: 60, size: 28, color: '#c0392b', name: '🚀 중개인 나대박' },
    realty: { x: 225, y: 60, size: 28, color: '#f39c12', name: '🏢 중개사 최건물' }
};

let nearTarget = null; // 입구 또는 NPC 근접 여부

// 키보드 조작
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

// 근접 여부 체크 (야외 입구 or 건물 내부 NPC)
function checkProximity() {
    nearTarget = null;
    const actionArea = document.getElementById('actionArea');
    const dialogue = document.getElementById('dialogue');
    
    if (currentScene === 'town') {
        // 마을 야외: 건물 입구 근접 체크
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
            dialogue.innerHTML = `📍 <b>[${nearTarget.name}]</b> 문 앞에 도착했습니다.`;
            actionArea.innerHTML = `<button class="enter-btn" onclick="enterBuilding('${nearTarget.id}')">🚪 건물 입장하기</button>`;
        } else {
            dialogue.innerHTML = "💬 마을을 거닐며 원하는 건물 입구로 이동해보세요!";
            actionArea.innerHTML = "";
        }
    } else {
        // 건물 내부: 직원(NPC) 및 출구 체크
        let npc = interiorNPCs[currentScene];
        let dist = Math.hypot((npc.x + npc.size/2) - (player.x + player.size/2), (npc.y + npc.size/2) - (player.y + player.size/2));
        
        // 출구 근처 체크 (하단 출구)
        if (player.y > canvas.height - 50) {
            dialogue.innerHTML = "🚪 밖으로 나가는 출구입니다.";
            actionArea.innerHTML = `<button class="exit-btn" onclick="exitBuilding()">🚪 밖으로 나가기</button>`;
        } else if (dist < 55) {
            dialogue.innerHTML = `💬 <b>${npc.name}</b>: "어서오세요, 어떤 상담이나 거래를 도와드릴까요?"`;
            renderDialogueOptions(currentScene);
        } else {
            dialogue.innerHTML = `🏢 [${buildings.find(b=>b.id===currentScene).name} 내부] 위쪽 창구에 있는 직원에게 다가가 보세요.`;
            actionArea.innerHTML = `<button class="exit-btn" onclick="exitBuilding()">🚪 밖으로 나가기</button>`;
        }
    }
}

// 건물 입장 및 퇴장
function enterBuilding(buildingId) {
    currentScene = buildingId;
    player.x = 225;
    player.y = 280; // 건물 하단 입구로 이동
    
    const bObj = buildings.find(b => b.id === buildingId);
    document.getElementById('locationText').innerText = bObj.name;
    checkProximity();
    draw();
}

function exitBuilding() {
    let bObj = buildings.find(b => b.id === currentScene);
    currentScene = 'town';
    // 해당 건물 문 앞 위치로 스폰
    player.x = bObj.x + bObj.w/2 - player.size/2;
    player.y = bObj.y + bObj.h + 10;
    
    document.getElementById('locationText').innerText = '야외 마을';
    checkProximity();
    draw();
}

// 직원과의 대화 옵션 (거래 실행)
function renderDialogueOptions(type) {
    const actionArea = document.getElementById('actionArea');
    
    if (type === 'bank') {
        actionArea.innerHTML = `
            <button class="action-btn" onclick="investBank()">🏦 예금 가입하기 (확정 이자 +5%)</button>
            <button class="exit-btn" onclick="exitBuilding()">🚪 대화 끝내고 나가기</button>
        `;
    } else if (type === 'stock') {
        actionArea.innerHTML = `
            <button class="action-btn" onclick="investStock()">📈 주식 매수 (50% 확률 +30% / -20%)</button>
            <button class="exit-btn" onclick="exitBuilding()">🚪 대화 끝내고 나가기</button>
        `;
    } else if (type === 'crypto') {
        actionArea.innerHTML = `
            <button class="action-btn" onclick="investCrypto()">🚀 코인 올인 (20% 확률 +150% / -40%)</button>
            <button class="exit-btn" onclick="exitBuilding()">🚪 대화 끝내고 나가기</button>
        `;
    } else if (type === 'realty') {
        actionArea.innerHTML = `
            <button class="action-btn" onclick="buyBuilding('반지하 고시원', 10000000, 500000)">🏚️ 고시원 (1천만)</button>
            <button class="action-btn" onclick="buyBuilding('원룸 빌라', 30000000, 1500000)">🏠 빌라 (3천만)</button>
            <button class="action-btn" onclick="buyBuilding('강남 타워', 100000000, 10000000)">🏙️ 강남타워 (1억 - 승리)</button>
            <button class="exit-btn" onclick="exitBuilding()">🚪 대화 끝내고 나가기</button>
        `;
    }
}

// 턴 진행 및 월세 입금
function processTurn() {
    let rentSum = 0;
    ownedBuildings.forEach(b => rentSum += b.rent);
    money += rentSum;
    turn += 1;
    updateUI();
    
    if (money >= 100000000) {
        alert("🎉 축하합니다! 1억 원을 모아 건물주가 되었습니다!");
    } else if (turn > 12) {
        alert("⏱️ 12턴이 지났습니다! 최종 보유 자산: " + money.toLocaleString() + "원");
    } else if (money <= 0) {
        alert("💥 파산했습니다! 게임 오버!");
    }
}

// 거래 함수들
function investBank() {
    let profit = Math.floor(money * 0.05);
    money += profit;
    alert(`🏦 [김수호 직원]: "감사합니다! 적금 이자로 +${profit.toLocaleString()}원이 입금되었습니다."`);
    processTurn();
}

function investStock() {
    if (Math.random() < 0.5) {
        let profit = Math.floor(money * 0.3);
        money += profit;
        alert(`📈 [박차트 매니저]: "축하합니다! 주식이 대폭등해서 +${profit.toLocaleString()}원 수익이 났습니다!"`);
    } else {
        let loss = Math.floor(money * 0.2);
        money -= loss;
        alert(`📉 [박차트 매니저]: "아쉬워요... 주가가 하락해서 -${loss.toLocaleString()}원 손실이 생겼습니다."`);
    }
    processTurn();
}

function investCrypto() {
    if (Math.random() < 0.2) {
        let profit = Math.floor(money * 1.5);
        money += profit;
        alert(`🚨 [나대박 중개인]: "대박 사건!! 코인 떡상으로 +${profit.toLocaleString()}원 초대박!"`);
    } else {
        let loss = Math.floor(money * 0.4);
        money -= loss;
        alert(`📉 [나대박 중개인]: "이런... 떡락장에 물려서 -${loss.toLocaleString()}원 손실이 났네요..."`);
    }
    processTurn();
}

function buyBuilding(name, price, rent) {
    if (money < price) {
        alert("[최건물 중개사]: 잔액이 부족해서 이 매물은 사실 수 없습니다!");
        return;
    }
    money -= price;
    ownedBuildings.push({ name, rent });
    alert(`🎉 [최건물 중개사]: "${name} 계약 성공! 이제 턴마다 월세 +${rent.toLocaleString()}원이 자동으로 들어옵니다."`);
    updateUI();
}

function updateUI() {
    document.getElementById('moneyText').innerText = money.toLocaleString();
    document.getElementById('turnText').innerText = turn;
}

// 캔버스 그리기 함수 (타운 vs 건물 내부)
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    if (currentScene === 'town') {
        drawTown();
    } else {
        drawInterior();
    }
    
    // 플레이어 캐릭터 그리기
    drawPixelChar(player.x, player.y, player.color, player.name);
}

// 마을 야외 맵 렌더링
function drawTown() {
    // 잔디/길 타일
    ctx.fillStyle = '#1e272e';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // 중앙 도로 표현
    ctx.fillStyle = '#34495e';
    ctx.fillRect(190, 0, 100, canvas.height);
    ctx.fillRect(0, 140, canvas.width, 80);
    
    // 건물들
    buildings.forEach(b => {
        ctx.fillStyle = b.color;
        ctx.fillRect(b.x, b.y, b.w, b.h);
        
        // 지붕 및 문
        ctx.fillStyle = 'rgba(0,0,0,0.25)';
        ctx.fillRect(b.x, b.y, b.w, 15);
        ctx.fillStyle = '#2c3e50';
        ctx.fillRect(b.x + b.w/2 - 10, b.y + b.h - 20, 20, 20); // 문
        
        // 외곽선
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.strokeRect(b.x, b.y, b.w, b.h);
        
        // 건물 이름
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 11px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(b.name, b.x + b.w/2, b.y + 35);
    });
}

// 건물 내부 맵 렌더링
function drawInterior() {
    let npc = interiorNPCs[currentScene];
    let bObj = buildings.find(b => b.id === currentScene);
    
    // 바닥 타일
    ctx.fillStyle = '#34495e';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // 내부 벽면
    ctx.fillStyle = bObj.color;
    ctx.fillRect(0, 0, canvas.width, 40);
    
    // 카운터(안내 창구 책상)
    ctx.fillStyle = '#7f8c8d';
    ctx.fillRect(140, 95, 200, 25);
    ctx.strokeStyle = '#ecf0f1';
    ctx.strokeRect(140, 95, 200, 25);
    
    // 하단 출구 표시
    ctx.fillStyle = '#e74c3c';
    ctx.fillRect(200, canvas.height - 15, 80, 15);
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 10px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText("EXIT 출구", 240, canvas.height - 4);
    
    // NPC 직원 캐릭터 그리기
    drawPixelChar(npc.x, npc.y, npc.color, npc.name);
}

// 픽셀 스타일 캐릭터 그리기 공통 함수
function drawPixelChar(x, y, color, name) {
    // 몸통
    ctx.fillStyle = color;
    ctx.fillRect(x, y, 24, 24);
    
    // 눈/얼굴 픽셀
    ctx.fillStyle = '#000000';
    ctx.fillRect(x + 4, y + 6, 4, 4);
    ctx.fillRect(x + 16, y + 6, 4, 4);
    
    // 캐릭터 이름표
    ctx.fillStyle = '#f1c40f';
    ctx.font = '10px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(name, x + 12, y - 6);
}

// 초기화 실행
draw();
checkProximity();
</script>
</body>
</html>
"""

components.html(game_html, height=660)

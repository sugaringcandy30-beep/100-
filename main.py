import random
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="김개미의 건물주 도전기", page_icon="🏢", layout="centered")

# 건물의 목록 및 가격/임대수익 정의
BUILDINGS = [
    {"name": "🏚️ 반지하 고시원", "price": 10000000, "rent": 500000},
    {"name": "🏠 원룸 빌라", "price": 30000000, "rent": 1500000},
    {"name": "🏪 편의점 입점 상가", "price": 50000000, "rent": 3000000},
    {"name": "🏬 홍대 꼬마빌딩", "price": 80000000, "rent": 5500000},
    {"name": "🏙️ 강남 랜드마크 타워", "price": 100000000, "rent": 10000000},
]

# 세션 상태 초기화
if "money" not in st.session_state:
    st.session_state.money = 1000000  # 초기 자금 100만 원
if "turn" not in st.session_state:
    st.session_state.turn = 1
if "history" not in st.session_state:
    st.session_state.history = []
if "status" not in st.session_state:
    st.session_state.status = "normal"
if "dialogue" not in st.session_state:
    st.session_state.dialogue = "안녕! 난 흙수저 김개미야. 12턴 안에 1억을 모아서 진짜 건물주가 되는 게 꿈이지!"
if "owned_buildings" not in st.session_state:
    st.session_state.owned_buildings = []  # 소유한 건물 리스트

# 캐릭터 이미지 URL
CHAR_IMAGES = {
    "normal": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&auto=format&fit=crop&q=80",
    "happy": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=400&auto=format&fit=crop&q=80",
    "sad": "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=400&auto=format&fit=crop&q=80",
    "panic": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&auto=format&fit=crop&q=80",
    "win": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&auto=format&fit=crop&q=80"
}

def reset_game():
    st.session_state.money = 1000000
    st.session_state.turn = 1
    st.session_state.status = "normal"
    st.session_state.dialogue = "좋아, 다시 처음부터 도전이다! 이번엔 강남 타워까지 삼킨다!"
    st.session_state.history = []
    st.session_state.owned_buildings = []

# 타이틀 및 진행도
st.title("🏢 김개미의 건물주 도전기 TRPG")
st.progress(min(st.session_state.turn / 12, 1.0), text=f"남은 기회: {13 - st.session_state.turn}턴 / 12턴")

st.divider()

# --- 캐릭터 & 상태 대화창 ---
col_img, col_talk = st.columns([1, 2])

with col_img:
    img_url = CHAR_IMAGES.get(st.session_state.status, CHAR_IMAGES["normal"])
    st.image(img_url, caption="주인공 : 김개미", use_container_width=True)

with col_talk:
    st.subheader("💬 김개미의 한마디")
    st.info(f'"{st.session_state.dialogue}"')
    
    # 총 임대 수입 계산
    total_rent = sum([b["rent"] for b in st.session_state.owned_buildings])
    
    m1, m2 = st.columns(2)
    m1.metric("📅 현재 턴", f"{st.session_state.turn} / 12 턴")
    m2.metric("💰 보유 현금", f"{st.session_state.money:,} 원")
    if total_rent > 0:
        st.caption(f"💵 턴마다 들어오는 월세 수입: **+{total_rent:,} 원**")

st.divider()

# --- 엔딩 조건 판정 ---
if st.session_state.money <= 0 and len(st.session_state.owned_buildings) == 0:
    st.error("💥 [GAME OVER] 자산을 모두 잃고 파산했습니다...")
    st.session_state.status = "panic"
    if st.button("🔄 다시 도전하기"):
        reset_game()
        st.rerun()

elif st.session_state.money >= 100000000 or any(b["name"] == "🏙️ 강남 랜드마크 타워" for b in st.session_state.owned_buildings):
    st.balloons()
    st.success("🎉 [CLEAR] 강남 건물주 달성 성공! 김개미는 드디어 전설이 되었습니다!")
    st.session_state.status = "win"
    if st.button("🏆 다시 시작하기"):
        reset_game()
        st.rerun()

elif st.session_state.turn > 12:
    st.error("⏱️ [TIME OVER] 12턴이 지났습니다!")
    if st.button("🔄 다시 도전하기"):
        reset_game()
        st.rerun()

else:
    # 탭 메뉴 (투자하기 vs 부동산 매수)
    tab1, tab2 = st.tabs(["🎯 투자의 시간", "🏘️ 부동산 매수"])

    # --- TAB 1: 금융 투자 ---
    with tab1:
        st.write("이번 턴에 어디에 투자하시겠습니까? (선택 시 턴이 진행되며, 보유 건물의 월세도 입금됩니다)")
        c1, c2, c3 = st.columns(3)
        
        # 월세 입금 로직 공통 함수
        def process_turn_and_rent():
            total_rent = sum([b["rent"] for b in st.session_state.owned_buildings])
            st.session_state.money += total_rent
            st.session_state.turn += 1
            return total_rent

        with c1:
            st.markdown("### 🏦 안전 적금")
            st.caption("확정 이자 +5%")
            if st.button("적금 가입"):
                rent = process_turn_and_rent()
                profit = int(st.session_state.money * 0.05)
                st.session_state.money += profit
                st.session_state.status = "happy"
                st.session_state.dialogue = f"안전하게 이자 {profit:,}원 모았어! (월세 +{rent:,}원 보너스)"
                st.session_state.history.append(f"{st.session_state.turn-1}턴: 적금 +{profit:,}원 (월세 +{rent:,}원)")
                st.rerun()

        with c2:
            st.markdown("### 📈 주식 투자")
            st.caption("50% 확률로 +30% OR -20%")
            if st.button("주식 매수"):
                rent = process_turn_and_rent()
                if random.random() < 0.5:
                    profit = int(st.session_state.money * 0.3)
                    st.session_state.money += profit
                    st.session_state.status = "happy"
                    st.session_state.dialogue = f"주식 떡상!! +{profit:,}원 이득 봤다! (월세 +{rent:,}원)"
                    st.session_state.history.append(f"{st.session_state.turn-1}턴: 주식 성공 +{profit:,}원")
                else:
                    loss = int(st.session_state.money * 0.2)
                    st.session_state.money -= loss
                    st.session_state.status = "sad"
                    st.session_state.dialogue = f"주식 떡락... -{loss:,}원 손실이다... 흑흑"
                    st.session_state.history.append(f"{st.session_state.turn-1}턴: 주식 실패 -{loss:,}원")
                st.rerun()

        with c3:
            st.markdown("### 🚀 코인 올인")
            st.caption("20% 확률로 +150% OR 80% 확률로 -40%")
            if st.button("코인 올인"):
                rent = process_turn_and_rent()
                if random.random() < 0.2:
                    profit = int(st.session_state.money * 1.5)
                    st.session_state.money += profit
                    st.session_state.status = "happy"
                    st.session_state.dialogue = f"🚨 화성 가즈아!! 코인 폭등으로 +{profit:,}원 획득!"
                    st.session_state.history.append(f"{st.session_state.turn-1}턴: 코인 초대박 +{profit:,}원")
                else:
                    loss = int(st.session_state.money * 0.4)
                    st.session_state.money -= loss
                    st.session_state.status = "panic"
                    st.session_state.dialogue = f"망했다... 코인 -{loss:,}원 떡락..."
                    st.session_state.history.append(f"{st.session_state.turn-1}턴: 코인 떡락 -{loss:,}원")
                st.rerun()

    # --- TAB 2: 부동산 매수 상점 ---
    with tab2:
        st.subheader("🛒 매매 가능한 매물 리스트")
        st.caption("건물을 매수하면 **매 턴마다 월세 수익**이 자동으로 들어옵니다!")
        
        for b in BUILDINGS:
            col_b1, col_b2, col_b3 = st.columns([2, 2, 1])
            with col_b1:
                st.write(f"**{b['name']}**")
            with col_b2:
                st.write(f"매매가: **{b['price']:,}원** (월세: +{b['rent']:,}원)")
            with col_b3:
                # 현금이 부족하면 버튼 비활성화
                if st.session_state.money < b['price']:
                    st.button("잔액 부족", key=b['name'], disabled=True)
                else:
                    if st.button("매수하기", key=b['name']):
                        st.session_state.money -= b['price']
                        st.session_state.owned_buildings.append(b)
                        st.session_state.status = "happy"
                        st.session_state.dialogue = f"축하해! {b['name']} 매수 완료! 이제 턴마다 월세가 들어와!"
                        st.session_state.history.append(f"{st.session_state.turn}턴: {b['name']} 매수 성공")
                        st.rerun()

st.divider()

# 소유 건물 현황 표시
if st.session_state.owned_buildings:
    st.subheader("🏢 김개미가 소유한 부동산")
    for ob in st.session_state.owned_buildings:
        st.success(f"• **{ob['name']}** (매 턴 월세 +{ob['rent']:,}원)")

# 지난 기록
with st.expander("📜 지난 투자 및 매수 기록 보기"):
    for log in reversed(st.session_state.history):
        st.write(log)

import random
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="자산 튀기기 시뮬레이터", page_icon="💰")

# 게임 초기화 (세션 상태 저장)
if "money" not in st.session_state:
    st.session_state.money = 1000000  # 초기 자금 100만 원
if "turn" not in st.session_state:
    st.session_state.turn = 1
if "history" not in st.session_state:
    st.session_state.history = []

# 타이틀
st.title("💰 100만 원으로 건물주 되기")
st.write("투자 선택을 통해 자산을 늘려보세요! 파산하지 않고 얼만큼 모을 수 있을까요?")

st.divider()

# 현재 상태 표시
col1, col2 = st.columns(2)
with col1:
    st.metric(label="📅 현재 턴", value=f"{st.session_state.turn} 턴")
with col2:
    st.metric(
        label="💵 보유 자산", value=f"{st.session_state.money:,} 원"
    )

st.divider()

# 승리/패배 조건 체크
if st.session_state.money <= 0:
    st.error("💥 자산을 모두 잃고 파산했습니다! 게임 오버.")
    if st.button("🎮 다시 시작하기"):
        st.session_state.money = 1000000
        st.session_state.turn = 1
        st.session_state.history = []
        st.rerun()
elif st.session_state.money >= 100000000:
    st.balloons()
    st.success("🎉 축하합니다! 1억 원을 달성하여 건물주가 되었습니다!")
    if st.button("🎮 다시 시작하기"):
        st.session_state.money = 1000000
        st.session_state.turn = 1
        st.session_state.history = []
        st.rerun()
else:
    st.subheader("🎯 투자를 선택하세요")

    col_a, col_b, col_c = st.columns(3)

    # 1. 안정적인 은행 예금
    with col_a:
        st.write("**🏦 은행 예금**")
        st.caption("확정 수익 +5%")
        if st.button("예금에 넣기"):
            profit = int(st.session_state.money * 0.05)
            st.session_state.money += profit
            st.session_state.turn += 1
            st.session_state.history.append(
                f"{st.session_state.turn-1}턴: 예금으로 +{profit:,}원 이자 획득"
            )
            st.rerun()

    # 2. 주식 투자 (하이 리스크 하이 리턴)
    with col_b:
        st.write("**📈 우량주 주식**")
        st.caption("50% 확률로 +30% OR -20%")
        if st.button("주식 매수"):
            if random.random() < 0.5:
                profit = int(st.session_state.money * 0.3)
                st.session_state.money += profit
                st.session_state.history.append(
                    f"{st.session_state.turn}턴: 주식 대박! +{profit:,}원 상승"
                )
            else:
                loss = int(st.session_state.money * 0.2)
                st.session_state.money -= loss
                st.session_state.history.append(
                    f"{st.session_state.turn}턴: 주식 떡락... -{loss:,}원 손실"
                )
            st.session_state.turn += 1
            st.rerun()

    # 3. 코인 올인 (초고위험)
    with col_c:
        st.write("**🚀 코인 대박**")
        st.caption("20% 확률로 +200% OR 80% 확률로 -50%")
        if st.button("코인 올인"):
            if random.random() < 0.2:
                profit = int(st.session_state.money * 2.0)
                st.session_state.money += profit
                st.session_state.history.append(
                    f"{st.session_state.turn}턴: 🚀 코인 떡상! +{profit:,}원 초대박"
                )
            else:
                loss = int(st.session_state.money * 0.5)
                st.session_state.money -= loss
                st.session_state.history.append(
                    f"{st.session_state.turn}턴: 📉 코인 구조대 실패... -{loss:,}원 손실"
                )
            st.session_state.turn += 1
            st.rerun()

st.divider()

# 투자 기록 보기
st.subheader("📜 지난 투자 기록")
for log in reversed(st.session_state.history[-5:]):
    st.text(log)

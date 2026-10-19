import streamlit as st

# Cấu hình trang Streamlit
st.set_page_config(page_title="Game Nối Từ Tiếng Việt", page_icon="🔗", layout="centered")

st.title("🔗 NỐI TỪ TIẾNG VIỆT")
st.write("Thử thách vốn từ vựng của bạn! Từ tiếp theo phải bắt đầu bằng **tiếng cuối** của từ trước đó.")

# Khởi tạo trạng thái game (Session State)
if "history" not in st.session_state:
    st.session_state.history = ["học tập"]  # Từ khởi đầu mặc định
if "score" not in st.session_state:
    st.session_state.score = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# Từ điển các từ mẫu gợi ý cho máy hoặc kiểm tra tính hợp lệ cơ bản
VALID_WORDS = {
    "học tập", "tập thể", "thể thao", "thao trường", "trường học", 
    "học sinh", "sinh viên", "viên bi", "bi a", "an toàn", "toàn bộ", 
    "bộ đội", "đội bóng", "bóng đá", "đá cầu", "cầu lông", "lông vũ",
    "vũ trụ", "trụ cột", "cột đèn", "đèn pin", "pin sạc", "sạc điện",
    "nước non", "non sông", "sông ngòi", "ngòi bút", "bút chì", "chìa khóa"
}

def reset_game():
    st.session_state.history = ["học tập"]
    st.session_state.score = 0
    st.session_state.game_over = False

# Hiển thị bảng điểm và từ hiện tại
current_word = st.session_state.history[-1]
last_syllable = current_word.split()[-1]

col1, col2 = st.columns(2)
with col1:
    st.metric(label="🏆 Điểm số", value=st.session_state.score)
with col2:
    st.metric(label="🎯 Từ hiện tại", value=current_word)

st.info(f"👉 **Luật chơi:** Nhập một từ bắt đầu bằng tiếng: **'{last_syllable.upper()}'**")

# Form nhập từ người chơi
with st.form(key="word_form", clear_on_submit=True):
    user_input = st.text_input("Nhập từ của bạn:", placeholder=f"Ví dụ: {last_syllable} ...")
    submit_button = st.form_submit_button(label="Nối từ")

if submit_button and user_input:
    clean_input = user_input.strip().lower()
    words = clean_input.split()
    
    # Kiểm tra tính hợp lệ
    if len(words) < 2:
        st.error("⚠️ Vui lòng nhập một từ có ít nhất 2 tiếng (ví dụ: 'học tập').")
    elif words[0] != last_syllable:
        st.error(f"❌ Từ phải bắt đầu bằng tiếng **'{last_syllable}'**!")
    elif clean_input in st.session_state.history:
        st.warning("⚠️ Từ này đã được sử dụng rồi, hãy tìm từ khác nhé!")
    else:
        # Thêm từ hợp lệ vào lịch sử
        st.session_state.history.append(clean_input)
        st.session_state.score += 10
        st.success(f"✅ Nối thành công: **{clean_input}** (+10 điểm)")
        
        # Máy tự động nối tiếp từ tiếp theo để tăng độ hấp dẫn
        next_possible = [w for w in VALID_WORDS if w.startswith(clean_input.split()[-1]) and w not in st.session_state.history]
        if next_possible:
            import random
            bot_word = random.choice(next_possible)
            st.session_state.history.append(bot_word)
            st.info(1 * f"🤖 Máy nối tiếp: **{bot_word}**")
        
        st.rerun()

# Nút chơi lại
if st.button("🔄 Chơi Lại Từ Đầu"):
    reset_game()
    st.rerun()

st.divider()

# Hiển thị lịch sử các từ đã nối
st.subheader("📜 Lịch sử các từ đã nối:")
for i, word in enumerate(reversed(st.session_state.history)):
    st.text(f"{len(st.session_state.history) - i}. {word.upper()}")

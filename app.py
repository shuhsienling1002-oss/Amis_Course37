import streamlit as st
import time
import random
from io import BytesIO

# --- 1. 核心相容性修復 ---
def safe_rerun():
    """自動判斷並執行重整"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except:
            st.stop()

def safe_play_audio(text):
    """語音播放安全模式"""
    try:
        from gtts import gTTS
        # 使用印尼語 (id) 發音
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception as e:
        st.caption(f"🔇 (語音生成暫時無法使用)")

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 37: O Tu'tu'", page_icon="🚗", layout="centered")

# --- CSS 美化 (工業金屬灰與亮黃) ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    .morph-tag { 
        background-color: #CFD8DC; color: #37474F; 
        padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;
        display: inline-block; margin-right: 5px;
    }
    
    /* 單字卡 */
    .word-card {
        background: linear-gradient(135deg, #ECEFF1 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #607D8B;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #455A64; }
    .chinese-text { font-size: 16px; color: #7f8c8d; }
    
    /* 句子框 */
    .sentence-box {
        background-color: #ECEFF1;
        border-left: 5px solid #90A4AE;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #CFD8DC; color: #37474F; border: 2px solid #607D8B; padding: 12px;
    }
    .stButton>button:hover { background-color: #B0BEC5; border-color: #455A64; }
    .stProgress > div > div > div > div { background-color: #607D8B; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Unit 37: 18個單字 - User Fix) ---
vocab_data = [
    {"amis": "Tosiya", "chi": "車子", "icon": "🚗", "source": "Row 999", "morph": "Noun"},
    {"amis": "Miparakat", "chi": "駕駛 / 開車", "icon": "🚦", "source": "User Fix", "morph": "Mi-Pa-Rakat"}, # 修正
    {"amis": "Fakeloh", "chi": "石頭", "icon": "🪨", "source": "Row 221", "morph": "Noun"},
    {"amis": "'Alo", "chi": "河流", "icon": "🌊", "source": "User Fix", "morph": "Noun"}, # 修正
    {"amis": "Sasing", "chi": "相片", "icon": "🖼️", "source": "Row 1029", "morph": "Noun"},
    {"amis": "Misasing", "chi": "拍照", "icon": "📸", "source": "Row 1029", "morph": "Mi-Sasing"},
    {"amis": "Tikami", "chi": "信 / 信件", "icon": "✉️", "source": "Row 322", "morph": "Noun"},
    {"amis": "Mipateli", "chi": "放置", "icon": "📥", "source": "User Fix", "morph": "Mi-Pa-Teli"}, # 修正
    {"amis": "Teli", "chi": "放置 (詞根)", "icon": "📍", "source": "Root", "morph": "Root"},
    {"amis": "Papotal", "chi": "外面", "icon": "🌳", "source": "Row 421", "morph": "Pa-Potal"},
    {"amis": "Salidong", "chi": "雨傘 / 遮蔽具", "icon": "☂️", "source": "Row 3484", "morph": "Sa-Lidong"},
    {"amis": "Lidong", "chi": "影子 / 陰涼處", "icon": "🌥️", "source": "Row 3484", "morph": "Root"},
    {"amis": "Foting", "chi": "魚", "icon": "🐟", "source": "Row 223", "morph": "Noun"},
    {"amis": "Nanom", "chi": "水", "icon": "💧", "source": "Row 999", "morph": "Noun"},
    {"amis": "Lalan", "chi": "路 / 道路", "icon": "🛣️", "source": "Row 1243", "morph": "Noun"},
    {"amis": "Koko'", "chi": "雞", "icon": "🐔", "source": "Common", "morph": "Noun"},
    {"amis": "Waco", "chi": "狗", "icon": "🐕", "source": "User Fix", "morph": "Noun"}, # 修正
    {"amis": "Posi", "chi": "貓", "icon": "🐈", "source": "User Fix", "morph": "Noun"}, # 修正
]

# --- 句子庫 (9句: 嚴格源自 CSV 並移除連字號) ---
sentences = [
    {"amis": "Telien no miparakatay to tosiya ko sapafangsis a nanom i tosiya.", "chi": "香水要被司機放在車上。", "icon": "🚗", "source": "Row 999 (User Fix)"},
    {"amis": "Mimingay a kohecalay koni a fakeloh.", "chi": "這塊石頭又小又白。", "icon": "🪨", "source": "Row 221"},
    {"amis": "Hali'ayam ko misasingay a tamdaw.", "chi": "攝影者愛鳥。", "icon": "📸", "source": "Row 1029"},
    {"amis": "O sapilidong to 'orad ato fali.", "chi": "用來避雨和避風的(東西)。", "icon": "☂️", "source": "Row 3484"},
    {"amis": "T-om-ireng ci Nakaw i papotal.", "chi": "Nakaw在外面站著。", "icon": "🌳", "source": "Row 421 (User Fix)"},
    {"amis": "Talariyar a mifoting ci mama.", "chi": "爸爸去海邊捕魚。", "icon": "🐟", "source": "Row 223"},
    {"amis": "Ira ko lalan a tayra i 'alo.", "chi": "有路去河邊。", "icon": "🛣️", "source": "User Fix"},
    {"amis": "Mipakaen to koko' ato waco.", "chi": "餵雞和狗。", "icon": "🐔", "source": "User Fix"},
    {"amis": "Micakay to tikami.", "chi": "買信(紙)。", "icon": "✉️", "source": "Adapted from Row 322"},
]

# --- 3. 隨機題庫 (5題) ---
raw_quiz_pool = [
    {
        "q": "Telien no miparakatay to tosiya ko...",
        "audio": "Telien no miparakatay to tosiya ko",
        "options": ["香水放在車上", "石頭放在車上", "雞放在車上"],
        "ans": "香水放在車上",
        "hint": "Miparakatay (司機), Nanom (水/香水) (User Fix)"
    },
    {
        "q": "Ira ko lalan a tayra i...",
        "audio": "Ira ko lalan a tayra i",
        "options": ["'Alo (河邊)", "Tosiya (車上)", "Fakeloh (石頭)"],
        "ans": "'Alo (河邊)",
        "hint": "User Fix: 'Alo"
    },
    {
        "q": "單字測驗：Miparakat",
        "audio": "Miparakat",
        "options": ["駕駛/開車", "走路", "跑步"],
        "ans": "駕駛/開車",
        "hint": "User Fix: Miparakat"
    },
    {
        "q": "單字測驗：Waco",
        "audio": "Waco",
        "options": ["狗", "貓", "雞"],
        "ans": "狗",
        "hint": "User Fix: Waco"
    },
    {
        "q": "O sapilidong to 'orad ato fali.",
        "audio": "O sapilidong to 'orad ato fali",
        "options": ["用來避雨和避風", "用來吃飯", "用來睡覺"],
        "ans": "用來避雨和避風",
        "hint": "Sapilidong (遮蔽物) (Row 3484)"
    }
]

# --- 4. 狀態初始化 (洗牌邏輯) ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    st.session_state.quiz_id = str(random.randint(1000, 9999))
    
    # 抽題與洗牌 (5題)
    selected_questions = random.sample(raw_quiz_pool, 5)
    final_questions = []
    for q in selected_questions:
        q_copy = q.copy()
        shuffled_opts = random.sample(q['options'], len(q['options']))
        q_copy['shuffled_options'] = shuffled_opts
        final_questions.append(q_copy)
        
    st.session_state.quiz_questions = final_questions
    st.session_state.init = True

# --- 5. 主介面 ---
st.markdown("<h1 style='text-align: center; color: #455A64;'>Unit 37: O Lalosidan</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>物品與工具 (User Corrected)</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 詞彙與句型", "🎲 隨機挑戰"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字 (構詞分析)")
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
                <div class="morph-tag">{word['morph']}</div>
                <div class="source-tag">src: {word['source']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊 聽發音", key=f"btn_vocab_{i}"):
                safe_play_audio(word['amis'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型 (Data-Driven)")
    for i, s in enumerate(sentences):
        st.markdown(f"""
        <div class="sentence-box">
            <div style="font-size: 20px; font-weight: bold; color: #455A64;">{s['icon']} {s['amis']}</div>
            <div style="font-size: 16px; color: #555; margin-top: 5px;">{s['chi']}</div>
            <div class="source-tag">src: {s['source']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 播放句型", key=f"btn_sent_{i}"):
            safe_play_audio(s['amis'])

# === Tab 2: 隨機挑戰模式 ===
with tab2:
    st.markdown("### 🎲 隨機評量")
    
    if st.session_state.current_q_idx < len(st.session_state.quiz_questions):
        q_data = st.session_state.quiz_questions[st.session_state.current_q_idx]
        
        st.progress((st.session_state.current_q_idx) / 5)
        st.markdown(f"**Question {st.session_state.current_q_idx + 1} / 5**")
        
        st.markdown(f"### {q_data['q']}")
        if q_data['audio']:
            if st.button("🎧 播放題目音檔", key=f"btn_audio_{st.session_state.current_q_idx}"):
                safe_play_audio(q_data['audio'])
        
        # 使用洗牌後的選項
        unique_key = f"q_{st.session_state.quiz_id}_{st.session_state.current_q_idx}"
        user_choice = st.radio("請選擇正確答案：", q_data['shuffled_options'], key=unique_key)
        
        if st.button("送出答案", key=f"btn_submit_{st.session_state.current_q_idx}"):
            if user_choice == q_data['ans']:
                st.balloons()
                st.success("🎉 答對了！")
                time.sleep(1)
                st.session_state.score += 20
                st.session_state.current_q_idx += 1
                safe_rerun()
            else:
                st.error(f"不對喔！提示：{q_data['hint']}")
                
    else:
        st.progress(1.0)
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #CFD8DC; border-radius: 20px; margin-top: 20px;'>
            <h1 style='color: #455A64;'>🏆 挑戰成功！</h1>
            <h3 style='color: #333;'>本次得分：{st.session_state.score}</h3>
            <p>你已經學會物品與工具的說法了！</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再來一局 (重新抽題)", key="btn_restart"):
            st.session_state.score = 0
            st.session_state.current_q_idx = 0
            st.session_state.quiz_id = str(random.randint(1000, 9999))
            
            new_questions = random.sample(raw_quiz_pool, 5)
            final_qs = []
            for q in new_questions:
                q_copy = q.copy()
                shuffled_opts = random.sample(q['options'], len(q['options']))
                q_copy['shuffled_options'] = shuffled_opts
                final_qs.append(q_copy)
            
            st.session_state.quiz_questions = final_qs
            safe_rerun()


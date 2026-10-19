import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(page_title="Penalty Shooters 2 Pro", page_icon="⚽", layout="centered")

st.title("⚽ Penalty Shooters 2: Pro Edition")
st.markdown("Đồ họa nâng cấp, Thủ môn linh hoạt, Trải nghiệm thực tế!")

# ------------------------------------------------------------------
# PHẦN 1: ĐỊNH NGHĨA ASSET HÌNH ẢNH (PLACEHOLDER)
# Trong thực tế, bạn sẽ thay các URL này bằng Base64 Data URI của ảnh thật
# ------------------------------------------------------------------
ASSETS = {
    # Ảnh nền sân vận động 3D
    "bg": "https://via.placeholder.com/700x480/1e4d2b/ffffff?text=Stadium+3D+Background",
    # Khung thành sắc nét
    "goal": "https://via.placeholder.com/400x180/ffffff/000000?text=Realistic+Goal+Net",
    # Quả bóng đá 3D
    "ball": "https://via.placeholder.com/24/ffffff/000000?text=⚽",
    # Cầu thủ đứng yên (nhìn sau lưng, giống người thật)
    "player_idle": "https://via.placeholder.com/100x150/ff0000/ffffff?text=Player+Idle",
    # Cầu thủ đang sút
    "player_kick": "https://via.placeholder.com/120x150/cc0000/ffffff?text=Player+Kick",
    # Thủ môn đứng yên (giống người thật)
    "keeper_idle": "https://via.placeholder.com/60x90/00ffff/000000?text=GK+Idle",
    # Thủ môn bay người trái/phải
    "keeper_dive_l": "https://via.placeholder.com/110x70/00cccc/000000?text=GK+Dive+L",
    "keeper_dive_r": "https://via.placeholder.com/110x70/00cccc/000000?text=GK+Dive+R",
}

# Mã nguồn HTML/JS/CSS nâng cấp đồ họa và logic
game_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ margin: 0; padding: 0; background-color: #0b1329; color: white; font-family: 'Arial', sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
        #gameContainer {{ position: relative; width: 700px; height: 480px; overflow: hidden; border-radius: 12px; box-shadow: 0 0 30px rgba(0,0,0,0.7); }}
        canvas {{ background-color: #1a1a1a; cursor: crosshair; }}
        
        /* UI Elements */
        #menuOverlay {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 100; transition: opacity 0.5s; }}
        .game-title {{ font-size: 48px; font-weight: bold; color: #ffcc00; text-shadow: 0 0 15px #ffcc00; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 2px; }}
        .play-btn {{ padding: 15px 40px; font-size: 22px; font-weight: bold; color: #111; background: linear-gradient(135deg, #00ffcc, #ffcc00); border: none; border-radius: 40px; cursor: pointer; box-shadow: 0 5px 20px rgba(0,255,204,0.5); transition: transform 0.1s, box-shadow 0.2s; }}
        .play-btn:hover {{ transform: scale(1.05); box-shadow: 0 8px 25px rgba(0,255,204,0.7); }}
        .play-btn:active {{ transform: scale(0.98); }}
        
        #scoreboard {{ position: absolute; top: 10px; left: 10px; right: 10px; display: flex; justify-content: space-between; font-size: 18px; font-weight: bold; color: #fff; text-shadow: 1px 1px 2px #000; z-index: 10; pointer-events: none; }}
        .stat-box {{ background: rgba(0,0,0,0.5); padding: 5px 10px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.2); }}
        
        #messageBox {{ position: absolute; top: 80px; width: 100%; text-align: center; font-size: 32px; font-weight: bold; text-transform: uppercase; text-shadow: 0 0 10px rgba(0,0,0,1); z-index: 50; pointer-events: none; }}
    </style>
</head>
<body>

    <div id="gameContainer">
        <div id="scoreboard">
            <div class="stat-box">⚽ Goals: <span id="goals" style="color: #00ffcc;">0</span></div>
            <div class="stat-box">Shot: <span id="shots">0</span>/10</div>
            <div class="stat-box">Saves: <span id="saves" style="color: #ff4d4d;">0</span></div>
        </div>
        
        <div id="messageBox"></div>

        <div id="menuOverlay">
            <div class="game-title">PENALTY<br>SHOOTERS 2</div>
            <p style="color: #ccc; margin-bottom: 25px; font-size: 18px;">Pro Edition: Nhân vật thật, Thủ môn Pro!</p>
            <button class="play-btn" onclick="startGame()">BẮT ĐẦU SÚT</button>
        </div>

        <canvas id="gameCanvas" width="700" height="480"></canvas>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        // ... (Các element UI khác tương tự code cũ) ...

        // ------------------------------------------------------------------
        # PHẦN 2: LOAD ASSET HÌNH ẢNH
        # ------------------------------------------------------------------
        const img = {{}};
        const assetsBaseUrl = {str(ASSETS)}; // Nhận URL từ Python
        let assetsLoaded = 0;
        const totalAssets = Object.keys(assetsBaseUrl).length;

        function loadAssets(callback) {{
            for (let key in assetsBaseUrl) {{
                img[key] = new Image();
                img[key].src = assetsBaseUrl[key];
                img[key].onload = () => {{
                    assetsLoaded++;
                    if (assetsLoaded === totalAssets) callback();
                }};
            }}
        }}

        // --- Trạng thái Game & Nhân vật ---
        let gameRunning = false;
        let goals = 0, shots = 0, saves = 0;
        const goalRect = {{ x: 150, y: 70, width: 400, height: 180 }};
        
        let ball = {{ x: 350, y: 400, radius: 12, targetX: 350, targetY: 400, speed: 10, isMoving: false }};
        let player = {{ x: 350, y: 400, width: 100, height: 150, state: 'idle' }}; // Trạng thái 'idle' hoặc 'kick'
        
        // Thủ môn nâng cấp: Có các trạng thái bay người
        let keeper = {{ 
            x: 350, y: 150, 
            width: 60, height: 90, // Kích thước lúc đứng yên
            targetX: 350, 
            speed: 7, 
            state: 'idle', // 'idle', 'dive_l', 'dive_r'
            animFrame: 0
        }};

        let targetIndicator = {{ x: -100, y: -100, alpha: 0 }};
        let messageTimer = 0;

        // ... (startGame, resetRound, updateScoreboard giống cũ) ...

        canvas.addEventListener("click", (e) => {{
            if (!gameRunning || ball.isMoving) return;
            // ... (Logic lấy clickX, clickY và kiểm tra khung thành giống cũ) ...
                
                shots++;
                player.state = 'kick'; // Đổi sprite cầu thủ sang tư thế sút
                
                // Logic sút bóng nhanh hơn
                ball.targetX = clickX; ball.targetY = clickY; ball.isMoving = true;
                ball.speed = 12; 

                targetIndicator.x = clickX; targetIndicator.y = clickY; targetIndicator.alpha = 1.0;

                # ------------------------------------------------------------------
                # PHẦN 3: LÀM THỦ MÔN LINH HOẠT HƠN (LOGIC PRO)
                # ------------------------------------------------------------------
                // 1. Phán đoán: Có tỷ lệ phán đoán sai (đứng yên hoặc bay sai hướng)
                let aiJudgment = Math.random(); 
                
                if (aiJudgment < 0.2) {{ 
                    // 20%: Thủ môn phán đoán sai hoàn toàn, đứng yên
                    keeper.targetX = keeper.x;
                    keeper.state = 'idle';
                }} else if (aiJudgment < 0.5) {{
                    // 30%: Bay người ngẫu nhiên (có thể trúng, có thể trật)
                    keeper.targetX = goalRect.x + 50 + Math.random() * (goalRect.width - 100);
                    keeper.state = keeper.targetX < 350 ? 'dive_l' : 'dive_r';
                }} else {{
                    // 50%: Bay người theo hướng bóng (Khó ăn hơn)
                    // Thêm một chút sai số nhỏ để không bao giờ bắt dính 100%
                    let error = (Math.random() - 0.5) * 60; 
                    keeper.targetX = Math.max(goalRect.x + 40, Math.min(goalRect.x + goalRect.width - 40, clickX + error));
                    keeper.state = keeper.targetX < 350 ? 'dive_l' : 'dive_r';
                }}
                
                // Tăng tốc độ bay của thủ môn dựa trên độ khó
                keeper.speed = 8 + Math.random() * 4; 
            // ...
        }});

        function update() {{
            if (!gameRunning) return;

            // Di chuyển bóng
            if (ball.isMoving) {{
                // ... (Logic di chuyển bóng giống cũ) ...
                    checkGoal();
                    player.state = 'idle'; // Sút xong về tư thế cũ
                }}
            }}

            // Di chuyển và cập nhật trạng thái thủ môn (Linh hoạt hơn)
            let kDx = keeper.targetX - keeper.x;
            if (Math.abs(kDx) > 3) {{
                keeper.x += Math.sign(kDx) * keeper.speed;
                // Nếu đang di chuyển nhanh, giữ trạng thái bay
            }} else {{
                // Đã đến điểm đến, nếu bóng chưa tới thì đứng yên chờ
                if (!ball.isMoving) keeper.state = 'idle';
            }}
            
            // ... (Message timer giống cũ) ...
        }}

        # ------------------------------------------------------------------
        # PHẦN 4: VẼ ĐỒ HOẠ ĐẸP HƠN (DÙNG ASSET PNG)
        # ------------------------------------------------------------------
        function draw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 1. Vẽ Nền Sân vận động 3D
            ctx.drawImage(img.bg, 0, 0, canvas.width, canvas.height);

            // 2. Vẽ Khung thành Realistic
            ctx.drawImage(img.goal, goalRect.x, goalRect.y, goalRect.width, goalRect.height);

            // 3. Vẽ Cầu thủ (Giống người thật)
            let pImg = player.state === 'kick' ? img.player_kick : img.player_idle;
            ctx.drawImage(pImg, player.x - player.width/2, player.y - player.height/2, player.width, player.height);

            // 4. Vẽ Thủ môn (Linh hoạt, thay đổi tư thế)
            let kImg = img.keeper_idle;
            let kw = keeper.width, kh = keeper.height;
            
            if (keeper.state === 'dive_l') {{
                kImg = img.keeper_dive_l; kw = 110; kh = 70; // Kích thước khi bay
            }} else if (keeper.state === 'dive_r') {{
                kImg = img.keeper_dive_r; kw = 110; kh = 70;
            }}
            
            ctx.drawImage(kImg, keeper.x - kw/2, keeper.y, kw, kh);

            // ... (Vẽ tâm ngắm red dot giống cũ) ...

            // 5. Vẽ Quả bóng 3D
            ctx.drawImage(img.ball, ball.x - ball.radius, ball.y - ball.radius, ball.radius*2, ball.radius*2);
        }}

        // Khởi tạo game sau khi load xong asset
        loadAssets(() => {{
            function gameLoop() {{ update(); draw(); requestAnimationFrame(gameLoop); }}
            gameLoop();
        }});
    </script>
</body>
</html>
"""

# Hiển thị game
components.html(game_html, height=560)

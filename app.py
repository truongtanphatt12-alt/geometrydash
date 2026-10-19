import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(page_title="Penalty Shooters 2 Pro", page_icon="⚽", layout="centered")

st.title("⚽ Penalty Shooters 2: Pro Edition")
st.markdown("Nút bấm bắt đầu game đã được nâng cấp thiết kế cực đẹp!")

# ------------------------------------------------------------------
# PHẦN ASSET HÌNH ẢNH (BẠN CÓ THỂ THAY BẰNG LINK ANH HOẶC BASE64 CỦA BẠN)
# ------------------------------------------------------------------
ASSETS = {
    "bg": "https://via.placeholder.com/700x480/1e4d2b/ffffff?text=Stadium+3D+Background",
    "goal": "https://via.placeholder.com/400x180/ffffff/000000?text=Realistic+Goal+Net",
    "ball": "https://via.placeholder.com/24/ffffff/000000?text=⚽",
    "player_idle": "https://via.placeholder.com/100x150/ff0000/ffffff?text=Player+Idle",
    "player_kick": "https://via.placeholder.com/120x150/cc0000/ffffff?text=Player+Kick",
    "keeper_idle": "https://via.placeholder.com/60x90/00ffff/000000?text=GK+Idle",
    "keeper_dive_l": "https://via.placeholder.com/110x70/00cccc/000000?text=GK+Dive+L",
    "keeper_dive_r": "https://via.placeholder.com/110x70/00cccc/000000?text=GK+Dive+R",
}

game_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ 
            margin: 0; 
            padding: 0; 
            background-color: #0b1329; 
            color: white; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: center; 
        }}
        #gameContainer {{ 
            position: relative; 
            width: 700px; 
            height: 480px; 
            overflow: hidden; 
            border-radius: 12px; 
            box-shadow: 0 0 30px rgba(0,0,0,0.8); 
        }}
        canvas {{ 
            background-color: #1a1a1a; 
            cursor: crosshair; 
        }}
        
        /* Overlay Menu */
        #menuOverlay {{ 
            position: absolute; 
            top: 0; 
            left: 0; 
            width: 100%; 
            height: 100%; 
            background: radial-gradient(circle, rgba(15,23,42,0.85) 0%, rgba(11,19,41,0.95) 100%); 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: center; 
            z-index: 100; 
            backdrop-filter: blur(4px);
        }}
        .game-title {{ 
            font-size: 44px; 
            font-weight: 900; 
            background: linear-gradient(135deg, #fff 0%, #ffcc00 50%, #ff9900 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 10px 20px rgba(255, 204, 0, 0.3);
            margin-bottom: 5px; 
            text-transform: uppercase; 
            letter-spacing: 2px; 
            text-align: center;
        }}
        
        /* NÚT BẮT ĐẦU GAME (START BUTTON STYLING) */
        .play-btn {{
            position: relative;
            padding: 18px 48px;
            font-size: 22px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: #0d1117;
            background: linear-gradient(135deg, #ffea00, #ff9100);
            border: none;
            border-radius: 50px;
            cursor: pointer;
            box-shadow: 0 0 20px rgba(255, 145, 0, 0.6), 0 6px 0px #b36200;
            transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            overflow: hidden;
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        /* Hiệu ứng Ánh sáng lướt qua trên nút */
        .play-btn::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: rgba(255, 255, 255, 0.3);
            transform: rotate(45deg) translateY(-100%);
            transition: transform 0.6s ease;
        }}

        .play-btn:hover::before {{
            transform: rotate(45deg) translateY(100%);
        }}

        .play-btn:hover {{
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 0 30px rgba(255, 200, 0, 0.9), 0 9px 0px #b36200;
            background: linear-gradient(135deg, #fff066, #ffa726);
        }}

        .play-btn:active {{
            transform: translateY(3px) scale(0.98);
            box-shadow: 0 0 15px rgba(255, 145, 0, 0.8), 0 2px 0px #b36200;
        }}
        
        #scoreboard {{ 
            position: absolute; 
            top: 12px; 
            left: 15px; 
            right: 15px; 
            display: flex; 
            justify-content: space-between; 
            font-size: 16px; 
            font-weight: 700; 
            color: #fff; 
            z-index: 10; 
            pointer-events: none; 
        }}
        .stat-box {{ 
            background: rgba(0, 0, 0, 0.6); 
            padding: 6px 14px; 
            border-radius: 20px; 
            border: 1px solid rgba(255,255,255,0.15); 
            backdrop-filter: blur(5px);
        }}
        
        #messageBox {{ 
            position: absolute; 
            top: 85px; 
            width: 100%; 
            text-align: center; 
            font-size: 30px; 
            font-weight: 900; 
            text-transform: uppercase; 
            text-shadow: 0 0 12px rgba(0,0,0,0.9); 
            z-index: 50; 
            pointer-events: none; 
        }}
    </style>
</head>
<body>

    <div id="gameContainer">
        <div id="scoreboard">
            <div class="stat-box">⚽ Goals: <span id="goals" style="color: #00ffcc;">0</span></div>
            <div class="stat-box">Lượt sút: <span id="shots">0</span>/10</div>
            <div class="stat-box">Thủ môn cản: <span id="saves" style="color: #ff4d4d;">0</span></div>
        </div>
        
        <div id="messageBox"></div>

        <!-- MENU GAME VỚI NÚT CHƠI MỚI -->
        <div id="menuOverlay">
            <div class="game-title">PENALTY SHOOTERS 2</div>
            <p style="color: #94a3b8; margin-top: 0; margin-bottom: 30px; font-size: 16px; font-weight: 500;">
                Hãy chọn góc sút để hạ gục thủ môn đối phương!
            </p>
            <button class="play-btn" onclick="startGame()">
                <span>⚽ BẮT ĐẦU SÚT</span>
            </button>
        </div>

        <canvas id="gameCanvas" width="700" height="480"></canvas>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const menuOverlay = document.getElementById("menuOverlay");
        const goalsEl = document.getElementById("goals");
        const shotsEl = document.getElementById("shots");
        const savesEl = document.getElementById("saves");
        const messageBox = document.getElementById("messageBox");

        // LOAD ASSET
        const img = {{}};
        const assetsBaseUrl = {str(ASSETS)};
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

        let gameRunning = false;
        let goals = 0, shots = 0, saves = 0;
        const goalRect = {{ x: 150, y: 70, width: 400, height: 180 }};
        
        let ball = {{ x: 350, y: 400, radius: 12, targetX: 350, targetY: 400, speed: 10, isMoving: false }};
        let player = {{ x: 350, y: 400, width: 100, height: 150, state: 'idle' }};
        let keeper = {{ x: 350, y: 150, width: 60, height: 90, targetX: 350, speed: 7, state: 'idle' }};

        let targetIndicator = {{ x: -100, y: -100, alpha: 0 }};
        let messageTimer = 0;

        function startGame() {{
            goals = 0; shots = 0; saves = 0;
            updateScoreboard();
            menuOverlay.style.opacity = "0";
            setTimeout(() => {{ menuOverlay.style.display = "none"; }}, 300);
            gameRunning = true;
            resetRound();
        }}

        function updateScoreboard() {{
            goalsEl.innerText = goals;
            shotsEl.innerText = shots;
            savesEl.innerText = saves;
        }}

        function resetRound() {{
            ball.x = 350; ball.y = 400; ball.isMoving = false;
            keeper.x = 350; keeper.targetX = 350; keeper.state = 'idle';
            player.state = 'idle';
            targetIndicator.alpha = 0;
        }}

        canvas.addEventListener("click", (e) => {{
            if (!gameRunning || ball.isMoving) return;

            const rect = canvas.getBoundingClientRect();
            let clickX = e.clientX - rect.left;
            let clickY = e.clientY - rect.top;

            if (clickX >= goalRect.x && clickX <= goalRect.x + goalRect.width &&
                clickY >= goalRect.y && clickY <= goalRect.y + goalRect.height) {{
                
                shots++;
                player.state = 'kick';
                ball.targetX = clickX; ball.targetY = clickY; ball.isMoving = true; ball.speed = 12;

                targetIndicator.x = clickX; targetIndicator.y = clickY; targetIndicator.alpha = 1.0;

                // AI thủ môn phán đoán linh hoạt
                let aiJudgment = Math.random();
                if (aiJudgment < 0.2) {{
                    keeper.targetX = keeper.x;
                    keeper.state = 'idle';
                }} else if (aiJudgment < 0.5) {{
                    keeper.targetX = goalRect.x + 50 + Math.random() * (goalRect.width - 100);
                    keeper.state = keeper.targetX < 350 ? 'dive_l' : 'dive_r';
                }} else {{
                    let error = (Math.random() - 0.5) * 60;
                    keeper.targetX = Math.max(goalRect.x + 40, Math.min(goalRect.x + goalRect.width - 40, clickX + error));
                    keeper.state = keeper.targetX < 350 ? 'dive_l' : 'dive_r';
                }}
                keeper.speed = 8 + Math.random() * 4;
            }}
        }});

        function update() {{
            if (!gameRunning) return;

            if (ball.isMoving) {{
                let dx = ball.targetX - ball.x;
                let dy = ball.targetY - ball.y;
                let dist = Math.hypot(dx, dy);

                if (dist > 5) {{
                    ball.x += (dx / dist) * ball.speed;
                    ball.y += (dy / dist) * ball.speed;
                }} else {{
                    checkGoal();
                    player.state = 'idle';
                }}
            }}

            let kDx = keeper.targetX - keeper.x;
            if (Math.abs(kDx) > 3) {{
                keeper.x += Math.sign(kDx) * keeper.speed;
            }} else {{
                if (!ball.isMoving) keeper.state = 'idle';
            }}

            if (messageTimer > 0) {{
                messageTimer--;
                if (messageTimer === 0) messageBox.innerText = "";
            }}
        }}

        function checkGoal() {{
            ball.isMoving = false;
            let distanceToKeeper = Math.hypot(ball.x - keeper.x, ball.y - keeper.y);

            if (distanceToKeeper < 50) {{
                saves++;
                messageBox.innerText = "❌ THỦ MÔN CẢN PHÁ!";
                messageBox.style.color = "#ff4d4d";
            }} else {{
                goals++;
                messageBox.innerText = "GOAL! ⚽ VÀO RẤT ĐẸP!";
                messageBox.style.color = "#00ffcc";
            }}

            updateScoreboard();
            messageTimer = 80;

            if (shots >= 10) {{
                gameRunning = false;
                setTimeout(() => {{
                    menuOverlay.style.display = "flex";
                    menuOverlay.style.opacity = "1";
                    document.querySelector(".game-title").innerText = "KẾT QUẢ TRẬN ĐẤU";
                    document.querySelector("#menuOverlay p").innerHTML = `Bạn ghi được <b style="color:#00ffcc">${goals}</b> / 10 bàn thắng!`;
                }}, 1500);
            }} else {{
                setTimeout(resetRound, 1200);
            }}
        }}

        function draw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 1. Sân 3D
            ctx.drawImage(img.bg, 0, 0, canvas.width, canvas.height);

            // 2. Khung thành
            ctx.drawImage(img.goal, goalRect.x, goalRect.y, goalRect.width, goalRect.height);

            // 3. Cầu thủ
            let pImg = player.state === 'kick' ? img.player_kick : img.player_idle;
            ctx.drawImage(pImg, player.x - player.width/2, player.y - player.height/2, player.width, player.height);

            // 4. Thủ môn
            let kImg = img.keeper_idle;
            let kw = keeper.width, kh = keeper.height;
            if (keeper.state === 'dive_l') {{ kImg = img.keeper_dive_l; kw = 110; kh = 70; }}
            else if (keeper.state === 'dive_r') {{ kImg = img.keeper_dive_r; kw = 110; kh = 70; }}
            ctx.drawImage(kImg, keeper.x - kw/2, keeper.y, kw, kh);

            // 5. Tâm ngắm Red Dot
            if (targetIndicator.alpha > 0) {{
                ctx.strokeStyle = "red";
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.arc(targetIndicator.x, targetIndicator.y, 14, 0, Math.PI * 2);
                ctx.stroke();
            }}

            // 6. Quả bóng
            ctx.drawImage(img.ball, ball.x - ball.radius, ball.y - ball.radius, ball.radius*2, ball.radius*2);
        }}

        loadAssets(() => {{
            function gameLoop() {{ update(); draw(); requestAnimationFrame(gameLoop); }}
            gameLoop();
        }});
    </script>
</body>
</html>
"""

components.html(game_html, height=560)

import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(page_title="Chicken Invaders - Streamlit", page_icon="🐔", layout="centered")

st.title("🐔 CHICKEN INVADERS")
st.caption("Game Bắn Gà Vũ Trụ - Tốc độ đạn đã được giảm lại cho vừa tầm, dễ chơi!")

# Mã nguồn HTML, CSS và JS
game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #050510;
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            user-select: none;
        }
        #gameContainer {
            position: relative;
            width: 700px;
            height: 520px;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 0 30px rgba(0, 150, 255, 0.4);
            border: 2px solid #1a2a4a;
        }
        canvas {
            background-color: #030308;
            display: block;
        }
        
        #menuOverlay {
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: radial-gradient(circle, rgba(10, 15, 35, 0.9) 0%, rgba(3, 3, 8, 0.98) 100%);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 10;
        }

        .game-title {
            font-size: 46px;
            font-weight: 900;
            background: linear-gradient(135deg, #ffffff 0%, #38bdf8 50%, #0284c7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 20px rgba(56, 189, 248, 0.5);
            margin: 0 0 10px 0;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-align: center;
        }

        .sub-title {
            color: #fbbf24;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 30px;
            text-shadow: 0 0 10px rgba(251, 191, 36, 0.4);
        }

        .play-btn {
            padding: 15px 42px;
            font-size: 22px;
            font-weight: 800;
            text-transform: uppercase;
            color: #0f172a;
            background: linear-gradient(135deg, #f59e0b, #fbbf24);
            border: none;
            border-radius: 40px;
            cursor: pointer;
            box-shadow: 0 0 25px rgba(245, 158, 11, 0.6);
            transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        .play-btn:hover {
            transform: scale(1.08);
            box-shadow: 0 0 35px rgba(245, 158, 11, 0.9);
            background: linear-gradient(135deg, #fbbf24, #fef08a);
        }

        .controls-hint {
            margin-top: 30px;
            font-size: 13px;
            color: #94a3b8;
            text-align: center;
            line-height: 1.6;
        }

        #uiHeader {
            position: absolute;
            top: 12px; left: 18px; right: 18px;
            display: flex;
            justify-content: space-between;
            font-size: 16px;
            font-weight: bold;
            color: #38bdf8;
            z-index: 5;
            pointer-events: none;
            text-shadow: 0 0 8px rgba(0,0,0,0.8);
        }
    </style>
</head>
<body>

    <div id="gameContainer">
        <div id="uiHeader">
            <div>SCORE: <span id="scoreText" style="color: #fff;">0</span></div>
            <div>WAVE: <span id="waveText" style="color: #fbbf24;">1</span></div>
            <div>LIVES: <span id="livesText" style="color: #ef4444;">❤️❤️❤️</span></div>
        </div>

        <div id="menuOverlay">
            <h1 class="game-title">CHICKEN INVADERS</h1>
            <div class="sub-title">🐔 BẮN GÀ VŨ TRỤ 🐔</div>
            <button class="play-btn" onclick="startGame()">START GAME</button>
            <div class="controls-hint">
                🎮 <b>ĐIỀU KHIỂN:</b><br>
                • Di chuyển: Phím <b>Mũi tên</b> hoặc <b>W/A/S/D</b><br>
                • Bắn đạn: Phím <b>SPACE (Dấu cách)</b>
            </div>
        </div>

        <canvas id="gameCanvas" width="700" height="520"></canvas>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const menuOverlay = document.getElementById("menuOverlay");
        const scoreText = document.getElementById("scoreText");
        const waveText = document.getElementById("waveText");
        const livesText = document.getElementById("livesText");

        let gameActive = false;
        let score = 0;
        let wave = 1;
        let lives = 3;

        const keys = {};
        window.addEventListener("keydown", e => {
            keys[e.code] = true;
            if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "Space"].includes(e.code)) {
                e.preventDefault();
            }
        });
        window.addEventListener("keyup", e => { keys[e.code] = false; });

        const stars = [];
        for (let i = 0; i < 70; i++) {
            stars.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                size: Math.random() * 2 + 0.5,
                speed: Math.random() * 1.5 + 0.5
            });
        }

        const player = {
            x: 330,
            y: 440,
            width: 40,
            height: 40,
            speed: 5.5,
            cooldown: 0
        };

        let bullets = [];
        let chickens = [];
        let eggs = [];
        let drumsticks = [];

        function startGame() {
            score = 0;
            wave = 1;
            lives = 3;
            player.x = 330;
            player.y = 440;
            bullets = [];
            eggs = [];
            drumsticks = [];
            
            updateUI();
            spawnChickens();
            menuOverlay.style.display = "none";
            gameActive = true;
        }

        function updateUI() {
            scoreText.innerText = score;
            waveText.innerText = wave;
            livesText.innerText = "❤️".repeat(Math.max(0, lives));
        }

        function spawnChickens() {
            chickens = [];
            const rows = Math.min(2 + wave, 5);
            const cols = 8;
            for (let r = 0; r < rows; r++) {
                for (let c = 0; c < cols; c++) {
                    chickens.push({
                        x: 80 + c * 70,
                        y: 50 + r * 50,
                        width: 42,
                        height: 38,
                        dir: 1,
                        speed: 0.6 + wave * 0.15,
                        animTimer: Math.random() * 10
                    });
                }
            }
        }

        function update() {
            stars.forEach(s => {
                s.y += s.speed;
                if (s.y > canvas.height) { s.y = 0; s.x = Math.random() * canvas.width; }
            });

            if (!gameActive) return;

            if ((keys["ArrowLeft"] || keys["KeyA"]) && player.x > 10) player.x -= player.speed;
            if ((keys["ArrowRight"] || keys["KeyD"]) && player.x < canvas.width - player.width - 10) player.x += player.speed;
            if ((keys["ArrowUp"] || keys["KeyW"]) && player.y > 100) player.y -= player.speed;
            if ((keys["ArrowDown"] || keys["KeyS"]) && player.y < canvas.height - player.height - 10) player.y += player.speed;

            if (player.cooldown > 0) player.cooldown--;
            if (keys["Space"] && player.cooldown === 0) {
                // GIẢM TỐC ĐỘ ĐẠN BAY (Từ 9 xuống 5.0 để đạn đi từ từ, dễ nhắm bắn)
                bullets.push({ x: player.x + player.width / 2 - 3, y: player.y, width: 6, height: 16, speed: 5.0 });
                player.cooldown = 12;
            }

            bullets.forEach((b, index) => {
                b.y -= b.speed;
                if (b.y < -20) bullets.splice(index, 1);
            });

            let changeDir = false;
            chickens.forEach(c => {
                c.x += c.speed * c.dir;
                c.animTimer += 0.08;
                if (c.x > canvas.width - 60 || c.x < 10) changeDir = true;

                if (Math.random() < 0.0012 * wave) {
                    eggs.push({ x: c.x + c.width / 2, y: c.y + c.height, width: 10, height: 14, speed: 2.2 + wave * 0.2 });
                }
            });

            if (changeDir) {
                chickens.forEach(c => {
                    c.dir *= -1;
                    c.y += 10;
                });
            }

            bullets.forEach((b, bIdx) => {
                chickens.forEach((c, cIdx) => {
                    if (b.x < c.x + c.width && b.x + b.width > c.x &&
                        b.y < c.y + c.height && b.y + b.height > c.y) {
                        
                        if (Math.random() < 0.4) {
                            drumsticks.push({ x: c.x + c.width / 2, y: c.y, width: 16, height: 16, speed: 2 });
                        }

                        chickens.splice(cIdx, 1);
                        bullets.splice(bIdx, 1);
                        score += 50;
                        updateUI();
                    }
                });
            });

            eggs.forEach((e, eIdx) => {
                e.y += e.speed;
                if (e.y > canvas.height) eggs.splice(eIdx, 1);

                if (e.x < player.x + player.width && e.x + e.width > player.x &&
                    e.y < player.y + player.height && e.y + e.height > player.y) {
                    eggs.splice(eIdx, 1);
                    playerHit();
                }
            });

            drumsticks.forEach((d, dIdx) => {
                d.y += d.speed;
                if (d.y > canvas.height) drumsticks.splice(dIdx, 1);

                if (d.x < player.x + player.width && d.x + d.width > player.x &&
                    d.y < player.y + player.height && d.y + d.height > player.y) {
                    drumsticks.splice(dIdx, 1);
                    score += 100;
                    updateUI();
                }
            });

            if (chickens.length === 0) {
                wave++;
                updateUI();
                spawnChickens();
            }
        }

        function playerHit() {
            lives--;
            updateUI();
            if (lives <= 0) {
                gameActive = false;
                setTimeout(() => {
                    menuOverlay.style.display = "flex";
                    document.querySelector(".game-title").innerText = "GAME OVER";
                    document.querySelector(".sub-title").innerHTML = `Bạn đạt được <b style="color:#38bdf8">${score}</b> điểm!`;
                }, 500);
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = "#ffffff";
            stars.forEach(s => {
                ctx.beginPath();
                ctx.arc(s.x, s.y, s.size, 0, Math.PI * 2);
                ctx.fill();
            });

            if (!gameActive && menuOverlay.style.display !== "none") return;

            // Phi thuyền
            ctx.fillStyle = "#38bdf8";
            ctx.beginPath();
            ctx.moveTo(player.x + player.width / 2, player.y);
            ctx.lineTo(player.x + player.width, player.y + player.height);
            ctx.lineTo(player.x, player.y + player.height);
            ctx.closePath();
            ctx.fill();

            ctx.fillStyle = "#f59e0b";
            ctx.beginPath();
            ctx.arc(player.x + player.width / 2, player.y + player.height + 4, 6, 0, Math.PI * 2);
            ctx.fill();

            // Đạn (đi chậm)
            ctx.fillStyle = "#38bdf8";
            ctx.shadowBlur = 10;
            ctx.shadowColor = "#38bdf8";
            bullets.forEach(b => {
                ctx.fillRect(b.x, b.y, b.width, b.height);
            });
            ctx.shadowBlur = 0;

            // Gà
            chickens.forEach(c => {
                let cx = c.x + c.width / 2;
                let cy = c.y + c.height / 2;
                let wingFlap = Math.sin(c.animTimer) * 6;

                ctx.fillStyle = "#60a5fa";
                ctx.beginPath();
                ctx.arc(cx, cy + 2, 14, 0, Math.PI * 2);
                ctx.fill();

                ctx.fillStyle = "#ffffff";
                ctx.beginPath();
                ctx.arc(cx, cy + 5, 10, 0, Math.PI);
                ctx.fill();

                ctx.fillStyle = "#ffffff";
                ctx.beginPath();
                ctx.ellipse(cx - 16, cy + wingFlap, 6, 12, Math.PI / 6, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.ellipse(cx + 16, cy - wingFlap, 6, 12, -Math.PI / 6, 0, Math.PI * 2);
                ctx.fill();

                ctx.fillStyle = "#ffffff";
                ctx.beginPath();
                ctx.arc(cx, cy - 8, 11, 0, Math.PI * 2);
                ctx.fill();

                ctx.fillStyle = "#000000";
                ctx.beginPath();
                ctx.arc(cx - 3, cy - 10, 2.5, 0, Math.PI * 2);
                ctx.arc(cx + 4, cy - 10, 2.5, 0, Math.PI * 2);
                ctx.fill();

                ctx.fillStyle = "#f59e0b";
                ctx.beginPath();
                ctx.moveTo(cx - 2, cy - 6);
                ctx.lineTo(cx + 5, cy - 4);
                ctx.lineTo(cx - 1, cy - 1);
                ctx.fill();

                ctx.fillStyle = "#ef4444";
                ctx.beginPath();
                ctx.arc(cx, cy - 18, 4, 0, Math.PI * 2);
                ctx.fill();
            });

            // Trứng
            ctx.fillStyle = "#fef08a";
            eggs.forEach(e => {
                ctx.beginPath();
                ctx.ellipse(e.x, e.y, e.width / 2, e.height / 2, 0, 0, Math.PI * 2);
                ctx.fill();
            });

            // Đùi gà
            ctx.fillStyle = "#fbbf24";
            drumsticks.forEach(d => {
                ctx.beginPath();
                ctx.arc(d.x, d.y, 6, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = "#ffffff";
                ctx.fillRect(d.x - 2, d.y - 8, 4, 6);
            });
        }

        function gameLoop() {
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }

        gameLoop();
    </script>
</body>
</html>
"""

components.html(game_html, height=560)

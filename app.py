import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(page_title="Slither.io - Streamlit Edition", page_icon="🐍", layout="centered")

st.title("🐍 Slither.io Game")

# Nhập Nickname
nickname = st.text_input("Biệt danh (Nickname):", value="Rắn Săn Mồi")

# Mã nguồn HTML/JS/CSS nâng cấp với Menu & Bàn phím + Tăng tốc
game_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            margin: 0;
            padding: 0;
            background-color: #0d0e15;
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
            height: 500px;
        }}
        canvas {{
            background-color: #161923;
            border: 3px solid #4e5d78;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.8);
        }}
        /* Menu Overlay */
        #menuOverlay {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(13, 14, 21, 0.88);
            border-radius: 10px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 10;
        }}
        .game-title {{
            font-size: 42px;
            font-weight: bold;
            color: #00ffcc;
            text-shadow: 0 0 10px #00ffcc;
            margin-bottom: 10px;
        }}
        .play-btn {{
            padding: 12px 30px;
            font-size: 20px;
            font-weight: bold;
            color: white;
            background: linear-gradient(135deg, #28a745, #20c997);
            border: none;
            border-radius: 25px;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(40, 167, 69, 0.4);
            transition: transform 0.2s, background 0.2s;
        }}
        .play-btn:hover {{
            transform: scale(1.05);
            background: linear-gradient(135deg, #218838, #1baa80);
        }}
        .controls-info {{
            margin-top: 20px;
            font-size: 14px;
            color: #a0aec0;
            text-align: center;
            line-height: 1.6;
        }}
        .score-board {{
            margin-bottom: 8px;
            font-size: 16px;
            font-weight: bold;
            color: #00ffcc;
            display: flex;
            justify-content: space-between;
            width: 100%;
        }}
    </style>
</head>
<body>

    <div style="width: 700px;">
        <div class="score-board">
            <div>Người chơi: <span id="playerName" style="color:white;">{nickname}</span></div>
            <div>Điểm: <span id="score">0</span></div>
            <div>Kỷ lục: <span id="highScore">0</span></div>
        </div>
    </div>

    <div id="gameContainer">
        <!-- Menu overlay -->
        <div id="menuOverlay">
            <div class="game-title">slither.io</div>
            <button class="play-btn" onclick="startGame()">Play Game</button>
            <div class="controls-info">
                🎮 <b>Hướng dẫn điều khiển:</b><br>
                • Nút <b>Mũi tên</b> hoặc <b>W/A/S/D</b>: Đổi hướng di chuyển<br>
                • Phím <b>SPACE (Dấu cách)</b> hoặc <b>SHIFT</b>: Tăng tốc ⚡<br>
                <i>(Lưu ý: Tăng tốc sẽ tiêu tốn dần độ dài của rắn)</i>
            </div>
        </div>

        <canvas id="gameCanvas" width="700" height="500"></canvas>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const scoreEl = document.getElementById("score");
        const highScoreEl = document.getElementById("highScore");
        const menuOverlay = document.getElementById("menuOverlay");

        let gameRunning = false;
        let score = 0;
        let highScore = 0;

        // Bàn phím
        const keys = {{}};
        
        window.addEventListener("keydown", (e) => {{
            keys[e.code] = true;
            // Ngăn trình duyệt cuộn trang khi bấm phím mũi tên hoặc Space
            if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "Space"].includes(e.code)) {{
                e.preventDefault();
            }}
        }});
        
        window.addEventListener("keyup", (e) => {{
            keys[e.code] = false;
        }});

        // Trạng thái Rắn
        let snake = {{}};
        let foods = [];
        const numFoods = 60;
        const colors = ["#ff4d4d", "#33cc33", "#ffcc00", "#ff00ff", "#00ffff", "#ff9933"];

        function initGame() {{
            score = 0;
            scoreEl.innerText = score;
            snake = {{
                x: canvas.width / 2,
                y: canvas.height / 2,
                angle: 0,           // Góc di chuyển tính bằng Radian
                turnSpeed: 0.08,    // Tốc độ quay đầu
                baseSpeed: 2.5,     // Tốc độ bình thường
                speed: 2.5,
                radius: 12,
                body: [],
                length: 20
            }};

            foods = [];
            for (let i = 0; i < numFoods; i++) {{
                foods.push(createFood());
            }}
        }}

        function createFood() {{
            return {{
                x: Math.random() * (canvas.width - 40) + 20,
                y: Math.random() * (canvas.height - 40) + 20,
                radius: Math.random() * 3 + 3,
                color: colors[Math.floor(Math.random() * colors.length)]
            }};
        }}

        function startGame() {{
            initGame();
            menuOverlay.style.display = "none";
            gameRunning = true;
        }}

        function gameOver() {{
            gameRunning = false;
            if (score > highScore) {{
                highScore = score;
                highScoreEl.innerText = highScore;
            }}
            menuOverlay.style.display = "flex";
        }}

        // Cập nhật trạng thái game
        function update() {{
            if (!gameRunning) return;

            // 1. Điều khiển góc quay bằng phím
            if (keys["ArrowLeft"] || keys["KeyA"]) {{
                snake.angle -= snake.turnSpeed;
            }}
            if (keys["ArrowRight"] || keys["KeyD"]) {{
                snake.angle += snake.turnSpeed;
            }}

            // 2. Tăng tốc (Boost) khi nhấn Space hoặc Shift
            let isBoosting = keys["Space"] || keys["ShiftLeft"] || keys["ShiftRight"];
            if (isBoosting && snake.length > 10) {{
                snake.speed = snake.baseSpeed * 2.0; // Tăng gấp đôi tốc độ
                snake.length -= 0.1;                 // Tiêu tốn chiều dài khi tăng tốc
                if (Math.random() < 0.3) {{
                    // Rơi ra hạt thức ăn nhỏ đằng sau khi boost
                    foods.push({{
                        x: snake.x - Math.cos(snake.angle) * 20,
                        y: snake.y - Math.sin(snake.angle) * 20,
                        radius: 2,
                        color: "#ffaa00"
                    }});
                }}
            }} else {{
                snake.speed = snake.baseSpeed;
            }}

            // 3. Di chuyển vị trí đầu rắn
            snake.x += Math.cos(snake.angle) * snake.speed;
            snake.y += Math.sin(snake.angle) * snake.speed;

            // Va chạm tường -> Game Over
            if (snake.x < snake.radius || snake.x > canvas.width - snake.radius ||
                snake.y < snake.radius || snake.y > canvas.height - snake.radius) {{
                gameOver();
                return;
            }}

            // Lưu lịch sử các khớp thân
            snake.body.unshift({{ x: snake.x, y: snake.y }});
            if (snake.body.length > Math.floor(snake.length)) {{
                snake.body.pop();
            }}

            // 4. Ăn thức ăn
            foods.forEach((food, index) => {{
                let dx = snake.x - food.x;
                let dy = snake.y - food.y;
                let dist = Math.hypot(dx, dy);

                if (dist < snake.radius + food.radius) {{
                    score += 10;
                    snake.length += 2;
                    scoreEl.innerText = Math.floor(score);
                    foods[index] = createFood();
                }}
            }});
        }}

        // Vẽ đồ họa
        function draw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Vẽ lưới nền
            ctx.strokeStyle = "#222736";
            ctx.lineWidth = 1;
            for (let x = 0; x < canvas.width; x += 40) {{
                ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
            }}
            for (let y = 0; y < canvas.height; y += 40) {{
                ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
            }}

            // Vẽ thức ăn
            foods.forEach(food => {{
                ctx.beginPath();
                ctx.arc(food.x, food.y, food.radius, 0, Math.PI * 2);
                ctx.fillStyle = food.color;
                ctx.shadowBlur = 8;
                ctx.shadowColor = food.color;
                ctx.fill();
                ctx.shadowBlur = 0;
            }});

            // Vẽ thân rắn
            for (let i = snake.body.length - 1; i >= 0; i--) {{
                let pt = snake.body[i];
                ctx.beginPath();
                ctx.arc(pt.x, pt.y, snake.radius - (i * 0.08 > 4 ? 4 : i * 0.08), 0, Math.PI * 2);
                ctx.fillStyle = i === 0 ? "#ff9900" : "#ffaa33";
                if (keys["Space"] || keys["ShiftLeft"] || keys["ShiftRight"]) {{
                    ctx.fillStyle = i === 0 ? "#ff3300" : "#ff6600"; // Đổi màu khi boost
                }}
                ctx.fill();
                ctx.strokeStyle = "#b35900";
                ctx.lineWidth = 1;
                ctx.stroke();
            }}

            // Vẽ mắt theo hướng quay
            if (snake.body.length > 0) {{
                let head = snake.body[0];
                let eyeOffset = 6;
                let eyeX1 = head.x + Math.cos(snake.angle + 0.6) * eyeOffset;
                let eyeY1 = head.y + Math.sin(snake.angle + 0.6) * eyeOffset;
                let eyeX2 = head.x + Math.cos(snake.angle - 0.6) * eyeOffset;
                let eyeY2 = head.y + Math.sin(snake.angle - 0.6) * eyeOffset;

                ctx.fillStyle = "white";
                ctx.beginPath(); ctx.arc(eyeX1, eyeY1, 3.5, 0, Math.PI * 2); ctx.fill();
                ctx.beginPath(); ctx.arc(eyeX2, eyeY2, 3.5, 0, Math.PI * 2); ctx.fill();

                ctx.fillStyle = "black";
                ctx.beginPath(); ctx.arc(eyeX1, eyeY1, 1.8, 0, Math.PI * 2); ctx.fill();
                ctx.beginPath(); ctx.arc(eyeX2, eyeY2, 1.8, 0, Math.PI * 2); ctx.fill();
            }}
        }}

        function gameLoop() {{
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }}

        gameLoop();
    </script>
</body>
</html>
"""

# Hiển thị Game trong ứng dụng Streamlit
components.html(game_html, height=580)

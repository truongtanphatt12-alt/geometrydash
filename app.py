import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(page_title="Penalty Shooters 2 - Streamlit Edition", page_icon="⚽", layout="centered")

st.title("⚽ Penalty Shooters 2")
st.write("Trò chơi sút phạt đền đỉnh cao ngay trên ứng dụng Streamlit!")

# Mã nguồn HTML/JS/CSS cho game Penalty Shooters 2
game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #0b1329;
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        #gameContainer {
            position: relative;
            width: 700px;
            height: 480px;
        }
        canvas {
            background: linear-gradient(to bottom, #2b5876, #4e4376);
            border: 3px solid #ffcc00;
            border-radius: 10px;
            box-shadow: 0 0 25px rgba(0,0,0,0.8);
            cursor: crosshair;
        }
        /* Menu Overlay */
        #menuOverlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(11, 19, 41, 0.9);
            border-radius: 10px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 10;
        }
        .game-title {
            font-size: 38px;
            font-weight: bold;
            color: #00ffcc;
            text-shadow: 0 0 10px #00ffcc;
            margin-bottom: 5px;
            text-transform: uppercase;
        }
        .play-btn {
            padding: 12px 35px;
            font-size: 20px;
            font-weight: bold;
            color: #111;
            background: linear-gradient(135deg, #00ffcc, #ffcc00);
            border: none;
            border-radius: 30px;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,255,204,0.4);
            transition: transform 0.2s, background 0.2s;
        }
        .play-btn:hover {
            transform: scale(1.08);
            background: linear-gradient(135deg, #00cca3, #e6b800);
        }
        .controls-info {
            margin-top: 15px;
            font-size: 14px;
            color: #d1d5db;
            text-align: center;
            line-height: 1.5;
        }
        .scoreboard {
            width: 700px;
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 16px;
            font-weight: bold;
            color: #ffcc00;
        }
        #messageBox {
            position: absolute;
            top: 15px;
            width: 100%;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            z-index: 5;
        }
    </style>
</head>
<body>

    <div class="scoreboard">
        <div>⚽ Tỷ số (Bàn thắng): <span id="goals" style="color: #00ffcc;">0</span></div>
        <div>Lượt sút: <span id="shots">0</span> / 10</div>
        <div>Thủ môn cản phá: <span id="saves" style="color: #ff4d4d;">0</span></div>
    </div>

    <div id="gameContainer">
        <div id="messageBox"></div>

        <!-- Menu màn hình chờ -->
        <div id="menuOverlay">
            <div class="game-title">Penalty Shooters 2</div>
            <p style="color: #aaa; margin-bottom: 20px;">Sẵn sàng ghi bàn vào lưới đối thủ chưa?</p>
            <button class="play-btn" onclick="startGame()">Sút Penalty Ngay</button>
            <div class="controls-info">
                🎯 <b>Cách chơi:</b><br>
                • Nhấn chuột vào trong khung thành để chọn điểm sút bóng.<br>
                • Đánh lừa thủ môn để ghi điểm số cao nhất!
            </div>
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

        let gameRunning = false;
        let goals = 0;
        let shots = 0;
        let saves = 0;

        // Vị trí khung thành
        const goalRect = { x: 150, y: 70, width: 400, height: 180 };

        // Đối tượng bóng
        let ball = {
            x: 350,
            y: 390,
            radius: 12,
            targetX: 350,
            targetY: 390,
            speed: 8,
            isMoving: false
        };

        // Đối tượng thủ môn
        let keeper = {
            x: 350,
            y: 160,
            width: 50,
            height: 70,
            targetX: 350,
            speed: 6,
            diving: false
        };

        let targetIndicator = { x: -100, y: -100, alpha: 0 };
        let stateMessage = "";
        let messageTimer = 0;

        function startGame() {
            goals = 0;
            shots = 0;
            saves = 0;
            updateScoreboard();
            menuOverlay.style.display = "none";
            gameRunning = true;
            resetRound();
        }

        function updateScoreboard() {
            goalsEl.innerText = goals;
            shotsEl.innerText = shots;
            savesEl.innerText = saves;
        }

        function resetRound() {
            ball.x = 350;
            ball.y = 390;
            ball.isMoving = false;
            keeper.x = 350;
            keeper.targetX = 350;
            targetIndicator.alpha = 0;
        }

        // Bắt sự kiện click chuột để sút bóng
        canvas.addEventListener("click", (e) => {
            if (!gameRunning || ball.isMoving) return;

            const rect = canvas.getBoundingClientRect();
            let clickX = e.clientX - rect.left;
            let clickY = e.clientY - rect.top;

            // Kiểm tra click có trong khung thành không
            if (clickX >= goalRect.x && clickX <= goalRect.x + goalRect.width &&
                clickY >= goalRect.y && clickY <= goalRect.y + goalRect.height) {
                
                ball.targetX = clickX;
                ball.targetY = clickY;
                ball.isMoving = true;
                shots++;

                // Hiển thị tâm ngắm sút
                targetIndicator.x = clickX;
                targetIndicator.y = clickY;
                targetIndicator.alpha = 1.0;

                // Thủ môn chọn hướng ngẫu nhiên để bay người cản phá
                let randomOffset = (Math.random() - 0.5) * 220;
                keeper.targetX = Math.max(goalRect.x + 30, Math.min(goalRect.x + goalRect.width - 30, clickX + randomOffset));
            }
        });

        function update() {
            if (!gameRunning) return;

            if (ball.isMoving) {
                // Di chuyển bóng đến vị trí người chơi chọn
                let dx = ball.targetX - ball.x;
                let dy = ball.targetY - ball.y;
                let dist = Math.hypot(dx, dy);

                if (dist > 4) {
                    ball.x += (dx / dist) * ball.speed;
                    ball.y += (dy / dist) * ball.speed;
                } else {
                    // Bóng đã tới đích, kiểm tra kết quả sút
                    checkGoal();
                }
            }

            // Thủ môn di chuyển theo hướng dự đoán
            let kDx = keeper.targetX - keeper.x;
            if (Math.abs(kDx) > 2) {
                keeper.x += Math.sign(kDx) * keeper.speed;
            }

            if (messageTimer > 0) {
                messageTimer--;
                if (messageTimer === 0) messageBox.innerText = "";
            }
        }

        function checkGoal() {
            ball.isMoving = false;

            // Kiểm tra xem thủ môn có bắt được bóng không (khoảng cách giữa bóng và thủ môn)
            let distanceToKeeper = Math.hypot(ball.x - keeper.x, ball.y - keeper.y);

            if (distanceToKeeper < 45) {
                // Thủ môn cản phá thành công
                saves++;
                messageBox.innerText = "❌ THỦ MÔN CẢN PHÁ XUẤT SẮC!";
                messageBox.style.color = "#ff4d4d";
            } else {
                // Ghi bàn
                goals++;
                messageBox.innerText = "GOAL! ⚽ VÀO BÓN RẤT ĐẸP!";
                messageBox.style.color = "#00ffcc";
            }

            updateScoreboard();
            messageTimer = 90; // Hiện thông báo trong ~1.5 giây

            // Kiểm tra kết thúc 10 lượt sút
            if (shots >= 10) {
                gameRunning = false;
                setTimeout(() => {
                    menuOverlay.style.display = "flex";
                    document.querySelector(".game-title").innerText = "KẾT QUẢ TRẬN ĐẤU";
                    document.querySelector("#menuOverlay p").innerHTML = `Bạn ghi được <b>${goals}</b> / 10 bàn thắng!`;
                }, 1500);
            } else {
                setTimeout(resetRound, 1200);
            }
        }

        function draw() {
            // Xóa màn hình
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 1. Vẽ sân cỏ & vạch vôi
            ctx.fillStyle = "#1e4d2b";
            ctx.fillRect(0, 260, canvas.width, 220);

            ctx.strokeStyle = "white";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(100, 260); ctx.lineTo(350, 480); ctx.moveTo(600, 260); ctx.lineTo(350, 480);
            ctx.stroke();

            // 2. Vẽ Khung thành (Goal)
            ctx.strokeStyle = "white";
            ctx.lineWidth = 5;
            ctx.strokeRect(goalRect.x, goalRect.y, goalRect.width, goalRect.height);

            // Lưới khung thành
            ctx.strokeStyle = "rgba(255, 255, 255, 0.25)";
            ctx.lineWidth = 1;
            for (let x = goalRect.x; x <= goalRect.x + goalRect.width; x += 20) {
                ctx.beginPath(); ctx.moveTo(x, goalRect.y); ctx.lineTo(x, goalRect.y + goalRect.height); ctx.stroke();
            }
            for (let y = goalRect.y; y <= goalRect.y + goalRect.height; y += 20) {
                ctx.beginPath(); ctx.moveTo(goalRect.x, y); ctx.lineTo(goalRect.x + goalRect.width, y); ctx.stroke();
            }

            // 3. Vẽ Thủ môn (Goalkeeper mặc áo xanh sáng)
            ctx.fillStyle = "#00ffff";
            ctx.fillRect(keeper.x - keeper.width / 2, keeper.y, keeper.width, keeper.height);
            // Đầu thủ môn
            ctx.beginPath();
            ctx.arc(keeper.x, keeper.y - 12, 12, 0, Math.PI * 2);
            ctx.fillStyle = "#ffccaa";
            ctx.fill();
            // Găng tay thủ môn
            ctx.fillStyle = "white";
            ctx.fillRect(keeper.x - 25, keeper.y + 20, 10, 15);
            ctx.fillRect(keeper.x + 15, keeper.y + 20, 10, 15);

            // 4. Vẽ Tâm ngắm khi click chuột
            if (targetIndicator.alpha > 0) {
                ctx.strokeStyle = "red";
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.arc(targetIndicator.x, targetIndicator.y, 15, 0, Math.PI * 2);
                ctx.stroke();
                ctx.fillStyle = "rgba(255, 0, 0, 0.4)";
                ctx.fill();
            }

            // 5. Vẽ Quả bóng (Football)
            ctx.beginPath();
            ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
            ctx.fillStyle = "white";
            ctx.fill();
            ctx.strokeStyle = "black";
            ctx.lineWidth = 2;
            ctx.stroke();
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

# Hiển thị game trong ứng dụng Streamlit
components.html(game_html, height=560)

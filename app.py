import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(page_title="Đào Vàng Cổ Điển - Streamlit", page_icon="⛏️", layout="centered")

st.title("⛏️ ĐÀO VÀNG CỔ ĐIỂN")
st.caption("Game Đào Vàng huyền thoại - Móc lắc chậm dễ căn chỉnh, có hình ảnh người điều khiển!")

# Mã nguồn HTML, CSS và JS nâng cấp
game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #0d0e15;
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
            width: 750px;
            height: 500px;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 0 30px rgba(255, 204, 0, 0.3);
            border: 3px solid #b37400;
        }
        canvas {
            background: linear-gradient(to bottom, #d4a359 0%, #a66e28 20%, #734311 100%);
            display: block;
        }
        
        /* Overlay Menu */
        #menuOverlay {
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(20, 12, 5, 0.92);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 10;
        }

        .game-title {
            font-size: 50px;
            font-weight: 900;
            color: #ffcc00;
            text-shadow: 3px 3px 0 #b87900, 0 0 15px rgba(255, 204, 0, 0.6);
            margin: 0 0 10px 0;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .sub-title {
            color: #ffd699;
            font-size: 18px;
            margin-bottom: 25px;
        }

        .play-btn {
            padding: 15px 45px;
            font-size: 22px;
            font-weight: 800;
            text-transform: uppercase;
            color: #3d2200;
            background: linear-gradient(135deg, #ffcc00, #ff9900);
            border: none;
            border-radius: 40px;
            cursor: pointer;
            box-shadow: 0 0 25px rgba(255, 204, 0, 0.6);
            transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        .play-btn:hover {
            transform: scale(1.08);
            box-shadow: 0 0 35px rgba(255, 204, 0, 0.9);
            background: linear-gradient(135deg, #ffe066, #ffaa00);
        }

        .controls-hint {
            margin-top: 25px;
            font-size: 14px;
            color: #d9b382;
            text-align: center;
            line-height: 1.6;
        }

        /* Thanh thông số phía trên */
        #uiHeader {
            position: absolute;
            top: 0; left: 0; width: 100%;
            height: 50px;
            background: #e69900;
            border-bottom: 3px solid #805200;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
            box-sizing: border-box;
            font-weight: bold;
            font-size: 16px;
            color: #331a00;
            z-index: 5;
        }

        .stat-item span {
            color: #006600;
            font-size: 18px;
        }
        .stat-target span {
            color: #cc0000;
            font-size: 18px;
        }
    </style>
</head>
<body>

    <div id="gameContainer">
        <div id="uiHeader">
            <div>
                <div class="stat-item">Tiền: <span id="moneyText">$0</span></div>
                <div class="stat-target">Mục tiêu: <span id="targetText">$650</span></div>
            </div>
            <div style="text-align: center; font-size: 20px; color: #4d2600;">
                ⛏️ LÃO ĐÀO VÀNG ⛏️
            </div>
            <div style="text-align: right;">
                <div>Thời gian: <span id="timeText" style="color: #cc0000; font-size: 20px;">60</span>s</div>
                <div>Cấp độ: <span id="levelText" style="color: #003366;">1</span></div>
            </div>
        </div>

        <div id="menuOverlay">
            <h1 class="game-title">ĐÀO VÀNG CỔ ĐIỂN</h1>
            <div class="sub-title">Thu thập thật nhiều vàng để hoàn thành mục tiêu!</div>
            <button class="play-btn" onclick="startGame()">BẮT ĐẦU ĐÀO</button>
            <div class="controls-hint">
                🎮 <b>CÁCH CHƠI:</b><br>
                • Nhấn phím <b>MŨI TÊN XUỐNG (↓)</b> hoặc <b>DẤU CÁCH (SPACE)</b> để thả móc!<br>
                • Tốc độ móc lắc đã được chỉnh chậm lại dễ căn ngắm hơn.
            </div>
        </div>

        <canvas id="gameCanvas" width="750" height="500"></canvas>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const menuOverlay = document.getElementById("menuOverlay");
        const moneyText = document.getElementById("moneyText");
        const targetText = document.getElementById("targetText");
        const timeText = document.getElementById("timeText");
        const levelText = document.getElementById("levelText");

        let gameActive = false;
        let money = 0;
        let targetMoney = 650;
        let timeLeft = 60;
        let currentLevel = 1;
        let timerInterval = null;

        // Trạng thái móc đào
        const minerPos = { x: 375, y: 55 };
        const hook = {
            x: 375,
            y: 95,
            angle: 0,
            // ĐÃ GIẢM TỐC ĐỘ LẮC MÓC (Từ 0.03 xuống 0.015 giúp người chơi dễ nhắm)
            angleSpeed: 0.015,
            length: 40,
            state: 'swing', // 'swing', 'shoot', 'retract'
            // ĐÃ GIẢM TỐC ĐỘ THẢ MÓC (Từ 8 xuống 5.0)
            shootSpeed: 5.0,
            retractSpeed: 5.0,
            caughtItem: null
        };

        let items = [];
        let winchAngle = 0; // Xoay bánh xe tời quay cáp

        window.addEventListener("keydown", e => {
            if (["ArrowDown", "Space"].includes(e.code)) {
                e.preventDefault();
                if (gameActive && hook.state === 'swing') {
                    hook.state = 'shoot';
                }
            }
        });

        function startGame() {
            money = 0;
            currentLevel = 1;
            targetMoney = 650;
            setupLevel();
            menuOverlay.style.display = "none";
            gameActive = true;
        }

        function setupLevel() {
            timeLeft = 60;
            hook.state = 'swing';
            hook.length = 40;
            hook.caughtItem = null;
            updateUI();

            items = [];
            // Vàng lớn (3 cục)
            for (let i = 0; i < 3; i++) {
                items.push(createItem('gold', 28 + Math.random() * 8, 500, 1.8));
            }
            // Vàng vừa & nhỏ (5 cục)
            for (let i = 0; i < 5; i++) {
                items.push(createItem('gold', 14 + Math.random() * 6, 150, 4.0));
            }
            // Đá nặng (3 cục)
            for (let i = 0; i < 3; i++) {
                items.push(createItem('rock', 22 + Math.random() * 10, 20, 1.2));
            }

            clearInterval(timerInterval);
            timerInterval = setInterval(() => {
                if (gameActive) {
                    timeLeft--;
                    timeText.innerText = timeLeft;
                    if (timeLeft <= 0) {
                        checkLevelEnd();
                    }
                }
            }, 1000);
        }

        function createItem(type, radius, value, pullSpeed) {
            return {
                x: 60 + Math.random() * 630,
                y: 150 + Math.random() * 300,
                radius: radius,
                type: type,
                value: value,
                pullSpeed: pullSpeed,
                caught: false
            };
        }

        function updateUI() {
            moneyText.innerText = "$" + money;
            targetText.innerText = "$" + targetMoney;
            timeText.innerText = timeLeft;
            levelText.innerText = currentLevel;
        }

        function update() {
            if (!gameActive) return;

            // 1. Xoay móc (Tốc độ lắc đã chậm lại)
            if (hook.state === 'swing') {
                hook.angle += hook.angleSpeed;
                if (hook.angle > 1.3 || hook.angle < -1.3) {
                    hook.angleSpeed *= -1;
                }
                hook.x = minerPos.x + Math.sin(hook.angle) * hook.length;
                hook.y = minerPos.y + Math.cos(hook.angle) * hook.length;
            } 
            // 2. Thả móc xuống
            else if (hook.state === 'shoot') {
                hook.length += hook.shootSpeed;
                hook.x = minerPos.x + Math.sin(hook.angle) * hook.length;
                hook.y = minerPos.y + Math.cos(hook.angle) * hook.length;

                if (hook.x < 10 || hook.x > canvas.width - 10 || hook.y > canvas.height - 10) {
                    hook.state = 'retract';
                    hook.retractSpeed = 6;
                }

                items.forEach(item => {
                    if (!item.caught) {
                        let dist = Math.hypot(hook.x - item.x, hook.y - item.y);
                        if (dist < item.radius + 5) {
                            item.caught = true;
                            hook.caughtItem = item;
                            hook.state = 'retract';
                            hook.retractSpeed = item.pullSpeed;
                        }
                    }
                });
            } 
            // 3. Kéo móc lên
            else if (hook.state === 'retract') {
                hook.length -= hook.retractSpeed;
                hook.x = minerPos.x + Math.sin(hook.angle) * hook.length;
                hook.y = minerPos.y + Math.cos(hook.angle) * hook.length;
                
                winchAngle += 0.2; // Quay tay tời khi kéo

                if (hook.caughtItem) {
                    hook.caughtItem.x = hook.x;
                    hook.caughtItem.y = hook.y + hook.caughtItem.radius / 2;
                }

                if (hook.length <= 40) {
                    hook.length = 40;
                    hook.state = 'swing';
                    if (hook.caughtItem) {
                        money += hook.caughtItem.value;
                        items = items.filter(i => i !== hook.caughtItem);
                        hook.caughtItem = null;
                        updateUI();
                    }
                }
            }
        }

        function checkLevelEnd() {
            clearInterval(timerInterval);
            if (money >= targetMoney) {
                currentLevel++;
                targetMoney += 700;
                alert("🎉 CHÚC MỪNG! BẠN ĐÃ ĐẠT MỤC TIÊU VÀ QUA MÀN!");
                setupLevel();
            } else {
                gameActive = false;
                setTimeout(() => {
                    menuOverlay.style.display = "flex";
                    document.querySelector(".game-title").innerText = "GAME OVER";
                    document.querySelector(".sub-title").innerHTML = `Bạn không đạt đủ chỉ tiêu <b>$${targetMoney}</b>!`;
                }, 300);
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 1. Mặt đất phía trên
            ctx.fillStyle = "#d49b4b";
            ctx.fillRect(0, 0, canvas.width, 60);

            // 2. Dây cáp
            ctx.strokeStyle = "#331a00";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(minerPos.x, minerPos.y);
            ctx.lineTo(hook.x, hook.y);
            ctx.stroke();

            // 3. VẼ NGƯỜI ĐIỀU KHIỂN LÃO ĐÀO VÀNG + CỔNG TỜI KÉO CÁP
            // - Xe/Khung tời kéo cáp
            ctx.fillStyle = "#663300";
            ctx.fillRect(minerPos.x - 25, minerPos.y - 12, 50, 14);
            
            // Bánh xe tời xoay
            ctx.fillStyle = "#402000";
            ctx.beginPath();
            ctx.arc(minerPos.x, minerPos.y - 5, 12, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = "#994d00";
            ctx.lineWidth = 3;
            ctx.stroke();

            // Tay quay tời
            let handleX = minerPos.x + Math.cos(winchAngle) * 12;
            let handleY = (minerPos.y - 5) + Math.sin(winchAngle) * 12;
            ctx.strokeStyle = "#ffcc00";
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(minerPos.x, minerPos.y - 5);
            ctx.lineTo(handleX, handleY);
            ctx.stroke();

            // - Lão đào vàng (Ông lão mũ vàng, râu trắng)
            let mx = minerPos.x - 15;
            let my = minerPos.y - 12;

            // Áo xanh
            ctx.fillStyle = "#0066cc";
            ctx.fillRect(mx - 18, my - 20, 22, 20);

            // Đầu & Mặt
            ctx.fillStyle = "#ffcc99";
            ctx.beginPath();
            ctx.arc(mx - 7, my - 26, 9, 0, Math.PI * 2);
            ctx.fill();

            // Bộ râu trắng đặc trưng của lão đào vàng
            ctx.fillStyle = "#ffffff";
            ctx.beginPath();
            ctx.arc(mx - 7, my - 22, 8, 0, Math.PI);
            ctx.fill();

            // Mũ bảo hộ vàng
            ctx.fillStyle = "#ffcc00";
            ctx.fillRect(mx - 18, my - 36, 22, 8);
            ctx.beginPath();
            ctx.arc(mx - 7, my - 34, 11, Math.PI, 0);
            ctx.fill();

            // 4. Móc sắt (Lắc chậm)
            ctx.strokeStyle = "#444";
            ctx.lineWidth = 4;
            ctx.beginPath();
            ctx.arc(hook.x, hook.y, 8, hook.angle, hook.angle + Math.PI);
            ctx.stroke();

            if (!gameActive && menuOverlay.style.display !== "none") return;

            // 5. Vẽ Vàng & Đá
            items.forEach(item => {
                ctx.beginPath();
                ctx.arc(item.x, item.y, item.radius, 0, Math.PI * 2);

                if (item.type === 'gold') {
                    ctx.fillStyle = "#ffcc00";
                    ctx.shadowBlur = 10;
                    ctx.shadowColor = "#ffea80";
                    ctx.fill();
                    ctx.shadowBlur = 0;
                    ctx.strokeStyle = "#e69900";
                    ctx.lineWidth = 3;
                    ctx.stroke();
                } else {
                    ctx.fillStyle = "#808080";
                    ctx.fill();
                    ctx.strokeStyle = "#555555";
                    ctx.lineWidth = 3;
                    ctx.stroke();
                }
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

# Hiển thị Game trên ứng dụng Streamlit
components.html(game_html, height=540)

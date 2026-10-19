import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(page_title="Đào Vàng Cổ Điển - Streamlit", page_icon="⛏️", layout="centered")

st.title("⛏️ ĐÀO VÀNG CỔ ĐIỂN")
st.caption("Game Đào Vàng huyền thoại - Hãy kéo thật nhiều vàng để đạt mục tiêu trước khi hết giờ!")

# Mã nguồn HTML, CSS và JS cho game Đào Vàng
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
                • Vàng to = nhiều tiền nhưng kéo chậm.<br>
                • Đá = nặng và ít tiền.
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
        const minerPos = { x: 375, y: 50 };
        const hook = {
            x: 375,
            y: 90,
            angle: 0,
            angleSpeed: 0.03,
            length: 40,
            state: 'swing', // 'swing', 'shoot', 'retract'
            shootSpeed: 8,
            retractSpeed: 8,
            caughtItem: null
        };

        let items = [];

        // Lắng nghe sự kiện bàn phím
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

            // Tạo danh sách Vàng & Đá ngẫu nhiên
            items = [];
            
            // Vàng lớn (3 cục)
            for (let i = 0; i < 3; i++) {
                items.push(createItem('gold', 28 + Math.random() * 8, 500, 2.5));
            }
            // Vàng vừa & nhỏ (5 cục)
            for (let i = 0; i < 5; i++) {
                items.push(createItem('gold', 14 + Math.random() * 6, 150, 5.5));
            }
            // Đá nặng (3 cục)
            for (let i = 0; i < 3; i++) {
                items.push(createItem('rock', 22 + Math.random() * 10, 20, 1.5));
            }

            // Đếm ngược thời gian
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

            // 1. Xoay móc
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

                // Kiểm tra va chạm với viền canvas
                if (hook.x < 10 || hook.x > canvas.width - 10 || hook.y > canvas.height - 10) {
                    hook.state = 'retract';
                    hook.retractSpeed = 8;
                }

                // Kiểm tra va chạm với đồ vật
                items.forEach(item => {
                    if (!item.caught) {
                        let dist = Math.hypot(hook.x - item.x, hook.y - item.y);
                        if (dist < item.radius + 5) {
                            item.caught = true;
                            hook.caughtItem = item;
                            hook.state = 'retract';
                            hook.retractSpeed = item.pullSpeed; // Tốc độ kéo phụ thuộc vào độ nặng
                        }
                    }
                });
            } 
            // 3. Kéo móc lên
            else if (hook.state === 'retract') {
                hook.length -= hook.retractSpeed;
                hook.x = minerPos.x + Math.sin(hook.angle) * hook.length;
                hook.y = minerPos.y + Math.cos(hook.angle) * hook.length;

                if (hook.caughtItem) {
                    hook.caughtItem.x = hook.x;
                    hook.caughtItem.y = hook.y + hook.caughtItem.radius / 2;
                }

                // Móc đã về vị trí cũ
                if (hook.length <= 40) {
                    hook.length = 40;
                    hook.state = 'swing';
                    if (hook.caughtItem) {
                        money += hook.caughtItem.value;
                        // Xóa vật phẩm đã kéo lên
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

            // 1. Bầu trời / Mặt đất phía trên
            ctx.fillStyle = "#e6a338";
            ctx.fillRect(0, 0, canvas.width, 60);

            // 2. Dây cáp
            ctx.strokeStyle = "#331a00";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(minerPos.x, minerPos.y);
            ctx.lineTo(hook.x, hook.y);
            ctx.stroke();

            // 3. Lão đào vàng
            ctx.fillStyle = "#0066cc";
            ctx.fillRect(minerPos.x - 15, minerPos.y - 25, 30, 25);
            ctx.fillStyle = "#ffcc99";
            ctx.beginPath(); ctx.arc(minerPos.x, minerPos.y - 30, 10, 0, Math.PI * 2); ctx.fill(); // Đầu
            ctx.fillStyle = "white";
            ctx.beginPath(); ctx.arc(minerPos.x, minerPos.y - 26, 8, 0, Math.PI); ctx.fill(); // Râu

            // 4. Móc sắt
            ctx.strokeStyle = "#555";
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
                    // Vàng phát sáng
                    ctx.fillStyle = "#ffcc00";
                    ctx.shadowBlur = 10;
                    ctx.shadowColor = "#ffea80";
                    ctx.fill();
                    ctx.shadowBlur = 0;
                    ctx.strokeStyle = "#e69900";
                    ctx.lineWidth = 3;
                    ctx.stroke();
                } else {
                    // Đá màu xám
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

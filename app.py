import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(page_title="Đào Vàng Cổ Điển - Streamlit", page_icon="⛏️", layout="centered")

st.title("⛏️ ĐÀO VÀNG CỔ ĐIỂN")
st.caption("Game Đào Vàng huyền thoại - Móc sắt kim loại 3D cực đẹp, tốc độ lắc siêu êm và dễ căn ngắm!")

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
            box-shadow: 0 0 30px rgba(255, 204, 0, 0.4);
            border: 3px solid #b37400;
        }
        canvas {
            background: linear-gradient(to bottom, #d4a359 0%, #a66e28 20%, #61380e 100%);
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

        .stat-item span { color: #006600; font-size: 18px; }
        .stat-target span { color: #cc0000; font-size: 18px; }
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
                • Móc kẹp kim loại 3D thiết kế sắc nét, lắc chậm vừa tầm.
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

        const minerPos = { x: 375, y: 55 };
        const hook = {
            x: 375,
            y: 95,
            angle: 0,
            // ĐÃ GIẢM TỐC ĐỘ LẮC (Từ 0.015 xuống 0.011 - Lắc siêu đằm tay và dễ nhắm)
            angleSpeed: 0.011,
            length: 40,
            state: 'swing',
            // ĐÃ GIẢM TỐC ĐỘ THẢ MÓC (Từ 5.0 xuống 3.8 - Đi cực kỳ chuẩn xác)
            shootSpeed: 3.8,
            retractSpeed: 3.8,
            caughtItem: null
        };

        let items = [];
        let winchAngle = 0;

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
            // Vàng siêu to (2 cục)
            for (let i = 0; i < 2; i++) {
                items.push(createItem('gold', 32 + Math.random() * 6, 500, 1.4));
            }
            // Vàng vừa (4 cục)
            for (let i = 0; i < 4; i++) {
                items.push(createItem('gold', 20 + Math.random() * 5, 250, 2.8));
            }
            // Vàng nhỏ (3 cục)
            for (let i = 0; i < 3; i++) {
                items.push(createItem('gold', 12 + Math.random() * 4, 100, 4.2));
            }
            // Đá (3 cục)
            for (let i = 0; i < 3; i++) {
                items.push(createItem('rock', 22 + Math.random() * 8, 20, 1.0));
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
            let points = [];
            let numPoints = type === 'gold' ? 7 + Math.floor(Math.random() * 3) : 6;
            
            for (let i = 0; i < numPoints; i++) {
                let angle = (i / numPoints) * Math.PI * 2;
                let rOffset = radius * (0.85 + Math.random() * 0.3);
                points.push({
                    x: Math.cos(angle) * rOffset,
                    y: Math.sin(angle) * rOffset
                });
            }

            return {
                x: 70 + Math.random() * 610,
                y: 160 + Math.random() * 290,
                radius: radius,
                type: type,
                value: value,
                pullSpeed: pullSpeed,
                caught: false,
                points: points
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

            if (hook.state === 'swing') {
                hook.angle += hook.angleSpeed;
                if (hook.angle > 1.3 || hook.angle < -1.3) {
                    hook.angleSpeed *= -1;
                }
                hook.x = minerPos.x + Math.sin(hook.angle) * hook.length;
                hook.y = minerPos.y + Math.cos(hook.angle) * hook.length;
            } 
            else if (hook.state === 'shoot') {
                hook.length += hook.shootSpeed;
                hook.x = minerPos.x + Math.sin(hook.angle) * hook.length;
                hook.y = minerPos.y + Math.cos(hook.angle) * hook.length;

                if (hook.x < 10 || hook.x > canvas.width - 10 || hook.y > canvas.height - 10) {
                    hook.state = 'retract';
                    hook.retractSpeed = 5;
                }

                items.forEach(item => {
                    if (!item.caught) {
                        let dist = Math.hypot(hook.x - item.x, hook.y - item.y);
                        if (dist < item.radius + 6) {
                            item.caught = true;
                            hook.caughtItem = item;
                            hook.state = 'retract';
                            hook.retractSpeed = item.pullSpeed;
                        }
                    }
                });
            } 
            else if (hook.state === 'retract') {
                hook.length -= hook.retractSpeed;
                hook.x = minerPos.x + Math.sin(hook.angle) * hook.length;
                hook.y = minerPos.y + Math.cos(hook.angle) * hook.length;
                
                winchAngle += 0.15;

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

            // 1. Mặt đất
            ctx.fillStyle = "#d49b4b";
            ctx.fillRect(0, 0, canvas.width, 60);

            // 2. Dây cáp
            ctx.strokeStyle = "#331a00";
            ctx.lineWidth = 2.5;
            ctx.beginPath();
            ctx.moveTo(minerPos.x, minerPos.y);
            ctx.lineTo(hook.x, hook.y);
            ctx.stroke();

            // 3. Người điều khiển & Khung tời
            ctx.fillStyle = "#663300";
            ctx.fillRect(minerPos.x - 25, minerPos.y - 12, 50, 14);
            
            ctx.fillStyle = "#402000";
            ctx.beginPath();
            ctx.arc(minerPos.x, minerPos.y - 5, 12, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = "#994d00";
            ctx.lineWidth = 3;
            ctx.stroke();

            let handleX = minerPos.x + Math.cos(winchAngle) * 12;
            let handleY = (minerPos.y - 5) + Math.sin(winchAngle) * 12;
            ctx.strokeStyle = "#ffcc00";
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(minerPos.x, minerPos.y - 5);
            ctx.lineTo(handleX, handleY);
            ctx.stroke();

            let mx = minerPos.x - 15;
            let my = minerPos.y - 12;

            ctx.fillStyle = "#0066cc";
            ctx.fillRect(mx - 18, my - 20, 22, 20);

            ctx.fillStyle = "#ffcc99";
            ctx.beginPath();
            ctx.arc(mx - 7, my - 26, 9, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = "#ffffff";
            ctx.beginPath();
            ctx.arc(mx - 7, my - 22, 8, 0, Math.PI);
            ctx.fill();

            ctx.fillStyle = "#ffcc00";
            ctx.fillRect(mx - 18, my - 36, 22, 8);
            ctx.beginPath();
            ctx.arc(mx - 7, my - 34, 11, Math.PI, 0);
            ctx.fill();

            // 4. VẼ MÓC KẸP SẮT KIM LOẠI 3D SẮC NÉT (3D METALLIC CLAW)
            ctx.save();
            ctx.translate(hook.x, hook.y);
            ctx.rotate(-hook.angle); // Xoay móc theo hướng cáp

            // Khớp nối tròn phía trên móc
            ctx.fillStyle = "#666";
            ctx.beginPath();
            ctx.arc(0, 0, 5, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = "#222";
            ctx.lineWidth = 1.5;
            ctx.stroke();

            // Hai càng kẹp kim loại uốn cong 3D
            let clawOpen = hook.caughtItem ? 0.2 : 0.5; // Kẹp chặt lại khi gắp được đồ

            // Càng kẹp bên trái
            ctx.fillStyle = "#888";
            ctx.beginPath();
            ctx.moveTo(-3, 0);
            ctx.quadraticCurveTo(-15, 12, -8, 22);
            ctx.quadraticCurveTo(-2, 25, 0, 18);
            ctx.quadraticCurveTo(-5, 10, -3, 0);
            ctx.fill();
            ctx.strokeStyle = "#222";
            ctx.lineWidth = 1.5;
            ctx.stroke();

            // Càng kẹp bên phải
            ctx.beginPath();
            ctx.moveTo(3, 0);
            ctx.quadraticCurveTo(15, 12, 8, 22);
            ctx.quadraticCurveTo(2, 25, 0, 18);
            ctx.quadraticCurveTo(5, 10, 3, 0);
            ctx.fill();
            ctx.stroke();

            // Vệt kim loại phát sáng trên càng kẹp
            ctx.fillStyle = "rgba(255, 255, 255, 0.6)";
            ctx.fillRect(-8, 8, 2, 8);
            ctx.fillRect(6, 8, 2, 8);

            ctx.restore();

            if (!gameActive && menuOverlay.style.display !== "none") return;

            // 5. VẼ VÀNG 3D VÀ ĐÁ
            items.forEach(item => {
                ctx.save();
                ctx.translate(item.x, item.y);

                if (item.type === 'gold') {
                    let goldGrad = ctx.createRadialGradient(-item.radius*0.3, -item.radius*0.3, item.radius*0.1, 0, 0, item.radius);
                    goldGrad.addColorStop(0, "#fffae6");
                    goldGrad.addColorStop(0.3, "#ffd700");
                    goldGrad.addColorStop(0.8, "#ffaa00");
                    goldGrad.addColorStop(1, "#b37700");

                    ctx.shadowColor = "rgba(255, 215, 0, 0.6)";
                    ctx.shadowBlur = 12;

                    ctx.beginPath();
                    ctx.moveTo(item.points[0].x, item.points[0].y);
                    for (let i = 1; i < item.points.length; i++) {
                        ctx.lineTo(item.points[i].x, item.points[i].y);
                    }
                    ctx.closePath();
                    ctx.fillStyle = goldGrad;
                    ctx.fill();

                    ctx.shadowBlur = 0;
                    ctx.strokeStyle = "#e69900";
                    ctx.lineWidth = 2;
                    ctx.stroke();

                    ctx.strokeStyle = "rgba(255, 255, 255, 0.4)";
                    ctx.lineWidth = 1.5;
                    ctx.beginPath();
                    ctx.moveTo(item.points[0].x * 0.5, item.points[0].y * 0.5);
                    ctx.lineTo(item.points[2].x * 0.5, item.points[2].y * 0.5);
                    ctx.stroke();

                    ctx.fillStyle = "rgba(255, 255, 255, 0.6)";
                    ctx.beginPath();
                    ctx.arc(-item.radius * 0.3, -item.radius * 0.3, item.radius * 0.22, 0, Math.PI * 2);
                    ctx.fill();
                } else {
                    let rockGrad = ctx.createRadialGradient(-item.radius*0.3, -item.radius*0.3, item.radius*0.1, 0, 0, item.radius);
                    rockGrad.addColorStop(0, "#b3b3b3");
                    rockGrad.addColorStop(0.7, "#666666");
                    rockGrad.addColorStop(1, "#333333");

                    ctx.beginPath();
                    ctx.moveTo(item.points[0].x, item.points[0].y);
                    for (let i = 1; i < item.points.length; i++) {
                        ctx.lineTo(item.points[i].x, item.points[i].y);
                    }
                    ctx.closePath();
                    ctx.fillStyle = rockGrad;
                    ctx.fill();
                    ctx.strokeStyle = "#262626";
                    ctx.lineWidth = 2;
                    ctx.stroke();
                }

                ctx.restore();
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

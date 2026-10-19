import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(page_title="Level Devil - Streamlit Edition", page_icon="😈", layout="centered")

st.title("😈 LEVEL DEVIL")
st.caption("Game Platformer Troll kinh điển - Hãy cẩn thận với những cái bẫy bất ngờ!")

# Mã nguồn HTML, CSS và JS cho game Level Devil
game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #111;
            color: white;
            font-family: 'Courier New', Courier, monospace;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            user-select: none;
        }
        #gameContainer {
            position: relative;
            width: 800px;
            height: 450px;
            box-shadow: 0 0 20px rgba(255, 68, 0, 0.4);
            border-radius: 8px;
            overflow: hidden;
        }
        canvas {
            background-color: #e58229;
            display: block;
        }
        
        /* Overlay Menu giống hệt ảnh mẫu */
        #menuOverlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: #e58229;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            z-index: 10;
        }

        .title-container {
            width: 100%;
            background-color: #791c0e;
            padding: 25px 0;
            text-align: center;
            position: relative;
            border-bottom: 8px solid #c24b17;
        }

        .game-title {
            font-size: 56px;
            font-weight: 900;
            color: #ee5b28;
            letter-spacing: 4px;
            text-shadow: 3px 3px 0px #380a04;
            margin: 0;
            text-transform: uppercase;
        }

        /* Dãy hình răng cưa lửa/gai dưới menu */
        .fire-teeth {
            width: 100%;
            height: 20px;
            background: repeating-linear-gradient(
                -45deg,
                #c24b17,
                #c24b17 10px,
                #e58229 10px,
                #e58229 20px
            );
            margin-bottom: 40px;
        }

        .btn-container {
            display: flex;
            gap: 40px;
            margin-top: 20px;
        }

        .mode-btn {
            width: 130px;
            height: 140px;
            background-color: #ffda66;
            border: 4px solid #791c0e;
            border-radius: 6px;
            cursor: pointer;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            padding: 0;
            box-shadow: 0 6px 0px #791c0e;
            transition: transform 0.1s, box-shadow 0.1s;
        }

        .mode-btn.two-p {
            background-color: #eb8f85;
        }

        .mode-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 9px 0px #791c0e;
        }

        .mode-btn:active {
            transform: translateY(3px);
            box-shadow: 0 3px 0px #791c0e;
        }

        .btn-icon {
            flex-grow: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        .player-sprite {
            width: 24px;
            height: 38px;
            background-color: #2b1d1d;
            border-radius: 4px 4px 0 0;
            position: relative;
        }
        .player-sprite.p2 {
            background-color: #8b2b2b;
        }

        .btn-label {
            width: 100%;
            background-color: #b83a21;
            color: #ffda66;
            font-size: 18px;
            font-weight: bold;
            padding: 6px 0;
            text-align: center;
            border-top: 3px solid #791c0e;
        }

        .mode-btn.two-p .btn-label {
            background-color: #791c0e;
            color: #eb8f85;
        }

        #uiHeader {
            position: absolute;
            top: 10px;
            left: 15px;
            right: 15px;
            display: flex;
            justify-content: space-between;
            font-size: 20px;
            font-weight: bold;
            color: #380a04;
            z-index: 5;
            pointer-events: none;
        }
    </style>
</head>
<body>

    <div id="gameContainer">
        <div id="uiHeader">
            <div id="levelText">LEVEL 1</div>
            <div id="deathText">DEATHS: 0</div>
        </div>

        <!-- Menu overlay khớp 100% hình ảnh -->
        <div id="menuOverlay">
            <div class="title-container">
                <h1 class="game-title">LEVEL DEVIL</h1>
            </div>
            <div class="fire-teeth"></div>

            <div class="btn-container">
                <div class="mode-btn" onclick="selectMode(1)">
                    <div class="btn-icon">
                        <div class="player-sprite"></div>
                    </div>
                    <div class="btn-label">1 Player</div>
                </div>

                <div class="mode-btn two-p" onclick="selectMode(2)">
                    <div class="btn-icon">
                        <div class="player-sprite p2"></div>
                        <div class="player-sprite"></div>
                    </div>
                    <div class="btn-label">2 Player</div>
                </div>
            </div>
        </div>

        <canvas id="gameCanvas" width="800" height="450"></canvas>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const menuOverlay = document.getElementById("menuOverlay");
        const levelText = document.getElementById("levelText");
        const deathText = document.getElementById("deathText");

        let gameMode = 1; // 1 hoặc 2 người chơi
        let currentLevel = 1;
        let totalDeaths = 0;
        let gameActive = false;

        // Bàn phím
        const keys = {};
        window.addEventListener("keydown", e => {
            keys[e.code] = true;
            if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "Space", "KeyW", "KeyA", "KeyS", "KeyD"].includes(e.code)) {
                e.preventDefault();
            }
        });
        window.addEventListener("keyup", e => { keys[e.code] = false; });

        // Cấu trúc nhân vật
        class Player {
            constructor(x, y, color, controls) {
                this.spawnX = x;
                this.spawnY = y;
                this.x = x;
                this.y = y;
                this.width = 24;
                this.height = 36;
                this.vx = 0;
                this.vy = 0;
                this.color = color;
                this.controls = controls; // {left, right, jump}
                this.isGrounded = false;
                this.alive = true;
            }

            reset() {
                this.x = this.spawnX;
                this.y = this.spawnY;
                this.vx = 0;
                this.vy = 0;
                this.isGrounded = false;
                this.alive = true;
            }

            update(platforms, hazards) {
                if (!this.alive) return;

                // Điều khiển di chuyển
                if (keys[this.controls.left]) this.vx = -4;
                else if (keys[this.controls.right]) this.vx = 4;
                else this.vx = 0;

                // Nhảy
                if (keys[this.controls.jump] && this.isGrounded) {
                    this.vy = -9.5;
                    this.isGrounded = false;
                }

                // Trọng lực
                this.vy += 0.5;

                // Cập nhật vị trí X & Va chạm
                this.x += this.vx;
                platforms.forEach(p => {
                    if (checkCollision(this, p)) {
                        if (this.vx > 0) this.x = p.x - this.width;
                        else if (this.vx < 0) this.x = p.x + p.w;
                    }
                });

                // Cập nhật vị trí Y & Va chạm
                this.y += this.vy;
                this.isGrounded = false;
                platforms.forEach(p => {
                    if (checkCollision(this, p)) {
                        if (this.vy > 0) {
                            this.y = p.y - this.height;
                            this.vy = 0;
                            this.isGrounded = true;
                        } else if (this.vy < 0) {
                            this.y = p.y + p.h;
                            this.vy = 0;
                        }
                    }
                });

                // Kiểm tra va chạm với bẫy / rớt ra ngoài
                if (this.y > canvas.height + 50) this.die();

                hazards.forEach(h => {
                    if (checkCollision(this, h)) this.die();
                });
            }

            die() {
                if (!this.alive) return;
                this.alive = false;
                totalDeaths++;
                deathText.innerText = `DEATHS: ${totalDeaths}`;
                setTimeout(() => resetCurrentLevel(), 300);
            }

            draw() {
                if (!this.alive) return;
                ctx.fillStyle = this.color;
                ctx.fillRect(this.x, this.y, this.width, this.height);
                
                // Vẽ mắt
                ctx.fillStyle = "#fff";
                ctx.fillRect(this.x + (this.vx >= 0 ? 14 : 4), this.y + 8, 5, 5);
            }
        }

        // Kiểm tra va chạm AABB
        function checkCollision(a, b) {
            return a.x < b.x + b.w &&
                   a.x + a.width > b.x &&
                   a.y < b.y + b.h &&
                   a.y + a.height > b.y;
        }

        // Định nghĩa các level & hiệu ứng TROLL đặc trưng của Level Devil
        let players = [];
        let platforms = [];
        let hazards = [];
        let door = { x: 0, y: 0, w: 32, h: 48 };

        function loadLevel(lvl) {
            currentLevel = lvl;
            levelText.innerText = `LEVEL ${currentLevel}`;
            platforms = [];
            hazards = [];

            if (lvl === 1) {
                // LEVEL 1: Cửa tự động dịch chuyển xa ra khi lại gần
                door = { x: 700, y: 312, w: 32, h: 48, defaultX: 700 };
                platforms = [
                    { x: 50, y: 360, w: 200, h: 40 },
                    { x: 300, y: 360, w: 200, h: 40 },
                    { x: 550, y: 360, w: 200, h: 40 }
                ];
            } else if (lvl === 2) {
                // LEVEL 2: Đất sụt lở bất ngờ khi đi qua
                door = { x: 700, y: 312, w: 32, h: 48 };
                platforms = [
                    { x: 50, y: 360, w: 180, h: 40 },
                    { x: 280, y: 360, w: 240, h: 40, isTrap: true, triggered: false }, // Đất biến mất
                    { x: 580, y: 360, w: 170, h: 40 }
                ];
            } else if (lvl === 3) {
                // LEVEL 3: Cọc nhọn bất ngờ nhô lên
                door = { x: 720, y: 312, w: 32, h: 48 };
                platforms = [
                    { x: 50, y: 360, w: 700, h: 40 }
                ];
                hazards = [
                    { x: 380, y: 400, w: 40, h: 30, targetY: 330, isSpikeTrap: true }
                ];
            }

            // Khởi tạo người chơi
            if (gameMode === 1) {
                players = [
                    new Player(80, 300, "#2b1d1d", { left: "ArrowLeft", right: "ArrowRight", jump: "ArrowUp" })
                ];
            } else {
                players = [
                    new Player(80, 300, "#2b1d1d", { left: "ArrowLeft", right: "ArrowRight", jump: "ArrowUp" }),
                    new Player(120, 300, "#8b2b2b", { left: "KeyA", right: "KeyD", jump: "KeyW" })
                ];
            }
        }

        function selectMode(mode) {
            gameMode = mode;
            menuOverlay.style.display = "none";
            gameActive = true;
            totalDeaths = 0;
            deathText.innerText = `DEATHS: 0`;
            loadLevel(1);
        }

        function resetCurrentLevel() {
            loadLevel(currentLevel);
        }

        function update() {
            if (!gameActive) return;

            players.forEach(p => p.update(platforms, hazards));

            // TROLL MECHANICS DỰA TRÊN LEVEL
            if (currentLevel === 1) {
                // Nếu người chơi lại gần cửa, cửa tự dịch chuyển sang phải
                players.forEach(p => {
                    if (Math.abs(p.x - door.x) < 100 && door.x < 740) {
                        door.x += 3;
                    }
                });
            } else if (currentLevel === 2) {
                // Bẫy đất sụt biến mất
                platforms.forEach((p, idx) => {
                    if (p.isTrap) {
                        players.forEach(player => {
                            if (player.x > p.x && player.x < p.x + p.w) {
                                p.y += 8; // Sụt hố xuống dưới
                            }
                        });
                    }
                });
            } else if (currentLevel === 3) {
                // Bẫy chông nhô lên bất ngờ
                hazards.forEach(h => {
                    if (h.isSpikeTrap) {
                        players.forEach(p => {
                            if (Math.abs(p.x - h.x) < 120 && h.y > h.targetY) {
                                h.y -= 5;
                            }
                        });
                    }
                });
            }

            // Kiểm tra thắng level (khi tất cả người chơi sống sót chạm cửa)
            let alivePlayers = players.filter(p => p.alive);
            if (alivePlayers.length > 0) {
                let allReachedDoor = alivePlayers.every(p => checkCollision(p, door));
                if (allReachedDoor) {
                    if (currentLevel < 3) {
                        loadLevel(currentLevel + 1);
                    } else {
                        alert("🎉 CHÚC MỪNG BẠN ĐÃ VƯỢT QUA LEVEL DEVIL!");
                        menuOverlay.style.display = "flex";
                        gameActive = false;
                    }
                }
            }
        }

        function draw() {
            // Nền cam ấm áp của Level Devil
            ctx.fillStyle = "#e58229";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            if (!gameActive) return;

            // Vẽ sàn / Platforms
            ctx.fillStyle = "#791c0e";
            platforms.forEach(p => {
                ctx.fillRect(p.x, p.y, p.w, p.h);
            });

            // Vẽ bẫy chông
            ctx.fillStyle = "#222";
            hazards.forEach(h => {
                ctx.beginPath();
                ctx.moveTo(h.x, h.y + h.h);
                ctx.lineTo(h.x + h.w / 2, h.y);
                ctx.lineTo(h.x + h.w, h.y + h.h);
                ctx.fill();
            });

            // Vẽ Cửa hoàn thành (Door)
            ctx.fillStyle = "#380a04";
            ctx.fillRect(door.x, door.y, door.w, door.h);
            ctx.fillStyle = "#ffda66";
            ctx.fillRect(door.x + 4, door.y + 4, door.w - 8, door.h - 8);

            // Vẽ người chơi
            players.forEach(p => p.draw());
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

# Hiển thị Game lên ứng dụng Streamlit
components.html(game_html, height=500)

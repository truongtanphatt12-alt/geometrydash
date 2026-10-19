import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(page_title="Level Devil - Streamlit Edition", page_icon="😈", layout="centered")

st.title("😈 LEVEL DEVIL")
st.caption("Game Platformer Troll kinh điển - Tốc độ mượt mà, Cấp độ khó tăng dần!")

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
        
        /* Overlay Menu */
        #menuOverlay {
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
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
            margin-bottom: 30px;
        }

        .btn-container {
            display: flex;
            gap: 40px;
            margin-top: 10px;
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

        .mode-btn.two-p { background-color: #eb8f85; }

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

        .player-preview {
            width: 24px;
            height: 34px;
            background-color: #222;
            border-radius: 6px 6px 2px 2px;
            position: relative;
        }
        .player-preview.p2 { background-color: #a32222; }

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
            top: 12px; left: 20px; right: 20px;
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

        <div id="menuOverlay">
            <div class="title-container">
                <h1 class="game-title">LEVEL DEVIL</h1>
            </div>
            <div class="fire-teeth"></div>

            <div class="btn-container">
                <div class="mode-btn" onclick="selectMode(1)">
                    <div class="btn-icon">
                        <div class="player-preview"></div>
                    </div>
                    <div class="btn-label">1 Player</div>
                </div>

                <div class="mode-btn two-p" onclick="selectMode(2)">
                    <div class="btn-icon">
                        <div class="player-preview p2"></div>
                        <div class="player-preview"></div>
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

        let gameMode = 1;
        let currentLevel = 1;
        let totalDeaths = 0;
        let gameActive = false;

        const keys = {};
        window.addEventListener("keydown", e => {
            keys[e.code] = true;
            if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "Space", "KeyW", "KeyA", "KeyS", "KeyD"].includes(e.code)) {
                e.preventDefault();
            }
        });
        window.addEventListener("keyup", e => { keys[e.code] = false; });

        // LỚP NHÂN VẬT ĐƯỢC CHỈNH TỐC ĐỘ VÀ ĐỒ HỌA MỚI
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
                this.controls = controls;
                this.isGrounded = false;
                this.alive = true;
                this.facing = 1; // 1: Phải, -1: Trái
                this.animTimer = 0;
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

                // GIẢM TỐC ĐỘ CHẠY LẠI (Từ 4.0 xuống 2.8) giúp điều khiển đằm tay hơn
                const moveSpeed = 2.8; 
                if (keys[this.controls.left]) {
                    this.vx = -moveSpeed;
                    this.facing = -1;
                } else if (keys[this.controls.right]) {
                    this.vx = moveSpeed;
                    this.facing = 1;
                } else {
                    this.vx = 0;
                }

                // GIẢM LỰC NHẢY (Từ -9.5 xuống -8.2) để dễ nhảy chính xác hơn
                if (keys[this.controls.jump] && this.isGrounded) {
                    this.vy = -8.2;
                    this.isGrounded = false;
                }

                // Trọng lực êm hơn
                this.vy += 0.42;

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

                if (this.y > canvas.height + 50) this.die();

                hazards.forEach(h => {
                    if (checkCollision(this, h)) this.die();
                });

                this.animTimer += Math.abs(this.vx);
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

                // 1. Thân nhân vật (Bo góc)
                ctx.fillStyle = this.color;
                ctx.beginPath();
                ctx.roundRect(this.x, this.y, this.width, this.height, [6, 6, 2, 2]);
                ctx.fill();

                // 2. Hai sừng quỷ nhỏ trên đầu
                ctx.fillStyle = "#380a04";
                ctx.beginPath();
                ctx.moveTo(this.x + 4, this.y);
                ctx.lineTo(this.x + 1, this.y - 5);
                ctx.lineTo(this.x + 8, this.y);
                ctx.fill();

                ctx.beginPath();
                ctx.moveTo(this.x + this.width - 8, this.y);
                ctx.lineTo(this.x + this.width - 1, this.y - 5);
                ctx.lineTo(this.x + this.width - 4, this.y);
                ctx.fill();

                // 3. Mắt nhân vật (Di chuyển theo hướng đi)
                ctx.fillStyle = "#ffffff";
                let eyeOffsetX = this.facing === 1 ? 11 : 3;
                ctx.fillRect(this.x + eyeOffsetX, this.y + 7, 5, 6);
                ctx.fillRect(this.x + eyeOffsetX + 6, this.y + 7, 5, 6);

                ctx.fillStyle = "#000000";
                let pupilX = this.facing === 1 ? 3 : 0;
                ctx.fillRect(this.x + eyeOffsetX + pupilX, this.y + 9, 2, 3);
                ctx.fillRect(this.x + eyeOffsetX + 6 + pupilX, this.y + 9, 2, 3);

                // 4. Chân nhúc nhích khi di chuyển
                ctx.fillStyle = "#111";
                let legOffset = Math.sin(this.animTimer * 0.2) * 3;
                if (this.isGrounded && this.vx !== 0) {
                    ctx.fillRect(this.x + 3, this.y + this.height, 5, 3 + legOffset);
                    ctx.fillRect(this.x + this.width - 8, this.y + this.height, 5, 3 - legOffset);
                } else {
                    ctx.fillRect(this.x + 4, this.y + this.height, 4, 3);
                    ctx.fillRect(this.x + this.width - 8, this.y + this.height, 4, 3);
                }
            }
        }

        function checkCollision(a, b) {
            return a.x < b.x + b.w &&
                   a.x + a.width > b.x &&
                   a.y < b.y + b.h &&
                   a.y + a.height > b.y;
        }

        let players = [];
        let platforms = [];
        let hazards = [];
        let door = { x: 0, y: 0, w: 32, h: 48 };

        // QUẢN LÝ 5 CẤP ĐỘ KHÓ TĂNG DẦN
        function loadLevel(lvl) {
            currentLevel = lvl;
            levelText.innerText = `LEVEL ${currentLevel}`;
            platforms = [];
            hazards = [];

            if (lvl === 1) {
                // LEVEL 1 (Dễ): Cửa ra vào nhích nhẹ ra xa
                door = { x: 700, y: 312, w: 32, h: 48 };
                platforms = [
                    { x: 50, y: 360, w: 700, h: 40 }
                ];
            } else if (lvl === 2) {
                // LEVEL 2 (Vừa): Bẫy cọc nhọn nhô lên
                door = { x: 700, y: 312, w: 32, h: 48 };
                platforms = [
                    { x: 50, y: 360, w: 250, h: 40 },
                    { x: 300, y: 360, w: 450, h: 40 }
                ];
                hazards = [
                    { x: 420, y: 400, w: 30, h: 30, targetY: 330, isSpike: true }
                ];
            } else if (lvl === 3) {
                // LEVEL 3 (Khó hơn): Sàn bị rớt khi giậm lên
                door = { x: 700, y: 312, w: 32, h: 48 };
                platforms = [
                    { x: 50, y: 360, w: 200, h: 40 },
                    { x: 290, y: 360, w: 200, h: 40, isFalling: true },
                    { x: 530, y: 360, w: 220, h: 40 }
                ];
            } else if (lvl === 4) {
                // LEVEL 4 (Rất khó): Khối trần hạ xuống đè chết
                door = { x: 710, y: 312, w: 32, h: 48 };
                platforms = [
                    { x: 50, y: 360, w: 700, h: 40 },
                    { x: 350, y: -100, w: 120, h: 200, isCrusher: true, targetY: 160 } // Trần sụt
                ];
            } else if (lvl === 5) {
                // LEVEL 5 (Siêu Troll): Cửa di chuyển + Sàn đứt đoạn
                door = { x: 680, y: 312, w: 32, h: 48 };
                platforms = [
                    { x: 50, y: 360, w: 180, h: 40 },
                    { x: 270, y: 360, w: 180, h: 40, isFalling: true },
                    { x: 490, y: 360, w: 260, h: 40 }
                ];
                hazards = [
                    { x: 540, y: 400, w: 30, h: 30, targetY: 330, isSpike: true }
                ];
            }

            // Khởi tạo vị trí Người chơi
            if (gameMode === 1) {
                players = [
                    new Player(80, 300, "#222222", { left: "ArrowLeft", right: "ArrowRight", jump: "ArrowUp" })
                ];
            } else {
                players = [
                    new Player(70, 300, "#222222", { left: "ArrowLeft", right: "ArrowRight", jump: "ArrowUp" }),
                    new Player(110, 300, "#a32222", { left: "KeyA", right: "KeyD", jump: "KeyW" })
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

            // TROLL MECHANICS THEO CẤP ĐỘ
            if (currentLevel === 1) {
                players.forEach(p => {
                    if (Math.abs(p.x - door.x) < 80 && door.x < 740) {
                        door.x += 1.8; // Cửa nhích ra xa vừa phải
                    }
                });
            } else if (currentLevel === 2) {
                hazards.forEach(h => {
                    if (h.isSpike) {
                        players.forEach(p => {
                            if (Math.abs(p.x - h.x) < 100 && h.y > h.targetY) {
                                h.y -= 4; // Bẫy cọc trồi lên
                            }
                        });
                    }
                });
            } else if (currentLevel === 3) {
                platforms.forEach(p => {
                    if (p.isFalling) {
                        players.forEach(player => {
                            if (player.x > p.x - 10 && player.x < p.x + p.w) {
                                p.y += 6; // Sàn rớt xuống
                            }
                        });
                    }
                });
            } else if (currentLevel === 4) {
                platforms.forEach(p => {
                    if (p.isCrusher) {
                        players.forEach(player => {
                            if (player.x > p.x - 50 && p.y < p.targetY) {
                                p.y += 5; // Trần đè xuống
                            }
                        });
                    }
                });
            } else if (currentLevel === 5) {
                // Tối hợp cọc nhọn + sàn rớt + cửa di chuyển
                players.forEach(p => {
                    if (Math.abs(p.x - door.x) < 70 && door.x < 740) door.x += 1.5;
                });
                platforms.forEach(p => {
                    if (p.isFalling) {
                        players.forEach(player => {
                            if (player.x > p.x - 10 && player.x < p.x + p.w) p.y += 6;
                        });
                    }
                });
                hazards.forEach(h => {
                    if (h.isSpike) {
                        players.forEach(p => {
                            if (Math.abs(p.x - h.x) < 80 && h.y > h.targetY) h.y -= 4;
                        });
                    }
                });
            }

            // Kiểm tra hoàn thành Level
            let alivePlayers = players.filter(p => p.alive);
            if (alivePlayers.length > 0) {
                let allReachedDoor = alivePlayers.every(p => checkCollision(p, door));
                if (allReachedDoor) {
                    if (currentLevel < 5) {
                        loadLevel(currentLevel + 1);
                    } else {
                        alert("🎉 XIN CHÚC MỪNG! BẠN ĐÃ CHINH PHỤC THÀNH CÔNG LEVEL DEVIL!");
                        menuOverlay.style.display = "flex";
                        gameActive = false;
                    }
                }
            }
        }

        function draw() {
            // Nền cam Level Devil
            ctx.fillStyle = "#e58229";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            if (!gameActive) return;

            // Sàn
            ctx.fillStyle = "#791c0e";
            platforms.forEach(p => {
                ctx.fillRect(p.x, p.y, p.w, p.h);
            });

            // Bẫy cọc nhọn
            ctx.fillStyle = "#222";
            hazards.forEach(h => {
                ctx.beginPath();
                ctx.moveTo(h.x, h.y + h.h);
                ctx.lineTo(h.x + h.w / 2, h.y);
                ctx.lineTo(h.x + h.w, h.y + h.h);
                ctx.fill();
            });

            // Cửa ra vào
            ctx.fillStyle = "#380a04";
            ctx.fillRect(door.x, door.y, door.w, door.h);
            ctx.fillStyle = "#ffda66";
            ctx.fillRect(door.x + 4, door.y + 4, door.w - 8, door.h - 8);

            // Nhân vật
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

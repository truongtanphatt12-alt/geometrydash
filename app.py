import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(page_title="Slither.io - Streamlit Edition", page_icon="🐍", layout="centered")

st.title("🐍 Slither.io Game")
st.write("Nhập tên người chơi và nhấn **Play Online** để bắt đầu chơi!")

# Nhập Nickname
nickname = st.text_input("Nickname:", value="Rắn Săn Mồi")

# Mã nguồn HTML/JS/CSS cho game Slither.io đơn giản
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
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}
        #gameCanvas {{
            background-color: #161923;
            border: 3px solid #4e5d78;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.8);
            cursor: crosshair;
        }}
        .score-board {{
            margin-top: 10px;
            font-size: 18px;
            font-weight: bold;
            color: #00ffcc;
        }}
    </style>
</head>
<body>

    <div class="score-board">
        Người chơi: <span id="playerName">{nickname}</span> | Điểm: <span id="score">0</span>
    </div>
    <br>
    <canvas id="gameCanvas" width="700" height="500"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const scoreEl = document.getElementById("score");

        let score = 0;
        let mouseX = canvas.width / 2;
        let mouseY = canvas.height / 2;

        // Rắn của người chơi
        let snake = {{
            x: canvas.width / 2,
            y: canvas.height / 2,
            radius: 12,
            speed: 3,
            body: [],
            length: 15
        }};

        // Khởi tạo các hạt thức ăn
        let foods = [];
        const numFoods = 60;
        const colors = ["#ff4d4d", "#333", "#33cc33", "#ffcc00", "#ff00ff", "#00ffff"];

        function createFood() {{
            return {{
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                radius: Math.random() * 4 + 3,
                color: colors[Math.floor(Math.random() * colors.length)]
            }};
        }}

        for (let i = 0; i < numFoods; i++) {{
            foods.push(createFood());
        }}

        // Theo dõi tọa độ chuột
        canvas.addEventListener("mousemove", (e) => {{
            const rect = canvas.getBoundingClientRect();
            mouseX = e.clientX - rect.left;
            mouseY = e.clientY - rect.top;
        }});

        // Cập nhật trạng thái game
        function update() {{
            // Tính góc di chuyển về phía chuột
            let dx = mouseX - snake.x;
            let dy = mouseY - snake.y;
            let angle = Math.atan2(dy, dx);
            let dist = Math.hypot(dx, dy);

            // Di chuyển đầu rắn nếu chuột ở khoảng cách nhất định
            if (dist > 5) {{
                snake.x += Math.cos(angle) * snake.speed;
                snake.y += Math.sin(angle) * snake.speed;
            }}

            // Giới hạn trong viền màn hình
            snake.x = Math.max(snake.radius, Math.min(canvas.width - snake.radius, snake.x));
            snake.y = Math.max(snake.radius, Math.min(canvas.height - snake.radius, snake.y));

            // Lưu lịch sử di chuyển cho thân rắn
            snake.body.unshift({{ x: snake.x, y: snake.y }});
            if (snake.body.length > snake.length) {{
                snake.body.pop();
            }}

            // Kiểm tra va chạm ăn thức ăn
            foods.forEach((food, index) => {{
                let fDx = snake.x - food.x;
                let fDy = snake.y - food.y;
                let fDist = Math.hypot(fDx, fDy);

                if (fDist < snake.radius + food.radius) {{
                    score += 10;
                    snake.length += 2;
                    scoreEl.innerText = score;
                    foods[index] = createFood(); // Tái tạo thức ăn mới
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
                ctx.beginPath();
                ctx.moveTo(x, 0);
                ctx.lineTo(x, canvas.height);
                ctx.stroke();
            }}
            for (let y = 0; y < canvas.height; y += 40) {{
                ctx.beginPath();
                ctx.moveTo(0, y);
                ctx.lineTo(canvas.width, y);
                ctx.stroke();
            }}

            // Vẽ thức ăn (phát sáng)
            foods.forEach(food => {{
                ctx.beginPath();
                ctx.arc(food.x, food.y, food.radius, 0, Math.PI * 2);
                ctx.fillStyle = food.color;
                ctx.shadowBlur = 10;
                ctx.shadowColor = food.color;
                ctx.fill();
                ctx.shadowBlur = 0;
            }});

            // Vẽ thân rắn
            for (let i = snake.body.length - 1; i >= 0; i--) {{
                let pt = snake.body[i];
                ctx.beginPath();
                ctx.arc(pt.x, pt.y, snake.radius - (i * 0.1 > 4 ? 4 : i * 0.1), 0, Math.PI * 2);
                ctx.fillStyle = i === 0 ? "#ff9900" : "#ffaa33";
                ctx.fill();
                ctx.strokeStyle = "#b35900";
                ctx.lineWidth = 1;
                ctx.stroke();
            }}

            // Vẽ mắt cho đầu rắn
            if (snake.body.length > 0) {{
                let head = snake.body[0];
                let dx = mouseX - head.x;
                let dy = mouseY - head.y;
                let angle = Math.atan2(dy, dx);

                let eyeOffset = 6;
                let eyeX1 = head.x + Math.cos(angle + 0.5) * eyeOffset;
                let eyeY1 = head.y + Math.sin(angle + 0.5) * eyeOffset;
                let eyeX2 = head.x + Math.cos(angle - 0.5) * eyeOffset;
                let eyeY2 = head.y + Math.sin(angle - 0.5) * eyeOffset;

                ctx.fillStyle = "white";
                ctx.beginPath(); ctx.arc(eyeX1, eyeY1, 3, 0, Math.PI * 2); ctx.fill();
                ctx.beginPath(); ctx.arc(eyeX2, eyeY2, 3, 0, Math.PI * 2); ctx.fill();

                ctx.fillStyle = "black";
                ctx.beginPath(); ctx.arc(eyeX1, eyeY1, 1.5, 0, Math.PI * 2); ctx.fill();
                ctx.beginPath(); ctx.arc(eyeX2, eyeY2, 1.5, 0, Math.PI * 2); ctx.fill();
            }}
        }}

        // Vòng lặp game
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

# Hiển thị Game lên ứng dụng Streamlit
components.html(game_html, height=600)

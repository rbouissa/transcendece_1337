# 🕹️ Transcendence

Transcendence is a full-stack multiplayer Pong game developed as part of the 1337/42 curriculum. It combines real-time gameplay with user authentication, profiles, leaderboards, and chat features — offering a complete social gaming experience on the web.

## 🚀 Tech Stack

### 🔧 Backend
- Node.js / NestJS (or Django if you used it)
- PostgreSQL
- WebSocket for real-time communication
- JWT & OAuth 2.0 authentication

### 🎨 Frontend
- React.js
- Tailwind CSS / Bootstrap
- Axios

### ⚙️ DevOps
- Docker / Docker Compose
- Nginx (for reverse proxy)
- Git, GitHub

## 🧩 Features

- 🧑‍🤝‍🧑 Real-time multiplayer Pong game
- 🔐 OAuth 2.0 login (e.g., 42 Intra)
- 🧾 JWT-secured sessions
- 👤 User profiles & avatars
- 🗣️ Private & global chat with WebSockets
- 🏆 Match history & leaderboard
- 🖼️ Responsive UI

## 🖥️ Setup Instructions

```bash
# Clone the repository
git clone https://github.com/your-username/transcendence.git
cd transcendence

# Build with Docker
docker-compose up --build

import express from "express";
import path from "path";
import cors from "cors";
import jwt from "jsonwebtoken";
import { createServer as createViteServer } from "vite";

const SECRET_KEY = "dev-secret-key";

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(cors());
  app.use(express.json());
  app.use(express.urlencoded({ extended: true }));

  // In-memory "database"
  const users: any[] = [];
  
  // Create a default user
  users.push({
    id: "1",
    email: "jsnashish@gmail.com",
    full_name: "Jason Ashish",
    password: "Jason123ashish", // plain text for mock
    is_active: true,
    created_at: new Date().toISOString()
  });

  // API Routes
  app.get("/api/v1/health", (req, res) => {
    res.json({ status: "ok", version: "1.0.0" });
  });

  app.post("/api/v1/auth/register", (req, res) => {
    const { email, password, full_name } = req.body;
    if (users.find(u => u.email === email)) {
      return res.status(400).json({ detail: "Email already registered" });
    }
    const newUser = {
      id: String(users.length + 1),
      email,
      full_name,
      password,
      is_active: true,
      created_at: new Date().toISOString()
    };
    users.push(newUser);
    res.status(201).json(newUser);
  });

  app.post("/api/v1/auth/login", (req, res) => {
    const { username, password } = req.body;
    const user = users.find(u => u.email === username && u.password === password);
    if (!user) {
      return res.status(400).json({ detail: "Incorrect email or password" });
    }
    const access_token = jwt.sign({ sub: user.id }, SECRET_KEY, { expiresIn: '7d' });
    res.json({ access_token, token_type: "bearer" });
  });

  app.get("/api/v1/auth/me", (req, res) => {
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      return res.status(401).json({ detail: "Not authenticated" });
    }
    const token = authHeader.split(" ")[1];
    try {
      const decoded: any = jwt.verify(token, SECRET_KEY);
      const user = users.find(u => u.id === decoded.sub);
      if (!user) {
        return res.status(401).json({ detail: "User not found" });
      }
      res.json(user);
    } catch (err) {
      res.status(401).json({ detail: "Invalid token" });
    }
  });

  // Vite middleware for development
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), 'dist');
    app.use(express.static(distPath));
    app.get('*', (req, res) => {
      res.sendFile(path.join(distPath, 'index.html'));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
}

startServer();

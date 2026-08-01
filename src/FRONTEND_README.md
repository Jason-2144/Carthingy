# CarScope AI - Frontend

## Folder Structure

- \`src/components/\`: Reusable UI components (buttons, inputs, cards) and complex feature-specific components. Contains \`ui/\` for generic Shadcn-like components.
- \`src/layouts/\`: Structural layout components (Dashboard Layout, Auth Layout, Sidebar, Navbar) that wrap pages.
- \`src/pages/\`: Top-level route components representing distinct views (Dashboard, Search, Settings, Login, etc.).
- \`src/hooks/\`: Custom React hooks (e.g., \`useAuth\`, \`useListings\`) abstracting state and TanStack Query logic.
- \`src/services/\`: API client configuration (Axios instances) and endpoint functions to communicate with the backend.
- \`src/contexts/\`: React Context providers for global state like Authentication, Theme, and Notifications.
- \`src/types/\`: TypeScript interfaces and Zod schemas defining API responses, forms, and component props.
- \`src/utils/\`: Utility functions (formatting dates, currency, class name merging, etc.).
- \`src/assets/\`: Static assets like placeholder images or icons.
- \`src/styles/\`: Global CSS and Tailwind configuration files.
- \`tests/\`: (Outside src) Unit, component, and E2E tests for the frontend.

## Architecture

The frontend is a React Single Page Application (SPA) built with Vite, TypeScript, and Tailwind CSS.
State management is handled by React Context (for global UI/Auth state) and TanStack Query (for asynchronous server state).
Routing is managed by React Router DOM.
Forms are built using React Hook Form and validated with Zod.
Animations are powered by Framer Motion.
Charts are rendered using Recharts.

All data is dynamically fetched from the FastAPI backend. No mock data is used in production builds.

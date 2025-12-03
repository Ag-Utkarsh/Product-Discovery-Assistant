# Frontend Component Map

## Overview
The frontend is a Single Page Application (SPA) built with React and Vite. It uses Tailwind CSS for styling and follows a component-based architecture.

## Key Components

### `App.jsx`
*   **Role:** Main layout and router.
*   **Responsibilities:**
    *   Sets up routing (React Router).
    *   Manages global layout structure.

### `ChatInterface.jsx`
*   **Role:** The core feature view.
*   **Responsibilities:**
    *   Displays the chat history (user messages and bot responses).
    *   Handles user input submission.
    *   Calls the backend `/chat` API.
    *   Renders `ProductCard` components within the chat stream when recommendations are received.

### `ProductCard.jsx`
*   **Role:** Reusable UI for displaying a single product.
*   **Props:** `product` object (title, price, image, etc.).
*   **Responsibilities:**
    *   Renders product image, title, and formatted price.
    *   Handles "View Details" interactions (if implemented).

### `ProductList.jsx` (Optional/If used)
*   **Role:** Grid view for the standard catalog.
*   **Responsibilities:**
    *   Fetches data from `/products`.
    *   Renders a grid of `ProductCard` components.

## Directory Structure

```text
src/
├── components/       # Reusable UI components (ProductCard, etc.)
├── pages/            # Full page views (Home, Chat)
├── services/         # API integration logic (api.js)
├── App.jsx           # Root component
└── main.jsx          # Entry point
```

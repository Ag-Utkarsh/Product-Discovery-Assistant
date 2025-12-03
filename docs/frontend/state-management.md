# Frontend State Management

## Strategy
The application uses **Local State** (React `useState`) for most features, as the complexity does not yet warrant a global store like Redux or Zustand.

## State Breakdown

### Chat State (`ChatInterface.jsx`)
*   `messages` (Array): Stores the history of the conversation.
    *   Structure: `{ type: 'user' | 'bot', content: string, products?: Array }`
*   `isLoading` (Boolean): Tracks whether a request to the backend is in progress. Used to show loading spinners.
*   `input` (String): The current value of the chat input field.

### Product List State (`ProductList.jsx` or similar)
*   `products` (Array): List of fetched products.
*   `loading` (Boolean): Loading state for the fetch operation.
*   `error` (String | Null): Stores error messages if the API call fails.

## API Integration
*   **Axios** is used for making HTTP requests.
*   API calls are typically handled within `useEffect` hooks (for initial load) or event handlers (for form submission).
*   Base URL is configured via `VITE_API_URL` environment variable.

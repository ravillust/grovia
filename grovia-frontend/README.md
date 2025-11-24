# GROVIA Frontend

Modern web application untuk deteksi penyakit tanaman menggunakan Vue 3 dan Vite.

## Features

- Modern UI with Vue 3 Composition API
- Image upload & preview
- Real-time disease detection
- Detection history management
- User authentication
- Responsive design
- Fast HMR with Vite

## Tech Stack

- **Framework**: Vue 3.4.21
- **Build Tool**: Vite 5.1.5
- **State Management**: Pinia 2.1.7
- **Routing**: Vue Router 4.3.0
- **HTTP Client**: Axios 1.6.7
- **Icons**: Lucide Vue Next 0.548.0

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Project Setup

### Install Dependencies

```sh
npm install
```

### Configure Environment

Create `.env` file:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

### Development Server

```sh
npm run dev
```

Server will run at: http://localhost:5173

### Build for Production

```sh
npm run build
```

### Preview Production Build

```sh
npm run preview
```

## Project Structure

```
src/
├── assets/              # Static assets (images, styles)
├── components/          # Vue components
│   ├── common/          # Shared components
│   ├── detection/       # Detection feature components
│   └── history/         # History feature components
├── composables/         # Composition functions
├── router/              # Vue Router configuration
├── services/            # API services
│   ├── api.js           # API client
│   └── storage.js       # LocalStorage utilities
├── stores/              # Pinia stores
│   ├── auth.js          # Authentication state
│   ├── detection.js     # Detection state
│   └── history.js       # History state
├── utils/               # Utility functions
├── views/               # Page views
└── main.js              # Application entry point
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier

## Browser Support

Modern browsers with ES6+ support:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

Educational Project - Grovia Team

Last Updated: November 18, 2025

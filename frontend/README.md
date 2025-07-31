# White Label Frontend

A modern, responsive React application built with TypeScript, Vite, and Tailwind CSS. This is a white label solution that can be customized for any project.

## 🚀 Features

- **Modern React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for utility-first styling
- **React Router v6** for navigation
- **React Query** for server state management
- **Heroicons** for consistent iconography
- **Responsive Design** that works on all devices
- **Professional Layout** with fixed navbar and sidebar
- **Generic Components** ready for customization

## 🛠️ Tech Stack

- **Frontend Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Routing**: React Router v6
- **State Management**: React Query (@tanstack/react-query)
- **HTTP Client**: Axios
- **Icons**: Heroicons
- **Linting**: ESLint

## 📦 Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```

3. Copy environment variables:
   ```bash
   cp .env.example .env
   ```

4. Start development server:
   ```bash
   npm run dev
   ```

## 🎨 Customization

### Brand Configuration
Edit these files to customize the branding:

- **App Name**: Update `VITE_APP_NAME` in `.env`
- **Logo/Brand**: Modify the title in `src/components/layout/Navbar.tsx`
- **Colors**: Update the color scheme in `tailwind.config.js`
- **Theme**: Modify CSS variables in `src/index.css`

### Navigation
Update the navigation menu in `src/components/layout/Sidebar.tsx`:

```typescript
const navigation = [
  { name: 'Dashboard', href: '/', icon: HomeIcon },
  { name: 'Your Page', href: '/your-page', icon: YourIcon },
  // Add more navigation items
];
```

### Dashboard Metrics
Customize the dashboard cards in `src/pages/Dashboard/Dashboard.tsx`:

```typescript
// Update the metrics to match your use case
<p className="text-sm font-medium text-gray-500">Your Metric</p>
<p className="text-3xl font-bold text-gray-900 mt-2">Your Value</p>
```

## 📁 Project Structure

```
src/
├── components/           # Reusable UI components
│   └── layout/          # Layout components (Navbar, Sidebar, Layout)
├── pages/               # Page components
│   ├── Dashboard/       # Dashboard with metrics
│   ├── Data/           # Data management page
│   ├── Users/          # User management page
│   ├── Analytics/      # Analytics page
│   └── Settings/       # Settings page
├── services/           # API services
│   └── api.ts         # Generic API service functions
├── hooks/              # Custom React hooks
│   └── useGeneric.ts  # Generic hooks for CRUD operations
├── types/              # TypeScript type definitions
│   └── index.ts       # Generic type interfaces
└── App.tsx            # Main app component with routing
```

## 🔌 API Integration

The app includes generic API services in `src/services/api.ts`:

```typescript
// Generic CRUD operations
apiService.getAll('your-endpoint')
apiService.getById('your-endpoint', id)
apiService.create('your-endpoint', data)
apiService.update('your-endpoint', id, data)
apiService.delete('your-endpoint', id)
```

## 🎯 Usage Examples

### Adding a New Page

1. Create a new page component:
   ```typescript
   // src/pages/YourPage/YourPage.tsx
   import React from 'react';
   
   const YourPage: React.FC = () => {
     return (
       <div className="space-y-6">
         <h1 className="text-2xl font-bold text-gray-900">Your Page</h1>
         {/* Your content */}
       </div>
     );
   };
   
   export default YourPage;
   ```

2. Add the route to `App.tsx`:
   ```typescript
   <Route path="your-page" element={<YourPage />} />
   ```

3. Add navigation link to `Sidebar.tsx`:
   ```typescript
   { name: 'Your Page', href: '/your-page', icon: YourIcon }
   ```

### Using Generic Hooks

```typescript
import { useData, useCreateItem } from '../hooks/useGeneric';

// In your component
const { data, isLoading } = useData('your-endpoint');
const createMutation = useCreateItem('your-endpoint');
```

## 🎨 Styling

The app uses Tailwind CSS with custom color scheme. Main brand colors:

- **Primary**: `recway-600` (#0284c7)
- **Primary Light**: `recway-100` (#e0f2fe)
- **Success**: `green-600`
- **Warning**: `yellow-600`
- **Error**: `red-600`

Common CSS classes included:
- `.card` - Standard card styling
- `.btn-primary` - Primary button styling
- `.btn-secondary` - Secondary button styling

## 📱 Responsive Design

The layout is fully responsive:
- **Mobile**: Collapsible sidebar
- **Tablet**: Adapted layout for medium screens
- **Desktop**: Full sidebar and optimal spacing

## 🚀 Build for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## 🔧 Development

- **Hot Reload**: Automatic refresh on file changes
- **TypeScript**: Full type checking
- **ESLint**: Code quality enforcement
- **Fast Refresh**: Preserve component state on edits

## 📄 License

This is a white label template - customize as needed for your project.

---

## 🎯 Next Steps

1. Replace "Brand Name" with your actual brand
2. Update the color scheme to match your brand
3. Add your specific pages and functionality
4. Connect to your backend API
5. Deploy to your preferred hosting platform

This template provides a solid foundation for any React application with modern best practices and professional styling.

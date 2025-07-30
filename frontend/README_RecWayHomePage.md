# RecWay Home Page - Componente Completo

Una página de inicio completa y auto-contenida para RecWay, adaptada desde SmartEpi para monitoreo ambiental.

## 📁 Archivos Incluidos

```
RecWayHomePage.tsx      # Componente React principal
RecWayHomePage.css      # Estilos CSS completos
HomePage.tsx            # Página que utiliza el componente
README_RecWayHomePage.md # Este archivo
```

## 🚀 Instalación Rápida

### 1. Dependencias Requeridas

```bash
# Dependencias principales
npm install lucide-react react-intersection-observer aos

# Tipos TypeScript
npm install --save-dev @types/aos
```

### 2. Archivos ya creados

Los siguientes archivos ya están en tu proyecto:

```
src/
├── components/
│   ├── RecWayHomePage.tsx     # Componente principal ✅
│   └── RecWayHomePage.css     # Estilos completos ✅
├── pages/
│   └── HomePage.tsx           # Página que usa el componente ✅
└── App.tsx                    # Configurado con nueva ruta ✅
```

### 3. Rutas Configuradas

- `/` - Dashboard (con layout existente)
- `/home` - Homepage completa de RecWay (sin layout)

## 🎯 Uso del Componente

### Acceso a la Homepage

1. **Servidor de desarrollo corriendo en**: http://localhost:5175
2. **Visita la homepage en**: http://localhost:5175/home

### Personalización Básica

```tsx
// En HomePage.tsx puedes personalizar:
<RecWayHomePage 
  companyName="Tu Empresa"
  heroTitle="Tu Título Personalizado"
  heroSubtitle="Tu descripción personalizada aquí..."
  contactEmail="contacto@tuempresa.com"
  contactPhone="+57 (300) 000-0000"
  contactAddress="Tu Dirección, Ciudad, País"
  onGetStarted={() => {
    // Tu lógica para comenzar
    window.location.href = '/dashboard';
  }}
  onContactSales={() => {
    // Tu lógica para contacto
    window.location.href = '/contact';
  }}
/>
```

## ⚙️ Características Implementadas

### 🎨 Diseño y UI
- ✅ **Hero Section** con animaciones y video circular
- ✅ **Gradientes** azul a verde para RecWay
- ✅ **Logo animado** con efectos hover
- ✅ **Responsive design** para móviles y desktop

### 🚀 Funcionalidades
- ✅ **6 Features cards** específicas para monitoreo ambiental:
  - Monitoreo en Tiempo Real con IoT
  - Análisis Predictivo con IA
  - Sensores Multivariables
  - Alertas Inteligentes
  - Visualización Avanzada
  - Gestión de Calidad del Agua

### 📊 Secciones Completas
- ✅ **How It Works** - 3 pasos del proceso
- ✅ **Team Section** - Perfiles del equipo
- ✅ **Pricing Plans** - 3 planes (Básico, Profesional, Enterprise)
- ✅ **Call to Action** con botones funcionales
- ✅ **Contact Section** con mapa integrado
- ✅ **Footer** con información de la empresa

### 🎭 Animaciones
- ✅ **AOS (Animate On Scroll)** configurado
- ✅ **Animaciones CSS** personalizadas
- ✅ **Efectos hover** en cards y botones
- ✅ **Transiciones suaves** en toda la página

## 🎨 Personalización de Estilos

### Variables CSS Principales

```css
:root {
  --recway-primary: #1e88e5;      /* Azul principal */
  --recway-secondary: #2563eb;    /* Azul secundario */
  --recway-accent: #10b981;       /* Verde acento */
  --recway-green: #059669;        /* Verde oscuro */
}
```

### Cambiar Colores de Marca

```css
/* En RecWayHomePage.css */
:root {
  --recway-primary: #tu-color-primario;
  --recway-accent: #tu-color-acento;
}
```

## 📱 Responsive Design

Breakpoints configurados:
- **Mobile**: < 640px
- **Tablet**: 640px - 768px
- **Desktop**: 768px - 1024px
- **Large**: > 1024px

## 🔧 Assets y Recursos

### Imágenes Placeholder
Las siguientes imágenes se cargan automáticamente:
- `/placeholder-env.svg` - Para cards How It Works
- Videos de Mixkit - Para hero y video section

### Assets Personalizados (Opcionales)
Si quieres usar tus propias imágenes, crea:

```
public/assets/
├── recway-logo.png              # Logo de la empresa
├── founder_profile_image.png    # Foto del fundador
├── co-founder_profile_image.png # Foto del co-fundador
├── how_it_works_1.jpg          # Imagen paso 1
├── how_it_works_2.jpg          # Imagen paso 2
├── how_it_works_3.jpg          # Imagen paso 3
└── recway_workflow.jpg         # Diagrama de flujo
```

## 🚀 Integración con Tu Sistema

### Navegación a Dashboard
```tsx
// En HomePage.tsx
const handleGetStarted = () => {
  window.location.href = '/'; // Va al dashboard
};
```

### Integrar con Autenticación
```tsx
import { useAuth } from '../hooks/useAuth';

const HomePage = () => {
  const { login, register } = useAuth();
  
  return (
    <RecWayHomePage 
      onGetStarted={() => {
        // Lógica de registro
        register();
      }}
      onContactSales={() => {
        // Abrir modal de contacto
        openContactModal();
      }}
    />
  );
};
```

## 📊 Métricas y Analytics

### Google Analytics (Opcional)
```tsx
// Tracking de eventos
const handleGetStarted = () => {
  // Enviar evento a GA
  gtag('event', 'click', {
    event_category: 'CTA',
    event_label: 'Get Started Button'
  });
  
  // Tu lógica aquí
  navigate('/dashboard');
};
```

## 🔍 SEO Optimizations

### Meta Tags Recomendados
```html
<!-- En index.html -->
<title>RecWay - Monitoreo Ambiental Inteligente</title>
<meta name="description" content="Plataforma avanzada de monitoreo ambiental con IoT e IA">
<meta name="keywords" content="monitoreo ambiental, IoT, sensores, análisis">
```

## 🐛 Solución de Problemas

### Videos no cargan
Los videos usan URLs de Mixkit que son gratuitas. Si necesitas videos propios:

```tsx
// En RecWayHomePage.tsx, cambiar:
<source src="/assets/tu-video.mp4" type="video/mp4" />
```

### Animaciones no funcionan
Verifica que AOS esté importado correctamente:

```tsx
import AOS from 'aos';
import 'aos/dist/aos.css';

useEffect(() => {
  AOS.init();
}, []);
```

### Estilos no se aplican
Asegúrate de importar el CSS:

```tsx
import '../components/RecWayHomePage.css';
```

## 📈 Próximos Pasos

### 1. Personalizar Contenido
- [ ] Cambiar textos por los de tu empresa
- [ ] Agregar imágenes reales
- [ ] Personalizar información de contacto

### 2. Integrar Funcionalidades
- [ ] Conectar formularios
- [ ] Agregar sistema de autenticación
- [ ] Integrar con backend

### 3. Optimizar
- [ ] Comprimir imágenes
- [ ] Configurar lazy loading
- [ ] Optimizar para SEO

## 📞 Soporte

¿Necesitas ayuda personalizando la homepage?

- 📧 **Email**: contacto@recway.com
- 💬 **Chat**: [Abrir chat en vivo]
- 📖 **Docs**: [Ver documentación completa]

---

### 🎉 ¡Tu homepage está lista!

Visita http://localhost:5175/home para ver tu nueva página de inicio de RecWay.

**¡Happy coding!** 🚀

## 🔄 Changelog

### v1.0.0 (Hoy)
- ✅ Componente RecWayHomePage completo
- ✅ Estilos CSS personalizados para RecWay
- ✅ Integración con React Router
- ✅ Animaciones AOS configuradas
- ✅ 6 secciones principales implementadas
- ✅ Diseño responsive
- ✅ Tema ambiental adaptado

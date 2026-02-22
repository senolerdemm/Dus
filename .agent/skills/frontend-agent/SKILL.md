---
name: Frontend Agent
description: DUS sistemi frontend tasarım ve geliştirme talimatları — UI/UX, sayfa yapısı, responsive design
---

# 🎨 Frontend Agent (React + Vite + Tailwind)

DUS sisteminin **React frontend uygulamasını** geliştirir.
Konum: `frontend/`

---

## Teknoloji

| Araç | Versiyon | Neden? |
|------|----------|--------|
| React | 18+ | Component-based, modern UI |
| Vite | 5+ | Hızlı dev server, HMR |
| Tailwind CSS | 3+ | Utility-first, hızlı styling |
| React Router | 6+ | SPA navigasyon |
| Axios | - | HTTP istekleri |

---

## Proje Oluşturma

```bash
cd /Users/senolerdem/Desktop/fastapi
npx -y create-vite@latest frontend -- --template react
cd frontend
npm install
npm install -D tailwindcss @tailwindcss/vite
npm install react-router-dom axios
```

### vite.config.js
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8000'  // Backend'e proxy
    }
  }
})
```

### index.css (Tailwind directives)
```css
@import "tailwindcss";
```

---

## Tasarım Felsefesi
- **Dark theme**, premium hissiyat
- **Duolingo** tarzı gamification
- Öğrencinin odaklanmasını sağlayan sade ama motive edici UX

---

## Renk Paleti (tailwind.config.js extend)

```javascript
colors: {
  'dus': {
    'primary': '#6C5CE7',
    'primary-light': '#A29BFE',
    'primary-dark': '#5A4BD1',
    'bg': '#0F0F1A',
    'card': '#1A1A2E',
    'card-alt': '#16213E',
    'border': '#2A2A4A',
    'success': '#00B894',
    'danger': '#FF6B6B',
    'warning': '#FDCB6E',
    'text': '#FFFFFF',
    'text-secondary': '#B0B0C8',
  }
}
```

## Kategori Renkleri
```javascript
const categoryColors = {
  1: '#FF6B6B',  // Oral Diagnoz
  2: '#4ECDC4',  // Periodontoloji
  3: '#45B7D1',  // Endodonti
  4: '#96CEB4',  // Ortodonti
  5: '#FFEAA7',  // Protetik
  6: '#DDA0DD',  // Pedodonti
  7: '#98D8C8',  // Cerrahi
  8: '#F7DC6F',  // Restoratif
};
```

---

## Tipografi (Google Fonts)
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```
- Body: `Inter`
- Sayılar/skor: `JetBrains Mono`

---

## Dosya Yapısı

```
frontend/src/
├── main.jsx                 # ReactDOM.createRoot
├── App.jsx                  # Router + Layout
├── index.css                # Tailwind + custom animasyonlar
│
├── api/
│   └── client.js            # Axios instance, JWT interceptor
│
├── context/
│   └── AuthContext.jsx      # createContext, useAuth hook
│
├── pages/
│   ├── LoginPage.jsx        # Giriş formu
│   ├── RegisterPage.jsx     # Kayıt formu
│   ├── HomePage.jsx         # Kategori kartları + hızlı başla
│   ├── QuizPage.jsx         # Soru gösterimi + zamanlayıcı
│   ├── ResultPage.jsx       # Skor + breakdown + AI analiz
│   ├── StatsPage.jsx        # İstatistikler + grafikler
│   ├── BookmarksPage.jsx    # İşaretlenmiş sorular
│   └── ProfilePage.jsx      # Kullanıcı profili
│
└── components/
    ├── Navbar.jsx           # Üst navigasyon
    ├── CategoryCard.jsx     # Kategori kartı (emoji + renk + sayı)
    ├── QuestionCard.jsx     # Soru metni gösterimi
    ├── OptionButton.jsx     # A-E şık butonu (animasyonlu)
    ├── Timer.jsx            # Geri sayım zamanlayıcı
    ├── ScoreCircle.jsx      # Dairesel skor göstergesi (SVG)
    └── Toast.jsx            # Bildirim mesajları
```

---

## Sayfa Detayları

### 🔐 LoginPage / RegisterPage
- Ortalanmış glassmorphism kart
- Input'lar: `bg-dus-card border-dus-border`
- Hata mesajları inline kırmızı
- Başarılı girişte → `navigate('/home')`

### 🏠 HomePage
- Hoş geldin + kullanıcı adı
- 8 kategori kartı: **CSS grid** `grid-cols-2 md:grid-cols-4`
- Her kart: emoji + isim + soru sayısı + renk şeridi
- "Karışık Sınav Başlat" büyük CTA buton
- Mini istatistik (toplam çözülen, başarı oranı)

### 🧪 QuizPage
- **Üst bar:** Soru no (3/20) | `<Timer />` | Kategori badge
- **Orta:** `<QuestionCard />` — soru metni büyük font
- **Şıklar:** 5x `<OptionButton />` — seçilince highlight
- **Alt bar:** 💡 İpucu (GPT-4o) | ⭐ İşaretle | → Sonraki
- **Cevap sonrası:** Yeşil/kırmızı animasyon → açıklama slide-down
- State: `{ questions[], currentIndex, answers[], startTime }`

### 📊 ResultPage
- `<ScoreCircle />` büyük dairesel SVG
- Doğru ✅ / Yanlış ❌ / Boş ⬜ sayıları
- Kategoriye göre mini bar'lar
- AI zayıf konu analizi (GPT-4o endpoint'inden)
- "Tekrar Dene" + "Ana Sayfa" butonları

### 📈 StatsPage
- Genel başarı yüzdesi (büyük)
- Kategoriye göre renkli bar chart (CSS flexbox)
- Son 5 sınav geçmişi tablosu

### ⭐ BookmarksPage
- İşaretlenmiş soruların kartları
- Kategoriye göre filtre tab'ları
- Not ekleme modal

### 👤 ProfilePage
- Kullanıcı bilgileri
- Toplam çözülen soru / başarı / süre
- Çıkış yap butonu

---

## API Client (api/client.js)

```javascript
import axios from 'axios';

const api = axios.create({ baseURL: '/api/v1' });

// JWT interceptor
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default api;
```

---

## Auth Context (context/AuthContext.jsx)

```javascript
const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));

  const login = async (username, password) => { ... };
  const register = async (data) => { ... };
  const logout = () => { ... };

  return (
    <AuthContext.Provider value={{ user, token, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
```

---

## Animasyonlar (index.css)

```css
/* Sayfa geçişi */
.page-enter { animation: fadeInUp 0.3s ease; }

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Doğru cevap pulse */
.correct-pulse { animation: correctPulse 0.6s ease; }
@keyframes correctPulse {
  0%   { box-shadow: 0 0 0 0 rgba(0, 184, 148, 0.4); }
  70%  { box-shadow: 0 0 0 15px rgba(0, 184, 148, 0); }
}

/* Yanlış cevap shake */
.wrong-shake { animation: wrongShake 0.4s ease; }
@keyframes wrongShake {
  25%  { transform: translateX(-8px); }
  75%  { transform: translateX(8px); }
}

/* Glassmorphism */
.glass { 
  @apply bg-dus-card/80 backdrop-blur-xl border border-dus-primary/20 rounded-2xl;
}
```

---

## Routing (App.jsx)

```jsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/home" element={<ProtectedRoute><HomePage /></ProtectedRoute>} />
          <Route path="/quiz" element={<ProtectedRoute><QuizPage /></ProtectedRoute>} />
          <Route path="/result" element={<ProtectedRoute><ResultPage /></ProtectedRoute>} />
          <Route path="/stats" element={<ProtectedRoute><StatsPage /></ProtectedRoute>} />
          <Route path="/bookmarks" element={<ProtectedRoute><BookmarksPage /></ProtectedRoute>} />
          <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
```

---

## Responsive
- Tailwind responsive: `sm:`, `md:`, `lg:`
- Quiz şıkları: mobilde `flex-col`, desktop'ta `grid-cols-2`
- Kategori kartları: mobilde `grid-cols-2`, tablet `grid-cols-3`, desktop `grid-cols-4`
- Navbar: mobilde hamburger menu

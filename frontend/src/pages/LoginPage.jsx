import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { FiMail, FiLock, FiUser } from 'react-icons/fi'

export default function LoginPage() {
    const [isRegister, setIsRegister] = useState(false)
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [fullName, setFullName] = useState('')
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)
    const { signIn, signUp } = useAuth()
    const navigate = useNavigate()

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError('')
        setLoading(true)
        try {
            if (isRegister) {
                await signUp(email, password, fullName)
            } else {
                await signIn(email, password)
            }
            navigate('/')
        } catch (err) {
            setError(err.message || 'Bir hata oluştu')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen flex items-center justify-center p-4"
            style={{ background: 'var(--duo-bg)' }}>
            <div className="w-full max-w-md animate-slide-up">
                {/* Logo */}
                <div className="text-center mb-8">
                    <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl mb-4"
                        style={{ background: 'linear-gradient(135deg, var(--duo-green), #7beb34)' }}>
                        <span className="text-4xl">🦷</span>
                    </div>
                    <h1 className="text-3xl font-black tracking-tight">ZenithDUS</h1>
                    <p className="mt-1" style={{ color: 'var(--duo-text-muted)' }}>AI Destekli DUS Hazırlık</p>
                </div>

                {/* Card */}
                <div className="duo-card" style={{ borderColor: 'var(--duo-border)' }}>
                    {/* Tab toggle */}
                    <div className="flex mb-6 rounded-xl overflow-hidden p-1 border-2" style={{ borderColor: 'var(--duo-border)', background: 'var(--duo-gray)' }}>
                        <button onClick={() => setIsRegister(false)}
                            className={`flex-1 py-3 font-bold text-sm transition-all rounded-lg ${!isRegister ? 'text-white' : ''}`}
                            style={{
                                background: !isRegister ? 'var(--duo-green)' : 'transparent',
                                color: isRegister ? 'var(--duo-text-muted)' : '#fff'
                            }}>
                            GİRİŞ YAP
                        </button>
                        <button onClick={() => setIsRegister(true)}
                            className={`flex-1 py-3 font-bold text-sm transition-all rounded-lg ${isRegister ? 'text-white' : ''}`}
                            style={{
                                background: isRegister ? 'var(--duo-blue)' : 'transparent',
                                color: !isRegister ? 'var(--duo-text-muted)' : '#fff'
                            }}>
                            KAYIT OL
                        </button>
                    </div>

                    {error && (
                        <div className="mb-4 p-3 rounded-lg text-sm font-semibold"
                            style={{ background: 'rgba(255,75,75,0.15)', color: 'var(--duo-red)', border: '1px solid var(--duo-red)' }}>
                            {error}
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-4">
                        {isRegister && (
                            <div className="relative animate-slide-up">
                                <FiUser className="absolute left-3 top-1/2 -translate-y-1/2 text-lg"
                                    style={{ color: 'var(--duo-text-muted)' }} />
                                <input className="duo-input pl-10" placeholder="Ad Soyad"
                                    value={fullName} onChange={e => setFullName(e.target.value)} required />
                            </div>
                        )}
                        <div className="relative">
                            <FiMail className="absolute left-3 top-1/2 -translate-y-1/2 text-lg"
                                style={{ color: 'var(--duo-text-muted)' }} />
                            <input className="duo-input pl-10" type="email" placeholder="E-posta"
                                value={email} onChange={e => setEmail(e.target.value)} required />
                        </div>
                        <div className="relative">
                            <FiLock className="absolute left-3 top-1/2 -translate-y-1/2 text-lg"
                                style={{ color: 'var(--duo-text-muted)' }} />
                            <input className="duo-input pl-10" type="password" placeholder="Şifre (min 6 karakter)"
                                value={password} onChange={e => setPassword(e.target.value)} required minLength={6} />
                        </div>

                        <button type="submit" disabled={loading}
                            className="btn-duo btn-duo-green w-full text-lg py-4 mt-2"
                            style={{ opacity: loading ? 0.7 : 1 }}>
                            {loading ? '⏳' : isRegister ? '🚀 KAYIT OL' : '🦷 GİRİŞ YAP'}
                        </button>
                    </form>
                </div>

                <p className="text-center mt-6 text-sm" style={{ color: 'var(--duo-text-muted)' }}>
                    Her gün 10 soru çöz, DUS'u kazan! 💪
                </p>
            </div>
        </div>
    )
}

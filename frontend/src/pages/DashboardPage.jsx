import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../lib/api'
import { FiZap, FiTarget, FiTrendingUp, FiBookmark, FiAward, FiLogOut } from 'react-icons/fi'

export default function DashboardPage() {
    const { user, signOut } = useAuth()
    const navigate = useNavigate()
    const [categories, setCategories] = useState([])
    const [stats, setStats] = useState(null)
    const [loading, setLoading] = useState(true)

    const fullName = user?.user_metadata?.full_name || 'Öğrenci'

    useEffect(() => {
        loadData()
    }, [])

    const loadData = async () => {
        try {
            const [catRes, statsRes] = await Promise.all([
                api.get('/categories/'),
                api.get('/stats/overview').catch(() => ({ data: null })),
            ])
            setCategories(catRes.data)
            setStats(statsRes.data)
        } catch (err) {
            console.error(err)
        } finally {
            setLoading(false)
        }
    }

    const startQuiz = (categoryId = null) => {
        navigate('/quiz', { state: { categoryId } })
    }

    const xp = stats?.correct_answers ? stats.correct_answers * 10 : 0
    const streak = stats?.total_quizzes || 0

    return (
        <div className="min-h-screen" style={{ background: 'var(--duo-bg)' }}>
            {/* Navbar */}
            <nav className="duo-nav">
                <div className="max-w-screen-xl w-full mx-auto px-4 md:px-8 py-3 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <span className="text-2xl">🦷</span>
                        <span className="font-black text-lg">SelinayaAşığımDUS</span>
                    </div>
                    <div className="flex items-center gap-3">
                        <span className="badge-xp">⚡ {xp} XP</span>
                        <span className="badge-streak">🔥 {streak}</span>
                        <button onClick={() => navigate('/stats')} className="p-2 rounded-lg transition-colors hover:bg-black/5 text-gray-400 hover:text-gray-600">
                            <FiTrendingUp size={20} />
                        </button>
                        <button onClick={() => navigate('/bookmarks')} className="p-2 rounded-lg transition-colors hover:bg-black/5 text-gray-400 hover:text-gray-600">
                            <FiBookmark size={20} />
                        </button>
                        <button onClick={signOut} className="p-2 rounded-lg transition-colors hover:bg-black/5"
                            style={{ color: 'var(--duo-text-muted)' }}>
                            <FiLogOut size={20} />
                        </button>
                    </div>
                </div>
            </nav>

            <div className="max-w-screen-xl w-full mx-auto px-4 md:px-8 py-8">
                {/* Greeting */}
                <div className="animate-slide-up mb-8">
                    <h1 className="text-2xl font-black mb-1">Merhaba, {fullName}! 👋</h1>
                    <p style={{ color: 'var(--duo-text-muted)' }}>Bugün ne çalışmak istersin?</p>
                </div>

                {/* Quick Stats */}
                {stats && (
                    <div className="grid grid-cols-3 gap-4 mb-8 animate-slide-up stagger-1">
                        <div className="duo-card text-center flex flex-col justify-center" style={{ borderTop: '4px solid var(--duo-green)' }}>
                            <div className="text-2xl font-black" style={{ color: 'var(--duo-green)' }}>
                                {stats.total_quizzes}
                            </div>
                            <div className="text-xs font-semibold mt-1" style={{ color: 'var(--duo-text-muted)' }}>Sınav</div>
                        </div>
                        <div className="duo-card text-center flex flex-col justify-center" style={{ borderTop: '4px solid var(--duo-blue)' }}>
                            <div className="text-2xl font-black" style={{ color: 'var(--duo-blue)' }}>
                                {stats.overall_percentage}%
                            </div>
                            <div className="text-xs font-semibold mt-1" style={{ color: 'var(--duo-text-muted)' }}>Başarı</div>
                        </div>
                        <div className="duo-card text-center flex flex-col justify-center" style={{ borderTop: '4px solid var(--duo-yellow)' }}>
                            <div className="text-2xl font-black" style={{ color: 'var(--duo-yellow)' }}>
                                {xp}
                            </div>
                            <div className="text-xs font-semibold mt-1" style={{ color: 'var(--duo-text-muted)' }}>XP</div>
                        </div>
                    </div>
                )}

                {/* Quick Start */}
                <div className="mb-8 animate-slide-up stagger-2">
                    <button onClick={() => startQuiz()} className="btn-duo btn-duo-green w-full text-lg py-5 animate-pulse-glow">
                        <FiZap size={22} /> HIZLI SINAV BAŞLAT
                    </button>
                </div>

                {/* Categories */}
                <div className="animate-slide-up stagger-3">
                    <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
                        <FiTarget /> Kategoriler
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {categories.map((cat, i) => (
                            <div key={cat.id}
                                onClick={() => startQuiz(cat.id)}
                                className={`duo-card cat-card cursor-pointer stagger-${i % 5 + 1}`}
                                style={{ borderLeftColor: cat.color, borderLeftWidth: '4px' }}>
                                <div className="flex items-center gap-3">
                                    <span className="text-3xl">{cat.icon}</span>
                                    <div className="flex-1">
                                        <h3 className="font-bold">{cat.name}</h3>
                                        <p className="text-xs mt-0.5" style={{ color: 'var(--duo-text-muted)' }}>
                                            {cat.description}
                                        </p>
                                    </div>
                                    <div className="text-right">
                                        <span className="text-sm font-bold" style={{ color: cat.color }}>
                                            {cat.question_count}
                                        </span>
                                        <div className="text-xs" style={{ color: 'var(--duo-text-muted)' }}>soru</div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Daily Motivation */}
                <div className="mt-8 duo-card text-center animate-slide-up stagger-4"
                    style={{
                        background: 'linear-gradient(135deg, rgba(88,204,2,0.08), rgba(28,176,246,0.08))',
                        borderColor: 'var(--duo-green)'
                    }}>
                    <div className="text-3xl mb-2">🏆</div>
                    <p className="font-bold text-sm">
                        "Başarı, her gün tekrarlanan küçük çabaların toplamıdır."
                    </p>
                    <p className="text-xs mt-1" style={{ color: 'var(--duo-text-muted)' }}>— Robert Collier</p>
                </div>
            </div>
        </div>
    )
}

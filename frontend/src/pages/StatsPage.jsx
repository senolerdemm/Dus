import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../lib/api'
import { FiArrowLeft, FiBarChart2, FiTrendingUp } from 'react-icons/fi'

export default function StatsPage() {
    const navigate = useNavigate()
    const [overview, setOverview] = useState(null)
    const [categoryStats, setCategoryStats] = useState([])
    const [history, setHistory] = useState([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        loadStats()
    }, [])

    const loadStats = async () => {
        try {
            const [ovRes, catRes, histRes] = await Promise.all([
                api.get('/stats/overview').catch(() => ({ data: null })),
                api.get('/stats/by-category').catch(() => ({ data: [] })),
                api.get('/quiz/history').catch(() => ({ data: [] })),
            ])
            setOverview(ovRes.data)
            setCategoryStats(catRes.data)
            setHistory(histRes.data)
        } catch (err) {
            console.error(err)
        } finally {
            setLoading(false)
        }
    }

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center" style={{ background: 'var(--duo-bg)' }}>
                <div className="animate-pop text-4xl">📊</div>
            </div>
        )
    }

    return (
        <div className="min-h-screen" style={{ background: 'var(--duo-bg)' }}>
            {/* Header */}
            <div className="duo-nav">
                <div className="max-w-screen-xl w-full mx-auto px-4 md:px-8 py-3 flex items-center gap-3">
                    <button onClick={() => navigate('/')} className="p-2 rounded-lg hover:bg-black/5 transition text-gray-400 hover:text-gray-600">
                        <FiArrowLeft size={20} />
                    </button>
                    <FiBarChart2 size={20} style={{ color: 'var(--duo-blue)' }} />
                    <h1 className="font-black text-lg">İstatistikler</h1>
                </div>
            </div>

            <div className="max-w-screen-xl w-full mx-auto px-4 md:px-8 py-6">
                {/* Overview */}
                {overview && (
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-8 animate-slide-up">
                        <div className="duo-card text-center" style={{ borderTop: '3px solid var(--duo-green)' }}>
                            <div className="text-2xl font-black" style={{ color: 'var(--duo-green)' }}>{overview.total_quizzes}</div>
                            <div className="text-xs font-semibold mt-1" style={{ color: 'var(--duo-text-muted)' }}>Toplam Sınav</div>
                        </div>
                        <div className="duo-card text-center" style={{ borderTop: '3px solid var(--duo-blue)' }}>
                            <div className="text-2xl font-black" style={{ color: 'var(--duo-blue)' }}>{overview.correct_answers}</div>
                            <div className="text-xs font-semibold mt-1" style={{ color: 'var(--duo-text-muted)' }}>Doğru Cevap</div>
                        </div>
                        <div className="duo-card text-center" style={{ borderTop: '3px solid var(--duo-red)' }}>
                            <div className="text-2xl font-black" style={{ color: 'var(--duo-red)' }}>{overview.wrong_answers}</div>
                            <div className="text-xs font-semibold mt-1" style={{ color: 'var(--duo-text-muted)' }}>Yanlış Cevap</div>
                        </div>
                        <div className="duo-card text-center" style={{ borderTop: '3px solid var(--duo-yellow)' }}>
                            <div className="text-2xl font-black" style={{ color: 'var(--duo-yellow)' }}>%{overview.overall_percentage}</div>
                            <div className="text-xs font-semibold mt-1" style={{ color: 'var(--duo-text-muted)' }}>Başarı Oranı</div>
                        </div>
                    </div>
                )}

                {/* Category Performance */}
                {categoryStats.length > 0 && (
                    <div className="mb-8 animate-slide-up stagger-2">
                        <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
                            <FiTrendingUp style={{ color: 'var(--duo-blue)' }} /> Kategori Performansı
                        </h2>
                        <div className="space-y-3">
                            {categoryStats.map(cat => (
                                <div key={cat.category_id} className="duo-card">
                                    <div className="flex items-center justify-between mb-2">
                                        <div className="flex items-center gap-2">
                                            <span>{cat.icon}</span>
                                            <span className="font-bold text-sm">{cat.category_name}</span>
                                        </div>
                                        <span className="text-sm font-bold" style={{ color: cat.percentage >= 70 ? 'var(--duo-green)' : cat.percentage >= 50 ? 'var(--duo-yellow)' : 'var(--duo-red)' }}>
                                            %{cat.percentage}
                                        </span>
                                    </div>
                                    <div className="duo-progress" style={{ height: '0.5rem' }}>
                                        <div className="duo-progress-bar" style={{
                                            width: `${cat.percentage}%`,
                                            background: cat.percentage >= 70 ? 'var(--duo-green)' : cat.percentage >= 50 ? 'var(--duo-yellow)' : 'var(--duo-red)',
                                        }} />
                                    </div>
                                    <div className="flex justify-between mt-1.5 text-xs" style={{ color: 'var(--duo-text-muted)' }}>
                                        <span>{cat.correct}/{cat.total_answered} doğru</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Quiz History */}
                {history.length > 0 && (
                    <div className="animate-slide-up stagger-3">
                        <h2 className="text-lg font-bold mb-4">📋 Sınav Geçmişi</h2>
                        <div className="space-y-2">
                            {history.slice(0, 10).map(h => (
                                <div key={h.id} className="duo-card flex items-center justify-between py-3">
                                    <div>
                                        <div className="font-bold text-sm">{h.category_name}</div>
                                        <div className="text-xs" style={{ color: 'var(--duo-text-muted)' }}>
                                            {h.score}/{h.total_questions} doğru • {Math.floor(h.time_spent_seconds / 60)}dk
                                        </div>
                                    </div>
                                    <span className="text-sm font-bold" style={{
                                        color: h.percentage >= 70 ? 'var(--duo-green)' : h.percentage >= 50 ? 'var(--duo-yellow)' : 'var(--duo-red)'
                                    }}>
                                        %{h.percentage}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {!overview && !categoryStats.length && (
                    <div className="text-center py-16 animate-slide-up">
                        <div className="text-5xl mb-4">📊</div>
                        <h2 className="text-xl font-bold mb-2">Henüz istatistik yok</h2>
                        <p className="mb-6" style={{ color: 'var(--duo-text-muted)' }}>İlk sınavını çözerek başla!</p>
                        <button onClick={() => navigate('/quiz', { state: {} })} className="btn-duo btn-duo-green">
                            SINAV BAŞLAT
                        </button>
                    </div>
                )}
            </div>
        </div>
    )
}

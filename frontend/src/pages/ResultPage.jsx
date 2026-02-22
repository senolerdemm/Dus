import { useLocation, useNavigate } from 'react-router-dom'
import { FiHome, FiRepeat, FiAward } from 'react-icons/fi'

export default function ResultPage() {
    const location = useLocation()
    const navigate = useNavigate()
    const { result, totalQuestions } = location.state || {}

    if (!result) {
        navigate('/')
        return null
    }

    const { score, percentage, grade_label, time_spent_seconds } = result
    const minutes = Math.floor(time_spent_seconds / 60)
    const seconds = time_spent_seconds % 60

    const getEmoji = () => {
        if (percentage >= 90) return '🏆'
        if (percentage >= 70) return '🎉'
        if (percentage >= 50) return '💪'
        return '📚'
    }

    const getColor = () => {
        if (percentage >= 70) return 'var(--duo-green)'
        if (percentage >= 50) return 'var(--duo-yellow)'
        return 'var(--duo-red)'
    }

    const earnedXP = score * 10

    return (
        <div className="min-h-screen flex items-center justify-center p-4" style={{ background: 'var(--duo-bg)' }}>
            <div className="max-w-md w-full text-center">
                {/* Trophy */}
                <div className="animate-pop mb-6">
                    <div className="text-7xl mb-2">{getEmoji()}</div>
                    <h1 className="text-3xl font-black">Sınav Tamamlandı!</h1>
                </div>

                {/* Score Circle */}
                <div className="animate-slide-up stagger-1 mb-8">
                    <div className="inline-flex items-center justify-center w-36 h-36 rounded-full border-4"
                        style={{ borderColor: getColor(), boxShadow: `0 0 30px ${getColor()}33` }}>
                        <div>
                            <div className="text-4xl font-black" style={{ color: getColor() }}>
                                %{percentage}
                            </div>
                            <div className="text-xs font-semibold" style={{ color: 'var(--duo-text-muted)' }}>
                                {grade_label}
                            </div>
                        </div>
                    </div>
                </div>

                {/* Stats Grid */}
                <div className="grid grid-cols-3 gap-3 mb-8 animate-slide-up stagger-2">
                    <div className="duo-card py-3">
                        <div className="text-xl font-black" style={{ color: 'var(--duo-green)' }}>{score}</div>
                        <div className="text-xs" style={{ color: 'var(--duo-text-muted)' }}>Doğru</div>
                    </div>
                    <div className="duo-card py-3">
                        <div className="text-xl font-black" style={{ color: 'var(--duo-red)' }}>{totalQuestions - score}</div>
                        <div className="text-xs" style={{ color: 'var(--duo-text-muted)' }}>Yanlış</div>
                    </div>
                    <div className="duo-card py-3">
                        <div className="text-xl font-black" style={{ color: 'var(--duo-blue)' }}>
                            {minutes}:{seconds.toString().padStart(2, '0')}
                        </div>
                        <div className="text-xs" style={{ color: 'var(--duo-text-muted)' }}>Süre</div>
                    </div>
                </div>

                {/* XP Earned */}
                <div className="animate-slide-up stagger-3 mb-8">
                    <div className="duo-card inline-flex items-center gap-2 px-6 py-3"
                        style={{ borderColor: 'var(--duo-yellow)', background: 'rgba(255,200,0,0.08)' }}>
                        <span className="text-2xl">⚡</span>
                        <span className="text-xl font-black" style={{ color: 'var(--duo-yellow)' }}>+{earnedXP} XP</span>
                        <span className="text-sm font-semibold" style={{ color: 'var(--duo-text-muted)' }}>kazandın!</span>
                    </div>
                </div>

                {/* Actions */}
                <div className="space-y-3 animate-slide-up stagger-4">
                    <button onClick={() => navigate('/quiz', { state: {} })}
                        className="btn-duo btn-duo-green w-full py-4 text-base">
                        <FiRepeat /> TEKRAR ÇÖZMEK
                    </button>
                    <button onClick={() => navigate('/')}
                        className="btn-duo btn-duo-outline w-full py-4 text-base">
                        <FiHome /> ANA SAYFAYA DÖN
                    </button>
                </div>
            </div>
        </div>
    )
}

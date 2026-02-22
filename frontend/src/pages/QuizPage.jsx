import { useState, useEffect } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import api from '../lib/api'
import { FiChevronRight, FiHelpCircle, FiX, FiBookmark } from 'react-icons/fi'

export default function QuizPage() {
    const location = useLocation()
    const navigate = useNavigate()
    const categoryId = location.state?.categoryId || null

    const [session, setSession] = useState(null)
    const [questions, setQuestions] = useState([])
    const [current, setCurrent] = useState(0)
    const [selected, setSelected] = useState(null)
    const [feedback, setFeedback] = useState(null) // { is_correct, correct_answer, explanation }
    const [score, setScore] = useState(0)
    const [loading, setLoading] = useState(true)
    const [startError, setStartError] = useState(null)
    const [answering, setAnswering] = useState(false)
    const [hint, setHint] = useState('')
    const [hintLoading, setHintLoading] = useState(false)
    const [isBookmarked, setIsBookmarked] = useState(false)
    const [bookmarking, setBookmarking] = useState(false)
    const [startTime] = useState(Date.now())

    useEffect(() => {
        startQuiz()
    }, [])

    const startQuiz = async () => {
        try {
            const { data } = await api.post('/quiz/start', {
                category_id: categoryId,
                question_count: 10,
            })
            setSession(data.session_id)
            setQuestions(data.questions)
        } catch (err) {
            const msg = err.response?.data?.detail || 'Sınav başlatılamadı'
            if (msg.toLowerCase().includes('yeterli soru bulunamadı')) {
                setStartError('Henüz bu kategoride çözebileceğiniz soru bulunmuyor. Lütfen daha sonra tekrar deneyin veya başka bir kategori seçin.')
            } else {
                setStartError(msg)
            }
        } finally {
            setLoading(false)
        }
    }

    const submitAnswer = async (answer) => {
        if (answering || feedback) return
        setSelected(answer)
        setAnswering(true)

        try {
            const { data } = await api.post('/quiz/answer', {
                session_id: session,
                question_id: questions[current].id,
                selected_answer: answer,
            })
            setFeedback(data)
            if (data.is_correct) setScore(s => s + 1)
        } catch (err) {
            console.error(err)
        } finally {
            setAnswering(false)
        }
    }

    const nextQuestion = () => {
        if (current + 1 >= questions.length) {
            finishQuiz()
        } else {
            setCurrent(c => c + 1)
            setSelected(null)
            setFeedback(null)
            setHint('')
            setIsBookmarked(false)
        }
    }

    const finishQuiz = async () => {
        const elapsed = Math.round((Date.now() - startTime) / 1000)
        try {
            const { data } = await api.post('/quiz/finish', {
                session_id: session,
                time_spent_seconds: elapsed,
            })
            navigate('/result', { state: { result: data, totalQuestions: questions.length } })
        } catch {
            navigate('/')
        }
    }

    const getHint = async () => {
        if (hintLoading || hint) return
        setHintLoading(true)
        try {
            const { data } = await api.post('/ai/hint', {
                question_id: questions[current].id,
            })
            setHint(data.hint)
        } catch {
            setHint('İpucu yüklenemedi')
        } finally {
            setHintLoading(false)
        }
    }

    const handleBookmark = async () => {
        if (bookmarking || isBookmarked) return
        setBookmarking(true)
        try {
            await api.post('/bookmarks/', { question_id: questions[current].id, note: 'Sınavdan kaydedildi' })
            setIsBookmarked(true)
        } catch (err) {
            console.error('Bookmark error:', err)
        } finally {
            setBookmarking(false)
        }
    }

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center p-4">
                <div className="text-center animate-pop">
                    <div className="text-5xl mb-4">🦷</div>
                    <p className="font-bold" style={{ color: 'var(--duo-text-muted)' }}>Sorular hazırlanıyor...</p>
                </div>
            </div>
        )
    }

    if (startError) {
        return (
            <div className="min-h-screen flex items-center justify-center p-4">
                <div className="text-center max-w-md w-full duo-card animate-pop border-x-4" style={{ borderColor: 'var(--duo-red)' }}>
                    <div className="text-5xl mb-4">😢</div>
                    <h2 className="text-xl font-bold mb-2">Başlangıç Hatası</h2>
                    <p className="mb-6 font-semibold" style={{ color: 'var(--duo-text-muted)' }}>{startError}</p>
                    <button onClick={() => navigate('/')} className="btn-duo btn-duo-outline w-full py-4 text-lg">
                        ANA SAYFAYA DÖN
                    </button>
                </div>
            </div>
        )
    }

    const q = questions[current]
    const progress = ((current + (feedback ? 1 : 0)) / questions.length) * 100
    const options = [
        { key: 'A', text: q.option_a },
        { key: 'B', text: q.option_b },
        { key: 'C', text: q.option_c },
        { key: 'D', text: q.option_d },
        { key: 'E', text: q.option_e },
    ]

    const getOptionClass = (key) => {
        if (!feedback) return selected === key ? 'selected' : ''
        if (key === feedback.correct_answer) return 'correct'
        if (key === selected && !feedback.is_correct) return 'wrong'
        return ''
    }

    return (
        <div className="min-h-screen flex flex-col pt-4">
            {/* Top Bar */}
            <div className="px-4 pb-2 max-w-4xl mx-auto w-full">
                <div className="flex items-center gap-4 mb-3">
                    <button onClick={() => navigate('/')} className="p-2 rounded-lg hover:bg-black/5 transition">
                        <FiX size={26} style={{ color: 'var(--duo-text-muted)' }} />
                    </button>
                    <div className="flex-1 duo-progress">
                        <div className="duo-progress-bar" style={{ width: `${progress}%` }} />
                    </div>
                    <div className="flex items-center gap-1.5 font-bold text-sm" style={{ color: 'var(--duo-green)' }}>
                        <span>⚡</span> {score * 10} XP
                    </div>
                </div>
                <div className="text-xs font-semibold text-center" style={{ color: 'var(--duo-text-muted)' }}>
                    {current + 1} / {questions.length}
                </div>
            </div>

            {/* Question Area */}
            <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full px-4 py-4">
                {/* Category badge */}
                <div className="mb-4">
                    <span className="inline-block px-3 py-1 rounded-full text-xs font-bold"
                        style={{ background: 'rgba(28,176,246,0.15)', color: 'var(--duo-blue)' }}>
                        {q.category_name}
                    </span>
                </div>

                {/* Question */}
                <div className="mb-6 animate-slide-up">
                    <h2 className="text-lg font-bold leading-relaxed">{q.question_text}</h2>
                </div>

                {/* Actions: Hint & Bookmark */}
                <div className="flex items-center gap-4 mb-4">
                    {!feedback && (
                        <button onClick={getHint} disabled={hintLoading || !!hint}
                            className="flex items-center gap-2 text-sm font-semibold transition-colors hover:text-gray-600"
                            style={{ color: hint ? 'var(--duo-yellow)' : 'var(--duo-text-muted)' }}>
                            <FiHelpCircle /> {hintLoading ? 'Yükleniyor...' : hint || 'İpucu Al (AI)'}
                        </button>
                    )}
                    <button onClick={handleBookmark} disabled={bookmarking || isBookmarked}
                        className="flex items-center gap-2 text-sm font-semibold transition-colors hover:text-gray-600 ml-auto"
                        style={{ color: isBookmarked ? 'var(--duo-blue)' : 'var(--duo-text-muted)' }}>
                        <FiBookmark className={isBookmarked ? 'fill-current' : ''} />
                        {bookmarking ? 'Kaydediliyor...' : isBookmarked ? 'Kaydedildi' : 'Soruyu Kaydet'}
                    </button>
                </div>
                {hint && !feedback && (
                    <div className="mb-4 p-3 rounded-lg text-sm animate-slide-up"
                        style={{ background: 'rgba(255,200,0,0.1)', border: '1px solid rgba(255,200,0,0.3)', color: 'var(--duo-yellow)' }}>
                        💡 {hint}
                    </div>
                )}

                {/* Options */}
                <div className="space-y-3 flex-1">
                    {options.map((opt, i) => (
                        <button key={opt.key}
                            onClick={() => submitAnswer(opt.key)}
                            disabled={!!feedback}
                            className={`quiz-option w-full text-left animate-slide-up stagger-${i + 1} ${getOptionClass(opt.key)}`}>
                            <span className="option-letter">{opt.key}</span>
                            <span className="flex-1">{opt.text}</span>
                            {feedback && opt.key === feedback.correct_answer && (
                                <span className="text-lg animate-pop">✅</span>
                            )}
                            {feedback && opt.key === selected && !feedback.is_correct && opt.key !== feedback.correct_answer && (
                                <span className="text-lg animate-shake">❌</span>
                            )}
                        </button>
                    ))}
                </div>
            </div>

            {/* Bottom Feedback */}
            {feedback && (
                <div className={`px-4 pb-4 pt-3 max-w-4xl mx-auto w-full animate-slide-up`}>
                    <div className={feedback.is_correct ? 'feedback-correct' : 'feedback-wrong'}>
                        <div className="flex items-center gap-2 mb-2">
                            <span className="text-xl">{feedback.is_correct ? '🎉' : '😢'}</span>
                            <span className="font-black text-lg"
                                style={{ color: feedback.is_correct ? 'var(--duo-green)' : 'var(--duo-red)' }}>
                                {feedback.is_correct ? 'Harika!' : 'Yanlış!'}
                            </span>
                        </div>
                        <p className="text-sm mb-3" style={{ color: 'var(--duo-text-muted)' }}>
                            {feedback.explanation}
                        </p>
                        <button onClick={nextQuestion} className={`btn-duo w-full py-3 ${feedback.is_correct ? 'btn-duo-green' : 'btn-duo-red'}`}>
                            {current + 1 >= questions.length ? 'SONUÇLARI GÖR' : 'DEVAM ET'} <FiChevronRight />
                        </button>
                    </div>
                </div>
            )}
        </div>
    )
}

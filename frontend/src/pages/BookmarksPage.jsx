import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../lib/api'
import { FiArrowLeft, FiBookmark, FiTrash2 } from 'react-icons/fi'

export default function BookmarksPage() {
    const navigate = useNavigate()
    const [bookmarks, setBookmarks] = useState([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        loadBookmarks()
    }, [])

    const loadBookmarks = async () => {
        try {
            const { data } = await api.get('/bookmarks/')
            setBookmarks(data)
        } catch (err) {
            console.error(err)
        } finally {
            setLoading(false)
        }
    }

    const removeBookmark = async (id) => {
        try {
            await api.delete(`/bookmarks/${id}`)
            setBookmarks(bms => bms.filter(b => b.id !== id))
        } catch (err) {
            console.error(err)
        }
    }

    return (
        <div className="min-h-screen" style={{ background: 'var(--duo-bg)' }}>
            <div className="duo-nav">
                <div className="max-w-screen-xl w-full mx-auto px-4 md:px-8 py-3 flex items-center gap-3">
                    <button onClick={() => navigate('/')} className="p-2 rounded-lg hover:bg-black/5 transition text-gray-400 hover:text-gray-600">
                        <FiArrowLeft size={20} />
                    </button>
                    <FiBookmark size={20} style={{ color: 'var(--duo-yellow)' }} />
                    <h1 className="font-black text-lg">Yer İşaretleri</h1>
                </div>
            </div>

            <div className="max-w-screen-xl w-full mx-auto px-4 md:px-8 py-6">
                {bookmarks.length === 0 && !loading ? (
                    <div className="text-center py-16 animate-slide-up">
                        <div className="text-5xl mb-4">🔖</div>
                        <h2 className="text-xl font-bold mb-2">Henüz yer işareti yok</h2>
                        <p style={{ color: 'var(--duo-text-muted)' }}>Quiz sırasında soruları işaretleyebilirsin</p>
                    </div>
                ) : (
                    <div className="space-y-3 animate-slide-up">
                        {bookmarks.map(bm => (
                            <div key={bm.id} className="duo-card">
                                <div className="flex items-start justify-between gap-3">
                                    <div className="flex-1">
                                        <span className="inline-block px-2 py-0.5 rounded text-xs font-bold mb-2"
                                            style={{ background: 'rgba(28,176,246,0.15)', color: 'var(--duo-blue)' }}>
                                            {bm.category_name}
                                        </span>
                                        <p className="text-sm font-semibold">{bm.question_text}</p>
                                        {bm.note && (
                                            <p className="text-xs mt-1" style={{ color: 'var(--duo-text-muted)' }}>📝 {bm.note}</p>
                                        )}
                                    </div>
                                    <button onClick={() => removeBookmark(bm.id)}
                                        className="p-2 rounded-lg hover:bg-black/5 transition flex-shrink-0"
                                        style={{ color: 'var(--duo-red)' }}>
                                        <FiTrash2 size={16} />
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    )
}

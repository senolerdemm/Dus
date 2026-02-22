import { createContext, useContext, useEffect, useState } from 'react'
import { supabase } from '../lib/supabase'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        if (!supabase) {
            setLoading(false)
            return
        }

        // Mevcut oturumu kontrol et
        supabase.auth.getSession().then(({ data: { session } }) => {
            if (session) {
                setUser(session.user)
                localStorage.setItem('access_token', session.access_token)
            }
            setLoading(false)
        })

        // Auth değişikliklerini dinle
        const { data: { subscription } } = supabase.auth.onAuthStateChange(
            (_event, session) => {
                if (session) {
                    setUser(session.user)
                    localStorage.setItem('access_token', session.access_token)
                } else {
                    setUser(null)
                    localStorage.removeItem('access_token')
                }
            }
        )

        return () => subscription.unsubscribe()
    }, [])

    const signUp = async (email, password, fullName) => {
        if (!supabase) throw new Error('Supabase bağlantısı kurulamadı')
        const { data, error } = await supabase.auth.signUp({
            email,
            password,
            options: { data: { full_name: fullName } },
        })
        if (error) throw error
        if (data.session) {
            localStorage.setItem('access_token', data.session.access_token)
        }
        return data
    }

    const signIn = async (email, password) => {
        if (!supabase) throw new Error('Supabase bağlantısı kurulamadı')
        const { data, error } = await supabase.auth.signInWithPassword({
            email,
            password,
        })
        if (error) throw error
        if (data.session) {
            localStorage.setItem('access_token', data.session.access_token)
        }
        return data
    }

    const signOut = async () => {
        if (supabase) await supabase.auth.signOut()
        localStorage.removeItem('access_token')
        setUser(null)
    }

    return (
        <AuthContext.Provider value={{ user, loading, signUp, signIn, signOut }}>
            {children}
        </AuthContext.Provider>
    )
}

export const useAuth = () => {
    const ctx = useContext(AuthContext)
    if (!ctx) throw new Error('useAuth must be used within AuthProvider')
    return ctx
}

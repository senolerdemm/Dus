import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseKey = import.meta.env.VITE_SUPABASE_KEY

if (!supabaseUrl || !supabaseKey) {
    console.error(
        '⚠️ VITE_SUPABASE_URL ve VITE_SUPABASE_KEY tanımlı değil!\n' +
        'frontend/.env dosyası oluşturun:\n' +
        'VITE_SUPABASE_URL=https://xxx.supabase.co\n' +
        'VITE_SUPABASE_KEY=eyJ...'
    )
}

export const supabase = supabaseUrl && supabaseKey
    ? createClient(supabaseUrl, supabaseKey)
    : null

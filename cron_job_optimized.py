#!/usr/bin/env python3
# cron_job_optimized.py - Genera cookie e salva su file JSON e Supabase

import asyncio
import os
import random
import gc
import json
from datetime import datetime
from supabase import create_client
from browser_use_sdk import AsyncBrowserUse
from playwright.async_api import async_playwright

# ==================== CONFIGURAZIONE ====================
# Leggi da variabili d'ambiente (impostate su Render)
KEYS_SUPABASE_URL = os.environ.get("KEYS_SUPABASE_URL", "https://kdqzfsmibquvvobjvjlj.supabase.co")
KEYS_SUPABASE_KEY = os.environ.get("KEYS_SUPABASE_KEY")

COOKIE_SUPABASE_URL = os.environ.get("COOKIE_SUPABASE_URL", "https://ofijopixtpwahgbwyutc.supabase.co")
COOKIE_SUPABASE_KEY = os.environ.get("COOKIE_SUPABASE_KEY")

DEFAULT_PASSWORD = "DDnmVV45!!"
MAX_ATTEMPTS = 7
PAUSE_BETWEEN_ACCOUNTS = 15
TIMEOUT = 90000

# Account EasyHits4U
ACCOUNTS = [
    {'email': 'sandrominori50+ulugarecexisa@gmail.com', 'name': 'ulugarecexisa'},
    # ... tutti i 35 account
]

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def get_all_working_keys():
    if not KEYS_SUPABASE_KEY:
        log("❌ KEYS_SUPABASE_KEY non impostata")
        return []
    try:
        supabase = create_client(KEYS_SUPABASE_URL, KEYS_SUPABASE_KEY)
        resp = supabase.table('browser_use_keys').select('api_key').eq('status', 'working').execute()
        if not resp.data:
            return []
        return [row['api_key'] for row in resp.data]
    except Exception as e:
        log(f"❌ Errore Supabase: {e}")
        return []

def get_random_working_key(exclude_keys=None):
    keys = get_all_working_keys()
    if not keys:
        return None
    if exclude_keys:
        keys = [k for k in keys if k not in exclude_keys]
        if not keys:
            return None
    return random.choice(keys)

def save_cookie_to_db(email, nome_utente, cookie_string, sesids, user_id):
    if not COOKIE_SUPABASE_KEY:
        return False
    try:
        supabase = create_client(COOKIE_SUPABASE_URL, COOKIE_SUPABASE_KEY)
        divella_format = f"{nome_utente}|{cookie_string}"
        data = {
            'email': email,
            'nome_utente': nome_utente,
            'account_name': nome_utente,
            'divella_format': divella_format,
            'cookie_string': cookie_string,
            'sesids': sesids,
            'user_id': user_id,
            'status': 'active',
            'updated_at': datetime.now().isoformat()
        }
        supabase.table('account_cookies').upsert(data, on_conflict='email').execute()
        log(f"   💾 Salvato su Supabase")
        return True
    except Exception as e:
        log(f"   ❌ Errore salvataggio: {e}")
        return False

# ... (resto del codice identico)

async def main():
    log("=" * 60)
    log("CRON JOB OTTIMIZZATO - GENERAZIONE COOKIE")
    log("=" * 60)
    
    if not KEYS_SUPABASE_KEY:
        log("❌ Variabile KEYS_SUPABASE_KEY non impostata")
        return
    
    # ... resto del main come prima ...

if __name__ == "__main__":
    asyncio.run(main())

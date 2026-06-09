#!/usr/bin/env python3
# cron_job_optimized.py - Versione ottimizzata

import asyncio
import os
import random
import gc
from datetime import datetime
from supabase import create_client
from browser_use_sdk import AsyncBrowserUse
from playwright.async_api import async_playwright

# ==================== CONFIGURAZIONE OTTIMIZZATA ====================
KEYS_SUPABASE_URL = os.environ.get("KEYS_SUPABASE_URL", "https://kdqzfsmibquvvobjvjlj.supabase.co")
KEYS_SUPABASE_KEY = os.environ.get("KEYS_SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")

COOKIE_SUPABASE_URL = os.environ.get("COOKIE_SUPABASE_URL", "https://ofijopixtpwahgbwyutc.supabase.co")
COOKIE_SUPABASE_KEY = os.environ.get("COOKIE_SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")

DEFAULT_PASSWORD = "DDnmVV45!!"

# PARAMETRI OTTIMIZZATI
MAX_ATTEMPTS = 7              # +2 tentativi
PAUSE_BETWEEN_ACCOUNTS = 15   # -5 secondi
TIMEOUT = 90000               # 90 secondi
TURNSTILE_WAIT = 30000        # 30 secondi per Turnstile

from config import ACCOUNTS

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def get_all_working_keys():
    try:
        supabase = create_client(KEYS_SUPABASE_URL, KEYS_SUPABASE_KEY)
        resp = supabase.table('browser_use_keys')\
            .select('api_key')\
            .eq('status', 'working')\
            .execute()
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

def update_key_status(api_key, status):
    try:
        supabase = create_client(KEYS_SUPABASE_URL, KEYS_SUPABASE_KEY)
        supabase.table('browser_use_keys')\
            .update({'status': status, 'last_used': datetime.now().isoformat()})\
            .eq('api_key', api_key)\
            .execute()
        log(f"   📝 Chiave {api_key[:20]}... -> {status}")
    except Exception as e:
        log(f"   ❌ Errore aggiornamento status: {e}")

def save_cookie_to_db(email, nome_utente, cookie_string, sesids, user_id):
    try:
        supabase = create_client(COOKIE_SUPABASE_URL, COOKIE_SUPABASE_KEY)
        divella_format = f"{nome_utente}|{cookie_string}"
        data = {
            'email': email,
            'nome_utente': nome_utente,
            'divella_format': divella_format,
            'cookie_string': cookie_string,
            'sesids': sesids,
            'user_id': user_id,
            'account_name': nome_utente,
            'status': 'active',
            'updated_at': datetime.now().isoformat()
        }
        supabase.table('account_cookies').upsert(data, on_conflict='email').execute()
        log(f"   💾 Salvato su Supabase")
        return True
    except Exception as e:
        log(f"   ❌ Errore salvataggio: {e}")
        return False

async def generate_cookie_for_account(api_key, account):
    email = account['email']
    nome = account['name']
    
    log(f"🚀 {nome} - {email}")
    log(f"   🔑 Chiave: {api_key[:20]}...")
    
    client = AsyncBrowserUse(api_key=api_key)
    profile = None
    
    try:
        profile = await client.profiles.create(name=f"cookie_{nome}")
        browser = await client.browsers.create(profile_id=profile.id)
        
        async with async_playwright() as p:
            pw_browser = await p.chromium.connect_over_cdp(browser.cdp_url)
            page = pw_browser.contexts[0].pages[0]
            
            await page.goto("https://www.easyhits4u.com/logon/", timeout=TIMEOUT)
            await page.wait_for_timeout(5000)
            
            # ATTESA PER TURNSTILE
            try:
                await page.wait_for_selector('input[name="cf-turnstile-response"]', timeout=TURNSTILE_WAIT)
                log(f"   🔐 Turnstile rilevato, attesa completamento...")
                await page.wait_for_timeout(3000)
            except:
                log(f"   ⚠️ Turnstile non rilevato, procedo...")
            
            await page.fill('#username', email)
            await page.fill('#password', DEFAULT_PASSWORD)
            await page.keyboard.press('Enter')
            
            await page.wait_for_timeout(45000)
            
            cookies = await page.context.cookies()
            cookie_string = '; '.join([f"{c['name']}={c['value']}" for c in cookies])
            sesids = next((c['value'] for c in cookies if c['name'] == 'sesids'), None)
            user_id = next((c['value'] for c in cookies if c['name'] == 'user_id'), None)
            
            if sesids and user_id:
                log(f"   ✅ OK - sesids={sesids}")
                save_cookie_to_db(email, nome, cookie_string, sesids, user_id)
                return True
            else:
                log(f"   ❌ Cookie non trovati")
                return False
            
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            log(f"   ⚠️ RATE LIMIT (429)")
            update_key_status(api_key, 'rate_limited')
            return "rate_limit"
        else:
            log(f"   ❌ Errore: {error_msg[:80]}")
            return False
    finally:
        if profile:
            try:
                await client.profiles.delete(profile.id)
                log(f"   🗑️ Profilo eliminato")
            except:
                pass
        try:
            await client.close()
            log(f"   🔒 Client chiuso")
        except:
            pass
        await asyncio.sleep(2)
        gc.collect()

async def main():
    log("=" * 60)
    log("CRON JOB OTTIMIZZATO - CAMBIO CHIAVE SU 429")
    log(f"Account totali: {len(ACCOUNTS)}")
    log(f"Tentativi massimi: {MAX_ATTEMPTS}")
    log(f"Timeout: {TIMEOUT//1000}s")
    log(f"Pausa tra account: {PAUSE_BETWEEN_ACCOUNTS}s")
    log("=" * 60)
    
    all_keys = get_all_working_keys()
    if not all_keys:
        log("❌ Nessuna chiave working")
        return
    
    log(f"🔑 Chiavi working disponibili: {len(all_keys)}")
    
    successi = 0
    falliti = 0
    
    for i, account in enumerate(ACCOUNTS):
        log(f"\n📌 [{i+1}/{len(ACCOUNTS)}] {account['name']}")
        
        used_keys = []
        
        for attempt in range(MAX_ATTEMPTS):
            api_key = get_random_working_key(exclude_keys=used_keys)
            if not api_key:
                log(f"   ❌ Nessuna chiave disponibile")
                break
            
            result = await generate_cookie_for_account(api_key, account)
            
            if result == True:
                successi += 1
                break
            elif result == "rate_limit":
                used_keys.append(api_key)
                log(f"   🔄 Tentativo {attempt+1}/{MAX_ATTEMPTS} - cambio chiave...")
                continue
            else:
                falliti += 1
                break
        
        if i < len(ACCOUNTS) - 1:
            log(f"   ⏳ Pausa {PAUSE_BETWEEN_ACCOUNTS} secondi...")
            await asyncio.sleep(PAUSE_BETWEEN_ACCOUNTS)
    
    log("\n" + "=" * 60)
    log("📊 RIEPILOGO FINALE")
    log("=" * 60)
    log(f"✅ Successi: {successi}")
    log(f"❌ Falliti: {falliti}")
    log(f"📊 Totale account: {len(ACCOUNTS)}")
    log(f"🎯 Percentuale successo: {successi/len(ACCOUNTS)*100:.1f}%")
    log("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
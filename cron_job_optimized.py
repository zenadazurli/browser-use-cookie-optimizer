#!/usr/bin/env python3
# cron_job_optimized.py - Genera cookie e salva in JSON

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
KEYS_SUPABASE_URL = "https://kdqzfsmibquvvobjvjlj.supabase.co"
KEYS_SUPABASE_KEY = "sb_publishable_bx4TPawDf5e3u07ko5YJcQ_dFkYfSQ-"

DEFAULT_PASSWORD = "DDnmVV45!!"
MAX_ATTEMPTS = 7
PAUSE_BETWEEN_ACCOUNTS = 15
TIMEOUT = 90000

# Account EasyHits4U
ACCOUNTS = [
    {'email': 'sandrominori50+ulugarecexisa@gmail.com', 'name': 'ulugarecexisa'},
    {'email': 'sandrominori50+ukageluli@gmail.com', 'name': 'ukageluli'},
    {'email': 'sandrominori50+ukaxiloki@gmail.com', 'name': 'ukaxiloki'},
    {'email': 'sandrominori50+uchikilaremu@gmail.com', 'name': 'uchikilaremu'},
    {'email': 'sandrominori50+ufrrmncrachinora@gmail.com', 'name': 'ufrrmncrachinora'},
    {'email': 'sandrominori50+unenomasagebebe@gmail.com', 'name': 'unenomasagebebe'},
    {'email': 'sandrominori50+uisnrnafwttvvceer@gmail.com', 'name': 'uisnrnafwttvvceer'},
    {'email': 'sandrominori50+ujuenpaorgl@gmail.com', 'name': 'ujuenpaorgl'},
    {'email': 'sandrominori50+uvuoobe@gmail.com', 'name': 'uvuoobe'},
    {'email': 'sandrominori50+uoovoge@gmail.com', 'name': 'uoovoge'},
    {'email': 'sandrominori50+ukafifoko@gmail.com', 'name': 'ukafifoko'},
    {'email': 'sandrominori50+ubozogaza@gmail.com', 'name': 'ubozogaza'},
    {'email': 'sandrominori50+udapasa@gmail.com', 'name': 'udapasa'},
    {'email': 'sandrominori50+uluglqupgbe@gmail.com', 'name': 'uluglqupgbe'},
    {'email': 'sandrominori50+unaglbene@gmail.com', 'name': 'unaglbene'},
    {'email': 'sandrominori50+umachizo@gmail.com', 'name': 'umachizo'},
    {'email': 'sandrominori50+ulaaacummgl@gmail.com', 'name': 'ulaaacummgl'},
    {'email': 'sandrominori50+ufrrageboki@gmail.com', 'name': 'ufrrageboki'},
    {'email': 'sandrominori50+unomama@gmail.com', 'name': 'unomama'},
    {'email': 'sandrominori50+ucuquaacuge@gmail.com', 'name': 'ucuquaacuge'},
    {'email': 'sandrominori50+ukufeno@gmail.com', 'name': 'ukufeno'},
    {'email': 'sandrominori50+ukitulobbqu@gmail.com', 'name': 'ukitulobbqu'},
    {'email': 'sandrominori50+udaglkilerm@gmail.com', 'name': 'udaglkilerm'},
    {'email': 'sandrominori50+usaadgapa@gmail.com', 'name': 'usaadgapa'},
    {'email': 'sandrominori50+uqumopgne@gmail.com', 'name': 'uqumopgne'},
    {'email': 'sandrominori50+upgximamazo@gmail.com', 'name': 'upgximamazo'},
    {'email': 'sandrominori50+uboooggnale@gmail.com', 'name': 'uboooggnale'},
    {'email': 'sandrominori50+uenqufetr@gmail.com', 'name': 'uenqufetr'},
    {'email': 'sandrominori50+umumure@gmail.com', 'name': 'umumure'},
    {'email': 'sandrominori50+udabbpgnc@gmail.com', 'name': 'udabbpgnc'},
    {'email': 'sandrominori50+uquliufnemu@gmail.com', 'name': 'uquliufnemu'},
    {'email': 'sandrominori50+ukikreazala@gmail.com', 'name': 'ukikreazala'},
    {'email': 'sandrominori50+ulibbra@gmail.com', 'name': 'ulibbra'},
    {'email': 'sandrominori50+uzarawalita@gmail.com', 'name': 'uzarawalita'},
    {'email': 'sandrominori50+ufitamina@gmail.com', 'name': 'ufitamina'},
]

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def get_all_working_keys():
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
            
            # Attesa Turnstile
            try:
                await page.wait_for_selector('input[name="cf-turnstile-response"]', timeout=30000)
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
                divella_format = f"{nome}|{cookie_string}"
                log(f"   ✅ OK - sesids={sesids}")
                return True, divella_format, cookie_string, sesids, user_id
            else:
                log(f"   ❌ Cookie non trovati")
                return False, None, None, None, None
            
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            log(f"   ⚠️ RATE LIMIT (429)")
            return "rate_limit", None, None, None, None
        else:
            log(f"   ❌ Errore: {error_msg[:80]}")
            return False, None, None, None, None
    finally:
        if profile:
            try:
                await client.profiles.delete(profile.id)
            except:
                pass
        try:
            await client.close()
        except:
            pass
        await asyncio.sleep(2)
        gc.collect()

async def main():
    log("=" * 60)
    log("CRON JOB OTTIMIZZATO - GENERAZIONE COOKIE")
    log("=" * 60)
    
    all_keys = get_all_working_keys()
    if not all_keys:
        log("❌ Nessuna chiave working")
        return
    
    log(f"🔑 Chiavi working: {len(all_keys)}")
    
    successi = 0
    falliti = 0
    cookies_list = []  # Lista per salvare i cookie per Divella
    
    for i, account in enumerate(ACCOUNTS):
        log(f"\n📌 [{i+1}/{len(ACCOUNTS)}] {account['name']}")
        
        used_keys = []
        success = False
        
        for attempt in range(MAX_ATTEMPTS):
            api_key = get_random_working_key(exclude_keys=used_keys)
            if not api_key:
                break
            
            result, divella_format, cookie_string, sesids, user_id = await generate_cookie_for_account(api_key, account)
            
            if result == True:
                success = True
                successi += 1
                # Salva cookie per Divella
                cookies_list.append({
                    'name': account['name'],
                    'email': account['email'],
                    'divella_format': divella_format,
                    'sesids': sesids,
                    'user_id': user_id
                })
                break
            elif result == "rate_limit":
                used_keys.append(api_key)
                continue
            else:
                falliti += 1
                break
        
        if not success:
            falliti += 1
        
        if i < len(ACCOUNTS) - 1:
            await asyncio.sleep(PAUSE_BETWEEN_ACCOUNTS)
    
    # Salva i cookie in file JSON per Divella
    try:
        with open("active_cookies.json", "w") as f:
            json.dump(cookies_list, f, indent=2)
        log(f"\n💾 active_cookies.json salvato con {len(cookies_list)} cookie")
    except Exception as e:
        log(f"⚠️ Errore salvataggio file: {e}")
    
    log("\n" + "=" * 60)
    log("📊 RIEPILOGO FINALE")
    log("=" * 60)
    log(f"✅ Successi: {successi}")
    log(f"❌ Falliti: {falliti}")
    log(f"📊 Totale: {len(ACCOUNTS)}")
    log("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())

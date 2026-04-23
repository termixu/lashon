#!/usr/bin/env python3
"""Загрузка всех источников (Sefaria, BDB) в локальный кэш"""

import sys
from pathlib import Path

# Добавляем корень проекта в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.sources import TanakhSources

def main():
    print("🕯️ HaLev HaLashon — Загрузка источников\n")
    
    sources = TanakhSources()
    
    # Проверка Sefaria
    print("📖 Проверка Sefaria (ТаНаХ)...")
    verse = sources.sefaria.get_verse("Genesis", 1, 1)
    if verse and "Not found" not in verse:
        print(f"   ✅ Sefaria загружена. Пример: Берешит 1:1 → {verse[:50]}...")
    else:
        print("   ❌ Ошибка загрузки Sefaria")
    
    # Проверка BDB
    print("\n📚 Проверка BDB (этимология)...")
    bdb_test = sources.bdb.get_root_by_letters("חסד")
    if bdb_test:
        print(f"   ✅ BDB загружен. Корень 'חסד' → {bdb_test.get('meaning', '')[:50]}...")
    else:
        print("   ❌ Ошибка загрузки BDB")
    
    # Проверка морфологии
    print("\n🔍 Проверка MORPHEME (морфология)...")
    morph_test = sources.morpheme.parse_word("בָּרָא")
    if "error" not in morph_test:
        print(f"   ✅ MORPHEME работает. 'בָּרָא' → корень: {morph_test.get('root')}")
    else:
        print(f"   ⚠️ MORPHEME не установлен. Установите: pip install morpheme")
    
    print("\n✅ Все источники готовы к работе!")

if __name__ == "__main__":
    main()
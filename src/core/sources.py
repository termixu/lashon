"""Sources — подключение к Sefaria, BDB, морфологии"""

import json
import requests
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
from functools import lru_cache

# ============================================================
# 1. Sefaria — ТаНаХ на иврите (основной источник)
# ============================================================

SEFARIA_TANAKH_URL = "https://raw.githubusercontent.com/Sefaria/Sefaria-Export/master/json/Tanakh.json"
SEFARIA_BOOKS_URL = "https://raw.githubusercontent.com/Sefaria/Sefaria-Export/master/json/books.json"

class SefariaClient:
    """Клиент для работы с Sefaria API и экспортом"""
    
    def __init__(self, cache_dir="data/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.tanakh = None
        self._load_tanakh()
    
    def _load_tanakh(self):
        """Загружает ТаНаХ из кэша или с GitHub"""
        cache_file = self.cache_dir / "tanakh.json"
        
        if cache_file.exists():
            with open(cache_file, "r", encoding="utf-8") as f:
                self.tanakh = json.load(f)
        else:
            print("Загрузка ТаНаХа из Sefaria...")
            response = requests.get(SEFARIA_TANAKH_URL)
            self.tanakh = response.json()
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(self.tanakh, f, ensure_ascii=False, indent=2)
            print("ТаНаХ сохранён в кэш")
    
    def get_verse(self, book: str, chapter: int, verse: int) -> str:
        """Возвращает стих на иврите
        
        Пример: get_verse("Genesis", 1, 1) -> "בְּרֵאשִׁית בָּרָא אֱלֹהִים..."
        """
        # Нормализация названия книги (Genesis -> Bereshit)
        hebrew_book = self._to_hebrew_book_name(book)
        
        try:
            book_data = self.tanakh[hebrew_book]
            chapter_data = book_data[str(chapter)]
            verse_text = chapter_data[str(verse)]
            return verse_text
        except (KeyError, TypeError):
            return f"[Не найдено: {book} {chapter}:{verse}]"
    
    def _to_hebrew_book_name(self, english_name: str) -> str:
        """Конвертирует английское название книги в ивритское"""
        mapping = {
            "Genesis": "Bereshit",
            "Exodus": "Shemot",
            "Leviticus": "Vayikra",
            "Numbers": "Bamidbar",
            "Deuteronomy": "Devarim",
            "Isaiah": "Yeshayahu",
            "Jeremiah": "Yirmeyahu",
            "Ezekiel": "Yechezkel",
            "Psalms": "Tehilim",
            "Proverbs": "Mishlei",
            "Job": "Iyov",
            "Daniel": "Daniel",
            "Ezra": "Ezra",
            "Nehemiah": "Nechemyah",
            "Chronicles": "Divrei Hayamim"
        }
        return mapping.get(english_name, english_name)
    
    def get_chapter(self, book: str, chapter: int) -> Dict[int, str]:
        """Возвращает всю главу"""
        hebrew_book = self._to_hebrew_book_name(book)
        return self.tanakh[hebrew_book][str(chapter)]


# ============================================================
# 2. BDB (Brown-Driver-Briggs) — этимологический словарь
# ============================================================

BDB_URL = "https://raw.githubusercontent.com/openscriptures/HebrewLexicon/master/bdb.json"

class BDBAnalyzer:
    """Анализ корней и значений слов"""
    
    def __init__(self, cache_dir="data/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.lexicon = self._load_bdb()
    
    def _load_bdb(self):
        """Загружает BDB из кэша или с GitHub"""
        cache_file = self.cache_dir / "bdb.json"
        
        if cache_file.exists():
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        
        print("Загрузка BDB словаря...")
        response = requests.get(BDB_URL)
        lexicon = response.json()
        
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(lexicon, f, ensure_ascii=False, indent=2)
        
        print("BDB сохранён в кэш")
        return lexicon
    
    def get_root(self, word: str) -> Optional[Dict]:
        """Возвращает информацию о корне слова"""
        # Простой поиск по слову (можно улучшить)
        word_clean = word.strip()
        for entry in self.lexicon:
            if entry.get("word") == word_clean:
                return entry
        return None
    
    def get_root_by_letters(self, root_letters: str) -> Optional[Dict]:
        """Поиск корня по трём буквам (например, 'חסד')"""
        for entry in self.lexicon:
            if entry.get("root") == root_letters:
                return entry
        return None


# ============================================================
# 3. Морфологический анализ (MORPHEME)
# ============================================================

try:
    from morpheme import parse as morpheme_parse
    MORPHEME_AVAILABLE = True
except ImportError:
    MORPHEME_AVAILABLE = False
    print("Предупреждение: morpheme не установлен. Установите: pip install morpheme")

class MorphemeAnalyzer:
    """Обёртка над MORPHEME для морфологического разбора"""
    
    def parse_word(self, word: str) -> Dict:
        """Разбирает слово на корень, биньян, время, лицо"""
        if not MORPHEME_AVAILABLE:
            return {"error": "morpheme not installed", "word": word}
        
        try:
            result = morpheme_parse(word)
            return {
                "word": word,
                "root": result.get("root", ""),
                "binyan": result.get("binyan", ""),
                "tense": result.get("tense", ""),
                "person": result.get("person", ""),
                "gender": result.get("gender", ""),
                "number": result.get("number", "")
            }
        except Exception as e:
            return {"error": str(e), "word": word}


# ============================================================
# 4. Септуагинта (греческий перевод) — через API
# ============================================================

SEPTUAGINT_URL = "https://raw.githubusercontent.com/eliranwong/OpenGreekNT/master/LXX/JSON"

class SeptuagintClient:
    """Клиент для получения греческого текста Септуагинты"""
    
    def __init__(self, cache_dir="data/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.texts = {}
    
    def get_verse(self, book: str, chapter: int, verse: int) -> str:
        """Возвращает греческий текст стиха"""
        # Пока заглушка — можно позже добавить реальный API
        return f"[LXX: {book} {chapter}:{verse} — требуется интеграция]"


# ============================================================
# 5. Вульгата (латынь) — через API
# ============================================================

class VulgateClient:
    """Клиент для получения латинского текста Вульгаты"""
    
    def get_verse(self, book: str, chapter: int, verse: int) -> str:
        """Возвращает латинский текст стиха"""
        # Пока заглушка
        return f"[Vulgate: {book} {chapter}:{verse} — требуется интеграция]"


# ============================================================
# 6. Главный класс, объединяющий все источники
# ============================================================

class TanakhSources:
    """Единый вход ко всем источникам (Sefaria, BDB, морфология, LXX, Vulgate)"""
    
    def __init__(self):
        self.sefaria = SefariaClient()
        self.bdb = BDBAnalyzer()
        self.morpheme = MorphemeAnalyzer()
        self.septuagint = SeptuagintClient()
        self.vulgate = VulgateClient()
    
    def get_verse_with_parallels(self, book: str, chapter: int, verse: int) -> Dict:
        """Возвращает стих со всеми параллельными текстами"""
        return {
            "reference": f"{book} {chapter}:{verse}",
            "hebrew_mt": self.sefaria.get_verse(book, chapter, verse),
            "greek_lxx": self.septuagint.get_verse(book, chapter, verse),
            "latin_vulgate": self.vulgate.get_verse(book, chapter, verse)
        }
    
    def analyze_word(self, word: str) -> Dict:
        """Полный анализ слова: корень, значение, морфология"""
        morphology = self.morpheme.parse_word(word)
        root = morphology.get("root", "")
        
        if root:
            bdb_info = self.bdb.get_root_by_letters(root)
        else:
            bdb_info = None
        
        return {
            "word": word,
            "morphology": morphology,
            "root_meaning": bdb_info.get("meaning", "") if bdb_info else "",
            "root_definition": bdb_info.get("definition", "") if bdb_info else ""
        }


# ============================================================
# Тестовый запуск
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Загрузка источников...")
    print("=" * 60)
    
    sources = TanakhSources()
    
    # Тест получения стиха из Sefaria
    verse = sources.sefaria.get_verse("Genesis", 1, 1)
    print(f"\n📖 Bereshit 1:1 из Sefaria:\n{verse}\n")
    
    # Тест этимологии
    word_analysis = sources.analyze_word("חֶסֶד")
    print(f"\n📖 Анализ слова 'חֶסֶד':")
    print(json.dumps(word_analysis, ensure_ascii=False, indent=2))
    
    print("\n✅ Источники готовы к работе")
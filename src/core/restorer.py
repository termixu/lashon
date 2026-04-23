"""Restorer — обнаружение искажений и восстановление текста"""

import json
from difflib import SequenceMatcher
from typing import Dict, List, Optional
from src.core.sources import TanakhSources

class TextRestorer:
    """Восстанавливает оригинальный ивритский текст, очищая от греческих/латинских искажений"""
    
    def __init__(self):
        self.sources = TanakhSources()
        self.load_corruption_patterns()
    
    def load_corruption_patterns(self):
        """Загружает базу известных искажений"""
        # Можно позже загружать из JSON
        self.corruption_patterns = {
            "greek": [
                {"hebrew": "בָּרָא", "greek": "ἐποίησεν", "issue": "creatio ex nihilo"},
                {"hebrew": "חֶסֶד", "greek": "ἔλεος", "issue": "mercy instead of covenant loyalty"},
                {"hebrew": "תּוֹרָה", "greek": "νόμος", "issue": "law instead of teaching"},
                {"hebrew": "צְדָקָה", "greek": "ἐλεημοσύνη", "issue": "alms instead of righteousness"},
            ],
            "latin": [
                {"hebrew": "יְהוָה", "latin": "Dominus", "issue": "name replaced with title 'Lord'"},
                {"hebrew": "מָשִׁיחַ", "latin": "Christus", "issue": "anointed become title"},
            ]
        }
    
    def detect_corruptions(self, book: str, chapter: int, verse: int) -> Dict:
        """Анализирует стих на наличие искажений"""
        
        verse_data = self.sources.get_verse_with_parallels(book, chapter, verse)
        hebrew_text = verse_data["hebrew_mt"]
        
        detected = []
        
        # Проверка каждого слова на известные искажения
        words = hebrew_text.split()
        for word in words:
            # Греческие искажения
            for pattern in self.corruption_patterns["greek"]:
                if pattern["hebrew"] in word or word == pattern["hebrew"]:
                    detected.append({
                        "type": "greek",
                        "hebrew_word": pattern["hebrew"],
                        "corrupted_to": pattern.get("greek", ""),
                        "issue": pattern["issue"],
                        "confidence": 0.85
                    })
            
            # Латинские искажения
            for pattern in self.corruption_patterns["latin"]:
                if pattern["hebrew"] in word or word == pattern["hebrew"]:
                    detected.append({
                        "type": "latin",
                        "hebrew_word": pattern["hebrew"],
                        "corrupted_to": pattern.get("latin", ""),
                        "issue": pattern["issue"],
                        "confidence": 0.90
                    })
        
        return {
            "reference": f"{book} {chapter}:{verse}",
            "hebrew_text": hebrew_text,
            "detected_corruptions": detected,
            "corruption_count": len(detected),
            "severity": "high" if len(detected) > 2 else "medium" if len(detected) > 0 else "none"
        }
    
    def restore_verse(self, book: str, chapter: int, verse: int) -> Dict:
        """Восстанавливает стих, заменяя искажения на оригинальные значения"""
        
        detection = self.detect_corruptions(book, chapter, verse)
        restored_text = detection["hebrew_text"]
        
        for corruption in detection["detected_corruptions"]:
            original = corruption["hebrew_word"]
            # Получаем истинное значение из BDB
            root_info = self.sources.bdb.get_root_by_letters(original)
            true_meaning = root_info.get("meaning", original) if root_info else original
            
            # Добавляем комментарий восстановления
            corruption["restored_meaning"] = true_meaning
        
        return {
            "reference": detection["reference"],
            "original_text": detection["hebrew_text"],
            "corruptions": detection["detected_corruptions"],
            "severity": detection["severity"],
            "restoration_notes": self._generate_notes(detection["detected_corruptions"])
        }
    
    def _generate_notes(self, corruptions: List[Dict]) -> str:
        """Генерирует пояснительные заметки по восстановлению"""
        if not corruptions:
            return "Искажений не обнаружено. Текст соответствует масоретской традиции."
        
        notes = []
        for c in corruptions:
            notes.append(f"• {c['hebrew_word']}: {c['issue']} → восстановлено как '{c.get('restored_meaning', c['hebrew_word'])}'")
        
        return "\n".join(notes)
    
    def compare_translations(self, book: str, chapter: int, verse: int) -> Dict:
        """Сравнивает MT, LXX, Vulgate для одного стиха"""
        
        verse_data = self.sources.get_verse_with_parallels(book, chapter, verse)
        
        hebrew = verse_data["hebrew_mt"]
        greek = verse_data["greek_lxx"]
        latin = verse_data["latin_vulgate"]
        
        return {
            "reference": f"{book} {chapter}:{verse}",
            "masoretic_text": hebrew,
            "septuagint": greek,
            "vulgate": latin,
            "hebrew_greek_similarity": SequenceMatcher(None, hebrew, greek).ratio(),
            "hebrew_latin_similarity": SequenceMatcher(None, hebrew, latin).ratio(),
            "note": "Чем ниже сходство — тем выше вероятность искажения в греческом/латинском переводе"
        }


# ============================================================
# Тестовый запуск
# ============================================================

if __name__ == "__main__":
    restorer = TextRestorer()
    
    # Тест 1: Обнаружение искажений
    print("=" * 60)
    print("1. Обнаружение искажений в Берешит 1:1")
    print("=" * 60)
    result = restorer.detect_corruptions("Genesis", 1, 1)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # Тест 2: Восстановление
    print("\n" + "=" * 60)
    print("2. Восстановление значения слов")
    print("=" * 60)
    restored = restorer.restore_verse("Genesis", 1, 1)
    print(f"Стих: {restored['reference']}")
    print(f"Искажений найдено: {len(restored['corruptions'])}")
    print(f"Заметки:\n{restored['restoration_notes']}")
    
    # Тест 3: Сравнение переводов
    print("\n" + "=" * 60)
    print("3. Сравнение переводов (MT vs LXX vs Vulgate)")
    print("=" * 60)
    comparison = restorer.compare_translations("Genesis", 1, 1)
    print(json.dumps(comparison, ensure_ascii=False, indent=2))
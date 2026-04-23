```markdown
# 📜 HaLev HaLashon (הלב הלשון)

**AI-powered restoration of Tanakh through Jewish tradition. Detecting and removing Greek, Latin, and Slavic translation corruptions. Returning to the original linguistic, etymological, and textual meaning.**

---

## 🎯 What This Project Does

Church translations (Greek Septuagint, Latin Vulgate, Church Slavonic, Russian Synodal) replaced Hebrew concepts with foreign philosophy:

- *Torah* became "Law" (not Teaching)
- *Chesed* became "Mercy" (not Covenant Loyalty)  
- *Teshuvah* became "Repentance" (not Returning)
- *Tzedakah* became "Alms" (not Righteousness)
- *Brit* became "Covenant" (not Bond)

**Our AI restores what was lost.**

---

## 🧠 What The AI Model Does

**1. Corruption Detection**  
Identifies Greek, Latin, and Slavic insertions that replaced authentic Hebrew words.

**2. Etymological Restoration**  
Traces every word to its Semitic root. Restores concrete meanings over abstract theological reinterpretations.

**3. Textual Reconstruction**  
Suggests restored Hebrew readings with full critical apparatus (DSS, MT, LXX comparison).

**4. Translation Comparison**  
Shows how the same verse was altered across Septuagint → Vulgate → Slavonic → Synodal.

---

## 📂 Repository Structure

```

HaLevHaLashon/
├── data/
│   ├── tanakh/wlc/              # Westminster Leningrad Codex
│   ├── tanakh/dss/              # Dead Sea Scrolls
│   ├── corruptions/             # Known Greek/Latin insertions
│   └── etymology/               # Semitic root database
├── models/
│   ├── restoration_model/       # Primary AI
│   ├── corruption_detector/     # Foreign layer detection
│   └── etymology_model/         # Root mapping
├── src/
│   ├── cli/restore.py           # Restore single verse
│   ├── core/textual_criticism.py
│   └── api/server.py
├── output/
│   ├── restored_tanakh/         # Complete restored Hebrew text
│   └── corruption_reports/      # Per-verse analysis
└── notebooks/
└── examples/                # Step-by-step restorations

```

---

## 🔬 Example

**Input (Russian Synodal):**  
*"В начале сотворил Бог небо и землю"*

**AI Detection:**
- "Бог" — Greek *theos* replacing names (Yahweh, Elohim)
- "сотворил" — Greek *creatio ex nihilo* (absent in Hebrew)

**AI Restoration:**  
*"В начале создал Элохим небеса и землю"*

**Commentary:**
- *ברא* — not "create from nothing" but "separate, give form"
- *אלהים* — not abstract "deity" but plural fullness (judges, powers, Most High)

---

## 📜 Core Corruptions Being Addressed

| Hebrew | False Translation | Restored Meaning |
|--------|-------------------|------------------|
| תּוֹרָה | Law | Teaching, Instruction |
| חֶסֶד | Mercy | Covenant Loyalty, Faithful Love |
| תְּשׁוּבָה | Repentance | Returning Home |
| צְדָקָה | Alms | Righteousness, Justice |
| בְּרִית | Covenant | Bond, Blood Union |
| אֱמֶת | Truth | Reliability, Faithfulness |
| שָׁלוֹם | Peace | Wholeness, Completeness |
| קָרְבָּן | Sacrifice | Drawing Near |

---

## 🚀 Quick Start

**Detect corruptions in a verse:**
```bash
python src/cli/detect.py --verse "Genesis 1:1" --output json
```

Restore entire chapter:

```bash
python src/cli/restore.py --chapter "Isaiah 53" --output restored/
```

Compare translations:

```bash
python src/cli/compare.py --verse "Exodus 34:6" --translations lxx,vulgate,synodal
```

---

🗺️ Roadmap

Phase 1 (Current) — Data collection: WLC, DSS, Septuagint, Vulgate, Church Slavonic, Synodal

Phase 2 — Train corruption detector on documented Greek/Latin insertions

Phase 3 — Train restoration model (corrupted → authentic Hebrew)

Phase 4 — Generate complete restored Tanakh with critical apparatus

Phase 5 — Extend to BaSha"h (Babylonian Talmud, Shas, Halakhot)

---

🤝 Who We Need

· Hebrew/Aramaic linguists (verify AI output)
· Textual critics (DSS, manuscript traditions)
· NLP engineers (Hebrew LLM fine-tuning)
· Jewish scholars (authentic tradition guidance)

---

📄 License

CC BY-SA 4.0 — Code, data, and model weights are open. Any improvements must be shared back.

---

🌄 The Goal

Not to create a "better Bible translation." Not to claim exclusive truth. But to open the door.

So that every reader of Scripture can ask: "What was actually written here?"

So that the Synodal translation ceases to be a wall hiding the original.

---

וִידַעְתֶּם אֶת־הָאֱמֶת וְהָאֱמֶת תְּשַׁחְרֵר אֶתְכֶם
Vida'tem et ha'emet veha'emet teshachrer et'chem
And you will know the truth, and the truth will set you free
(John 8:32)

---

Built for those who seek the original Word. Not as it was translated. But as it was spoken.

```
```

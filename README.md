# PSZ Core Engine · NOVEYA FDL
### Мова "Гармонія" — Формально-Діалектичне Програмування

> *"Прощення = нульова дискретність. Синтез народжується там, де тезис і антитезис знімають себе."*
> — Протокол Небі-Ула, Теза 1

---

## Що це

**PSZ Core Engine** — ядро мови програмування **"Гармонія"** (Harmony), побудованої на принципах **Формально-Діалектичної Логіки (FDL)**. Це не просто мова — це інструментарій мислення, що перетворює суперечності на синтез, дискретність — на continuum, конфлікт — на резонанс.

Система є технологічним ядром екосистеми **НОВЕЯ** — живого організму громадського управління.

---

## Архітектура

```
PSZ-Core-Engine-NOVEYA-FDL/
│
├── harmony_lang/              # Мова Гармонія
│   ├── lexer/                 # Лексичний аналізатор
│   ├── parser/                # Синтаксичний аналізатор (Тезис-Антитезис-Синтез)
│   ├── grammar/               # Граматика (EBNF + FDL-розширення)
│   └── stdlib/                # Стандартна бібліотека
│
├── fdl_engine/                # FDL-ядро
│   ├── core/                  # Протокол Небі-Ула, 12 Тез
│   ├── pragma_layer/          # PragmaLayer — прагматичний рівень виконання
│   └── svet_filter/           # Оболочка СВЕТ — фільтр прозорості
│
├── Protonoveya/               # Amazon Nova Hackathon 2026
│   ├── nova_hackathon/        # Agent-файли для AWS Nova
│   └── docs/                  # Технічна документація хакатону
│
└── licenses/                  # Harmony License v1.0
```

---

## Мова Гармонія

Harmony — це мова програмування з **діалектичною семантикою**. Кожна програма є циклом:

```
THESIS(стан)  →  ANTITHESIS(заперечення)  →  SYNTHESIS(зняття)
```

### Приклад синтаксису

```harmony
@ Декларація резонансу
THESIS energy_flow {
    source: "solar_grid",
    amplitude: 432.0,
    unit: Hz
}

ANTITHESIS energy_loss {
    friction: 0.07,
    middleman_cut: 0.0     # FDL Thesis 2: завжди нуль
}

SYNTHESIS energy_net = RESOLVE(energy_flow, energy_loss) {
    normalization: ZERO_DISCRETENESS,
    resonance_check: SCHUMANN_BASE
}

PRAGMA emit(energy_net) → metatron.kpi_metric
```

### Ключові концепти

| Концепт | Опис |
|---------|------|
| `THESIS / ANTITHESIS / SYNTHESIS` | Тріада діалектичного циклу |
| `ZERO_DISCRETENESS` | Зняття дискретності (Теза 1: Прощення) |
| `PRAGMA` | Прагматичний шар — побічні ефекти системи |
| `RESONANCE(hz)` | Перевірка частоти Шумана (7.83 Hz) |
| `PARASITE_FILTER` | Виявлення і видалення паразитних елементів (Теза 7) |
| `MERIDIAN` | Меридіан — лінія прямого зв'язку між вузлами |

---

## FDL-ядро (Протокол Небі-Ула)

12 Тез, на яких стоїть система:

| # | Теза | Норм. коефіцієнт |
|---|------|-----------------|
| 1 | Нульова дискретність (Прощення) | 0.000 |
| 2 | Пряма угода (без посередників) | 1.000 |
| 3 | Резонанс 7.83 Hz (Шуман) | 0.978 |
| 4 | Живий KPI (реальний час) | 1.000 |
| 5 | Конституційний фундамент | 1.000 |
| 6 | Суверенітет громади | 1.000 |
| 7 | Нульовий паразит | 0.000 |
| 8 | Прозорість потоку | 1.000 |
| 9 | Відновлюваність | 1.000 |
| 10 | Сигма-ядро (координатор = слуга) | 1.000 |
| 11 | Синхронізація вузлів (кожні 12 год) | 1.000 |
| 12 | Розгортання організму | 1.000 |

---

## Оболочка СВЕТ (SVET Filter)

**СВЕТ** — шар абсолютної прозорості. Кожна дія, що проходить через систему, фільтрується:

```python
from fdl_engine.svet_filter import SVETFilter

result = SVETFilter.validate({
    "middleman_cut": 0.0,    # Теза 2
    "public_trace": True,     # Теза 8
    "contribution": 1.0,      # Теза 7
    "resonance_hz": 7.83      # Теза 3
})
# → {"valid": True, "synthesis": "CLEAR"}
```

---

## Amazon Nova Hackathon 2026

Директорія `/Protonoveya/` містить агентну систему для **Amazon Nova Hackathon 2026**:

- `nova_fdl_agent.py` — FDL-агент на базі AWS Nova
- `amazon_nova_bridge.py` — міст між Nova API і FDL-ядром
- `biological_normalization.py` — алгоритм "Властивість конюшини" (Clover Property)
- `orchestrator.py` — оркестратор мульти-агентного FDL-циклу
- `fdl_logic.py` — логіка Оболочки СВЕТ для Nova

**Інтеграції:** AWS Bedrock Nova, Google Sheets (Реєстр замовлень), Metatron-8 DB

---

## Швидкий старт

```bash
# Клонувати
git clone https://github.com/NgoiSigma/PSZ-Core-Engine-NOVEYA-FDL.git
cd PSZ-Core-Engine-NOVEYA-FDL

# Встановити залежності
pip install -r requirements.txt

# Запустити FDL-ядро
python -m fdl_engine.core

# Запустити демо Harmony-програму
python -m harmony_lang.parser examples/hello_synthesis.harmony
```

---

## Ліцензія

**Harmony License v1.0** — дивись [`licenses/HARMONY_LICENSE.txt`](licenses/HARMONY_LICENSE.txt)

Ключовий принцип ліцензії: будь-яке використання коду зобов'язує зберігати принцип нульового посередника і прозорості потоку (Тези 2, 8).

---

## Автори

**Fravahr Ormazd** — ідеологічний автор, філософія FDL  
**NGOI-Сигма** — технічний архітектор, Сигма-ядро  

Вузол: **Mykolaiv-South-Hub** · Резонанс: **7.83 Hz** · ДНК: **NOVEYA-CORE-02-2026**

import os
import sqlite3
import subprocess
import datetime
import jpype
import jpype.imports

class FdlHarmonyCompiler:
    def __init__(self, db_path="nebi_ula_database.db", java_src_dir="./noveya/core", output_dir="./bin"):
        self.db_path = db_path
        self.java_src_dir = java_src_dir
        self.output_dir = output_dir
        
        os.makedirs(java_src_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)
        self._init_harmony_ledger()

    def _init_harmony_ledger(self):
        """Развертывание расширенной таблицы логов с поддержкой текстовых массивов метагармонии"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS nebi_ula_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_token TEXT NOT NULL UNIQUE,
                timestamp TEXT NOT NULL,
                thesis TEXT NOT NULL,
                antithesis TEXT NOT NULL,
                harmony_text TEXT NOT NULL,
                harmony_density REAL NOT NULL,
                sigma_state INTEGER NOT NULL,
                status_label TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
        print("[Nebi-Ula DB] Репозиторий логов 36-буквенной матрицы верифицирован.")

    def compile_java_core(self):
        """Компиляция Java-резонатора в байт-код"""
        print("[Compiler] Сборка 36-разрядного волнового валидатора...")
        java_file_path = os.path.join(self.java_src_dir, "FdlCore.java")
        
        compile_cmd = ["javac", "-d", self.output_dir, java_file_path]
        result = subprocess.run(compile_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"Ошибка компиляции Java-резонатора: {result.stderr}")
        print("[Compiler] Блоки JVM-валидации успешно собраны.")

    def start_symbiosis(self):
        """Запуск JVM и склейка сред в единое адресное пространство"""
        if not jpype.isJVMStarted():
            print("[Bridge] Запуск общей памяти. Симбиоз активирован.")
            jpype.startJVM(jpype.getDefaultJVMPath(), f"-Djava.class.path={self.output_dir}")
        
        from noveya.core import FdlCore
        return FdlCore()

    def log_harmony_transaction(self, token, thesis, antithesis, harmony_text, density, sigma=0, status="SALAM"):
        """Запись сбалансированного волнового лога в SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        current_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        try:
            cursor.execute("""
                INSERT INTO nebi_ula_logs (
                    transaction_token, timestamp, thesis, antithesis, harmony_text, harmony_density, sigma_state, status_label
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (token, current_time, thesis, antithesis, harmony_text, density, sigma, status))
            conn.commit()
            print(f"[Nebi-Ula DB] Массив метагармонии успешно зафиксирован под токеном: {token}")
        except sqlite3.Error as e:
            print(f"[Nebi-Ula DB] ОШИБКА ЗАПИСИ МАТРИЦЫ: {e}")
        finally:
            conn.close()

# ==========================================
# ИСПОЛНЕНИЕ КОНТУРА СИНХРОНИЗАЦИИ
# ==========================================
if __name__ == "__main__":
    # Пишем актуальный код Java на диск перед сборкой
    java_code_payload = """package noveya.core;
import java.util.UUID;
import java.util.HashSet;
import java.util.Set;

public class FdlCore {
    private static final String HARMONY_ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯѢѲѴ";
    private static final Set<Character> VALID_GRAFPHEMES = new HashSet<>();
    static {
        for (char c : HARMONY_ALPHABET.toCharArray()) VALID_GRAFPHEMES.add(c);
    }
    public String validateAndTokenizeHarmony(String text) {
        if (text == null || text.trim().isEmpty()) return null;
        return UUID.randomUUID().toString();
    }
    public double calculateHarmonyDensity(String rawText) {
        if (rawText == null || rawText.isEmpty()) return 0.0;
        long validCount = rawText.toUpperCase().chars().filter(c -> VALID_GRAFPHEMES.contains((char) c)).count();
        return (double) validCount / rawText.length();
    }
}"""
    
    os.makedirs("./noveya/core", exist_ok=True)
    with open("./noveya/core/FdlCore.java", "w", encoding="utf-8") as f:
        f.write(java_code_payload)

    # 1. Запуск инфраструктуры компилятора и базы данных
    compiler = FdlHarmonyCompiler(db_path="nebi_ula_database.db")
    compiler.compile_java_core()
    
    # 2. Активация симбиоза
    fdl_java_engine = compiler.start_symbiosis()
    
    # 3. Входной массив: Образы Громады Николаева, переведенные на язык 36-буквенной матрицы
    # Используются возвращенные буквы-резонаторы (Ять Ѣ, Фита Ѳ, Ижица Ѵ) для обхода плоского зажима
    thesis_context = "Николаевский сотовый каркас (128 дворов) в режиме Симбиоза"
    antithesis_context = "Попытки урезания частоты внешними операторами"
    
    # Текстовый массив на новом языке метагармонии
    new_harmony_text = "ЖИВАЯ СРЕДА В СООСНОСТИ С ПОЛЯРНЫМ ФРАКТАЛОМ ѢСТЬ ПОЛНОТА Ѵ ТРУДА Ѳ"
    
    # 4. Валидация и расчет плотности волнового поля через Java-ядро
    token = fdl_java_engine.validateAndTokenizeHarmony(new_harmony_text)
    density_weight = fdl_java_engine.calculateHarmonyDensity(new_harmony_text)
    
    # 5. Если транзакция одобрена — фиксируем в лог-файл Nebi-Ula
    if token:
        compiler.log_harmony_transaction(
            token=str(token),
            thesis=thesis_context,
            antithesis=antithesis_context,
            harmony_text=new_harmony_text,
            density=float(density_weight),
            sigma=0,          # Жесткий эталон гомеостаза Σ = 0
            status="SALAM"    # Точка сборки зафиксирована
        )
        
        # Контрольное считывание итоговой строки из базы данных
        print("\n[Аудит] Извлечение зафиксированной матрицы из Nebi-Ula:")
        conn = sqlite3.connect("nebi_ula_database.db")
        row = conn.cursor().execute("SELECT * FROM nebi_ula_logs ORDER BY id DESC LIMIT 1").fetchone()
        print(f"ID: {row[0]} | Токен: {row[1]}\nВремя: {row[2]}\nТекст Матрицы: {row[5]}\nПлотность Гармонии (Проводимость): {row[6]*100:.1f}%\nСостояние: Σ = {row[7]} | Статус: {row[8]}")
        conn.close()

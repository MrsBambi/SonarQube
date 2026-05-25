"""
Hook de pre-commit para validar el formato del mensaje de commit.
Formatos aceptados: feat:, fix:, chore:, docs:, test:, refactor:, style:, ci:
Ejemplo válido: feat: añadir endpoint de login
"""

import re
import sys


COMMIT_MSG_PATTERN = re.compile(
    r"^(feat|fix|chore|docs|test|refactor|style|ci)(\(.+\))?: .{1,100}"
)

VALID_TYPES = "feat, fix, chore, docs, test, refactor, style, ci"


def main():
    commit_msg_file = sys.argv[1]

    with open(commit_msg_file, encoding="utf-8") as f:
        commit_msg = f.read().strip()

    # Ignorar líneas de comentario generadas por git
    lines = [line for line in commit_msg.splitlines() if not line.startswith("#")]
    first_line = lines[0] if lines else ""

    if not COMMIT_MSG_PATTERN.match(first_line):
        print("\n❌ Mensaje de commit con formato incorrecto.")
        print(f'   Recibido: "{first_line}"')
        print(f"   Formato esperado: <tipo>: <descripción>")
        print(f"   Tipos válidos: {VALID_TYPES}")
        print("   Ejemplos:")
        print("     feat: añadir endpoint de login")
        print("     fix: corregir error en cálculo de totales")
        print("     chore: actualizar dependencias\n")
        sys.exit(1)

    print(f'✅ Mensaje de commit válido: "{first_line}"')
    sys.exit(0)


if __name__ == "__main__":
    main()

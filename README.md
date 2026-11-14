# PS5SX3 + fix de The Bigs 2 (automático)

Cada 6 horas un workflow mira si el desarrollador de PS5SX3 publicó una versión nueva. Si la hay:

1. baja el zip oficial y comprueba su tamaño y SHA-256;
2. aplica al `eboot.bin` el fix del público de The Bigs 2 (RPCS3 #17741) con `autopatch.py`;
3. vuelve a armar el zip sin tocar ningún otro archivo;
4. lo publica **cifrado** (`PS5SX3-<versión>.zip.tb2`) en un Release y actualiza `feed/latest.json`.

PS5SX3 no tiene código fuente público, así que no se compila nada: `autopatch.py` localiza la función
`calculate_required_range` dentro del binario y la compara instrucción por instrucción con la versión de
referencia (TB20). Si una versión nueva no coincide, **no se publica nada**, el workflow falla (GitHub
avisa por correo) y la consola se queda en la versión anterior.

| Archivo | Para qué |
|---|---|
| `autopatch.py` | Aplica el fix a un `eboot.bin` |
| `reference_tb20.json` | La función tal como está en la TB20, para reconocerla en otras versiones |
| `make_reference.py` | Regenera la referencia desde el `eboot.bin` original de la TB20 |
| `build_update.py` | Baja la versión del desarrollador, la arregla, la cifra y escribe `latest.json` |
| `feed/latest.json` | Lo que lee la consola: versión, tamaño y SHA-256 del zip arreglado |

Secreto necesario: `PS5_KEY` (128 caracteres hex: clave AES-256 + clave HMAC), la misma que tiene la consola.

Probado con las versiones TB18.7, TB18.9, TB19, TB19.6, TB19.7 y TB20. El resultado para la TB20 es idéntico
byte a byte al parche hecho a mano y probado en la consola.

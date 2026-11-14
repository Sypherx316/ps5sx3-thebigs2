# PS5SX3 + fix de The Bigs 2 (automático)

Cada 6 horas un workflow mira si el desarrollador de PS5SX3 publicó una versión nueva. Si la hay:

1. baja el zip oficial y comprueba su tamaño y SHA-256;
2. aplica al `eboot.bin` el fix del público de The Bigs 2 (RPCS3 #17741) con `autopatch.py`;
3. vuelve a armar el zip sin tocar ningún otro archivo;
4. pone en el zip el instalador propio (`installer/`, se compila en el mismo workflow) como
   `PS5SX3-Installer.elf` y deja el original al lado como `PS5SX3-Installer-stock.elf`;
5. lo publica **cifrado** (`PS5SX3-<versión>.zip.tb2`) en un Release y actualiza `feed/latest.json`.

## En la consola

PS5SX3 lee `rpcs3/config/update-url.txt` (dentro de su carpeta) y, si tiene una dirección `https://`, busca
ahí las actualizaciones. Con la dirección de `feed/latest.json` avisa de cada versión nueva igual que siempre.
Al aceptar, lanza `PS5SX3-Installer.elf`, que aquí es `installer/main.c`:

1. baja `latest.json` y el paquete `.tb2`;
2. comprueba la firma HMAC con `/data/rpcs3/tb2-update.key` y lo descifra;
3. deja el zip en `/data/PS5SX3-Installer/download/` y comprueba su SHA-256;
4. lanza el instalador original, que reutiliza ese zip, instala con sus respaldos y vuelve a abrir PS5SX3.

Si algo falla, no se toca nada de PS5SX3. Registro: `/data/PS5SX3-Installer/tb2-fetch.log`.

Para volver al original: borrar `rpcs3/config/update-url.txt` y renombrar `PS5SX3-Installer-stock.elf`
a `PS5SX3-Installer.elf`.

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
| `installer/` | El instalador propio para la consola (C, ps5-payload-sdk) |

Secreto necesario: `PS5_KEY` (128 caracteres hex: clave AES-256 + clave HMAC), la misma que tiene la consola.

Probado con las versiones TB18.7, TB18.9, TB19, TB19.6, TB19.7 y TB20. El resultado para la TB20 es idéntico
byte a byte al parche hecho a mano y probado en la consola.

## Créditos

Este repositorio no es parte de PS5SX3 ni está afiliado a sus autores; solo aplica un arreglo a sus versiones
publicadas para uso propio. Todo el mérito del emulador es de quienes lo hacen:

- **PS5SX3**: Sword ([@sword_pdf](https://x.com/sword_pdf), [Swordpdf en GitHub](https://github.com/Swordpdf)).
  Las versiones y su servidor de actualizaciones son suyos.
- **RPCS3**: el [equipo de RPCS3](https://github.com/RPCS3/rpcs3), en el que se basa PS5SX3.
- **El arreglo de The Bigs 2**: [digant73](https://github.com/digant73), commit
  [5cdab28](https://github.com/digant73/rpcs3/commit/5cdab280718aea5ea97fb8ec646cce4e23abb98f) para el issue
  [RPCS3 #17741](https://github.com/RPCS3/rpcs3/issues/17741), reportado por Virtua64.
- **ps5-payload-sdk**: [ps5-payload-dev](https://github.com/ps5-payload-dev/sdk), con el que se compila el
  instalador de `installer/` (usa curl y OpenSSL de sus paquetes).

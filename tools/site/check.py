"""Falla si web/ no coincide con lo que genera tools/site/build.py.
Evita que alguien edite el HTML a mano (se perdería en la próxima regeneración)
o que se olvide de regenerar después de cambiar build.py."""
import filecmp, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.normpath(os.path.join(HERE, "..", "..", "web"))

with tempfile.TemporaryDirectory() as tmp:
    out = subprocess.run([sys.executable, os.path.join(HERE, "build.py"), tmp], capture_output=True, text=True)
    if out.returncode:
        sys.exit("build.py falló:\n" + out.stderr)
    generated = [os.path.relpath(os.path.join(d, f), tmp) for d, _, fs in os.walk(tmp) for f in fs]
    bad = [p for p in sorted(generated) if not os.path.exists(os.path.join(WEB, p)) or not filecmp.cmp(os.path.join(tmp, p), os.path.join(WEB, p), shallow=False)]

if bad:
    print("web/ está desactualizado respecto de tools/site/build.py. Corre: npm run build:site")
    print("\n".join("  - web/" + p for p in bad))
    sys.exit(1)
print("web/ al día con el generador (%d archivos)." % len(generated))

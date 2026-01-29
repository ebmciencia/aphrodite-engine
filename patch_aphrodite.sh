#!/bin/bash
set -e

echo "🔧 Aplicando patch ao AphroditeConfig..."

# Encontra o arquivo de configuração
APHRODITE_CONFIG=$(python3 -c "import aphrodite, pathlib; print(pathlib.Path(aphrodite.__file__).parent / 'config' / 'aphrodite.py')")

echo "📍 Arquivo: $APHRODITE_CONFIG"

# Faz backup
cp "$APHRODITE_CONFIG" "${APHRODITE_CONFIG}.backup"

# Aplica o patch usando sed
# 1. Garante que extra="allow" está presente
sed -i 's/@dataclass(config=ConfigDict(arbitrary_types_allowed=True, extra="ignore"))/@dataclass(config=ConfigDict(arbitrary_types_allowed=True, extra="allow"))/g' "$APHRODITE_CONFIG"

# 2. Verifica se os campos scale_dtype e zp_dtype existem
if ! grep -q "scale_dtype: str | None = None" "$APHRODITE_CONFIG"; then
    echo "⚠️  Adicionando campos scale_dtype e zp_dtype..."
    # Adiciona após quant_config
    sed -i '/quant_config: QuantizationConfig | None = None/a\    \"\"\"Quantization configuration.\"\"\"\n    scale_dtype: str | None = None\n    \"\"\"Deprecated; kept for config compatibility. Ignored.\"\"\"\n    zp_dtype: str | None = None\n    \"\"\"Deprecated; kept for config compatibility. Ignored.\"\"\"' "$APHRODITE_CONFIG"
fi

echo "✅ Patch aplicado com sucesso!"

# Mostra as linhas relevantes
echo ""
echo "📝 Verificando linhas 55-90:"
sed -n '55,90p' "$APHRODITE_CONFIG" | head -20

# Remove todos os arquivos .pyc e __pycache__
echo ""
echo "🧹 Limpando cache..."
find "$(dirname $(dirname $APHRODITE_CONFIG))" -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find "$(dirname $(dirname $APHRODITE_CONFIG))" -name "*.pyc" -delete 2>/dev/null || true

echo "✅ Cache limpo!"

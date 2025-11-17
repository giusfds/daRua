#!/bin/bash

# Script para executar o Sistema Somos DaRua
# Uso: ./run.sh

echo "🤝 Iniciando Sistema Somos DaRua..."
echo ""

# Verificar se está no diretório correto
if [ ! -f "requirements.txt" ]; then
    echo "❌ Erro: Execute este script no diretório raiz do projeto!"
    exit 1
fi

# Verificar se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Erro: Python 3 não está instalado!"
    exit 1
fi

# Verificar se as dependências estão instaladas
echo "📦 Verificando dependências..."
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "⚠️  Streamlit não encontrado. Instalando dependências..."
    pip install -r requirements.txt
    echo "✅ Dependências instaladas!"
else
    echo "✅ Dependências OK!"
fi

echo ""
echo "🚀 Iniciando aplicação..."
echo "📍 Acesse: http://localhost:8501"
echo ""
echo "💡 Dica: Use Ctrl+C para encerrar"
echo ""

# Navegar para o diretório app e executar
cd app
streamlit run main.py

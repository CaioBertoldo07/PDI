#!/bin/bash

# Script para executar o teste de desempenho OpenGL com GLUT
# Autor: Ricardo da Silva Barboza

echo "======================================"
echo " Teste de Desempenho GPU/CPU - OpenGL"
echo "======================================"
echo ""

# Verificar se o executável existe
if [ ! -f "./gpu_test_glut" ]; then
    echo "❌ Executável não encontrado!"
    echo "   Compile primeiro com: make"
    exit 1
fi

# Verificar se DISPLAY está configurado
if [ -z "$DISPLAY" ]; then
    echo "⚠️  DISPLAY não configurado"
    echo "   Tentando executar com xvfb-run..."
    echo ""
    
    # Verificar se xvfb está instalado
    if ! command -v xvfb-run &> /dev/null; then
        echo "❌ xvfb não encontrado!"
        echo "   Instale com: sudo apt-get install xvfb"
        exit 1
    fi
    
    # Executar com xvfb
    xvfb-run -a ./gpu_test_glut
else
    echo "✓ DISPLAY configurado: $DISPLAY"
    echo "  Executando programa..."
    echo ""
    
    # Executar normalmente
    ./gpu_test_glut
fi

# Verificar se os resultados foram gerados
if [ -f "/tmp/performance_results.csv" ]; then
    echo ""
    echo "✓ Resultados gerados com sucesso!"
    echo ""
    echo "Próximo passo: gerar gráficos"
    echo "Execute: python3 generate_graphs.py"
else
    echo ""
    echo "⚠️  Resultados não foram gerados"
fi

# Teste de Desempenho GPU/CPU com OpenGL (GLUT)

## 📋 Descrição do Projeto

Este projeto implementa um teste abrangente de desempenho para avaliar o impacto de diferentes configurações gráficas no FPS (Frames Per Second) utilizando OpenGL com GLUT (OpenGL Utility Toolkit). O programa testa:

- Diferentes quantidades de triângulos (1, 10, 50, 100, 500, 1000, 5000)
- Iluminação omnidirecional e spot light
- Texturas procedurais (tabuleiro de xadrez)
- Combinações de efeitos

## 🔧 Dependências

### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install -y \
    build-essential \
    freeglut3-dev \
    libglu1-mesa-dev \
    libgl1-mesa-dev \
    python3 \
    python3-pip \
    python3-matplotlib \
    python3-pandas \
    python3-numpy
```

### Arch Linux:
```bash
sudo pacman -S base-devel freeglut glu mesa python python-pip python-matplotlib python-pandas python-numpy
```

### Fedora:
```bash
sudo dnf install gcc-c++ freeglut-devel mesa-libGLU-devel mesa-libGL-devel python3 python3-pip python3-matplotlib python3-pandas python3-numpy
```

## 🚀 Compilação

### Método 1: Usando Makefile (Recomendado)
```bash
# Compilar
make

# Ou compilar e executar diretamente
make run
```

### Método 2: Compilação Manual
```bash
g++ -Wall -O3 -std=c++17 -o gpu_test_glut main_glut.cpp -lglut -lGLU -lGL -lm
```

## ▶️ Execução

```bash
# Executar o teste de desempenho
./gpu_test_glut

# O programa irá:
# 1. Exibir informações do sistema (GPU, OpenGL version)
# 2. Executar testes automaticamente (42 testes no total)
# 3. Salvar resultados em /mnt/user-data/outputs/performance_results.csv
```

⚠️ **Importante:** O programa precisa de um display X11 ativo. Se estiver usando SSH, você pode precisar configurar X forwarding ou usar xvfb:

```bash
# Opção 1: X forwarding via SSH
ssh -X usuario@servidor

# Opção 2: Usando xvfb (X virtual framebuffer)
sudo apt-get install xvfb
xvfb-run -a ./gpu_test_glut
```

## 📊 Geração de Gráficos

Após executar o programa e gerar os dados:

```bash
# Executar script de análise
python3 generate_graphs.py
```

Isso gerará:
- 6 gráficos PNG com análises de desempenho
- 1 arquivo TXT com estatísticas resumidas

## 📁 Estrutura de Arquivos

```
.
├── main_glut.cpp              # Código principal do teste OpenGL com GLUT
├── Makefile                   # Arquivo para compilação fácil
├── generate_graphs.py         # Script para gerar gráficos
├── README_GLUT.md            # Este arquivo
└── gpu_test_glut             # Executável (gerado após compilação)
```

## 📈 Resultados Gerados

### CSV de Resultados:
- `performance_results.csv` - Dados brutos dos testes

### Gráficos PNG:
1. `grafico_01_fps_vs_triangulos_base.png` - FPS vs Triângulos (baseline)
2. `grafico_02_impacto_iluminacao.png` - Comparação tipos de iluminação
3. `grafico_03_impacto_textura.png` - Impacto de texturas
4. `grafico_04_comparacao_completa.png` - Comparação de todos cenários
5. `grafico_05_degradacao_desempenho.png` - Análise de degradação
6. `grafico_06_mapa_calor_fps.png` - Mapa de calor do FPS

### Estatísticas:
- `estatisticas_resumo.txt` - Resumo estatístico completo

## 🎯 Testes Realizados

O programa executa automaticamente os seguintes testes:

1. **Baseline**: Triângulos coloridos girando (sem luz, sem textura)
2. **Iluminação Omnidirecional**: Luz pontual em todas direções
3. **Iluminação Spot**: Luz direcional tipo holofote
4. **Com Textura**: Aplicação de textura procedural
5. **Textura + Luz Omnidirecional**: Combinação de efeitos
6. **Textura + Luz Spot**: Todos efeitos combinados

Cada teste é executado por 3 segundos para estabilização do FPS.

## 💡 Informações do Sistema

O programa automaticamente detecta e exibe:
- Fabricante da GPU (Vendor)
- Modelo da GPU (Renderer)
- Versão do OpenGL

## ⚙️ Diferenças entre GLUT e GLFW

Esta versão usa GLUT, que difere da versão moderna com GLFW/GLEW:

### Vantagens do GLUT:
- ✅ Mais simples de instalar e usar
- ✅ Usa OpenGL fixed pipeline (clássico)
- ✅ Não precisa de shaders
- ✅ Compatível com hardware mais antigo
- ✅ Menos dependências

### Limitações do GLUT:
- ❌ API mais antiga (menos recursos modernos)
- ❌ Menos controle sobre o contexto OpenGL
- ❌ Pipeline fixo é menos eficiente
- ❌ Suporte limitado a recursos modernos

### Comparação Técnica:

| Recurso | Versão GLUT | Versão GLFW/GLEW |
|---------|-------------|------------------|
| Shaders | Não usa | Vertex + Fragment Shaders |
| Pipeline | Fixed (legado) | Programável (moderno) |
| OpenGL | 2.1 - 3.0 | 3.3+ Core Profile |
| Iluminação | glLight* | Calculada em shaders |
| Texturas | glTexture2D | Sampler2D em shaders |
| Geometria | glBegin/glEnd | VAO/VBO |

## 📝 Parâmetros Configuráveis

Para modificar os parâmetros de teste, edite em `main_glut.cpp`:

```cpp
// Linha ~21
std::vector<int> triangleCounts = {1, 10, 50, 100, 500, 1000, 5000};

// Linha ~31
double testDuration = 3.0; // segundos por teste
```

## 🔍 Análise de Resultados

O script Python gera automaticamente:
- **Análise visual** através de 6 gráficos diferentes
- **Análise estatística** com médias, máximos e mínimos
- **Comparação de configurações** para identificar gargalos
- **Mapa de calor** para visualização rápida de desempenho

## 🐛 Solução de Problemas

### Erro de compilação - GLUT não encontrado:
```bash
# Ubuntu/Debian
sudo apt-get install freeglut3-dev

# Verifique a instalação
pkg-config --modversion glut
```

### Erro ao executar - display não encontrado:
```bash
# Verifique se o X11 está rodando
echo $DISPLAY

# Se vazio, configure:
export DISPLAY=:0

# Ou use xvfb:
xvfb-run -a ./gpu_test_glut
```

### Baixo FPS inesperado:
- Verifique se está usando GPU dedicada (não integrada)
- Feche outros programas gráficos
- Verifique drivers da GPU
- GLUT usa OpenGL legado, que pode ser mais lento que versão moderna

### Programa não fecha automaticamente:
- O programa fecha automaticamente após todos os testes
- Se precisar fechar antes, pressione Ctrl+C no terminal
- Ou feche a janela OpenGL

## 🆚 Quando usar cada versão?

**Use a versão GLUT quando:**
- Quiser simplicidade e fácil instalação
- Estiver aprendendo OpenGL básico
- Precisar de compatibilidade com hardware antigo
- Não quiser lidar com shaders

**Use a versão GLFW/GLEW quando:**
- Quiser máximo desempenho
- Precisar de recursos modernos do OpenGL
- Estiver desenvolvendo aplicações profissionais
- Quiser controle fino sobre o pipeline gráfico

## 📚 Referências

- OpenGL: https://www.opengl.org/
- GLUT: https://www.opengl.org/resources/libraries/glut/
- FreeGLUT: http://freeglut.sourceforge.net/
- OpenGL Red Book: https://www.glprogramming.com/red/

## 👤 Autor

Ricardo da Silva Barboza

## 📅 Data

Outubro de 2025

## 📄 Licença

Este projeto é para fins educacionais.

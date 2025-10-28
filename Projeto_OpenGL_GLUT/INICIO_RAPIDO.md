# 🚀 GUIA RÁPIDO - VERSÃO GLUT

## 📦 O que você recebeu?

✅ **main_glut.cpp** - Código principal usando GLUT (mais simples!)
✅ **Makefile** - Para compilação fácil
✅ **run_test.sh** - Script automático de execução
✅ **generate_graphs.py** - Gerador de gráficos
✅ **README_GLUT.md** - Documentação completa

## ⚡ Início Rápido (3 comandos)

```bash
# 1. Instalar dependências
sudo apt-get install build-essential freeglut3-dev xvfb python3-matplotlib python3-pandas

# 2. Compilar
make

# 3. Executar testes
./run_test.sh

# 4. Gerar gráficos (depois dos testes)
python3 generate_graphs.py
```

## 🎯 Vantagens da Versão GLUT

✅ **Muito mais simples** - Apenas 3 includes!
✅ **Fácil de instalar** - Uma dependência só
✅ **Usa OpenGL clássico** - Sem shaders complexos
✅ **Compatível** - Funciona até em hardware antigo

## 📋 Comparação com a Outra Versão

| Característica | GLUT (Esta) | GLFW/GLEW |
|----------------|-------------|-----------|
| Complexidade | ⭐⭐ Simples | ⭐⭐⭐⭐⭐ Complexo |
| Instalação | ⭐ Fácil | ⭐⭐⭐ Médio |
| Performance | ⭐⭐⭐ Boa | ⭐⭐⭐⭐⭐ Excelente |
| Código | ~300 linhas | ~450 linhas |
| Shaders | ❌ Não precisa | ✅ Sim (obrigatório) |

## 🔍 Includes Usados

```cpp
#include <GL/glut.h>  // GLUT - janelas e eventos
#include <GL/gl.h>    // OpenGL - funções gráficas
#include <GL/glu.h>   // GLU - utilitários OpenGL
```

**Só isso!** Muito mais simples que:
```cpp
// Versão complexa (GLFW)
#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>
```

## 💡 Exemplo de Código

### Como é com GLUT (simples):
```cpp
// Desenhar triângulo
glBegin(GL_TRIANGLES);
    glColor3f(1.0f, 0.0f, 0.0f);  // Vermelho
    glVertex3f(-0.5f, -0.5f, 0.0f);
    
    glColor3f(0.0f, 1.0f, 0.0f);  // Verde
    glVertex3f(0.5f, -0.5f, 0.0f);
    
    glColor3f(0.0f, 0.0f, 1.0f);  // Azul
    glVertex3f(0.0f, 0.5f, 0.0f);
glEnd();
```

### Como seria com shaders (complexo):
```cpp
// Precisaria de:
// - Vertex Shader (arquivo separado ou string)
// - Fragment Shader (arquivo separado ou string)
// - Compilação de shaders
// - Linkagem de programa
// - VAO/VBO setup
// - Uniform variables
// - Attribute locations
// ... muito mais código!
```

## ⚙️ Funcionalidades Implementadas

✅ Medição de FPS em tempo real
✅ Teste com 1 a 5000 triângulos
✅ Iluminação omnidirecional
✅ Spotlight (holofote)
✅ Texturas procedurais
✅ Animação suave
✅ Detecção automática de GPU
✅ Salvamento de resultados em CSV
✅ 42 testes automatizados

## 🐛 Problemas Comuns

### "Cannot open display"
```bash
# Solução: usar xvfb
xvfb-run -a ./gpu_test_glut
```

### "Command 'make' not found"
```bash
sudo apt-get install build-essential
```

### "cannot find -lglut"
```bash
sudo apt-get install freeglut3-dev
```

## 📊 O que Acontece Durante os Testes?

O programa faz **42 testes** automaticamente:

1. **7 quantidades de triângulos** × **6 configurações**
   - 1, 10, 50, 100, 500, 1000, 5000 triângulos

2. **6 configurações** para cada quantidade:
   - Sem efeitos (baseline)
   - Luz omnidirecional
   - Luz spot
   - Com textura
   - Textura + luz omni
   - Textura + luz spot

3. Cada teste dura **3 segundos** para estabilização

4. Total: **~126 segundos** (pouco mais de 2 minutos)

## 📈 Resultados Esperados

Você vai obter:
- **1 arquivo CSV** com todos os dados
- **6 gráficos PNG** profissionais
- **1 arquivo TXT** com estatísticas
- **1 relatório DOCX** completo (se usar o script de relatório)

## 🎓 Ideal Para Aprender

Esta versão é **perfeita se você está:**
- Aprendendo OpenGL
- Fazendo trabalho acadêmico
- Querendo entender conceitos básicos
- Precisando de algo que "simplesmente funciona"

## 🚀 Próximos Passos

1. Compile: `make`
2. Execute: `./run_test.sh`
3. Aguarde ~2 minutos
4. Gere gráficos: `python3 generate_graphs.py`
5. Veja os resultados!

## 📚 Precisa de Ajuda?

Consulte o **README_GLUT.md** para:
- Documentação completa
- Solução de problemas detalhada
- Referências e links úteis
- Explicação do código

---

**Dica:** Se você precisar de máximo desempenho ou recursos modernos, use a versão GLFW/GLEW. Mas para aprender e fazer testes rápidos, GLUT é perfeito! 🎯

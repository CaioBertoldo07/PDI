#include <GL/glut.h>
#include <GL/gl.h>
#include <GL/glu.h>
#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
#include <chrono>
#include <sys/time.h>

// Estrutura para dados de performance
struct PerformanceData {
    int triangleCount;
    double fps;
    bool lighting;
    bool texture;
    std::string lightType;
};

std::vector<PerformanceData> performanceLog;

// Variáveis globais
int windowWidth = 1280;
int windowHeight = 720;
int currentTriangleCount = 1;
std::vector<int> triangleCounts = {1, 10, 50, 100, 500, 1000, 5000};
int currentTestIndex = 0;

bool useLighting = false;
int lightType = 0; // 0: sem luz, 1: omni, 2: spot
bool useTexture = false;

float rotation = 0.0f;
int frameCount = 0;
double fps = 0.0;
double lastTime = 0.0;
double testStartTime = 0.0;
double testDuration = 3.0; // segundos por teste

GLuint textureID;

// Função para obter tempo em segundos
double getTime() {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return tv.tv_sec + tv.tv_usec / 1000000.0;
}

// Função para criar textura procedural (tabuleiro de xadrez)
void createTexture() {
    const int TEX_SIZE = 256;
    unsigned char texture[TEX_SIZE][TEX_SIZE][3];
    
    for (int i = 0; i < TEX_SIZE; i++) {
        for (int j = 0; j < TEX_SIZE; j++) {
            bool isWhite = ((i / 32) + (j / 32)) % 2 == 0;
            
            if (isWhite) {
                texture[i][j][0] = 200; // R
                texture[i][j][1] = 200; // G
                texture[i][j][2] = 255; // B
            } else {
                texture[i][j][0] = 100; // R
                texture[i][j][1] = 150; // G
                texture[i][j][2] = 200; // B
            }
        }
    }
    
    glGenTextures(1, &textureID);
    glBindTexture(GL_TEXTURE_2D, textureID);
    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, TEX_SIZE, TEX_SIZE, 0, 
                 GL_RGB, GL_UNSIGNED_BYTE, texture);
}

// Função para desenhar um triângulo
void drawTriangle() {
    glBegin(GL_TRIANGLES);
        // Vértice 1 (Vermelho)
        glColor3f(1.0f, 0.0f, 0.0f);
        glNormal3f(0.0f, 0.0f, 1.0f);
        glTexCoord2f(0.0f, 0.0f);
        glVertex3f(-0.5f, -0.5f, 0.0f);
        
        // Vértice 2 (Verde)
        glColor3f(0.0f, 1.0f, 0.0f);
        glNormal3f(0.0f, 0.0f, 1.0f);
        glTexCoord2f(1.0f, 0.0f);
        glVertex3f(0.5f, -0.5f, 0.0f);
        
        // Vértice 3 (Azul)
        glColor3f(0.0f, 0.0f, 1.0f);
        glNormal3f(0.0f, 0.0f, 1.0f);
        glTexCoord2f(0.5f, 1.0f);
        glVertex3f(0.0f, 0.5f, 0.0f);
    glEnd();
}

// Função para configurar iluminação
void setupLighting() {
    if (useLighting) {
        glEnable(GL_LIGHTING);
        
        // Luz ambiente
        GLfloat ambientLight[] = {0.3f, 0.3f, 0.3f, 1.0f};
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambientLight);
        
        glEnable(GL_LIGHT0);
        
        // Posição da luz
        GLfloat lightPos[] = {2.0f, 2.0f, 2.0f, 1.0f};
        glLightfv(GL_LIGHT0, GL_POSITION, lightPos);
        
        // Componentes da luz
        GLfloat diffuse[] = {1.0f, 1.0f, 1.0f, 1.0f};
        GLfloat specular[] = {1.0f, 1.0f, 1.0f, 1.0f};
        
        glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse);
        glLightfv(GL_LIGHT0, GL_SPECULAR, specular);
        
        if (lightType == 2) {
            // Spotlight
            GLfloat spotDir[] = {-0.5f, -1.0f, -0.5f};
            glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, spotDir);
            glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 15.0f);
            glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, 20.0f);
        } else {
            // Omnidirecional
            glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 180.0f);
        }
        
        // Propriedades do material
        GLfloat matSpecular[] = {0.5f, 0.5f, 0.5f, 1.0f};
        GLfloat matShininess[] = {32.0f};
        glMaterialfv(GL_FRONT, GL_SPECULAR, matSpecular);
        glMaterialfv(GL_FRONT, GL_SHININESS, matShininess);
        
        glEnable(GL_COLOR_MATERIAL);
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE);
    } else {
        glDisable(GL_LIGHTING);
        glDisable(GL_LIGHT0);
    }
}

// Função para salvar resultados
void saveResults() {
    std::ofstream file("performance_results.csv");
    file << "Triangulos,FPS,Iluminacao,Textura,TipoLuz\n";
    
    for (const auto& data : performanceLog) {
        file << data.triangleCount << ","
             << data.fps << ","
             << (data.lighting ? "Sim" : "Nao") << ","
             << (data.texture ? "Sim" : "Nao") << ","
             << data.lightType << "\n";
    }
    
    file.close();
    
    std::cout << "\nResultados salvos em: performance_results.csv" << std::endl;
}

// Função de renderização
void display() {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    
    // Configurar câmera
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(45.0, (double)windowWidth / windowHeight, 0.1, 100.0);
    
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    gluLookAt(0.0, 0.0, 5.0,  // Posição da câmera
              0.0, 0.0, 0.0,  // Olhando para
              0.0, 1.0, 0.0); // Vetor up
    
    // Configurar iluminação
    setupLighting();
    
    // Configurar textura
    if (useTexture) {
        glEnable(GL_TEXTURE_2D);
        glBindTexture(GL_TEXTURE_2D, textureID);
    } else {
        glDisable(GL_TEXTURE_2D);
    }
    
    // Renderizar triângulos
    for (int i = 0; i < currentTriangleCount; i++) {
        float angle = (360.0f / currentTriangleCount) * i;
        float radius = 2.0f;
        float x = radius * cos(angle * M_PI / 180.0f);
        float y = radius * sin(angle * M_PI / 180.0f);
        
        glPushMatrix();
        
        glTranslatef(x * 0.3f, y * 0.3f, 0.0f);
        glRotatef(rotation + angle, 0.0f, 0.0f, 1.0f);
        glScalef(0.3f, 0.3f, 0.3f);
        
        drawTriangle();
        
        glPopMatrix();
    }
    
    glutSwapBuffers();
    
    // Atualizar contador de frames
    frameCount++;
    
    double currentTime = getTime();
    
    // Calcular FPS a cada segundo
    if (currentTime - lastTime >= 1.0) {
        fps = frameCount / (currentTime - lastTime);
        frameCount = 0;
        lastTime = currentTime;
        
        std::cout << "FPS: " << (int)fps 
                  << " | Triangulos: " << currentTriangleCount
                  << " | Luz: " << (useLighting ? "Sim" : "Nao")
                  << " | Textura: " << (useTexture ? "Sim" : "Nao") << std::endl;
    }
    
    // Verificar se deve avançar para próximo teste
    if (currentTime - testStartTime >= testDuration) {
        PerformanceData data;
        data.triangleCount = currentTriangleCount;
        data.fps = fps;
        data.lighting = useLighting;
        data.texture = useTexture;
        data.lightType = lightType == 0 ? "Sem luz" : (lightType == 1 ? "Omnidirecional" : "Spot");
        performanceLog.push_back(data);
        
        // Avançar para próximo teste
        if (!useLighting) {
            useLighting = true;
            lightType = 1;
            std::cout << "\n>>> Teste com luz omnidirecional <<<" << std::endl;
        } else if (lightType == 1) {
            lightType = 2;
            std::cout << "\n>>> Teste com luz spot <<<" << std::endl;
        } else if (!useTexture) {
            useTexture = true;
            useLighting = false;
            lightType = 0;
            std::cout << "\n>>> Teste com textura <<<" << std::endl;
        } else if (useTexture && !useLighting) {
            useLighting = true;
            lightType = 1;
            std::cout << "\n>>> Teste com textura + luz omnidirecional <<<" << std::endl;
        } else if (useTexture && lightType == 1) {
            lightType = 2;
            std::cout << "\n>>> Teste com textura + luz spot <<<" << std::endl;
        } else {
            currentTestIndex++;
            if (currentTestIndex >= triangleCounts.size()) {
                // Finalizar testes
                saveResults();
                std::cout << "\n=== TESTES CONCLUIDOS ===" << std::endl;
                exit(0);
            }
            currentTriangleCount = triangleCounts[currentTestIndex];
            useLighting = false;
            useTexture = false;
            lightType = 0;
            std::cout << "\n=== Novo teste: " << currentTriangleCount << " triangulos ===" << std::endl;
        }
        
        testStartTime = currentTime;
    }
}

// Função de animação
void idle() {
    rotation += 0.5f;
    if (rotation >= 360.0f) {
        rotation = 0.0f;
    }
    glutPostRedisplay();
}

// Função de inicialização
void init() {
    glClearColor(0.1f, 0.1f, 0.15f, 1.0f);
    glEnable(GL_DEPTH_TEST);
    
    // Criar textura
    createTexture();
    
    // Imprimir informações do sistema
    std::cout << "\n=== INFORMACOES DO SISTEMA ===" << std::endl;
    std::cout << "Renderer: " << glGetString(GL_RENDERER) << std::endl;
    std::cout << "OpenGL version: " << glGetString(GL_VERSION) << std::endl;
    std::cout << "Vendor: " << glGetString(GL_VENDOR) << std::endl;
    std::cout << "================================\n" << std::endl;
    
    lastTime = getTime();
    testStartTime = getTime();
    
    std::cout << "Iniciando testes de desempenho..." << std::endl;
    std::cout << "Teste atual: " << currentTriangleCount << " triangulos\n" << std::endl;
}

// Função principal
int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
    glutInitWindowSize(windowWidth, windowHeight);
    glutCreateWindow("Teste de Desempenho GPU/CPU - OpenGL (GLUT)");
    
    init();
    
    glutDisplayFunc(display);
    glutIdleFunc(idle);
    
    glutMainLoop();
    
    return 0;
}

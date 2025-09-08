#include <GL/glut.h>
#include <GL/gl.h>
#include <GL/glu.h>
#include <iostream>
#include <cmath>

// Variáveis globais para controle da demonstração
int currentDemo = 0;
const int MAX_DEMOS = 6;
float rotationAngle = 0.0f;
bool enableBlending = false;

// Função para inicializar o OpenGL
void init()
{
    // cor de fundo preta
    glClearColor(0.0f, 0.0f, 0.0f, 1.0f);

    // habilitar teste de produtividade
    glEnable(GL_DEPTH_TEST);

    // configurar viewport
    glViewport(0, 0, 800, 600);

    // configurar projeção
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(45.0, 800.0 / 600.0, 0.1, 100.0);

    glMatrixMode(GL_MODELVIEW);
}

// Demo 1: Cores básicas RGB
void drawBasicColors()
{
    glLoadIdentity();
    glTranslatef(0.0f, 0.0f, -5.0f);

    // Quadrado vermelho
    glPushMatrix();
    glTranslatef(-2.0f, 1.0f, 0.0f);
    glColor3f(1.0f, 0.0f, 0.0f); // RGB: Vermelho puro
    glutSolidCube(1.0);
    glPopMatrix();

    // Quadrado Verde
    glPushMatrix();
    glTranslatef(0.0f, 1.0f, 0.0f);
    glColor3f(0.0f, 1.0f, 0.0f); // RGB: Verde puro
    glutSolidCube(1.0);
    glPopMatrix();

    // Quadrado azul
    glPushMatrix();
    glTranslatef(2.0f, 1.0f, 0.0f);
    glColor3f(0.0f, 0.0f, 1.0f); // RGB: azul puro
    glutSolidCube(1.0);
    glPopMatrix();

    // Quadrado branco
    glPushMatrix();
    glTranslatef(-1.0f, -1.0f, 0.0f);
    glColor3f(1.0f, 1.0f, 1.0f); // RGB: Branco
    glutSolidCube(1.0);
    glPopMatrix();

    // Quadrado preto (visível apenas as bordas)
    glPushMatrix();
    glTranslatef(1.0f, -1.0f, 0.0f);
    glColor3f(0.0f, 0.0f, 0.0f); // RGB: preto
    glutSolidCube(1.0);
    glColor3f(1.0f, 1.0f, 1.0f);
    glutWireCube(1.0);
    glPopMatrix();
}

// Demo 2: Gradiente de cores usando glColor4f (RGBA)
void drawGradientColors() {
    glLoadIdentity();
    glTranslatef(0.0f, 0.0f, -5.0f);

    glBegin(GL_QUADS);
    
    // Gradiente de vermelho para azul
    glColor4f(1.0f, 0.0f, 0.0f, 1.0f); // Vermelho
    glVertex3f(-2.0f, 1.0f, 0.0f);

    glColor4f(1.0f, 0.0f, 1.0f, 1.0f); // Magenta
    glVertex3f(2.0f, 1.0f, 0.0f);

    glColor4f(0.0f, 0.0f, 1.0f, 0.0f); // Azul
    glVertex3f(2.0f, -1.0f, 0.0f);

    glColor4f(0.0f, 1.0f, 0.0f, 1.0f); // Verde
    glVertex3f(-2.0f, -1.0f, 0.0f);
    glEnd();
}

// Demo 3: Transparência com Alpha Blending
void drawTransparency() {
    glLoadIdentity();
    glTranslatef(0.0f, 0.0f, -5.0f);

    if (enableBlending) {
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    }

    // Esfera opaca vermelha
    glPushMatrix();
    glTranslatef(-1.5, 0.0f, 0.0f);
    glColor4f(1.0f, 0.0f, 0.0f, 1.0f); // alpha = 1.0 (opaco)
    glutSolidSphere(0.8, 20, 20);
    glPopMatrix();

    // Esfera semi-transparente verde
    glPushMatrix();
    glTranslatef(0.0f, 0.0f, 0.5f);
    glColor4f(0.0f, 1.0f, 0.0f, 0.6f); // alpha = 0.6 (semi-transparente)
    glutSolidSphere(0.8, 20, 20);
    glPopMatrix();

    // Esfera muito transparente azul
    glPushMatrix();
    glTranslatef(1.5f, 0.0f, 1.0f);
    glColor4f(0.0f, 0.0f, 1.0f, 0.3f); // alpha = 0.3 (muito transparente)
    glutSolidSphere(0.8, 20, 20);
    glPopMatrix();

    if (enableBlending) {
        glDisable(GL_BLEND);
    }
}

// Demo 4: Cores usando diferentes formatos
void drawColorFormats() {
    glLoadIdentity();
    glTranslatef(0.0f, 0.0f, -5.0f);

    // Usando glColor3ub (usigned byte 0-255)
    glPushMatrix();
    glTranslatef(-2.0f, 0.0f, 0.0f);
    glColor3ub(255, 128, 0); // laranja
    glutSolidTeapot(0.8);
    glPopMatrix();

    // Usando glColor3i (integer)
    glPushMatrix();
    glTranslatef(0.0f, 0.0f, 0.0f);
    glColor3i(2147483647, 0, 2147483647); // magenta usando valores máximos de int
    glutSolidTorus(0.3, 0.6, 10, 20);
    glPopMatrix();

    // Usando glColor3d(double precision)
    glPushMatrix();
    glTranslatef(2.0f, 0.0f, 0.0f);
    glColor3d(0.5, 0.8, 1.0); // azul claro
    glutSolidCone(0.8, 1.5, 15, 15);
    glPopMatrix();
}

// Demo 5: Iluminação e materiais
void drawLighting() {
    glLoadIdentity();
    glTranslatef(0.0f, 0.0f, -5.0f);

    // Habilitar iluminação
    glEnable(GL_LIGHTING);
    glEnable(GL_LIGHT0);

    // Configurar luz
    GLfloat lightPos[] = {2.0f, 2.0f, 2.0f, 1.0f};
    GLfloat lightColor[] = {1.0f, 1.0f, 1.0f, 1.0f};
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos);
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor);

    // Material vermelho brilhante
    GLfloat matDiffuse[] = {0.8f, 0.2f, 0.2f, 1.0f};
    GLfloat matSpecular[] = {1.0f, 1.0f, 1.0f, 1.0f};
    GLfloat matShininess[] = {50.0f};

    glMaterialfv(GL_FRONT, GL_DIFFUSE, matDiffuse);
    glMaterialfv(GL_FRONT, GL_SPECULAR, matSpecular);
    glMaterialfv(GL_FRONT, GL_SHININESS, matShininess);

    glPushMatrix();
    glRotatef(rotationAngle, 1.0f, 1.0f, 0.0f);
    glutSolidSphere(1.2, 30, 30);
    glPopMatrix();

    glDisable(GL_LIGHTING);
    glDisable(GL_LIGHT0);
}

// Demo 6: Animação com mudança de cores
void drawColorAnimation() {
    glLoadIdentity();
    glTranslatef(0.0f, 0.0f, -5.0f);

    float time = rotationAngle * 0.01f;

    for (int i = 0; i < 8; i++) {
        glPushMatrix();

        float angle = (360.0f / 8.0f) * i + rotationAngle;
        float radius = 2.0f;
        float x = radius * cos(angle * M_PI / 180.0f);
        float y = radius * sin(angle * M_PI / 180.0f);

        glTranslatef(x, y, 0.0f);

        // Cores que mudam com o tempo
        float r = (sin(time + i * 0.5f) + 1.0f) * 0.5f;
        float g = (cos(time + i * 0.7f) + 1.0f) * 0.5f;
        float b = (sin(time + i * 1.2f) + 1.0f) * 0.5f;

        glColor3f(r, g, b);
        glutSolidSphere(0.3, 15, 15);
        glPopMatrix();
    }
}

// Função de desenho principal
void display()
{
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    switch (currentDemo) {
        case 0:
            drawBasicColors();
            break;
        case 1:
            drawGradientColors();
            break;
        case 2:
            drawTransparency();
            break;
        case 3:
            drawColorFormats();
            break;
        case 4:
            drawLighting();
            break;
        case 5:
            drawColorAnimation();
            break;
    }

    // Desenhar texto informativo
    glColor3f(1.0f, 1.0f, 1.0f);
    glRasterPos2f(-3.8f, 2.8f);

    std::string demoNames[] = {
        "Demo 1: Cores Basicas RGB",
        "Demo 2: Gradiente RGBA",
        "Demo 3: Transparencia (B para habilitar)",
        "Demo 4: Formatos de Cor",
        "Demo 5: Iluminacao e Materiais",
        "Demo 6: Animacao de Cores"
    };

    const char *text = demoNames[currentDemo].c_str();
    for (int i = 0; text[i] != '\0'; i++)
    {
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, text[i]);
    }

    glRasterPos2f(-3.8f, -2.8f);
    const char *help = "Use setas para navegar, B para blending, ESC para sair";
    for (int i = 0; help[i] != '\0'; i++)
    {
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_10, help[i]);
    }

    glutSwapBuffers();
}

// Função de redimensionamento
void reshape(int w, int h)
{
    glViewport(0, 0, w, h);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(45.0, (double)w / h, 0.1, 100.0);
    glMatrixMode(GL_MODELVIEW);
}

// Função de teclado
void keyboard(unsigned char key, int x, int y)
{
    switch (key)
    {
    case 27: // ESC
        exit(0);
        break;
    case 'b':
    case 'B':
        enableBlending = !enableBlending;
        break;
    }
    glutPostRedisplay();
}

// Função de teclas especiais
void specialKeys(int key, int x, int y) {
    switch (key) {
        case GLUT_KEY_RIGHT:
            currentDemo = (currentDemo + 1) % MAX_DEMOS;
            break;
        case GLUT_KEY_LEFT:
            currentDemo = (currentDemo - 1) % MAX_DEMOS;
            break;
    }
    glutPostRedisplay();
}

// Função de atualização (para animação)
void update(int value) {
    rotationAngle += 2.0f;
    if (rotationAngle > 360.0f) {
        rotationAngle -= 360.0f;
    }
    glutPostRedisplay();
    glutTimerFunc(16, update, 0); // ~60 FPS
}

// Função principal
int main(int argc, char **argv) { 
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
    glutInitWindowSize(800, 600);
    glutInitWindowPosition(100, 100);
    glutCreateWindow("Analise de Cores e Transparencias - GLUT/OpenGL");

    init();

    glutDisplayFunc(display);
    glutReshapeFunc(reshape);
    glutKeyboardFunc(keyboard);
    glutSpecialFunc(specialKeys);
    glutTimerFunc(16, update, 0);

    std::cout << "=== ANALISE DE CORES E TRANSPARENCIAS ===\n";
    std::cout << "Controles:\n";
    std::cout << "- Setas esquerda/direita: Navegar entre demos\n";
    std::cout << "- B: Habilitar/desabilitar blending (transparencia)\n";
    std::cout << "- ESC: Sair\n\n";
    std::cout << "Demos disponiveis:\n";
    std::cout << "1. Cores basicas RGB\n";
    std::cout << "2. Gradientes RGBA\n";
    std::cout << "3. Transparencia\n";
    std::cout << "4. Formatos de cor \n";
    std::cout << "5. Iluminacao e Materiais\n";
    std::cout << "6. Animacao de Cores\n";

    glutMainLoop();
    return 0;
}

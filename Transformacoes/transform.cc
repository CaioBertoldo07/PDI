#include <GL/glut.h>
#include <GL/gl.h>
#include <GL/glu.h>
#include <math.h>
#include <iostream>

// Variáveis para controlar as trasnformações
float translateX = 0.0f, translateY = 0.0f;
float scaleX = 1.0f, scaleY = 1.0f;
float rotationAngle = 0.0f;
bool reflectX = false, reflectY = false;
int currentShape = 0; // 0 = quadrado, 1 = triângulo, 2 = círculo

// Área desejada para todas as formas
const float AREA = 1.0f;

// Calculando dimensões para mesma área
const float SQUARE_SIDE = sqrt(AREA);                         // lado = √área
const float TRIANGLE_SIDE = sqrt((4.0f * AREA) / sqrt(3.0f)); // lado = √(4*área/√3)
const float CIRCLE_RADIUS = sqrt(AREA / M_PI);                // raio = √(área/π)

// Função para aplicar transformações customizadas
void applyCustomTransformations()
{
    // Translação
    glTranslatef(translateX, translateY, 0.0f);

    // Reflexão customizada (implementada como escala negativa)
    float reflectScaleX = reflectX ? -1.0f : 1.0f;
    float reflectScaleY = reflectY ? -1.0f : 1.0f;
    glScalef(reflectScaleX, reflectScaleY, 1.0f);

    // Escala
    glScalef(scaleX, scaleY, 1.0f);

    // Rotação 
    glRotatef(rotationAngle, 0.0f, 0.0f, 1.0f);
}

// Matriz de trasnformação personalizada para rotação
void customRotate(float angle, float x, float y, float z)
{
    float radians = angle * M_PI / 180.0f;
    float cosA = cos(radians);
    float sinA = sin(radians);

    

    GLfloat rotMatrix[16] = {
        cosA, sinA, 0, 0,
        -sinA, cosA, 0, 0,
        0, 0, 1, 0,
        0, 0, 0, 1};

    glMultMatrixf(rotMatrix);
}

// Função para desenhar quadrado
void drawSquare()
{
    float halfSide = SQUARE_SIDE / 2.0f;

    glColor3f(1.0f, 0.0f, 0.0f); // Vermelho
    glBegin(GL_QUADS);
    glVertex2f(-halfSide, -halfSide);
    glVertex2f(halfSide, -halfSide);
    glVertex2f(halfSide, halfSide);
    glVertex2f(-halfSide, halfSide);
    glEnd();
}

// Função para desenhar triângulo equilátero
void drawTriangle()
{
    float height = (TRIANGLE_SIDE * sqrt(3.0f)) / 2.0f;
    float halfBase = TRIANGLE_SIDE / 2.0f;
    float centroidY = height / 3.0f;

    glColor3f(0.0f, 1.0f, 0.0f); // Verde
    glBegin(GL_TRIANGLES);
    glVertex2f(0.0f, height - centroidY);
    glVertex2f(-halfBase, -centroidY);
    glVertex2f(halfBase, -centroidY);
    glEnd();
}

// Função para desenhar círculo
void drawCircle()
{
    const int segments = 100;

    glColor3f(0.0f, 0.0f, 1.0f); // azul
    glBegin(GL_TRIANGLE_FAN);
    glVertex2f(0.0f, 0.0f); // centro
    for (int i = 0; i <= segments; i++)
    {
        float angle = 2.0f * M_PI * i / segments;
        float x = CIRCLE_RADIUS * cos(angle);
        float y = CIRCLE_RADIUS * sin(angle);
        glVertex2f(x, y);
    }
    glEnd();
}

// Função de display
void display()
{
    glClear(GL_COLOR_BUFFER_BIT);
    glLoadIdentity();

    // Aplicar transformações
    applyCustomTransformations();

    // Desenhar  forma atual
    switch (currentShape)
    {
    case 0:
        drawSquare();
        break;
    case 1:
        drawTriangle();
        break;
    case 2:
        drawCircle();
        break;
    }

    // resetar matriz para desenhar texto
    glLoadIdentity();

    // Desenhar informações na tela
    glColor3f(1.0f, 1.0f, 1.0f);
    glRasterPos2f(-0.95f, 0.0f);

    const char *shapeNames[] = {"Quadrado", "Triangulo", "Circulo"};
    std::string info = "Forma: " + std::string(shapeNames[currentShape]);
    for (char c : info)
    {
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, c);
    }

    glRasterPos2f(-0.95f, 0.85f);
    std::string controls = "Controles: 1,2,3=formas | WASD=translacao | QE=escala | RF=rotacao | XY=reflexao | ESPACO=reset";
    for (char c : controls)
    {
        glutBitmapCharacter(GLUT_BITMAP_8_BY_13, c);
    }

    glutSwapBuffers();
}

// Função de reshape
void reshape(int width, int height)
{
    if (height == 0)
        height = 1;

    glViewport(0, 0, width, height);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    float aspect = (float)width / (float)height;
    if (width >= height)
    {
        glOrtho(-2.0 * aspect, 2.0 * aspect, -2.0, 2.0, -1.0, 1.0);
    }
    else
    {
        glOrtho(-2.0, 2.0, -2.0 / aspect, 2.0 / aspect, -1.0, 1.0);
    }

    glMatrixMode(GL_MODELVIEW);
}

// Função para resetar transformações
void resetTransformations()
{
    translateX = translateY = 0.0f;
    scaleX = scaleY = 1.0f;
    rotationAngle = 0.0f;
    reflectX = reflectY = false;
}

// Função de teclado
void keyboard(unsigned char key, int x, int y)
{
    const float TRANSLATE_STEP = 0.1f;
    const float SCALE_STEP = 0.1f;
    const float ROTATION_STEP = 5.0f;

    switch (key)
    {
    // Seleção de formas
    case '1':
        currentShape = 0;
        break; // quadrado
    case '2':
        currentShape = 1;
        break; // Triângulo
    case '3':
        currentShape = 2;
        break; // Círculo

    // Translação
    case 'w':
    case 'W':
        translateY += TRANSLATE_STEP;
        break;
    case 's':
    case 'S':
        translateY -= TRANSLATE_STEP;
        break;
    case 'a':
    case 'A':
        translateX -= TRANSLATE_STEP;
        break;
    case 'd':
    case 'D':
        translateX += TRANSLATE_STEP;
        break;

    // Escala
    case 'q':
    case 'Q':
        scaleX += SCALE_STEP;
        scaleY += SCALE_STEP;
        break;
    case 'e':
    case 'E':
        scaleX -= SCALE_STEP;
        scaleY -= SCALE_STEP;
        if (scaleX < 0.0f)
            scaleX = 1.0f;
        if (scaleY < 0.1f)
            scaleY = 0.1f;
        break;

    // Rotação
    case 'r':
    case 'R':
        rotationAngle += ROTATION_STEP;
        break;
    case 'f':
    case 'F':
        rotationAngle -= ROTATION_STEP;
        break;

    // Reflexão
    case 'x':
    case 'X':
        reflectX = !reflectX;
        break;
    case 'y':
    case 'Y':
        reflectY = !reflectY;
        break;

    // Reset
    case ' ':
        resetTransformations();
        break;

    // Sair
    case 27:
        exit(0);
        break; // ESC
    }
    glutPostRedisplay();
}

// Função de inicialização
void init()
{
    glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    // Imprimir informações sobre as áreas
    std::cout << "=== INFORMACOES DAS FORMAS ===" << std::endl;
    std::cout << "Area desejada: " << AREA << std::endl;
    std::cout << "Quadrado - Lado: " << SQUARE_SIDE << ", Area: " << SQUARE_SIDE * SQUARE_SIDE << std::endl;
    std::cout << "Triangulo - Lado: " << TRIANGLE_SIDE << ", Area: " << (TRIANGLE_SIDE * TRIANGLE_SIDE * sqrt(3.0f)) / 4.0f << std::endl;
    std::cout << "Circulo - Raio: " << CIRCLE_RADIUS << ", Area: " << M_PI * CIRCLE_RADIUS * CIRCLE_RADIUS << std::endl;
    std::cout << "\n=== CONTROLES ===\n"
              << std::endl;
    std::cout << "1, 2, 3: Alternar entre quadrado, triangulo e circulo" << std::endl;
    std::cout << "W, A, S, D: Translacao" << std::endl;
    std::cout << "Q, E: Aumentar/diminuir escala" << std::endl;
    std::cout << "R, F: Rotacao horaria/anti-horaria" << std::endl;
    std::cout << "X, Y: Relexao nos eixos X e Y" << std::endl;
    std::cout << "ESPACO: Reset das transformacoes" << std::endl;
    std::cout << "ESC: Sair" << std::endl;
}

// Função principal
int main(int argc, char **argv)
{
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
    glutInitWindowSize(800, 600);
    glutInitWindowPosition(100, 160);
    glutCreateWindow("Formas Geometricas com Transformacoes");

    init();

    glutDisplayFunc(display);
    glutReshapeFunc(reshape);
    glutKeyboardFunc(keyboard);

    glutMainLoop();

    return 0;
}

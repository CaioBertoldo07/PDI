#include <GL/glut.h>
#include <GL/gl.h>
#include <GL/glu.h>
#include <math.h>
#include <iostream>
#include <vector>

// Estrutura para armazenar pontos 2D
struct Point2D
{
    float x, y;
    Point2D(float _x = 0, float _y = 0) : x(_x), y(_y) {}
};

// Variáveis para controlar as transformações
float translateX = 0.0f, translateY = 0.0f;
float scaleX = 1.0f, scaleY = 1.0f;
float rotationAngle = 0.0f;
bool reflectX = false, reflectY = false;
int currentShape = 0;             // 0=quadrado, 1=triângulo, 2=círculo
bool useManualTransforms = false; // false=OpenGL, true=Manual

// Área desejada para todas as formas
const float AREA = 1.0f;

// Calculando dimensões para mesma área
const float SQUARE_SIDE = sqrt(AREA);                         // lado = √área
const float TRIANGLE_SIDE = sqrt((4.0f * AREA) / sqrt(3.0f)); // lado = √(4*área/√3)
const float CIRCLE_RADIUS = sqrt(AREA / M_PI);                // raio = √(área/π)

// ============================================================================
// FUNÇÕES DE TRANSFORMAÇÃO MANUAL
// ============================================================================

// Função manual de translação
Point2D manualTranslate(const Point2D &p, float tx, float ty)
{
    return Point2D(p.x + tx, p.y + ty);
}

// Função manual de escala
Point2D manualScale(const Point2D &p, float sx, float sy)
{
    return Point2D(p.x * sx, p.y * sy);
}

// Função manual de rotação
Point2D manualRotate(const Point2D &p, float angle)
{
    float radians = angle * M_PI / 180.0f;
    float cosA = cos(radians);
    float sinA = sin(radians);

    return Point2D(
        p.x * cosA - p.y * sinA,
        p.x * sinA + p.y * cosA);
}

// Função manual de reflexão
Point2D manualReflect(const Point2D &p, bool reflX, bool reflY)
{
    float nx = reflX ? -p.x : p.x;
    float ny = reflY ? -p.y : p.y;
    return Point2D(nx, ny);
}

// Aplicar todas as transformações manuais em um ponto
Point2D applyManualTransformations(const Point2D &p)
{
    Point2D result = p;

    // Ordem das transformações: Rotação -> Escala -> Reflexão -> Translação
    result = manualRotate(result, rotationAngle);
    result = manualScale(result, scaleX, scaleY);
    result = manualReflect(result, reflectX, reflectY);
    result = manualTranslate(result, translateX, translateY);

    return result;
}

// ============================================================================
// FUNÇÕES DE TRANSFORMAÇÃO USANDO OPENGL
// ============================================================================

// Função para aplicar transformações customizadas
void applyCustomTransformations()
{
    // Translação customizada
    glTranslatef(translateX, translateY, 0.0f);

    // Reflexão customizada (implementada como escala negativa)
    float reflectScaleX = reflectX ? -1.0f : 1.0f;
    float reflectScaleY = reflectY ? -1.0f : 1.0f;
    glScalef(reflectScaleX, reflectScaleY, 1.0f);

    // Escala customizada
    glScalef(scaleX, scaleY, 1.0f);

    // Rotação customizada
    glRotatef(rotationAngle, 0.0f, 0.0f, 1.0f);
}

// Matriz de transformação personalizada para rotação
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

    if (useManualTransforms)
    {
        // Desenhar usando transformações manuais
        std::vector<Point2D> vertices = {
            Point2D(-halfSide, -halfSide),
            Point2D(halfSide, -halfSide),
            Point2D(halfSide, halfSide),
            Point2D(-halfSide, halfSide)};

        glBegin(GL_QUADS);
        for (const auto &v : vertices)
        {
            Point2D transformed = applyManualTransformations(v);
            glVertex2f(transformed.x, transformed.y);
        }
        glEnd();
    }
    else
    {
        // Desenhar usando funções OpenGL
        glBegin(GL_QUADS);
        glVertex2f(-halfSide, -halfSide);
        glVertex2f(halfSide, -halfSide);
        glVertex2f(halfSide, halfSide);
        glVertex2f(-halfSide, halfSide);
        glEnd();
    }
}

// Função para desenhar triângulo equilátero
void drawTriangle()
{
    float height = (TRIANGLE_SIDE * sqrt(3.0f)) / 2.0f;
    float halfBase = TRIANGLE_SIDE / 2.0f;
    float centroidY = height / 3.0f;

    glColor3f(0.0f, 1.0f, 0.0f); // Verde

    if (useManualTransforms)
    {
        // Desenhar usando transformações manuais
        std::vector<Point2D> vertices = {
            Point2D(0.0f, height - centroidY),
            Point2D(-halfBase, -centroidY),
            Point2D(halfBase, -centroidY)};

        glBegin(GL_TRIANGLES);
        for (const auto &v : vertices)
        {
            Point2D transformed = applyManualTransformations(v);
            glVertex2f(transformed.x, transformed.y);
        }
        glEnd();
    }
    else
    {
        // Desenhar usando funções OpenGL
        glBegin(GL_TRIANGLES);
        glVertex2f(0.0f, height - centroidY);
        glVertex2f(-halfBase, -centroidY);
        glVertex2f(halfBase, -centroidY);
        glEnd();
    }
}

// Função para desenhar círculo
void drawCircle()
{
    const int segments = 100;

    glColor3f(0.0f, 0.0f, 1.0f); // Azul

    if (useManualTransforms)
    {
        // Desenhar usando transformações manuais
        std::vector<Point2D> vertices;
        vertices.push_back(Point2D(0.0f, 0.0f)); // Centro

        for (int i = 0; i <= segments; i++)
        {
            float angle = 2.0f * M_PI * i / segments;
            float x = CIRCLE_RADIUS * cos(angle);
            float y = CIRCLE_RADIUS * sin(angle);
            vertices.push_back(Point2D(x, y));
        }

        glBegin(GL_TRIANGLE_FAN);
        for (const auto &v : vertices)
        {
            Point2D transformed = applyManualTransformations(v);
            glVertex2f(transformed.x, transformed.y);
        }
        glEnd();
    }
    else
    {
        // Desenhar usando funções OpenGL
        glBegin(GL_TRIANGLE_FAN);
        glVertex2f(0.0f, 0.0f);
        for (int i = 0; i <= segments; i++)
        {
            float angle = 2.0f * M_PI * i / segments;
            float x = CIRCLE_RADIUS * cos(angle);
            float y = CIRCLE_RADIUS * sin(angle);
            glVertex2f(x, y);
        }
        glEnd();
    }
}

// Função de display
void display()
{
    glClear(GL_COLOR_BUFFER_BIT);
    glLoadIdentity();

    // Aplicar transformações apenas se estiver usando OpenGL
    if (!useManualTransforms)
    {
        applyCustomTransformations();
    }

    // Desenhar forma atual (as funções já lidam com manual vs OpenGL)
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

    // Resetar matriz para desenhar texto
    glLoadIdentity();

    // Desenhar informações na tela
    glColor3f(1.0f, 1.0f, 1.0f);
    glRasterPos2f(-0.95f, 0.9f);

    const char *shapeNames[] = {"Quadrado", "Triangulo", "Circulo"};
    std::string info = "Forma: " + std::string(shapeNames[currentShape]);
    for (char c : info)
    {
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, c);
    }

    glRasterPos2f(-0.95f, 0.84f);
    std::string mode = useManualTransforms ? "Modo: MANUAL (M para alternar)" : "Modo: OPENGL (M para alternar)";
    for (char c : mode)
    {
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, c);
    }

    glRasterPos2f(-0.95f, 0.78f);
    std::string controls = "1,2,3=formas | WASD=translacao | QE=escala | RF=rotacao | XY=reflexao | ESPACO=reset";
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
        break; // Quadrado
    case '2':
        currentShape = 1;
        break; // Triângulo
    case '3':
        currentShape = 2;
        break; // Círculo

    // Alternar entre modo manual e OpenGL
    case 'm':
    case 'M':
        useManualTransforms = !useManualTransforms;
        std::cout << "Modo alterado para: " << (useManualTransforms ? "MANUAL" : "OPENGL") << std::endl;
        break;

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
        if (scaleX < 0.1f)
            scaleX = 0.1f;
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
    std::cout << "\n=== CONTROLES ===" << std::endl;
    std::cout << "M: Alternar entre transformacoes OpenGL e Manuais" << std::endl;
    std::cout << "1, 2, 3: Alternar entre quadrado, triangulo e circulo" << std::endl;
    std::cout << "W, A, S, D: Translacao" << std::endl;
    std::cout << "Q, E: Aumentar/diminuir escala" << std::endl;
    std::cout << "R, F: Rotacao horaria/anti-horaria" << std::endl;
    std::cout << "X, Y: Reflexao nos eixos X e Y" << std::endl;
    std::cout << "ESPACO: Reset das transformacoes" << std::endl;
    std::cout << "ESC: Sair" << std::endl;
    std::cout << "\n=== MODOS DE TRANSFORMACAO ===" << std::endl;
    std::cout << "OpenGL: Usa glTranslatef, glScalef, glRotatef" << std::endl;
    std::cout << "Manual: Usa funcoes matematicas proprias" << std::endl;
}

// Função principal
int main(int argc, char **argv)
{
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
    glutInitWindowSize(800, 600);
    glutInitWindowPosition(100, 100);
    glutCreateWindow("Formas Geometricas com Transformacoes - OpenGL/GLUT");

    init();

    glutDisplayFunc(display);
    glutReshapeFunc(reshape);
    glutKeyboardFunc(keyboard);

    glutMainLoop();

    return 0;
}
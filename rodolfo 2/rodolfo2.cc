#include <GL/glut.h>
#include <cmath>

// ---------- Dados de área ----------
float ladoQuadrado = 1.0f;                   // área = 1
float ladoTriangulo = sqrt(4.0 / sqrt(3.0)); // lado ≈ 1.5197
float raioCirculo = sqrt(1.0 / M_PI);        // raio ≈ 0.564

// ---------- Funções próprias de transformação ----------
void refletirX(float &x, float &y)
{
    y = -y; // reflexão em relação ao eixo X
}

void refletirY(float &x, float &y)
{
    x = -x; // reflexão em relação ao eixo Y
}

// ---------- Funções para desenho ----------
void drawSquare()
{
    float h = ladoQuadrado / 2.0f;
    glBegin(GL_QUADS);
    glVertex2f(-h, -h);
    glVertex2f(h, -h);
    glVertex2f(h, h);
    glVertex2f(-h, h);
    glEnd();
}

// Triângulo com reflexão manual em relação ao eixo Y
void drawTriangleRefletido()
{
    float h = sqrt(3.0f) / 2.0f * ladoTriangulo;

    // Coordenadas originais do triângulo equilátero
    float x1 = -ladoTriangulo / 2, y1 = -h / 3;
    float x2 = ladoTriangulo / 2, y2 = -h / 3;
    float x3 = 0, y3 = 2 * h / 3;

    // Aplicar reflexão em Y nos vértices
    refletirY(x1, y1);
    refletirY(x2, y2);
    refletirY(x3, y3);

    // Desenhar triângulo refletido
    glBegin(GL_TRIANGLES);
    glVertex2f(x1, y1);
    glVertex2f(x2, y2);
    glVertex2f(x3, y3);
    glEnd();
}

void drawCircle(int num_segments = 100)
{
    glBegin(GL_POLYGON);
    for (int i = 0; i < num_segments; i++)
    {
        float theta = 2.0f * M_PI * i / num_segments;
        float x = raioCirculo * cos(theta);
        float y = raioCirculo * sin(theta);
        glVertex2f(x, y);
    }
    glEnd();
}

// ---------- Exibição ----------
void display()
{
    glClear(GL_COLOR_BUFFER_BIT);

    // Quadrado - azul (transformações internas do OpenGL)
    glPushMatrix();
    glColor3f(0, 0, 1);
    glTranslatef(-1.5, 0.0, 0.0); // translação
    glRotatef(45, 0, 0, 1);       // rotação 45 graus
    glScalef(1.2, 1.2, 1);        // escala
    drawSquare();
    glPopMatrix();

    // Triângulo - vermelho (com reflexão manual + translação e rotação internas)
    glPushMatrix();
    glColor3f(1, 0, 0);
    glTranslatef(1.5, 0.0, 0.0); // translação
    glRotatef(-30, 0, 0, 1);     // rotação
    drawTriangleRefletido();     // reflexão manual
    glPopMatrix();

    // Círculo - verde (transformações internas do OpenGL)
    glPushMatrix();
    glColor3f(0, 1, 0);
    glTranslatef(0.0, -1.5, 0.0); // translação
    glScalef(1.5, 0.5, 1.0);      // escala não uniforme
    drawCircle();
    glPopMatrix();

    glFlush();
}

// ---------- Configuração ----------
void init()
{
    glClearColor(1, 1, 1, 1); // fundo branco
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(-3, 3, -3, 3);
}

int main(int argc, char **argv)
{
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
    glutInitWindowSize(600, 600);
    glutCreateWindow("Quadrado, Triângulo e Círculo com Transformações");
    init();
    glutDisplayFunc(display);
    glutMainLoop();
    return 0;
}
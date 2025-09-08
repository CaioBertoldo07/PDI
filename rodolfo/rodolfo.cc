#include <GL/glut.h>
#include <cmath>

// Função para desenhar um círculo
void drawCircle(float cx, float cy, float r, int num_segments)
{
    glBegin(GL_POLYGON);
    for (int i = 0; i < num_segments; i++)
    {
        float theta = 2.0f * 3.1415926f * float(i) / float(num_segments);
        float x = r * cosf(theta);
        float y = r * sinf(theta);
        glVertex2f(x + cx, y + cy);
    }
    glEnd();
}

// Função de exibição
void display()
{
    glClear(GL_COLOR_BUFFER_BIT);

    // Desenhar quadrado azul opaco
    glColor3f(0.0f, 0.0f, 1.0f); // Azul sólido
    glBegin(GL_QUADS);
    glVertex2f(-0.5f, -0.5f);
    glVertex2f(0.5f, -0.5f);
    glVertex2f(0.5f, 0.5f);
    glVertex2f(-0.5f, 0.5f);
    glEnd();

    // Ativar blending para transparência
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    // Desenhar círculo amarelo semi-transparente
    glColor4f(1.0f, 1.0f, 0.0f, 0.5f); // Amarelo com 50% de transparência
    drawCircle(0.0f, 0.0f, 0.3f, 100);

    glDisable(GL_BLEND);

    glFlush();
}

// Função principal
int main(int argc, char **argv)
{
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
    glutInitWindowSize(600, 600);
    glutInitWindowPosition(100, 100);
    glutCreateWindow("Quadrado Azul e Circulo Amarelo Transparente");
    glutDisplayFunc(display);
    glutMainLoop();
    return 0;
}
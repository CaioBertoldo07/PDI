# Makefile para compilar programa OpenGL com GLUT

CXX = g++
CXXFLAGS = -Wall -O3 -std=c++17
LIBS = -lglut -lGLU -lGL -lm
TARGET = gpu_test_glut
SRC = main_glut.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC) $(LIBS)
	@echo ""
	@echo "✓ Compilação concluída com sucesso!"
	@echo "Execute com: ./$(TARGET)"
	@echo ""

clean:
	rm -f $(TARGET)
	@echo "Arquivos limpos"

run: $(TARGET)
	./$(TARGET)

.PHONY: all clean run

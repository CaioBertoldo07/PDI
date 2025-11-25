"""
Script Complementar: Demonstração Didática de Antiserrilhamento
Cria exemplos sintéticos para ilustrar o conceito de aliasing e anti-aliasing

Aluno: Caio Bertoldo Bezerra
UEA - Processamento Digital de Imagens
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt


class AntiAliasingDidatico:
    """
    Classe para criar demonstrações didáticas de anti-aliasing
    """
    
    def __init__(self):
        self.output_dir = "exemplos_didaticos"
        import os
        os.makedirs(self.output_dir, exist_ok=True)
    
    def criar_linha_diagonal_sem_aa(self, tamanho=400):
        """
        Cria uma linha diagonal SEM anti-aliasing (serrilhada)
        
        Args:
            tamanho: Tamanho da imagem (quadrada)
            
        Returns:
            Imagem com linha diagonal serrilhada
        """
        img = np.zeros((tamanho, tamanho, 3), dtype=np.uint8)
        img.fill(255)  # Fundo branco
        
        # Desenhar linha diagonal sem anti-aliasing
        cv2.line(img, (50, 50), (tamanho-50, tamanho-50), (0, 0, 255), 2, cv2.LINE_4)
        
        return img
    
    def criar_linha_diagonal_com_aa(self, tamanho=400):
        """
        Cria uma linha diagonal COM anti-aliasing (suave)
        
        Args:
            tamanho: Tamanho da imagem (quadrada)
            
        Returns:
            Imagem com linha diagonal suavizada
        """
        img = np.zeros((tamanho, tamanho, 3), dtype=np.uint8)
        img.fill(255)  # Fundo branco
        
        # Desenhar linha diagonal com anti-aliasing
        cv2.line(img, (50, 50), (tamanho-50, tamanho-50), (0, 0, 255), 2, cv2.LINE_AA)
        
        return img
    
    def criar_circulo_sem_aa(self, tamanho=400):
        """
        Cria um círculo SEM anti-aliasing
        """
        img = np.zeros((tamanho, tamanho, 3), dtype=np.uint8)
        img.fill(255)
        
        centro = (tamanho // 2, tamanho // 2)
        raio = tamanho // 3
        
        cv2.circle(img, centro, raio, (255, 0, 0), 2, cv2.LINE_4)
        
        return img
    
    def criar_circulo_com_aa(self, tamanho=400):
        """
        Cria um círculo COM anti-aliasing
        """
        img = np.zeros((tamanho, tamanho, 3), dtype=np.uint8)
        img.fill(255)
        
        centro = (tamanho // 2, tamanho // 2)
        raio = tamanho // 3
        
        cv2.circle(img, centro, raio, (255, 0, 0), 2, cv2.LINE_AA)
        
        return img
    
    def criar_texto_sem_aa(self, tamanho=400):
        """
        Cria texto SEM anti-aliasing
        """
        img = np.zeros((tamanho, tamanho, 3), dtype=np.uint8)
        img.fill(255)
        
        texto = "AA"
        fonte = cv2.FONT_HERSHEY_SIMPLEX
        escala = 5
        espessura = 10
        
        # Calcular tamanho do texto para centralizar
        (w, h), _ = cv2.getTextSize(texto, fonte, escala, espessura)
        x = (tamanho - w) // 2
        y = (tamanho + h) // 2
        
        cv2.putText(img, texto, (x, y), fonte, escala, (0, 128, 0), espessura, cv2.LINE_4)
        
        return img
    
    def criar_texto_com_aa(self, tamanho=400):
        """
        Cria texto COM anti-aliasing
        """
        img = np.zeros((tamanho, tamanho, 3), dtype=np.uint8)
        img.fill(255)
        
        texto = "AA"
        fonte = cv2.FONT_HERSHEY_SIMPLEX
        escala = 5
        espessura = 10
        
        # Calcular tamanho do texto para centralizar
        (w, h), _ = cv2.getTextSize(texto, fonte, escala, espessura)
        x = (tamanho - w) // 2
        y = (tamanho + h) // 2
        
        cv2.putText(img, texto, (x, y), fonte, escala, (0, 128, 0), espessura, cv2.LINE_AA)
        
        return img
    
    def criar_comparacao_zoom(self, img_sem_aa, img_com_aa, fator_zoom=4):
        """
        Cria uma comparação com zoom para visualizar melhor o efeito
        """
        altura, largura = img_sem_aa.shape[:2]
        centro_y, centro_x = altura // 2, largura // 2
        tamanho_crop = 50
        
        # Extrair região central
        y1 = centro_y - tamanho_crop
        y2 = centro_y + tamanho_crop
        x1 = centro_x - tamanho_crop
        x2 = centro_x + tamanho_crop
        
        crop_sem_aa = img_sem_aa[y1:y2, x1:x2]
        crop_com_aa = img_com_aa[y1:y2, x1:x2]
        
        # Aplicar zoom
        novo_tamanho = (tamanho_crop * fator_zoom * 2, tamanho_crop * fator_zoom * 2)
        zoom_sem_aa = cv2.resize(crop_sem_aa, novo_tamanho, interpolation=cv2.INTER_NEAREST)
        zoom_com_aa = cv2.resize(crop_com_aa, novo_tamanho, interpolation=cv2.INTER_NEAREST)
        
        return zoom_sem_aa, zoom_com_aa
    
    def demonstrar_linhas(self):
        """
        Demonstra o efeito em linhas diagonais
        """
        print("→ Gerando demonstração de linhas diagonais...")
        
        img_sem_aa = self.criar_linha_diagonal_sem_aa()
        img_com_aa = self.criar_linha_diagonal_com_aa()
        
        zoom_sem_aa, zoom_com_aa = self.criar_comparacao_zoom(img_sem_aa, img_com_aa)
        
        # Criar visualização
        fig, axes = plt.subplots(2, 2, figsize=(14, 14))
        fig.suptitle('Anti-aliasing em Linhas Diagonais', fontsize=16, fontweight='bold')
        
        axes[0, 0].imshow(cv2.cvtColor(img_sem_aa, cv2.COLOR_BGR2RGB))
        axes[0, 0].set_title('SEM Anti-aliasing\n(Serrilhamento visível)')
        axes[0, 0].axis('off')
        
        axes[0, 1].imshow(cv2.cvtColor(img_com_aa, cv2.COLOR_BGR2RGB))
        axes[0, 1].set_title('COM Anti-aliasing\n(Bordas suaves)')
        axes[0, 1].axis('off')
        
        axes[1, 0].imshow(cv2.cvtColor(zoom_sem_aa, cv2.COLOR_BGR2RGB))
        axes[1, 0].set_title('Zoom - SEM AA\n(Pixels em "escada")')
        axes[1, 0].axis('off')
        
        axes[1, 1].imshow(cv2.cvtColor(zoom_com_aa, cv2.COLOR_BGR2RGB))
        axes[1, 1].set_title('Zoom - COM AA\n(Transição suave)')
        axes[1, 1].axis('off')
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/demonstracao_linhas.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  ✓ Salvo: demonstracao_linhas.png")
    
    def demonstrar_circulos(self):
        """
        Demonstra o efeito em círculos
        """
        print("→ Gerando demonstração de círculos...")
        
        img_sem_aa = self.criar_circulo_sem_aa()
        img_com_aa = self.criar_circulo_com_aa()
        
        zoom_sem_aa, zoom_com_aa = self.criar_comparacao_zoom(img_sem_aa, img_com_aa)
        
        # Criar visualização
        fig, axes = plt.subplots(2, 2, figsize=(14, 14))
        fig.suptitle('Anti-aliasing em Círculos', fontsize=16, fontweight='bold')
        
        axes[0, 0].imshow(cv2.cvtColor(img_sem_aa, cv2.COLOR_BGR2RGB))
        axes[0, 0].set_title('SEM Anti-aliasing\n(Bordas dentadas)')
        axes[0, 0].axis('off')
        
        axes[0, 1].imshow(cv2.cvtColor(img_com_aa, cv2.COLOR_BGR2RGB))
        axes[0, 1].set_title('COM Anti-aliasing\n(Bordas arredondadas)')
        axes[0, 1].axis('off')
        
        axes[1, 0].imshow(cv2.cvtColor(zoom_sem_aa, cv2.COLOR_BGR2RGB))
        axes[1, 0].set_title('Zoom - SEM AA\n(Efeito de degraus)')
        axes[1, 0].axis('off')
        
        axes[1, 1].imshow(cv2.cvtColor(zoom_com_aa, cv2.COLOR_BGR2RGB))
        axes[1, 1].set_title('Zoom - COM AA\n(Gradiente suave)')
        axes[1, 1].axis('off')
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/demonstracao_circulos.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  ✓ Salvo: demonstracao_circulos.png")
    
    def demonstrar_texto(self):
        """
        Demonstra o efeito em texto
        """
        print("→ Gerando demonstração de texto...")
        
        img_sem_aa = self.criar_texto_sem_aa()
        img_com_aa = self.criar_texto_com_aa()
        
        zoom_sem_aa, zoom_com_aa = self.criar_comparacao_zoom(img_sem_aa, img_com_aa)
        
        # Criar visualização
        fig, axes = plt.subplots(2, 2, figsize=(14, 14))
        fig.suptitle('Anti-aliasing em Texto', fontsize=16, fontweight='bold')
        
        axes[0, 0].imshow(cv2.cvtColor(img_sem_aa, cv2.COLOR_BGR2RGB))
        axes[0, 0].set_title('SEM Anti-aliasing\n(Texto áspero)')
        axes[0, 0].axis('off')
        
        axes[0, 1].imshow(cv2.cvtColor(img_com_aa, cv2.COLOR_BGR2RGB))
        axes[0, 1].set_title('COM Anti-aliasing\n(Texto suavizado)')
        axes[0, 1].axis('off')
        
        axes[1, 0].imshow(cv2.cvtColor(zoom_sem_aa, cv2.COLOR_BGR2RGB))
        axes[1, 0].set_title('Zoom - SEM AA\n(Bordas irregulares)')
        axes[1, 0].axis('off')
        
        axes[1, 1].imshow(cv2.cvtColor(zoom_com_aa, cv2.COLOR_BGR2RGB))
        axes[1, 1].set_title('Zoom - COM AA\n(Legibilidade melhorada)')
        axes[1, 1].axis('off')
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/demonstracao_texto.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  ✓ Salvo: demonstracao_texto.png")
    
    def explicar_pixel_level(self):
        """
        Cria uma explicação a nível de pixel do anti-aliasing
        """
        print("→ Gerando explicação a nível de pixel...")
        
        # Criar um padrão simples para demonstrar
        tamanho = 20
        img_aliased = np.ones((tamanho, tamanho, 3), dtype=np.uint8) * 255
        img_antialiased = np.ones((tamanho, tamanho, 3), dtype=np.uint8) * 255
        
        # Linha diagonal aliased (serrilhada)
        for i in range(tamanho):
            j = i
            if j < tamanho:
                img_aliased[i, j] = [255, 0, 0]
        
        # Linha diagonal antialiased (com tons intermediários)
        for i in range(tamanho):
            j = i
            if j < tamanho:
                img_antialiased[i, j] = [255, 0, 0]
                # Adicionar pixels de transição
                if j > 0:
                    img_antialiased[i, j-1] = [255, 128, 128]
                if j < tamanho - 1:
                    img_antialiased[i, j+1] = [255, 128, 128]
        
        # Ampliar para visualização
        fator = 20
        img_aliased_zoom = cv2.resize(img_aliased, 
                                     (tamanho * fator, tamanho * fator), 
                                     interpolation=cv2.INTER_NEAREST)
        img_antialiased_zoom = cv2.resize(img_antialiased, 
                                         (tamanho * fator, tamanho * fator), 
                                         interpolation=cv2.INTER_NEAREST)
        
        # Criar visualização
        fig, axes = plt.subplots(1, 2, figsize=(16, 8))
        fig.suptitle('Anti-aliasing a Nível de Pixel', fontsize=16, fontweight='bold')
        
        axes[0].imshow(cv2.cvtColor(img_aliased_zoom, cv2.COLOR_BGR2RGB))
        axes[0].set_title('SEM Anti-aliasing\n(Apenas pixels vermelhos ou brancos)')
        axes[0].grid(True, color='gray', linewidth=0.5)
        axes[0].set_xticks(np.arange(0, tamanho * fator, fator))
        axes[0].set_yticks(np.arange(0, tamanho * fator, fator))
        
        axes[1].imshow(cv2.cvtColor(img_antialiased_zoom, cv2.COLOR_BGR2RGB))
        axes[1].set_title('COM Anti-aliasing\n(Pixels intermediários criam transição suave)')
        axes[1].grid(True, color='gray', linewidth=0.5)
        axes[1].set_xticks(np.arange(0, tamanho * fator, fator))
        axes[1].set_yticks(np.arange(0, tamanho * fator, fator))
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/explicacao_pixel_level.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  ✓ Salvo: explicacao_pixel_level.png")
    
    def criar_diagrama_conceitual(self):
        """
        Cria um diagrama conceitual explicando o anti-aliasing
        """
        print("→ Gerando diagrama conceitual...")
        
        fig = plt.figure(figsize=(14, 10))
        
        # Texto explicativo
        explicacao = """
        CONCEITO DE ANTISERRILHAMENTO (ANTI-ALIASING)
        
        PROBLEMA:
        • Em imagens digitais, pixels são quadrados discretos
        • Linhas diagonais e curvas aparecem como "degraus" (aliasing/serrilhamento)
        • Resulta em bordas ásperas e visuais desagradáveis
        
        CAUSA:
        • Amostragem discreta de uma forma contínua
        • Teorema de Nyquist: frequências altas causam aliasing
        • Pixels ou são 100% da cor ou 0%
        
        SOLUÇÃO - ANTI-ALIASING:
        • Adiciona pixels de transição com cores intermediárias
        • Cria gradientes suaves entre cores
        • Simula resolução mais alta
        
        TÉCNICAS PRINCIPAIS:
        
        1. SUPERSAMPLING (SSAA)
           • Renderiza em resolução maior
           • Reduz ao tamanho desejado
           • Alta qualidade, mas custoso
        
        2. FILTROS DE SUAVIZAÇÃO
           • Gaussian Blur: suavização uniforme
           • Bilateral: preserva bordas importantes
           • Median: remove ruído mantendo detalhes
        
        3. SUBPIXEL RENDERING
           • Usa componentes RGB individuais
           • Aumenta resolução efetiva
        
        APLICAÇÕES:
        • Computação Gráfica (jogos, renderização 3D)
        • Processamento de Imagens
        • Interfaces gráficas (fontes, ícones)
        • Impressão e visualização
        
        MÉTRICAS DE QUALIDADE:
        • PSNR (Peak Signal-to-Noise Ratio)
        • MSE (Mean Squared Error)
        • Avaliação visual subjetiva
        """
        
        plt.text(0.05, 0.95, explicacao, 
                transform=fig.transFigure,
                fontsize=11,
                verticalalignment='top',
                fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
        
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/diagrama_conceitual.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  ✓ Salvo: diagrama_conceitual.png")
    
    def executar_demonstracao_completa(self):
        """
        Executa todas as demonstrações didáticas
        """
        print("\n" + "="*60)
        print("DEMONSTRAÇÕES DIDÁTICAS DE ANTI-ALIASING")
        print("="*60 + "\n")
        
        self.demonstrar_linhas()
        self.demonstrar_circulos()
        self.demonstrar_texto()
        self.explicar_pixel_level()
        self.criar_diagrama_conceitual()
        
        print("\n" + "="*60)
        print(f"✓ Demonstrações salvas em: {self.output_dir}/")
        print("="*60 + "\n")
        
        print("ARQUIVOS GERADOS:")
        print("  • demonstracao_linhas.png - Efeito em linhas diagonais")
        print("  • demonstracao_circulos.png - Efeito em círculos")
        print("  • demonstracao_texto.png - Efeito em texto")
        print("  • explicacao_pixel_level.png - Explicação a nível de pixel")
        print("  • diagrama_conceitual.png - Diagrama teórico completo")
        print("\nEssas imagens são ideais para incluir na seção de Referencial Teórico!\n")


def main():
    """
    Função principal
    """
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║        DEMONSTRAÇÕES DIDÁTICAS DE ANTI-ALIASING            ║
    ║              Material Complementar para Relatório           ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    demo = AntiAliasingDidatico()
    demo.executar_demonstracao_completa()


if __name__ == "__main__":
    main()
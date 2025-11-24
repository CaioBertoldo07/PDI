import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os

class AntiAliasingDemo:
    """
    Classe para demonstração de técnicas de antiserrilhamento em imagens
    """
    
    def __init__(self, output_dir="resultados"):
        """
        Inicializa a classe e cria diretório de saída
        
        Args:
            output_dir: Diretório para salvar os resultados
        """
        self.output_dir = output_dir
        Path(output_dir).mkdir(exist_ok=True)
        
    def carregar_imagem(self, caminho):
        """
        Carrega uma imagem e retorna em BGR (OpenCV) e RGB (visualização)
        
        Args:
            caminho: Caminho da imagem
            
        Returns:
            Tupla (imagem_bgr, imagem_rgb)
        """
        img_bgr = cv2.imread(caminho)
        if img_bgr is None:
            raise ValueError(f"Não foi possível carregar a imagem: {caminho}")
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        return img_bgr, img_rgb
    
    def analisar_caracteristicas(self, img, nome_imagem):
        """
        Analisa e exibe características técnicas da imagem
        
        Args:
            img: Imagem a ser analisada
            nome_imagem: Nome descritivo da imagem
            
        Returns:
            Dicionário com as características
        """
        altura, largura = img.shape[:2]
        canais = img.shape[2] if len(img.shape) == 3 else 1
        
        # Análise de paleta de cores
        cores_unicas = len(np.unique(img.reshape(-1, img.shape[2]), axis=0))
        
        # Análise de gamut (faixa dinâmica)
        valor_min = img.min()
        valor_max = img.max()
        
        caracteristicas = {
            "nome": nome_imagem,
            "tamanho": f"{largura}x{altura}",
            "pixels_totais": largura * altura,
            "canais": canais,
            "tipo_cor": "RGB" if canais == 3 else "Grayscale",
            "profundidade": img.dtype,
            "cores_unicas": cores_unicas,
            "valor_minimo": int(valor_min),
            "valor_maximo": int(valor_max),
            "faixa_dinamica": int(valor_max - valor_min),
            "tamanho_memoria_mb": img.nbytes / (1024 * 1024)
        }
        
        print(f"\n{'='*60}")
        print(f"CARACTERÍSTICAS TÉCNICAS - {nome_imagem.upper()}")
        print(f"{'='*60}")
        print(f"Dimensões: {caracteristicas['tamanho']}")
        print(f"Total de pixels: {caracteristicas['pixels_totais']:,}")
        print(f"Canais de cor: {caracteristicas['canais']} ({caracteristicas['tipo_cor']})")
        print(f"Profundidade de bits: {caracteristicas['profundidade']}")
        print(f"Cores únicas: {caracteristicas['cores_unicas']:,}")
        print(f"Gamut (Valor Min-Max): {caracteristicas['valor_minimo']}-{caracteristicas['valor_maximo']}")
        print(f"Faixa Dinâmica: {caracteristicas['faixa_dinamica']}")
        print(f"Tamanho em memória: {caracteristicas['tamanho_memoria_mb']:.2f} MB")
        
        return caracteristicas
    
    def decompor_canais_rgb(self, img_rgb, nome_imagem):
        """
        Decompõe a imagem em canais R, G e B
        
        Args:
            img_rgb: Imagem em RGB
            nome_imagem: Nome da imagem para salvar
            
        Returns:
            Tupla (canal_r, canal_g, canal_b)
        """
        r, g, b = cv2.split(img_rgb)
        
        # Criar visualização dos canais
        fig, axes = plt.subplots(2, 4, figsize=(16, 8))
        fig.suptitle(f'Decomposição RGB - {nome_imagem}', fontsize=16, fontweight='bold')
        
        # Imagem original
        axes[0, 0].imshow(img_rgb)
        axes[0, 0].set_title('Imagem Original')
        axes[0, 0].axis('off')
        
        # Canal Vermelho
        img_r = np.zeros_like(img_rgb)
        img_r[:,:,0] = r
        axes[0, 1].imshow(img_r)
        axes[0, 1].set_title('Canal Vermelho (R)')
        axes[0, 1].axis('off')
        
        # Canal Verde
        img_g = np.zeros_like(img_rgb)
        img_g[:,:,1] = g
        axes[0, 2].imshow(img_g)
        axes[0, 2].set_title('Canal Verde (G)')
        axes[0, 2].axis('off')
        
        # Canal Azul
        img_b = np.zeros_like(img_rgb)
        img_b[:,:,2] = b
        axes[0, 3].imshow(img_b)
        axes[0, 3].set_title('Canal Azul (B)')
        axes[0, 3].axis('off')
        
        # Canais em escala de cinza
        axes[1, 1].imshow(r, cmap='Reds')
        axes[1, 1].set_title('Canal R (Intensidade)')
        axes[1, 1].axis('off')
        
        axes[1, 2].imshow(g, cmap='Greens')
        axes[1, 2].set_title('Canal G (Intensidade)')
        axes[1, 2].axis('off')
        
        axes[1, 3].imshow(b, cmap='Blues')
        axes[1, 3].set_title('Canal B (Intensidade)')
        axes[1, 3].axis('off')
        
        # Remover subplot não utilizado
        fig.delaxes(axes[1, 0])
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/decomposicao_rgb_{nome_imagem}.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        return r, g, b
    
    def gerar_histogramas(self, img_rgb, nome_imagem):
        """
        Gera histogramas para cada canal RGB
        
        Args:
            img_rgb: Imagem em RGB
            nome_imagem: Nome da imagem para salvar
        """
        r, g, b = cv2.split(img_rgb)
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f'Histogramas RGB - {nome_imagem}', fontsize=16, fontweight='bold')
        
        # Histograma combinado
        axes[0, 0].hist(r.ravel(), bins=256, color='red', alpha=0.5, label='Red')
        axes[0, 0].hist(g.ravel(), bins=256, color='green', alpha=0.5, label='Green')
        axes[0, 0].hist(b.ravel(), bins=256, color='blue', alpha=0.5, label='Blue')
        axes[0, 0].set_title('Histograma Combinado')
        axes[0, 0].set_xlabel('Intensidade de Pixel')
        axes[0, 0].set_ylabel('Frequência')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Histograma Canal Vermelho
        axes[0, 1].hist(r.ravel(), bins=256, color='red', alpha=0.7)
        axes[0, 1].set_title('Histograma Canal Vermelho')
        axes[0, 1].set_xlabel('Intensidade')
        axes[0, 1].set_ylabel('Frequência')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Histograma Canal Verde
        axes[1, 0].hist(g.ravel(), bins=256, color='green', alpha=0.7)
        axes[1, 0].set_title('Histograma Canal Verde')
        axes[1, 0].set_xlabel('Intensidade')
        axes[1, 0].set_ylabel('Frequência')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Histograma Canal Azul
        axes[1, 1].hist(b.ravel(), bins=256, color='blue', alpha=0.7)
        axes[1, 1].set_title('Histograma Canal Azul')
        axes[1, 1].set_xlabel('Intensidade')
        axes[1, 1].set_ylabel('Frequência')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/histogramas_{nome_imagem}.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Histogramas salvos: histogramas_{nome_imagem}.png")
    
    def aplicar_gaussian_blur(self, img, kernel_size=5):
        """
        Aplica filtro Gaussiano para suavização (técnica básica de anti-aliasing)
        
        Args:
            img: Imagem de entrada
            kernel_size: Tamanho do kernel (deve ser ímpar)
            
        Returns:
            Imagem suavizada
        """
        return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
    
    def aplicar_bilateral_filter(self, img, d=9, sigma_color=75, sigma_space=75):
        """
        Aplica filtro bilateral para suavização preservando bordas
        
        Args:
            img: Imagem de entrada
            d: Diâmetro do pixel vizinho
            sigma_color: Filtro sigma no espaço de cor
            sigma_space: Filtro sigma no espaço de coordenadas
            
        Returns:
            Imagem com filtro bilateral
        """
        return cv2.bilateralFilter(img, d, sigma_color, sigma_space)
    
    def aplicar_median_blur(self, img, kernel_size=5):
        """
        Aplica filtro de mediana para redução de ruído
        
        Args:
            img: Imagem de entrada
            kernel_size: Tamanho do kernel
            
        Returns:
            Imagem com filtro de mediana
        """
        return cv2.medianBlur(img, kernel_size)
    
    def aplicar_supersampling(self, img, scale_factor=2):
        """
        Aplica supersampling (SSAA) - técnica clássica de anti-aliasing
        Redimensiona para cima e depois volta ao tamanho original
        
        Args:
            img: Imagem de entrada
            scale_factor: Fator de escala para supersampling
            
        Returns:
            Imagem com supersampling aplicado
        """
        altura, largura = img.shape[:2]
        
        # Aumenta a resolução
        img_upscaled = cv2.resize(img, (largura * scale_factor, altura * scale_factor), 
                                  interpolation=cv2.INTER_CUBIC)
        
        # Reduz de volta ao tamanho original com interpolação de alta qualidade
        img_downscaled = cv2.resize(img_upscaled, (largura, altura), 
                                    interpolation=cv2.INTER_AREA)
        
        return img_downscaled
    
    def aplicar_morphological_antialiasing(self, img):
        """
        Aplica operações morfológicas para suavizar bordas (anti-aliasing morfológico)
        
        Args:
            img: Imagem de entrada
            
        Returns:
            Imagem com anti-aliasing morfológico
        """
        # Converter para escala de cinza temporariamente para operações morfológicas
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        
        # Aplicar closing seguido de opening para suavizar
        kernel = np.ones((3,3), np.uint8)
        closed = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
        opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel)
        
        # Converter de volta para RGB
        result = cv2.cvtColor(opened, cv2.COLOR_GRAY2RGB)
        
        return result
    
    def comparar_tecnicas_antialiasing(self, img_rgb, nome_imagem):
        """
        Compara diferentes técnicas de anti-aliasing
        
        Args:
            img_rgb: Imagem RGB de entrada
            nome_imagem: Nome da imagem para salvar resultados
        """
        # Converter para BGR para OpenCV
        img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
        
        # Aplicar diferentes técnicas
        img_gaussian = self.aplicar_gaussian_blur(img_bgr)
        img_bilateral = self.aplicar_bilateral_filter(img_bgr)
        img_median = self.aplicar_median_blur(img_bgr)
        img_ssaa = self.aplicar_supersampling(img_bgr, scale_factor=2)
        
        # Converter de volta para RGB para visualização
        img_gaussian_rgb = cv2.cvtColor(img_gaussian, cv2.COLOR_BGR2RGB)
        img_bilateral_rgb = cv2.cvtColor(img_bilateral, cv2.COLOR_BGR2RGB)
        img_median_rgb = cv2.cvtColor(img_median, cv2.COLOR_BGR2RGB)
        img_ssaa_rgb = cv2.cvtColor(img_ssaa, cv2.COLOR_BGR2RGB)
        
        # Criar visualização comparativa
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle(f'Comparação de Técnicas de Antiserrilhamento - {nome_imagem}', 
                     fontsize=16, fontweight='bold')
        
        # Imagem original
        axes[0, 0].imshow(img_rgb)
        axes[0, 0].set_title('Original')
        axes[0, 0].axis('off')
        
        # Gaussian Blur
        axes[0, 1].imshow(img_gaussian_rgb)
        axes[0, 1].set_title('Filtro Gaussiano\n(Suavização básica)')
        axes[0, 1].axis('off')
        
        # Bilateral Filter
        axes[0, 2].imshow(img_bilateral_rgb)
        axes[0, 2].set_title('Filtro Bilateral\n(Preserva bordas)')
        axes[0, 2].axis('off')
        
        # Median Blur
        axes[1, 0].imshow(img_median_rgb)
        axes[1, 0].set_title('Filtro de Mediana\n(Reduz ruído)')
        axes[1, 0].axis('off')
        
        # Supersampling
        axes[1, 1].imshow(img_ssaa_rgb)
        axes[1, 1].set_title('Supersampling (SSAA)\n(Anti-aliasing clássico)')
        axes[1, 1].axis('off')
        
        # Diferença entre original e SSAA
        diff = cv2.absdiff(img_rgb, img_ssaa_rgb)
        axes[1, 2].imshow(diff)
        axes[1, 2].set_title('Diferença (Original vs SSAA)\n(Ampliada para visualização)')
        axes[1, 2].axis('off')
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/comparacao_antialiasing_{nome_imagem}.png", 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Comparação salva: comparacao_antialiasing_{nome_imagem}.png")
        
        # Salvar imagens individuais processadas
        cv2.imwrite(f"{self.output_dir}/{nome_imagem}_gaussian.png", img_gaussian)
        cv2.imwrite(f"{self.output_dir}/{nome_imagem}_bilateral.png", img_bilateral)
        cv2.imwrite(f"{self.output_dir}/{nome_imagem}_median.png", img_median)
        cv2.imwrite(f"{self.output_dir}/{nome_imagem}_ssaa.png", img_ssaa)
        
        return {
            'gaussian': img_gaussian_rgb,
            'bilateral': img_bilateral_rgb,
            'median': img_median_rgb,
            'ssaa': img_ssaa_rgb
        }
    
    def analisar_bordas(self, img_rgb, nome_imagem):
        """
        Analisa detecção de bordas para demonstrar efeito do anti-aliasing
        
        Args:
            img_rgb: Imagem RGB
            nome_imagem: Nome da imagem
        """
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
        
        # Aplicar Canny para detectar bordas
        bordas_original = cv2.Canny(img_gray, 50, 150)
        
        # Aplicar anti-aliasing e depois detectar bordas
        img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
        img_suavizada = self.aplicar_gaussian_blur(img_bgr)
        img_suavizada_gray = cv2.cvtColor(img_suavizada, cv2.COLOR_BGR2GRAY)
        bordas_suavizadas = cv2.Canny(img_suavizada_gray, 50, 150)
        
        # Visualização
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f'Análise de Bordas - {nome_imagem}', fontsize=16, fontweight='bold')
        
        axes[0, 0].imshow(img_rgb)
        axes[0, 0].set_title('Imagem Original')
        axes[0, 0].axis('off')
        
        axes[0, 1].imshow(bordas_original, cmap='gray')
        axes[0, 1].set_title('Bordas (Original)')
        axes[0, 1].axis('off')
        
        axes[1, 0].imshow(cv2.cvtColor(img_suavizada, cv2.COLOR_BGR2RGB))
        axes[1, 0].set_title('Imagem com Anti-aliasing')
        axes[1, 0].axis('off')
        
        axes[1, 1].imshow(bordas_suavizadas, cmap='gray')
        axes[1, 1].set_title('Bordas (Anti-aliasing)\n(Bordas mais suaves)')
        axes[1, 1].axis('off')
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/analise_bordas_{nome_imagem}.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Análise de bordas salva: analise_bordas_{nome_imagem}.png")
    
    def demonstrar_efeito_escala(self, img_rgb, nome_imagem):
        """
        Demonstra o efeito do anti-aliasing em diferentes escalas
        
        Args:
            img_rgb: Imagem RGB
            nome_imagem: Nome da imagem
        """
        img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
        
        # Redimensionar sem e com anti-aliasing
        nova_largura = img_rgb.shape[1] // 2
        nova_altura = img_rgb.shape[0] // 2
        
        # Sem anti-aliasing (INTER_NEAREST - preserva pixels originais)
        img_sem_aa = cv2.resize(img_bgr, (nova_largura, nova_altura), 
                                interpolation=cv2.INTER_NEAREST)
        
        # Com anti-aliasing (INTER_AREA - melhor para redução)
        img_com_aa = cv2.resize(img_bgr, (nova_largura, nova_altura), 
                                interpolation=cv2.INTER_AREA)
        
        # Voltar ao tamanho original para comparação
        img_sem_aa_up = cv2.resize(img_sem_aa, (img_rgb.shape[1], img_rgb.shape[0]), 
                                   interpolation=cv2.INTER_NEAREST)
        img_com_aa_up = cv2.resize(img_com_aa, (img_rgb.shape[1], img_rgb.shape[0]), 
                                   interpolation=cv2.INTER_CUBIC)
        
        # Converter para RGB
        img_sem_aa_rgb = cv2.cvtColor(img_sem_aa_up, cv2.COLOR_BGR2RGB)
        img_com_aa_rgb = cv2.cvtColor(img_com_aa_up, cv2.COLOR_BGR2RGB)
        
        # Visualização
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        fig.suptitle(f'Efeito de Anti-aliasing em Redimensionamento - {nome_imagem}', 
                     fontsize=16, fontweight='bold')
        
        axes[0].imshow(img_rgb)
        axes[0].set_title('Original')
        axes[0].axis('off')
        
        axes[1].imshow(img_sem_aa_rgb)
        axes[1].set_title('Sem Anti-aliasing\n(Serrilhamento visível)')
        axes[1].axis('off')
        
        axes[2].imshow(img_com_aa_rgb)
        axes[2].set_title('Com Anti-aliasing\n(Bordas suavizadas)')
        axes[2].axis('off')
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/efeito_escala_{nome_imagem}.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Demonstração de escala salva: efeito_escala_{nome_imagem}.png")
    
    def calcular_metricas_qualidade(self, img_original, img_processada):
        """
        Calcula métricas de qualidade entre imagem original e processada
        
        Args:
            img_original: Imagem original
            img_processada: Imagem após anti-aliasing
            
        Returns:
            Dicionário com métricas
        """
        # MSE (Mean Squared Error)
        mse = np.mean((img_original.astype(float) - img_processada.astype(float)) ** 2)
        
        # PSNR (Peak Signal-to-Noise Ratio)
        if mse == 0:
            psnr = float('inf')
        else:
            max_pixel = 255.0
            psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
        
        # Diferença absoluta média
        mae = np.mean(np.abs(img_original.astype(float) - img_processada.astype(float)))
        
        return {
            'MSE': mse,
            'PSNR': psnr,
            'MAE': mae
        }
    
    def processar_imagem_completo(self, caminho_imagem, nome_imagem):
        """
        Executa o pipeline completo de análise e processamento
        
        Args:
            caminho_imagem: Caminho da imagem
            nome_imagem: Nome descritivo da imagem
        """
        print(f"\n{'#'*60}")
        print(f"PROCESSANDO: {nome_imagem.upper()}")
        print(f"{'#'*60}")
        
        # 1. Carregar imagem
        img_bgr, img_rgb = self.carregar_imagem(caminho_imagem)
        print(f"✓ Imagem carregada com sucesso")
        
        # 2. Analisar características
        caracteristicas = self.analisar_caracteristicas(img_rgb, nome_imagem)
        
        # 3. Decompor canais RGB
        print(f"\n→ Decompondo canais RGB...")
        r, g, b = self.decompor_canais_rgb(img_rgb, nome_imagem)
        print(f"✓ Decomposição RGB salva: decomposicao_rgb_{nome_imagem}.png")
        
        # 4. Gerar histogramas
        print(f"\n→ Gerando histogramas...")
        self.gerar_histogramas(img_rgb, nome_imagem)
        
        # 5. Comparar técnicas de anti-aliasing
        print(f"\n→ Aplicando técnicas de antiserrilhamento...")
        resultados = self.comparar_tecnicas_antialiasing(img_rgb, nome_imagem)
        
        # 6. Analisar bordas
        print(f"\n→ Analisando detecção de bordas...")
        self.analisar_bordas(img_rgb, nome_imagem)
        
        # 7. Demonstrar efeito em escala
        print(f"\n→ Demonstrando efeito em diferentes escalas...")
        self.demonstrar_efeito_escala(img_rgb, nome_imagem)
        
        # 8. Calcular métricas de qualidade
        print(f"\n→ Calculando métricas de qualidade...")
        img_bgr_ssaa = cv2.cvtColor(resultados['ssaa'], cv2.COLOR_RGB2BGR)
        metricas = self.calcular_metricas_qualidade(img_bgr, img_bgr_ssaa)
        
        print(f"\nMÉTRICAS DE QUALIDADE (Original vs SSAA):")
        print(f"  MSE (Mean Squared Error): {metricas['MSE']:.2f}")
        print(f"  PSNR (Peak Signal-to-Noise Ratio): {metricas['PSNR']:.2f} dB")
        print(f"  MAE (Mean Absolute Error): {metricas['MAE']:.2f}")
        
        print(f"\n{'='*60}")
        print(f"✓ Processamento de '{nome_imagem}' concluído com sucesso!")
        print(f"{'='*60}\n")
        
        return caracteristicas, metricas


def main():
    """
    Função principal para executar a demonstração
    """
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║   DEMONSTRAÇÃO DE ANTISERRILHAMENTO (ANTI-ALIASING)        ║
    ║   Processamento Digital de Imagens                          ║
    ║   Aluno: Caio Bertoldo Bezerra                             ║
    ║   UEA - Universidade do Estado do Amazonas                 ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Inicializar demonstração
    demo = AntiAliasingDemo(output_dir="resultados_antialiasing")
    
    # Lista de imagens para processar
    # IMPORTANTE: Substitua pelos caminhos corretos das suas imagens
    imagens = [
        ("img/PESSOA.jpg", "pessoa"),
        ("img/OBJETO.jpg", "objeto"),
        ("img/DOCUMENTO.jpg", "documento")
    ]
    
    # Verificar se as imagens existem
    imagens_encontradas = []
    for caminho, nome in imagens:
        if os.path.exists(caminho):
            imagens_encontradas.append((caminho, nome))
        else:
            print(f"⚠ AVISO: Imagem não encontrada: {caminho}")
            print(f"   Por favor, coloque a imagem na pasta correta ou atualize o caminho.\n")
    
    if not imagens_encontradas:
        print("\n" + "="*60)
        print("INSTRUÇÕES:")
        print("="*60)
        print("1. Crie uma pasta chamada 'imG' no mesmo diretório deste script")
        print("2. Adicione suas três fotos:")
        print("   - pessoa.jpg (foto de uma pessoa)")
        print("   - objeto.jpg (foto de um objeto)")
        print("   - documento.jpg (foto de um documento)")
        print("3. Execute o script novamente")
        print("="*60)
        print("\nOu atualize os caminhos das imagens no código (linha 464-468)\n")
        return
    
    # Processar cada imagem encontrada
    resultados_gerais = {}
    for caminho, nome in imagens_encontradas:
        try:
            caracteristicas, metricas = demo.processar_imagem_completo(caminho, nome)
            resultados_gerais[nome] = {
                'caracteristicas': caracteristicas,
                'metricas': metricas
            }
        except Exception as e:
            print(f"\n❌ ERRO ao processar {nome}: {str(e)}\n")
            continue
    
    # Resumo final
    if resultados_gerais:
        print("\n" + "="*60)
        print("RESUMO FINAL - TODAS AS IMAGENS")
        print("="*60)
        
        for nome, dados in resultados_gerais.items():
            print(f"\n{nome.upper()}:")
            print(f"  Dimensões: {dados['caracteristicas']['tamanho']}")
            print(f"  Total de pixels: {dados['caracteristicas']['pixels_totais']:,}")
            print(f"  PSNR (Original vs SSAA): {dados['metricas']['PSNR']:.2f} dB")
        
        print(f"\n{'='*60}")
        print(f"✓ Todos os resultados foram salvos em: resultados_antialiasing/")
        print(f"{'='*60}\n")
        
        print("ARQUIVOS GERADOS PARA CADA IMAGEM:")
        print("  - decomposicao_rgb_[nome].png (Canais R, G, B separados)")
        print("  - histogramas_[nome].png (Histogramas de cada canal)")
        print("  - comparacao_antialiasing_[nome].png (Comparação de técnicas)")
        print("  - analise_bordas_[nome].png (Detecção de bordas)")
        print("  - efeito_escala_[nome].png (Efeito em redimensionamento)")
        print("  - [nome]_gaussian.png, _bilateral.png, _median.png, _ssaa.png")
        print("\n✓ Demonstração concluída com sucesso!")
    else:
        print("\n❌ Nenhuma imagem foi processada com sucesso.")
        print("   Verifique os caminhos das imagens e tente novamente.\n")


if __name__ == "__main__":
    main()
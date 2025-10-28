#!/usr/bin/env python3
"""
Script para gerar gráficos de análise de desempenho GPU/CPU
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def load_data(csv_path):
    """Carrega dados do CSV"""
    df = pd.read_csv(csv_path)
    return df

def plot_fps_vs_triangles(df, output_dir):
    """Gráfico: FPS vs Número de Triângulos (sem iluminação/textura)"""
    df_base = df[(df['Iluminacao'] == 'Nao') & (df['Textura'] == 'Nao')]
    
    plt.figure(figsize=(12, 6))
    plt.plot(df_base['Triangulos'], df_base['FPS'], 'o-', linewidth=2, markersize=8)
    plt.xlabel('Número de Triângulos', fontsize=12)
    plt.ylabel('FPS (Frames por Segundo)', fontsize=12)
    plt.title('Desempenho: FPS vs Número de Triângulos\n(Sem Iluminação e Textura)', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/grafico_01_fps_vs_triangulos_base.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfico 1 gerado: FPS vs Triângulos (Base)")

def plot_lighting_impact(df, output_dir):
    """Gráfico: Impacto da Iluminação no FPS"""
    df_no_tex = df[df['Textura'] == 'Nao']
    
    plt.figure(figsize=(14, 7))
    
    for light_type in df_no_tex['TipoLuz'].unique():
        df_light = df_no_tex[df_no_tex['TipoLuz'] == light_type]
        plt.plot(df_light['Triangulos'], df_light['FPS'], 'o-', label=light_type, linewidth=2, markersize=8)
    
    plt.xlabel('Número de Triângulos', fontsize=12)
    plt.ylabel('FPS (Frames por Segundo)', fontsize=12)
    plt.title('Impacto dos Tipos de Iluminação no Desempenho\n(Sem Textura)', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/grafico_02_impacto_iluminacao.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfico 2 gerado: Impacto da Iluminação")

def plot_texture_impact(df, output_dir):
    """Gráfico: Impacto da Textura no FPS"""
    plt.figure(figsize=(14, 7))
    
    # Sem textura, sem luz
    df_no_tex = df[(df['Textura'] == 'Nao') & (df['Iluminacao'] == 'Nao')]
    plt.plot(df_no_tex['Triangulos'], df_no_tex['FPS'], 'o-', label='Sem Textura/Luz', linewidth=2, markersize=8)
    
    # Com textura, sem luz
    df_tex = df[(df['Textura'] == 'Sim') & (df['Iluminacao'] == 'Nao')]
    if not df_tex.empty:
        plt.plot(df_tex['Triangulos'], df_tex['FPS'], 's-', label='Com Textura, Sem Luz', linewidth=2, markersize=8)
    
    plt.xlabel('Número de Triângulos', fontsize=12)
    plt.ylabel('FPS (Frames por Segundo)', fontsize=12)
    plt.title('Impacto da Textura no Desempenho', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/grafico_03_impacto_textura.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfico 3 gerado: Impacto da Textura")

def plot_combined_effects(df, output_dir):
    """Gráfico: Comparação de Todos os Cenários"""
    plt.figure(figsize=(16, 8))
    
    scenarios = [
        ('Nao', 'Nao', 'Sem luz', 'Base (Sem Luz/Textura)'),
        ('Sim', 'Nao', 'Omnidirecional', 'Luz Omnidirecional'),
        ('Sim', 'Nao', 'Spot', 'Luz Spot'),
        ('Nao', 'Sim', 'Sem luz', 'Com Textura'),
        ('Sim', 'Sim', 'Omnidirecional', 'Textura + Luz Omni'),
        ('Sim', 'Sim', 'Spot', 'Textura + Luz Spot')
    ]
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(scenarios)))
    
    for i, (luz, tex, tipo_luz, label) in enumerate(scenarios):
        df_scenario = df[(df['Iluminacao'] == luz) & (df['Textura'] == tex) & (df['TipoLuz'] == tipo_luz)]
        if not df_scenario.empty:
            plt.plot(df_scenario['Triangulos'], df_scenario['FPS'], 'o-', 
                    label=label, linewidth=2, markersize=6, color=colors[i])
    
    plt.xlabel('Número de Triângulos', fontsize=12)
    plt.ylabel('FPS (Frames por Segundo)', fontsize=12)
    plt.title('Comparação Completa: Impacto de Iluminação e Textura no Desempenho', 
             fontsize=14, fontweight='bold')
    plt.legend(fontsize=10, loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/grafico_04_comparacao_completa.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfico 4 gerado: Comparação Completa")

def plot_performance_degradation(df, output_dir):
    """Gráfico: Degradação de Desempenho Relativa"""
    df_base = df[(df['Iluminacao'] == 'Nao') & (df['Textura'] == 'Nao')]
    
    if df_base.empty:
        print("! Aviso: Dados base não encontrados para análise de degradação")
        return
    
    plt.figure(figsize=(14, 7))
    
    for triangle_count in df_base['Triangulos'].unique():
        base_fps = df_base[df_base['Triangulos'] == triangle_count]['FPS'].values[0]
        
        degradations = []
        labels = []
        
        for luz, tex in [('Sim', 'Nao'), ('Nao', 'Sim'), ('Sim', 'Sim')]:
            df_scenario = df[(df['Iluminacao'] == luz) & (df['Textura'] == tex) & 
                           (df['Triangulos'] == triangle_count)]
            if not df_scenario.empty:
                fps = df_scenario['FPS'].values[0]
                degradation = ((base_fps - fps) / base_fps) * 100
                degradations.append(degradation)
                
                if luz == 'Sim' and tex == 'Nao':
                    labels.append('Iluminação')
                elif luz == 'Nao' and tex == 'Sim':
                    labels.append('Textura')
                else:
                    labels.append('Ilum. + Tex.')
        
        x = np.arange(len(labels))
        plt.bar(x + (triangle_count / 10000), degradations, width=0.15, 
               label=f'{triangle_count} triângulos')
    
    plt.xlabel('Tipo de Efeito', fontsize=12)
    plt.ylabel('Degradação de Desempenho (%)', fontsize=12)
    plt.title('Degradação de Desempenho por Tipo de Efeito', fontsize=14, fontweight='bold')
    plt.xticks(x, labels)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/grafico_05_degradacao_desempenho.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfico 5 gerado: Degradação de Desempenho")

def plot_fps_heatmap(df, output_dir):
    """Gráfico: Mapa de Calor do FPS"""
    # Criar matriz de FPS por quantidade de triângulos e configuração
    configs = []
    for _, row in df.iterrows():
        config = f"{row['TipoLuz']}"
        if row['Textura'] == 'Sim':
            config += " + Tex"
        configs.append(config)
    
    df['Configuracao'] = configs
    
    pivot_table = df.pivot_table(values='FPS', index='Configuracao', columns='Triangulos', aggfunc='mean')
    
    plt.figure(figsize=(14, 8))
    im = plt.imshow(pivot_table, aspect='auto', cmap='RdYlGn', interpolation='nearest')
    
    plt.colorbar(im, label='FPS')
    plt.xlabel('Número de Triângulos', fontsize=12)
    plt.ylabel('Configuração', fontsize=12)
    plt.title('Mapa de Calor: FPS por Configuração e Quantidade de Triângulos', 
             fontsize=14, fontweight='bold')
    
    plt.xticks(range(len(pivot_table.columns)), pivot_table.columns, rotation=45)
    plt.yticks(range(len(pivot_table.index)), pivot_table.index)
    
    # Adicionar valores nas células
    for i in range(len(pivot_table.index)):
        for j in range(len(pivot_table.columns)):
            value = pivot_table.iloc[i, j]
            if not np.isnan(value):
                plt.text(j, i, f'{value:.0f}', ha='center', va='center', 
                        color='black', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/grafico_06_mapa_calor_fps.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfico 6 gerado: Mapa de Calor FPS")

def generate_summary_stats(df, output_path):
    """Gera estatísticas resumidas"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("RESUMO ESTATÍSTICO - TESTE DE DESEMPENHO GPU/CPU\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Total de testes realizados: {len(df)}\n")
        f.write(f"FPS Médio Geral: {df['FPS'].mean():.2f}\n")
        f.write(f"FPS Máximo: {df['FPS'].max():.2f}\n")
        f.write(f"FPS Mínimo: {df['FPS'].min():.2f}\n\n")
        
        f.write("-" * 80 + "\n")
        f.write("DESEMPENHO POR CONFIGURAÇÃO:\n")
        f.write("-" * 80 + "\n\n")
        
        for luz in df['Iluminacao'].unique():
            for tex in df['Textura'].unique():
                df_config = df[(df['Iluminacao'] == luz) & (df['Textura'] == tex)]
                if not df_config.empty:
                    f.write(f"Iluminação: {luz} | Textura: {tex}\n")
                    f.write(f"  FPS Médio: {df_config['FPS'].mean():.2f}\n")
                    f.write(f"  FPS Máximo: {df_config['FPS'].max():.2f}\n")
                    f.write(f"  FPS Mínimo: {df_config['FPS'].min():.2f}\n\n")
        
        f.write("-" * 80 + "\n")
        f.write("ANÁLISE POR QUANTIDADE DE TRIÂNGULOS:\n")
        f.write("-" * 80 + "\n\n")
        
        for tri_count in sorted(df['Triangulos'].unique()):
            df_tri = df[df['Triangulos'] == tri_count]
            f.write(f"{tri_count} Triângulos:\n")
            f.write(f"  FPS Médio: {df_tri['FPS'].mean():.2f}\n")
            f.write(f"  Variação: {df_tri['FPS'].std():.2f}\n\n")
    
    print(f"✓ Estatísticas salvas em: {output_path}")

def main():
    # Configurações
    csv_path = 'performance_results.csv'
    output_dir = 'outputs'
    
    # Verificar se o arquivo existe
    if not Path(csv_path).exists():
        print(f"Erro: Arquivo {csv_path} não encontrado!")
        print("Execute o programa OpenGL primeiro para gerar os dados.")
        return
    
    # Carregar dados
    print("\nCarregando dados de desempenho...")
    df = load_data(csv_path)
    print(f"✓ Dados carregados: {len(df)} testes\n")
    
    # Gerar gráficos
    print("Gerando gráficos de análise...\n")
    
    plot_fps_vs_triangles(df, output_dir)
    plot_lighting_impact(df, output_dir)
    plot_texture_impact(df, output_dir)
    plot_combined_effects(df, output_dir)
    plot_performance_degradation(df, output_dir)
    plot_fps_heatmap(df, output_dir)
    
    # Gerar estatísticas
    print("\nGerando estatísticas resumidas...")
    stats_path = f'{output_dir}/estatisticas_resumo.txt'
    generate_summary_stats(df, stats_path)
    
    print("\n" + "=" * 80)
    print("✓ ANÁLISE CONCLUÍDA COM SUCESSO!")
    print("=" * 80)
    print(f"\nArquivos gerados em: {output_dir}/")
    print("  - 6 gráficos PNG")
    print("  - 1 arquivo de estatísticas TXT")
    print("\n")

if __name__ == '__main__':
    main()

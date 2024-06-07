import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def draw_plots(json_url, top_n=10):
    response = requests.get(json_url)
    response.raise_for_status()
    
    data = response.json()
    
    df = pd.DataFrame(data)
    
    if not os.path.exists('plots'):
        os.makedirs('plots')
    
    plot_paths = []
    
    columns_to_plot = ['mean', 'max', 'min', 'floor_mean', 'floor_max', 'floor_min', 'ceiling_mean', 'ceiling_max', 'ceiling_min']
    
    sns.set(style="whitegrid")
    
    top_df = df.nlargest(top_n, 'mean')
    
    for col in columns_to_plot:
        plt.figure(figsize=(12, 8))
        
        ax = sns.barplot(x='name', y=col, data=top_df, palette='viridis')
        
        ax.set_xlabel('Name', fontsize=14)
        ax.set_ylabel(col.replace('_', ' ').title(), fontsize=14)
        ax.set_title(f'Top {top_n} Names by {col.replace("_", " ").title()}', fontsize=16)
        
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
        
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.2f'), 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha = 'center', va = 'center', 
                        xytext = (0, 9), 
                        textcoords = 'offset points')
        
        plt.tight_layout()
        
        plot_path = f'plots/{col}_top_{top_n}_by_name.png'
        plt.savefig(plot_path, dpi=300)
        plt.close()
        
        plot_paths.append(plot_path)
    
    for col in columns_to_plot:
        fig = px.bar(df, x='name', y=col, title=f'{col.replace("_", " ").title()} by Name', labels={'name': 'Name', col: col.replace('_', ' ').title()})
        fig.update_layout(xaxis_tickangle=-45)
        plot_path = f'plots/interactive_{col}_by_name.html'
        fig.write_html(plot_path)
        plot_paths.append(plot_path)
    
    return plot_paths

json_url = "https://ai-process-sandy.s3.eu-west-1.amazonaws.com/purge/deviation.json"
plot_paths = draw_plots(json_url)

for path in plot_paths:
    print(path)
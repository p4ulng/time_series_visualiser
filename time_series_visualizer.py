import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')
df['date']=pd.to_datetime(df['date'])
df=df.set_index('date').rename(columns={"value":'views'})
# print(df)
# Clean data
df = df[(df['views']<=df['views'].quantile(0.975))&
        (df['views']>=df['views'].quantile(0.025))
        ]
df_bar=df
df_bar=df_bar.assign(Year=df_bar.index.year,Month=df_bar.index.month)
# print(df_bar)
# print(type(df.index))

def draw_line_plot():
    # Draw line plot
    fig,ax=plt.subplots()

    ax.plot(df.index,df['views'],label='line')

    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")    

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar=df.copy()
    df_bar=(df_bar.assign(Year=df_bar.index.year,Month=df_bar.index.month)
        .groupby(['Year','Month'])
        .mean()
        .round(1)
        .unstack()
    )
    #Draw the graph
    fig,ax=plt.subplots()

    df_bar.plot(ax=ax,kind='bar')

    ax.set_xlabel('Years')
    ax.set_ylabel("Average Page Views")
    months = ['January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December']
    ax.legend(title='Months',labels=months)

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['date'] = pd.to_datetime(df_box['date'])
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    
    df_box['monthnum']=df_box['date'].dt.month
    df_box=df_box.sort_values('monthnum')
    # Draw box plots (using Seaborn)
    fig,ax=plt.subplots(1,2,figsize=(15,5))

    sns.boxplot(data=df_box,x='year',y='views',ax=ax[0])
    ax[0].set(title='Year-wise Box Plot (Trend)',xlabel='Year',ylabel='Page Views')
    sns.boxplot(data=df_box,x='month',y='views',ax=ax[1])
    ax[1].set(title='Month-wise Box Plot (Seasonality)',xlabel='Month',ylabel='Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

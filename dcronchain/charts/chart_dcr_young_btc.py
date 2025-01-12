#Compare the behaviour of Decred and Bitcoin
import pandas as pd
import numpy as np
import os
os.getcwd()
os.chdir('D:\code_development\checkonchain\checkonchain')


from checkonchain.dcronchain.charts.__init__ import *
from checkonchain.btconchain.btc_add_metrics import *
from checkonchain.dcronchain.dcr_add_metrics import *
from checkonchain.ltconchain.ltc_add_metrics import *
"""**************************************************************************
                            Part 0 - Code Setup
***************************************************************************"""

"""############## PULL DATSETS ##############"""

"""##### Bitcoin #####"""
print('CALCULATING BITCOIN DATAFRAMES')
BTC_sply = btc_add_metrics().btc_sply_curtailed(2400000) #Theoretical Supply curve
BTC_real = btc_add_metrics().btc_real() #Actual Performance
BTC_half = btc_supply_schedule(0).btc_halvings_stepped() # Calculate Max-Min step to plot up Bitcoin halvings
# Blockchain.com hashrate w/ coinmetrics block (UPDATE 5 Oct 2019)
# Note need to add coinmetrics block manually
BTC_hash = btc_add_metrics().btc_hash() #Actual Performance
#BTC_hash = pd.read_csv(r"btconchain\data\btc_blockchaincom_hashrate.csv")
#BTC_hash
#BTC_hash = pd.concat([BTC_hash.set_index('blk',drop=False),BTC_real[['blk','date']].set_index('blk',drop=True)],axis=1,join='inner')
#BTC_hash = BTC_hash.drop(BTC_hash.index[0])
#BTC_hash.reset_index(drop=True)


"""##### Decred #####"""
print('CALCULATING DECRED DATAFRAMES')
DCR_sply = dcr_add_metrics().dcr_sply(2400000*2-33600*2) #Theoretical Supply curve
DCR_real = dcr_add_metrics().dcr_real() #Actual Market Performance
DCR_natv = dcr_add_metrics().dcr_natv() #Actual On-chain Performance
# Calculate the btc_block where supply = 1.68million BTC
dcr_btc_blk_start = int(BTC_sply[BTC_sply['Sply_ideal']==1680000]['blk'])
# Create btc_blk height  (1BTC block == 2 DCR blocks)
DCR_sply['btc_blk'] = dcr_btc_blk_start + 0.5*DCR_sply['blk']
DCR_real['btc_blk'] = dcr_btc_blk_start + 0.5*DCR_real['blk']


"""##### Litecoin #####"""
print('CALCULATING LITECOIN DATAFRAMES')
#LTC_sply = ltc_add_metrics().ltc_sply(1200000*4) #Theoretical Supply curve
#LTC_real = ltc_add_metrics().ltc_real() #Actual Performance
#Calculate BTC block height assuming LTC launched on same date (0.25x)
#LTC_sply['btc_blk'] = 0.25*LTC_sply['blk']
#LTC_real['btc_blk'] = 0.25*LTC_real['blk']


"""**************************************************************************
                            Part 1 - Monetary Policy
***************************************************************************"""

class dcrbtc_monetary_policy():
    
    def __init__(self):
        pass

    def chart_dcrbtc_sply_area(self):
        """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        CREATE PLOT 01
                SUPPLY CURVES - STACKED AREA CHARTS
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
        x_data = [
            BTC_sply['blk'],
            DCR_sply['btc_blk'],
            DCR_sply['btc_blk'],
            DCR_sply['btc_blk'],
            DCR_sply['btc_blk']
        ]
        y_data = [
            BTC_sply['Sply_ideal'],
            DCR_sply['Sply_ideal'],
            DCR_sply['PoWSply_ideal'],
            DCR_sply['PoSSply_ideal'],
            DCR_sply['FundSply_ideal']
        ]
        name_data = [
            'BTC Supply',
            'DCR Total Supply',
            'DCR PoW Supply',
            'DCR PoS Supply',
            'DCR Treasury Supply',
        ]
        color_data = [
            'rgb(255, 153, 0)',
            'rgb(46, 214, 161)',
            'rgb(41, 112, 255)',
            'rgb(46, 214, 161)',
            'rgb(237, 109, 71)'
        ]
        fill_data = [
            'tozeroy',
            'tonexty',
            'tonexty',
            'tonexty',
            'tozeroy'
        ]
        opacity_data = [
            0.5,1,0.5,0.5,0.5
        ]
        fig = go.Figure()
        for i in range(0,5):
            fig.add_trace(go.Scatter(
                x=x_data[i], 
                y=y_data[i],
                name=name_data[i], 
                fill=fill_data[i],
                #fillcolor=color_data[i],
                #line_color= color_data[i],
                line=dict(
                    color=color_data[i],
                    width=2
                    #opacity=opacity_data[i]
                )))
        fig.update_layout(template="plotly_dark",title="Bitcoin and Decred Theoretical Supply Curves")
        
        return fig


    def chart_dcrbtc_sply_s2f(self):
        """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        CREATE PLOT
                SUPPLY CURVES AND STOCK TO FLOW RATIOS
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
        # BTC Theoretical Supply curve
        # DCR Theoretical Supply curve
        # DCR Theoretical Supply curve (Offset to BTC 1.68million)
        # BTC Theoretical S2F
        # DCR Theoretical S2F
        # DCR Theoretical S2F (Offset to BTC 1.68million)
        # BTC Halvings
        x_data = [
            BTC_sply['blk'],
            BTC_sply['blk'],
            BTC_real['blk'],
            DCR_sply['btc_blk']+372384,
            DCR_sply['btc_blk']+372384,
            DCR_real['btc_blk']+372384,
            DCR_sply['btc_blk'],
            DCR_sply['btc_blk'],
            DCR_real['btc_blk'],
            BTC_half['blk']
            ]
        y_data = [
            BTC_sply['Sply_ideal'],
            BTC_sply['S2F_ideal'],
            BTC_real['S2F'],
            DCR_sply['Sply_ideal'],
            DCR_sply['S2F_ideal'],
            DCR_real['S2F'],
            DCR_sply['Sply_ideal'],
            DCR_sply['S2F_ideal'],
            DCR_real['S2F'],
            BTC_half['y_arb']
            ]
        name_data = [
            'Bitcoin Coin Supply',
            'Bitcoin S2F Ratio',
            'Bitcoin S2F Ratio (Actual)',
            'Decred Coin Supply',
            'Decred S2F Ratio',
            'Decred S2F Ratio (Actual)',
            'Decred Coin Supply (Offset)',
            'Decred S2F Ratio (Offset)',
            'Decred S2F Ratio (Offset, Actual)',
            'BTC Halvings'
            ]
        color_data = [
            'rgb(237, 109, 71)','rgb(237, 109, 71)','rgb(237, 109, 71)',
            'rgb(112, 203, 255)','rgb(112, 203, 255)','rgb(112, 203, 255)',
            'rgb(46, 214, 161)','rgb(46, 214, 161)','rgb(46, 214, 161)',
            'rgb(200, 92, 92)' 
            ]
        dash_data = [
            'solid','dot','solid',
            'solid','dot','solid',
            'solid','dot','solid',
            'dash'
            ]
        width_data = [
            5,5,1,4,4,1,4,4,1,1
            ]
        opacity_data = [
            1,1,0.75,
            1,1,0.75,
            1,1,0.75,
            1
            ]
        legend_data = [
            True,True,True,
            True,True,True,
            True,True,True,
            True
            ]
        title_data = [
            '<b>Bitcoin and Decred Monetary Policy</b>',
            '<b>Bitcoin Block Height</b>',
            '<b>Coin Supply</b>',
            '<b>Stock-to-Flow Ratio</b>'
            ]
        loop_data = [[0,3,6],[1,2,4,5,7,8,9]]
        range_data = [[0,2400000],[0,21000000],[-1,5]]
        type_data = ['linear','linear','log']
        autorange_data = [False,False,False]

        fig=check_standard_charts(
            title_data,
            range_data,
            type_data,
            autorange_data
            ).subplot_lines_doubleaxis(
                loop_data,
                x_data,
                y_data,
                name_data,
                color_data,
                dash_data,
                width_data,
                opacity_data,
                legend_data
                )
    
        return fig


    def chart_dcrbtc_sply_marketcap(self):
        """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        CREATE PLOT 03
            SUPPLY AND DEMAND - % of Supply Mined VS Market Cap
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""

        x_data = [
            BTC_real['SplyCur']/21e6,BTC_real['SplyCur']/21e6,BTC_sply['Sply_ideal']/21e6,
            DCR_real['SplyCur']/21e6,DCR_real['SplyCur']/21e6,DCR_sply['Sply_ideal']/21e6,
            LTC_real['SplyCur']/84e6,LTC_real['SplyCur']/84e6,LTC_sply['Sply_ideal']/84e6,
            BTC_half['end_pct_totsply']
            ]
        y_data = [
            BTC_real['CapMrktCurUSD'],BTC_real['CapRealUSD'],BTC_sply['CapS2Fmodel'],
            DCR_real['CapMrktCurUSD'],DCR_real['CapRealUSD'],DCR_sply['CapS2Fmodel'],
            LTC_real['CapMrktCurUSD'],LTC_real['CapRealUSD'],LTC_sply['CapS2Fmodel'],
            BTC_half['y_arb']
            ]
        name_data = [
            'Bitcoin Market Cap','Bitcoin Realised Cap','Bitcoin S2F Model',
            'Decred Market Cap','Decred Realised Cap','Decred S2F Model',
            'Litecoin Market Cap','Litecoin Realised Cap','Litecoin S2F Model',
            'BTC Halvings'
            ]
        color_data = [
            'rgb(237, 109, 71)','rgb(237, 109, 71)','rgb(237, 109, 71)',
            'rgb(46, 214, 161)','rgb(46, 214, 161)','rgb(46, 214, 161)',
            'rgb(255, 192, 0)','rgb(255, 192, 0)','rgb(255, 192, 0)',
            'rgb(200, 92, 92)' 
            ]
        dash_data = [
            'solid','dash','solid',
            'solid','dash','solid',
            'solid','dash','solid',
            'dot'
            ]
        width_data = [
            2,2,1,
            2,2,1,
            2,2,1,
            1
            ]
        opacity_data = [
            1,1,0.75,
            1,1,0.75,
            1,1,0.75,
            1
            ]
        legend_data = [
            True,True,True,
            True,True,True,
            False,False,False,
            True
            ]

        title_data = [
            '<b>Market Capitalisation vs Supply Mined</b>',
            '<b>Coin Supply Issued</b>',
            '<b>Coin Market Cap</b>'
            ]
        range_data = [[0,1],[4,15]]
        type_data = ['linear','log']
        autorange_data = [False,False]
        loop_data = [range(0,10)]
        
        fig=check_standard_charts(
            title_data,
            range_data,
            type_data,
            autorange_data
            ).subplot_lines_singleaxis(
                loop_data,
                x_data,
                y_data,
                name_data,
                color_data,
                dash_data,
                width_data,
                opacity_data,
                legend_data
                )
        fig.update_xaxes(dtick=0.1)
        fig.update_layout(title_text=title_data[0])
        #fig.update_layout(
        #    paper_bgcolor='rgb(0,0,0)',
        #    plot_bgcolor='rgb(0,0,0)')
        return fig

    def chart_dcrbtc_s2f_model(self):
        """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        CREATE PLOT 04
                STOCK-TO-FLOW - S2F Market Cap
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""

        x_data = [
            BTC_real['S2F'],
            DCR_real['S2F'],
            LTC_real['S2F'],
            BTC_half['S2F'],BTC_real['S2F']
        ]
        y_data = [
            BTC_real['CapMrktCurUSD'],
            DCR_real['CapMrktCurUSD'],
            LTC_real['CapMrktCurUSD'],
            BTC_half['y_arb'],BTC_real['CapPlanBmodel']
            ]
        name_data = [
            'Bitcoin Market Cap',
            'Decred Market Cap',
            'Litecoin Market Cap',
            'Bitcoin Halvings','Plan B Model'
            ]
        color_data = [
            'rgb(237, 109, 71)',
            'rgb(46, 214, 161)',
            'rgb(255, 192, 0)',
            'rgb(255,255,255)','rgb(255,255,255)'
            ]
        dash_data = [
            'solid',
            'solid',
            'solid',
            'dash','solid'
            ]
        size_data = [
            4,4,4,2,2
            ]
        legend_data = [
            True,True,False,
            True,True
        ]
        fig = make_subplots(specs=[[{"secondary_y": False}]])
        for i in range(0,3):
            fig.add_trace(go.Scatter(
                mode = 'markers',
                x=x_data[i], y=y_data[i],
                name=name_data[i],
                showlegend=legend_data[i],
                marker=dict(size=size_data[i],color=color_data[i])),
                secondary_y=False)
        for i in range(3,4):
            fig.add_trace(go.Scatter(
                x=x_data[i], y=y_data[i],
                name=name_data[i],
                showlegend=legend_data[i],
                line=dict(width=size_data[i],color=color_data[i],dash=dash_data[i])),
                secondary_y=False)

        """$$$$$$$$$$$$$$$ FORMATTING $$$$$$$$$$$$$$$$"""
        # Add figure title
        fig.update_layout(title_text="Market Capitalisation vs Stock-to-Flow Ratio")
        fig.update_xaxes(
            title_text="<b>Stock-to-Flow Ratio</b>",
            type='log',
            range=[-1,2]
            )
        fig.update_yaxes(
            title_text="<b>Coin Market Cap</b>",
            type="log",
            range=[4,12],
            secondary_y=False)
        fig.update_layout(template="plotly_dark")
        return fig

    
#dcrbtc_monetary_policy().chart_dcrbtc_sply_area().show()
#dcrbtc_monetary_policy().chart_dcrbtc_sply_s2f().show()
#dcrbtc_monetary_policy().chart_dcrbtc_sply_marketcap().show()
#dcrbtc_monetary_policy().chart_dcrbtc_s2f_model().show()


class ltcbtc_monetary_policy():
    
    def __init__(self):
        pass

    def chart_ltcbtc_sply_area(self):
        """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        CREATE PLOT 01
                SUPPLY CURVES - STACKED AREA CHARTS
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
        x_data = [
            BTC_sply['blk'],
            LTC_sply['btc_blk']
        ]
        y_data = [
            BTC_sply['Sply_ideal'],
            LTC_sply['Sply_ideal']
        ]
        name_data = [
            'BTC Total Supply',
            'LTC Total Supply'
        ]
        color_data = [
            'rgb(255, 153, 0)',
            'rgb(255, 192, 0)'
        ]
        fill_data = [
            'tonexty',
            'tozeroy'
        ]
        opacity_data = [
            1,1
        ]
        fig = go.Figure()
        for i in range(0,1):
            fig.add_trace(go.Scatter(
                x=x_data[i], 
                y=y_data[i],
                name=name_data[i], 
                fill=fill_data[i],
                #fillcolor=color_data[i],
                #line_color= color_data[i],
                line=dict(
                    color=color_data[i],
                    width=2
                    #opacity=opacity_data[i]
                )))
        fig.update_layout(template="plotly_dark",title="Bitcoin and Litecoin Theoretical Supply Curves")
        
        return fig


    def chart_ltcbtc_sply_s2f(self):
        """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        CREATE PLOT
                SUPPLY CURVES AND STOCK TO FLOW RATIOS
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
        # BTC Theoretical Supply curve
        # DCR Theoretical Supply curve
        # DCR Theoretical Supply curve (Offset to BTC 1.68million)
        # BTC Theoretical S2F
        # DCR Theoretical S2F
        # DCR Theoretical S2F (Offset to BTC 1.68million)
        # BTC Halvings
        x_data = [
            BTC_sply['blk'],
            BTC_sply['blk'],
            BTC_real['blk'],
            LTC_sply['btc_blk']+148500,
            LTC_sply['btc_blk']+148500,
            LTC_real['btc_blk']+148500,
            LTC_sply['btc_blk'],
            LTC_sply['btc_blk'],
            LTC_real['btc_blk'],
            BTC_half['blk']
        ]
        y_data = [
            BTC_sply['Sply_ideal'],
            BTC_sply['S2F_ideal'],
            BTC_real['S2F'],
            LTC_sply['Sply_ideal'],
            LTC_sply['S2F_ideal'],
            LTC_real['S2F'],
            LTC_sply['Sply_ideal'],
            LTC_sply['S2F_ideal'],
            LTC_real['S2F'],
            BTC_half['y_arb']
            ]
        name_data = [
            'Bitcoin Coin Supply',
            'Bitcoin S2F Ratio',
            'Bitcoin S2F Ratio (Actual)',
            'Litecoin Coin Supply',
            'Litecoin S2F Ratio',
            'Litecoin S2F Ratio (Actual)',
            'Litecoin Coin Supply (Offset)',
            'Litecoin S2F Ratio (Offset)',
            'Litecoin S2F Ratio (Offset, Actual)',
            'BTC Halvings'
            ]
        color_data = [
            'rgb(237, 109, 71)','rgb(237, 109, 71)','rgb(237, 109, 71)',
            'rgb(255, 192, 0)','rgb(255, 192, 0)','rgb(255, 192, 0)',
            'rgb(250, 38, 53)','rgb(250, 38, 53)','rgb(250, 38, 53)',
            'rgb(255, 255, 255)' 
            ]
        dash_data = [
            'solid','dot','solid',
            'solid','dot','solid',
            'solid','dot','solid',
            'solid'
            ]
        width_data = [
            5,5,1,4,4,1,4,4,1,0.5
            ]
        opacity_data = [
            1,1,0.75,
            1,1,0.75,
            1,1,0.75,
            0.5
        ]
        name_data[6]

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        for i in [0,3,6]:
            fig.add_trace(go.Scatter(
                x=x_data[i], y=y_data[i],
                name=name_data[i],
                opacity=opacity_data[i],
                line=dict(width=width_data[i],color=color_data[i],dash=dash_data[i])),
                secondary_y=False)
        for i in [1,2,4,5,7,8,9]:
            fig.add_trace(go.Scatter(
                x=x_data[i], y=y_data[i],
                name=name_data[i],
                opacity=opacity_data[i],
                line=dict(width=width_data[i],color=color_data[i],dash=dash_data[i])),
                secondary_y=True)
        """$$$$$$$$$$$$$$$ FORMATTING $$$$$$$$$$$$$$$$"""
        # Add figure title
        fig.update_layout(title_text="Bitcoin and Litecoin Monetary Policy")
        fig.update_xaxes(
            title_text="<b>Bitcoin Block Height</b>",
            type='linear',
            range=[0,1200000]
            )
        fig.update_yaxes(
            title_text="<b>Coin Supply</b>",
            type="linear",
            range=[0,21000000],
            secondary_y=False)
        fig.update_yaxes(
            title_text="<b>Stock-to-Flow Ratio</b>",
            type="log",
            range=[-1,5],
            secondary_y=True)
        fig.update_layout(template="plotly_dark")
        return fig

    def chart_ltcbtc_sply_marketcap(self):
        """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        CREATE PLOT 03
            SUPPLY AND DEMAND - % of Supply Mined VS Market Cap
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""

        BTC_sply['CapS2Fmodel_ideal'] = np.exp(3.31954*np.log(BTC_sply['S2F_ideal'])+14.6227)
        DCR_sply['CapS2Fmodel_ideal'] = np.exp(3.31954*np.log(DCR_sply['S2F_ideal'])+14.6227)
        LTC_sply['CapS2Fmodel_ideal'] = np.exp(3.31954*np.log(LTC_sply['S2F_ideal'])+14.6227)
        x_data = [
            BTC_real['SplyCur']/21e6,BTC_real['SplyCur']/21e6,BTC_sply['Sply_ideal']/21e6,
            DCR_real['SplyCur']/21e6,DCR_real['SplyCur']/21e6,DCR_sply['Sply_ideal']/21e6,
            LTC_real['SplyCur']/84e6,LTC_real['SplyCur']/84e6,LTC_sply['Sply_ideal']/84e6,
            BTC_half['end_pct_totsply']
        ]
        y_data = [
            BTC_real['CapMrktCurUSD'],BTC_real['CapRealUSD'],BTC_sply['CapS2Fmodel_ideal'],
            DCR_real['CapMrktCurUSD'],DCR_real['CapRealUSD'],DCR_sply['CapS2Fmodel_ideal'],
            LTC_real['CapMrktCurUSD'],LTC_real['CapRealUSD'],LTC_sply['CapS2Fmodel_ideal'],
            BTC_half['y_arb']
            ]
        name_data = [
            'Bitcoin Market Cap','Bitcoin Realised Cap','Bitcoin S2F Model',
            'Decred Market Cap','Decred Realised Cap','Decred S2F Model',
            'Litecoin Market Cap','Litecoin Realised Cap','Litecoin S2F Model',
            'BTC Halvings'
            ]
        color_data = [
            'rgb(237, 109, 71)','rgb(237, 109, 71)','rgb(237, 109, 71)',
            'rgb(46, 214, 161)','rgb(46, 214, 161)','rgb(46, 214, 161)',
            'rgb(255, 192, 0)','rgb(255, 192, 0)','rgb(255, 192, 0)',
            'rgb(255, 255, 255)' 
            ]
        dash_data = [
            'solid','dash','solid',
            'solid','dash','solid',
            'solid','dash','solid',
            'dot'
            ]
        width_data = [
            2,2,1,
            2,2,1,
            2,2,1,
            0.5
            ]
        opacity_data = [
            1,1,0.5,
            1,1,0.5,
            1,1,0.5,
            1
        ]
        legend_data = [
            True,True,True,
            True,True,True,
            True,True,True,
            True
        ]

        fig = make_subplots(specs=[[{"secondary_y": False}]])
        for i in range(0,10):
            fig.add_trace(go.Scatter(
                x=x_data[i], y=y_data[i],
                name=name_data[i],
                opacity=opacity_data[i],
                showlegend=legend_data[i],
                line=dict(width=width_data[i],color=color_data[i],dash=dash_data[i])),
                secondary_y=False)

        """$$$$$$$$$$$$$$$ FORMATTING $$$$$$$$$$$$$$$$"""
        # Add figure title
        fig.update_layout(title_text="Market Capitalisation vs Supply Mined")
        fig.update_xaxes(
            title_text="<b>Coin Supply Issued</b>",
            type='linear',
            range=[0,1],
            dtick = 0.1
            )
        fig.update_yaxes(
            title_text="<b>Coin Market Cap</b>",
            type="log",
            range=[4,15],
            secondary_y=False)
        fig.update_layout(template="plotly_dark")
        return fig


    def chart_ltcbtc_s2f_model(self):
        """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        CREATE PLOT 04
                STOCK-TO-FLOW - S2F Market Cap
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""

        x_data = [
            BTC_real['S2F'],
            DCR_real['S2F'],
            LTC_real['S2F'],
            BTC_half['S2F'],BTC_real['S2F']
        ]
        y_data = [
            BTC_real['CapMrktCurUSD'],
            DCR_real['CapMrktCurUSD'],
            LTC_real['CapMrktCurUSD'],
            BTC_half['y_arb'],BTC_real['CapS2Fmodel']
            ]
        name_data = [
            'Bitcoin Market Cap',
            'Decred Market Cap',
            'Litecoin Market Cap',
            'Bitcoin Halvings','Plan B Model'
            ]
        color_data = [
            'rgb(237, 109, 71)',
            'rgb(46, 214, 161)',
            'rgb(255, 192, 0)',
            'rgb(255,255,255)','rgb(255,255,255)'
            ]
        dash_data = [
            'solid',
            'solid',
            'solid',
            'dash','solid'
            ]
        size_data = [
            4,4,4,2,2
            ]
        legend_data = [
            True,True,True,
            True,True
        ]
        fig = make_subplots(specs=[[{"secondary_y": False}]])
        for i in range(0,3):
            fig.add_trace(go.Scatter(
                mode = 'markers',
                x=x_data[i], y=y_data[i],
                name=name_data[i],
                showlegend=legend_data[i],
                marker=dict(size=size_data[i],color=color_data[i])),
                secondary_y=False)
        for i in range(3,4):
            fig.add_trace(go.Scatter(
                x=x_data[i], y=y_data[i],
                name=name_data[i],
                showlegend=legend_data[i],
                line=dict(width=size_data[i],color=color_data[i],dash=dash_data[i])),
                secondary_y=False)

        """$$$$$$$$$$$$$$$ FORMATTING $$$$$$$$$$$$$$$$"""
        # Add figure title
        fig.update_layout(title_text="Market Capitalisation vs Stock-to-Flow Ratio")
        fig.update_xaxes(
            title_text="<b>Stock-to-Flow Ratio</b>",
            type='log',
            range=[-1,2]
            )
        fig.update_yaxes(
            title_text="<b>Coin Market Cap</b>",
            type="log",
            range=[4,12],
            secondary_y=False)
        fig.update_layout(template="plotly_dark")
        return fig


#ltcbtc_monetary_policy().chart_ltcbtc_sply_area().show()
#ltcbtc_monetary_policy().chart_ltcbtc_sply_s2f().show()
#ltcbtc_monetary_policy().chart_ltcbtc_sply_marketcap().show()
#ltcbtc_monetary_policy().chart_ltcbtc_s2f_model().show()

"""**************************************************************************
                            Part 2 - Proof of Work
***************************************************************************"""

class dcrbtc_pow_security():

    def __init__(self):
        pass

    def chart_dcrbtc_btc_premine(self):
        """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        CREATE PLOT
        Bitcoin premine + hashrate up to 1.68 Million Supply
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
        
        #Typical CPU hashrates from 2009
        # https://en.bitcoin.it/wiki/Non-specialized_hardware_comparison
        # https://en.wikipedia.org/wiki/List_of_Intel_Core_i7_microprocessors#Nehalem_microarchitecture_(1st_generation)
        core_i7_920 = [[0,19.2e6],[21e6,19.2e6]]
        core_i7_920 = pd.DataFrame(data=core_i7_920,columns=['sply_arb','hashrate_Hs'])
        core_i7_920

        #Calculate early Bitcoin sub-set up to supply of 1.68million
        #Establish the grounds for a low premine
        BTC_early = BTC_real[BTC_real['SplyCur']<(1.68e6*2)]
        BTC_early = BTC_early[BTC_early['blk']>0]
        BTC_early = pd.concat([BTC_early.set_index('blk',drop=False),BTC_hash],axis=1,join='inner')

        x_data = [
            BTC_early['SplyCur'],
            BTC_early['SplyCur'],
            core_i7_920['sply_arb'],
            [1.68e6,1.68e6]

        ]
        y_data = [
            BTC_early['DiffMean'],
            BTC_early['pow_hashrate_THs']*1e12,
            core_i7_920['hashrate_Hs'],
            [0,1e10]
            ]

        name_data = [
            'Bitcoin Difficulty',
            'Bitcoin Hashrate',
            '1x Core i7 920 Hashrate (4/8 p/t)',
            'Satoshi 1.68M Premine?'
            ]
        color_data = [
            'rgb(237, 109, 71)',
            'rgb(20, 169, 233)',
            'rgb(250, 38, 53)',
            'rgb(250, 38, 53)'

            ]
        dash_data = [
            'solid',
            'solid',
            'dash',
            'dash'
            ]
        width_data = [
            4,4,4,4
            ]

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        for i in [0]:
            fig.add_trace(go.Scatter(
                mode = 'lines',
                x=x_data[i], y=y_data[i],
                name=name_data[i],
                #yaxis=axis_data[i],
                line=dict(width=width_data[i],color=color_data[i],dash=dash_data[i])),
                secondary_y=False)
        for i in [1,2,3]:
            fig.add_trace(go.Scatter(
                mode = 'lines',
                x=x_data[i], y=y_data[i],
                name=name_data[i],
                line=dict(width=width_data[i],color=color_data[i],dash=dash_data[i])),
                secondary_y=True)
        """$$$$$$$$$$$$$$$ FORMATTING $$$$$$$$$$$$$$$$"""
        # Add figure title
        fig.update_layout(
            title_text="How large was Bitcoin's Early Premine?",
            titlefont=dict(size=26)
            )
        fig.update_xaxes(
            title_text="<b>Bitcoin Supply Mined</b>",
            titlefont=dict(size=14),
            type='linear',
            range=[0,2.5e6]
            )
        fig.update_yaxes(
            title_text="<b>Bitcoin Difficulty</b>",
            type="log",
            titlefont=dict(color='rgb(237, 109, 71)',size=14),
            tickfont=dict(color='rgb(237, 109, 71)',size=14),
            secondary_y=False)
        fig.update_yaxes(
            title_text="<b>Hashrate (H/s)</b>",
            type="log",
            range=[5,9],
            titlefont=dict(color='rgb(20, 169, 233)',size=14),
            tickfont=dict(color='rgb(20, 169, 233)',size=14),
            secondary_y=True)
        fig.update_layout(template="plotly_dark")
        return fig

    def chart_dcrbtc_diff_sply(self):
        """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        CREATE PLOT 03
            SUPPLY AND DEMAND - % of Supply Mined VS Market Cap
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
        btc_01 = BTC_real[BTC_real['age_sply']<=0.1]
        btc_01 = btc_01['DiffMean'][btc_01.index[-1]]
        dcr_01 = DCR_real[DCR_real['age_sply']<=0.1]
        dcr_01 = DCR_real['pow_diff'][DCR_real.index[0]]

        loop_data = [[0,1],[]]
        x_data = [
            BTC_real['age_sply'],
            DCR_real['age_sply'],
            #LTC_real['SplyCur']/84e6,
            BTC_half['end_pct_totsply']
            ]
        y_data = [
            BTC_real['DiffMean'],
            DCR_real['pow_diff']/dcr_01,
            #LTC_real['DiffMean'],
            BTC_half['y_arb']
            ]
        name_data = [
            'Bitcoin Difficulty',
            'Decred Difficulty',
            #'Litecoin Difficulty',
            'BTC Halvings'
            ]
        color_data = [
            'rgb(237, 109, 71)',
            'rgb(46, 214, 161)',
            #'rgb(255, 192, 0)',
            'rgb(255, 255, 255)' 
            ]
        dash_data = [
            'solid',
            'solid',
            #'solid',
            'dot'
            ]
        width_data = [
            2,
            2,
            #2,
            1
            ]
        opacity_data = [
            1,
            1,
            #1,
            1
            ]
        legend_data = [
            True,
            True,
            #True,
            True
            ]

        title_data = [
            '<b>Difficulty Adjustment</b>',
            '<b>Coin Supply Issued</b>',
            '<b>Bitcoin Difficulty</b>',
            '<b>Decred Difficulty</b>'
            ]
        range_data = [[0,1],[0,15],[0,6]]
        type_data = ['linear','log','log']
        autorange_data = [False,True,True]
        
        
        fig=check_standard_charts().subplot_lines_doubleaxis(
            title_data,
            range_data,
            type_data,
            autorange_data,
            loop_data,
            x_data,
            y_data,
            name_data,
            color_data,
            dash_data,
            width_data,
            opacity_data,
            legend_data
            )
        fig.update_xaxes(dtick=0.1)
        fig.update_layout(title_text=title_data[0])
        #fig.update_layout(
        #    paper_bgcolor='rgb(0,0,0)',
        #    plot_bgcolor='rgb(0,0,0)')
        return fig



#dcrbtc_pow_security().chart_dcrbtc_btc_premine().show()
dcrbtc_pow_security().chart_dcrbtc_diff_sply().show()


"""**************************************************************************
                            Part 3 - User Adoption
***************************************************************************"""

class dcrbtc_userbase():

    def __init__(self):
        pass

    def chart_dcrbtc_volactaddress_sply(self):
        """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        CREATE PLOT
        ONCHAIN VOLUME AND ACTIVE ADDRESS VS COIN SUPPLY
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""

        # Plot against coin supply
        # Yaxis 1 = Difficulty Adjustment Growth
        # Yaxis 2 = Hashrate

        x_data = [
            BTC_real['SplyCur']/21e6, #BTC TxTfrValAdjNtv
            DCR_real['SplyCur']/21e6, #DCR TxTfrValAdjNtv
            BTC_real['SplyCur']/21e6, #AdrActCnt
            DCR_real['SplyCur']/21e6, #AdrActCnt
            BTC_real['SplyCur']/21e6, #AdrActCnt
            DCR_real['SplyCur']/21e6  #AdrActCnt
            ]
        
        y_data = [
            BTC_real['TxTfrValAdjNtv'].rolling(28).mean(),
            DCR_real['TxTfrValAdjNtv'].rolling(28).mean(),
            BTC_real['AdrActCnt'].rolling(28).mean(),
            DCR_real['AdrActCnt'].rolling(28).mean(),
            BTC_real['TxTfrValAdjUSD'].rolling(28).mean(),
            DCR_real['TxTfrValAdjUSD'].rolling(28).mean()
            ]

        name_data = [
            'Bitcoin Transferred BTC (Adj)',
            'Decred Transferred DCR (Adj)',
            'Bitcoin Active Address',
            'Decred Active Address',
            'Bitcoin Transferred USD (Adj)',
            'Decred Transferred USD (Adj)'
            ]
        color_data = [
            'rgb(239, 125, 50)',
            'rgb(112, 203, 255)',
            'rgb(255, 204, 102)',
            'rgb(41, 112, 255)',
            'rgb(200, 92, 92)',
            'rgb(46, 214, 161)'
            ]

        dash_data = [
            'solid',
            'solid',
            'solid',
            'solid',
            'dot',
            'dot'
            ]
        width_data = [
            2,2,2,2,3,3
            ]

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        for i in [0,1,2,3]:
            fig.add_trace(go.Scatter(
                mode = 'lines',
                x=x_data[i], y=y_data[i],
                name=name_data[i],
                line=dict(width=width_data[i],color=color_data[i],dash=dash_data[i])),
                secondary_y=False)
        for i in [4,5]:
            fig.add_trace(go.Scatter(
                mode = 'lines',
                x=x_data[i], y=y_data[i],
                name=name_data[i],
                line=dict(width=width_data[i],color=color_data[i],dash=dash_data[i])),
                secondary_y=True)
        """$$$$$$$$$$$$$$$ FORMATTING $$$$$$$$$$$$$$$$"""
        # Add figure title
        fig.update_layout(title_text="Daily On-chain Activity")
        fig.update_xaxes(
            title_text="<b>Total Supply Minted</b>",
            type='linear',
            range=[0,1],
            tickformat= ',.0%',
            dtick=0.1
            )
        fig.update_yaxes(
            title_text="<b>Active Address | Native Coins Transferred (Daily Adj)</b>",
            type="log",
            range=[2,7],
            secondary_y=False)
        fig.update_yaxes(
            title_text="<b>USD Value Transferred (Adj)</b>",
            type="log",
            range=[3,10],
            showgrid=False,
            secondary_y=True)
        fig.update_layout(template="plotly_dark")
        
        return fig

#dcrbtc_userbase().chart_dcrbtc_volactaddress_sply().show()


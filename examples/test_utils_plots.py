import matplotlib.pyplot as plt 
import numpy as np

plt.rcdefaults()
FS = 10
plt.rc('grid'  ,linewidth=0.25,alpha=0.25,linestyle='--')
plt.rc('axes'  ,grid=True)
plt.rc('axes'  ,labelsize=FS)    # xy-labels font
plt.rc('xtick' ,labelsize=FS-1)  # x-ticks font
plt.rc('ytick' ,labelsize=FS-1)  # x-ticks font 
plt.rc('legend',fontsize=FS)     # legend font
plt.rc('legend',framealpha=1)
plt.rc('lines' ,linewidth=0.9) # lw

plt.rcParams.update({
    "text.usetex": False,  # Change to True if you want to use LaTeX for text rendering
    "font.family": "serif",
})

def add_last(arr): 
        return arr + [arr[-1]]

def get_subplots(data,Tss,ar=2):

    aspect_ratio      = ar
    cm2in             = 1/2.54
    figw              = 18*cm2in
    figh              = figw*aspect_ratio**-1 
    fig, ax_main_arr = plt.subplots(2,1,figsize=(figw, figh),sharex=True,gridspec_kw={"height_ratios":[1, 1.25]},layout="constrained")

    ax_main = ax_main_arr[0]

    ax_right_inner = ax_main.twinx()
    ax_left_outer  = ax_main.twinx()
    ax_right_outer = ax_main.twinx()

    c1 = 'tab:orange'
    c2 = 'tab:cyan'
    c3 = 'm'
    c4 = 'tab:green'
   

    ax_left_outer.set_ylim(0,90);ax_left_outer.set_yticks(np.arange(0,105,15))
    ax_main_arr[0].set_ylim(0,10)

    ax_right_inner.set_ylim(0,1000);ax_right_inner.tick_params("y", rotation=90)
    ax_right_outer.set_ylim(0,1000);ax_right_outer.tick_params("y", rotation=90)

    def make_patch_spines_invisible(ax):
        ax.set_frame_on(True)
        ax.patch.set_visible(False)
        for sp in ax.spines.values():
            sp.set_visible(False)

    def setup_axis(ax, position, offset, color, label, side='right'):

        ax.spines[side].set_position(('outward', offset))
        
        make_patch_spines_invisible(ax)
        ax.spines[side].set_visible(True)
        
        ax.yaxis.set_label_position(side)
        ax.yaxis.set_ticks_position(side)
        
        ax.set_ylabel(label, color=color)
        ax.tick_params(axis='y', colors=color)

    ax_main.set_ylabel("$W_s  (m/s)$", color=c2)
    ax_main.tick_params(axis='y', colors=c2)
    ax_main.spines['left'].set_color(c2)

    ax_right_inner.set_ylabel("$I_s (W/m^2)$", color=c3)
    ax_right_inner.tick_params(axis='y', colors=c3)
    ax_right_inner.spines['right'].set_color(c3)

    xy_offset = 50
    setup_axis(ax_left_outer, 'left', xy_offset , c1, "$W_d (^\circ)$", side='left')
    setup_axis(ax_right_outer, 'right', xy_offset, c4, "$I_c (A)$", side='right')

    ms=0
    ax_main       .plot( add_last( data['wind_speed']), color=c2,   ms=ms,marker='o',mfc='w', drawstyle='steps-post', label="Wind Speed")
    ax_right_inner.plot( add_last( data['solar_radiation']), color=c3,   ms=ms,marker='o',mfc='w', drawstyle='steps-post', label="Temp")
    ax_left_outer .plot( add_last( data['wind_direction']), color=c1,   ms=ms,marker='o',mfc='w', drawstyle='steps-post', label="Angle")
    ax_right_outer.plot( add_last( data['current']),  color=c4,   ms=ms,marker='o',mfc='w', drawstyle='steps-post', label="Current")

    ax_main_arr[1].plot(add_last(data["air_temperature"]),'tab:blue',drawstyle='steps-post',label=r'$T_{amb}$')

    ax_main_arr[1].plot(add_last(Tss),'k',drawstyle='steps-post',label=r'$T_c^{ss}$')

    ax_main_arr[1].set_ylabel('$Temperature$'+'$(^\circ C)$')
    ax_main_arr[1].set_xlabel("Time interval (n.º)",labelpad=8)

    ax_main_arr[1].set_xticklabels([])
    for i in range(data['n_intervals']):
        ax_main_arr[1].text(i+0.5,np.min(data['air_temperature'])-6,f"$t_{i+1}$",ha='center')
    
    return ax_main_arr


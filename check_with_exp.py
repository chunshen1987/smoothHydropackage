#! /usr/bin/env python

import pylab as plt
from numpy import *
import sys
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from os import path
from CSplottools import getPlotElements

centrality_name = ['0_5', '5_10', '10_20', '20_30', '30_40',
                   '40_50', '50_60', '60_70']
centrality_name_th = ['0005', '0510', '1020', '2030', '3040',
                      '4050', '5060', '6070']
centrality_label = ['0-5%', '5-10%', '10-20%', '20-30%', '30-40%',
                    '40-50%', '50-60%', '60-70%']

panel_label = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']
plotfontsize = 20
plotLinewidth = 2
plotMarkerSize = 8

exp_path = './exp_data'

class color:
    """
    define colors in the terminal
    """
    purple = '\033[95m'
    cyan = '\033[96m'
    darkcyan = '\033[36m'
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    bold = '\033[1m'
    underline = '\033[4m'
    end = '\033[0m'


def plot_diffv2_charged_vs_ATLAS(folder_path, icen):
    expdata_path = path.abspath(
        path.join(exp_path, 'LHC2760',
                  'ATLAS_data/ChargedHadron_vnpT_data/arranged_data'))

    fig = plt.figure()
    ax = plt.axes([0.15, 0.13, 0.8, 0.82])
    iplot = 0

    # exp data
    plotlinestyle, plotMarker, plotColor, plotshadowColor = (
        getPlotElements(iplot))
    expdata = loadtxt(path.join(expdata_path, 'v2_%s.txt'
                                % (centrality_name[icen])))
    plt.errorbar(expdata[:, 0], expdata[:, 1],
                 yerr=sqrt(expdata[:, 2] ** 2. + expdata[:, 3] ** 2.),
                 color=plotColor, linestyle='none',
                 linewidth=plotLinewidth,
                 marker=plotMarker, markersize=plotMarkerSize,
                 label='ATLAS data $v_2\{2\}$')

    # theory curves


    plt.plot([0, 10], [0, 0], 'k--', linewidth=plotLinewidth)
    hl = plt.legend(loc=2, fontsize=plotfontsize - 3)
    hl.draw_frame(False)
    plt.xlim([0, 3])
    plt.ylim([0, 0.35])
    plt.xticks(linspace(0.0, 3.0, 7), color='k', size=plotfontsize)
    plt.yticks(linspace(0.0, 0.3, 7), color='k', size=plotfontsize)
    minorLocator = MultipleLocator(0.1)
    ax.xaxis.set_minor_locator(minorLocator)
    plt.xlabel(r'$p_T$ (GeV)', {'fontsize': plotfontsize + 5})
    plt.ylabel(r'$v_2$', {'fontsize': plotfontsize + 5})
    plt.text(0.05, 0.25, 'Pb+Pb %s @ LHC'
             % (centrality_label[icen]), fontsize=plotfontsize)
    plt.savefig(path.expanduser('~/Desktop/charged_v2diff_vs_ATLAS_C%s.pdf'
                % centrality_name[icen]), format='pdf')
    plt.close()
    # plt.show()


def plot_pid_diffv2_vs_ALICE(folder_path, icen):
    expdata_path = path.abspath(
        path.join(exp_path, 'LHC2760',
                  'ALICE_data/v2/Identified_particles'))
    particle_list = ['pion', 'kaon', 'antiproton']
    particle_lable = [r'$\pi^+$', r'$K^+$', r'$p$']

    fig = plt.figure()
    ax = plt.axes([0.15, 0.13, 0.8, 0.82])
    iplot = 0
    for ipart in range(len(particle_list)):
        particle_name = particle_list[ipart]
        expdata = loadtxt(path.join(expdata_path, '%s_v2_2_%s.dat'
                                    % (particle_name,
                                       centrality_name_th[icen])))
        # exp data
        plotlinestyle, plotMarker, plotColor, plotshadowColor = (
            getPlotElements(iplot))
        plt.errorbar(expdata[:, 0], expdata[:, 2], xerr=expdata[:, 1],
                     yerr=expdata[:, 3],
                     color=plotColor, linestyle='none',
                     linewidth=plotLinewidth,
                     marker=plotMarker, markersize=plotMarkerSize,
                     label=particle_lable[ipart])
        # theory curves

        iplot += 1
    # plt.plot([0, 10], [0, 0], 'k--', linewidth = plotLinewidth)
    hl = plt.legend(loc=4, ncol=1, fontsize=plotfontsize - 3)
    hl.draw_frame(False)
    plt.xlim([0, 3])
    plt.ylim([0.0, 0.3])
    plt.xticks(linspace(0.0, 3.0, 7), color='k', size=plotfontsize)
    plt.yticks(color='k', size=plotfontsize)
    minorLocator = MultipleLocator(0.1)
    ax.xaxis.set_minor_locator(minorLocator)
    plt.xlabel(r'$p_T$ (GeV)', {'fontsize': plotfontsize + 5})
    plt.ylabel(r'$v_2$', {'fontsize': plotfontsize + 5})
    plt.text(0.05, 0.27, 'Pb+Pb %s @ LHC' % centrality_label[icen],
             fontsize=plotfontsize)
    plt.savefig(path.expanduser('~/Desktop/pidv2_vs_ALICE_C%s.pdf'
                % centrality_name[icen]), format='pdf')
    plt.close()
    #plt.show()


def plot_vn_vs_cen_ALICE(folder_path):
    # exp data
    expdata_path = path.abspath(
        path.join(exp_path, 'LHC2760', 'ALICE_data'))
    v2_exp = loadtxt(
        path.join(expdata_path,
                  'v2/Charged_hadrons/ALICE_Ch_v2int_Sp_nonflowcorrected.dat'))

    fig = plt.figure()
    plt.axes([0.15, 0.13, 0.8, 0.82])
    iplot = 0

    plotlinestyle, plotMarker, plotColor, plotshadowColor = (
        getPlotElements(iplot))
    iplot += 1
    plt.errorbar(v2_exp[:, 0], v2_exp[:, 1], v2_exp[:, 2],
                 color=plotColor, linestyle='none',
                 linewidth=plotLinewidth,
                 marker=plotMarker, markersize=plotMarkerSize,
                 label=r'ALICE $v_2\{\mathrm{SP}\}$ data')

    #theory


    hl = plt.legend(loc=2, fontsize=plotfontsize - 3)
    hl.draw_frame(False)
    plt.xlim([0, 70])
    plt.ylim([0.0, 0.15])
    plt.xticks(linspace(0, 70, 8), color='k', size=plotfontsize)
    plt.yticks(color='k', size=plotfontsize)
    #minorLocator = MultipleLocator(0.1)
    #ax.xaxis.set_minor_locator(minorLocator)
    plt.xlabel(r'Centrality (%)', {'fontsize': plotfontsize + 5})
    plt.ylabel(r'$v_2$', {'fontsize': plotfontsize + 5})
    plt.savefig(path.expanduser('~/Desktop/v2_vs_cen_ALICE.pdf'),
                format='pdf')
    plt.close()
    #plt.show()


def plot_pidspectra_vs_ALICE(folder_path, icen):
    expdata_path = path.abspath(
        path.join(exp_path, 'LHC2760', 'ALICE_data/ALICEIdSpdata'))

    particle_list = ['pion+', 'Kaon+', 'Proton']
    particle_lable = [r'$\pi^+$', r'$K^+$', r'$p$']

    fig = plt.figure()
    ax = plt.axes([0.15, 0.13, 0.8, 0.82])
    iplot = 0
    for ipart in range(len(particle_list)):
        particle_name = particle_list[ipart]
        expdata = loadtxt(
            path.join(expdata_path,
                      '%s_C%s.dat' % (particle_name,
                                      centrality_name_th[icen])))
        # exp data
        plotlinestyle, plotMarker, plotColor, plotshadowColor = (
            getPlotElements(iplot))
        plt.errorbar(expdata[:, 0], expdata[:, 1] / 2 / pi / expdata[:, 0],
                     yerr=expdata[:, 2] / 2 / pi / expdata[:, 0],
                     color=plotColor, linestyle='none',
                     linewidth=plotLinewidth,
                     marker=plotMarker, markersize=plotMarkerSize,
                     label=particle_lable[ipart])
        # theory curves

        iplot += 1
    # plt.plot([0, 10], [0, 0], 'k--', linewidth = plotLinewidth)
    hl = plt.legend(loc=3, ncol=1, fontsize=plotfontsize - 3)
    hl.draw_frame(False)
    plt.xlim([0, 3])
    plt.ylim([1e-3, 3e3])
    plt.yscale('log')
    plt.xticks(linspace(0.0, 3.0, 7), color='k', size=plotfontsize)
    plt.yticks(color='k', size=plotfontsize)
    minorLocator = MultipleLocator(0.1)
    ax.xaxis.set_minor_locator(minorLocator)
    plt.xlabel(r'$p_T$ (GeV)', {'fontsize': plotfontsize + 5})
    plt.ylabel(r'$dN/(2\pi dy p_T dp_T)$ (GeV$^{-2}$)',
               {'fontsize': plotfontsize + 5})
    plt.text(1.5, 1000, 'Pb+Pb %s @ LHC' % (centrality_label[icen]),
             fontsize=plotfontsize)
    plt.savefig(path.expanduser('~/Desktop/pidSpectra_vs_ALICE_C%s.pdf'
                % centrality_name[icen]), format='pdf')
    plt.close()
    #plt.show()


def make_LHC2760_comparisons(folder_path):

    plot_vn_vs_cen_ALICE(folder_path)

    for icen in range(8):
        plot_diffv2_charged_vs_ATLAS(folder_path, icen)
        plot_pidspectra_vs_ALICE(folder_path, icen)
    for icen in range(1,7):
        plot_pid_diffv2_vs_ALICE(folder_path, icen)


def make_RHIC200_comparisons(folder_path):
    pass


def generate_plots(folder_path, ecm):
    if '%.0f' % ecm == '2760':
        make_LHC2760_comparisons(folder_path)
    elif '%.0f' % ecm == '200':
        make_RHIC200_comparisons(folder_path)
    else:
        raise ValueError("The experimental data is not available "
                         + "at this collision energy in this package")
        exit(1)


def print_help_message():
    print "This script generates plots for comparisons with experimental data"
    print "Usage : "
    print(color.bold + "./check_with_exp.py results_folder -ecm ecm "
          + color.end)
    print "Usage of check_with_exp.py command line arguments: "
    print(color.bold + "-ecm" + color.end
          + "   collision energy (GeV) only support 200 and 2760")
    print(color.bold + "-h | -help" + color.end + "    This message")


if __name__ == "__main__":
    folder_path = path.abspath(path.join('./', str(sys.argv[1])))
    while len(sys.argv) > 2:
        option = sys.argv[2]
        del sys.argv[2]
        if option == '-ecm':
            ecm = float(sys.argv[2])
            del sys.argv[2]
        elif option == '-h':
            print_help_message()
            sys.exit(0)
        else:
            print sys.argv[0], ': invalid option', option
            print_help_message()
            sys.exit(1)
    generate_plots(folder_path, ecm)
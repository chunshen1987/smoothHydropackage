#! /usr/bin/env python

import pylab as plt
from numpy import *
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


def plot_diffv2_charged_vs_ATLAS(icen):
    expdata_path = path.abspath(
        path.join(exp_path, 'LHC2760',
                  'ATLAS_data/ChargedHadron_vnpT_data/arranged_data'))

    fig, ax = plt.subplots()
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
                 label='ATLAS data')

    # theory curves
    plotlinestyle, plotMarker, plotColor, plotshadowColor = (
        getPlotElements(iplot))
    plt.plot(vndata[:, 0], vndata[:, 1], color=plotColor,
             linestyle=plotlinestyle, linewidth=plotLinewidth,
             marker='', markersize=plotMarkerSize,
             label=r'$v_%d$' % iorder)

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
    plt.ylabel(r'$v_n\{2\}$', {'fontsize': plotfontsize + 5})
    plt.text(0.05, 0.25, '%s $\eta/s = %s$ Pb+Pb %s @ LHC'
             % (
        model_label[imodel], vis_label[imodel], centrality_label[icen]),
             fontsize=plotfontsize)
    fig.set_tight_layout(True)
    plt.savefig('/Users/Chun/Desktop/charged_vn_diff_vs_ATLAS_C%s_%s.pdf'
                % (centrality_name[icen], model_name[imodel]), format='pdf')
    # plt.show()


def plot_pid_diffvn2_vs_ALICE(imodel, icen):
    expdata_path = path.abspath('../LHC_ALICEdata/v2/Identified_particles')
    particle_list = ['pion', 'kaon', 'antiproton']
    particle_lable = [r'$\pi^+$', r'$K^+$', r'$p$']

    fig, ax = plt.subplots()
    iplot = 0
    for ipart in range(len(particle_list)):
        particle_name = particle_list[ipart]
        expdata = loadtxt(path.join(expdata_path, '%s_v2_2_%s.dat'
                                    % (
            particle_name, centrality_name_th[icen])))
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
        particle_list_th = ['pion_p_hydro', 'kaon_p_hydro', 'proton_hydro']
        file_name = ('Pb_%s_%s.db'
                     % (centrality_name[icen], model_name[imodel]))
        database_name = path.join(folder_path, file_name)
        dndata = getdiffvn2(database_name, 2, particle_list_th[ipart])
        plotlinestyle, plotMarker, plotColor, plotshadowColor = (
            getPlotElements(iplot))
        plt.plot(dndata[:, 0], dndata[:, 1], color=plotColor,
                 linestyle=plotlinestyle, linewidth=plotLinewidth,
                 marker='', markersize=plotMarkerSize)
        plt.fill_between(dndata[:, 0],
                         dndata[:, 1] - dndata[:, 2],
                         dndata[:, 1] + dndata[:, 2],
                         color=plotColor, alpha=0.2)
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
    plt.ylabel(r'$v_2\{2\}$', {'fontsize': plotfontsize + 5})
    plt.text(0.05, 0.27, '%s $\eta/s = %s$ Pb+Pb %s @ LHC'
             % (
        model_label[imodel], vis_label[imodel], centrality_label[icen]),
             fontsize=plotfontsize)
    fig.set_tight_layout(True)
    plt.savefig('/Users/Chun/Desktop/pidv2_vs_ALICE_C%s_%s.pdf'
                % (centrality_name[icen], model_name[imodel]), format='pdf')
    #plt.show()


def plot_vn_vs_cen_ALICE(imodel):
    # exp data
    v2_exp = loadtxt(
        '/Volumes/ChunShen_works/Works_on_going/LHC_ebe/LHC_ALICEdata/v2/Charged_hadrons/ALICE_Ch_v2int_Sp_nonflowcorrected.dat')
    v3_exp = loadtxt(
        '/Volumes/ChunShen_works/Works_on_going/LHC_ebe/LHC_ALICEdata/v3/ALICE_Chv3_Sp_int.dat')
    v4_exp = loadtxt(
        '/Volumes/ChunShen_works/Works_on_going/LHC_ebe/LHC_ALICEdata/v4/v4_SP.dat')

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
    plotlinestyle, plotMarker, plotColor, plotshadowColor = (
        getPlotElements(iplot))
    iplot += 1
    plt.errorbar(v3_exp[:, 0], v3_exp[:, 1], v3_exp[:, 2],
                 color=plotColor, linestyle='none',
                 linewidth=plotLinewidth,
                 marker=plotMarker, markersize=plotMarkerSize,
                 label=r'ALICE $v_3\{\mathrm{SP}\}$ data')

    plotlinestyle, plotMarker, plotColor, plotshadowColor = (
        getPlotElements(iplot))
    iplot += 1
    plt.errorbar(v4_exp[:, 0], v4_exp[:, 1], v4_exp[:, 2],
                 color=plotColor, linestyle='none',
                 linewidth=plotLinewidth,
                 marker=plotMarker, markersize=plotMarkerSize,
                 label=r'ALICE $v_4\{\mathrm{SP}\}$ data')

    #theory
    v2_th = []
    v2_th_err = []
    v3_th = []
    v3_th_err = []
    v4_th = []
    v4_th_err = []
    v5_th = []
    v5_th_err = []
    cen_central = [2.5, 7.5, 15, 25, 35, 45, 55, 65]
    for icen in range(len(centrality_name)):
        file_name = ('Pb_%s_%s.db'
                     % (centrality_name[icen], model_name[imodel]))
        database_name = path.join(folder_path, file_name)
        v2data = getintevn2(database_name, 2, 'charged_hydro', 0.2, 3.5)
        v3data = getintevn2(database_name, 3, 'charged_hydro', 0.2, 3.5)
        v4data = getintevn2(database_name, 4, 'charged_hydro', 0.2, 3.5)
        v5data = getintevn2(database_name, 5, 'charged_hydro', 0.2, 3.5)
        v2_th.append(v2data[0])
        v2_th_err.append(v2data[1])
        v3_th.append(v3data[0])
        v3_th_err.append(v3data[1])
        v4_th.append(v4data[0])
        v4_th_err.append(v4data[1])
        v5_th.append(v5data[0])
        v5_th_err.append(v5data[1])
    v2_th = array(v2_th)
    v2_th_err = array(v2_th_err)
    v3_th = array(v3_th)
    v3_th_err = array(v3_th_err)
    v4_th = array(v4_th)
    v4_th_err = array(v4_th_err)
    v5_th = array(v5_th)
    v5_th_err = array(v5_th_err)

    iplot = 0
    plotlinestyle, plotMarker, plotColor, plotshadowColor = (
        getPlotElements(iplot))
    iplot += 1
    plt.plot(cen_central, v2_th,
             color=plotColor, linestyle='-',
             linewidth=plotLinewidth,
             marker='', markersize=plotMarkerSize,
             label=labeltext[imodel] + r' $v_2\{\mathrm{SP}\}$')
    plt.fill_between(cen_central, v2_th - v2_th_err, v2_th + v2_th_err,
                     color=plotColor, alpha=0.2)

    plotlinestyle, plotMarker, plotColor, plotshadowColor = (
        getPlotElements(iplot))
    iplot += 1
    plt.plot(cen_central, v3_th,
             color=plotColor, linestyle='--',
             linewidth=plotLinewidth,
             marker='', markersize=plotMarkerSize,
             label=labeltext[imodel] + r' $v_3\{\mathrm{SP}\}$')
    plt.fill_between(cen_central, v3_th - v3_th_err, v3_th + v3_th_err,
                     color=plotColor, alpha=0.2)

    plotlinestyle, plotMarker, plotColor, plotshadowColor = (
        getPlotElements(iplot))
    iplot += 1
    plt.plot(cen_central, v4_th,
             color=plotColor, linestyle='-.',
             linewidth=plotLinewidth,
             marker='', markersize=plotMarkerSize,
             label=labeltext[imodel] + r' $v_4\{\mathrm{SP}\}$')
    plt.fill_between(cen_central, v4_th - v4_th_err, v4_th + v4_th_err,
                     color=plotColor, alpha=0.2)

    plotlinestyle, plotMarker, plotColor, plotshadowColor = (
        getPlotElements(iplot))
    iplot += 1
    plt.plot(cen_central, v5_th,
             color=plotColor, linestyle=':',
             linewidth=plotLinewidth,
             marker='', markersize=plotMarkerSize,
             label=labeltext[imodel] + r' $v_5\{\mathrm{SP}\}$')
    plt.fill_between(cen_central, v5_th - v5_th_err, v5_th + v5_th_err,
                     color=plotColor, alpha=0.2)

    hl = plt.legend(loc=2, ncol=2, fontsize=plotfontsize - 6)
    hl.draw_frame(False)
    plt.xlim([0, 70])
    plt.ylim([0.0, 0.15])
    plt.xticks(linspace(0, 70, 8), color='k', size=plotfontsize)
    plt.yticks(color='k', size=plotfontsize)
    #minorLocator = MultipleLocator(0.1)
    #ax.xaxis.set_minor_locator(minorLocator)
    plt.xlabel(r'Centrality (%)', {'fontsize': plotfontsize + 5})
    plt.ylabel(r'$v_n\{SP\}$', {'fontsize': plotfontsize + 5})
    plt.savefig('/Users/Chun/Desktop/vn_vs_cen_ALICE_%s.pdf'
                % (model_name[imodel]), format='pdf')
    #plt.show()


def plot_pidspectra_vs_ALICE(imodel, icen):
    expdata_path = path.abspath('../LHC_ALICEdata/ALICEIdSpdata')

    particle_list = ['pion+', 'Kaon+', 'Proton']
    particle_lable = [r'$\pi^+$', r'$K^+$', r'$p$']

    fig, ax = plt.subplots()
    iplot = 0
    for ipart in range(len(particle_list)):
        particle_name = particle_list[ipart]
        expdata = loadtxt(path.join(expdata_path, '%s_C%s.dat'
                                    % (
            particle_name, centrality_name_th[icen])))
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
        particle_list_th = ['pion_p_hydro', 'kaon_p_hydro', 'proton_hydro']
        file_name = ('Pb_%s_%s.db'
                     % (centrality_name[icen], model_name[imodel]))
        database_name = path.join(folder_path, file_name)
        dndata = getpTspectra(database_name, particle_list_th[ipart])
        plotlinestyle, plotMarker, plotColor, plotshadowColor = (
            getPlotElements(iplot))
        plt.plot(dndata[:, 0], dndata[:, 1], color=plotColor,
                 linestyle=plotlinestyle, linewidth=plotLinewidth,
                 marker='', markersize=plotMarkerSize)
        plt.fill_between(dndata[:, 0],
                         dndata[:, 1] - dndata[:, 2],
                         dndata[:, 1] + dndata[:, 2],
                         color=plotColor, alpha=0.2)
        iplot += 1
    # plt.plot([0, 10], [0, 0], 'k--', linewidth = plotLinewidth)
    hl = plt.legend(loc=3, ncol=1, fontsize=plotfontsize - 3)
    hl.draw_frame(False)
    plt.xlim([0, 3])
    plt.ylim([1e-2, 1e4])
    plt.yscale('log')
    plt.xticks(linspace(0.0, 3.0, 7), color='k', size=plotfontsize)
    plt.yticks(color='k', size=plotfontsize)
    minorLocator = MultipleLocator(0.1)
    ax.xaxis.set_minor_locator(minorLocator)
    plt.xlabel(r'$p_T$ (GeV)', {'fontsize': plotfontsize + 5})
    plt.ylabel(r'$dN/(2\pi dy p_T dp_T)$ (GeV$^{-2}$)',
               {'fontsize': plotfontsize + 5})
    plt.text(0.05, 3000, '%s $\eta/s = %s$ Pb+Pb %s @ LHC'
             % (
        model_label[imodel], vis_label[imodel], centrality_label[icen]),
             fontsize=plotfontsize)
    fig.set_tight_layout(True)
    plt.savefig('/Users/Chun/Desktop/pidSpectra_vs_ALICE_C%s_%s.pdf'
                % (centrality_name[icen], model_name[imodel]), format='pdf')
    #plt.show()


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
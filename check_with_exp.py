#! /usr/bin/env python

import pylab as plt
from numpy import *
import sys
from glob import glob
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from os import path
from CSplottools import getPlotElements

centrality_name = ['0_5', '5_10', '10_20', '20_30', '30_40',
                   '40_50', '50_60', '60_70']
centrality_name_th = ['0005', '0510', '1020', '2030', '3040',
                      '4050', '5060', '6070']
centrality_name_theory = ['0-5', '5-10', '10-20', '20-30', '30-40',
                          '40-50', '50-60', '60-70', '70-80']
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
    th_data = loadtxt(
        glob(path.join(folder_path, '*C%s*/Charged_vndata.dat'
                       % centrality_name_theory[icen]))[0])
    plt.plot(th_data[:, 0], th_data[:, 8],
             color=plotColor, linestyle=plotlinestyle,
             linewidth=plotLinewidth, marker='', markersize=plotMarkerSize)

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
        th_particle_name_list = ['pion_p', 'Kaon_p', 'proton']
        th_data = loadtxt(
            glob(path.join(folder_path,
                           '*C%s*/%s_vndata.dat'
                           % (centrality_name_theory[icen],
                              th_particle_name_list[ipart])))[0])
        plt.plot(th_data[:, 0], th_data[:, 8],
                 color=plotColor, linestyle=plotlinestyle,
                 linewidth=plotLinewidth, marker='', markersize=plotMarkerSize)

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
    cen_th = array([2.5, 7.5, 15, 25, 35, 45, 55, 65, 75])
    v2_th = []
    for icen in range(len(centrality_name_theory)):
        temp_data = loadtxt(
            glob(path.join(folder_path,
                           '*C%s*/Charged_ptcut02_integrated_vndata.dat'
                           % centrality_name_theory[icen]))[0])
        v2_th.append(temp_data[2, 5])
    v2_th = array(v2_th)
    plt.plot(cen_th, v2_th, color=plotColor, linestyle=plotlinestyle,
             linewidth=plotLinewidth,
             marker='', markersize=plotMarkerSize,
             label=r'theory $\bar{v}_2$')

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


def plot_multiplicity_vs_cen_ALICE(folder_path):
    # exp data
    expdata_path = path.abspath(
        path.join(exp_path, 'LHC2760', 'ALICE_data'))
    dn_exp = loadtxt(path.join(expdata_path, 'Multiplicity_Centrality.dat'))

    fig = plt.figure()
    plt.axes([0.15, 0.13, 0.8, 0.82])
    iplot = 0

    plotlinestyle, plotMarker, plotColor, plotshadowColor = (
        getPlotElements(iplot))
    iplot += 1
    plt.errorbar(dn_exp[:, 0], dn_exp[:, 2], xerr=dn_exp[:, 1],
                 yerr=dn_exp[:, 3], color=plotColor, linestyle='none',
                 linewidth=plotLinewidth,
                 marker=plotMarker, markersize=plotMarkerSize,
                 label=r'ALICE data')

    #theory
    temp_data = loadtxt(path.join(folder_path, 'initial_conditions',
                                  'centralityCut_total_entropy.dat'))
    npart_th = temp_data[:,1]
    dn_th = []
    for icen in range(len(centrality_name_theory)):
        temp_data = loadtxt(
            glob(path.join(folder_path,
                           '*C%s*/Charged_eta_integrated_vndata.dat'
                           % centrality_name_theory[icen]))[0])
        dn_th.append(temp_data[0, 1])
    dn_th = array(dn_th)
    plt.plot(npart_th, dn_th/(npart_th/2.),
             color=plotColor, linestyle=plotlinestyle, linewidth=plotLinewidth,
             marker='', markersize=plotMarkerSize,
             label=r'theory')

    hl = plt.legend(loc=2, fontsize=plotfontsize - 3)
    hl.draw_frame(False)
    plt.xlim([0, 400])
    plt.ylim([3, 9])
    plt.xticks(linspace(0, 400, 9), color='k', size=plotfontsize)
    plt.yticks(color='k', size=plotfontsize)
    #minorLocator = MultipleLocator(0.1)
    #ax.xaxis.set_minor_locator(minorLocator)
    plt.xlabel(r'$N_\mathrm{part}$', {'fontsize': plotfontsize + 5})
    plt.ylabel(r'$dN^\mathrm{ch}/d\eta/(N_\mathrm{part}/2)$',
               {'fontsize': plotfontsize + 5})
    plt.savefig(path.expanduser('~/Desktop/multiplicity_vs_cen_ALICE.pdf'),
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
        th_particle_name_list = ['pion_p', 'Kaon_p', 'proton']
        th_data = loadtxt(
            glob(path.join(folder_path,
                           '*C%s*/%s_vndata.dat'
                           % (centrality_name_theory[icen],
                              th_particle_name_list[ipart])))[0])
        plt.plot(th_data[:, 0], th_data[:, 2],
                 color=plotColor, linestyle=plotlinestyle,
                 linewidth=plotLinewidth, marker='', markersize=plotMarkerSize)

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
    """
    Generate comparisons for Pb+Pb collisions at 2.76 A TeV
    """
    plot_multiplicity_vs_cen_ALICE(folder_path)
    # pT-integrated flow
    plot_vn_vs_cen_ALICE(folder_path)

    # pT-differential flow and spectra
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


def print_help_message():
    print "This script generates plots for comparisons with experimental data"
    print "Usage : "
    print(color.bold + "./check_with_exp.py results_folder -ecm ecm "
          + "[-folder results_folder]"
          + color.end)
    print "Usage of check_with_exp.py command line arguments: "
    print(color.bold + "-ecm" + color.end
          + "      collision energy (GeV) only support "
          + color.purple + "200" + color.end + " and "
          + color.purple + "2760" + color.end)
    print(color.bold + "-folder" + color.end
          + "   specify the results folder "
          + color.bold + "./RESULTS [default]" + color.end)
    print(color.bold + "-h | -help" + color.end + "    This message")


if __name__ == "__main__":
    folder_path = path.abspath('./RESULTS')
    if len(sys.argv) == 1:
        print_help_message()
        exit(0)

    while len(sys.argv) > 1:
        option = sys.argv[1]
        del sys.argv[1]
        if option == '-folder':
            folder_path = path.abspath(path.join('./', str(sys.argv[1])))
            del sys.argv[1]
        elif option == '-ecm':
            ecm = float(sys.argv[1])
            del sys.argv[1]
        elif option == '-h':
            print_help_message()
            sys.exit(0)
        else:
            print sys.argv[0], ': invalid option', option
            print_help_message()
            sys.exit(1)
    try:
        ecm
    except NameError:
        print('collision energy is not defined!')
        exit(1)

    if path.isdir(folder_path):
        generate_plots(folder_path, ecm)
    else:
        print('results folder is not found: %s' % folder_path)
        exit(1)

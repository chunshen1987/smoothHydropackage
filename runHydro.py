#! /usr/bin/env python

import shutil
from os import path, makedirs
import subprocess

import sys


cen_list = ['0-5', '5-10', '10-20', '20-30', '30-40',
           '40-50', '50-60', '60-70', '70-80']


def run_hydro_with_iS(icen, hydro_path, iS_path, run_record, err_record,
                      norm_factor, vis, edec, tau0):
    #hydro
    if path.exists(path.join(hydro_path, 'results')):
        shutil.rmtree(path.join(hydro_path, 'results'))
    makedirs(path.join(hydro_path, 'results'))
    cmd = './VISHNew.e'
    args = (' IINIT=2 IEOS=7 iEin=1 iLS=130'
            + ' T0=%6.4f edec=%7.5f vis=%6.4f factor=%11.9f'
            % (tau0, edec, vis, norm_factor,))
    shutil.copyfile('./results/sdAvg_order_2_C%s.dat' % cen_list[icen],
                    path.join(hydro_path, 'Initial', 'InitialSd.dat'))
    print "%s : %s" % (cen_list[icen], cmd + args)
    sys.stdout.flush()
    run_record.write(cmd + args)
    p = subprocess.Popen(cmd + args, shell=True, stdout=run_record,
                         stderr=err_record, cwd=hydro_path)
    p.wait()
    #iS
    if path.exists(path.join(iS_path, 'results')):
        shutil.rmtree(path.join(iS_path, 'results'))
    shutil.move(path.join(hydro_path, 'results'),
                path.join(iS_path, 'results'))
    print "%s : %s" % (cen_list[icen], 'iS_withResonance.sh')
    sys.stdout.flush()
    p = subprocess.Popen('./iS_withResonance.sh',
                         shell=True, stdout=run_record, stderr=err_record,
                         cwd=iS_path)
    p.wait()


def fit_hydro(dNdeta_goal, vis, edec, tau0):
    run_record_file_name = 'run_record_fitNorm.dat'
    err_record_file_name = 'err_record_fitNorm.dat'
    run_record = open(path.join('.', run_record_file_name), 'a')
    err_record = open(path.join('.', err_record_file_name), 'a')
    hydro_path = path.abspath('./VISHNew')
    iS_path = path.abspath('./iS')
    norm_factor = 1.0
    tol = 1e-3
    target_file = 'Charged_eta_integrated_vndata.dat'
    while 1:
        icen = 0
        run_hydro_with_iS(icen, hydro_path, iS_path, run_record, err_record,
                          norm_factor, vis, edec, tau0)
        #get target results
        temp_data = open(path.join(iS_path, 'results', target_file), 'r')
        dN_deta = float(temp_data.readline().split()[1])
        temp_data.close()
        print "dNdeta_goal = %g, dNdeta = %g, norm = : %g" % (
            dNdeta_goal, dN_deta, norm_factor,)
        sys.stdout.flush()
        shutil.rmtree(path.join(iS_path, 'results'))
        if abs(dNdeta - dNdeta_goal) / dNdeta_goal > tol:
            norm_factor = norm_factor * dNdeta_goal / dNdeta
        else:
            break
    shutil.move(path.join('.', run_record_file_name),
                path.abspath('./results'))
    shutil.move(path.join('.', err_record_file_name),
                path.abspath('./results'))
    return norm_factor


def run_hydro_all_centralities(norm_factor, vis, edec, tau0):
    run_record_file_name = 'run_record_hydrowithiS.dat'
    err_record_file_name = 'err_record_hydrowithiS.dat'
    run_record = open(path.join('.', run_record_file_name), 'a')
    err_record = open(path.join('.', err_record_file_name), 'a')
    hydro_path = path.abspath('./VISHNew')
    iS_path = path.abspath('./iS')
    for icen in range(len(cen_list)):
        run_hydro_with_iS(icen, hydro_path, iS_path, run_record, err_record,
                          norm_factor, vis, edec, tau0)
        shutil.move(path.join(iS_path, 'results'),
                    path.join('results', 'MCGlbRHICVis008C%sT120Tau6_sd_v2'
                                         % cen_list[icen]))
    shutil.move(path.join('.', run_record_file_name), 'results')
    shutil.move(path.join('.', err_record_file_name), 'results')

if __name__ == "__main__":
    vis = 0.08
    edec = 0.18  # GeV/fm^3
    tau0 = 0.6   # fm/c
    while len(sys.argv) > 1:
        option = sys.argv[1]
        del sys.argv[1]
        if option == '-vis':
            vis = float(sys.argv[1])
            del sys.argv[1]
        elif option == '-edec':
            edec = float(sys.argv[1])
            del sys.argv[1]
        elif option == '-tau0':
            tau0 = float(sys.argv[1])
            del sys.argv[1]
        elif option == '-dNdeta':
            dN_deta = float(sys.argv[1])
            del sys.argv[1]
        else:
            print sys.argv[0], ': invalid option', option
            sys.exit(1)
    norm_factor = fit_hydro(dN_deta, vis, edec, tau0)
    run_hydro_all_centralities(norm_factor, vis, edec, tau0)

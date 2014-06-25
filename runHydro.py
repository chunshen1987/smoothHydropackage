#! /usr/bin/env python

import shutil
from os import path, makedirs, remove
import subprocess
from glob import glob

import sys


cen_list = ['0-5', '5-10', '10-20', '20-30', '30-40',
            '40-50', '50-60', '60-70', '70-80']


def run_hydro_with_iS(icen, hydro_path, iS_path, run_record, err_record,
                      norm_factor, vis, edec, tau0):
    # hydro
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


def run_hybrid_calculation(icen, hydro_path, iSS_path, run_record, err_record,
                           norm_factor, vis, edec, tau0):
    """
        Perform hydro + UrQMD hybrid approach on averaged initial conditions
    """
    result_folder = 'MCGlbRHICVis008C%sT120Tau6' % cen_list[icen]
    results_folder_path = path.join(path.abspath('./results'), result_folder)
    if path.exists(results_folder_path):
        shutil.rmtree(results_folder_path)
    makedirs(results_folder_path)
    # hydro
    hydro_folder_path = path.join(hydro_path, 'results')
    if path.exists(path.join(hydro_folder_path)):
        shutil.rmtree(hydro_folder_path)
    makedirs(hydro_folder_path)
    cmd = './VISHNew.e'
    args = (' IINIT=2 IEOS=7 iEin=1 iLS=130 '
            + 'T0=%6.4f edec=%7.5f vis=%6.4f factor=%11.9f'
            % (tau0, edec, vis, norm_factor,))
    shutil.copyfile('./results/sdAvg_order_2_C%s.dat' % cen_list[icen],
                    path.join(hydro_path, 'Initial', 'InitialSd.dat'))
    print "%s : %s" % (cen_list[icen], cmd + args)
    sys.stdout.flush()
    run_record.write(cmd + args)
    p = subprocess.Popen(cmd + args, shell=True, stdout=run_record,
                         stderr=err_record, cwd=hydro_path)
    p.wait()
    worth_storing = []
    for aGlob in ['surface.dat', 'dec*.dat', 'ecc*.dat']:
        worth_storing.extend(glob(path.join(hydro_folder_path, aGlob)))
    for aFile in glob(path.join(hydro_folder_path, '*')):
        if aFile in worth_storing:
            shutil.copy(aFile, results_folder_path)
    
    #iSS
    iSS_folder_path = path.join(iSS_path, 'results')
    if path.exists(iSS_folder_path):
        shutil.rmtree(iSS_folder_path)
    output_file = 'OSCAR.DAT'
    if path.isfile(path.join(iSS_path, output_file)):
        remove(path.join(iSS_path, output_file))
    shutil.move(path.join(hydro_path, 'results'),
                path.join(iSS_path, 'results'))
    print "%s : %s" % (cen_list[icen], 'iSS.e')
    sys.stdout.flush()
    p = subprocess.Popen('ulimit -n 1000; ./iSS.e', shell=True,
                         stdout=run_record, stderr=err_record, cwd=iSS_path)
    p.wait()
    worth_storing = []
    for aGlob in ['*vn*.dat']:
        worth_storing.extend(glob(path.join(iSS_folder_path, aGlob)))
    for aFile in glob(path.join(iSS_folder_path, '*')):
        if aFile in worth_storing:
            shutil.copy(aFile, results_folder_path)
    shutil.rmtree(iSS_folder_path)  # clean up
    
    #osc2u
    o2u_path = path.abspath('./osc2u')
    input_file = 'OSCAR.DAT'
    output_file = 'fort.14'
    if path.isfile(path.join(o2u_path, input_file)):
        remove(path.join(o2u_path, input_file))
    if path.isfile(path.join(o2u_path, output_file)):
        remove(path.join(o2u_path, output_file))
    shutil.move(path.join(iSS_path, input_file), o2u_path)
    print "%s : %s" % (cen_list[icen], 'osu2u.e')
    sys.stdout.flush()
    p = subprocess.Popen('./osc2u.e < %s' % input_file, shell=True,
                         stdout=run_record, stderr=err_record, cwd=o2u_path)
    p.wait()
    remove(path.join(o2u_path, input_file))  # clean up
    
    #UrQMD
    UrQMD_path = path.abspath('./urqmd')
    input_file = 'OSCAR.input'
    output_file = 'particle_list.dat'
    if path.isfile(path.join(UrQMD_path, input_file)):
        remove(path.join(UrQMD_path, input_file))
    if path.isfile(path.join(UrQMD_path, output_file)):
        remove(path.join(UrQMD_path, output_file))
    shutil.move(path.join(o2u_path, 'fort.14'),
                path.join(UrQMD_path, input_file))
    print "%s : %s" % (cen_list[icen], 'runqmd.sh')
    sys.stdout.flush()
    p = subprocess.Popen('bash runqmd.sh', shell=True, stdout=run_record,
                         stderr=err_record, cwd=UrQMD_path)
    p.wait()
    worth_storing = []
    for aGlob in ['particle_list.dat']:
        worth_storing.extend(glob(path.join(UrQMD_path, aGlob)))
    for aFile in glob(path.join(UrQMD_path, '*')):
        if aFile in worth_storing:
            shutil.copy(aFile, results_folder_path)


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
        # get target results
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
    tau0 = 0.6  # fm/c
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

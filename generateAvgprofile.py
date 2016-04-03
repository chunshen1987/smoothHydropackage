#! /usr/bin/env python

import sys, shutil
from numpy import *
from os import path, makedirs
import subprocess

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


#dictionary for parameter list in superMC
superMCParameters = {
    'which_mc_model'                :   5,
    'sub_model'                     :   1,
    'Npmin'                         :   0,
    'Npmax'                         :   1000,
    'bmin'                          :   0,
    'bmax'                          :   20,
    'cutdSdy'                       :   1,
    'cutdSdy_lowerBound'            :   551.864,
    'cutdSdy_upperBound'            :   1000000.0,
    'Aproj'                         :   208,
    'Atarg'                         :   208,
    'ecm'                           :   2760,
    'finalFactor'                   :   1.0,
    'use_ed'                        :   1,
    'use_sd'                        :   1,
    'alpha'                         :   0.118,
    'lambda'                        :   0.288,
    'operation'                     :   3,
    'include_NN_correlation'        :   1,
    'shape_of_nucleon'              :   2,
    'shape_of_entropy'              :   2,
    'cc_fluctuation_model'          :   6,
    'output_TATB'                   :   1,
    'output_rho_binary'             :   1,
    'output_TA'                     :   1,
    'output_rhob'                   :   1,
    'output_spectator_density'      :   1,
    'nev'                           :   5000,
    'average_from_order'            :   2,
    'average_to_order'              :   2,
    'maxx'                          :   15.0,
    'maxy'                          :   15.0,
    'dx'                            :   0.1,
    'dy'                            :   0.1,
}

nucleus_name_dict = {
    208: 'Pb',
    197: 'Au',
    238: 'U',
    63: 'Cu',
    1: 'p',
    2: 'd',
    3: 'He',
}

nucleus_number_dict = {
    'Pb': 208,
    'Au': 197,
    'U': 238,
    'Cu': 63,
    'p': 1,
    'd': 2,
    'He': 3,
}


def form_assignment_string_from_dict(adict):
    """
        Generate a parameter-equals-value string from the given dictionary. The
        generated string has a leading blank.
    """
    result = ""
    for aparameter in adict.keys():
        result += " {}={}".format(aparameter, adict[aparameter])
    return result


def translate_centrality_cut(centrality_bound, cut_type='total_entropy'):
    """
    translate the centrality boundaries to Npart, dS/dy, b values and update
    the parameter lists for simulations
    """

    centrality_lower_bound = centrality_bound[0]
    centrality_upper_bound = centrality_bound[1]

    if superMCParameters['which_mc_model'] == 5:
        model_name = 'MCGlb'
    elif superMCParameters['which_mc_model'] == 1:
        model_name = 'MCKLN'

    if superMCParameters['cc_fluctuation_model'] != 0:
        multiplicity_fluctuation = 'withMultFluct'
    else:
        multiplicity_fluctuation = 'noMultFluct'

    collision_energy = '%d' % superMCParameters['ecm']

    Aproj = superMCParameters['Aproj']
    Atrag = superMCParameters['Atarg']

    if Aproj == Atrag:  #symmetric collision
        nucleus_name = nucleus_name_dict[Aproj]+nucleus_name_dict[Atrag]
    else:  # asymmetric collision
        nucleus_name = (nucleus_name_dict[min(Aproj, Atrag)]
                        + nucleus_name_dict[max(Aproj, Atrag)])

    centrality_cut_file_name = (
        'iebe_centralityCut_%s_%s_sigmaNN_gauss_d0.9_%s.dat'
        % (cut_type, model_name + nucleus_name + collision_energy,
           multiplicity_fluctuation)
    )

    try:
        centrality_cut_file = loadtxt(
            path.join(path.abspath('./centrality_cut_tables'),
                      centrality_cut_file_name))
    except IOError:
        print "Can not find the centrality cut table for the collision system"
        print centrality_cut_file_name
        exit(1)

    lower_idx = (
        centrality_cut_file[:, 0].searchsorted(centrality_lower_bound+1e-30))
    upper_idx = (
        centrality_cut_file[:, 0].searchsorted(centrality_upper_bound))

    cut_value_upper = (
        (centrality_cut_file[lower_idx-1, 1]
         - centrality_cut_file[lower_idx, 1])
        /(centrality_cut_file[lower_idx-1, 0]
          - centrality_cut_file[lower_idx, 0])
        *(centrality_lower_bound - centrality_cut_file[lower_idx-1, 0])
        + centrality_cut_file[lower_idx-1, 1]
    )
    cut_value_low = (
        (centrality_cut_file[upper_idx-1, 1]
         - centrality_cut_file[upper_idx, 1])
        /(centrality_cut_file[upper_idx-1, 0]
          - centrality_cut_file[upper_idx, 0])
        *(centrality_upper_bound - centrality_cut_file[upper_idx-1, 0])
        + centrality_cut_file[upper_idx-1, 1]
    )
    if cut_type == 'total_entropy':
        superMCParameters['cutdSdy'] = 1
        npart_min = min(centrality_cut_file[lower_idx-1:upper_idx+1, 2])
        npart_max = max(centrality_cut_file[lower_idx-1:upper_idx+1, 3])
        b_min = min(centrality_cut_file[lower_idx-1:upper_idx+1, 4])
        b_max = max(centrality_cut_file[lower_idx-1:upper_idx+1, 5])
        superMCParameters['cutdSdy_lowerBound'] = cut_value_low
        superMCParameters['cutdSdy_upperBound'] = cut_value_upper
    elif cut_type == 'Npart':
        superMCParameters['cutdSdy'] = 0
        b_min = min(centrality_cut_file[lower_idx-1:upper_idx+1, 4])
        b_max = max(centrality_cut_file[lower_idx-1:upper_idx+1, 5])
    superMCParameters['Npmax'] = npart_max
    superMCParameters['Npmin'] = npart_min
    superMCParameters['bmax'] = b_max
    superMCParameters['bmin'] = b_min

    #print out information
    print '-'*80
    print('%s collisions at sqrt{s} = %s A GeV with %s initial conditions'
          % (nucleus_name , collision_energy, model_name))
    print("Centrality : %g - %g"
          % (centrality_lower_bound, centrality_upper_bound) + r"%")
    print 'centrality cut on ', cut_type
    if cut_type == 'total_entropy':
        print 'dS/dy :', cut_value_low, '-', cut_value_upper
    print "Npart: ", npart_min, '-', npart_max
    print "b: ", b_min, '-', b_max, ' fm'
    print '-'*80
    return


def update_superMC_dict(model, ecm, collsys):
    """
    update the superMCParameters dictionary with users input settings
    """
    if model == 'MCGlb':
        superMCParameters['which_mc_model'] = 5
        superMCParameters['sub_model'] = 1
        if superMCParameters['cc_fluctuation_model'] != 0:
            superMCParameters['cc_fluctuation_model'] = 6
            if abs(ecm - 200.) < 1e-6:
                superMCParameters['cc_fluctuation_Gamma_theta'] = 0.61
                superMCParameters['alpha'] = 0.14
            elif abs(ecm - 2760.) < 1e-6:
                superMCParameters['cc_fluctuation_Gamma_theta'] = 0.73
                superMCParameters['alpha'] = 0.118
            elif abs(ecm - 5020.) < 1e-6:
                superMCParameters['cc_fluctuation_Gamma_theta'] = 0.75
                superMCParameters['alpha'] = 0.118
            else:
                print(sys.argv[0], 
                      ": please specify cc_fluctuation_Gamma_theta for ecm = ",
                      ecm)
    elif model == 'MCKLN':
        superMCParameters['which_mc_model'] = 1
        superMCParameters['sub_model'] = 7
        if superMCParameters['cc_fluctuation_model'] != 0:
            superMCParameters['cc_fluctuation_model'] = 1
    else:
        print sys.argv[0], ': invalid initial model type', model
        print_help_message()
        sys.exit(1)

    superMCParameters['ecm'] = ecm
    superMCParameters['Aproj'] = nucleus_number_dict[collsys[0]]
    superMCParameters['Atarg'] = nucleus_number_dict[collsys[1]]

    # for checking
    #for x in superMCParameters.keys():
    #    print x + ': ' + str(superMCParameters[x])

    return

def generateAvgprofile(output_path, centrality_bounds, 
                       cut_type='total_entropy'):
    runRecord = open('./runRecord.dat', 'a')
    errRecord = open('./errRecord.dat', 'a')
    translate_centrality_cut(centrality_bounds, cut_type)
    cen_string = '%g-%g' %(centrality_bounds[0], centrality_bounds[1])
    option = form_assignment_string_from_dict(superMCParameters)
    cmd = './superMC.e' + option
    superMC_folder = path.abspath('./superMC')
    print cmd
    runRecord.write(cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=runRecord,
                         stderr=errRecord, cwd=superMC_folder)
    p.wait()

    # save files
    if not path.exists(output_path):
        print("create folder: ", output_path)
        makedirs(path.abspath(output_path))
    store_folder = output_path
    from_order = superMCParameters['average_from_order']
    to_order = superMCParameters['average_to_order']
    for iorder in range(from_order, to_order+1):
        if superMCParameters['use_sd']:
            filename_list = ['TATB_fromSd', 'sdAvg', 'rho_binary_fromSd',
                             'nuclear_thickness_TA_fromSd', 
                             'nuclear_thickness_TB_fromSd',
                             'spectator_density_A_fromSd',
                             'spectator_density_B_fromSd']
            for afile in filename_list:
                shutil.move(
                    path.join(superMC_folder, 'data',
                              '%s_order_%d_block.dat' % (afile, iorder)),
                    path.join(store_folder, '%s_order_%d_C%s.dat' 
                                            % (afile, iorder, cen_string)))
        if superMCParameters['use_ed']:
            filename_list = ['TATB_fromEd', 'edAvg', 'rho_binary_fromEd',
                             'nuclear_thickness_TA_fromEd', 
                             'nuclear_thickness_TB_fromEd',
                             'spectator_density_A_fromEd',
                             'spectator_density_B_fromEd']
            for afile in filename_list:
                shutil.move(
                    path.join(superMC_folder, 'data',
                              '%s_order_%d_block.dat' % (afile, iorder)),
                    path.join(store_folder, '%s_order_%d_C%s.dat' 
                                            % (afile, iorder, cen_string)))

    shutil.move('./runRecord.dat', path.join(store_folder, 'runRecord.dat'))
    shutil.move('./errRecord.dat', path.join(store_folder, 'errRecord.dat'))

def print_help_message():
    print "Usage : "
    print(color.bold
          + "./generateAvgprofile.py -ecm ecm "
          + "-cen cen_bounds"
          + "[-model model -collision_system collsys -cut_type cut_type]"
          + color.end)
    print "Usage of generateAvgprofile.py command line arguments: "
    print(color.bold + "-cen" + color.end
          + "   centrality bounds(%): "
          + color.purple + "20-30" + color.end)
    print(color.bold + "-ecm" + color.end
          + "   collision energy (GeV): "
          + color.purple + "7.7, 11.5, 19.6, 27, 39, 62.4, 200, 2760, 5500"
          + color.end)
    print(color.bold + "-cut_type" + color.end
          + "   centrality cut type: "
          + color.purple + color.bold + "total_entropy[default]" + color.end
          + color.purple + ", Npart" + color.end)
    print(color.bold + "-model" + color.end + " initial condition model: "
          + color.purple + color.bold + " MCGlb[default]" + color.end
          + color.purple + ", MCKLN" + color.end)
    print(color.bold + "-collision_system" + color.end
          + " type of collision system: "
          + color.purple + color.bold + " Pb+Pb[default]" + color.end
          + color.purple + ", Au+Au, Cu+Au, U+U, p+Pb, p+Au, d+Au, He+Au"
          + color.end)


if __name__ == "__main__":
    # set default values
    model = 'MCGlb'
    cut_type = 'total_entropy'
    collsys = 'Pb+Pb'.split('+')
    output_path = path.abspath('./RESULTS/initial_conditions')

    while len(sys.argv) > 1:
        option = sys.argv[1]
        del sys.argv[1]
        if option == '-model':
            model = str(sys.argv[1])
            del sys.argv[1]
        elif option == '-collision_system':
            collsys = str(sys.argv[1]).split('+')
            del sys.argv[1]
        elif option == '-cut_type':
            cut_type = str(sys.argv[1])
            del sys.argv[1]
            if cut_type not in ['total_entropy', 'Npart']:
                print sys.argv[0], ': invalid centrality cut type', cut_type
                print_help_message()
                sys.exit(1)
        elif option == '-cen':
            centrality_bounds = map(float, str(sys.argv[1]).split('-'))
            del sys.argv[1]
        elif option == '-ecm':
            ecm = float(sys.argv[1])
            del sys.argv[1]
        elif option == '-output':
            folder = float(sys.argv[1])
            output_path = path.join(path.abspath('./'), folder)
            del sys.argv[1]
        elif option == '-h':
            print_help_message()
            sys.exit(0)
        else:
            print sys.argv[0], ': invalid option ', option
            print_help_message()
            sys.exit(1)

    try:
        update_superMC_dict(model, ecm, collsys)
        generateAvgprofile(output_path, centrality_bounds, cut_type)
    except NameError:
        print_help_message()
        sys.exit(1)

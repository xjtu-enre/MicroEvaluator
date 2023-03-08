PROJECT_METRICS = ['score', 'SMQ', 'ODD', 'IDD', 'SPREAD', 'FOUCUS', 'ICF', 'ECF', 'REI']

MODULE_METRICS = ['scoh', 'scop', 'odd', 'idd', 'spread', 'focus', 'icf', 'ecf', 'rei', 'DSM']
TEMP_MODULE_METRICS = ['scoh', 'scop', 'odd', 'idd', 'DSM']

CLASS_METRICS = ['CIS', 'NOM', 'NOP', 'NAC', 'NDC', 'NOI', 'NOID', 'CTM', 'IDCC', 'IODD', 'IIDD', 'EDCC', 'c_FAN_IN',
                 'c_FAN_OUT', 'CBC', 'c_chm', 'c_chd', 'c_variablesQty', 'privateMethodsQty', 'protectedMethodsQty',
                 'staticMethodsQty', 'defaultMethodsQty', 'abstractMethodsQty', 'finalMethodsQty',
                 'synchronizedMethodsQty', 'publicFieldsQty', 'privateFieldsQty', 'protectedFieldsQty',
                 'staticFieldsQty', 'defaultFieldsQty', 'finalFieldsQty', 'synchronizedFieldsQty', 'RFC', 'NOF', 'NOVM',
                 'NOSI', 'TCC', 'LCC', 'LCOM', 'LOCM*', 'WMC', 'c_modifiers']

METHOD_METRICS = ['startLine', 'CBM', 'm_FAN_IN', 'm_FAN_OUT', 'IDMC', 'EDMC', 'IsOverride', 'OverridedQty',
                  'methodsInvokedQty', 'methodsInvokedLocalQty', 'methodsInvokedIndirectLocalQty', 'm_variablesQty',
                  'parametersQty', 'm_modifier']

PROJECT_METRICS_LEVEL = ['loc', 'loc_level', 'score', 'score_level', 'SMQ', 'SMQ_level', 'ODD', 'ODD_level', 'IDD',
                         'IDD_level',
                         'SPREAD', 'SPREAD_level',
                         'FOUCUS', 'FOUCUS_level', 'ICF', 'ICF_level', 'ECF', 'ECF_level', 'REI', 'REI_level',
                         'projectname',
                         'projectindex']

MODULE_METRIC_LEVEL = ['loc', 'loc_level', 'scoh',
                       'scoh_level', 'scop', 'scop_level', 'odd', 'odd_level', 'idd', 'idd_level',
                       'spread', 'spread_level', 'focus', 'focus_level', 'icf', 'icf_level', 'ecf', 'ecf_level', 'rei',
                       'rei_level', 'DSM', 'DSM_level', 'projectname',
                       'projectindex']

# MAX_METRICS：越大越好；MIN_METRICS:越小越好
MIN_METRICS = ['ODD', 'IDD', 'SPREAD', 'ECF', 'REI', 'scop', 'odd', 'idd', 'spread', 'ecf', 'rei', 'DSM']

MAX_METRICS = ['SMQ', 'FOUCUS', 'ICF', 'scoh', 'focus', 'icf', 'score']
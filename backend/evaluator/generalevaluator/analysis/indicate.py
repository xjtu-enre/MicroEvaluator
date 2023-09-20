import xlsxwriter
import numpy as np


def gen_xlsx(file_path, metric_change, modules_name, result):
    workbook = xlsxwriter.Workbook(file_path)
    bold = workbook.add_format({'bold': 1})
    _gen_change_sheet(workbook, bold, metric_change, modules_name)
    _gen_hotmap_sheet(workbook, bold, metric_change, modules_name)
    _gen_diff_sheet(workbook, bold, result)
    workbook.close()


def _gen_change_sheet(workbook, bold, metric_change, modules_name):
    worksheet1 = workbook.add_worksheet('变化幅度')
    # headings1 = ["module_name", "scoh", "scop", "odd", "idd", "DSM"]
    headings1 = ["module_name", "scoh", "scop", "odd", "idd", "spread", "focus", "icf", "ecf", "rei", "chm", "chd",
                 "DSM"]
    worksheet1.write_row('A1', headings1, bold)
    for index1 in range(0, len(metric_change)):
        worksheet1.write_string('A' + str(index1 + 2), modules_name[index1])
        for index2 in range(0, len(metric_change[index1])):
            worksheet1.write_number(index1 + 1, index2 + 1, metric_change[index1][index2])


def _gen_hotmap_sheet(workbook, bold, metric_change, modules_name):
    worksheet1 = workbook.add_worksheet('演化趋势')
    headings1 = ["module_name", "scoh", "scop", "odd", "idd", "DSC"]
    worksheet1.write_row('A1', headings1, bold)
    #这里metric_change长度为零，max和min获取不到数据报错
    max = np.amax(metric_change, axis=0)
    min = np.amin(metric_change, axis=0)
    for index1 in range(0, len(metric_change)):
        worksheet1.write_string('A' + str(index1 + 2), modules_name[index1])
        for index2 in range(0, len(metric_change[index1])):
            if index2 == 0:
                norm_value = float(
                    format((metric_change[index1][index2] - min[index2]) / (max[index2] - min[index2]), '.4f'))
            else:
                norm_value = float(
                    format((max[index2] - metric_change[index1][index2]) / (max[index2] - min[index2]), '.4f'))
            worksheet1.write_number(index1 + 1, index2 + 1, norm_value)
    worksheet1.conditional_format(1, 1, len(metric_change) + 1, 6,
                                  {'type': '3_color_scale', 'min_color': '#F08080', 'max_color': '#006400'})


def _gen_diff_sheet(workbook, bold, result):
    worksheet2 = workbook.add_worksheet('class_diff_result')
    headings2 = ["module_name", "scoh", "scop", "odd", "idd", "spread", "focus", "rei", "icf", "ecf", "DSM",
                 "class_name", "c_chm", "c_chd", "CBC",
                 "IDCC", "IODD", "IIDD",
                 "EDCC", "c_FAN_IN", "c_FAN_OUT", "NAC", "NDC↓", "NOP", "NOI", "NOID", "RFC", "NOSI", "CTM", "NOM",
                 "NOVM", "CIS", "privateMethodsQty", "protectedMethodsQty", "staticMethodsQty", 'defaultMethodsQty',
                 'abstractMethodsQty', 'finalMethodsQty', 'synchronizedMethodsQty', "TCC↑", "LCC↑", "LCOM",
                 "LCOM*",
                 "WMC", "c_variablesQty", "NOF", "publicFieldsQty", "privateFieldsQty", "protectedFieldsQty",
                 'staticFieldsQty', 'defaultFieldsQty↓', 'finalFieldsQty↓', 'synchronizedFieldsQty',
                 "c_modifiers", "status"]
    worksheet2.write_row('A1', headings2, bold)

    worksheet3 = workbook.add_worksheet('method_diff_result')
    headings3 = ["module_name", "class_name", "method_name", "CBM↓", "IDMC↑", "EDMC↓", "m_FAN_IN↓", "m_FAN_OUT↓",
                 "IsOverride", "OverridedQty",
                 "methodsInvokedQty↓", "methodsInvokedLocalQty↑", "methodsInvokedIndirectLocalQty↓", "m_variablesQty",
                 "parametersQty", "status"]
    worksheet3.write_row('A1', headings3, bold)

    index1 = 1
    index2 = 1
    for module_name in result:
        scoh = result[module_name]['scoh']
        scop = result[module_name]['scop']
        odd = result[module_name]['odd']
        idd = result[module_name]['idd']
        spread = result[module_name]['spread']
        focus = result[module_name]['focus']
        rei = result[module_name]['rei']
        icf = result[module_name]['icf']
        ecf = result[module_name]['ecf']
        DSM = result[module_name]['DSM']
        for class_name in result[module_name]['classes']:
            c_chm = result[module_name]['classes'][class_name]['c_chm']
            c_chd = result[module_name]['classes'][class_name]['c_chd']
            CIS = result[module_name]['classes'][class_name]['CIS']
            NOVM = result[module_name]['classes'][class_name]['NOVM']
            NOM = result[module_name]['classes'][class_name]['NOM']
            NAC = result[module_name]['classes'][class_name]['NAC']
            NDC = result[module_name]['classes'][class_name]['NDC']
            NOI = result[module_name]['classes'][class_name]['NOI']
            NOID = result[module_name]['classes'][class_name]['NOID']
            CTM = result[module_name]['classes'][class_name]['CTM']
            IDCC = result[module_name]['classes'][class_name]['IDCC']
            IODD = result[module_name]['classes'][class_name]['IODD']
            IIDD = result[module_name]['classes'][class_name]['IIDD']
            EDCC = result[module_name]['classes'][class_name]['EDCC']
            NOP = result[module_name]['classes'][class_name]['NOP']
            c_FAN_IN = result[module_name]['classes'][class_name]['c_FAN_IN']
            c_FAN_OUT = result[module_name]['classes'][class_name]['c_FAN_OUT']
            CBC = result[module_name]['classes'][class_name]['CBC']
            RFC = result[module_name]['classes'][class_name]['RFC']
            TCC = result[module_name]['classes'][class_name]['TCC']
            LCC = result[module_name]['classes'][class_name]['LCC']
            LCOM = result[module_name]['classes'][class_name]['LCOM']
            LCOM_norm = result[module_name]['classes'][class_name]['LOCM*']
            WMC = result[module_name]['classes'][class_name]['WMC']
            c_modifiers = result[module_name]['classes'][class_name]['c_modifiers']
            NOSI = result[module_name]['classes'][class_name]['NOSI']
            privateMethodsQty = result[module_name]['classes'][class_name]['privateMethodsQty']
            protectedMethodsQty = result[module_name]['classes'][class_name]['protectedMethodsQty']
            staticMethodsQty = result[module_name]['classes'][class_name]['staticMethodsQty']
            defaultMethodsQty = result[module_name]['classes'][class_name]['defaultMethodsQty']
            abstractMethodsQty = result[module_name]['classes'][class_name]['abstractMethodsQty']
            finalMethodsQty = result[module_name]['classes'][class_name]['finalMethodsQty']
            synchronizedMethodsQty = result[module_name]['classes'][class_name]['synchronizedMethodsQty']
            c_variablesQty = result[module_name]['classes'][class_name]['c_variablesQty']
            NOF = result[module_name]['classes'][class_name]['NOF']
            publicFieldsQty = result[module_name]['classes'][class_name]['publicFieldsQty']
            privateFieldsQty = result[module_name]['classes'][class_name]['privateFieldsQty']
            protectedFieldsQty = result[module_name]['classes'][class_name]['protectedFieldsQty']
            staticFieldsQty = result[module_name]['classes'][class_name]['staticFieldsQty']
            defaultFieldsQty = result[module_name]['classes'][class_name]['defaultFieldsQty']
            finalFieldsQty = result[module_name]['classes'][class_name]['finalFieldsQty']
            synchronizedFieldsQty = result[module_name]['classes'][class_name]['synchronizedFieldsQty']
            status = '' if 'status' not in result[module_name]['classes'][class_name] else \
                result[module_name]['classes'][class_name]['status']
            worksheet2.write_row(index1, 0,
                                 [module_name, scoh, scop, odd, idd, spread, focus, rei, icf, ecf, DSM, class_name,
                                  c_chm, c_chd, CBC, IDCC, IODD, IIDD, EDCC, c_FAN_IN, c_FAN_OUT, NAC,
                                  NDC, NOP, NOI, NOID, RFC, NOSI, CTM, NOM, NOVM, CIS, privateMethodsQty,
                                  protectedMethodsQty,
                                  staticMethodsQty, defaultMethodsQty, abstractMethodsQty, finalMethodsQty,
                                  synchronizedMethodsQty,
                                  TCC, LCC, LCOM, LCOM_norm, WMC, c_variablesQty,
                                  NOF, publicFieldsQty, privateFieldsQty, protectedFieldsQty, staticFieldsQty,
                                  defaultFieldsQty, finalFieldsQty, synchronizedFieldsQty,
                                  c_modifiers, status])
            for method_name in result[module_name]['classes'][class_name]['methods']:
                CBM = result[module_name]['classes'][class_name]['methods'][method_name]['CBM']
                m_FAN_IN = result[module_name]['classes'][class_name]['methods'][method_name]['m_FAN_IN']
                m_FAN_OUT = result[module_name]['classes'][class_name]['methods'][method_name]['m_FAN_OUT']
                m_variablesQty = result[module_name]['classes'][class_name]['methods'][method_name][
                    'm_variablesQty']
                IDMC = result[module_name]['classes'][class_name]['methods'][method_name]['IDMC']
                EDMC = result[module_name]['classes'][class_name]['methods'][method_name]['EDMC']
                IsOverride = result[module_name]['classes'][class_name]['methods'][method_name]['IsOverride']
                OverridedQty = result[module_name]['classes'][class_name]['methods'][method_name]['OverridedQty']
                methodsInvokedQty = result[module_name]['classes'][class_name]['methods'][method_name][
                    'methodsInvokedQty']
                methodsInvokedLocalQty = result[module_name]['classes'][class_name]['methods'][method_name][
                    'methodsInvokedLocalQty']
                methodsInvokedIndirectLocalQty = result[module_name]['classes'][class_name]['methods'][method_name][
                    'methodsInvokedIndirectLocalQty']
                parametersQty = result[module_name]['classes'][class_name]['methods'][method_name]['parametersQty']
                status = '' if 'status' not in result[module_name]['classes'][class_name]['methods'][method_name] else \
                    result[module_name]['classes'][class_name]['methods'][method_name]['status']
                worksheet3.write_row(index2, 0,
                                     [module_name, class_name, method_name, CBM, IDMC, EDMC,
                                      m_FAN_IN, m_FAN_OUT, IsOverride, OverridedQty, methodsInvokedQty,
                                      methodsInvokedLocalQty,
                                      methodsInvokedIndirectLocalQty,
                                      m_variablesQty, parametersQty, status])
                index2 += 1
            index1 += 1

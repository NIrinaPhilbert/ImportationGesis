import csv
import json
import pandas as pdexcel
import requests
import csv
import time
from datetime import datetime

uid_dataset = [{'tRM_CSB_Cons_Ext':'GSUZkSLVfZy'},{'tRM_CSB_CEXT_Utilisation_Prescription': 'GSUZkSLVfZy'}, {'tRM_CSB_Depistage_PEC': 'ToV2hqPjApV'},{'tRM_CSB_Depistage_PEC_ISTVIH': 'ToV2hqPjApV'}, {'tRM_CSB_SURVEILLANCE_NUT': 'fVhjtnQnFpu'},{'tRM_CSB_CONS_PRENAT': 'zVl3gPlL9HO'}, {'tRM_CSB_Maternite': 'zVl3gPlL9HO'},{'tRM_CSB_PEV_Enfants': 'zVl3gPlL9HO'}, {'tRM_CSB_PF': 'zVl3gPlL9HO'},{'tRM_CSB_DENTISTERI': 'kuBlaKJhV7W'}, {'tRM_CSB_Scolaire': 'QDJ43MNqsGP'},{'tRM_CSB_GES_STO_INTRANTS': 'NZ52X9Fw4lB'}, {'tRM_CSB_INTRANT_IST_VIH_NUT_PF': 'NZ52X9Fw4lB'},{'tRM_CSB_INTRANT_Tub_Lepre_MSR': 'NZ52X9Fw4lB'}, {'tRM_CSB_FANOME': 'NZ52X9Fw4lB'},{'tRM_CSB_FANOME': 'fYvqcl44zlF'}, {'tRM_CSB_GESTFIN': 'fYvqcl44zlF'}]
def browse_json_array(label, mylist):
    result = ''
    for value in mylist:
        try:
            result = value[label]
        except:
            pass
    return result

def get_uid_ou_dhis2(vcodegesis):
    uiddhis2 = ""

    csv_file = open('metadatagesis/fscsv.csv', 'r')
    csv_reader = csv.DictReader(csv_file)
    for line in csv_reader:
        codegesis = line['CODE_GESIS']
        codegesis = int(codegesis)
        # print("codegesis="+codegesis)
        if codegesis == vcodegesis:
            uiddhis2 = line['UID_DHIS2']
            print("uiddhis2=" + uiddhis2)

    return uiddhis2


def get_de_uid(tablename, vcolonnegesis, vcode):
    de_coc_uid = ""
    de_uid = ""
    if (tablename == 'tRM_CSB_Cons_Ext') or (tablename == 'tRM_CSB_Violences_traumatismes'):
        csv_file = open('metadatagesis/de_ce_traumatismeetviolencecsv.csv', 'r')

    else:
        csv_file = open('metadatagesis/decsv.csv', 'r')

    csv_reader = csv.DictReader(csv_file)
    for line in csv_reader:
        colonnefilemapping = str(line['AccessDBColumn'])
        if (vcode != ""):
            codefilemapping = str(line['Code'])
            if colonnefilemapping == vcolonnegesis and codefilemapping == vcode:
                de_uid = line['DataElementUId']
                coc_uid = line['CoCUid']
        else:
            if colonnefilemapping == vcolonnegesis:
                de_uid = line['DataElementUId']
                coc_uid = line['CoCUid']

    print("colonne gesis=" + vcolonnegesis + "code = " + vcode + "de_uid=" + de_uid)
    return de_uid


def get_co_uid(tablename, vcolonnegesis, vcode):
    coc_uid = ""
    if (tablename == 'tRM_CSB_Cons_Ext') or (tablename == 'tRM_CSB_Violences_traumatismes'):
        csv_file = open('metadatagesis/de_ce_traumatismeetviolencecsv.csv', 'r')

    else:
        csv_file = open('metadatagesis/decsv.csv', 'r')

    csv_reader = csv.DictReader(csv_file)
    for line in csv_reader:
        colonnefilemapping = line['AccessDBColumn']
        if (vcode != ""):
            codefilemapping = line['Code']
            if colonnefilemapping == vcolonnegesis and codefilemapping == vcode:
                de_uid = line['DataElementUId']
                coc_uid = line['CoCUid']
        else:
            if colonnefilemapping == vcolonnegesis:
                de_uid = line['DataElementUId']
                coc_uid = line['CoCUid']

    return coc_uid


def check_if_row_dataframe_has_value(df, index, colonneinutile, codegesisfs, uidoudhis2):
    res = False
    if (uidoudhis2 != ""):
        i = 0
        for col_name in df.columns:
            if pdexcel.isnull(dfexcel.at[index, col_name]) == False and col_name not in colonneinutile:
                i += 1
        if i > 0:
            res = True

    else:
        print("Existance uid dhis2 introuvable pour le code gesis", codegesisfs)
    return res


def get_periode_format_annee_mois(vAnnee, vMois):
    zAnneeMois = ""
    zMois = str(vMois)
    zAnnee = str(vAnnee)
    if len(zMois) == 1:
        zMois = "0" + zMois
    zAnneeMois = zAnnee + zMois
    return zAnneeMois

def importer_gesis_vers_dhis2(tablename,filedbname,ListNomColonneInutile):
    global dfexcel
    #dfexcel = pdexcel.read_excel(filedbname)
    dfexcel = pdexcel.read_csv(filedbname)
    dataSetID = browse_json_array(tablename, uid_dataset)
    for index,row in dfexcel.iterrows():
        codegesisfs = int(dfexcel.loc[index,'cCodeStru'])
        ou_uid = get_uid_ou_dhis2(codegesisfs)
        if(tablename == 'tRM_CSB_Cons_Ext'):
            vcode = dfexcel.loc[index, "cCode"]
        else:
            vcode = ""
        if check_if_row_dataframe_has_value(dfexcel,index,ListNomColonneInutile,codegesisfs,ou_uid) == True:
            print("\n\n")
            print("debut Iteration ligne")
            zPeriode = get_periode_format_annee_mois(dfexcel.loc[index,'cAnnee'],dfexcel.loc[index,'cPeriode'])
            print("periode="+zPeriode)
            for col_name in dfexcel.columns:

                #print("nomcolonne=",col_name,"valeur colonne=",value_colonne)
                #if dfexcel.loc[index, col_name] != "nan" and col_name not in ListNomColonneInutile:
                if pdexcel.isnull(dfexcel.at[index,col_name]) == False and col_name not in ListNomColonneInutile:
                    print("code gesis fs=",codegesisfs)
                    print("ou ="+ou_uid)
                    print("periode=",zPeriode)
                    print("ds ="+dataSetID)
                    value_colonne = int(dfexcel.loc[index, col_name])
                    print("nomcolonne=",col_name,"valeur colonne=",value_colonne)
                    de_uid = get_de_uid(tablename,col_name,vcode)
                    coc_uid = get_co_uid(tablename,col_name,vcode)
                    print("de_uid=",de_uid)
                    print("co_uid=",coc_uid)
                    print("fin colonne")
                    print("\n")
                    if(de_uid != "" and len(de_uid) ==11 and coc_uid != "" and len(coc_uid) ==11):
                        submit(de_uid,coc_uid,dataSetID,ou_uid,zPeriode,str(value_colonne))
                        time.sleep(1)

                else:
                    continue
            print("fin iteration colonne")
            terminerdataset(dataSetID,zPeriode,ou_uid)
            time.sleep(1)

        else:
            continue
        print("fin iteration ligne")

    print("============test====================")


def submit(de, co, ds, ou, pe, value):
    print("n\n")
    try:

        if de != "null":
            payload = {}
            url = "https://gesis.snis-sante.net/api/dataValues"
            url_for_custom_form = "https://gesis.snis-sante.net/api/dataValues?de=" + de + "&co=" + co + "&ds=" + ds + "&ou=" + ou + "&pe=" + pe + "&value=" + value
            # post = requests.post(url_custom_form, auth = (os.environ['v_param'] , os.environ['w_param']) , data = payload)
            post = requests.post(url_for_custom_form, auth=("Nirina", "Nirina@2017old"), data=payload)
            if post.status_code not in [200, 201]:
                print("status code:" + str(post.status_code) + "text sup " + post.text)
                raise ValueError("Data could not be submitted")
            else:
                print("data was submitted")


        else:
            url = "https://gesis.snis-sante.net/api/completeDataSetRegistrations"
            if value == "complete":
                completed = "true"
            else:
                completed = "false"
            my_json_data = {
                "completeDataSetRegistrations":
                    [
                        {
                            "dataSet": ds,
                            "period": pe,
                            "organisationUnit": ou,
                            "completed": completed
                        }
                    ]
            }
            # post = requests.post(url,json=my_json_data,auth = (os.environ['v_param'] , os.environ['w_param']))
            post = requests.post(url, json=my_json_data, auth=("Nirina", "Nirina@2017old"))

            try:
                print("post result :" + post.json())
            except:
                pass

            if post.status_code not in [200, 201]:
                raise ValueError("Data could not be completed")
            else:
                print("data was completed")
    except Exception as e:
        raise ValueError("Error de compilation" + str(e))
    print("\n\n")


def terminerdataset(ds, pe, ou):
    value = ""
    url = "https://gesis.snis-sante.net/api/completeDataSetRegistrations"
    if value == "complete":
        completed = "true"
    else:
        completed = "false"
    completed = "true"
    my_json_data = {
        "completeDataSetRegistrations":
            [
                {
                    "dataSet": ds,
                    "period": pe,
                    "organisationUnit": ou,
                    "completed": completed
                }
            ]
    }
    # post = requests.post(url,json=my_json_data,auth = (os.environ['v_param'] , os.environ['w_param']))
    post = requests.post(url, json=my_json_data, auth=("Nirina", "Nirina@2017old"))

    try:
        print("post result :" + post.json())
    except:
        pass

    if post.status_code not in [200, 201]:
        raise ValueError("Data could not be completed")
    else:
        print("data was completed")



# Press the green button in the gutter to run the script.
# ListNomColonneInutileTab3 = "cAnnee cCodeNiv cCodeStru cPeriode cTypeRapport cType cCode c$_Tot_M c$_Tot_F c$_Tot_NC"
ListNomColonneInutileTab18 = "cAnnee cCodeNiv cCodeStru cPeriode cTypeRapport"
filedbname = 'TestTab3.csv'
Tablename = 'tRM_CSB_Cons_Ext'
importer_gesis_vers_dhis2(Tablename, filedbname, ListNomColonneInutileTab18)
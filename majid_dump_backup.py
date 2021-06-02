import terminusdb_client as woql
from terminusdb_client import WOQLQuery
import pprint
import time
import pickle
import os
from utils_3store import *
pp = pprint.PrettyPrinter(indent=4) # for debugger

# updated below
variable_info = {}
type_info = {}
schema_declarations = []
property_name_info = {} # remap variable info: property_name -> (variable_name,scoped,type)
client = None
csv_file = None # handle to the open csv file we are creating

def dump_variables(polid,polity_name):
    global variable_info,type_info,client,csv_file
    ignore_pv = ['@context', '@id', '@type', 'rdfs:label', 'scm:original_PolID']
    ignore_pv_level2 = ['@context', '@type', 'rdfs:label', 'scm:original_PolID']
    value_options = ["scm:String","scm:DecimalRange","scm:IntegerRange","scm:EpistemicState","scm:GYearRange"]
    
    start_time = time.time()
    def dump_line(var_name,actual_value='',start_value='',end_value='',confidence_value='simple'):
        # Note that var_name could have embedded |
        csv_file.write(f"NGA|{polity_name}|{var_name}|{actual_value}|{start_value}|{end_value}|{confidence_value}|\n")

    # do a read_object to get all the data at once
    results = WOQLQuery().read_object(polid,'v:o').execute(client)
    #results = WOQLQuery().triple(polid,'v:Property_name','v:Values').execute(client) 
    #results = WOQLQuery().read_object('doc:Administrative_levels_Value_afdurrn_82','v:o').execute(client)
#    results2 = WOQLQuery().read_object('doc:Capital_Value_afdurrn_38','v:oo').execute(client)
    obj = results['bindings'][0]['o'] # bindings is a single list
    for pv,value in obj.items():
        if pv in ignore_pv:
            continue
        pv_stripped = pv.split(':')[1] # lose scm: prefix
        try:
            var_name, scoped, property_type = property_name_info[pv_stripped]
        except KeyError:
            # complain about missing pv data
            continue

        def unpack_value(value):
            Value_From = value
            Value_To = ''
            if 'Range' in property_type and Value_From[0] == '[':
                vs = Value_From.split(',')
                # strip []
                Value_From = vs[0][1:]
                Value_To   = vs[1][:-1]
            return Value_From,Value_To

        if scoped:
            if type(value) is dict:
                value = [value] # make iterable
            for value_dict in value:
                actual_value =''
                start_value = ''
                end_value = ''
                confidence_value = ''
                Value_From = ''
                Value_To = ''
                Date_From = ''
                Date_To = ''
                Confidence = 'simple'
                inferred = False
                for sp,sv in value_dict.items():
                    if sp in ignore_pv_level2:
                        continue
                    if sp == '@id':
                        #results_level2 = WOQLQuery().all(sv).execute(client) 
                        doc_name = sv.split(':')[1]
                        correct_doc_name ='terminusdb:///data/' + doc_name
                        #results_level2 = WOQLQuery().triple(correct_doc_name, 'v:ppp', 'v:vvv').execute(client)
                        results_2 = WOQLQuery().read_object(correct_doc_name, 'v:oo').execute(client)
                        obj_2 = results_2['bindings'][0]['oo'] # bindings is a single list
                        for pv_2, value_2 in obj_2.items():
                            if pv_2 in value_options:
                                actual_value = value_2['@value']
                            if pv_2 == 'scm:confidence':
                                confidence_value = value_2['scm:Confidence']['@value']
                                #if confidence_value == 'inferred':
                                    #inferred = True
                                    #confidence_value = 'inferred ' + 
                            if pv_2 == 'scm:start':
                                start_value = value_2['@value']
                            if pv_2 == 'scm:end':
                                end_value = value_2['@value']
                        #results_level2 = WOQLQuery().triple(sv, 'scm:IntegerRange', 'v:vv').execute(client)
                        #majid = results_level2['api:variable_names'][0]
                        #print('Hallo')
                dump_line(var_name,actual_value,start_value,end_value,confidence_value)
        else:
            # already have the values
            Value_From,Value_To = unpack_value(value['@value'])
            dump_line(var_name,Value_From,Value_To)

    print('Time for %s: %.1fs' % (polity_name,time.time() - start_time))


if __name__ == "__main__":
    # global client
    start_time = time.time()
    db_id = "seshat_jsb_mb_2_full" #  this gets its own scm: and doc: world
    client = woql.WOQLClient(server_url = "https://127.0.0.1:6363", insecure=True)
    client.connect(key="root", account="admin", user="admin")
    existing = client.get_database(db_id, client.account())
    if existing:
        client.set_db(db_id,client.account())
        schema_tuple = load_schema_info()
        if schema_tuple is None:
            sys.exit(0)

        schema_declarations, variable_info, type_info = schema_tuple
        # create inverted mapping
        for variable,entry in variable_info.items():
            property_name, scoped, property_type = entry
            property_name_info[property_name]  = (variable,scoped,property_type)
            
        csv_filename = 'seshat_4.csv';
        try:
            csv_file = open(csv_filename,"w")
        except IOError:
            print("ERROR: Could not open %s for writing." %  csv_filename)
            sys.exit(0)
        # probe for all polities
        results = WOQLQuery().triple('v:Polity_ID','original_PolID','v:PolityName').execute(client)
        for b in results['bindings']:
            polid = b['Polity_ID']
            polity_name = b['PolityName']['@value']
            if polid == 'http://terminusdb.com/schema/woql#code book':
                continue
            dump_variables(polid,polity_name);
        csv_file.close()
    else:
        print(f"Database {db_id} does not exist!")
    print('Execution time: %.1fs' % (time.time() - start_time))

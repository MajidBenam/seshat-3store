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
    start_time = time.time()
    def dump_line(var_name,Value_From,Value_To='',Date_From='',Date_To='',confidence='simple'):
        # Note that var_name could have embedded |
        csv_file.write(f"NGA|{polity_name}|{var_name}|{Value_From}|{Value_To}|{Date_From}|{Date_To}|simple||{confidence}|\n")

    # do a read_object to get all the data at once
    results = WOQLQuery().read_object(polid,'v:o').execute(client)
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
                Value_From = ''
                Value_To = ''
                Date_From = ''
                Date_To = ''
                Confidence = 'simple'
                inferred = False
                for sp,sv in value_dict.items():
                    if sp in ignore_pv:
                        continue
                    ssp = sp.split(':')[1] # lose scm: prefix
                    if ssp == 'start':
                        Date_From = pretty_year(sv['@value'])
                    elif ssp == 'end':
                        Date_To = pretty_year(sv['@value'])
                    elif ssp == 'confidence':
                        if type(sv) is dict:
                            sv = [sv] # make iterable
                        for sv_dict in sv:
                            for cp,cv in sv_dict.items():
                                if cp in ignore_pv:
                                    continue
                                sv = cv['@value']
                                if sv == 'inferred':
                                    inferred = True
                                else:
                                    Confidence = sv
                    else:
                        # must be the actual value property
                        Value_From,Value_To = unpack_value(sv['@value'])
                        # if 'Date' or 'gYear' in property_type: pretty_year(Value_From) pretty_year(Value_To)
                if inferred:
                    Value_From = 'inferred ' + Value_From
                dump_line(var_name,Value_From,Value_To,Date_From,Date_To,Confidence)
        else:
            # already have the values
            Value_From,Value_To = unpack_value(value['@value'])
            dump_line(var_name,Value_From,Value_To)

    print('Time for %s: %.1fs' % (polity_name,time.time() - start_time))


if __name__ == "__main__":
    # global client
    start_time = time.time()
    db_id = "seshat_jsb_mb" #  this gets its own scm: and doc: world
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
            
        csv_filename = 'seshat.csv';
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
            dump_variables(polid,polity_name);
        csv_file.close()
    else:
        print(f"Database {db_id} does not exist!")
    print('Execution time: %.1fs' % (time.time() - start_time))

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
    rdf_type = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'
    rdf_label = 'http://www.w3.org/2000/01/rdf-schema#label'
    start_time = time.time()
    def dump_line(var_name,Value_From,Value_To='',Date_From='',Date_To='',confidence='simple'):
        # Note that var_name could have embedded |
        csv_file.write(f"NGA|{polity_name}|{var_name}|{Value_From}|{Value_To}|{Date_From}|{Date_To}|simple||{confidence}|\n")

    # OK this is a complete hack to unpack results directly
    # There is probably something in Dataframe that does this better
    results = WOQLQuery().triple(polid,'v:Property_name','v:Values').execute(client) # get all the 'values' for any asserted property on this polity
    for b in results['bindings']:
        pv = b['Property_name']
        value = b['Values']
        if pv in [rdf_type, rdf_label, 'terminusdb:///schema#original_PolID']:
            continue
        pv_stripped = pv.split('#')[1] # lose scm: prefix (terminusdb:///schema#)
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
            # TODO can we collected all the scoped variables up and issue a single query to get them all?
            # TODO this will require sepearate variables of course for each scoped _Value instance
            # var_name -> (instance, prop_var, value_var) plus the qv query
            # still need to probe the enumerations though
            # unpack a scoped <property>_Value instance
            # NOTE: Attempted to do this in dump_csv_from_db2.py but the first major query for scoped variables for a pollity
            # hung the server for an hour and then crashed the AWS instance!
            results_vi = WOQLQuery().triple(value,'v:scoped_property','v:scoped_value').execute(client)
            Value_From = ''
            Value_To = ''
            Date_From = ''
            Date_To = ''
            Confidence = 'simple'
            inferred = False
            for sb in results_vi['bindings']:
                sp = sb['scoped_property']
                sv = sb['scoped_value']
                if sp in [rdf_type]:
                    continue
                ssp = sp.split('#')[1] # lose scm: prefix (terminusdb:///schema#)
                if ssp == 'start':
                    Date_From = pretty_year(sv['@value'])
                elif ssp == 'end':
                    Date_To = pretty_year(sv['@value'])
                elif ssp == 'confidence':
                    results_ci = WOQLQuery().triple(sv,'v:cp','v:cv').execute(client)
                    for cb in results_ci['bindings']:
                        cp = cb['cp']
                        cv = cb['cv']
                        if cp in [rdf_type]:
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
    existing = client.get_database(db_id, client.uid())
    if existing:
        client.db(db_id) # set the current db
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

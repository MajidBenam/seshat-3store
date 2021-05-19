
schema_declarations = {'combine_section_subsection_variable':False,
                       'csv_file':'equinox_tiny.csv'}    # equinox.csv
enumerations = [
    # This is only used in ScopedValue
    ("Confidence", "Confidence Tags", "Tags that can be added to values to indicate confidence in the value of some piece data", [
    ["inferred", "Inferred", "The value has been logically inferred from other evidence"], # This means that if we parse 'inferred present' we need to assert present as value w/ confidence inferred
    ["disputed", "Disputed", "The evidence is disputed - some believe this data to be incorrect"], # for {} values
    ["unknown", "Unknown", "It can be said with a high degree of confidence that it is not known whether the feature was present or absent in the context."],

    # Actually treat suspected like inferred...a type of confidence on, e.g., unknown below
    # uncertain is represented as alternative entries (triples) for the same date or as a numeric range (using a Range type)
    ]),

    # present/absent properties via ScopedEpistemicState
    ("EpistemicState", "Epistemic State", "The existence of a feature in the historical record", [
    ["absent", "Absent", "The feature was absent in this historical context"],
    ["present", "Present", "The feature was present in this historical context"],
    ["absent-to-present", "Absent To Present", "The feature was in transition from absent to present in this historical context"],
    ["present-to-absent", "Present To Absent", "The feature was in transition from present to absent in this historical context"],
    #["unknown", "Unknown", "It can be said with a high degree of confidence that it is not known whether the feature was present or absent in the context."],
    #["suspected_unknown", "Suspected unknown", "An RA asserts that it can be said with a high degree of confidence that it is not known whether the feature was present or absent in the context."],
    ]),
    ]

class_defns = [
    # Must have this since define_seshat_schema.py assumes this as a default domain for all properties
    ("PoliticalAuthority","Political Authority","A human social group with some autonomous political authority.", ["Organization"]),
    ("Polity","Polity","A polity is defined as an independent political unit. Kinds of polities range from villages (local communities) through simple and complex chiefdoms to states and empires. A polity can be either centralized or not (e.g., organized as a confederation). What distinguishes a polity from other human groupings and organizations is that it is politically independent of any overarching authority; it possesses sovereignty. Polities are defined spatially by the area enclosed within a boundary on the world map. There may be more than one such areas. Polities are dynamical entities, and thus their geographical extent may change with time. Thus, typically each polity will be defined by a set of multiple boundaries, each for a specified period of time. For prehistoric periods and for areas populated by a multitude of small-scale polities we use a variant called quasi-polity.",
     ["PoliticalAuthority"]),
    ]

topics = [
    ("GeneralVariables","General variables","",["Topic"]),
    ("SocialComplexityVariables","Social Complexity variables","",["Topic"]),
    ("HierarchicalComplexity","Hierarchical Complexity","",["SocialComplexityVariables"]),
    ("Professions","Professions","",["SocialComplexityVariables"]),
    ("SocialScale","Social Scale","",["SocialComplexityVariables"])
    ]

unscoped_properties = [
    ('original_PolID','xsd:string','Original Polity ID','The original name encoding on the wiki, preserving capitalization'),
    ]
scoped_properties = [
    ("Capital","String",["GeneralVariables"],"General variables||Capital",""),
    ("Duration","GYearRange",["GeneralVariables"],"General variables||Duration",""),
    ("religion","String",["GeneralVariables"],"General variables||Religion",""),
    ("Peak_Date","GYearRange",["GeneralVariables"],"General variables||Peak Date",""),
    ("GV_RA","String",["GeneralVariables"],"General variables||RA",""),
    ("Military_levels","IntegerRange",["HierarchicalComplexity"],"Social Complexity variables|Hierarchical Complexity|Military levels",""),
    ("Professional_soldiers","EpistemicState",["Professions"],"Social Complexity variables|Professions|Professional soldiers",""),
    ("Polity_territory","DecimalRange",["SocialScale"],"Social Complexity variables|Social Scale|Polity territory","")
    ]

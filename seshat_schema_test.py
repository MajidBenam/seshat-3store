# define a reduced scheme for insertion testing
class_defns = [
    ("PoliticalAuthority","Political Authority","A human social group with some autonomous political authority.",
     ["Organization"]),
    ("Polity","Polity","A polity is defined as an independent political unit. Kinds of polities range from villages (local communities) through simple and complex chiefdoms to states and empires. A polity can be either centralized or not (e.g., organized as a confederation). What distinguishes a polity from other human groupings and organizations is that it is politically independent of any overarching authority; it possesses sovereignty. Polities are defined spatially by the area enclosed within a boundary on the world map. There may be more than one such areas. Polities are dynamical entities, and thus their geographical extent may change with time. Thus, typically each polity will be defined by a set of multiple boundaries, each for a specified period of time. For prehistoric periods and for areas populated by a multitude of small-scale polities we use a variant called quasi-polity.",
     ["PoliticalAuthority"]),
    ]

topics = [
    # The subset needed for scoped variables below
    ("SocialComplexity","Social Complexity","Social Complexity Variables",["Topic"]),
    ("Scale","Scale","Dealing with Social Scale",["Topic"]),
    
    ("Public","Public","Dealing with public, collective characteristics, decision making, etc",["Topic"]),
    ("Politics","Politics","Dealing with political authority and organization",["Topic"]),
    ("InternalAffairs","Internal Affairs","Dealing with a group's internal organisation",["Topic"]),
    ("BureaucraticSystem","Bureaucratic System","A bureaucratic system, decisions are made by office holders",
     ["InternalAffairs", "Politics"]),
    ]

enumerations = [
    ("Confidence", "Confidence Tags", "Tags that can be added to values to indicate confidence in the value of some piece data", [
    ["inferred", "Inferred", "The value has been logically inferred from other evidence"], # This means that if we parse 'inferred present' we need to assert present as value w/ confidence inferred
    ["disputed", "Disputed", "The evidence is disputed - some believe this data to be incorrect"], # for {} values
    ["dubious", "Dubious", "The evidence is dubious - most believe this data to be incorrect"], # is this used?
    ["uncertain", "Uncertain", "The evidence has a high degree of uncertainty"] # is this used?
    ]),
    
    ("EpistemicState", "Epistemic State", "The existence of a feature in the historical record", [
    ["absent", "Absent", "The feature was absent in this historical context"],
    ["present", "Present", "The feature was present in this historical context"],
    ["unknown", "Unknown", "It can be said with a high degree of confidence that it is not known whether the feature was present or absent in the context."]
    ]),
    ]
# NOTE all types must be explicitly prefixed!
unscoped_properties = [
    ('original_PolID','xsd:string','Original Polity ID','The original name encoding on the wiki, preserving capitalization'),
    ("predecessor", "scm:PoliticalAuthority", "Preceding Polity",
     "The immediate preceding political authority. This code is based on the core region of the polity (not the NGA region).  E.g. Achaemenid Empire's core region was Persia, where they were preceded by the Median Empire."),
    ("successor", "scm:PoliticalAuthority", "Succeeding Polity",
     "Name. Only name it here and don't code the nature of change (it's coded on the page of the succeeding quasipolity). This code is based on the core region of the current polity (not the NGA region). E.g. Achaemenid Empire's core region was Persia, where they were succeeded by the Macedonian Empire."),
    ("peak_date","xsd:gYearRange","Peak date","Date of peak size"),
    ]
scoped_properties =[
    ("territory", "xdd:decimal", ["Scale", "SocialComplexity"],
     "Polity territory", "in km2"),
    ("longest_communication_distance", "xdd:integerRange", ["Scale", "SocialComplexity"],
     "Longest Communication Distance",
     "Distance in kilometers between the capital and the furthest provincial capital. The figure for the most direct land and/or sea route that was available is used. <p>As an alternative for prehistoric communities, it refers to the distance between largest quasi-capital and furthest village within the quasi-polity.</p>"),
    ("full_time_bureaucrats", "ScopedEpistemicState", ["Public", "BureaucraticSystem"],
     "Full-time bureaucrats",
     "Codes the presence of full-time specialist bureaucratic officials."),
    ]


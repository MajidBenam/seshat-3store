#  /Users/jsb/PsychoHistory/Turchin/Seshat/3store/seshat.py, Mon Feb 15 22:50:29 2021, Edit by jsb



import terminusdb_client as woql

from terminusdb_client import WOQLQuery

import pickle

import os

# DEAD MAJID? why is this here?  import fnmatch, glob, traceback, errno, sys, atexit, locale, imp, stat

import pprint

pp = pprint.PrettyPrinter(indent=4)



# What about Categories?



# kevin.js: initial un-numbered q

class_defns = [

    ("PoliticalAuthority","Political Authority","A human social group with some autonomous political authority.",

     ["Organization"]),

    ("Polity","Polity","A polity is defined as an independent political unit. Kinds of polities range from villages (local communities) through simple and complex chiefdoms to states and empires. A polity can be either centralized or not (e.g., organized as a confederation). What distinguishes a polity from other human groupings and organizations is that it is politically independent of any overarching authority; it possesses sovereignty. Polities are defined spatially by the area enclosed within a boundary on the world map. There may be more than one such areas. Polities are dynamical entities, and thus their geographical extent may change with time. Thus, typically each polity will be defined by a set of multiple boundaries, each for a specified period of time. For prehistoric periods and for areas populated by a multitude of small-scale polities we use a variant called quasi-polity.",

     ["PoliticalAuthority"]),

    ("QuasiPolity","Quasi-Polity","The polity-based approach is not feasible for those periods when a region is divided up among a multitude of small-scale polities (e.g., independent villages or even many small chiefdoms). In this instance we use the concept of 'quasi-polity'. Similarly, for societies known only archaeologically we may not be able to establish the boundaries of polities, even approximately. Quasi-polity is defined as a cultural area with some degree of cultural homogeneity (including linguistic, if known) that is distinct from surrounding areas. For example, the Marshall Islands before German occupation had no overarching native or colonial authority (chiefs controlled various subsets of islands and atolls) and therefore it was not a polity. But it was a quasi-polity because of the significant cultural and linguistic uniformity.<P>We collect data for the quasi-polity as a whole. This way we can integrate over (often patchy) data from different sites and different polities to estimate what the 'generic' social and political system was like. Data is not entered for the whole region but for a 'typical' polity in it. For example, when coding a quasi-polity, its territory is not the area of the region as a whole, but the average or typical area of autonomous groups within the NGA.",

     ["PoliticalAuthority"]),

    ("SubPolity", "Sub-Polity","A human social group that has some governing authority within a specific region or area of a polity - used to describe regional governments, etc.",

     ["PoliticalAuthority"]),



    ("SupraculturalEntity","Supra-Cultural Entity","Political Authority entities are often embedded within larger-scale cultural groupings of polities or quasipolities. These are sometimes referred to as 'civilizations'. For example, medieval European kingdoms were part of Latin Christendom. During the periods of disunity in China, warring states there, nevertheless, belonged to the same Chinese cultural sphere. Archaeologists often use 'archaeological traditions' to denote such large-scale cultural entities (for example, Peregrine's Atlas of Cultural Evolution). Note, 'supracultural entity' refers to cultural interdependence, and is distinct from a political confederation or alliance, which should be coded under 'supra-polity relations.'.",

     ["Organization"]),

    ("InterestGroup","Interest Group","An Interest Group (IG) is a social group that pursues some common interest, so that its members are united by a common goal or goals. Polities and religious cults are also interest groups, but this category is broader. It also includes ethnic groups, professional associations, warrior bands, solidarity associations, mutual aid societies, firms and banks (including their pre-modern variants), etc. The Interest Group is defined sociologically, not geographically. However, a geographic area, enclosed within a boundary, refering to its area of operation, may be associated with it in the same way as with a polity or a Religious System(RS). ",

     ["Organization"]),



    ("Settlement","Settlement","A semi-permanent or permanent human settlement",

     ["Organization"]),

    ("City","City","A concentrated human settlement, typically large",

     ["Settlement"]),

    ]



# kevin.js: q2

topics = [

    ("SocialComplexity","Social Complexity","Social Complexity Variables",["Topic"]),

    ("HierarchicalComplexity","Hierarchical Complexity","Encodes the number of levels in the most important hierarchies of a social system.",["SocialComplexity"]),

    ("Language","Language","Dealing with languages",["Topic"]), # missing Topic

    

    ("Politics","Politics","Dealing with political authority and organization",["Topic"]),

    ("Finance","Finance","Dealing with financial affairs",["Politics"]),

    ("Money","Money","Dealing with money",["Finance"]),

    ("Legal","Legal","Dealing with legal matters",["Politics"]),

    # BUG? no parent("Topic")?  used to mixin

    ("Economics","Economics","Dealing with Economics",),

    # JSB since Money inherits from Finance this is a noop; Economics is standalone

    # Finance inherits from Politics which inherits from Topic

    ("MonetarySystem","Monetary System","The System that produces money",["Finance", "Money", "Economics"]),

    

    ("Work","Work","Dealing with work",["Topic"]),

    ("Professions","Professions","A system of professional work",["Work"]),

    

    ("Food","Food","Dealing with food",["Topic"]),

    ("Agriculture","Agriculture","Dealing with agricultural matters",["Food"]),

    ("Fishing","Fishing","Dealing with fishing matters",["Food"]),

    ("Hunting","Hunting","Dealing with hunting matters",["Food"]),

    

    ("Ritual","Ritual","Dealing with rituals",["Topic"]),

    ("Burial","Burial","Burial Related Variables",

     ["Ritual"]),

    

    ("Military","Military","Dealing with Military matters",["Topic"]),

    ("Mining","Mining","Dealing with Mining and Mineral Extraction",["Topic"]),

    

    ("Minerals","Minerals","Dealing with Minerals",["Topic"]),

    ("Metals","Metals","Dealing with Metals",["Minerals"]),

    

    ("Transport","Transport","Dealing with Transport matters",["Topic"]),

    

    ("Communication","Communication","Dealing with Communication",["Topic"]),

    ("Science","Science","Dealing with scientific method",["Topic"]),

    ("MeasurementSystem","Measurement System","Textual evidence of a measurement system: measurement units are named in sources (e.g. pound, aroura). Archaeological evidence includes finding containers of standard volume, etc. ('inferred present')",

     ["Science", "SocialComplexity"]),

    

    ("Writing","Writing","Dealing with written word",["Topic"]),

    ("WritingSystem","Writing System","Relating to different types of a writing system.",

     ["Writing", "SocialComplexity"]),

    ("Literature","Literature","Dealing with literature",["Topic"]),

    ("WritingGenre","Written Genres","Relating to different types of written material.",

     ["Literature","SocialComplexity"]),

    

    ("Ideology","Ideology","Dealing with Ideological matters",["Topic"]),

    ("Religion","Religion","Relating to religion",

     ["Ideology"]),

    

    ("Construction","Construction","Dealing with Construction matters",["Topic"]),

    ("Housing","Housing","Dealing with housing matters",

     ["Construction"]),

    ("Building","Building","A specific building", # see kevin.js: q11! this was some inlined code.  Why?

     ["Construction"]),

    ("Infrastructure","Infrastructure","The built infrastructure that a society depends upon",

     ["Construction"]),

    ("PostalSystem","Postal System","A system for sending physical messages",

     ["Communication", "Infrastructure", "Transport"]),

    ("SpecialSites","Special Sites","Sites not associated with residential areas. This position is primarily useful for coding archaneologically known societies.",

     ["Infrastructure", "Construction"]),

    ("TransportInfrastructure","Transport Infrastructure","Relating to Transport Infrastructure.",

     ["Transport", "Infrastructure"]),

    

    ("Scale","Scale","Dealing with Social Scale",["Topic"]),

    

    ("Public","Public","Dealing with public, collective characteristics, decision making, etc",["Topic"]),

    ("SpecializedBuildings","Specialized Buildings","Polity-owned: includes owned by the community, or the state.",

     ["Public", "Construction"]),

    

    ("Private","Private","Dealing with private, individual or factional decision making",["Topic"]),

    

    ("InternalAffairs","Internal Affairs","Dealing with a group's internal organisation",["Topic"]),

    ("BureaucraticSystem","Bureaucratic System","A bureaucratic system, decisions are made by office holders",

     ["InternalAffairs", "Politics"]),

    

    ("ExternalAffairs","External Affairs","Dealing with a group's external affairs",["Topic"]),

    ("SupraPolityRelations","Supra-Polity Relations","Relating to relationships between polities.",

     ["ExternalAffairs"]),

    

    ("Resilience","Resilience","Resilience Related Variables",["Topic"]),

    ("Naval","Naval","Dealing with naval matters",["Topic"]),

    ("Entertainment","Entertainment","Dealing with entertainment",),

    ]



# kevin.js: q5+q6

# Note calls to normaliseID() below

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



    ("DegreeOfCentralization", "Degree of Centralization", "An indication of how centralized a political authority was", [

    ["unknown_centralization", "Unknown", "Unknown Centralization"],

    ["loose", "Loose", "The central government exercises a certain degree of control, especially over military matters and international relations. Otherwise the regional rulers are left alone"],

    ["quasipolity", "Quasi-polity", "Used for a situation where the poliity is in reality many politically independent groups"],

    ["no_centralization",  "None", "There is no centralised system"],

    ["confederated_state", "Confederated State", "Regions enjoy a large degree of autonomy in internal (regional) government. In particular, the regional governors are either hereditary rulers, or are elected by regional elites or by the population of the region; and regional governments can levy and dispose of regional taxes."],

    ["nominal", "Nominal", "Regional rulers pay only nominal allegiance to the overall ruler and maintain independence on all important aspects of governing, including taxation and warfare. (example: Japan during the Sengoku period)"],

    ["unitary_state", "Unitary State", "Regional governors are appointed and removed by the central authorities, taxes are imposed by, and transmitted to the center"],

    ]),



    ("SupraPolityRelations", "Supra-Polity Relations", "The relationship between a polity and its paramount power", [

    ["vassalage","Vassalage", "A central government exercises a certain degree of control, especially over military matters and international relations. Otherwise the polity is left alone."],

    ["no_supra_polity_relations", "None", "No relations with any supracultural entity"],

    ["nominal_allegiance", "Nominal Allegiance", "Paying only nominal allegiance to the overall ruler and maintaining independence on all important aspects of governing, including taxation and warfare."],

    ["personal_union", "Personal Union", "The focal polity is united with another, or others, as a result of a dynastic marriage"],

    ["alliance", "Alliance", "Belongs to a long-term military-political alliance of independent polities (long-term refers to more or less permanent relationship between polities extending over multiple years"],

    ["unknown_supra_polity_relations", "Unknown", "Unknown Relations"]

    ]),



    ("PoliticalEvolution", "Political Evolution", "How a political authority evolves into another one", [

    ["assimilation", "Cultural Assimilation", "Assimilation by another political authority in the absence of substantial population replacement"],

    ["continuity", "Continuity", "Gradual change without any discontinuity"],

    ["elite_migration","Elite Migration", "The preceding elites were replaced by new elites coming from elsewhere"],

    ["population_migration", "Population Migration", "Evidence for substantial population replacement"],

    ["unknown_evolution", "Unknown", "Unknown Evolution"]

    ]),



    ("IncomeSource", "Income Source", "A source of income", [

    ["governed_population", "Governed Population", "The official directly collects tribute from the population (for example, the kormlenie system in Medieval Russia)"],

    ["land", "Land", "Living off land supplied by the state."],

    ["state_salary", "State Salary", "can be paid either in currency or in kind (e.g., koku of rice)."],

    ["no_income", "No Income", "The state officials are not compensated (example: in the Republican and Principate Rome the magistrates were wealthy individuals who served without salary, motivated by prestige and social or career advancement)"],

    ["unknown_income", "Unknown", "Unknown source of income"]

    ]),

    ]



# kevin.js: q9

# These are the low-level (castable) types we use in boxed classes, e.g., scm:String has property String that holds an xsd:string

# Note capitalization!

boxed_basic_types = [

    # ("xsd:boolean", "Boolean","True or False"),

    ("xsd:string", "String","Any text or sequence of characters"),

    ("xsd:decimal", "Decimal", "A decimal number."),

    ("xsd:integer", "Integer", "A simple number."),

    ("xsd:positiveInteger", "Positive Integer", "A simple number greater than 0."),

    ("xsd:anyURI", "Any URI", "Any URl. An xsd:anyURI value."),

    ("xsd:gYear", "Year", "A particular Gregorian 4 digit year YYYY - negative years are BCE."),

    ("xdd:gYearRange", "Year", "A 4-digit Gregorian year, YYYY, or if uncertain, a range of years YYYY-YYYY."),

    ("xdd:integerRange", "Integer", "A simple number or range of numbers."),

    ("xdd:decimalRange", "Decimal Number", "A decimal value or, if uncertain, a range of decimal values."),

    ("xdd:dateRange", "Date Range", "A date or a range of dates YYYY-MM-DD"),

    ]



# kevin.js: q11

# that is, they are direct properties that point to instances of classes or are raw datatypes

unscoped_properties = [

    ("predecessor", "PoliticalAuthority", "Preceding Polity",

     "The immediate preceding political authority. This code is based on the core region of the polity (not the NGA region).  E.g. Achaemenid Empire's core region was Persia, where they were preceded by the Median Empire."),

    ("successor", "PoliticalAuthority", "Succeeding Polity",

     "Name. Only name it here and don't code the nature of change (it's coded on the page of the succeeding quasipolity). This code is based on the core region of the current polity (not the NGA region). E.g. Achaemenid Empire's core region was Persia, where they were succeeded by the Macedonian Empire."),

    ("best_building", "Building", "Most Costly Building",

     "The most impressive or costly building constructed by the political authority"),

    ("references", "CitedWork", "References",

     "The References from the wiki"),

    # JSB this requires that scm:String is already defined

    ("provenance_note", "xsd:string", "Provenance Note", "Provenance Notes"),

    ("peak_date","xsd:gYear","Peak date","Date of peak size"),

    ]



# kevin.js: q15

scoped_properties =[

    ("territory", "xdd:decimal", ["Scale", "SocialComplexity"],

     "Polity territory", "in km2"),

    ("longest_communication_distance", "xdd:integerRange", ["Scale", "SocialComplexity"],

     "Longest Communication Distance",

     "Distance in kilometers between the capital and the furthest provincial capital. The figure for the most direct land and/or sea route that was available is used. <p>As an alternative for prehistoric communities, it refers to the distance between largest quasi-capital and furthest village within the quasi-polity.</p>"),

    ("fastest_travel", "xdd:decimalRange", ["Transport"],

     "Fastest Individual Communication",

     "This is the fastest time (in days) an individual can travel from the capital city to the most outlying provincial capital (if one exists), usually keeping within the boundaries of the polity. This might be by ship, horse, horse relay, or on foot, or a combination."),

    ("population", "xdd:integerRange", ["Scale", "SocialComplexity"],

     "Population",

     "Estimated population; can change as a result of a political authority adding/losing new territories or by population growth/decline within a region"),

    ("capital_city", "xsd:string", ["SocialComplexity"],

     "Capital City",

     "The city where the ruler spends most of his or her time. If there was more than one capital, all are included. Note that the capital may be different from the largest city (see below). <p>'Capital' may be difficult to code for archaeologically known societies. If there is reasonable basis to believe that the largest known settlement was the seat of the ruler it is coded as capital. Archaeologists are able to recognize special architectural structures, such as a ceremonial centres and some kind of citadels or palaces. These features could be recognized with certainty after a careful study of the whole region and the settlement network. If such an inference cannot be made, this variable is coded as unknown (again, the largest settlement is coded elsewhere).</p>"),

    ("degree_of_centralization", "ScopedDegreeOfCentralization", ["SocialComplexity"],

     "Degree of Centralization",

     "How centralized was power in this political authority?"),

    ("largest_settlement_population", "xdd:integerRange", ["SocialComplexity", "Scale"],

     "Largest Settlement Population",

     "Population count of the largest settlement within the entity. <p>Note that the largest settlement could be different from the capital. Where possible, the dynamics (that is, how population changed during the temporal period of the polity) are included in the notes. Note that we are also building a city database - this will be merged into that eventually.</p>"),

    ("linguistic_family", "xsd:string", ["SocialComplexity","Language"],

     "Linguistic Family",

     "The Linguistic family or families that the main languages belonged to. https://en.wikipedia.org/wiki/List_of_language_families"),

    ("alternative_names", "xsd:string", [],

     "Alternative names",

     "Names used in the historical literature or common names used by the inhabitants"),

    ("territorial_area", "xdd:integerRange", [],

     "Territorial Area",

     "The area in squared kilometers of the entity's territory."),

    ("utm_zone", "xsd:string", [],

     "UTM Zone",

     "The UTM Zone that corresponds most directly with the entity - e.g. where the polity's capital city is located, or the location of the NGA. For more see: http://www.dmap.co.uk/utmworld.htm"),

    ("lang", "xsd:string", ["Language"],

     "Language",

     "The language(s) are listed that were generally used for administration, religion, and military affairs. The languages spoken by the majority of the population are also listed, if different from the above."),

    ("peak", "xdd:integerRange", [],

     "Peak Date",

     "The period when the political power was at its peak, whether militarily, in terms of the size of territory controlled, or the degree of cultural development. This variable has a subjective element, but typically historians agree when the peak was."),

    ("centralization", "ScopedDegreeOfCentralization", ["InternalAffairs"],

     "Degree of Centralization",

     "How centralized was power in this political authority?"),

    ("supra_polity_relations", "ScopedSupraPolityRelations", ["ExternalAffairs"],

     "Supra-polity relations",

     "What was the relationship between this political authority and larger / higher order power."),

    ("predecessor_relationship", "ScopedPoliticalEvolution", [],

     "Relationship to Preceding Polity",

     "How this political authority evolved from its predecessor."),

    ("supracultural_entity", "xsd:string", ["ExternalAffairs"],

     "Supra-cultural Entity",

     "Political Authorities can be embedded within larger-scale cultural groupings of polities or quasipolities. These are sometimes referred to as civilizations. For example, medieval European kingdoms were part of Latin Christendom. During the periods of disunity in China, warring states there, nevertheless, belonged to the same Chinese cultural sphere. Archaeologists often use archaeological traditions to denote such large-scale cultural entities (for example, Peregrines Atlas of Cultural Evolution).  Note supracultural entity refers to cultural interdependence, and is distinct from a political confederation or alliance, which is coded under supra-polity relations."),

    ("supracultural_scale", "xdd:integerRange", ["Scale"],

     "Supra-cultural Scale",

     "An estimate of the area encompassed by the supracultural entity - in km squared."),

    ("monetary_articles", "ScopedEpistemicState", ["MonetarySystem", "SocialComplexity"],

     "Articles",

     "Articles with use-value used for exchange and trade, e.g. axes, cattle, grain."),

    ("debt_and_credit", "ScopedEpistemicState", ["MonetarySystem", "SocialComplexity"],

     "Debt and credit",

     "Commercial and market debt and credit structures that take physical form, e.g. a contract on parchment (not just verbal agreements)"),

    ("foreign_coins", "ScopedEpistemicState", ["MonetarySystem", "SocialComplexity"],

     "Foreign Coins",

     "Coins minted by some external polity are used for exchange"),

    ("indigenous_coins", "ScopedEpistemicState", ["MonetarySystem", "SocialComplexity"],

     "Indigenous Coins",

     "Coins minted by local authority are in use for exchange"),

    ("paper_currency", "ScopedEpistemicState", ["MonetarySystem", "SocialComplexity"],

     "Paper Currency",

     "Currency notes or other kind of fiat currency"),

    ("precious_metals", "ScopedEpistemicState", ["MonetarySystem", "SocialComplexity"],

     "Precious Metals",

     "Bullion: non-coined silver, gold, platinum."),

    ("stores_of_wealth", "ScopedEpistemicState", ["MonetarySystem", "SocialComplexity"],

     "Stores of Wealth",

     "Special places for storing wealth: (example: hoard, chest for storing valuables, treasury room). Note for the future: perhaps should separate these into individual variables."),

    ("monetary_tokens", "ScopedEpistemicState", ["MonetarySystem", "SocialComplexity"],

     "Tokens",

     "Tokens used for exchange and trade, e.g. cowrie shells."),

    ("courts", "ScopedEpistemicState", ["Legal", "SocialComplexity"],

     "Courts",

     "Encodes the historical presence of buildings specialized for legal proceedings only."),

    ("formal_legal_code", "ScopedEpistemicState", ["Legal", "SocialComplexity"],

     "Formal Legal Code",

     "Codes the historical presence of a formal legal code. Usually, but not always written down. If not written down, it is coded as 'present' when a uniform legal system is established by oral transmission (e.g., officials are taught the rules, or the laws are announced in a public space)."),

    ("judges", "ScopedEpistemicState", ["Legal", "SocialComplexity"],

     "Judges",

     "Codes the historical presence of specialist judges"),

    ("professional_lawyers", "ScopedEpistemicState", ["Legal", "SocialComplexity"],

     "Professional Lawyers",

     "Encodes the historical presence of specialist professional lawyers."),

    ("cost", "xdd:decimalRange", ["Scale", "SocialComplexity"],

     "Cost",

     "cost in people-years.", "Building"),

    ("extent", "xdd:decimalRange", ["Scale", "SocialComplexity"],

     "Extent",

     "Length of building along longest axis in metres", "Building"),

    ("height", "xdd:decimalRange", ["Scale", "SocialComplexity"],

     "Height",

     "Height of building in metres", "Building"),

    ("administrative_levels", "xdd:integerRange", ["HierarchicalComplexity"],

     "Administrative Levels",

     "Number of levels in the administrative hierarchy. <p>An example of hierarchy for a state society could be (5) the overall ruler, (4) provincial/regional governors, (3) district heads, (2) town mayors, (1) village heads. Note that unlike in settlement hierarchy, the people hierarchy is coded here. </p> <p>Archaeological polities are usually coded as 'unknown', unless experts can identified ranks of chiefs or officials independently of the settlement hierarchy.</p> <p>Note: Often there are more than one concurrent administrative hierarchy. In the example above the hierarchy refers to the territorial government. In addition, the ruler may have a hierarchically organized central bureaucracy located in the capital. For example, (4)the overall ruler, (3) chiefs of various ministries, (2) mid-level bureaucrats, (1) scribes and clerks. In the narrative paragraph detail what is known about both hierarchies. The machine-readable code should reflect the largest number (the longer chain of command). </p>"),

    ("military_levels", "xdd:integerRange", ["HierarchicalComplexity"],

     "Military Levels",

     "Number of levels in the military hierarchy. <p>Starts with the commander-in-chief and works down to the private (level 1).</p> <p>Even in primitive societies such as simple chiefdoms it is often possible to distinguish at least two levels : a commander and soldiers. A complex chiefdom would be coded as having three levels. The presence of warrior burials might be the basis for inferring the existence of a military organization. (The lowest military level is always the individual soldier).</p>"),

    ("religious_levels", "xdd:integerRange", ["HierarchicalComplexity"],

     "Religious Levels",

     "Number of levels in the religious hierarchy. <P>Starts with the head of the official cult (if present) and works down to the local priest (level 1).</p>"),

    ("settlement_levels", "xdd:integerRange", ["HierarchicalComplexity"],

     "Settlement Levels",

     "This variable records the hierarchy of not just settlement sizes, but also their complexity as reflected in different roles they play within the (quasi)polity. As settlements become more populous they acquire more complex functions: transportational (e.g. port); economic (e.g. market); administrative (e.g. storehouse, local government building); cultural (e.g. theatre); religious (e.g. temple), utilitarian (e.g. hospital), monumental (e.g. statues, plazas). <p>Example: (6) Large City (monumental structures, theatre, market, hospital, central government buildings) (5) City (market, theatre, regional government buildings) (4) Large Town (market, administrative buildings) (3) Town (administrative buildings, storehouse)) (2) Village (shrine) (1) Hamlet (residential only).</p> <p>In the narrative annotations, the different levels and their functions are listed. A Crude estimate of population sizes is included. For example, Large Town (market, temple, administrative buildings): 2,000-5,000 inhabitants. </p>"),

    ("bureaucrat_income_source", "ScopedIncomeSource", ["Public", "BureaucraticSystem"],

     "Bureaucrat Income Source",

     "Encodes the primary sources of income for professional bureaucrats / administrators"),

    ("examination_system", "ScopedEpistemicState", ["Public", "BureaucraticSystem"],

     "Examination System",

     "Codes the presence of an official Examination System. The paradigmatic example is the Chinese imperial system."),

    ("full_time_bureaucrats", "ScopedEpistemicState", ["Public", "BureaucraticSystem"],

     "Full-time Bureaucrats",

     "Codes the presence of full-time specialist bureaucratic officials."),

    ("government_buildings", "ScopedEpistemicState", ["BureaucraticSystem", "Public", "Infrastructure"],

     "Government Buildings",

     "Codes the historical presence of specialized government administration buildings. These buildings are distinct from the ruler\'s palace and could be used for document storage, registration offices, minting money, etc. Defense structures also are not included here."),

    ("merit_promotion", "ScopedEpistemicState", ["BureaucraticSystem", "Public"],

     "Merit Promotion",

     "Codes the historical presence of merit promotion. <i>Present</i> means there were regular, institutionalized procedures for promotion based on performance. When exceptional individuals are promoted to the top ranks, in the absence of institutionalized procedures, this does not count (it is encoded elsewhere)."),

    ("military_officers", "ScopedEpistemicState", ["Professions", "Military"],

     "Military Officers",

     "Full-time specialist military officers."),

    ("professional_soldiers", "ScopedEpistemicState", ["Professions", "Military"],

     "Soldiers",

     "Full-time specialist paid soldiers."),

    ("priests", "ScopedEpistemicState", ["Professions", "Religion"],

     "Priesthood",

     "Codes the presence of full-time specialist religious officials."),

    ("bureaucrats", "ScopedEpistemicState", ["Professions", "BureaucraticSystem"],

     "Full-time Bureaucrats",

     "Codes the presence of full-time specialist bureaucratic officials."),

    ("public_buildings", "ScopedEpistemicState", ["Public", "SpecializedBuildings"],

     "Communal Buildings",

     "This encodes the historical presence of Communal buildings. It distinguishes between settlements that consist of only private households (coded 'absent') and settlements where there are communal buildings which could be used for a variety of uses (coded 'present')."),

    ("special_houses", "ScopedEpistemicState", ["SpecializedBuildings"],

     "Special Purpose Houses",

     "Encodes the historical presence of houses that were used in a distinctive or special manner. This code reflects differentiation between houses."),

    ("symbolic_building", "ScopedEpistemicState", ["SpecializedBuildings"],

     "Symbolic Buildings",

     "Encodes the historical presence of specialized purely symbolic buildings. <P>These are non-utilitarian constructions that display symbols, or are themselves symbols of the community or polity (or a ruler as a symbol of the polity). Examples include Taj Mahal mausoleum, Trajan\'s Column, Ashoka\'s Pillars, Qin Shih Huang\'s Terracota Army, the Statue of Liberty. Has to be constructed by humans, so sacred groves or mountains are not symbolic buildings. A palace is also not a symbolic building, because it has other, utilitarian functions (houses the ruler).</P>"),

    ("fun_houses", "ScopedEpistemicState", ["SpecializedBuildings", "Entertainment"],

     "Entertainment Buildings",

     "Encodes the historical presence of specialist entertainment buildings. These include theaters, arenas, race tracks."),

    ("libraries", "ScopedEpistemicState", ["SpecializedBuildings",  "Writing"],

     "Knowledge / Information Buildings",

     "Encodes the historical presence of specialist information / knowledge buildings. These include astronomic observatories, libraries, and museums."),

    ("utilities", "ScopedEpistemicState", ["SpecializedBuildings", "Infrastructure"],

     "Utilitarian Public Buildings",

     "Encodes the historical presence of public utilities. Typical examples include aqueducts, sewers, and granaries (which are also included as separate variables). In the narrative annotations, examples of utilitarian buildings and the most impressive/costly/large ones are included."),

    ("emporia", "ScopedEpistemicState", ["SpecializedBuildings"],

     "Trading Emporia",

     "Encodes the historical presence of trading settlements characterised by their peripheral locations, on the shore at the edge of a polity, a lack of infrastructure (typically those in Europe contained no churches) and often of a short-lived nature. They include isolated caravanserai along trade routes."),

    ("enclosures", "ScopedEpistemicState", ["SpecializedBuildings"],

     "Enclosure",

     "Encodes the historical presence of 'enclosures': a clearly demarcated special-purpose area. It can be separated from surrounding land by earthworks (including banks or ditches), walls, or fencing. It may be as small as a few meters across, or encompass many hectares. It is non-residential, but could serve numerous purposes, both practical (animal pens) as well as religious and ceremonial."),

    ("other_site", "ScopedEpistemicState", ["SpecializedBuildings"],

     "Other Site",

     "Encodes the historical presence of specialised non-residential sites. A description of the site is provided in the notes."),

    ("roads", "ScopedEpistemicState", ["Transport"],

     "Roads",

     "Encodes the historical presence of roads that were either built or maintained by the political authority."),

    ("bridges", "ScopedEpistemicState", ["Transport"],

     "Bridges",

     "Encodes the historical presence of bridges that were either built or maintained by the political authority."),

    ("canals", "ScopedEpistemicState", ["Transport"],

     "Canals",

     "Encodes the historical presence of canals or artificial waterways that were built or maintained by the political authority."),

    ("ports", "ScopedEpistemicState", ["Transport", "Naval"],

     "Ports",

     "Encodes the historical presence of ports that were either built or maintained by the political authority. These include river ports. Direct historical or archaeological evidence of Ports is absent when no port has been excavated or all evidence of such has been obliterated. Indirect historical or archaeological data is absent when there is no evidence that suggests that the polity engaged in maritime or riverine trade, conflict, or transportation, such as evidence of merchant shipping, administrative records of customs duties, or evidence that at the same period of time a trading relation in the region had a port (for example, due to natural processes, there is little evidence of ancient ports in delta Egypt at a time we know there was a timber trade with the Levant). When evidence for the variable itself is available the code is 'present.' When other forms of evidence suggests the existence of the variable (or not) the code may be 'inferred present' (or 'inferred absent'). When indirect evidence is <i>not</i> available the code will be either absent, temporal uncertainty, suspected unknown, or unknown."),

    ("length_unit", "ScopedEpistemicState", ["MeasurementSystem"],

     "Length",

     "Encodes the historical presence of a standard way of measuring length. For example: feet, miles, kilometers, inches"),

    ("area_unit", "ScopedEpistemicState", ["MeasurementSystem"],

     "Area",

     "Encodes the historical presence of a standard way of measuring areas. For example: squared feet, hectares"),

    ("volume_unit", "ScopedEpistemicState", ["MeasurementSystem"],

     "Volume",

     "Encodes the historical presence of a standard way of measuring volume. For example: pint, litre"),

    ("weight_unit", "ScopedEpistemicState", ["MeasurementSystem"],

     "Weight",

     "Encodes the historical presence of a standard way of measuring weight. For example: pounds, kilograms"),

    ("time_unit", "ScopedEpistemicState", ["MeasurementSystem"],

     "Time",

     "Encodes the historical presence of a standard way of measuring time. A natural unit such as 'day' doesn\'t qualify. Nor does a vague one like 'season'. Archaeological evidence is a clock (e.g., sundial)"),

    ("geometrical_unit", "ScopedEpistemicState", ["MeasurementSystem"],

     "Geometrical",

     "Encodes the historical presence of a standard way of measuring geometries - for example: degrees."),

    ("advanced_unit", "ScopedEpistemicState", ["MeasurementSystem"],

     "Other",

     "More advanced measurements: temperature, force, astronomical."),

    ("mnemonics", "ScopedEpistemicState", ["WritingSystem"],

     "Mnemonic Devices",

     "Marks that serve as memory devices that help people recall larger pieces of information"),

    ("non_written_records", "ScopedEpistemicState", ["WritingSystem"],

     "Non-written Records",

     "Knoweldge representation systems that do not use writing - using color, material, etc to convey meaning. e.g., quipu https://en.wikipedia.org/wiki/Quipu"),

    ("script", "ScopedEpistemicState", ["WritingSystem"],

     "Script",

     "A system for writing symbols that have meaning attached to them. (note that if written records are present, then so is script by defintion)"),

    ("written_records", "ScopedEpistemicState", ["WritingSystem"],

     "Written Records",

     "More than short and fragmentary inscriptions, such as found on tombs or runic stones. There must be several sentences strung together, at the very minimum. For example, royal proclamations from Mesopotamia and Egypt qualify as written records;"),

    ("non_phonetic", "ScopedEpistemicState", ["WritingSystem"],

     "Non-phonetic Writing",

     "this refers to the kind of script - non-phonetic scripts do not represent the sound of the word but attach symbols to the meaning."),

    ("phonetic", "ScopedEpistemicState", ["WritingSystem"],

     "Phonetic Alphabet",

     "this refers to the kind of script - phonetic scripts have alphabets with letters and combinations of letters which represent sounds."),

    ("lists", "ScopedEpistemicState", ["WritingGenre"],

     "Lists and Tables",

     "Written lists, tables and classifications (e.g. debt lists, tax-lists...)"),

    ("calendar", "ScopedEpistemicState", ["WritingGenre"],

     "Calendar",

     "Written calendar or dating system"),

    ("sacred_texts", "ScopedEpistemicState", ["WritingGenre", "Religion"],

     "Sacred Texts",

     "Sacred Texts originate from supernatural agents (deities), or are directly inspired by them."),

    ("religious_literature", "ScopedEpistemicState", ["WritingGenre", "Religion"],

     "Religious Literature",

     "Religious literature differs from the sacred texts. For example, it may provide commentary on the sacred texts, or advice on how to live a virtuous life."),

    ("manuals", "ScopedEpistemicState", ["WritingGenre"],

     "Practical Literature",

     "Practical guides and manuals to help people do useful stuff. For example manuals on agriculture, military, cooking, etc"),

    ("history", "ScopedEpistemicState", ["WritingGenre"],

     "History",

     "Written history existed"),

    ("philosophy", "ScopedEpistemicState", ["WritingGenre"],

     "Philosophy",

     "Written philosophical treatises"),

    ("science", "ScopedEpistemicState", ["WritingGenre", "Science"],

     "Science",

     "Written scientific works, including mathematics, natural sciences, social sciences"),

    ("fiction", "ScopedEpistemicState", ["WritingGenre"],

     "Fiction",

     "Written fictional works - including poetry, novels, short-stories, etc.  (poetry will be factored out in future versions of the codebook)."),

    ("couriers", "ScopedEpistemicState", ["PostalSystem"],

     "Couriers",

     "Full-time professional couriers."),

    ("post_offices", "ScopedEpistemicState", ["PostalSystem", "SpecializedBuildings"],

     "Postal Stations",

     "Specialized buildings exclusively devoted to the postal service."),

    ("private_mail", "ScopedEpistemicState", ["PostalSystem"],

     "General Service",

     "A postal service that not only serves the ruler\'s needs, but carries mail for private citizens."),

    ("fortifications", "ScopedEpistemicState", ["Military", "Infrastructure", "Resilience"],

     "Fortifications",

     "IV-5-7. Fortifications."),

    ("sewage", "ScopedEpistemicState", ["Infrastructure", "Resilience"],

     "Sewage",

     "IV-5-4. Sewage management systems"),

    ("irrigation", "ScopedEpistemicState", ["Infrastructure", "Public"],

     "Irrigation Systems",

     "Encodes the historical presence of irrigation systems."),

    ("potable_water", "ScopedEpistemicState", ["Infrastructure", "Public"],

     "Drinking Water Supply",

     "Encodes the historical presence of systems to supply drinking water to the public."),

    ("markets", "ScopedEpistemicState", ["Infrastructure"],

     "Markets",

     "Encodes the historical presence of markets."),

    ("siloes", "ScopedEpistemicState", ["Infrastructure", "Construction", "Food"],

     "Food Storage Sites",

     "The historical presence of specialized structures (grain siloes...) for storing food."),

    ("special_sites", "ScopedEpistemicState", ["Infrastructure"],

     "Special Sites",

     "The types of special sites that are associated with the polity - primarily useful for coding archaneologically known societies."),

    ("ceremonial_sites", "ScopedEpistemicState", ["Ritual", "Infrastructure"],

     "Ceremonial Site",

     "Encodes the historical presence of sites that were specifically used for ceremonies."),

    ("burial_sites", "ScopedEpistemicState", ["Burial", "Infrastructure"],

     "Burial Site",

     "Encodes the historical presence of burial sites, dissociated from settlement habitation, with monumental features."),

    ("mines", "ScopedEpistemicState", ["Mining", "Infrastructure"],

     "Mine or Quarry",

     "Encodes the historical presence of mines or quarries within the political authority."),

    ("irrigation", "ScopedEpistemicState", ["Infrastructure", "Public"],

     "Irrigation Systems",

     "Encodes the historical presence of irrigation systems."),

    ("potable_water", "ScopedEpistemicState", ["Infrastructure", "Public"],

     "Drinking Water Supply",

     "Encodes the historical presence of systems to supply drinking water to the public."),

    ("markets", "ScopedEpistemicState", ["Infrastructure"],

     "Markets",

     "Encodes the historical presence of markets."),

    ("siloes", "ScopedEpistemicState", ["Infrastructure", "Construction", "Food"],

     "Food Storage Sites",

     "The historical presence of specialized structures (grain siloes...) for storing food."),

    ("special_sites", "ScopedEpistemicState", ["Infrastructure"],

     "Special Sites",

     "The types of special sites that are associated with the polity - primarily useful for coding archaneologically known societies."),

    ("ceremonial_sites", "ScopedEpistemicState", ["Ritual", "Infrastructure"],

     "Ceremonial Site",

     "Encodes the historical presence of sites that were specifically used for ceremonies."),

    ("burial_sites", "ScopedEpistemicState", ["Burial", "Infrastructure"],

     "Burial Site",

     "Encodes the historical presence of burial sites, dissociated from settlement habitation, with monumental features."),

    ("mines", "ScopedEpistemicState", ["Mining", "Infrastructure"],

     "Mine or Quarry",

     "Encodes the historical presence of mines or quarries within the political authority."),

    ]



# From woql_query.py

def fixed_generate_choice_list(

    cls=None,

    clslabel=None,

    clsdesc=None,

    choices=None,

    graph=None,

    parent=None,

    ):

    if not graph:

        graph = WOQLQuery()._graph

    clist = []

    if False:

        # ensure that _: is part of the current @context per Kevin/Gavin

        # some deep OWL or rdf thing

        # without it you get an API error, e.g.: api:message":"Error: key_has_unknown_prefix(\"_:Confidence\")

        # This code fails...it needs to be done such that each time the WOQLQuery() constructor is called

        # the _: prefix is available wherever it needs to be...

        # this might work if we cache qu = WOQLQuery() and then replace all the WOQLQuery() calls here with qu

        try:

            ctxt = WOQLQuery()._cursor['@context'] # access current context

        except KeyError:

            # missing

            ctxt = {}

            WOQLQuery()._context(ctxt) # update cursor context

        ctxt['_'] = '_' # ensure _: is available

        

    if ":" not in cls:

        listid = "_:" + cls

    else:

        listid = "_:" + cls.split(":")[1]

    lastid = listid

    wq = WOQLQuery().add_class(cls, graph).label(clslabel)

    if clsdesc:

        wq.description(clsdesc)

    if parent:

        wq.parent(parent)

    confs = [wq]

    for i in range(len(choices)): #  JSB range(len(choices)) rather than choices

        if not choices[i]:

            continue

        if type(choices[i]) is list:

            chid = choices[i][0]

            clab = choices[i][1]

            desc = choices[i][2] if len(choices[i]) >= 3 else False

        else:

            chid = choices[i]

            clab = utils.label_from_url(chid)

            desc = False

        cq = WOQLQuery().insert(chid, cls, graph).label(clab)

        if desc:

            cq.description(desc)

        confs.append(cq)

        if i < len(choices) - 1:

            nextid = listid + "_" + str(i) # JSB str()

        else:

            nextid = "rdf:nil"

        clist.append(WOQLQuery().add_quad(lastid, "rdf:first", chid, graph))

        clist.append(WOQLQuery().add_quad(lastid, "rdf:rest", nextid, graph))

        lastid = nextid

    oneof = WOQLQuery().woql_and(

        WOQLQuery().add_quad(cls, "owl:oneOf", listid, graph), *clist)

    return WOQLQuery().woql_and(*confs, oneof)



def normaliseID(raw, _type):

    """Ensure all ids in raw have a (proper) prefix.

    """

    schema_prefix = "scm:"  # In case we decide to call it 'seshat:' or something

    if _type == "id":

        if type(raw) is list:

            ids = []

            for p in raw:

                ids.append(normaliseID(p,'id'))

            return ids

        else:

            bits = raw.split(":")

            if len(bits) > 1:

                return raw # already prefixed

            else:

                return schema_prefix + raw

    if _type == "type":

        # coerce something like 'xdd:IntegerRange' to our 'scm:integerRange' type, which has different case conventions

        bits = raw.split(":")

        if len(bits) > 1:

            raw = bits[1]

        return schema_prefix + raw[0].upper() + raw[1:]

    return raw



# Build several dictionaries

# wiki section/subsection names to schema names

# wiki variable names to schema names and their underlying xdd/xsd types

# save as pkl with same version number

def create_seshat_schema(client):

    """The query which creates the schema

    Parameters - it uses variables rather than the fluent style as an example

    ==========

    client : a WOQLClient() connection

    """

    # presummably this goes into 'scm:' by default

    # what do I do if I wanted to name the schema to publish it (like bike_scm)?

    # presummably I would have to then dump it in rdf format and make it available on the web for parsing by other 3store apps right?

    # what do I use to load an external schema?



    # This controls 'debugging mode' True to incrementally execute, False to append and execute once

    execute_incrementally = True

    def process_q(q,message=None):

        if execute_incrementally:

            if message is not None:

                print(message)

            q.execute(client,commit_msg=message)

        return q

    

    # kevin.js: initial un-numbered q

    q = WOQLQuery().doctype("Organization",

                            label="Organization",

                            description="A human organization of any type - has the capacity to act as a unit, in some sense").abstract()

    all_q = process_q(q,"Organization")

    for class_defn in class_defns:

        if len(class_defn) == 4:

            name,label,description,parents = class_defn

        else:

            name,label,description = class_defn

            parents = []

        # name = normaliseID(name,'id')

        q = WOQLQuery().doctype(name,label=label,description=description)

        for parent in parents:

            # parent = normaliseID(parent,'id')

            q.parent(parent)

        all_q = all_q + process_q(q,name)



    # kevin.js: q2

    q = WOQLQuery().doctype("Topic",

                            label="Topic Class",

                            description="A class that represents a topic").abstract()

    all_q = all_q + process_q(q,"Topic")

    for topic in topics:

        if len(topic) == 4:

            name,label,description,parents = topic

        else:

            name,label,description = topic

            parents = []

        # name = normaliseID(name,'id')

        q = WOQLQuery().doctype(name,label=label,description=description)

        for parent in parents:

            # parent = normaliseID(parent,'id')

            q.parent(parent)

        all_q = all_q + process_q(q,name)



    q = WOQLQuery().doctype("CitedWork",label="Cited Work").property("remote_url", "xsd:anyURI")

    all_q = all_q + process_q(q,'CitedWork')

    

    # kevin.js: q7

    # wrap this expression in parens to make indentation nice and stop python from complaining

    q = (WOQLQuery().add_class("Note").label("A Note on a value").description("Editorial note on the value")

         .property("citation", "scm:CitedWork").label("Citation").description("A link to a cited work")

         .property("quotation", "xsd:string").label("Quotation").description("A quotation from a work"))

    all_q = all_q + process_q(q,'Note')





    # wrap this expression in parens to make indentation nice and stop python from complaining

    q = (WOQLQuery().add_class("ScopedValue")

         .abstract()                          

         .property("start", "xdd:integerRange").label("From").description("The start of a time range")

         .property("end", "xdd:integerRange").label("To").description("The end of a time range")

         .property("confidence", "scm:Confidence").label("Confidence").description("Qualifiers of the confidence of a variable value")

         .property("notes", "scm:Note") .label("Notes").description("Editorial notes on values"))

    all_q = all_q + process_q(q,'ScopedValue')



    # This call defines the boxed datatypes we use, e.g., scm:IntegerRange whose 'type' is xdd:IntegerRange

    # kevin.js: q9

    if False:

        q = (WOQLQuery().add_class("scm:Box")

             .label("Box Class")

             .description("A class that represents a boxed datatype")

             .abstract())

        all_q = all_q + process_q(q,'scm:Box')

        

    for bbt in boxed_basic_types:

        datatype,label,description = bbt

        Datatype = normaliseID(datatype,'type') # get the scm: prefixed, upper-cased name

        # TODO build a dict Datatype -> datatype

        qt = WOQLQuery().add_class(Datatype).label(label)

        # no parent, e.g., scm:Box, needs to be added to qt so far (except it bundles all our types together)



        # so scm:Integer is a class with a property scm:Integer that permits an xsd:integer

        # when when we mixin scm:Integer into a <prop>_Value class, and it has type xsd:integer

        # we know that we need to

        # idgen() for a new _Value instance

        # insert('v:property_Value',<scoped_value_class>

        # cast('v:csv_data_value','xsd:integer','v:CastValue),

        # add_triple('v:property_Value','scm:Integer','v:CastValue') << lookup

        qp = (WOQLQuery().add_property(Datatype,datatype)

              .domain(Datatype)

              .label(label)

              .description(description))

        q = WOQLQuery().woql_and(qt,qp)

        all_q = all_q + process_q(q,Datatype)

              

    # kevin.js: q5+q6

    # Is this class needed for generate_choice_list()?

    # JSB probably not.  it is like Box which just serves to organize the different types

    # q = WOQLQuery().doctype("Enumerated",label="Enumerated Type",description="A type that consists of a fixed set of choices")

    # all_q = all_q + process_q(q,"Enumerated")



    for etype in enumerations:

        name,label,description,choices = etype

        scoped_name = "Scoped" + name

        name = normaliseID(name,'id')

        scoped_name = normaliseID(scoped_name,'id')

        # choices = normaliseID(choices,'id')

        for choice in choices:

            choice[0] = normaliseID(choice[0],'id')

        if False:  # DEBUG since fixed_generate_choice_list() uses prefix _:, which causes upset

            # q = WOQLQuery().generate_choice_list(name,clslabel=label,clsdesc=description,choices=choices)

            qus = fixed_generate_choice_list(cls=name,clslabel=label,clsdesc=description,choices=choices)

            qsc = fixed_generate_choice_list(cls=scoped_name,clslabel=label,clsdesc=description,choices=choices)

        else:

            # HACK define the class but not its structure

            qus = WOQLQuery().doctype(name,label=label,description=description) 

            qsc = WOQLQuery().doctype(scoped_name,label=label,description=description)

        q = WOQLQuery().woql_and(qus,qsc)

        all_q = all_q + process_q(q,scoped_name)





    # kevin.js: q11

    for p in unscoped_properties:

        if len(p) == 5:

            npid, nptype, label, description, domain = p

        else:

            npid, nptype, label, description = p

            domain = "scm:PoliticalAuthority"

        nptype = normaliseID(nptype, "type") # convert raw types to our boxed types

        npid = normaliseID(npid, "id")

        q = WOQLQuery().add_property(npid, nptype).label(label).description(description).domain(domain)

        all_q = all_q + process_q(q,npid)



    # kevin.js: q15

    for p in scoped_properties:

        if len(p) == 6:

            npid, nptype, parents, label, description, domain = p

        else:

            npid, nptype, parents, label, description = p

            domain = "scm:PoliticalAuthority"

        parents = normaliseID(parents,"id")

        parents.append("scm:ScopedValue") # these seshat polity properties always inherit from ScopedValue -- that is where datatypes and values are stored

        nptype = normaliseID(nptype, "type") # convert to our boxed types

        npid = normaliseID(npid, "id")

        parents.append(nptype)

        newclass = npid + "_Value"



        q = WOQLQuery().add_class(newclass).label(label).description(description)

        for parent in parents:

            q.parent(parent)

        all_q = all_q + process_q(q,newclass)

        q = WOQLQuery().add_property(npid, nptype).label(label).description(description).domain(domain)

        all_q = all_q + process_q(q,npid)



    if not execute_incrementally:

        execute_incrementally = True # force execution

        process_q(all_q,"Defining the Seshat Schema")



    return True



if __name__ == "__main__":

    db_id = "seshat_jsb_mb" #  this gets its own scm: and doc: world

    client = woql.WOQLClient(server_url = "https://127.0.0.1:6363", insecure=True)

    client.connect(key="root", account="admin", user="admin")

    existing = client.get_database(db_id, client.uid())

    if not existing:

        # any need to supply prefixes?  what about include_schema=True so you don't have to reload it?

        client.create_database(db_id, accountid="admin", label = "Seshat Databank Jim", description = "Create a graph with historical data")

        # TODO pickle.dump((wiki_to_ss,wiki_to_var_type),fh)

    else:

        # updating data (and/or the schema)

        # TODO results = pickle.load(fh); wiki_to_ss,wiki_to_var_type = results

        client.db(db_id)



    if not existing: # or True to call each time

        create_seshat_schema(client)



    seshat_dir =  '/Users/jsb/PsychoHistory/Turchin/Seshat'

    scrape_file = 'most_recent_seshat_scrape.csv'; delimiter='|'

    scrape_file = os.path.join(os.path.abspath(seshat_dir), scrape_file)

    #parse_seshat_csv(client,scrape_file,delimiter)




-- 0. Insert data into PP_NET table
INSERT INTO portown.pp_net (id,ds,dsl,net_level_id,parent_net_id) VALUES
	 (37564,'GP','Medicaid - SC',1,NULL),
	 (28,'Centene','Centene',2,NULL),
	 (29,'TX','Texas',3,28),
	 (6236,'IL','Illinois',3,28),
	 (30,'GA','Georgia',3,28),
	 (6336,'CA','California',3,28),
	 (6237,'NLH','NextLevelHealth',4,6236),
	 (6337,'MediCal','Medical',4,6337),
	 (14068,'SUPVEN','Superior Vendors',4,29),
	 (32,'SUP','Superior',4,29);
INSERT INTO portown.pp_net (id,ds,dsl,net_level_id,parent_net_id) VALUES
	 (7719,'CENSUP','Cenpatico Superior',4,29),
	 (33,'PS','Peach State',4,30),
	 (7676,'CENPS','Cenpatico Peach State',4,30),
	 (35,'GP','START',5,32),
	 (2441,'GPC','CHIP',5,32),
	 (2442,'GPR','CHIP RSA',5,32),
	 (38,'FC','Star Health',5,32),
	 (37,'PSHP','Peach State Health Plan',5,33),
	 (14629,'DNULVLGA','DNU Legacy VL GA',5,33),
	 (7677,'BH','Cenpatico Peach State Health Plan',5,7676);
INSERT INTO portown.pp_net (id,ds,dsl,net_level_id,parent_net_id) VALUES
	 (7722,'BHK','Cenpatico STAR Kids',5,7719),
	 (7726,'KD','Cenpatico CHIP',5,7719),
	 (7728,'KDBH','Cenpatico STAR',5,7719),
	 (14837,'DLIB','DNU LIBNXT',5,6237),
	 (6238,'EN','NextLevel Health Medicaid',5,6237),
	 (7017,'CV','Cal Viva',5,6337),
	 (7018,'CM','Cal Molina',5,6337),
	 (7019,'CD','Cal Dental',5,6337),
	 (14097,'SHSE','Superior Health plan - Starkids ESI',5,14068),
	 (14089,'SHCE','Superior Health plan - CHIPRSA ESA',5,14068);
INSERT INTO portown.pp_net (id,ds,dsl,net_level_id,parent_net_id) VALUES
	 (14087,'SHCR','Superioc Health plan - CHIP ESI',5,14068),
	 (14776,'TXDQMD','DentaQuest - Star Medicaid TX - VAL',6,35),
	 (14342,'ACCUSMTX','Accu Reference Star Medicaid TX',6,35),
	 (13899,'CMKMDTX','Caremark Star Medicaid - TX',6,35),
	 (14552,'CPLSMTX','CPL Star Medicaid TX',6,35),
	 (14549,'CPLCIPTX','CPL CHIP TX - VAL',6,2441),
	 (14337,'ACCUCHIPTX','AccuReference CHIP TX - VAL',6,2441),
	 (14339,'BIOCHIPTX','BioReference CHIP TX - VAL',6,2441),
	 (14421,'QSTCHIPTX','Quest CHIP TX - VAL',6,2441),
	 (14518,'LCCCHIPTX','Labcorp CHIP TX - VAL',6,2441);
INSERT INTO portown.pp_net (id,ds,dsl,net_level_id,parent_net_id) VALUES
	 (46,'FC','TX Star Health Foster Care',6,38),
	 (3258,'USFCTX','US Script - Star Health Foster Care TX',6,38),
	 (13900,'CMKFCTX','Caremark - Star Health Foster Care TX',6,38),
	 (14341,'ACCUUSHFCTX','Accu Reference Star health Foster Care TX',6,38),
	 (47,'MD','Medicaid GA',6,37),
	 (331,'CCPSHP','Care Centrix PSHP',6,37),
	 (332,'DDPSHP','Denta Quest PSHP',6,37),
	 (334,'USPSHP','US Script PSHP',6,37),
	 (14600,'OPTPSHP','Opticare PSHP GA - VAL',6,37),
	 (333,'OCPSHP','Opticare PSHP',6,14629);
INSERT INTO portown.pp_net (id,ds,dsl,net_level_id,parent_net_id) VALUES
	 (14045,'ESIGA','ESI PSHP',6,14629),
	 (3781,'CPLPSHP','Clinical Pathology Lan - PSHP',6,14629),
	 (6408,'LCPPSHP','Labcorp PSHP',6,14629),
	 (8417,'ACCUPSHP','Accu Reference PSHP',6,14629),
	 (6406,'QUPSHP','Quest PSHP',6,14629),
	 (7678,'MD','Cenpatico Medicaid GA',6,7677),
	 (7723,'KD','Cenpatico TX CHIP',6,7722),
	 (6257,'MD','NextLevel Health Medicaid',6,6238),
	 (6577,'NIANXT','NIA Next Level Health',6,6238),
	 (6579,'ENVVSNNXT','Envolve Vision Next Level Health',6,6238);
INSERT INTO portown.pp_net (id,ds,dsl,net_level_id,parent_net_id) VALUES
	 (6796,'LIBNXT','Liberty Dental Next Level Health',6,6238),
	 (14764,'LIBDNEXTIL','Liberty Dental Next Level Health - VAL',6,6238),
	 (7727,'MD','Cenpatico TX Star',6,7726),
	 (7729,'FC','Cenpatico TX Foster Care',6,7728),
	 (14698,'STARKD','ESI Superior Health Plan - STARKID - VAL',6,14069),
	 (7039,'CV','CV CalViva Standard',6,7017),
	 (7040,'VE','CV CalViva Expansion',6,7017),
	 (7056,'VK','CV CalViva Kaiser',6,7017),
	 (14595,'OPTCVCA','Opticare Calviva CA - VAL',6,7017),
	 (15043,'ASHCA','Ash Calviva CA - VAL',6,7017);
INSERT INTO portown.pp_net (id,ds,dsl,net_level_id,parent_net_id) VALUES
	 (14694,'CHIPRSA','ESI Superior Health Plan - CHIPRSA - VAL',6,14089),
	 (14693,'ESICHIP','ESI Superior Health Plan - CHIP - VAL',6,14087),
	 (7037,'CM','CM Molina Standard',6,7018),
	 (7038,'CG','CM Molina Expansion',6,7018),
	 (7036,'TL','Medi-Cal Dental',6,7019);

-- 1. Insert data into FMG_ATTRIBUTE_TYPES table
INSERT INTO portown.fmg_attribute_types (id,metatype,description) VALUES
	 (100640,'PROV_ACR_ACCRED','ACR Accreditation'),
	 (101277,'PROV_AAAASF_ACCRED','AAAASF Accreditation'),
	 (100638,'PROV_AAAHC_ACCRED','AAAHC Accreditation'),
	 (101278,'PROV_AASM_ACCRED','Provider AASM Accred'),
	 (502,'PROV_NPI','Provider NPI'),
	 (100073,'PROV_MEDICARE_ID','Provider Medicare Id');


-- 2. Insert data into FMG_ATTRIBUTE_FIELDS table
INSERT INTO portown.fmg_attribute_fields (id,attribute_id,fmgcode,field_name,"datatype") VALUES
	 (101143,100640,'YES_NO','ACR Accred?','string'),
	 (102935,100640,NULL,'Validation Date','date'),
	 (101141,100640,NULL,'Effective Date','date'),
	 (102915,100640,NULL,'Expiration Date','date'),
	 (104380,100640,'ACR_ACCRED_LEVEL','Accred level','string'),
	 (101955,101277,'YES_NO','AAAASF Accreditation','string'),
	 (102775,101277,NULL,'Validation Date','date'),
	 (101956,101277,NULL,'Effective Date','date'),
	 (102795,101277,NULL,'Expiration Date','date'),
	 (101136,100638,'YES_NO','AAAHC Accreditation','string');
INSERT INTO portown.fmg_attribute_fields (id,attribute_id,fmgcode,field_name,"datatype") VALUES
	 (102835,100638,NULL,'Validation Date','date'),
	 (101137,100638,NULL,'Effective Date','date'),
	 (102815,100638,NULL,'Expiration Date','date'),
	 (104381,100638,'AAHC_ACCRED_LEVEL','Accred level','string'),
	 (102856,101278,NULL,'endDate','date'),
	 (101957,101278,NULL,'AASM Accreditation','string'),
	 (101958,101278,NULL,'effectiveDate','date'),
	 (709,502,NULL,'endDate','date'),
	 (706,502,NULL,'number','string'),
	 (708,502,NULL,'effectiveDate','date');
INSERT INTO portown.fmg_attribute_fields (id,attribute_id,fmgcode,field_name,"datatype") VALUES
	 (707,502,NULL,'type','string'),
	 (100283,100073,NULL,'number','string');


-- 3. Insert data into PP_PROV_TIN table
INSERT INTO portown.pp_prov_tin (id,name,tin) VALUES
	 (1,'Kaptured Inc','43-5343234');

-- 4. Insert data into PP_PROV_TYPE table
INSERT INTO portown.pp_prov_type (id,"type",category) VALUES
	 (1,'HOSP','Medical');

-- 5. Insert data into PP_SPEC table
INSERT INTO portown.pp_spec (id,"type",description,site_visit_req) VALUES
	 (1,'Multi-Specialty','Multi Specialty Institution','No');

-- 6. Insert data into PP_ADDR table
INSERT INTO portown.pp_addr (id,"type",addr1,addr2,city,state,zip,county,latitude,longitude,start_date,end_date,fips) VALUES
	 (1,'BILLING','13377 Batten Lane',NULL,'Odessa','FL','33556','Pasco',NULL,NULL,'2020-01-01',NULL,'12101'),
	 (2,'MAILING','P.O.8433',NULL,'Odessa','FL','33556','Pasco',NULL,NULL,'2020-01-01',NULL,'12101'),
	 (3,'main','3160 Cedar Ave','Apt 42','Dallas','TX','75203','Dallas County',NULL,NULL,'2019-01-01',NULL,'48113'),
	 (4,'main','4865 Pine Dr','Apt 37','San Antonio','TX','78205','Bexar County',NULL,NULL,'2019-01-01',NULL,'48029'),
	 (5,'main','4611 Main Rd','Suite 913','Dallas','TX','75203','Dallas County',NULL,NULL,'2019-01-01',NULL,'48113'),
	 (6,'main','823 Park Ave','—','Houston','TX','77004','Harris County',NULL,NULL,'2019-01-01',NULL,'48201'),
	 (7,'main','1998 Park Ln','—','Houston','TX','77004','Harris County',NULL,NULL,'2019-01-01',NULL,'48201'),
	 (8,'main','9805 Oak Ave','—','Austin','TX','78701','Travis County',NULL,NULL,'2019-01-01',NULL,'48453'),
	 (9,'main','3064 Lake Dr','Suite 196','Dallas','TX','75201','Dallas County',NULL,NULL,'2019-01-01',NULL,'48113'),
	 (10,'main','3579 Oak Pl','PO Box 187','Dallas','TX','75203','Dallas County',NULL,NULL,'2019-01-01',NULL,'48113');
INSERT INTO portown.pp_addr (id,"type",addr1,addr2,city,state,zip,county,latitude,longitude,start_date,end_date,fips) VALUES
	 (11,'main','361 Elm Blvd','Suite 586','San Antonio','TX','78205','Bexar County',NULL,NULL,'2019-01-01',NULL,'48029'),
	 (12,'main','1201 Cedar Ln','—','Houston','TX','77003','Harris County',NULL,NULL,'2019-01-01',NULL,'48201'),
	 (13,'main','5511 Oak St','Apt 23','Houston','TX','77003','Harris County',NULL,NULL,'2019-01-01',NULL,'48201'),
	 (14,'main','3489 Sunset Pl','Apt 38','San Antonio','TX','78206','Bexar County',NULL,NULL,'2019-01-01',NULL,'48029'),
	 (15,'main','1268 Maple Blvd','PO Box 365','San Antonio','TX','78207','Bexar County',NULL,NULL,'2019-01-01',NULL,'48029'),
	 (16,'main','1591 Sunset Ave','Apt 47','Dallas','TX','75202','Dallas County',NULL,NULL,'2019-01-01',NULL,'48113'),
	 (17,'main','4106 Maple Rd','PO Box 59','Austin','TX','78703','Travis County',NULL,NULL,'2019-01-01',NULL,'48453'),
	 (18,'main','4645 Maple Pl','—','Rockford','IL','61107','Winnebago County',NULL,NULL,'2019-01-01',NULL,'17201'),
	 (19,'main','7665 Elm St','—','Rockford','IL','61108','Winnebago County',NULL,NULL,'2019-01-01',NULL,'17201'),
	 (20,'main','5430 Oak Ave','Suite 718','Springfield','IL','62703','Sangamon County',NULL,NULL,'2019-01-01',NULL,'17167');
INSERT INTO portown.pp_addr (id,"type",addr1,addr2,city,state,zip,county,latitude,longitude,start_date,end_date,fips) VALUES
	 (21,'main','3722 Cedar Pl','—','Peoria','IL','61603','Peoria County',NULL,NULL,'2019-01-01',NULL,'17143'),
	 (22,'main','4139 Maple Rd','Suite 361','Springfield','IL','62702','Sangamon County',NULL,NULL,'2019-01-01',NULL,'17167'),
	 (23,'main','6543 Elm Rd','Suite 510','Rockford','IL','61107','Winnebago County',NULL,NULL,'2019-01-01',NULL,'17201'),
	 (24,'main','5097 Main Rd','Suite 302','Rockford','IL','61107','Winnebago County',NULL,NULL,'2019-01-01',NULL,'17201'),
	 (25,'main','9209 Cedar Ave','PO Box 60','Chicago','IL','60618','Cook County',NULL,NULL,'2019-01-01',NULL,'17031'),
	 (26,'main','406 Pine Dr','PO Box 59','Peoria','IL','61602','Peoria County',NULL,NULL,'2019-01-01',NULL,'17143'),
	 (27,'main','9953 Lake Ave','—','Rockford','IL','61108','Winnebago County',NULL,NULL,'2019-01-01',NULL,'17201'),
	 (28,'main','6397 Oak Ave','Apt 5','Peoria','IL','61603','Peoria County',NULL,NULL,'2019-01-01',NULL,'17143'),
	 (29,'main','3232 Park Dr','Apt 43','Peoria','IL','61604','Peoria County',NULL,NULL,'2019-01-01',NULL,'17143'),
	 (30,'main','4290 Pine St','—','Peoria','IL','61604','Peoria County',NULL,NULL,'2019-01-01',NULL,'17143');
INSERT INTO portown.pp_addr (id,"type",addr1,addr2,city,state,zip,county,latitude,longitude,start_date,end_date,fips) VALUES
	 (31,'main','4377 Elm Ave','Apt 10','Chicago','IL','60618','Cook County',NULL,NULL,'2019-01-01',NULL,'17031'),
	 (32,'main','8439 Main Ln','Suite 702','Peoria','IL','61602','Peoria County',NULL,NULL,'2019-01-01',NULL,'17143'),
	 (33,'main','5791 Hill Rd','—','Macon','GA','31204','Bibb County',NULL,NULL,'2019-01-01',NULL,'13021'),
	 (34,'main','5861 Oak St','—','Macon','GA','31205','Bibb County',NULL,NULL,'2019-01-01',NULL,'13021'),
	 (35,'main','9039 Oak St','Apt 4','Savannah','GA','31404','Chatham County',NULL,NULL,'2019-01-01',NULL,'13051'),
	 (36,'main','3166 Oak Blvd','PO Box 280','Savannah','GA','31401','Chatham County',NULL,NULL,'2019-01-01',NULL,'13051'),
	 (37,'main','9289 Sunset Dr','Suite 472','Savannah','GA','31401','Chatham County',NULL,NULL,'2019-01-01',NULL,'13051'),
	 (38,'main','2205 Park Pl','—','Savannah','GA','31405','Chatham County',NULL,NULL,'2019-01-01',NULL,'13051'),
	 (39,'main','9709 Maple Blvd','Apt 8','Savannah','GA','31404','Chatham County',NULL,NULL,'2019-01-01',NULL,'13051'),
	 (40,'main','5908 Main Dr','Suite 879','Atlanta','GA','30304','Fulton County',NULL,NULL,'2019-01-01',NULL,'13121');
INSERT INTO portown.pp_addr (id,"type",addr1,addr2,city,state,zip,county,latitude,longitude,start_date,end_date,fips) VALUES
	 (41,'main','2861 Hill Rd','—','Augusta','GA','30905','Richmond County',NULL,NULL,'2019-01-01',NULL,'13245'),
	 (42,'main','2011 Maple Rd','Suite 890','Augusta','GA','30901','Richmond County',NULL,NULL,'2019-01-01',NULL,'13245'),
	 (43,'main','3899 Pine St','—','Atlanta','GA','30303','Fulton County',NULL,NULL,'2019-01-01',NULL,'13121'),
	 (44,'main','8189 Sunset Ln','PO Box 144','Savannah','GA','31404','Chatham County',NULL,NULL,'2019-01-01',NULL,'13051'),
	 (45,'main','2811 Main St','Suite 937','Atlanta','GA','30303','Fulton County',NULL,NULL,'2019-01-01',NULL,'13121'),
	 (46,'main','5113 Maple Ln','PO Box 204','Augusta','GA','30904','Richmond County',NULL,NULL,'2019-01-01',NULL,'13245'),
	 (47,'main','2757 Maple Pl','Suite 203','Augusta','GA','30901','Richmond County',NULL,NULL,'2019-01-01',NULL,'13245'),
	 (48,'main','1011 Oak Ave','PO Box 227','San Francisco','CA','94109','San Francisco County',NULL,NULL,'2019-01-01',NULL,'06075'),
	 (49,'main','8502 Cedar Blvd','Apt 40','Los Angeles','CA','90029','Los Angeles County',NULL,NULL,'2019-01-01',NULL,'06037'),
	 (50,'main','9135 Cedar Rd','Apt 25','Sacramento','CA','95814','Sacramento County',NULL,NULL,'2019-01-01',NULL,'06067');
INSERT INTO portown.pp_addr (id,"type",addr1,addr2,city,state,zip,county,latitude,longitude,start_date,end_date,fips) VALUES
	 (51,'main','3329 Lake St','Suite 928','San Francisco','CA','94133','San Francisco County',NULL,NULL,'2019-01-01',NULL,'06075'),
	 (52,'main','8986 Maple Dr','—','Sacramento','CA','95814','Sacramento County',NULL,NULL,'2019-01-01',NULL,'06067'),
	 (53,'main','8539 Main Ave','Suite 924','Sacramento','CA','95816','Sacramento County',NULL,NULL,'2019-01-01',NULL,'06067'),
	 (54,'main','7911 Pine Pl','PO Box 165','Los Angeles','CA','90029','Los Angeles County',NULL,NULL,'2019-01-01',NULL,'06037'),
	 (55,'main','4546 Cedar Dr','Apt 15','Sacramento','CA','95815','Sacramento County',NULL,NULL,'2019-01-01',NULL,'06067'),
	 (56,'main','741 Oak Ave','Apt 6','San Diego','CA','92103','San Diego County',NULL,NULL,'2019-01-01',NULL,'06073'),
	 (57,'main','9949 Lake St','—','San Diego','CA','92101','San Diego County',NULL,NULL,'2019-01-01',NULL,'06073'),
	 (58,'main','3668 Elm Pl','Apt 23','Sacramento','CA','95814','Sacramento County',NULL,NULL,'2019-01-01',NULL,'06067'),
	 (59,'main','4150 Park Rd','Apt 10','San Francisco','CA','94110','San Francisco County',NULL,NULL,'2019-01-01',NULL,'06075'),
	 (60,'main','8700 Main Dr','PO Box 241','Los Angeles','CA','90029','Los Angeles County',NULL,NULL,'2019-01-01',NULL,'06037');
INSERT INTO portown.pp_addr (id,"type",addr1,addr2,city,state,zip,county,latitude,longitude,start_date,end_date,fips) VALUES
	 (61,'main','1606 Hill St','Apt 20','San Francisco','CA','94109','San Francisco County',NULL,NULL,'2019-01-01',NULL,'06075'),
	 (62,'main','8257 Oak Ave','—','Sacramento','CA','95814','Sacramento County',NULL,NULL,'2019-01-01',NULL,'06067');


-- 7. Insert data into PP_PHONES table
INSERT INTO portown.pp_phones (id,"type",area_code,exchange,"number") VALUES
	 (1,'CELL','813','357','9150');


-- 8. Insert data into PP_PROV table
INSERT INTO portown.pp_prov (id,name,tin_id,prov_type_id,address_id,specialty_id) VALUES
	 (1,'Kaptured Hospital',1,1,1,1);

-- 9. Insert data into PP_ADDR_PHONES table
INSERT INTO portown.pp_addr_phones (id,address_id,phone_id) VALUES
	 (1,1,1),
	 (2,2,1);

-- 10. Insert data into PP_PROV_ADDR table
INSERT INTO portown.pp_prov_addr (id,prov_id,address_id) VALUES
	 (1,1,1);

-- 11. Insert data into PP_PROV_ATTRIB table
INSERT INTO portown.pp_prov_attrib (id,prov_id,attribute_id) VALUES
	 (4,1,100640),
	 (5,1,101277),
	 (6,1,100638),
	 (2,1,101278),
	 (1,1,502),
	 (3,1,100073);


-- 12. Insert data into PP_PROV_ATTRIB_VALUES table
INSERT INTO portown.pp_prov_attrib_values (id,prov_attribute_id,field_id,value,value_date,value_number) VALUES
	 (7,4,101143,'Y',NULL,NULL),
	 (8,4,101141,NULL,'2021-05-01',NULL),
	 (9,4,104380,'Breast MRI',NULL,NULL),
	 (10,5,101955,'Y',NULL,NULL),
	 (11,5,101956,NULL,'2022-10-01',NULL),
	 (13,6,101137,NULL,'2018-08-01',NULL),
	 (12,6,101136,'Y',NULL,NULL),
	 (14,6,104381,'Medicare Deemed Status',NULL,NULL),
	 (5,2,101958,'','2020-07-01',NULL),
	 (4,2,101957,'YES',NULL,NULL);
INSERT INTO portown.pp_prov_attrib_values (id,prov_attribute_id,field_id,value,value_date,value_number) VALUES
	 (1,1,706,'235625546',NULL,NULL),
	 (2,1,708,NULL,'2019-01-01',NULL),
	 (3,1,707,'type 1',NULL,NULL),
	 (6,3,100283,'FL34634359',NULL,NULL);

-- 13. Insert data into PP_PROV_TIN_LOC
INSERT INTO portown.pp_prov_tin_loc (id,tin_id,address_id,"name","primary",print_suppress,office_mgr,train,bus,transit_route,handicap,prov_tin_prc_cont_id) VALUES
	 (1,1,3,'Lone Star Family Health Center','N','N','Tim Miller','N',NULL,NULL,NULL,NULL),
	 (2,1,4,'Bluebonnet Community Clinic','N','N','Sam Stein','N',NULL,NULL,NULL,NULL),
	 (3,1,5,'North Texas Regional Medical Center','N','N','John Last','N',NULL,NULL,NULL,NULL),
	 (4,1,6,'Rio Grande Valley Children’s Hospital','N','N','David Thompson','N',NULL,NULL,NULL,NULL),
	 (5,1,7,'Hill Country Wellness Center','N','N','Sarah Longwell','N',NULL,NULL,NULL,NULL);

-- 14. Insert data into PP_PROV_LOC
INSERT INTO portown.pp_prov_loc (prov_id,loc_id,name_usage,"primary",start_date,end_date,print_supress) VALUES
	 (1,1,NULL,'N',NULL,NULL,NULL),
	 (1,2,NULL,'N',NULL,NULL,NULL),
	 (1,3,NULL,'Y',NULL,NULL,NULL),
	 (1,4,NULL,'N',NULL,NULL,NULL),
	 (1,5,NULL,'N',NULL,NULL,NULL);

-- 15. Insert data into PP_PROV_NET_CYCLE
INSERT INTO portown.pp_prov_net_cycle (id,prov_id,net_id,status,start_date,end_date) VALUES
	 (1,1,3258,'PAR','2001-06-01','4000-01-01'),
	 (2,1,7723,'PAR','2005-01-01','2018-12-31'),
	 (3,1,7723,'PAR','2020-01-01','4000-01-01'),
	 (4,1,14694,'PAR','2015-01-01','4000-01-01');

-- 16. Insert data into PP_PROV_NET_LOC_CYCLE
INSERT INTO portown.pp_prov_net_loc_cycle (id,prov_net_cycle_id,prov_id,loc_id,start_date,end_date,"primary") VALUES
	 (1,1,1,1,'2001-06-01','2010-10-31','N'),
	 (2,1,1,1,'2011-07-01','4000-01-01','Y'),
	 (3,1,1,2,'2015-08-01','4000-01-01','N'),
	 (4,2,1,3,'2005-01-01','2018-12-31','N'),
	 (5,3,1,4,'2020-01-01','4000-01-01','N'),
	 (6,4,1,5,'2015-01-01','4000-01-01','N'),
	 (7,4,1,4,'2020-01-01','4000-01-01','N');




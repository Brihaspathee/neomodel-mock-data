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

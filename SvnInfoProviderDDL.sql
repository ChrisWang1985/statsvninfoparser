drop table if exists svn_project_info;
-- 项目表, 用于记录每个项目的名称, 隶属哪个产品, 以及svn地址
create table svn_project_info(
	id int(11) not null PRIMARY KEY auto_increment,
	projectName varchar(255) not null,
	svnUrl varchar(511) not null,
	productName varchar(255) not NULL,
	insertTime varchar(50) not NULL
);

drop table if exists svn_project_summary_info;
-- 项目svn数据汇总表,用于记录index.html的汇总表格信息
create table svn_project_summary_info(
	id int(11) not null PRIMARY KEY auto_increment,
	projectId int(11) not null,
	projectSvnName varchar(255) not null,
	reportGenTime varchar(50) not null,
	headRevision varchar(11) not null,
	reportPeriodStartTime varchar(50) not null,
	reportPeriodEndTime VARCHAR(50) not null,
	totalFiles int not null,
	lineOfCodes LONG not null,
	insertTime varchar(50) not NULL
);

drop table if exists svn_project_dev_summary_info;
-- 项目研发数据汇总表, 用于记录项目关联研发的代码量数据
create table svn_project_dev_summary_info(
	id int(11) not null PRIMARY KEY auto_increment,
	projectId int(11) not null,
	authorId varchar(30) not null,
	author varchar(50) not null,
	loc varchar(50) not null,
	changes varchar(50) not null,
	lpc varchar(30) not null,
	monthlyCodeInfoId int(11) not null,
	insertTime varchar(50) not NULL
);

drop table if exists svn_project_dev_monthly_code_info;
-- 项目研发代码量明细表, 用于记录最近12个月及12个月之前贡献给该项目的代码量
create table svn_project_dev_monthly_code_info(
	id int(11) not null primary key auto_increment,
	projectId int(11) not null,
	author varchar(50) not null,
	last1MonthCode varchar(50) not null,
	last2MonthCode varchar(50) not null,
	last3MonthCode varchar(50) not null,
	last4MonthCode varchar(50) not null,
	last5MonthCode varchar(50) not null,
	last6MonthCode varchar(50) not null,
	last7MonthCode varchar(50) not null,
	last8MonthCode varchar(50) not null,
	last9MonthCode varchar(50) not null,
	last10MonthCode varchar(50) not null,
	last11MonthCode varchar(50) not null,
	last12MonthCode varchar(50) not null,
	previousYearsCode varchar(50) not null,
	insertTime varchar(50) not NULL
);

drop table if exists svn_project_file_summary_info;
-- 项目文件信息汇总表, 用于记录svn上该项目关联文件的汇总信息
create table svn_project_file_summary_info(
	id int(11) not null primary key auto_increment,
	projectId int(11) not null,
	totalFiles int(11) not null,
	avgFileSize VARCHAR(50) not null,
	avgRevisionPerFile VARCHAR(30) not null,
	insertTime varchar(50) not NULL
);

drop table if exists svn_project_file_types_info;
-- 项目文件类型表, 用于记录该项目中svn上的文件名, 每个文件的类型, 文件的代码量, 平均代码行数
create table svn_project_file_types_info(
	id int(11) not null primary key auto_increment,
	projectId int(11) not null,
	files VARCHAR(50) not null,
	loc VARCHAR(50) not null,
	type varchar(50) not null,
	locPerFile VARCHAR(50) not null,
	insertTime varchar(50) not NULL
);

drop table if exists svn_project_large_file_info;
-- 项目大文件信息表, 用于记录大型文件的代码行数与文件名
create table svn_project_large_file_info(
	id int(11) not null primary key auto_increment,
	projectId int(11) not null,
	loc VARCHAR(30) not null,
	`file` VARCHAR(511) not null,
	insertTime varchar(50) not NULL
);

drop table if exists svn_project_file_with_most_revisions_info;
-- 项目文件最多版本表,用于记录被修改最多的文件
create table svn_project_file_with_most_revisions_info(
	id int(11) not null primary key auto_increment,
	projectId int(11) not null,
	`file` VARCHAR(511) not null,
	revisions VARCHAR(30) not null,
	insertTime varchar(50) not NULL
);

drop table if exists svn_project_dir_summary_info;
-- 项目目录汇总表
create table svn_project_dir_summary_info(
	id int(11) not null primary key auto_increment,
	projectId int(11) not null,
	loc VARCHAR(50) not null,
	`change` VARCHAR(50) not null,
	dir VARCHAR(255) not NULL,
	insertTime varchar(50) not NULL
);
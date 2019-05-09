#!/bin/bash/env python 
#Devops Account Mismatch Tool
#Requires Panda module pip install pandas
import pandas as pd 
import argparse

parser=argparse.ArgumentParser(description='Processes Two CSV files obtained via the DevOps portal lookups and process them for inconsistency. Which leads to failure to users sync',
version='0.9 Demo Version', usage='main2.py [-h] help [-v] version dbfile lefile')
parser.add_argument('dbuserfile',help="DB users file taken from DevOps")
parser.add_argument('leuserfile', help="LE users file taken from DevOps")
args = parser.parse_args()

dbuserfile = args.dbuserfile
leuserfile = args.leuserfile

def getData():
	global combine
	global dbusers
	global leusers
	dbusers = pd.read_csv(dbuserfile)
	leusers = pd.read_csv(leuserfile)
	dbusers = dbusers[pd.notnull(dbusers['roles'])]
	#Drop useless pieces of info
	leusers=leusers.drop(leusers[leusers.email=='chatbot@liveassistfor365.com'].index)
	leusers=leusers.drop(leusers[leusers.isEnabled==False].index)
	#combine the tables
	combine = dbusers.merge(leusers, left_on='loginName', right_on='email')
	#create combined table ocntianing needed values
	#print combine.loc[:, ["loginName_x", "roles", "permissionGroups"]]

def checkRoles(combine):
	#loop through above table
	for index, row in combine.iterrows():
	#if Adminsitrator however not got lp admin group then
		if (len(combine.at[index, 'roles']) == 34) & (combine.at[index, 'permissionGroups'] != '[0]'):
			print ('Invalid Roles: ' +  combine.at[index, 'loginName_x'] + ' LP :'+ combine.at[index,'permissionGroups'] + ' Roles: ' + combine.at[index, 'roles'])
	#if Supervisor but only not supervisor lp role group
		elif (len(combine.at[index, 'roles']) == 19) & (combine.at[index, 'permissionGroups'] !='[2]'):
			print ('Invalid Roles: ' +  combine.at[index, 'loginName_x'] + ' LP :'+ combine.at[index,'permissionGroups'] + ' Roles: ' + combine.at[index, 'roles'])
		else:
			pass
				
def checkLEusers():
	#Merge tables to create new table
	leRoleTable = dbusers.merge(leusers, left_on='loginName', right_on='email')
	#print leRoleTable.loc[:, ["loginName_x", "roles", "permissionGroups", 'isEnabled']]
	for index, row in leRoleTable.iterrows():
	#if you have le group [0][1][2] but no roles in DB users then show me.
		if (leRoleTable.at[index, 'permissionGroups'] == '[0]' or '[1]' or '[2]') and (str(leRoleTable.at[index, 'roles']) == 'nan'):
			print (leRoleTable.at[index, 'loginName_x'] + ' has bank roles however permission Group shows ' + leRoleTable.at[index, 'permissionGroups'])
		else:
			pass
		
getData()
checkRoles(combine)
checkLEusers()

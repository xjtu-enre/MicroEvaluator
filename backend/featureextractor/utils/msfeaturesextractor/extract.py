import os
import csv

FILEPATH = 'C:\\Users\\20465\\Desktop\\data\\projectMessage.csv'
NEW_FILEPATH_V3 = 'C:\\Users\\20465\\Desktop\\data\\projectMessage_new_v3.csv'
NEW_FILEPATH_V4 = 'C:\\Users\\20465\\Desktop\\data\\projectMessage_new_v4.csv'
PROJECTS = 'C:\\Users\\20465\\Desktop\\data\\projectMessage_new_v4.csv'
API_NAMES = ['controller']


def get_services():
	# 遍历当前目录gitcodes下的每一个文件夹，分析其代码结构，提取每个项目的微服务名
	results = []
	with open(FILEPATH, 'r') as f:
		reader = csv.reader(f)
		header = next(reader)
		for line in reader:
			servicesname = [] 
			servicesurl = []
			apiurls = []
			for dir, subdir, file_name_list in os.walk(line[3]):
				if 'src' in subdir and 'main' in os.listdir(dir + '\\src') and 'test' in os.listdir(dir + '\\src'):
					# apiurls.append(get_api_url(dir))
					# servicesurl.append(dir)
					length = len(dir.split('\\'))
					servicename = dir.split('\\')[length-1]
					servicesname.append(servicename)
			line[4] = ';'.join(servicesname)
			# line.insert(5, ';'.join(servicesurl))
			# line.insert(6, ';'.join(apiurls))
			results.append(line)
	print(results)
	
	with open(NEW_FILEPATH_V1, 'w', encoding='utf_8_sig', newline='') as f:
		csv_write = csv.writer(f)
		csv_head = ["projectName", "description", "giturl", "downloadurl", "servicesname", "servicesurl", "language", "loc", "sumloc", "star", "fork", "tags", "createTime", "lastupdateTime"]
		csv_write.writerow(csv_head)
		for line in results:
			csv_write.writerow(line)
	f.close()


def get_scs_url():
	results = []
	with open(FILEPATH, 'r') as f:
		reader = csv.reader(f)
		header = next(reader)
		for line in reader:
			servicesurl = []
			project_url = line[3]
			services_name = line[4]
			names = services_name.split(';')
			for name in names:
				for dir, subdir, file_name_list in os.walk(project_url):
					if name in subdir:
						servicesurl.append(dir + '\\' + name)
			line.insert(5, ';'.join(servicesurl))
			results.append(line)

	with open(NEW_FILEPATH_V3, 'w', encoding='utf_8_sig', newline='') as f:
		csv_write = csv.writer(f)
		csv_head = ["projectName", "description", "giturl", "downloadurl", "servicesname", "servicesurl", "apiurls", "language", "loc", "sumloc", "star", "fork", "tags", "createTime", "lastupdateTime"]
		csv_write.writerow(csv_head)
		for line in results:
			csv_write.writerow(line)
	f.close()


def get_api_url(project_url, services):
	service = services.split(',')
	apiurl = []
	for sc in service:
		servicepath = project_url + '\\' + sc
		for dir, subdir, file_name_list in os.walk(servicepath + '\\src\\main\\java'):
			for item in API_NAMES:
				if item in subdir:
					apiurl.append(os.path.join(dir, item))
	print(','.join(apiurl))
	return ','.join(apiurl)


if __name__ == '__main__':
	get_api_url(r'C:\Users\20465\Desktop\data\versiondata\train-ticket', 'ts-assurance-service,ts-auth-service,ts-preserve-other-service,ts-food-map-service,ts-preserve-service,ts-security-service,ts-ticketinfo-service,ts-train-service,ts-seat-service,ts-inside-payment-service,ts-admin-route-service,ts-cancel-service,ts-route-plan-service,ts-user-service,ts-order-other-service,ts-admin-order-service,ts-consign-service,ts-order-service,ts-execute-service,ts-price-service,ts-travel2-service,ts-notification-service,ts-payment-service,ts-station-service,ts-basic-service,ts-travel-plan-service,ts-admin-user-service,ts-admin-basic-info-service,ts-admin-travel-service,ts-rebook-service,ts-food-service,ts-travel-service,ts-route-service,ts-contacts-service,ts-consign-price-service,ts-config-service,ts-verification-code-service')


def get_apis():
	results = []
	with open(NEW_FILEPATH_V3, 'r') as f:
		reader = csv.reader(f)
		header = next(reader)
		for line in reader:
			apisurl = []
			services_url = line[5]
			urls = services_url.split(';')
			for url in urls:
				apisurl.append(get_api_url(url))
			line.insert(6, ';'.join(apisurl))
			results.append(line)

	with open(NEW_FILEPATH_V4, 'w', encoding='utf_8_sig', newline='') as f:
		csv_write = csv.writer(f)
		csv_head = ["projectName", "description", "giturl", "downloadurl", "servicesname", "servicesurl", "apiurls", "language", "loc", "sumloc", "star", "fork", "tags", "createTime", "lastupdateTime"]
		csv_write.writerow(csv_head)
		for line in results:
			csv_write.writerow(line)
	f.close()


# get_services()
# get_scs_url()
# get_apis()
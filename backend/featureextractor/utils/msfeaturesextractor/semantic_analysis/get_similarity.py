import os
import os.path
import javalang
import csv
import nltk
from nltk.stem import SnowballStemmer
from collections import defaultdict
from gensim import models, corpora, similarities
# from evaluator.const import project_const

# SERVICES_NAME = ['ts-admin-basic-info-service', 'ts-admin-order-service', 'ts-admin-route-service', 'ts-admin-travel-service', 'ts-admin-user-service', 'ts-assurance-service', 'ts-auth-service', 'ts-basic-service', 'ts-cancel-service', 'ts-common', 'ts-config-service', 'ts-consign-price-service', 'ts-consign-service', 'ts-contacts-service', 'ts-execute-service', 'ts-food-map-service', 'ts-food-service', 'ts-inside-payment-service', 'ts-news-service', 'ts-notification-service', 'ts-order-other-service', 'ts-order-service', 'ts-payment-service', 'ts-preserve-other-service', 'ts-preserve-service', 'ts-price-service', 'ts-rebook-service', 'ts-route-plan-service', 'ts-route-service', 'ts-seat-service', 'ts-security-service', 'ts-station-service', 'ts-ticket-office-service', 'ts-ticketinfo-service', 'ts-train-service', 'ts-travel-plan-service', 'ts-travel-service', 'ts-travel2-service', 'ts-ui-dashboard', 'ts-user-service', 'ts-verification-code-service', 'ts-voucher-service']
PROJECTMESSAGE_NEW_V4 = 'C:\\Users\\20465\\Desktop\\data\\projectMessage_new_v4.csv'


def main():
    # 根据前面收集数据集的代码处理后，存储了项目在本地的路径以及每个项目下的微服务名，此处进行读取使用
    projecturl_servicesurl = get_projectpath_and_servicesurl()
    print(projecturl_servicesurl)
    # 遍历每个项目计算每个项目的相似度文件
    for projectpath in projecturl_servicesurl:
        # print(projectpath)
        # 遍历项目路径下每个微服务，并获取各微服务内java文件路径及其包名
        if os.path.exists(projectpath):
            filepaths = []
            packagenames = []
            for service in projecturl_servicesurl[projectpath].split(';'):
                servicebasepath = service
                # print(servicebasepath)
                # 1、获取该微服务下所有java文件路径和其对应的包名
                temp_fileaths, temp_packages = get_all_path(servicebasepath)
                filepaths.extend(temp_fileaths)
                packagenames.extend(temp_packages)
            # print('filepaths', filepaths)
            # print('packagenames', packagenames)
            if len(filepaths) != 0:
                # 2、获取每个java文件的标识符集合
                identifierlist = get_identifier(filepaths)
                # print(len(identifierlist))
                # 3、进行文本分析以及相似度计算。参数2为选择词干提取器(1、思诺博词干提取器（中庸）  2、波特词干提取器（宽松）  3、朗卡斯特词干提取器（严格）)
                similaritiesList = text_analysis(identifierlist, 3)
                # # print(similaritiesList)
                # # dictsim[servicebasepath] = similaritiesList
                # 4、输出相似度到文件
                # print(similaritiesList)
                output2CSV(similaritiesList, projectpath, packagenames)

def get_projectpath_and_servicesurl():
    projecturl_servicesurl = {}
    with open(PROJECTMESSAGE_NEW_V4, 'r') as f:
        reader = csv.reader(f)
        # 去除第一行
        header = next(reader)
        for line in reader:
            projecturl_servicesurl[line[3]] = line[5]
    return projecturl_servicesurl


def get_all_path(servicebasepath):
    # 获取sevice下的main和test路径
    javapaths = get_src_path(servicebasepath)
    filter = ['.java']
    filepaths = []
    packagenames = []

    for dir, subdir, file_name_list in os.walk(servicebasepath):
        for filename in file_name_list:
            # 加入\\?\解决因为某些文件名过长而导致无法打来文件的问题
            filepath = os.path.join('\\\?\\' + dir, filename)
            ext = os.path.splitext(filepath)[1]
            if ext in filter:
                filepaths.append(filepath)
                packagenames.append(get_package_name(filepath, javapaths))
    return filepaths, packagenames     


def get_src_path(servicebasepath):
    result = []
    for root1, dirs1, files1 in os.walk(servicebasepath):
        if 'src' in dirs1:
            for root2, dirs2, files2 in os.walk(os.path.join(root1, 'src')):
                if root2 == os.path.join(root1, 'src\\main\\java'):
                    result.append('\\\?\\' + root2)
                elif root2 == os.path.join(root1, 'src\\test\\java'):
                    result.append('\\\?\\' + root2)           
    return result


def get_identifier(filepaths):
    result = []
    for filepath in filepaths:
        # 将源代码读入
        programfile = open(filepath, encoding='utf-8')
        programtext = programfile.read()
        # 生成token
        programtoken = list(javalang.tokenizer.tokenize(programtext))
        # for item in programtoken:
        #     print(item)
        # 过滤token中的Identifier
        temp_token = [token.value for token in programtoken if isinstance(token, javalang.tokenizer.Identifier)]
        result.append(' '.join('%s' %id for id in temp_token))
        programfile.close()
    # print(result)
    return result


def text_analysis(identifierlist, chooseid):
    # print(identifiersNew)
    # 处理_
    texts = handle_underline(identifierlist)
    # print('____', texts, '\n')
    # 处理驼峰
    texts = handle_hump(texts)
    # print('hump', texts)
    # 读取java停用词文件
    java_stop_words = get_java_stopwords('../../data/javastopwords.txt')
    # print(java_stop_words)
    # 去掉停用词
    identifiers_new = [[word for word in text if word not in java_stop_words] for text in texts]
    # print(identifiers_new)
    # 词干提取
    if chooseid == 1:
        stemmer = SnowballStemmer('english')
    elif chooseid == 2:
        stemmer = nltk.PorterStemmer()  #偏宽松
    elif chooseid == 3:
        stemmer = nltk.LancasterStemmer()   #偏严格
    texts=[[stemmer.stem(t) for t in sentence] for sentence in identifiers_new]
    # print(texts)
    # 统计词频,去除只出现1次的单词
    texts = get_frequency(texts)
    # for text in texts:
    #     print(text)
    # 词典：列出所有单词，把所有单词取一个set，并对set中每一个单词分配一个id号的map
    dictionary = corpora.Dictionary(texts) 
    # write_to_txt('./dictionary.txt', dictionary.token2id) 
    print(len(dictionary.token2id))
    # 生成每篇文档对应的词袋向量 => list of (token_id, token_count)
    corpus = [dictionary.doc2bow(text) for text in texts] 
    # print(len(corpus))
    # write_to_txt('./corpus.txt', corpus) 
    # 生成tf-idf模型
    tfidf_model = models.TfidfModel(corpus) 
    # 对整个语料库进行加权计算：TF-IDF会将权重过低的词语过滤掉（因为TF-IDF认为TF越大，IDF越大（即在其他文档中出现的次数越少），则该此条具有较好的分类功能）
    corpus_tfidf = tfidf_model[corpus]
    # with open('./corpus_tfidf.txt', 'w') as f:
    #     for doc in corpus_tfidf:
    #         f.write(str(doc))
    #     #     write_to_txt('./corpus_lsi.txt', doc) 
    #         # print(doc)
    #     f.close()
    #     # write_to_txt('./corpus_tfidf.txt', doc) 
    # 利用LSI模型进行整个语料库的主题提取,即降维
    # LSI：浅语义分析算法,总的来讲就是把一个语料库中的文本编号作为列,语料库中出现的各个词作为行来形成一个矩阵，矩阵中的第i行第j列的值就是第j个文本第i个词所被赋予的tf-idf权值
    if len(dictionary.token2id) < 200:
        num_topics = 50
    else:
        num_topics = 200
    lsi_model = models.LsiModel(corpus_tfidf, id2word = dictionary, num_topics = num_topics)
    corpus_lsi = lsi_model[corpus_tfidf] 
    # with open('./corpus_lsi.txt', 'w') as f:
    #     for doc in corpus_lsi:
    #         f.write(str(doc))
    #     #     write_to_txt('./corpus_lsi.txt', doc) 
    #         # print(doc)
    #     f.close()
    # 计算相似度
    num_features = len(dictionary.token2id.keys())
    # print(num_features)
    index = similarities.MatrixSimilarity(lsi_model[corpus_tfidf], num_features = num_features)
    # 利用搜索词与文本集进行对比，得出每个文本间的相似度
    similarities_list=[]
    for onecorpusTf in corpus_lsi:
        similarities_list.append(index[onecorpusTf])
    # print(similarities_list)
    # write_to_txt('./similarities.txt', similarities_list) 
    
    return similarities_list

# def write_to_txt(filepath, context):
#     f = open(filepath, 'w')
#     f.write(str(context))
#     f.close()


def get_java_stopwords(filepath):
    stopwords = []
    f = open(filepath)
    # print(type(f.read()))
    for line in f.readlines():
        line = line.strip('\n')
        stopwords.append(line)
    return stopwords


def handle_underline(identifierslist):
    result_texts = []
    for identifiers in identifierslist:
        temp = []
        for word in identifiers.split(' '):
            temp.extend([i for i in word.split("_") if len(i)>0])
        result_texts.append(temp)
    return result_texts


def handle_hump(texts):
    result = []
    for text in texts:
        temptext = []
        for word in text:
            temptext.extend(split_camel_case(word))
        result.append(temptext)
    return result


def get_frequency(texts):
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1
    texts = [[token for token in text if frequency[token] > 1]for text in texts]
    return texts


def output2CSV(similarities, projectpath, packagenames):
    filepath = projectpath + '\\concerndep.csv'
    with open(filepath, 'w', newline='') as f:
        csv_write= csv.writer(f)
        # csv_head = ["file1","file2","count"]
        # csv_write.writerow(csv_head)
        dict={}
        # for servicebasepath in servicesimilarities:
        for i in range(len(similarities)):
            for j in range(i + 1, len(similarities[i])):
                if similarities[i][j] > 0.40:
                    # print(similarities[i][j])
                    # print(packagenames[i])
                    # print(packagenames[j])
                    dict[(packagenames[i],packagenames[j])]=similarities[i][j]
        for key in dict:
            csv_write.writerow((key[0], key[1], dict[key]))
    f.close()


def get_package_name(filepath, javapaths):
    for javapath in javapaths:
        if javapath in filepath:
            packagename = filepath[len(javapath):].replace('\\', '.')
            return packagename[1:len(packagename)-5]


def split_camel_case(string):
    tokens = []
    token = []
    for prev, char, next in zip(' ' + string, string, string[1:] + ' '):
        if is_camel_case_boundary(prev, char, next):
            if token:
                tokens.append(''.join(token))
            token = [char]
        else:
            token.append(char)
    if token:
        tokens.append(''.join(token))
    return tokens


def is_camel_case_boundary(prev, char, next):
    if prev.isdigit():
        return not char.isdigit()
    if char.isupper():
        return next.islower() or prev.isalpha() and not prev.isupper()
    return char.isdigit()

main()

# print(split_camel_case('LAOOGER'))